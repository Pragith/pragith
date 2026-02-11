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
    WorkItem(
        slug="enterprise-mcp-server",
        title="Enterprise Context MCP Server",
        subtitle="Model Context Protocol Implementation",
        summary="Built a secure MCP server to expose internal APIs and documentation to AI agents and LLM clients.",
        stack=["Python", "MCP SDK", "FastAPI", "OAuth2", "Docker"],
        industry="Internal Tools / Developer Experience",
        challenge="Engineers wasted 20% of their time context-switching to find documentation and query distributed system status dashboards.",
        solution="Developed a custom MCP server integrating Jira, Confluence, and Prometheus. Enabled natural language queries for system status and docs directly within the IDE and Claude Desktop.",
        outcome="Reduced 'how do I' questions by 40%. Enabled zero-context onboarding for new hires by providing instant access to institutional knowledge."
    ),
    WorkItem(
        slug="data-exchange-optimization",
        title="High-Performance Data Exchange",
        subtitle="Binary Protocol Optimization",
        summary="Eliminated serialization bottlenecks in a 100TB+ data platform by moving from JSON to Apache Arrow Flight.",
        stack=["Apache Arrow", "gRPC", "Python", "Rust", "Kubernetes"],
        industry="AdTech / Real-Time Bidding",
        challenge="Downstream ML models were starving for data because the JSON-over-HTTP API couldn't keep up with 50GB/hour ingestion rates.",
        solution="Re-architected the internal data mesh to use Apache Arrow Flight (binary stream) instead of REST. Implemented zero-copy reads for local consumers.",
        outcome="Increased data throughput by 15x. Reduced compute costs by eliminating 90% of serialization/deserialization CPU cycles."
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
