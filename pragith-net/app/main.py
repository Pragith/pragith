from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.services.blog_loader import blog_service
from app.services.mailer import mailer_service

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
            "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google.com https://www.gstatic.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data:; "
            "frame-src https://www.google.com https://calendly.com; "
            "connect-src 'self' https://www.google-analytics.com https://www.googletagmanager.com"
        )
        return response

app.add_middleware(SecurityHeadersMiddleware)

# Static & Templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

from datetime import datetime
templates.env.globals["now"] = datetime.now

# Context Processor for common variables
@app.middleware("http")
async def add_context(request: Request, call_next):
    # Inject GA_TAG into request state so templates can access it
    request.state.ga_tag = settings.GA_TAG
    return await call_next(request)

# Routes

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse(url="/static/favicon.ico", status_code=301)

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

@app.get("/build", response_class=HTMLResponse)
async def build_page(request: Request):
    return templates.TemplateResponse("build.html", {"request": request})

@app.get("/stack", response_class=HTMLResponse)
async def stack(request: Request):
    return templates.TemplateResponse("stack.html", {"request": request})


@app.get("/blog", response_class=HTMLResponse)
async def blog_list(request: Request):
    posts = blog_service.get_all()
    return templates.TemplateResponse("blog_list.html", {"request": request, "posts": posts})

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
    from app.services.currency import convert_rate
    
    client_ip = request.client.host if request.client else "127.0.0.1"
    converted_rate, currency_code, currency_symbol = await convert_rate(
        settings.HOURLY_RATE,
        client_ip
    )
    
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "ga_tag": settings.GA_TAG,
        "hourly_rate": converted_rate,
        "currency_code": currency_code,
        "currency_symbol": currency_symbol,
        "base_rate_usd": settings.HOURLY_RATE,
        "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
        "calendly_url": settings.CALENDLY_URL,
    })


@app.post("/contact", response_class=HTMLResponse)
@limiter.limit("5/minute")
async def contact_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    inquiry_type: str = Form(...),
    message: str = Form(...),
    website: str = Form(""),
    recaptcha_response: str = Form(alias="g-recaptcha-response", default="")
):
    # Honeypot check — bots fill hidden fields
    if website:
        return RedirectResponse("/contact", status_code=303)
    
    # Verify captcha (skip if no key configured)
    if settings.RECAPTCHA_SECRET_KEY and not mailer_service.verify_recaptcha(recaptcha_response):
        return templates.TemplateResponse("contact.html", {
            "request": request, 
            "error": "reCAPTCHA verification failed. Please try again.",
            "form": {"name": name, "email": email, "inquiry_type": inquiry_type, "message": message},
            "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
        })

    success = mailer_service.send_contact_email(name, email, inquiry_type, message)

    if success:
        return templates.TemplateResponse("contact_success.html", {"request": request})
    else:
        return templates.TemplateResponse("contact.html", {
            "request": request, 
            "error": "Failed to send message. Please try again later.",
            "form": {"name": name, "email": email, "inquiry_type": inquiry_type, "message": message},
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

# Error Handlers
@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

@app.exception_handler(500)
async def server_error_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("500.html", {"request": request}, status_code=500)
