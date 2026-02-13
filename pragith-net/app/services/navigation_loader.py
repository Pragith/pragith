from pathlib import Path

import yaml


class NavigationService:
    def __init__(self) -> None:
        self._config = self._load_config()

    def _load_config(self) -> dict:
        path = Path(__file__).resolve().parent.parent / "content" / "navigation.yaml"
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def get_client_config(self) -> dict:
        brand = self._config.get("brand", {})
        cta = self._config.get("cta", {})
        links = self._config.get("links", [])

        normalized_links = []
        for item in links:
            href = str(item.get("href", "")).strip()
            label = str(item.get("label", "")).strip()
            if not href or not label:
                continue
            normalized_links.append({"href": href, "label": label})

        return {
            "brand": {
                "href": str(brand.get("href", "/")).strip() or "/",
                "label": str(brand.get("label", "Pragith Prakash")).strip() or "Pragith Prakash",
            },
            "cta": {
                "href": str(cta.get("href", "/contact")).strip() or "/contact",
                "label": str(cta.get("label", "Define the Build →")).strip() or "Define the Build →",
            },
            "links": normalized_links,
        }


navigation_service = NavigationService()
