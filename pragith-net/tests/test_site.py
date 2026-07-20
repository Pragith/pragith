import json
import re
from html.parser import HTMLParser
from xml.etree import ElementTree

from fastapi.testclient import TestClient

from app.content.site import CERTIFICATIONS, INDEXABLE_PATHS
from app.main import app


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
        "/speaking": "/teaching",
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
    })
    assert response.status_code == 200
    assert "Message received" in response.text
    assert "Paid architecture / discovery session" in captured["body"]


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
