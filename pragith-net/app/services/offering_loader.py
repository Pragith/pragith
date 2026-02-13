from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import yaml


@dataclass
class Offering:
    slug: str
    title: str
    target_client: str
    outcome: str
    estimated_hours: str
    base_hours: int
    price_usd_min: int
    price_usd_max: int
    price_usd_high_min: int
    price_usd_high_max: int
    public: bool


class OfferingService:
    def __init__(self) -> None:
        self._offerings = self._load_offerings()

    def _load_offerings(self) -> List[Offering]:
        content_path = Path(__file__).resolve().parent.parent / "content" / "offerings.yaml"
        with content_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        offerings_raw = data.get("offerings", [])
        offerings: List[Offering] = []
        for item in offerings_raw:
            offerings.append(
                Offering(
                    slug=str(item.get("slug", "")).strip(),
                    title=str(item.get("title", "")).strip(),
                    target_client=str(item.get("target_client", "")).strip(),
                    outcome=str(item.get("outcome", "")).strip(),
                    estimated_hours=str(item.get("estimated_hours", "")).strip(),
                    base_hours=int(item.get("base_hours", 30)),
                    price_usd_min=int(item.get("price_usd_min", 0)),
                    price_usd_max=int(item.get("price_usd_max", 0)),
                    price_usd_high_min=int(item.get("price_usd_high_min", 0)),
                    price_usd_high_max=int(item.get("price_usd_high_max", 0)),
                    public=item.get("public", True),
                )
            )
        return offerings

    def get_all(self) -> List[Offering]:
        return self._offerings

    def get_by_slug(self, slug: str) -> Optional[Offering]:
        for offering in self._offerings:
            if offering.slug == slug:
                return offering
        return None


offering_service = OfferingService()
