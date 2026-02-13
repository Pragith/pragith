from dataclasses import dataclass
from pathlib import Path
from typing import List

import yaml


@dataclass
class ProjectTypeRule:
    contains: str
    project_type: str


class MarketingService:
    def __init__(self) -> None:
        self._config = self._load_config()
        self._rules: List[ProjectTypeRule] = [
            ProjectTypeRule(
                contains=str(item.get("contains", "")).strip().lower(),
                project_type=str(item.get("project_type", "")).strip(),
            )
            for item in self._config.get("project_type_rules", [])
            if item.get("contains") and item.get("project_type")
        ]
        self._default_project_type = str(
            self._config.get("default_project_type", "Other / Unsure")
        ).strip()

    def _load_config(self) -> dict:
        path = Path(__file__).resolve().parent.parent / "content" / "marketing.yaml"
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def get_client_config(self) -> dict:
        utm = self._config.get("utm_defaults", {})
        return {
            "utm_defaults": {
                "source": str(utm.get("source", "pragith_net")),
                "medium": str(utm.get("medium", "website_cta")),
                "campaign": str(utm.get("campaign", "inbound_consulting")),
            },
            "default_project_type": self._default_project_type,
            "project_type_rules": [
                {"contains": r.contains, "project_type": r.project_type} for r in self._rules
            ],
        }

    def resolve_project_type(self, ref_page: str) -> str:
        page = (ref_page or "").lower()
        for rule in self._rules:
            if rule.contains in page:
                return rule.project_type
        return self._default_project_type


marketing_service = MarketingService()
