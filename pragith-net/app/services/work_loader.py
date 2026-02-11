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
        summary="Led the modernization of a legacy on-prem analytics stack into a cloud-native, scalable data platform supporting real-time ingestion and advanced analytics workloads.",
        stack=["GCP", "BigQuery", "Airflow", "Terraform", "Pub/Sub", "Datadog"],
        industry="Enterprise Analytics",
        role="Principal Architect",
        challenge="The organization relied on fragmented SQL Server + on-prem ETL systems with limited scalability, no CI/CD discipline, and an inability to handle growing data volumes.",
        solution="Designed a target-state cloud-native architecture featuring a data lake, centralized warehouse (BigQuery), and event-driven ingestion. Implemented Infrastructure as Code (Terraform) for reproducibility and introduced CI/CD pipelines (GitHub Actions) for data workflows.",
        outcome="Enabled scalable analytics workloads, standardized deployment workflows, reduced manual data engineering overhead, and significantly improved system reliability and observability."
    ),
    WorkItem(
        slug="ai-marketing-intelligence-platform",
        title="AI-Assisted Marketing Intelligence Platform",
        subtitle="Generative AI & Analytics Architecture",
        summary="Architected an AI-driven analytics platform to support performance marketing insights, automated reporting, and anomaly detection.",
        stack=["Python", "LLMs", "SQL", "Cloud Warehouse", "Machine Learning"],
        industry="MarTech / Media",
        role="Lead Architect",
        challenge="Marketing teams relied on manual BI processes with static dashboards and delayed campaign insights, preventing real-time optimization.",
        solution="Built a scalable ingestion architecture from ad platforms. Implemented ML pipelines for anomaly detection and an LLM-assisted insight summarization layer. Optimized query performance and introduced decision automation workflows.",
        outcome="Faster insight turnaround, reduced manual reporting workload, improved data reliability/governance, and enabled automated decision-making workflows."
    ),
    WorkItem(
        slug="real-time-event-processing",
        title="Real-Time Event Processing Pipeline",
        subtitle="High-Volume Streaming Architecture",
        summary="Designed and deployed a distributed streaming architecture for processing high-volume event data with strict latency requirements.",
        stack=["Kafka", "Dataflow/Spark", "Cloud Warehouse", "Streaming"],
        industry="Real-Time Analytics",
        role="Systems Architect",
        challenge="The existing batch-based pipeline was unable to meet near real-time reporting needs, creating latency in critical business data.",
        solution="Designed a streaming topology using Kafka/Pub/Sub and Dataflow/Spark. Implemented schema evolution controls, enforced IAM security boundaries, and established dead-letter queue handling for reliability.",
        outcome="Reduced data latency from batch to near real-time. Improved pipeline reliability and introduced formal operational runbooks for incident management."
    ),
    WorkItem(
        slug="enterprise-integration-automation",
        title="Enterprise Integration & Document Automation",
        subtitle="Process Automation & Compliance",
        summary="Engineered an automated document ingestion and compliance analysis workflow integrating external APIs and internal systems.",
        stack=["Python", "APIs", "OAuth", "Document Parsing", "Automation"],
        industry="RegTech / Compliance",
        role="Lead Engineer",
        challenge="Manual compliance verification and document processing created significant operational bottlenecks and consistency issues.",
        solution="Designed a secure authentication pipeline (OAuth/MFA). Implemented PDF parsing logic, rule-based clause detection, and automated validation checks. Orchestrated data export workflows with monitoring and retry mechanisms.",
        outcome="Drastically reduced manual review cycles, improved compliance consistency, and standardized reporting outputs."
    ),
    WorkItem(
        slug="devops-platform-standardization",
        title="DevOps Platform Standardization",
        subtitle="Infrastructure & Engineering Velocity",
        summary="Established standardized DevOps workflows, CI/CD pipelines, and containerization standards for cloud-native engineering teams.",
        stack=["Docker", "Kubernetes", "Terraform", "CI/CD", "Observability"],
        industry="Platform Engineering",
        role="Platform Lead",
        challenge="Engineering teams suffered from inconsistent deployments, environment configuration drift, and lack of reproducibility.",
        solution="Defined containerization standards and built modular IaC components. Implemented pipeline gating rules, enforced code review discipline, and integrated security scanning into the CI/CD lifecycle.",
        outcome="Reduced deployment failures, improved environment parity, increased deployment frequency, and significantly boosted engineering productivity."
    ),
    WorkItem(
        slug="ai-orchestrated-development",
        title="AI-Orchestrated Development Workflow",
        subtitle="Internal Developer Platform (IDP)",
        summary="Implemented structured AI-assisted engineering workflows to accelerate feature delivery while maintaining code quality.",
        stack=["GenAI", "Prompt Engineering", "CI/CD Integration", "Developer Tools"],
        industry="Software Engineering",
        role="Architect",
        challenge="Traditional development cycles were bottlenecked by repetitive boilerplate implementation, testing, and documentation tasks.",
        solution="Designed a prompt engineering framework and multi-agent task decomposition system. Implemented automated documentation and test scaffolding generation with human-in-the-loop validation.",
        outcome="Reduced development cycle time, improved documentation quality, and increased consistency in implementation patterns across the team."
    ),
    WorkItem(
        slug="multi-cloud-advisory",
        title="Multi-Cloud Architecture Advisory",
        subtitle="Strategic Technology Consulting",
        summary="Advised executive and engineering stakeholders on multi-cloud strategy, workload distribution, and cost optimization.",
        stack=["AWS", "GCP", "Azure", "FinOps", "Governance"],
        industry="Enterprise Strategy",
        role="Strategic Advisor",
        challenge="The organization was operating across AWS, GCP, and Azure without clear architecture governance, leading to security risks and cost inefficiencies.",
        solution="Conducted an architecture audit and identified cost inefficiencies. Designed a global governance framework, identity harmonization strategy, and cross-cloud networking patterns.",
        outcome="Established a clear cloud governance model, reduced vendor lock-in risk, improved cost visibility, and defined a long-term architecture roadmap."
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
