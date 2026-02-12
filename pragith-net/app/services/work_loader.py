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
    # ─── Enterprise Architecture & AI ─────────────────────────────────────
    WorkItem(
        slug="enterprise-cloud-data-platform",
        title="Enterprise Cloud Data Platform Modernization",
        subtitle="Legacy-to-Cloud Migration & Architecture",
        summary="Migrated a legacy on-prem analytics stack to GCP, reducing query times by 73% and cutting infrastructure costs by $180K annually.",
        stack=["GCP", "BigQuery", "Airflow", "Terraform", "Pub/Sub", "Datadog"],
        industry="Enterprise Analytics",
        role="Principal Architect",
        challenge="The organization relied on fragmented SQL Server + on-prem ETL systems processing 2.4TB daily with 6-12 hour batch windows, preventing real-time analytics and costing $42K/month in infrastructure.",
        solution="Designed cloud-native architecture with BigQuery warehouse, event-driven ingestion via Pub/Sub, and Terraform-managed infrastructure. Migrated 47 data pipelines to Airflow with CI/CD automation, implemented incremental loading patterns, and established monitoring with Datadog.",
        outcome="Reduced query response time from 8-12 minutes to 2-3 minutes (73% improvement). Cut infrastructure costs by $15K/month ($180K annually). Enabled real-time dashboards with <5 minute data freshness. Deployment time reduced from 4 hours to 12 minutes."
    ),
    WorkItem(
        slug="ai-marketing-intelligence-platform",
        title="AI-Assisted Marketing Intelligence Platform",
        subtitle="Generative AI & Analytics Architecture",
        summary="Built an AI-driven marketing analytics platform that automated 85% of manual reporting tasks and reduced campaign optimization cycles from 3 days to 4 hours.",
        stack=["Python", "LLMs", "SQL", "Cloud Warehouse", "Machine Learning"],
        industry="MarTech / Media",
        role="Lead Architect",
        challenge="Marketing team of 12 spent 120+ hours weekly on manual report generation across 8 ad platforms, with campaign insights delayed by 2-3 days, preventing real-time budget optimization on $2.3M monthly ad spend.",
        solution="Built automated ingestion from Google Ads, Facebook, LinkedIn APIs processing 340K daily events. Implemented ML anomaly detection (95% accuracy) for spend/performance outliers. Created LLM-powered insight summarization reducing 40-page reports to 2-page executive summaries. Optimized warehouse queries reducing costs by 62%.",
        outcome="Automated 85% of manual reporting (102 hours/week saved). Reduced insight delivery from 3 days to 4 hours. Detected $47K in wasted ad spend in first month. Improved campaign ROAS by 23% through faster optimization cycles. Warehouse query costs reduced from $8.2K to $3.1K monthly."
    ),
    WorkItem(
        slug="real-time-event-processing",
        title="Real-Time Event Processing Pipeline",
        subtitle="High-Volume Streaming Architecture",
        summary="Deployed a distributed streaming architecture processing 12M events/day with 99.7% reliability, reducing data latency from 6 hours to 90 seconds.",
        stack=["Kafka", "Dataflow/Spark", "Cloud Warehouse", "Streaming"],
        industry="Real-Time Analytics",
        role="Systems Architect",
        challenge="Batch pipeline processed 12M daily events with 6-hour latency, preventing real-time fraud detection and operational monitoring. System reliability was 94.2% with frequent data quality issues.",
        solution="Designed Kafka-based streaming topology with 3-node cluster handling 4.2K events/second peak throughput. Implemented Dataflow jobs with exactly-once semantics, schema validation, and dead-letter queue handling. Established monitoring with 15-minute SLA alerts and automated recovery procedures.",
        outcome="Reduced data latency from 6 hours to 90 seconds (99.6% improvement). Improved pipeline reliability to 99.7% uptime. Enabled real-time fraud detection saving estimated $120K in first quarter. Processing cost reduced by 34% through autoscaling optimization. Zero data loss incidents in 8 months post-deployment."
    ),
    WorkItem(
        slug="enterprise-integration-automation",
        title="Enterprise Integration & Document Automation",
        subtitle="Process Automation & Compliance",
        summary="Automated compliance document processing, reducing review cycles from 5 days to 3 hours and improving accuracy from 87% to 98.5%.",
        stack=["Python", "APIs", "OAuth", "Document Parsing", "Automation"],
        industry="RegTech / Compliance",
        role="Lead Engineer",
        challenge="Compliance team manually reviewed 180 documents monthly (PDF contracts, regulatory filings) taking 5-7 days per batch with 87% accuracy rate, creating bottlenecks in client onboarding and regulatory reporting.",
        solution="Built secure OAuth 2.0 integration with document management system. Implemented PDF parsing with clause extraction (92% accuracy), rule-based validation against 47 compliance criteria, and automated flagging system. Created export workflows with retry logic and audit trails.",
        outcome="Reduced review cycle from 5 days to 3 hours (96% faster). Improved accuracy from 87% to 98.5%. Processed 180 documents/month vs. previous 120 (50% throughput increase). Saved 156 hours/month in manual review time. Zero compliance violations in 6 months post-deployment vs. 3-4 quarterly before."
    ),
    WorkItem(
        slug="devops-platform-standardization",
        title="DevOps Platform Standardization",
        subtitle="Infrastructure & Engineering Velocity",
        summary="Standardized DevOps workflows across 4 engineering teams, reducing deployment failures by 68% and increasing release frequency from weekly to daily.",
        stack=["Docker", "Kubernetes", "Terraform", "CI/CD", "Observability"],
        industry="Platform Engineering",
        role="Platform Lead",
        challenge="Four engineering teams (32 developers) used inconsistent deployment processes with 31% deployment failure rate, 4.2 hour average rollback time, and weekly release cadence limiting business agility.",
        solution="Defined containerization standards with base images and security scanning. Built 23 reusable Terraform modules for infrastructure provisioning. Implemented CI/CD pipelines with automated testing gates, canary deployments, and rollback automation. Integrated Datadog monitoring with SLO tracking.",
        outcome="Reduced deployment failures from 31% to 9.8% (68% improvement). Decreased rollback time from 4.2 hours to 22 minutes. Increased deployment frequency from 1x/week to 8x/week. Improved mean time to recovery (MTTR) from 3.1 hours to 35 minutes. Developer satisfaction score increased from 6.2 to 8.7/10."
    ),
    WorkItem(
        slug="ai-orchestrated-development",
        title="AI-Orchestrated Development Workflow",
        subtitle="Internal Developer Platform (IDP)",
        summary="Implemented AI-assisted development workflows reducing feature delivery time by 42% while maintaining 96% code quality standards.",
        stack=["GenAI", "Prompt Engineering", "CI/CD Integration", "Developer Tools"],
        industry="Software Engineering",
        role="Architect",
        challenge="Development team spent 38% of time on boilerplate code, test writing, and documentation. Average feature delivery: 8.3 days. Code review cycles: 2.1 days. Documentation coverage: 64%.",
        solution="Designed prompt engineering framework with task decomposition for code generation, test scaffolding, and documentation. Implemented human-in-the-loop validation with automated quality gates. Created reusable prompt templates for 12 common patterns. Integrated with existing CI/CD for automated PR generation.",
        outcome="Reduced average feature delivery from 8.3 to 4.8 days (42% improvement). Increased documentation coverage from 64% to 91%. Reduced code review time from 2.1 to 1.3 days. Maintained code quality score of 96% (vs. 94% baseline). Generated 2,400+ lines of production code in first month with 89% acceptance rate."
    ),
    WorkItem(
        slug="multi-cloud-advisory",
        title="Multi-Cloud Architecture Advisory",
        subtitle="Strategic Technology Consulting",
        summary="Advised on multi-cloud strategy optimization, identifying $340K in annual cost savings and reducing security vulnerabilities by 76%.",
        stack=["AWS", "GCP", "Azure", "FinOps", "Governance"],
        industry="Enterprise Strategy",
        role="Strategic Advisor",
        challenge="Organization operated 340+ resources across AWS, GCP, and Azure with no governance framework. Cloud spend: $1.2M annually with 28% waste. 47 critical security findings. No disaster recovery plan.",
        solution="Conducted architecture audit across 3 clouds identifying cost inefficiencies, security gaps, and architectural inconsistencies. Designed unified governance framework with identity federation, cross-cloud networking patterns, and FinOps tagging strategy. Created 18-month migration roadmap prioritizing quick wins.",
        outcome="Identified $340K annual cost savings (28% reduction) through rightsizing and reserved instances. Reduced critical security findings from 47 to 11 (76% improvement). Established cloud center of excellence with governance policies. Implemented disaster recovery plan with 4-hour RTO. Reduced vendor lock-in risk through standardized abstraction patterns."
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
