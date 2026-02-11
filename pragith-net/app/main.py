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
        return response

app.add_middleware(SecurityHeadersMiddleware)

# Static & Templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Context Processor for common variables
@app.middleware("http")
async def add_context(request: Request, call_next):
    # This is not a standard middleware for context, 
    # but we can pass common data via request state or template globals if needed.
    # For now, we'll just handle it in routes or use a helper.
    return await call_next(request)

# Routes

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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

@app.get("/consult", response_class=HTMLResponse)
async def consult(request: Request):
    return templates.TemplateResponse("consult.html", {"request": request})

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
    return templates.TemplateResponse("contact.html", {"request": request, "site_key": "TODO-PUBLIC-KEY-ENV"}) 
    # NOTE: Need to expose PUBLIC key to template too. 
    # We should add RECAPTCHA_SITE_KEY to config and pass it here.

@app.post("/contact", response_class=HTMLResponse)
@limiter.limit("5/minute")
async def contact_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    company: str = Form(...),
    message: str = Form(...),
    recaptcha_response: str = Form(alias="g-recaptcha-response")
):
    # Verify captcha
    # In dev, we might skip if key is missing, handled in service.
    if not mailer_service.verify_recaptcha(recaptcha_response):
        return templates.TemplateResponse("contact.html", {
            "request": request, 
            "error": "reCAPTCHA verification failed. Please try again.",
            "form": {"name": name, "email": email, "company": company, "message": message}
        })

    # Send email
    success = mailer_service.send_contact_email(name, email, company, message) 
    # mailer_service.send_contact_error(name, email, company, message) - Check signature in mailer.py
    # Signature: send_contact_email(name, email, company, message)
    
    # Correct call:
    success = mailer_service.send_contact_email(name, email, company, message)

    if success:
        return templates.TemplateResponse("contact_success.html", {"request": request})
    else:
        return templates.TemplateResponse("contact.html", {
            "request": request, 
            "error": "Failed to send message. Please try again later.",
            "form": {"name": name, "email": email, "company": company, "message": message}
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
