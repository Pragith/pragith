from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
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
            "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google.com https://www.gstatic.com https://static.hotjar.com https://script.hotjar.com https://t.contentsquare.net https://www.clarity.ms; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https://*.hotjar.com https://*.contentsquare.net https://www.clarity.ms https://c.clarity.ms; "
            "frame-src https://www.google.com https://calendly.com; "
            "connect-src 'self' https://www.google-analytics.com https://www.googletagmanager.com https://*.hotjar.com wss://*.hotjar.com https://*.contentsquare.net https://www.clarity.ms https://c.clarity.ms"
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
templates.env.globals["hotjar_site_id"] = settings.HOTJAR_SITE_ID
templates.env.globals["clarity_project_id"] = settings.CLARITY_PROJECT_ID
templates.env.globals["recaptcha_site_key"] = settings.RECAPTCHA_SITE_KEY
templates.env.globals["marketing_config"] = marketing_service.get_client_config()
templates.env.globals["navigation_config"] = navigation_service.get_client_config()
templates.env.globals["nav_mode"] = settings.NAV_MODE
templates.env.globals["nav_offset_top"] = settings.NAV_OFFSET_TOP
templates.env.globals["nav_offset_left"] = settings.NAV_OFFSET_LEFT
templates.env.globals["nav_left_width"] = settings.NAV_LEFT_WIDTH

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
    return templates.TemplateResponse("index.html", {"request": request, "ga_tag": settings.GA_TAG})

@app.get("/agents", response_class=HTMLResponse)
async def agents(request: Request):
    return templates.TemplateResponse("agents.html", {"request": request})

from app.services.work_loader import work_service

@app.get("/work", response_class=HTMLResponse)
async def work(request: Request):
    works = work_service.get_all()
    return templates.TemplateResponse("work.html", {"request": request, "works": works})

@app.get("/work/{slug}", response_class=HTMLResponse)
async def work_detail(request: Request, slug: str):
    work_item = work_service.get_by_slug(slug)
    if not work_item:
        raise HTTPException(status_code=404, detail="Project not found")
    return templates.TemplateResponse("work_detail.html", {"request": request, "work": work_item})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/build", response_class=RedirectResponse)
async def build_page(request: Request):
    return RedirectResponse(url="/agents", status_code=301)

@app.get("/stack", response_class=HTMLResponse)
async def stack(request: Request):
    return templates.TemplateResponse("stack.html", {"request": request})


from typing import Optional

@app.get("/blog", response_class=HTMLResponse)
async def blog_list(request: Request, year: Optional[int] = None):
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

@app.get("/blog/tag/{tag}", response_class=HTMLResponse)
async def blog_tag(request: Request, tag: str):
    posts = blog_service.get_by_tag(tag)
    return templates.TemplateResponse("blog_list.html", {"request": request, "posts": posts, "tag": tag})

@app.get("/blog/{slug}", response_class=HTMLResponse)
async def blog_detail(request: Request, slug: str):
    post = blog_service.get_by_slug(slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("blog_detail.html", {"request": request, "post": post})

@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    q = request.query_params

    project_type = q.get("project_type", "").strip()
    if not project_type:
        ref_page = (q.get("ref_page", "") or "").lower()
        project_type = marketing_service.resolve_project_type(ref_page)

    inquiry_type = q.get("inquiry_type", "").strip() or "Within 90 days"
    decision_authority = q.get("decision_authority", "").strip()
    challenge_type = q.get("challenge_type", "").strip()
    team_size = q.get("team_size", "").strip()
    package = q.get("package", "").strip()
    outcome = q.get("outcome", "").strip()
    ref_page = q.get("ref_page", "").strip()
    utm_source = q.get("utm_source", "").strip()
    utm_medium = q.get("utm_medium", "").strip()
    utm_campaign = q.get("utm_campaign", "").strip()
    utm_content = q.get("utm_content", "").strip()
    cta_id = q.get("cta_id", "").strip()

    prefill_message = q.get("message", "").strip()
    if not prefill_message:
        lines = ["I want to discuss a scoped build."]
        if package:
            lines.append(f"Package of interest: {package}")
        if outcome:
            lines.append(f"Target outcome: {outcome}")
        if ref_page:
            lines.append(f"Ref page: {ref_page}")
        prefill_message = "\n".join(lines)

    form_defaults = {
        "name": q.get("name", ""),
        "email": q.get("email", ""),
        "company": q.get("company", ""),
        "team_size": team_size,
        "project_type": project_type,
        "inquiry_type": inquiry_type,
        "decision_authority": decision_authority,
        "challenge_type": challenge_type,
        "message": prefill_message,
        "utm_source": utm_source,
        "utm_medium": utm_medium,
        "utm_campaign": utm_campaign,
        "utm_content": utm_content,
        "ref_page": ref_page,
        "cta_id": cta_id,
        "package": package,
    }

    return templates.TemplateResponse("contact.html", {
        "request": request,
        "ga_tag": settings.GA_TAG,
        "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
        "calendly_url": settings.CALENDLY_URL,
        "form": form_defaults,
    })


@app.post("/contact", response_class=HTMLResponse)
@limiter.limit("5/minute")
async def contact_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    inquiry_type: str = Form(...),
    message: str = Form(""),
    company: str = Form(""),
    team_size: str = Form(""),
    project_type: str = Form(""),
    decision_authority: str = Form(...),
    challenge_type: str = Form(...),
    utm_source: str = Form(""),
    utm_medium: str = Form(""),
    utm_campaign: str = Form(""),
    utm_content: str = Form(""),
    ref_page: str = Form(""),
    cta_id: str = Form(""),
    package: str = Form(""),
    website: str = Form(""),
    recaptcha_response: str = Form(alias="g-recaptcha-response", default="")
):
    # Honeypot check  -  bots fill hidden fields
    if website:
        return RedirectResponse("/contact", status_code=303)
    
    # Verify captcha (skip if no key configured)
    if settings.RECAPTCHA_SECRET_KEY and not mailer_service.verify_recaptcha(recaptcha_response):
        return templates.TemplateResponse("contact.html", {
            "request": request, 
            "error": "reCAPTCHA verification failed. Please try again.",
            "form": {
                "name": name,
                "email": email,
                "company": company,
                "team_size": team_size,
                "project_type": project_type,
                "inquiry_type": inquiry_type,
                "decision_authority": decision_authority,
                "challenge_type": challenge_type,
                "message": message,
                "utm_source": utm_source,
                "utm_medium": utm_medium,
                "utm_campaign": utm_campaign,
                "utm_content": utm_content,
                "ref_page": ref_page,
                "cta_id": cta_id,
                "package": package,
            },
            "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
        })

    enriched_message = message
    metadata = []
    if company:
        metadata.append(f"Company: {company}")
    if project_type:
        metadata.append(f"Project Type: {project_type}")
    if decision_authority:
        metadata.append(f"Decision Authority: {decision_authority}")
    if challenge_type:
        metadata.append(f"Primary Challenge: {challenge_type}")
    if team_size:
        metadata.append(f"Team Size: {team_size}")
    if package:
        metadata.append(f"Package: {package}")
    if ref_page:
        metadata.append(f"Ref Page: {ref_page}")
    if cta_id:
        metadata.append(f"CTA ID: {cta_id}")
    if utm_source or utm_medium or utm_campaign or utm_content:
        metadata.append(
            f"UTM: source={utm_source or '-'} medium={utm_medium or '-'} campaign={utm_campaign or '-'} content={utm_content or '-'}"
        )
    if metadata:
        enriched_message = f"{message}\n\n---\n" + "\n".join(metadata)

    success = mailer_service.send_contact_email(name, email, inquiry_type, enriched_message)

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
                "team_size": team_size,
                "project_type": project_type,
                "inquiry_type": inquiry_type,
                "decision_authority": decision_authority,
                "challenge_type": challenge_type,
                "message": message,
                "utm_source": utm_source,
                "utm_medium": utm_medium,
                "utm_campaign": utm_campaign,
                "utm_content": utm_content,
                "ref_page": ref_page,
                "cta_id": cta_id,
                "package": package,
            },
            "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
        })

@app.get("/faq", response_class=HTMLResponse)
async def faq(request: Request):
    return templates.TemplateResponse("faq.html", {"request": request})

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

@app.get("/business/automation", response_class=HTMLResponse)
async def business_automation(request: Request):
    return templates.TemplateResponse("business/automation.html", {"request": request})

@app.get("/business/whatsapp-automation", response_class=HTMLResponse)
async def business_whatsapp_automation(request: Request):
    return templates.TemplateResponse("business/whatsapp_automation.html", {"request": request})

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
    website: str = Form(""),
    recaptcha_response: str = Form(alias="g-recaptcha-response", default=""),
):
    if website:
        return RedirectResponse("/business/dashboards", status_code=303)

    if settings.RECAPTCHA_SECRET_KEY and not mailer_service.verify_recaptcha(recaptcha_response):
        return RedirectResponse("/business/dashboards?demo=recaptcha", status_code=303)

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
        return RedirectResponse("/business/dashboards?demo=sent", status_code=303)
    return RedirectResponse("/business/dashboards?demo=error", status_code=303)

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
