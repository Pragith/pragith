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
    role: str
    challenge: str
    solution: str
    outcome: str

WORK_ITEMS = [
    # ─── Flagship Projects ───────────────────────────────────────────────
    WorkItem(
        slug="network-bandwidth-prediction",
        title="Network Bandwidth Prediction Engine",
        subtitle="Predictive Analytics Dashboard",
        summary="Built a predictive dashboard forecasting bandwidth consumption across every network device, with drill-down to individual interfaces and directional traffic patterns.",
        stack=["R", "QlikView", "SQL Server"],
        industry="Telecommunications / Enterprise IT",
        role="Solo contributor",
        challenge="The organization was over-provisioning bandwidth across hundreds of network devices, leading to significant cost overruns with ISPs. There was no visibility into future consumption patterns at the interface level.",
        solution="Developed a predictive analytics engine using Simple Moving Average with seasonality and intersection analysis. Built an interactive dashboard with drill-down capability from device level to individual interface/link, segmented by inbound and outbound traffic over configurable time windows.",
        outcome="Delivered high cost savings by enabling precise bandwidth subscription with ISPs. Recognized with appreciation from top management."
    ),
    WorkItem(
        slug="it-events-prediction",
        title="IT Events Prediction System",
        subtitle="Capacity & Staffing Intelligence",
        summary="Predictive system enabling proactive capacity management and optimal engineer staffing by forecasting IT events across multiple operational dimensions.",
        stack=["R", "Excel", "QlikView"],
        industry="Enterprise IT / Operations",
        role="Team effort",
        challenge="Reactive incident management was causing SLA breaches and inefficient staffing. A previously written prediction script took 5 hours to execute, making it impractical for operational use.",
        solution="Re-wrote the entire business logic from scratch, reducing execution time from 5 hours to 1 minute. Built multi-dimensional prediction across Category, Type, Item, and other operational dimensions using SMA with seasonality and intersection analysis.",
        outcome="Enabled proactive prevention of IT events before occurrence. Optimized engineer staffing based on forecasted demand, preventing understaffing during peak periods."
    ),
    WorkItem(
        slug="automation-candidate-classifier",
        title="NLP-Based Automation Candidate Classifier",
        subtitle="Text Analytics & Decision Intelligence",
        summary="An NLP solution that automatically classifies IT incident dumps to identify automation candidates, enabling Project Managers to make data-driven automation investment decisions.",
        stack=["R", "Python", "Shiny", "NLP"],
        industry="IT Service Management",
        role="Solo contributor",
        challenge="Onboarding new customers required weeks to months of manual analysis to identify which IT processes could be automated. This bottleneck limited the organization's ability to scale.",
        solution="Built a text analytics pipeline using Part-of-Speech tagging, TF-IDF vectorization, and Topic Modeling to automatically classify incident records. Deployed as an interactive Shiny dashboard with real-time classification capabilities.",
        outcome="Reduced customer onboarding timeline from weeks/months to days. Enabled rapid identification of automation opportunities across multiple customer bases."
    ),
    WorkItem(
        slug="anomaly-detection-dashboard",
        title="Time-Series Anomaly Detection Engine",
        subtitle="SAX Algorithm Implementation",
        summary="Research-grade anomaly detection system implementing the SAX algorithm from scratch for identifying anomalies in time-series data across performance monitoring and sensor networks.",
        stack=["R", "Shiny"],
        industry="Cross-Industry / Research",
        role="Solo contributor",
        challenge="Standard threshold-based monitoring generated excessive noise and missed subtle anomalies in time-series data from performance monitors and IoT sensors.",
        solution="Implemented the Symbolic Aggregate approXimation (SAX) algorithm from a published research paper, built entirely from scratch in R. Deployed as a hosted Shiny application.",
        outcome="Enabled detection of complex temporal anomalies across multiple data domains including infrastructure performance monitoring and sensor telemetry."
    ),
    WorkItem(
        slug="merchant-analysis-dashboard",
        title="Enterprise Merchant Analysis Platform",
        subtitle="Sales Intelligence Dashboard",
        summary="Cross-functional sales intelligence dashboard providing product performance insights across categories, built in collaboration with senior leadership and business analysts.",
        stack=["Excel", "SQL", "Pivots"],
        industry="Payments / FinTech",
        role="Team effort",
        challenge="Executive leadership lacked visibility into how internal product lines were performing across categories over time. Decision-making on product strategy was largely intuition-driven.",
        solution="Collaborated with Senior Business Analysts, Product Managers, Product Directors, VP of Sales, and Senior Data Analysts. Introduced Excel Slicers with Pivot Tables (first in the team) and wrote optimized SQL queries for data extraction.",
        outcome="Enabled data-driven product strategy decisions — identification of underperforming products for deprecation and high-performing products for investment."
    ),

    # ─── Additional Projects ─────────────────────────────────────────────
    WorkItem(
        slug="provisioning-bot",
        title="Provisioning Automation Bot",
        subtitle="Process Automation",
        summary="Automated provisioning workflow that eliminated manual setup steps, recognized with appreciation from top management.",
        stack=["Python"],
        industry="Enterprise IT",
        role="Solo contributor",
        challenge="Manual provisioning processes were time-consuming, error-prone, and a bottleneck for service delivery.",
        solution="Built an end-to-end automation bot in Python that handled the complete provisioning workflow with error handling and audit logging.",
        outcome="Eliminated manual provisioning overhead. Recognized with appreciation from top management for delivery speed and reliability."
    ),
    WorkItem(
        slug="rtb-publisher-dashboard",
        title="Real-Time Bidding Publisher Dashboard",
        subtitle="AdTech Analytics Prototype",
        summary="Prototype analytics dashboard for real-time ad bidding publisher performance, demonstrating data visualization capabilities for the programmatic advertising pipeline.",
        stack=["Excel", "PowerPoint", "SQL"],
        industry="AdTech / Programmatic Advertising",
        role="Solo contributor",
        challenge="Publishers lacked real-time visibility into bidding performance metrics, making it difficult to optimize ad inventory.",
        solution="Designed and developed a prototype dashboard showcasing key RTB metrics with drill-down capabilities and trend analysis.",
        outcome="Validated the dashboard concept for stakeholder buy-in, establishing the foundation for production development."
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
