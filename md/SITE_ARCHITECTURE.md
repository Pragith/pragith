# Pragith.net – Complete Site Architecture

**Last Updated:** 2026-02-11  
**Status:** Production-Ready Foundation

---

## Site Structure

```
/                   → Homepage (index.html)
/work               → Portfolio & Case Studies (work.html)
/work/<slug>        → Individual Case Study (work_detail.html)
/agents             → AI-Assisted Delivery (agents.html)
/build              → Methodology (build.html)
/stack              → Technology Stack (stack.html)
/contact            → Contact & Consulting (contact.html)
/blog               → Blog List (blog_list.html)
/blog/<slug>        → Blog Post (blog_detail.html)
/blog/tag/<tag>     → Tag-Filtered Posts (blog_list.html)
/faq                → FAQ (faq.html)
/legal              → Terms (legal.html)
/privacy            → Privacy Policy (privacy.html)
```

---

## 1. Global Layout (base.html)

### Meta
- **Title:** Pragith Prakash | Principal AI & Data Engineer
- **Description:** Principal AI & Data Engineer specializing in enterprise platforms, multi-cloud architecture, and AI-assisted delivery.

### Assets
- ✅ Optimized Tailwind CSS (`/static/css/style.min.css`)
- ✅ Google Fonts: DM Sans (display), Inter (body)
- ✅ Font preloading for performance
- ✅ Favicon reference
- ✅ Google Analytics (conditional via `ga_tag`)
- ✅ reCAPTCHA

### Navigation
**Header:**
- Work
- Agents
- Build
- Stack
- Blog
- Contact (CTA button)

**Footer (4 columns):**
1. **Site:** Home, Work, Blog
2. **Services:** Advisory, AI Teams, Build
3. **Legal:** Terms, Privacy, FAQ
4. **Connect:** LinkedIn, GitHub, Email

---

## 2. Homepage (index.html)

### Hero Section
```
Badge: "Available for Select Projects"
Headline: "Enterprise AI & Cloud Platform Architect"
Subheading: "Architecting high-performance platforms. 
             Scaling multi-terabyte analytics. 
             Shipping production AI systems."

CTAs:
  - View Work →
  - Start a Project
```

### Stats Section
| Metric | Label | Description |
|--------|-------|-------------|
| **13+** | Years | Enterprise Systems |
| **100TB+** | Scale | Production Data Systems |
| **AI** | Approach | AI-Assisted Delivery |

### Quick Navigation Tiles
1. **Work** – Case studies & portfolio projects
2. **Agents** – AI systems and automation
3. **Build** – Services & engagement models
4. **Stack** – Technologies & tools

### Core Capabilities (4 Cards)
1. **Cloud Architecture**
   - Google Cloud (BigQuery, GKE, Dataflow)
   - AWS (Lambda, Kinesis, DynamoDB)
   - Azure (Databricks, Synapse)

2. **Data Engineering**
   - Apache Spark, Kafka, Airflow
   - Real-time Streaming Systems
   - Petabyte-Scale Processing

3. **DevOps & Infrastructure**
   - Kubernetes, Terraform, Docker
   - CI/CD Pipeline Automation
   - Production Observability

4. **AI & Automation**
   - Google ADK & Model Context Protocol
   - AI Workflow Automation
   - Model Deployment & Operations

### Footer CTA
```
"Ready to Build?"
"I partner with founders, CTOs, and engineering leaders 
 to ship production-grade systems."
CTA: Start a Project →
```

---

## 3. Agents Page (agents.html)

### Philosophy
```
Badge: "How I Work"
Headline: "Human-Led, AI-Amplified"
Subtext: "I use structured AI workflows to accelerate delivery 
          across engineering, data, infrastructure, and product.
          Faster results, consistent quality."
```

### How It Works (3 Steps)
1. **You Define Goals** – Feature, pipeline, infrastructure, or full system
2. **AI Agents Execute** – Handles repetitive tasks, I focus on architecture
3. **You Get Results** – Production-ready code, infrastructure, documentation

### AI-Assisted Capabilities (4 Cards)

#### 01. Engineering Agent
**What it does:**
- Writes boilerplate code
- Generates tests
- Handles refactoring
- Maintains documentation

**Why it matters:**
- Fully-tested, well-documented code
- Zero technical debt from skipped docs
- Code migrations in hours, not weeks

#### 02. Data Agent
**What it does:**
- Monitors data quality
- Validates schemas
- Detects anomalies
- Profiles datasets automatically

**Why it matters:**
- Real-time quality monitoring
- Automated anomaly detection
- Schema evolution tracking

#### 03. Infrastructure Agent
**What it does:**
- Generates Infrastructure as Code
- Validates security policies
- Optimizes cloud costs

**Why it matters:**
- Security compliance built-in
- Cost optimization in real-time
- Terraform/CloudFormation generated & validated

#### 04. Product Agent
**What it does:**
- Parses requirements
- Maps user journeys
- Rapidly prototypes UI/UX

**Why it matters:**
- Functional prototypes ready for testing
- User journey maps from requirements
- Faster iteration on product-market fit

### Powered By
- Google ADK
- Gemini 2.0
- Claude Sonnet
- GPT-4
- OpenAI Codex
- Vertex AI
- Model Context Protocol
- ElevenLabs
- Veo

### CTA
```
"Interested in Working Together?"
"I help teams move faster with structured AI workflows 
 across engineering, data, and infrastructure."
CTAs:
  - Let's Discuss Your Project →
  - View Case Studies
```

---

## 4. Build Page (build.html)

### Headline
```
"PoC to Production"
"A disciplined framework for taking ideas from 
 'works on my machine' to 'scales globally' without the bloat."
```

### Methodology (3 Phases)

#### Phase 01: Rapid Prototyping
- Validate core value proposition immediately
- Functional, throw-away prototypes in days
- Test assumptions before committing to architecture

**Tools:** FastAPI, Streamlit, Docker Compose

#### Phase 02: Cloud-Native Architecture
- Design for durability and scale
- Select right managed services (AWS/GCP/Azure)
- Minimize operational overhead, maximize performance

**Tools:** Kubernetes, Serverless, Event-Driven

#### Phase 03: Production Hardening
- Observability, security, automation
- Comprehensive logging, monitoring, CI/CD pipelines

**Tools:** Terraform, GitHub Actions, Datadog/Prometheus

### CTA
```
"Ready to Build Your System?"
"Whether you're starting from scratch or modernizing legacy 
 infrastructure, I can help you ship production-grade systems 
 that scale."
CTAs:
  - Discuss Your Project →
  - View Case Studies
```

---

## 5. Stack Page (stack.html)

### Headline
```
"Technology Stack"
"Every technology choice is deliberate. These tools solve 
 real problems at scale and are selected based on project 
 requirements."
```

### Categories

#### Cloud Infrastructure
1. **Google Cloud Platform**
   - Best-in-class for data analytics and ML workflows
   - BigQuery, GKE, Dataflow, Pub/Sub

2. **Amazon Web Services**
   - Unmatched service breadth and maturity
   - Lambda, Kinesis, DynamoDB, ECS/EKS

3. **Microsoft Azure**
   - Enterprise integration strength
   - Databricks, Synapse, AKS

#### Data Engineering
- **Apache Spark** – Petabyte-scale transformations
- **Apache Airflow** – Code-first workflow orchestration
- **Kafka / Pub/Sub** – Real-time streaming backbone
- **dbt** – Analytics engineering standard

#### DevOps & Infrastructure
- **Docker & Kubernetes** – Container orchestration at scale
- **Terraform / OpenTofu** – Infrastructure as Code
- **GitHub Actions** – Native CI/CD integration
- **Prometheus & Grafana** – Production observability

#### AI & Automation
- **Google GenAI Agent Development Kit (ADK)** – Production AI agents
- **Model Context Protocol (MCP)** – Standardized tool interface
- **Vector Databases (Pinecone, Milvus)** – Semantic search at scale

#### Backend & API
- **Python (FastAPI, Flask)** – Rapid development velocity
- **Go** – High-performance services
- **GraphQL** – Client-driven data fetching
- **gRPC** – High-performance RPC

### CTA
```
"Need the Right Stack for Your Project?"
"I help teams make pragmatic technology choices that align 
 with business goals and scale requirements."
CTA: Discuss Your Architecture →
```

---

## 6. Contact & Consulting (contact.html)

### Headline
```
"Let's Work Together"
"Strategic advisory, technical consulting, and architecture 
 reviews for data and AI challenges."
```

### Services (Left Column)

#### Architecture Review
Deep dive into current cloud architecture. Identification of bottlenecks, security risks, and cost optimization opportunities.

#### AI Strategy & Roadmap
Pragmatic assessment of where AI can drive value. Roadmap development from PoC to production.

#### Data Platform Modernization
Migration strategies from legacy on-prem systems to modern cloud lakehouses.

#### CTO Advisory
Technical leadership support for startup founders and non-technical executives.

### Rate Card
```
Standard Rate: {{ currency_symbol }}{{ hourly_rate }}/hr
(If non-USD: ~${{ base_rate_usd }} USD)

"Engagements typically start with a 1-hour discovery call 
 to assess fit and scope."
```

### Engagement Types
- One-time architecture reviews
- Ongoing fractional CTO advisory
- Workshop facilitation & training
- Technical due diligence

### Contact Form (Right Column)
**Fields:**
- Name *
- Email *
- Company
- Message *
- reCAPTCHA

**Submission:** POST `/contact`  
**Success:** Redirects to `contact_success.html`

---

## 7. Work Page (work.html)

### Headline
```
"Selected Work"
"Case studies in building scalable data platforms, 
 real-time systems, and AI infrastructure."
```

### Work Item Structure
```
Industry • Subtitle
Title (linked to /work/<slug>)
Summary
Stack Tags: [Tech1, Tech2, Tech3...]
→ Arrow button to detail page
```

### CTA
```
"Like What You See?"
"I'm available for select consulting engagements and 
 strategic advisory roles."
CTA: Explore Consulting →
```

---

## 8. Blog System

### Blog List (blog_list.html)
```
Title: "Engineering Log"
Filter: /blog/tag/<tag>

Post Preview:
  - Date
  - Title
  - Summary
  - Tags (clickable)
  - Read More →
```

### Blog Detail (blog_detail.html)
```
Date
Title
Summary
Tags (pills)
Markdown-rendered content
```

### Blog Features
- ✅ Markdown-based
- ✅ Tag filtering
- ✅ Tag normalization
- ✅ Clean detail pages
- ⬜ Reading time indicator (TODO)
- ⬜ Featured post support (TODO)
- ⬜ OpenGraph metadata (TODO)
- ⬜ Structured data (TODO)

---

## 9. FAQ Page (faq.html)

### Questions Covered

**Do you sign NDAs?**  
Yes. I routinely work with sensitive IP and regulated data. Happy to sign standard mutual NDA.

**Do you work on-site?**  
Primarily remote. Can travel for critical workshops, kick-offs, or deployments in UAE or North America.

**What is your billing model?**  
Hourly for advisory. Fixed-price for defined projects with milestone-based payments.

**Who owns the IP?**  
You do. Upon full payment, all code, documentation, and artifacts become your exclusive property.

**Are you available for full-time roles?**  
Focused on independent consulting. Open to fractional CTO or Principal Architect roles.

---

## 10. Error Pages

### 404 (404.html)
```
"404"
"Page not found."
CTA: Return Home →
```

### 500 (500.html)
```
"500"
"Internal Server Error. Something went wrong."
CTA: Return Home →
```

---

## Technical Architecture

### Performance
- ✅ Optimized Tailwind CSS (~50KB minified)
- ✅ Font preloading
- ✅ No CDN bloat
- ✅ Production-ready build pipeline

### SEO
- ✅ Clean URL structure
- ✅ Semantic HTML
- ✅ Meta descriptions
- ⬜ OpenGraph tags (TODO)
- ⬜ Twitter cards (TODO)
- ⬜ Structured data (TODO)

### Security
- ✅ reCAPTCHA integration
- ✅ Rate limiting on contact form
- ⬜ CSP headers (TODO)
- ⬜ Honeypot field (TODO)

### Analytics
- ✅ Google Analytics (conditional)
- ✅ CTA tracking via `data-analytics` attributes

---

## Content Strategy

### Current Positioning
**Primary:** Enterprise AI & Cloud Platform Architect  
**Differentiator:** AI-Assisted Delivery  
**Target Market:** Enterprise clients, CTOs, technical founders

### Authority Signals
**Current:**
- 13+ years experience
- 100TB+ scale systems
- Multi-cloud expertise
- AI-assisted workflows

**Missing (High Priority):**
- ⬜ Detailed case study with metrics
- ⬜ Architecture deep dive post
- ⬜ Client logos/testimonials
- ⬜ Quantified business impact

---

## Deployment Checklist

### Pre-Deploy
- ✅ Tailwind CSS rebuilt
- ✅ All jargon removed
- ✅ Positioning strengthened
- ⬜ Favicon file added
- ⬜ reCAPTCHA key replaced
- ⬜ Rate updated ($150-175/hr recommended)

### Post-Deploy
- ⬜ Test all pages render correctly
- ⬜ Verify form submissions
- ⬜ Check analytics tracking
- ⬜ Validate responsive design
- ⬜ Test contact form rate limiting

---

## Next Phase Priorities

### Week 1
1. Add favicon file
2. Replace reCAPTCHA placeholder
3. Consider rate increase
4. Add OpenGraph/Twitter cards

### Month 1
5. Write one detailed case study
6. Add structured data (Schema.org)
7. Implement blog enhancements
8. Add expected response time to contact form

### Quarter 1
9. Collect client testimonials
10. Create architecture deep dive content
11. Add client logos (with permission)
12. Develop authority content series

---

**Status:** Foundation is production-ready. Next phase is authority building through content and social proof.
