"""Verified public content for pragith.net.

Unverified metrics belong in editorial notes, never in rendered page data.
"""

CANONICAL_TITLE = "AI Forward Deployed Engineer"
EXPERIENCE_LABEL = "14+ years"

CERTIFICATIONS = [
    "Google Cloud Professional Data Engineer",
    "Google Cloud Professional Cloud Architect",
    "Databricks Certified Data Engineer Associate",
    "Databricks Certified Generative AI Engineer Associate",
    "AWS Certified Cloud Practitioner",
]

CLOUD_PLATFORMS = ["AWS", "Google Cloud", "Microsoft Azure", "Databricks"]

CAPABILITIES = [
    {
        "title": "AI Engineering",
        "summary": "Applied AI systems that connect models to governed data, tools and operational workflows.",
        "href": "/services/ai-systems",
    },
    {
        "title": "Data Platforms",
        "summary": "Batch, streaming and analytics platforms designed for reliability, traceability and practical ownership.",
        "href": "/services#data-platforms",
    },
    {
        "title": "Cloud / MLOps / DevOps",
        "summary": "Cloud architecture, delivery automation, observability and production support across major platforms.",
        "href": "/services#cloud-platforms",
    },
    {
        "title": "Technical Education",
        "summary": "Workshops, graduate instruction and team enablement grounded in real engineering constraints.",
        "href": "/teaching",
    },
]

CASE_STUDIES = [
    {
        "slug": "enterprise-data-platform",
        "title": "Enterprise data platform operations",
        "preview": "Operating and improving a multi-cloud analytics estate processing multi-terabyte workloads through hundreds of pipelines.",
        "context": "A large enterprise analytics environment supported high-volume reporting, modelling and downstream decision systems.",
        "constraint": "The platform had to remain reliable while releases, schema changes and upstream dependencies continued to evolve.",
        "role": "I worked across platform operations, data engineering, release automation and production incident resolution.",
        "architecture": "Cloud data storage and compute, orchestrated batch pipelines, SQL and Python transformation layers, CI/CD and centralized observability.",
        "implementation": "I improved deployment workflows, investigated pipeline failures, supported data consumers and strengthened monitoring around critical processing paths.",
        "result": "The platform supported multi-terabyte daily processing across hundreds of pipelines with clearer operational ownership and repeatable releases.",
        "technologies": ["Python", "SQL", "Google Cloud", "AWS", "Airflow", "Databricks", "CI/CD"],
        "lessons": "Platform reliability depends as much on ownership, release discipline and observability as it does on individual technologies.",
    },
    {
        "slug": "event-driven-data-systems",
        "title": "Near-real-time and event-driven data systems",
        "preview": "Designing cloud data flows for operational systems where freshness, resilience and traceability mattered.",
        "context": "Operational applications needed timely data movement between source systems, cloud services and downstream consumers.",
        "constraint": "The integration had to tolerate partial failures, variable event volume and sensitive operational data.",
        "role": "I led technical design and implementation across ingestion, processing, reliability controls and deployment.",
        "architecture": "Event-driven ingestion, streaming and asynchronous processing, durable storage, API integration and monitored delivery pipelines.",
        "implementation": "I designed processing boundaries, retry behaviour, deployment automation and operational checks for data movement and downstream availability.",
        "result": "The resulting system supported timely operational data delivery with explicit failure handling and traceable processing stages.",
        "technologies": ["Python", "Kafka", "Pub/Sub", "Cloud Run", "Dataflow", "APIs", "Docker"],
        "lessons": "Near-real-time architecture is valuable only when replay, failure isolation and operational support are designed with the happy path.",
    },
    {
        "slug": "ai-mlops-automation",
        "title": "AI and MLOps delivery automation",
        "preview": "Moving AI capabilities from internal prototypes into observable, controlled engineering workflows.",
        "context": "An enterprise team was introducing AI-assisted capabilities into existing analytics and engineering workflows.",
        "constraint": "Model behaviour, access, cost and failure modes needed to fit established delivery and support practices.",
        "role": "I contributed architecture, implementation, production support and release automation for the AI platform and an internal assistant.",
        "architecture": "Model and tool orchestration, governed data access, API services, structured outputs, evaluation hooks, CI/CD and operational telemetry.",
        "implementation": "I connected models to approved tools and data, added deployment controls, supported production debugging and helped define reliable operating boundaries.",
        "result": "The team gained a supportable path for deploying AI-assisted workflows without treating model output as automatically correct.",
        "technologies": ["Python", "FastAPI", "LLMs", "MLflow", "Docker", "Kubernetes", "CI/CD"],
        "lessons": "Useful enterprise AI combines model capability with evaluation, permissions, human approval and conventional software operations.",
    },
    {
        "slug": "regulated-integrations",
        "title": "Governance-sensitive data integrations",
        "preview": "Building traceable data pipelines for sensitive forensic, regulatory and healthcare-adjacent workloads.",
        "context": "Sensitive datasets had to move through analytical workflows while preserving auditability and controlled access.",
        "constraint": "Engineering decisions needed to account for traceability, repeatability, restricted data and governance review.",
        "role": "I designed and implemented data processing and integration workflows in collaboration with domain, security and governance stakeholders.",
        "architecture": "Controlled ingestion, validation, transformation and reporting layers with access boundaries, logs and reproducible processing.",
        "implementation": "I built auditable pipelines, documented data handling, supported validation and worked with cross-functional reviewers on operational controls.",
        "result": "The workflows made sensitive analytical processing more repeatable, reviewable and supportable.",
        "technologies": ["Python", "SQL", "Cloud storage", "ETL", "Data validation", "Access controls"],
        "lessons": "In governance-sensitive environments, documentation and traceability are part of the system rather than a final compliance exercise.",
    },
    {
        "slug": "executive-analytics",
        "title": "Executive analytics and semantic reporting",
        "preview": "Connecting operational sources to governed models and decision-focused dashboards.",
        "context": "Leadership and operational teams needed consistent measures across several source systems and reporting audiences.",
        "constraint": "Definitions, refresh behaviour and access had to remain understandable beyond the original dashboard implementation.",
        "role": "I worked across source integration, modelling, dashboard delivery and stakeholder enablement.",
        "architecture": "Source connectors, transformation models, governed metrics, semantic layers and role-aware dashboards with scheduled or near-real-time refresh.",
        "implementation": "I aligned measures with decision needs, built reusable models and documented ownership from source through presentation.",
        "result": "Stakeholders received a clearer path from operational data to consistent, maintainable executive reporting.",
        "technologies": ["SQL", "Python", "Looker", "Apache Superset", "Cloud warehouses", "Semantic modelling"],
        "lessons": "An executive dashboard is credible when metric definitions, lineage and ownership are as clear as its visual presentation.",
    },
    {
        "slug": "engineering-enablement",
        "title": "Engineering education and enablement",
        "preview": "Teaching data science, machine learning, cloud and data engineering through applied programs and workshops.",
        "context": "Learners and engineering teams needed practical instruction that connected concepts to deployable systems.",
        "constraint": "Programs had to serve mixed experience levels while retaining technical depth and useful assessment.",
        "role": "I served as a lead instructor, graduate-level educator, workshop organizer and technical mentor.",
        "architecture": "Project-led curricula spanning Python, statistics, machine learning, APIs, cloud data systems, dashboards and engineering practices.",
        "implementation": "I designed lessons, delivered live instruction, reviewed projects and adapted examples to learner and team needs.",
        "result": "Participants received structured, applied learning across data, AI and cloud engineering topics.",
        "technologies": ["Python", "SQL", "R", "Machine learning", "Cloud platforms", "APIs", "BI"],
        "lessons": "Technical education works best when learners can connect architecture decisions to code, operations and real constraints.",
    },
]

PROJECTS = [
    {
        "slug": "headmaster",
        "title": "Headmaster",
        "status": "Beta",
        "summary": "A portable, OIDC-gated administration interface for Headscale with nodes, users, routes, policy and audit workflows.",
        "version": "0.1.1",
        "href": "https://github.com/Pragith/headmaster",
        "link_label": "View repository",
    },
    {
        "slug": "caffeinate-d",
        "title": "Caffeinate-d",
        "status": "Beta",
        "summary": "A small native macOS menu-bar wrapper for the system caffeinate command.",
        "version": "Source version 0.2.0",
        "href": "/projects/caffeinate-d",
        "link_label": "Project details",
    },
    {
        "slug": "agent-keyboard",
        "title": "Agent Keyboard",
        "status": "Prototype",
        "summary": "A browser interaction prototype for a tactile coding-agent control deck. The CLI bridge is not implemented.",
        "version": "Browser prototype",
        "href": "/projects/agent-keyboard/",
        "link_label": "Open prototype",
    },
]

EXPERIENCE = [
    {
        "period": "2024–present",
        "title": "AI systems and enterprise platform delivery",
        "context": "Enterprise marketing and analytics technology",
        "body": "Architecture, implementation and production support for AI-assisted workflows, multi-cloud data platforms, internal tooling, CI/CD and observability. Work includes an internal AI assistant and an analytics estate processing multi-terabyte daily workloads through hundreds of pipelines.",
    },
    {
        "period": "2021–2024",
        "title": "Data operations, business intelligence and platform reliability",
        "context": "Large-scale enterprise analytics",
        "body": "Operational ownership across cloud data processing, release automation, dashboard systems, incident investigation and reliability improvements for high-volume analytical workloads.",
    },
    {
        "period": "2021",
        "title": "Cloud data and applied research leadership",
        "context": "Healthcare-adjacent operational software",
        "body": "Led technical quality and applied data research, including event-driven integrations, real-time cloud pipelines, delivery automation and governance-sensitive operational controls.",
    },
    {
        "period": "2017–2021",
        "title": "Data science and analytics consulting",
        "context": "Global consulting and regulated environments",
        "body": "Designed cloud analytics, modelling and compliance-grade processing for enterprise and Fortune 500 environments, including sensitive forensic and regulatory datasets requiring auditability and traceability.",
    },
    {
        "period": "2015–2017",
        "title": "Enterprise data science and operational analytics",
        "context": "Global technology services",
        "body": "Built analytical systems over high-volume operational and log data, with responsibility for modelling, implementation, performance investigation and stakeholder delivery.",
    },
    {
        "period": "2012–2015",
        "title": "Data analysis and platform foundations",
        "context": "Digital services and early-stage data products",
        "body": "Worked across reporting, backend development, real-time analytics and the foundations of production data platforms using Python, SQL, R and distributed processing tools.",
    },
]

SERVICES = [
    ("ai-systems", "AI Engineering and Agentic Systems", "Model and tool orchestration, retrieval, structured output, evaluation, observability, approval gates and secure integration with business systems."),
    ("data-platforms", "Data Platform Engineering", "Architecture and implementation for batch, streaming, lakehouse, warehouse and analytics platforms, including reliability and ownership."),
    ("cloud-platforms", "MLOps, DevOps and Cloud Architecture", "Delivery automation, infrastructure as code, model operations, containers, observability and production debugging across AWS, Google Cloud, Azure and Databricks."),
    ("forward-deployed", "Forward-Deployed Engineering", "Hands-on work alongside product, security, data and platform teams to move from an ambiguous problem to an operating system."),
    ("analytics", "Analytics and Executive BI", "Source integration, governed data models, semantic layers, decision-focused dashboards and maintainable reporting operations."),
    ("training", "Engineering Training and Enablement", "Technical workshops, curriculum development, team enablement and applied instruction across data, AI, cloud and software delivery."),
]

INDEXABLE_PATHS = [
    "/", "/about", "/experience", "/case-studies", "/services",
    "/services/ai-systems", "/services/executive-bi", "/teaching",
    "/projects", "/resume", "/writing",
    "/contact", "/business", "/privacy", "/legal",
]
INDEXABLE_PATHS.extend(f"/case-studies/{item['slug']}" for item in CASE_STUDIES)
