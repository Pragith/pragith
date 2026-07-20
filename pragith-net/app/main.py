from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings
from app.content.site import (
    CANONICAL_TITLE,
    CAPABILITIES,
    CASE_STUDIES,
    CERTIFICATIONS,
    CLOUD_PLATFORMS,
    EXPERIENCE,
    EXPERIENCE_LABEL,
    PROJECTS,
    SERVICES,
)
from app.services.mailer import mailer_service
from app.services.sitemap import generate_sitemap
from app.themes import ThemeService

app = FastAPI(title=settings.PROJECT_NAME, docs_url=None, redoc_url=None)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers.update({
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
            "Content-Security-Policy": (
                "default-src 'self'; script-src 'self' 'unsafe-inline' "
                "https://www.googletagmanager.com https://www.google.com https://www.gstatic.com "
                "https://www.clarity.ms https://scripts.clarity.ms; style-src 'self' 'unsafe-inline' "
                "https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; "
                "img-src 'self' data: https:; frame-src https://www.google.com; "
                "connect-src 'self' https://www.googletagmanager.com https://*.google-analytics.com "
                "https://*.analytics.google.com https://*.clarity.ms; worker-src 'self' blob:"
            ),
        })
        return response


app.add_middleware(SecurityHeadersMiddleware)

_APP_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=str(_APP_DIR / "static")), name="static")
app.mount(
    "/projects/agent-keyboard",
    StaticFiles(directory=str(_APP_DIR / "static" / "agent-keyboard"), html=True),
    name="agent-keyboard",
)
templates = Jinja2Templates(directory=str(_APP_DIR / "templates"))
theme_service = ThemeService(settings.THEME)
templates.env.globals.update({
    "now": datetime.now,
    "theme": theme_service,
    "ga_tag": settings.GA_TAG,
    "clarity_project_id": settings.CLARITY_PROJECT_ID,
    "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
    "canonical_title": CANONICAL_TITLE,
    "experience_label": EXPERIENCE_LABEL,
    "certifications": CERTIFICATIONS,
})


def render(
    request: Request,
    template: str,
    *,
    title: str,
    description: str,
    canonical_path: str,
    robots: str = "index,follow",
    status_code: int = 200,
    **context,
):
    return templates.TemplateResponse(request=request, name=template, context={
        "request": request,
        "page_title": title,
        "page_description": description,
        "canonical_url": f"https://pragith.net{canonical_path}",
        "robots": robots,
        **context,
    }, status_code=status_code)


@app.get("/theme.css", include_in_schema=False)
async def theme_css():
    return Response(content=theme_service.css, media_type="text/css")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse("/static/favicon.ico", status_code=301)


@app.get("/robots.txt", include_in_schema=False)
async def robots():
    return Response(
        "User-agent: *\nAllow: /\nDisallow: /projects/agent-keyboard\nSitemap: https://pragith.net/sitemap.xml\n",
        media_type="text/plain",
    )


@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap():
    return Response(generate_sitemap(), media_type="application/xml")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return render(
        request,
        "index.html",
        title="Pragith Prakash | AI Forward Deployed Engineer",
        description="Pragith Prakash designs and delivers AI systems, data platforms and cloud automation across AWS, Google Cloud, Azure and Databricks.",
        canonical_path="/",
        capabilities=CAPABILITIES,
        case_studies=CASE_STUDIES[:3],
        projects=PROJECTS,
        cloud_platforms=CLOUD_PLATFORMS,
    )


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return render(
        request, "about.html",
        title="About Pragith Prakash | AI Forward Deployed Engineer",
        description="Professional background, teaching, certifications and engineering approach of Pragith Prakash.",
        canonical_path="/about",
    )


@app.get("/experience", response_class=HTMLResponse)
async def experience(request: Request):
    return render(
        request, "experience.html",
        title="Experience | Pragith Prakash",
        description="An anonymized career timeline spanning enterprise AI, data platforms, cloud delivery, analytics and technical education.",
        canonical_path="/experience", experience=EXPERIENCE,
    )


@app.get("/resume", response_class=HTMLResponse)
async def resume(request: Request):
    return render(
        request, "resume.html",
        title="Resume | Pragith Prakash",
        description="Printable professional resume for Pragith Prakash, AI Forward Deployed Engineer, consultant and educator.",
        canonical_path="/resume", experience=EXPERIENCE,
    )


@app.get("/case-studies", response_class=HTMLResponse)
async def case_studies(request: Request):
    return render(
        request, "case_studies.html",
        title="Case Studies | Pragith Prakash",
        description="Anonymized examples of enterprise data platforms, AI delivery, cloud integrations, analytics and engineering enablement.",
        canonical_path="/case-studies", case_studies=CASE_STUDIES,
    )


@app.get("/case-studies/{slug}", response_class=HTMLResponse)
async def case_study(request: Request, slug: str):
    item = next((item for item in CASE_STUDIES if item["slug"] == slug), None)
    if not item:
        raise HTTPException(status_code=404)
    return render(
        request, "case_study.html",
        title=f"{item['title']} | Case Study",
        description=item["preview"], canonical_path=f"/case-studies/{slug}", item=item,
    )


@app.get("/services", response_class=HTMLResponse)
async def services(request: Request):
    return render(
        request, "services.html",
        title="Services | Pragith Prakash",
        description="Hands-on AI, data platform, cloud, MLOps, analytics and engineering enablement services.",
        canonical_path="/services", services=SERVICES,
    )


@app.get("/services/ai-systems", response_class=HTMLResponse)
async def ai_systems(request: Request):
    return render(
        request, "ai_systems.html",
        title="AI Systems and Automation | Pragith Prakash",
        description="Controlled AI orchestration, evaluation, observability, access, approval gates, failure handling and cost management.",
        canonical_path="/services/ai-systems",
    )


@app.get("/services/executive-bi", response_class=HTMLResponse)
async def executive_bi(request: Request):
    return render(
        request, "executive_bi.html",
        title="Analytics and Executive BI | Pragith Prakash",
        description="Vendor-neutral source integration, semantic modelling, governance, dashboards, access control and reporting operations.",
        canonical_path="/services/executive-bi",
    )


@app.get("/teaching", response_class=HTMLResponse)
async def teaching(request: Request):
    return render(
        request, "teaching.html",
        title="Teaching and Enablement | Pragith Prakash",
        description="Graduate instruction, workforce programs, workshops and team enablement across AI, data, cloud and software engineering.",
        canonical_path="/teaching",
    )


@app.get("/projects", response_class=HTMLResponse)
async def projects(request: Request):
    return render(
        request, "projects.html",
        title="Projects and Labs | Pragith Prakash",
        description="Open-source tools and clearly labelled experiments by Pragith Prakash.",
        canonical_path="/projects", projects=PROJECTS,
    )


@app.get("/projects/caffeinate-d", response_class=HTMLResponse)
async def caffeinate_d(request: Request):
    return render(
        request, "caffeinate_d.html",
        title="Caffeinate-d | Pragith Prakash",
        description="A small native macOS menu-bar wrapper for the system caffeinate command.",
        canonical_path="/projects/caffeinate-d", robots="noindex,follow",
    )


@app.get("/writing", response_class=HTMLResponse)
async def writing(request: Request):
    return render(
        request, "writing.html",
        title="Writing and Appearances | Pragith Prakash",
        description="Selected technical writing, talks and appearances by Pragith Prakash.",
        canonical_path="/writing",
    )


@app.get("/business", response_class=HTMLResponse)
async def business(request: Request):
    return render(
        request, "business.html",
        title="Business Services | Vriksh Consulting Services Inc.",
        description="Packaged analytics, automation and technical enablement services delivered through Vriksh Consulting Services Inc.",
        canonical_path="/business",
    )


@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    tracking = {
        field: request.query_params.get(field, "")
        for field in (
            "ref_page", "cta_id", "utm_source", "utm_medium",
            "utm_campaign", "utm_content",
        )
    }
    return render(
        request, "contact.html",
        title="Contact Pragith Prakash",
        description="Discuss an AI, data platform, cloud architecture, analytics or technical education engagement with Pragith Prakash.",
        canonical_path="/contact", form={}, tracking=tracking,
        recaptcha_site_key=settings.RECAPTCHA_SITE_KEY,
    )


@app.post("/contact", response_class=HTMLResponse)
@limiter.limit("5/minute")
async def contact_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    company: str = Form(""),
    engagement_type: str = Form("Initial fit assessment"),
    timeline: str = Form(""),
    message: str = Form(""),
    website: str = Form(""),
    ref_page: str = Form(""),
    cta_id: str = Form(""),
    utm_source: str = Form(""),
    utm_medium: str = Form(""),
    utm_campaign: str = Form(""),
    utm_content: str = Form(""),
    recaptcha_response: str = Form(alias="g-recaptcha-response", default=""),
):
    if website:
        return RedirectResponse("/contact", status_code=303)
    form_data = await request.form()
    if settings.RECAPTCHA_SECRET_KEY and not mailer_service.verify_recaptcha(recaptcha_response):
        return render(
            request, "contact.html", title="Contact Pragith Prakash",
            description="Contact Pragith Prakash.", canonical_path="/contact",
            error="reCAPTCHA verification failed.", form=form_data, tracking=form_data,
        )
    attribution = (
        f"Source page: {ref_page or 'direct'}\n"
        f"CTA: {cta_id or 'direct'}\n"
        f"UTM source: {utm_source}\n"
        f"UTM medium: {utm_medium}\n"
        f"UTM campaign: {utm_campaign}\n"
        f"UTM content: {utm_content}"
    )
    body = (
        f"Engagement: {engagement_type}\nCompany: {company}\nTimeline: {timeline}\n\n"
        f"{message}\n\nAttribution\n{attribution}"
    )
    if mailer_service.send_contact_email(name, email, "Website enquiry", body):
        return render(
            request, "contact_success.html", title="Message received | Pragith Prakash",
            description="Your message has been received.", canonical_path="/contact", robots="noindex,follow",
        )
    return render(
        request, "contact.html", title="Contact Pragith Prakash",
        description="Contact Pragith Prakash.", canonical_path="/contact",
        error="The message could not be sent. Please try again.", form=form_data, tracking=form_data,
    )


@app.get("/privacy", response_class=HTMLResponse)
async def privacy(request: Request):
    return render(request, "privacy.html", title="Privacy | Pragith Prakash", description="Privacy information for pragith.net.", canonical_path="/privacy")


@app.get("/legal", response_class=HTMLResponse)
async def legal(request: Request):
    return render(request, "legal.html", title="Legal | Pragith Prakash", description="Legal information for pragith.net.", canonical_path="/legal")


REDIRECTS = {
    "/ai": "/services/ai-systems",
    "/apps": "/projects",
    "/apps/caffeinated": "/projects/caffeinate-d",
    "/apps/agent-keyboard": "/projects/agent-keyboard/",
    "/business/dashboards": "/services/executive-bi",
    "/work": "/case-studies",
    "/notes": "/writing",
    "/training": "/teaching",
    "/speaking": (
        "/teaching?ref=speaking&utm_source=pragith_net&"
        "utm_medium=legacy_redirect&utm_campaign=speaking"
    ),
    "/packages": "/services",
}


@app.get("/{legacy_path:path}", include_in_schema=False)
async def legacy_or_404(request: Request, legacy_path: str):
    path = f"/{legacy_path}"
    if path in REDIRECTS:
        return RedirectResponse(REDIRECTS[path], status_code=301)
    raise HTTPException(status_code=404)


@app.exception_handler(404)
async def not_found(request: Request, exc: HTTPException):
    return render(
        request, "404.html", title="Page not found | Pragith Prakash",
        description="The requested page could not be found.", canonical_path=request.url.path,
        robots="noindex,follow", status_code=404,
    )
