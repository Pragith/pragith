import json
import re
from html.parser import HTMLParser
from xml.etree import ElementTree

from fastapi.testclient import TestClient

from app.content.site import CERTIFICATIONS, INDEXABLE_PATHS
from app.config import settings
from app.main import app
from app.services.mailer import mailer_service


client = TestClient(app, base_url="http://localhost")


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)


def test_every_indexable_route_is_successful_and_canonical():
    for path in INDEXABLE_PATHS:
        response = client.get(path)
        assert response.status_code == 200, path
        html = response.text
        assert f'<link rel="canonical" href="https://pragith.net{path}">' in html
        assert '<meta name="robots" content="index,follow">' in html
        assert '<meta property="og:title"' in html
        assert '<script type="application/ld+json">' in html


def test_configured_analytics_are_rendered():
    html = client.get("/").text
    if settings.GA_TAG:
        assert "https://www.googletagmanager.com/gtag/js?id=" in html
        assert settings.GA_TAG in html
        assert "anonymize_ip" in html
    if settings.CLARITY_PROJECT_ID:
        assert "https://www.clarity.ms/tag/" in html
        assert settings.CLARITY_PROJECT_ID in html


def test_sitemap_contains_only_successful_indexable_routes():
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    root = ElementTree.fromstring(response.text)
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [node.text for node in root.findall("s:url/s:loc", namespace)]
    assert urls == [f"https://pragith.net{path}" for path in INDEXABLE_PATHS]
    for url in urls:
        path = url.removeprefix("https://pragith.net") or "/"
        assert client.get(path).status_code == 200


def test_legacy_routes_redirect_to_canonical_pages():
    expected = {
        "/ai": "/services/ai-systems",
        "/apps": "/projects",
        "/apps/caffeinated": "/projects/caffeinate-d",
        "/business/dashboards": "/services/executive-bi",
        "/work": "/case-studies",
        "/notes": "/writing",
        "/training": "/teaching",
        "/speaking": (
            "/teaching?ref=speaking&utm_source=pragith_net&"
            "utm_medium=legacy_redirect&utm_campaign=speaking"
        ),
    }
    for old, new in expected.items():
        response = client.get(old, follow_redirects=False)
        assert response.status_code == 301, old
        assert response.headers["location"] == new


def test_canonical_title_experience_and_certifications():
    combined = "\n".join(client.get(path).text for path in ["/", "/about", "/resume"])
    assert "AI Forward Deployed Engineer" in combined
    assert "14+ years" in combined
    assert "13+ years" not in combined
    assert "15+ years" not in combined
    for certification in CERTIFICATIONS:
        assert certification in combined
    assert "Databricks Certified Generative AI Associate" not in combined


def test_published_pages_exclude_banned_marketing_language():
    banned = [
        "extreme velocity", "massive objectives within hours",
        "zero-hallucination execution", "agent-native systems",
        "silent automation", "absolute focus", "complete source truth",
        "bloated teams", "intelligence deployed", "architecture that executes",
        "systems that ship", "sovereign GPU infrastructure", "Pragith AI Inc.",
    ]
    published = "\n".join(client.get(path).text.lower() for path in INDEXABLE_PATHS)
    for phrase in banned:
        assert phrase.lower() not in published


def test_personal_pages_do_not_use_first_person_plural():
    personal_paths = [path for path in INDEXABLE_PATHS if path != "/business"]
    for path in personal_paths:
        text = re.sub(r"<[^>]+>", " ", client.get(path).text)
        assert not re.search(r"\b(we|our|ours)\b", text, flags=re.IGNORECASE), path
    assert re.search(r"\bwe\b", client.get("/business").text, flags=re.IGNORECASE)


def test_projects_are_honest_about_maturity():
    projects = client.get("/projects").text
    assert "Velvet IPTV Player" in projects and "Production" in projects
    assert "https://velvet.plus" in projects
    assert "Headmaster" in projects and "Beta" in projects
    assert "Caffeinate-d" in projects and "Source version 0.2.0" in projects
    assert "Agent Keyboard" in projects and "Prototype" in projects
    assert "The CLI bridge is not implemented" in projects
    caffeinate = client.get("/projects/caffeinate-d").text
    assert '<meta name="robots" content="noindex,follow">' in caffeinate
    assert "matching packaged release" in caffeinate


def test_contact_form_uses_approved_engagement_models():
    html = client.get("/contact").text
    for label in [
        "Initial fit assessment", "Paid architecture / discovery session",
        "Hourly engineering", "Milestone delivery", "Other",
    ]:
        assert label in html
    assert "Others" not in html
    assert "$95" not in html


def test_contact_page_preserves_internal_attribution():
    html = client.get(
        "/contact?ref_page=teaching&cta_id=discuss-training&"
        "utm_source=pragith_net&utm_medium=internal_cta&"
        "utm_campaign=contact&utm_content=discuss-training"
    ).text
    expected = {
        "ref_page": "teaching",
        "cta_id": "discuss-training",
        "utm_source": "pragith_net",
        "utm_medium": "internal_cta",
        "utm_campaign": "contact",
        "utm_content": "discuss-training",
        "tag1": "",
        "tag2": "",
    }
    for field, value in expected.items():
        assert f'name="{field}" value="{value}"' in html

    teaching = client.get("/teaching").text
    assert "contact_cta_click" in teaching
    assert "utm_medium: 'internal_cta'" in teaching


def test_contact_page_smartly_prefills_from_source_tags():
    html = client.get(
        "/contact?ref_page=speaking&cta_id=invite-pragith-to-speak&"
        "tag1=speaking&tag2=invite-pragith-to-speak"
    ).text
    assert "<option selected>Speaking engagement</option>" in html
    assert "I’d like to discuss a speaking engagement." in html
    assert "Event and audience:" in html
    assert 'name="tag1" value="speaking"' in html
    assert 'name="tag2" value="invite-pragith-to-speak"' in html


def test_recaptcha_v3_is_loaded_only_for_the_contact_form():
    contact = client.get("/contact").text
    home = client.get("/").text
    if settings.RECAPTCHA_SITE_KEY:
        assert "recaptcha/api.js?render=" in contact
        assert 'id="contact-recaptcha-response"' in contact
        assert "grecaptcha.execute(siteKey, {action: 'submit_contact'})" in contact
        assert 'class="g-recaptcha"' not in contact
        assert "recaptcha/api.js" not in home


def test_contact_submission_uses_selected_engagement(monkeypatch):
    captured = {}

    def fake_send(name, email, subject, body):
        captured.update(name=name, email=email, subject=subject, body=body)
        return True

    monkeypatch.setattr("app.main.mailer_service.send_contact_email", fake_send)
    monkeypatch.setattr("app.main.mailer_service.verify_recaptcha", lambda _: True)
    response = client.post("/contact", data={
        "name": "Site visitor",
        "email": "visitor@example.com",
        "company": "Example organization",
        "engagement_type": "Paid architecture / discovery session",
        "timeline": "This quarter",
        "message": "We need to review a data platform architecture.",
        "ref_page": "speaking",
        "cta_id": "discuss-training",
        "utm_source": "pragith_net",
        "utm_medium": "internal_cta",
        "utm_campaign": "contact",
        "utm_content": "discuss-training",
        "tag1": "speaking",
        "tag2": "discuss-training",
    })
    assert response.status_code == 200
    assert "Message received" in response.text
    assert "Paid architecture / discovery session" in captured["body"]
    assert "Source page: speaking" in captured["body"]
    assert "CTA: discuss-training" in captured["body"]
    assert "UTM campaign: contact" in captured["body"]
    assert "Tag 1: speaking" in captured["body"]
    assert "Tag 2: discuss-training" in captured["body"]


def test_recaptcha_v3_requires_score_and_expected_action(monkeypatch):
    class Response:
        def __init__(self, payload):
            self.payload = payload

        def raise_for_status(self):
            return None

        def json(self):
            return self.payload

    payload = {"success": True, "score": 0.9, "action": "submit_contact"}

    def fake_post(url, data, timeout):
        assert url.endswith("/recaptcha/api/siteverify")
        assert data["response"] == "browser-token"
        assert timeout == 5
        return Response(payload)

    monkeypatch.setattr("app.services.mailer.settings.RECAPTCHA_SECRET_KEY", "test-secret")
    monkeypatch.setattr("app.services.mailer.requests.post", fake_post)
    assert mailer_service.verify_recaptcha("browser-token") is True

    payload["action"] = "different_action"
    assert mailer_service.verify_recaptcha("browser-token") is False

    payload.update(action="submit_contact", score=0.1)
    assert mailer_service.verify_recaptcha("browser-token") is False


def test_unknown_route_is_a_noindexed_404():
    response = client.get("/not-a-real-route")
    assert response.status_code == 404
    assert '<meta name="robots" content="noindex,follow">' in response.text


def test_internal_links_resolve_and_json_ld_is_valid():
    checked = set()
    for path in INDEXABLE_PATHS:
        html = client.get(path).text
        for payload in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL):
            json.loads(payload)
        parser = LinkParser()
        parser.feed(html)
        for href in parser.links:
            if not href.startswith("/") or href.startswith("//"):
                continue
            target = href.split("#", 1)[0] or path
            if target in checked:
                continue
            checked.add(target)
            assert client.get(target).status_code < 400, target
