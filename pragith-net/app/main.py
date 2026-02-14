from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from urllib.parse import quote
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.services.blog_loader import blog_service
from app.services.mailer import mailer_service
from app.services.sitemap import sitemap_service
from app.services.offering_loader import offering_service
from app.services.marketing_loader import marketing_service
from app.services.navigation_loader import navigation_service
from app.services.currency import convert_rate

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=None, # Disable Swagger UI in prod
    redoc_url=None
)

# Rate Limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google.com https://www.gstatic.com https://www.clarity.ms https://scripts.clarity.ms; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https://www.clarity.ms https://c.clarity.ms; "
            "frame-src https://www.google.com https://calendly.com; "
            "connect-src 'self' https://www.google-analytics.com https://www.googletagmanager.com https://www.clarity.ms https://c.clarity.ms https://b.clarity.ms; "
            "worker-src 'self' blob:"
        )
        return response

app.add_middleware(SecurityHeadersMiddleware)

# Static & Templates (use absolute paths so app works from any CWD)
from pathlib import Path
_APP_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=str(_APP_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(_APP_DIR / "templates"))

from datetime import datetime
templates.env.globals["now"] = datetime.now

# Initialize Theme Service
from app.themes import ThemeService
theme_service = ThemeService(settings.THEME)
templates.env.globals["theme"] = theme_service
templates.env.globals["show_products"] = settings.SHOW_PRODUCTS
templates.env.globals["ga_tag"] = settings.GA_TAG
templates.env.globals["clarity_project_id"] = settings.CLARITY_PROJECT_ID
templates.env.globals["recaptcha_site_key"] = settings.RECAPTCHA_SITE_KEY
templates.env.globals["marketing_config"] = marketing_service.get_client_config()
templates.env.globals["navigation_config"] = navigation_service.get_client_config()
templates.env.globals["nav_mode"] = settings.NAV_MODE
templates.env.globals["nav_offset_top"] = settings.NAV_OFFSET_TOP
templates.env.globals["nav_offset_left"] = settings.NAV_OFFSET_LEFT
templates.env.globals["nav_left_width"] = settings.NAV_LEFT_WIDTH


def _contact_meta(project_type: str = "", ref_page: str = "", cta_id: str = "") -> dict:
    signal = " ".join([
        (project_type or "").strip().lower(),
        (ref_page or "").strip().lower(),
        (cta_id or "").strip().lower(),
    ])

    title = "Start Your Project"
    subtitle = "Share your goals, current systems, and delivery timeline."

    if "dashboard" in signal:
        title = "Discuss Dashboard System"
        subtitle = "Share KPI priorities, data sources, and reporting goals."
    elif "training" in signal:
        title = "Request Corporate Training"
        subtitle = "Qualified intake for enterprise AI and data training engagements."
    elif "keynote" in signal or "speaking" in signal:
        title = "Discuss Speaking Engagement"
        subtitle = "Share event format, audience, and outcomes to scope the right session."
    elif "voice receptionist" in signal:
        title = "Discuss Voice Receptionist System"
        subtitle = "Share call flow, routing rules, and handover expectations."
    elif "booking" in signal:
        title = "Discuss Booking Automation System"
        subtitle = "Share booking flow, constraints, and operational requirements."
    elif "whatsapp" in signal:
        title = "Discuss WhatsApp Automation System"
        subtitle = "Share lead flow, response logic, and workflow requirements."
    elif "automation" in signal:
        title = "Discuss Automation System"
        subtitle = "Share the workflow you want to automate and expected outcomes."

    return {"title": title, "subtitle": subtitle}

# Context Processor for common variables
@app.middleware("http")
async def add_context(request: Request, call_next):
    # Inject GA_TAG into request state so templates can access it
    request.state.ga_tag = settings.GA_TAG
    return await call_next(request)

# Routes

@app.get("/theme.css", include_in_schema=False)
async def theme_css():
    return Response(content=theme_service.css, media_type="text/css")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse(url="/static/favicon.ico", status_code=301)

@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap():
    """Generate and serve XML sitemap."""
    # Reset and rebuild sitemap
    sitemap_service._urls = []
    sitemap_service.generate_static_urls()
    sitemap_service.add_blog_posts(blog_service.get_all())
    
    from app.services.work_loader import work_service
    sitemap_service.add_work_items(work_service.get_all())
    sitemap_service.add_offerings(offering_service.get_all())
    
    xml_content = sitemap_service.generate_xml()
    return Response(content=xml_content, media_type="application/xml")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    ip_address = _get_client_ip(request)
    local_rate, currency_code, currency_symbol = await convert_rate(1.0, ip_address)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "ga_tag": settings.GA_TAG,
        "currency_code": currency_code,
        "currency_symbol": currency_symbol,
        "currency_rate": local_rate,
        "hourly_rate_usd": 95.0,
    })

@app.get("/solutions", response_class=HTMLResponse)
async def solutions(request: Request):
    return templates.TemplateResponse("solutions.html", {"request": request})


@app.get("/live-demos", response_class=HTMLResponse)
async def live_demos(request: Request):
    demo_status = request.query_params.get("demo", "").strip()
    return templates.TemplateResponse("live_demos.html", {"request": request, "demo_status": demo_status})


@app.get("/engagement", response_class=HTMLResponse)
async def engagement(request: Request):
    return templates.TemplateResponse("engagement.html", {"request": request})

from app.services.work_loader import work_service

@app.get("/work", response_class=HTMLResponse)
async def work(request: Request):
    works = work_service.get_all()
    return templates.TemplateResponse("work.html", {"request": request, "works": works})



@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/build", response_class=RedirectResponse)
async def build_page(request: Request):
    return RedirectResponse(url="/engagement", status_code=301)

@app.get("/stack", response_class=HTMLResponse)
async def stack(request: Request):
    return templates.TemplateResponse("stack.html", {"request": request})


from typing import Optional

@app.get("/writing", response_class=HTMLResponse)
async def writing_list(request: Request, year: Optional[int] = None):
    all_posts = blog_service.get_all()
    
    # Extract years
    years = sorted(list(set([p.date.year for p in all_posts])), reverse=True)
    current_year = datetime.now().year
    
    # Default to current year if not specified
    selected_year = year if year else current_year
    
    # Filter posts
    posts = [p for p in all_posts if p.date.year == selected_year]
    
    return templates.TemplateResponse("blog_list.html", {
        "request": request, 
        "posts": posts, 
        "years": years, 
        "selected_year": selected_year,
        "current_year": current_year
    })

@app.get("/writing/tag/{tag}", response_class=HTMLResponse)
async def writing_tag(request: Request, tag: str):
    posts = blog_service.get_by_tag(tag)
    return templates.TemplateResponse("blog_list.html", {"request": request, "posts": posts, "tag": tag})

@app.get("/writing/{slug}", response_class=HTMLResponse)
async def writing_detail(request: Request, slug: str):
    post = blog_service.get_by_slug(slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("blog_detail.html", {"request": request, "post": post})

@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    q = request.query_params

    form_defaults = {
        "name": q.get("name", ""),
        "email": q.get("email", ""),
        "company": q.get("company", ""),
        "timeline": q.get("timeline", ""),
        "what_do_you_need_built": q.get("what_do_you_need_built", ""),
        "budget_range": q.get("budget_range", ""),
        "utm_source": q.get("utm_source", ""),
        "utm_medium": q.get("utm_medium", ""),
        "utm_campaign": q.get("utm_campaign", ""),
        "utm_content": q.get("utm_content", ""),
        "ref_page": q.get("ref_page", ""),
        "cta_id": q.get("cta_id", ""),
    }
    contact_meta = _contact_meta()

    return templates.TemplateResponse("contact.html", {
        "request": request,
        "ga_tag": settings.GA_TAG,
        "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
        "calendly_url": settings.CALENDLY_URL,
        "form": form_defaults,
        "contact_meta": contact_meta,
    })


@app.post("/contact", response_class=HTMLResponse)
@limiter.limit("5/minute")
async def contact_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    company: str = Form(""),
    timeline: str = Form(""),
    what_do_you_need_built: str = Form(""),
    budget_range: str = Form(""),
    utm_source: str = Form(""),
    utm_medium: str = Form(""),
    utm_campaign: str = Form(""),
    utm_content: str = Form(""),
    ref_page: str = Form(""),
    cta_id: str = Form(""),
    website: str = Form(""),
    recaptcha_response: str = Form(alias="g-recaptcha-response", default="")
):
    # Honeypot check  -  bots fill hidden fields
    if website:
        return RedirectResponse("/contact", status_code=303)

    if settings.RECAPTCHA_SECRET_KEY and not mailer_service.verify_recaptcha(recaptcha_response):
        contact_meta = _contact_meta(ref_page=ref_page, cta_id=cta_id)
        return templates.TemplateResponse(
            "contact.html",
            {
                "request": request,
                "error": "reCAPTCHA verification failed. Please try again.",
                "form": {
                    "name": name,
                    "email": email,
                    "company": company,
                    "timeline": timeline,
                    "what_do_you_need_built": what_do_you_need_built,
                    "budget_range": budget_range,
                    "utm_source": utm_source,
                    "utm_medium": utm_medium,
                    "utm_campaign": utm_campaign,
                    "utm_content": utm_content,
                    "ref_page": ref_page,
                    "cta_id": cta_id,
                },
                "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
                "contact_meta": contact_meta,
            },
        )
    
    enriched_message = what_do_you_need_built
    metadata = []
    if company:
        metadata.append(f"Company: {company}")
    if timeline:
        metadata.append(f"Timeline: {timeline}")
    if budget_range:
        metadata.append(f"Budget Range: {budget_range}")
    if ref_page:
        metadata.append(f"Ref Page: {ref_page}")
    if cta_id:
        metadata.append(f"CTA ID: {cta_id}")
    if utm_source or utm_medium or utm_campaign or utm_content:
        metadata.append(
            f"UTM: source={utm_source or '-'} medium={utm_medium or '-'} campaign={utm_campaign or '-'} content={utm_content or '-'}"
        )
    if metadata:
        enriched_message = f"{what_do_you_need_built}\n\n---\n" + "\n".join(metadata)

    success = mailer_service.send_contact_email(name, email, "New Intake Form Submission", enriched_message)

    if success:
        return templates.TemplateResponse("contact_success.html", {"request": request})
    else:
        return templates.TemplateResponse("contact.html", {
            "request": request, 
            "error": "Failed to send message. Please try again later.",
            "form": {
                "name": name,
                "email": email,
                "company": company,
                "timeline": timeline,
                "what_do_you_need_built": what_do_you_need_built,
                "budget_range": budget_range,
                "utm_source": utm_source,
                "utm_medium": utm_medium,
                "utm_campaign": utm_campaign,
                "utm_content": utm_content,
                "ref_page": ref_page,
                "cta_id": cta_id,
            },
            "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
        })


@app.get("/faq", response_class=HTMLResponse)
async def faq(request: Request):
    ip_address = _get_client_ip(request)
    local_rate, currency_code, currency_symbol = await convert_rate(1.0, ip_address)
    return templates.TemplateResponse("faq.html", {
        "request": request,
        "currency_code": currency_code,
        "currency_symbol": currency_symbol,
        "currency_rate": local_rate,
        "hourly_rate_usd": 95.0,
    })

@app.get("/legal", response_class=HTMLResponse)
async def legal(request: Request):
    return templates.TemplateResponse("legal.html", {"request": request})

@app.get("/privacy", response_class=HTMLResponse)
async def privacy(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})

# Business Section
@app.get("/business", response_class=HTMLResponse)
@app.get("/business/", response_class=HTMLResponse)
async def business_home(request: Request):
    return templates.TemplateResponse("business/index.html", {"request": request})

@app.get("/business/dashboards", response_class=HTMLResponse)
async def business_dashboards(request: Request):
    demo_status = request.query_params.get("demo", "").strip()
    return templates.TemplateResponse(
        "business/dashboards.html",
        {"request": request, "demo_status": demo_status},
    )

@app.post("/demo-access", response_class=HTMLResponse)
@limiter.limit("5/minute")
async def demo_access_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    company: str = Form(""),
    role: str = Form(""),
    notes: str = Form(""),
    utm_source: str = Form(""),
    utm_medium: str = Form(""),
    utm_campaign: str = Form(""),
    utm_content: str = Form(""),
    ref_page: str = Form(""),
    cta_id: str = Form(""),
    return_to: str = Form("/live-demos"),
    website: str = Form(""),
    recaptcha_response: str = Form(alias="g-recaptcha-response", default=""),
):
    safe_return_to = return_to if return_to.startswith("/") and not return_to.startswith("//") else "/live-demos"

    if website:
        return RedirectResponse(safe_return_to, status_code=303)

    if settings.RECAPTCHA_SECRET_KEY and not mailer_service.verify_recaptcha(recaptcha_response):
        return RedirectResponse(f"{safe_return_to}?demo=recaptcha", status_code=303)

    success = mailer_service.send_dashboard_demo_access_email(
        name=name,
        email=email,
        company=company,
        role=role,
        notes=notes,
        ref_page=ref_page,
        cta_id=cta_id,
        utm_source=utm_source,
        utm_medium=utm_medium,
        utm_campaign=utm_campaign,
        utm_content=utm_content,
    )
    if success:
        return RedirectResponse(f"{safe_return_to}?demo=sent", status_code=303)
    return RedirectResponse(f"{safe_return_to}?demo=error", status_code=303)


def _get_client_ip(request: Request) -> str:
    for header in ("cf-connecting-ip", "x-forwarded-for", "x-real-ip"):
        value = request.headers.get(header, "").strip()
        if value:
            if header == "x-forwarded-for":
                return value.split(",")[0].strip()
            return value
    if request.client and request.client.host:
        return request.client.host
    return "127.0.0.1"

@app.get("/pricing", response_class=HTMLResponse)
async def pricing(request: Request):
    ip_address = _get_client_ip(request)
    local_rate, currency_code, currency_symbol = await convert_rate(1.0, ip_address)
    return templates.TemplateResponse(
        "pricing.html",
        {
            "request": request,
            "offerings": offering_service.get_all(),
            "my_hourly_usd": 95.0,
            "market_hourly_usd": 145.0,
            "currency_code": currency_code,
            "currency_symbol": currency_symbol,
            "currency_rate": local_rate,
        },
    )

@app.get("/offerings", response_class=HTMLResponse)
async def offerings(request: Request):
    return templates.TemplateResponse(
        "offerings.html",
        {"request": request, "offerings": offering_service.get_all()},
    )

@app.get("/packages/{slug}", response_class=HTMLResponse)
async def offering_detail(request: Request, slug: str):
    offering = offering_service.get_by_slug(slug)
    if not offering:
        raise HTTPException(status_code=404, detail="Offering not found")
    return templates.TemplateResponse("offering_detail.html", {"request": request, "offering": offering})

@app.get("/o/{slug}", response_class=RedirectResponse)
async def offering_short_redirect(slug: str):
    return RedirectResponse(url=f"/packages/{slug}", status_code=301)

@app.get("/training", response_class=HTMLResponse)
async def training(request: Request):
    return templates.TemplateResponse("training.html", {"request": request})

@app.get("/training/corporate", response_class=HTMLResponse)
async def training_corporate(request: Request):
    return templates.TemplateResponse("training/corporate.html", {"request": request})

@app.get("/training/bootcamps", response_class=HTMLResponse)
async def training_bootcamps(request: Request):
    return templates.TemplateResponse("training/bootcamps.html", {"request": request})

@app.get("/speaking", response_class=HTMLResponse)
async def speaking(request: Request):
    return templates.TemplateResponse("speaking.html", {"request": request})

# Error Handlers
@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

@app.exception_handler(500)
async def server_error_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("500.html", {"request": request}, status_code=500)
