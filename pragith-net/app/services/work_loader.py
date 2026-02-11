from typing import List, Optional
from pydantic import BaseModel

class WorkItem(BaseModel):
    slug: str
    title: str
    subtitle: str
    summary: str
    hero_image: Optional[str] = None
    stack: List[str]
    industry: str
    challenge: str
    solution: str
    outcome: str

# Mock data for now, ideally this could come from YAML/Markdown too
WORK_ITEMS = [
    WorkItem(
        slug="enterprise-data-platform",
        title="Validating Enterprise Data Platforms",
        subtitle="Multi-Cloud Analytics Architecture",
        summary="Architected a 50TB+ daily data platform for a Fortune 500 retailer.",
        stack=["GCP", "BigQuery", "Dataflow", "Airflow", "Terraform"],
        industry="Retail / E-commerce",
        challenge="Legacy on-premise hadoop cluster was failing to meet SLAs for daily reporting, causing 48-hour delays in executive insights.",
        solution="Designed and implemented a serverless lakehouse on GCP using BigQuery and Dataflow. Migrated 5PB of historical data with zero downtime.",
        outcome="Reduced report latency from 48 hours to 15 minutes. Cut infrastructure costs by 40%."
    ),
    WorkItem(
        slug="real-time-fraud-detection",
        title="Real-Time Fraud Detection System",
        subtitle="Streaming AI Architecture",
        summary="Built a sub-second fraud detection engine processing 10k TPS.",
        stack=["AWS", "Kinesis", "Lambda", "DynamoDB", "Rust"],
        industry="FinTech",
        challenge="Rule-based fraud system was generating high false positives and missing sophisticated bot attacks.",
        solution="Implemented an event-driven architecture using Kinesis and Lambda. Deployed a custom anomaly detection model accessible via low-latency API.",
        outcome="Prevented $2M+ in fraud losses in Q1. Reduced false positive rate by 60%."
    ),
]

class WorkService:
    def get_all(self) -> List[WorkItem]:
        return WORK_ITEMS
    
    def get_by_slug(self, slug: str) -> Optional[WorkItem]:
        for item in WORK_ITEMS:
            if item.slug == slug:
                return item
        return None

work_service = WorkService()
