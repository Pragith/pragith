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
# Agent Keyboard: self-contained static app (index.html/style.css/app.js),
# source of truth lives in agent-fleet and is bind-mounted in via
# docker-compose.yml (see the "web" service's volumes). html=True serves
# index.html for the bare "/apps/agent-keyboard" path.
app.mount(
    "/apps/agent-keyboard",
    StaticFiles(directory=str(_APP_DIR / "static" / "agent-keyboard"), html=True),
    name="agent-keyboard",
)
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
    sitemap_service._urls = []
    sitemap_service.generate_static_urls()
    sitemap_service.add_blog_posts(blog_service.get_all())
    from app.services.offering_loader import offering_service
    sitemap_service.add_offerings(offering_service.get_all())
    xml_content = sitemap_service.generate_xml()
    return Response(content=xml_content, media_type="application/xml")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/ai", response_class=HTMLResponse)
async def ai_fleet(request: Request):
    return templates.TemplateResponse("ai.html", {"request": request})

@app.get("/apps", response_class=HTMLResponse)
async def apps_hub(request: Request):
    return templates.TemplateResponse("apps.html", {"request": request})

@app.get("/apps/caffeinated", response_class=HTMLResponse)
async def caffeinated_app(request: Request):
    return templates.TemplateResponse("apps/caffeinate-d.html", {"request": request})

@app.get("/business/dashboards", response_class=HTMLResponse)
async def business_dashboards(request: Request):
    demo_status = request.query_params.get("demo", "").strip()
    return templates.TemplateResponse("business/dashboards.html", {"request": request, "demo_status": demo_status})

@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "form": {},
        "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
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
    website: str = Form(""),
    recaptcha_response: str = Form(alias="g-recaptcha-response", default="")
):
    if website:
        return RedirectResponse("/contact", status_code=303)
    
    if settings.RECAPTCHA_SECRET_KEY and not mailer_service.verify_recaptcha(recaptcha_response):
        return templates.TemplateResponse("contact.html", {"request": request, "error": "reCAPTCHA failed."})
        
    enriched_message = f"{what_do_you_need_built}\n\nCompany: {company}\nTimeline: {timeline}\nBudget: {budget_range}"
    success = mailer_service.send_contact_email(name, email, "New Intake", enriched_message)
    if success:
        return templates.TemplateResponse("contact_success.html", {"request": request})
    return templates.TemplateResponse("contact.html", {"request": request, "error": "Failed to send."})

@app.post("/demo-access", response_class=HTMLResponse)
@limiter.limit("5/minute")
async def demo_access_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    company: str = Form(""),
    role: str = Form(""),
    notes: str = Form(""),
    return_to: str = Form("/business/dashboards"),
    website: str = Form(""),
    recaptcha_response: str = Form(alias="g-recaptcha-response", default=""),
):
    safe_return_to = return_to if return_to.startswith("/") and not return_to.startswith("//") else "/business/dashboards"
    if website:
        return RedirectResponse(safe_return_to, status_code=303)
    if settings.RECAPTCHA_SECRET_KEY and not mailer_service.verify_recaptcha(recaptcha_response):
        return RedirectResponse(f"{safe_return_to}?demo=recaptcha", status_code=303)
        
    success = mailer_service.send_dashboard_demo_access_email(
        name=name, email=email, company=company, role=role, notes=notes,
        ref_page="", cta_id="", utm_source="", utm_medium="", utm_campaign="", utm_content=""
    )
    if success:
        return RedirectResponse(f"{safe_return_to}?demo=sent", status_code=303)
    return RedirectResponse(f"{safe_return_to}?demo=error", status_code=303)

@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

@app.exception_handler(500)
async def server_error_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("500.html", {"request": request}, status_code=500)
