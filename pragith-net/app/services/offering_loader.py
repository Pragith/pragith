from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Offering:
    slug: str
    title: str
    target_client: str
    outcome: str
    estimated_hours: str


OFFERINGS: List[Offering] = [
    Offering(
        slug="ai-audit",
        title="AI Readiness Audit",
        target_client="SMEs",
        outcome="AI adoption roadmap with prioritized automation plan",
        estimated_hours="15-20 hours",
    ),
    Offering(
        slug="wa-agent",
        title="WhatsApp AI Agent Setup",
        target_client="Clinics, salons, consultants",
        outcome="Automated lead capture and appointment booking",
        estimated_hours="30-40 hours",
    ),
    Offering(
        slug="clinic-booking",
        title="Appointment and Clinic Booking Automation",
        target_client="Medical, dental, physio, wellness",
        outcome="24/7 booking, reminders, and rescheduling",
        estimated_hours="30-45 hours",
    ),
    Offering(
        slug="voice-receptionist",
        title="Voice AI Receptionist",
        target_client="Clinics, real estate, service businesses",
        outcome="AI call answering, booking, and call logging",
        estimated_hours="40-50 hours",
    ),
    Offering(
        slug="crm-wa-sync",
        title="CRM and WhatsApp Integration",
        target_client="Sales-driven SMEs",
        outcome="Automated lead capture and CRM pipeline sync",
        estimated_hours="25-35 hours",
    ),
    Offering(
        slug="kpi-dashboard",
        title="Analytics Dashboard Setup",
        target_client="SMBs, marketing teams",
        outcome="Executive KPI dashboard with automated refresh",
        estimated_hours="30-40 hours",
    ),
    Offering(
        slug="cloud-setup",
        title="Cloud Infrastructure Setup",
        target_client="Growing startups, SMEs",
        outcome="Production-ready cloud architecture with CI/CD",
        estimated_hours="35-50 hours",
    ),
    Offering(
        slug="data-pipeline",
        title="Data Pipeline Build",
        target_client="Data-driven companies",
        outcome="Automated ingestion, transformation, and storage",
        estimated_hours="35-50 hours",
    ),
    Offering(
        slug="clinic-suite",
        title="Clinic Automation Package",
        target_client="Healthcare businesses",
        outcome="Booking, voice AI, reminders, and dashboard in one system",
        estimated_hours="50-60 hours",
    ),
    Offering(
        slug="real-estate-leads",
        title="Real Estate Lead Automation",
        target_client="Real estate agencies",
        outcome="WhatsApp lead capture, viewing booking, and CRM sync",
        estimated_hours="35-45 hours",
    ),
    Offering(
        slug="custom-ai-agent",
        title="Custom AI Agent Build",
        target_client="SMEs, enterprises",
        outcome="Tailored AI agent for sales, operations, or analytics",
        estimated_hours="40-60 hours",
    ),
]


class OfferingService:
    def __init__(self) -> None:
        self._offerings = OFFERINGS

    def get_all(self) -> List[Offering]:
        return self._offerings

    def get_by_slug(self, slug: str) -> Optional[Offering]:
        for offering in self._offerings:
            if offering.slug == slug:
                return offering
        return None


offering_service = OfferingService()
