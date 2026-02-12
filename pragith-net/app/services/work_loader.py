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
    # ─── Data Science & Analytics ─────────────────────────────────────
    WorkItem(
        slug="network-bandwidth-prediction",
        title="Network Bandwidth Prediction Dashboard",
        subtitle="Predictive Analytics & Cost Optimization",
        summary="Built a predictive dashboard displaying network bandwidth consumption forecasts at every device with drill-down capability, enabling high cost savings through optimized ISP subscriptions.",
        stack=["R", "Qlikview", "SQL Server"],
        industry="IT Operations",
        role="Solo Contributor",
        challenge="Organization lacked visibility into future bandwidth requirements across network devices, leading to over-provisioning and excessive costs from internet service providers. No drill-down capability to analyze consumption patterns at interface/link level or distinguish inward vs. outward traffic.",
        solution="Implemented predictive models using Simple Moving Average with Seasonality & Intersection Analysis in R. Created interactive Qlikview dashboard with drill-down capability to device, interface, and directional traffic levels. Integrated with SQL Server for historical consumption data and forecast storage.",
        outcome="Received appreciation from top management. Enabled high cost savings by subscribing for only required bandwidth from ISP. Provided granular visibility into bandwidth consumption patterns over time with drill-down to interface/link level and traffic direction."
    ),
    WorkItem(
        slug="it-events-prediction",
        title="IT Events Prediction Dashboard",
        subtitle="Proactive Capacity Management & Staffing",
        summary="Developed a predictive dashboard for IT events across multiple dimensions, enabling proactive capacity management and optimal engineer staffing. Reduced execution time from 5 hours to 1 minute through complete business logic rewrite.",
        stack=["R", "Excel", "Qlikview"],
        industry="IT Operations",
        role="Team Contributor",
        challenge="IT operations lacked predictive insights into future events across dimensions like Category, Type, and Item. Previous implementation had 5-hour execution time making it impractical for operational use. Reactive approach prevented proactive measures in capacity management and staffing.",
        solution="Re-wrote entire business logic from scratch after inheriting poorly performing script. Implemented Simple Moving Average with Seasonality & Intersection Analysis in R. Created multi-dimensional dashboard in Qlikview displaying predicted IT events over time across Category, Type, Item, and other dimensions.",
        outcome="Reduced execution time from 5 hours to 1 minute (99.7% improvement). Enabled proactive prevention of IT events. Optimized engineer staffing for foreseen events. Provided actionable insights for capacity management decisions across multiple operational dimensions."
    ),
    WorkItem(
        slug="automation-candidate-dashboard",
        title="Automation Candidate Dashboard",
        subtitle="NLP-Based IT Incident Classification",
        summary="Created an NLP-based solution automatically classifying IT incident dumps into categories, helping Project Managers identify automation candidates and drastically reducing customer onboarding time from weeks to days.",
        stack=["R", "Python", "Excel", "Shiny"],
        industry="IT Service Management",
        role="Solo Contributor",
        challenge="Project Managers needed to manually analyze IT incident dumps to identify automation candidates, taking weeks to months per customer. This slow process limited ability to onboard new customers and scale automation projects across the organization.",
        solution="Built NLP classification system using Text Analytics (Part-of-Speech, TF-IDF, Topic Modeling) in R and Python. Developed interactive Shiny dashboard for visualization and decision support. Implemented Machine Learning techniques to continuously improve classification accuracy. Created automated categorization of incidents to suggest automation potential.",
        outcome="Drastically reduced customer onboarding time from weeks & months to days. Enabled Project Managers to make informed decisions on automation candidates. Brought in more projects from multiple customers within short periods. Dashboard hosted and actively used for new customer evaluations."
    ),
    WorkItem(
        slug="anomaly-detection-dashboard",
        title="Anomaly Detection Dashboard (SAX Algorithm)",
        subtitle="Time-Series Anomaly Detection",
        summary="Pure R implementation of SAX algorithm from research paper for identifying anomalies in time-series data through an interactive Shiny dashboard, hosted on Shinyapps.io.",
        stack=["R", "Shiny", "SAX Algorithm"],
        industry="Data Analytics",
        role="Solo Contributor",
        challenge="Organization needed a robust method to identify anomalies in various types of time-series data including performance monitoring metrics and sensor data. Required implementation of academic research (SAX algorithm) into production-ready tool accessible to non-technical users.",
        solution="Implemented SAX (Symbolic Aggregate approXimation) algorithm from scratch in pure R based on research paper. Built interactive Shiny dashboard for visualization and anomaly detection. Deployed to Shinyapps.io for cloud-based access. Designed for multiple data types including performance monitoring and sensor data.",
        outcome="Successfully deployed production-ready anomaly detection system. Enabled identification of anomalies across multiple data types (performance monitoring, sensors). Provided accessible interface for non-technical users. Hosted on Shinyapps.io for organization-wide access."
    ),
    WorkItem(
        slug="merchant-analysis-dashboard",
        title="Merchant Analysis Dashboard",
        subtitle="Product Performance Analytics",
        summary="Collaborated with Senior Business Analysts, Product Managers, Directors, and VP of Sales to create an Excel dashboard showcasing internal product sales performance across categories, enabling strategic product decisions.",
        stack=["Excel", "SQL"],
        industry="Retail / Product Analytics",
        role="Team Contributor",
        challenge="Stakeholders lacked visibility into how internal products were performing over time across different product categories. Needed interactive dashboard to support strategic decisions on product portfolio management, including shelving underperforming products and pushing well-performing ones.",
        solution="Introduced Excel Slicers with Pivots for the first time in the team to create interactive dashboard. Wrote optimized SQL queries to pull sales data efficiently. Collaborated with Senior Business Analysts, Product Managers, Product Directors, VP of Sales, and Senior Data Analysts to define metrics and visualizations.",
        outcome="Helped stakeholders take appropriate decisions such as shelving underperforming products and pushing well-performing products. Provided interactive analysis capability through Excel Slicers. Improved data retrieval performance through optimized SQL queries. Established new dashboard standard for the team."
    ),
    WorkItem(
        slug="provisioning-bot",
        title="Provisioning Bot",
        subtitle="IT Automation & Process Efficiency",
        summary="Developed an automated provisioning bot using Python that streamlined IT resource provisioning processes, receiving appreciation from top management.",
        stack=["Python", "Automation"],
        industry="IT Operations",
        role="Solo Contributor",
        challenge="Manual IT resource provisioning processes were time-consuming, error-prone, and created bottlenecks in service delivery. Required consistent, repeatable automation to improve efficiency and reduce human error.",
        solution="Built automated provisioning bot in Python handling resource allocation and configuration tasks. Implemented error handling and logging for reliability. Designed for integration with existing IT systems and workflows.",
        outcome="Received appreciation from top management. Streamlined IT resource provisioning processes. Reduced manual effort and human error in provisioning workflows. Improved service delivery speed and consistency."
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
