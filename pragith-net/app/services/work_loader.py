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
    # ─── Enterprise Data & AI Platforms (2021-Present) ─────────────────────────────────────
    WorkItem(
        slug="tinuiti-enterprise-analytics-platform",
        title="Enterprise Analytics & AI Platform Operations",
        subtitle="Multi-Terabyte Data Platform Architecture",
        summary="Architected and operated enterprise-scale analytics platforms processing multi-terabyte datasets daily across 100+ global marketing clients, supporting 500+ automated pipelines with 99.5%+ reliability.",
        stack=["GCP", "BigQuery", "Airflow", "Python", "Terraform", "CI/CD", "Dataflow"],
        industry="MarTech / Digital Marketing",
        role="Senior AI Ops Engineer / Senior BI Engineer",
        challenge="Organization needed to scale analytics infrastructure supporting 100+ enterprise clients processing 5-10TB daily data volumes. Legacy systems had 92-94% pipeline reliability with 8-12 hour deployment cycles. Manual operations required 40+ hours weekly for monitoring and incident response across ingestion, transformation, analytics, and activation layers.",
        solution="Architected cloud-native data platform on GCP with BigQuery warehouse, Airflow orchestration (500+ DAGs), and Terraform-managed infrastructure. Implemented CI/CD automation enabling 3-5 production deployments per week. Built near-real-time decisioning workflows for media optimization across multiple geographic regions. Established observability framework with automated alerting and self-healing mechanisms.",
        outcome="Achieved 99.5%+ platform reliability (vs. 92-94% baseline). Reduced deployment cycles from 8-12 hours to 45-60 minutes (85-92% improvement). Enabled multiple production deployments per week (3-5x vs. weekly previously). Processed 5-10TB daily across 100+ clients with <15 minute data freshness SLA. Reduced manual operations effort by 60-70% through automation. Supported near-real-time media optimization workflows across 15+ geographic regions."
    ),
    WorkItem(
        slug="sofvie-healthcare-data-pipelines",
        title="Real-Time Healthcare Data Pipelines",
        subtitle="Production Healthcare Workflows & Compliance",
        summary="Delivered real-time cloud data pipelines supporting production healthcare workflows with 99.8% reliability, processing 50K+ daily clinical events under strict HIPAA compliance requirements.",
        stack=["AWS", "Python", "Event-Driven Architecture", "CI/CD", "Healthcare APIs"],
        industry="HealthTech",
        role="Quality & Technical Services Manager / Lead R&D Data Scientist",
        challenge="Healthcare platform required real-time data pipelines processing 50K+ daily clinical events (appointments, prescriptions, patient records) with <5 minute latency under strict HIPAA compliance. Legacy batch systems had 6-8 hour delays preventing real-time clinical decision support. Deployment reliability was 91-93% with 12-18 hour release cycles creating operational risk.",
        solution="Built event-driven data pipelines on AWS processing continuous clinical data streams with <5 minute end-to-end latency. Implemented HIPAA-compliant architecture with encryption at rest/transit, audit logging, and access controls. Standardized CI/CD enabling 2-3 production releases weekly with automated testing gates. Created monitoring dashboards tracking 25+ clinical and technical KPIs with automated alerting.",
        outcome="Achieved 99.8% pipeline reliability supporting production healthcare workflows. Reduced data latency from 6-8 hours to <5 minutes (98%+ improvement). Enabled real-time clinical decision support for 5,000+ daily patient interactions. Improved deployment reliability from 91-93% to 99%+ through standardized CI/CD. Reduced release cycles from 12-18 hours to 2-3 hours (83-86% improvement). Maintained 100% HIPAA compliance with zero security incidents over 11-month period."
    ),
    
    # ─── Analytics & Data Science Consulting (2018-2021) ─────────────────────────────────────
    WorkItem(
        slug="dentsu-marketing-analytics-platforms",
        title="Fortune 500 Marketing Analytics Platforms",
        subtitle="Cloud-Native Analytics & Modeling Workflows",
        summary="Designed analytics platforms supporting large-scale digital marketing datasets for 10+ Fortune 500 clients, reducing insight turnaround from 3-5 days to 4-6 hours through modernized cloud-native pipelines.",
        stack=["GCP", "BigQuery", "Python", "SQL", "Data Modeling", "ETL/ELT"],
        industry="Marketing Analytics / Consulting",
        role="Senior Consultant, Data Science",
        challenge="Fortune 500 clients required analytics platforms processing 500GB-2TB daily marketing data across 8-12 advertising channels (Google Ads, Facebook, LinkedIn, programmatic). Legacy on-prem systems had 3-5 day insight turnaround preventing real-time campaign optimization. Manual ETL processes consumed 30-40 hours weekly per client with 15-20% error rates.",
        solution="Designed cloud-native analytics platforms on GCP with BigQuery warehouses processing multi-channel marketing data. Implemented automated ELT pipelines ingesting from 8-12 ad platform APIs with incremental loading patterns. Built data modeling workflows supporting campaign attribution, audience segmentation, and performance forecasting. Created standardized reporting frameworks reducing custom report development from weeks to days.",
        outcome="Reduced insight turnaround from 3-5 days to 4-6 hours (85-90% improvement) across 10+ Fortune 500 clients. Automated 80-85% of manual ETL effort (30-40 hours weekly saved per client). Decreased data error rates from 15-20% to 2-3% through automated validation. Enabled high-volume campaign analytics spanning multiple channels, regions, and reporting cadences. Supported $50M+ monthly ad spend optimization across client portfolio."
    ),
    
    # ─── Compliance & Enterprise AI (2015-2018) ─────────────────────────────────────
    WorkItem(
        slug="ey-forensic-data-pipelines",
        title="Compliance-Grade Forensic Data Pipelines",
        subtitle="Regulatory & Audit Analytics Systems",
        summary="Built compliance-grade data pipelines processing 2-5TB sensitive forensic datasets for regulatory investigations, achieving 100% auditability with zero data integrity incidents across 15+ engagements.",
        stack=["Python", "SQL", "Data Governance", "ETL", "Audit Frameworks"],
        industry="Big-4 Consulting / Forensics",
        role="Consultant, Data Science",
        challenge="Forensic investigations required processing 2-5TB sensitive datasets (financial transactions, communications, operational logs) with 100% auditability and traceability for regulatory review. Manual data processing took 3-4 weeks per engagement with 10-15% data integrity issues. No standardized frameworks resulted in inconsistent quality and regulatory risk.",
        solution="Built compliance-grade data pipelines with end-to-end lineage tracking, automated validation rules, and comprehensive audit trails. Implemented data governance frameworks ensuring chain of custody, access controls, and immutable logging. Created standardized ETL templates for common forensic patterns (transaction analysis, communication networks, anomaly detection). Designed analytics systems optimized for regulatory review and courtroom presentation.",
        outcome="Achieved 100% auditability and traceability across 15+ forensic engagements. Reduced data processing time from 3-4 weeks to 5-7 days (75-82% improvement). Decreased data integrity issues from 10-15% to <1% through automated validation. Enabled enterprise-scale forensic analytics supporting regulatory investigations worth $500M-$1B+ in disputed amounts. Maintained zero data integrity incidents and zero regulatory findings across all engagements."
    ),
    WorkItem(
        slug="wipro-enterprise-ai-platforms",
        title="Enterprise AI Platform Optimization",
        subtitle="IT Operations Analytics & Cost Reduction",
        summary="Optimized enterprise AI platforms processing 10M+ daily operational events, achieving 99.7% improvement in execution performance (5 hours to 1 minute) and $120K+ annual infrastructure cost avoidance.",
        stack=["R", "Python", "Machine Learning", "Performance Optimization", "Enterprise IT"],
        industry="Enterprise IT / Global Services",
        role="Data Scientist",
        challenge="Enterprise AI platforms processed 10M+ daily operational events (logs, metrics, incidents) across global IT environments with 5-hour execution times making real-time analytics impractical. High infrastructure costs ($180K annually) due to inefficient processing. Manual analytics workflows consumed 50-60 hours weekly across operations teams.",
        solution="Re-engineered analytics workflows implementing vectorized operations, optimized data structures, and parallel processing patterns. Built automated ML pipelines for anomaly detection, capacity forecasting, and incident prediction. Optimized execution paths reducing compute requirements by 60-70%. Created self-service analytics dashboards eliminating 40-50 hours weekly manual reporting effort.",
        outcome="Achieved 99.7% execution performance improvement (5 hours to 1 minute, 300x faster). Delivered $120K+ annual infrastructure cost avoidance through optimized processing (67% reduction). Automated 80-85% of manual analytics workflows (40-50 hours weekly saved). Improved system responsiveness enabling real-time operational insights. Deployed across global IT environments supporting 50,000+ end users and 5,000+ infrastructure components."
    ),
    
    # ─── Early Career Analytics Projects (2012-2015) ─────────────────────────────────────
    WorkItem(
        slug="network-bandwidth-prediction",
        title="Network Bandwidth Prediction Dashboard",
        subtitle="Predictive Analytics & Cost Optimization",
        summary="Delivered predictive analytics dashboard forecasting bandwidth consumption across 100+ network devices, achieving 25-30% reduction in ISP subscription costs through data-driven capacity planning.",
        stack=["R", "Qlikview", "SQL Server"],
        industry="IT Operations",
        role="Solo Contributor",
        challenge="Organization over-provisioned bandwidth across 100+ network devices due to lack of consumption forecasting, resulting in 25-30% excess ISP costs annually. No capability to drill down to interface-level analysis or distinguish directional traffic patterns for optimization.",
        solution="Built predictive models using Simple Moving Average with Seasonality & Intersection Analysis in R, processing 12 months of historical data. Developed interactive Qlikview dashboard with 3-level drill-down (device → interface → traffic direction). Integrated SQL Server backend storing 500K+ consumption records with automated daily refresh.",
        outcome="Achieved 25-30% reduction in annual ISP subscription costs (estimated $40K-50K savings). Delivered device-level forecasts with 85-90% accuracy over 30-day horizon. Enabled interface-level bandwidth optimization across 300+ links. Received formal recognition from C-level management for cost impact."
    ),
    WorkItem(
        slug="it-events-prediction",
        title="IT Events Prediction Dashboard",
        subtitle="Proactive Capacity Management & Staffing",
        summary="Re-engineered IT event prediction system reducing execution time by 99.7% (5 hours to 1 minute) while enabling proactive capacity planning across 8 event categories and 15+ event types.",
        stack=["R", "Excel", "Qlikview"],
        industry="IT Operations",
        role="Team Contributor",
        challenge="Legacy prediction script required 5 hours to process 30K monthly IT events, making daily forecasts impractical. Reactive staffing approach resulted in 20-25% over-staffing during low-activity periods and 15-20% under-staffing during peaks across 50-person operations team.",
        solution="Completely rewrote business logic from scratch, implementing vectorized R operations and optimized data structures. Applied Simple Moving Average with Seasonality & Intersection Analysis across 8 event categories, 15 event types, and 200+ configuration items. Built multi-dimensional Qlikview dashboard with 7-day, 14-day, and 30-day forecast views.",
        outcome="Reduced execution time from 5 hours to 1 minute (300x improvement, 99.7% reduction). Enabled daily forecast updates vs. weekly previously. Improved staffing efficiency by 15-20% through predictive scheduling. Prevented estimated 30-40 critical events monthly through proactive capacity allocation. Deployed across 3 regional operations centers serving 5,000+ end users."
    ),
    WorkItem(
        slug="automation-candidate-dashboard",
        title="Automation Candidate Dashboard",
        subtitle="NLP-Based IT Incident Classification",
        summary="Built NLP-powered incident classification system reducing customer onboarding from 4-6 weeks to 3-5 days (90% reduction) and accelerating automation project pipeline by 300%.",
        stack=["R", "Python", "Excel", "Shiny"],
        industry="IT Service Management",
        role="Solo Contributor",
        challenge="Manual analysis of 5K-10K incident records per customer required 4-6 weeks by Project Managers to identify automation candidates, limiting new customer acquisition to 2-3 annually. No standardized methodology resulted in inconsistent automation recommendations and missed opportunities.",
        solution="Developed NLP classification engine using TF-IDF, Part-of-Speech tagging, and Topic Modeling (LDA) in Python and R. Trained on 50K+ historical incidents across 12 automation categories. Built interactive Shiny dashboard with automated categorization, confidence scoring, and ROI estimation. Deployed ML model achieving 82-85% classification accuracy validated against expert reviews.",
        outcome="Reduced customer onboarding from 4-6 weeks to 3-5 days (90% reduction, 8-10x faster). Increased new customer acquisition from 2-3 to 8-10 annually (300% growth). Processed 150K+ incidents across 12 customers in first year. Identified automation opportunities worth estimated $200K-250K in annual labor savings. Received executive sponsorship for company-wide deployment."
    ),
    
    # ─── Education & Community Leadership ─────────────────────────────────────
    WorkItem(
        slug="correlation-one-lead-instructor",
        title="Lead Instructor - Enterprise Data Science Training",
        subtitle="Walmart Data Science Bootcamp & DS4A Programs",
        summary="Served as Lead Instructor for Walmart's Data Science Bootcamp and Data Science for All (DS4A) programs, training 200+ professionals in advanced data science, ML, and deep learning methodologies.",
        stack=["Python", "Machine Learning", "Deep Learning", "Data Science", "Curriculum Design"],
        industry="Education / Professional Training",
        role="Lead Instructor",
        challenge="Correlation One needed experienced practitioners to deliver intensive data science bootcamps upskilling 80-120 professionals per cohort in advanced analytics, ML, and deep learning. Required translating complex technical concepts into practical, industry-relevant curriculum for diverse backgrounds (business analysts, engineers, product managers) with 6-8 week compressed timelines.",
        solution="Designed and delivered comprehensive curriculum covering statistical analysis, machine learning algorithms, deep learning architectures, and production ML systems. Led Walmart Data Science Bootcamp (Fall 2022) training 80+ professionals in enterprise data science practices. Instructed DS4A Bootcamp (Winter 2023) cohorts in data science and data engineering fundamentals. Created hands-on projects simulating real-world business problems with measurable outcomes.",
        outcome="Successfully trained 200+ professionals across multiple cohorts (2021-2023). Achieved 90%+ student satisfaction scores and 85%+ completion rates. Enabled career transitions for 40-50 participants into data science roles. Delivered specialized training in Deep Learning, Machine Learning, and advanced analytical techniques. Equipped professionals for data-centric roles in enterprise environments through industry-relevant curriculum."
    ),
    WorkItem(
        slug="cambrian-college-professor",
        title="Adjunct Professor - Graduate Business Analytics",
        subtitle="Advanced Analytics & Real-Time API Development",
        summary="Delivered graduate-level courses in statistical analysis, data visualization, dashboard creation, and real-time API development using Python, enhancing industry readiness for 150+ graduate students.",
        stack=["Python", "Statistical Analysis", "Data Visualization", "APIs", "Dashboard Development"],
        industry="Higher Education",
        role="Adjunct / Partial Load Professor",
        challenge="Graduate business analytics program required industry-experienced instructors to deliver practical, hands-on courses in advanced statistical analysis, data visualization, and modern API development. Students needed real-world skills bridging academic theory with contemporary business analytics practices for immediate industry application.",
        solution="Designed and delivered graduate courses covering advanced statistical methods, data visualization best practices, interactive dashboard development, and real-time API creation using Python. Created industry-aligned curriculum with hands-on projects using real datasets and business scenarios. Integrated modern tools and frameworks (Pandas, Matplotlib, Plotly, FastAPI, Flask) preparing students for immediate workplace contribution.",
        outcome="Enhanced proficiency and industry relevance for 150+ graduate students (2020-2023). Achieved 88-92% student satisfaction ratings across multiple semesters. Prepared students for immediate industry contribution through practical, hands-on curriculum. Integrated contemporary business analytics methodologies and tools reflecting current industry practices. Contributed to program's reputation attracting 20-25% increase in enrollment over 3-year period."
    ),
    WorkItem(
        slug="google-developer-groups-lead",
        title="Google Developer Groups - Chapter Lead",
        subtitle="Community Building & Technical Mentorship",
        summary="Organized 25+ community events, workshops, and DevFests focused on cloud, AI/ML, and modern software engineering, mentoring 300+ local developers on cloud-native architecture and scalable systems.",
        stack=["GCP", "Cloud Architecture", "AI/ML", "DevOps", "Community Leadership"],
        industry="Developer Community / Volunteer",
        role="Volunteer Chapter Lead",
        challenge="Regional tech community lacked accessible learning opportunities in cloud-native architecture, AI/ML, and modern software engineering practices. Local developers needed mentorship on Google Cloud Platform, DevOps, and scalable systems to advance careers and contribute to regional tech talent development.",
        solution="Organized and led 25+ community-driven events, workshops, and annual DevFests (2020-Present) focused on GCP, AI/ML, and modern software engineering. Created hands-on workshops covering cloud-native architecture, Kubernetes, serverless computing, and ML deployment. Mentored local developers through 1:1 sessions and group learning on scalable systems design. Collaborated with Google and global GDG chapters aligning community engagement with emerging technology trends.",
        outcome="Organized 25+ events reaching 300+ local developers over 5-year period. Mentored developers on cloud-native architecture, DevOps, and scalable systems contributing to regional tech talent development. Grew chapter membership by 150% (from 80 to 200+ active members). Enabled 15-20 community members to achieve Google Cloud certifications. Established partnerships with 5 local tech companies for internship and employment opportunities."
    ),
    WorkItem(
        slug="vriksh-consulting-founder",
        title="Vriksh Consulting Services - Founder & Director",
        subtitle="Enterprise DevOps, Data Engineering & AI Consulting",
        summary="Founded consulting firm delivering end-to-end DevOps, Data Engineering, and AI solutions for 12+ clients, generating $250K+ revenue while providing cloud-certified training programs upskilling 50+ professionals.",
        stack=["DevOps", "Data Engineering", "AI/ML", "Cloud Platforms", "Training & Consulting"],
        industry="Technology Consulting / Professional Services",
        role="Founder & Director",
        challenge="Enterprises needed specialized expertise in DevOps, Data Engineering, and AI for complex, niche technological challenges. Market gap existed for boutique consulting combining strategic insights, hands-on technical delivery, and professional training. Required building client base, delivering measurable outcomes, and establishing reputation in competitive consulting market.",
        solution="Established consulting practice (Oct 2021-Present) offering comprehensive DevOps, Data Engineering, Data Science, and AI solutions. Delivered bespoke data and AI products enabling clients to achieve strategic goals and operational efficiency. Designed and delivered cloud-certified training programs in DevOps, Data Engineering, and AI. Built client relationships through referrals, community engagement, and demonstrated expertise in complex technical challenges.",
        outcome="Served 12+ clients across healthcare, finance, retail, and technology sectors generating $250K+ revenue. Delivered 8 major projects including cloud migrations, data platform modernizations, and AI system implementations. Developed and delivered training programs upskilling 50+ professionals with 90%+ satisfaction ratings. Achieved 100% client retention rate with 8 clients engaging for multiple projects. Established reputation for delivering complex technical solutions with measurable business impact."
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
