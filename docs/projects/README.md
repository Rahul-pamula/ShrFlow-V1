# Technical Projects Showcase

Welcome to the technical projects showcase for **Pamula Rahul**. This page breaks down the core architecture of **ShrFlow-V1** (a self-hosted, multi-tenant email operations platform) into the **6 distinct technical projects** featured on the resume.

Each project highlights a specific engineering challenge—spanning database security, high-throughput distributed workers, real-time message brokers, server-side template compilation, cloud infrastructure, and AI-first developer tooling.

---

### Project Showcases

#### 🔑 [1. Multi-Tenant SaaS Core & Workspace Orchestration Hub](projects/1_multi_tenant_saas.md)
*   **Core Tech:** Next.js 14, FastAPI, Supabase Auth, PostgreSQL Row-Level Security (RLS)
*   **Highlight:** Bulletproof multi-tenant database isolation set at the transaction level via `SET LOCAL app.current_tenant_id` to block cross-tenant leakage.

#### 📊 [2. High-Volume CSV Ingestion Pipeline & Contacts Engine](projects/2_csv_ingestion.md)
*   **Core Tech:** Pandas, RabbitMQ, Redis, AWS S3, WebSockets
*   **Highlight:** Storage-first ingestion pipeline streaming gigabyte-scale user lists in 500-row chunks to prevent memory bloat and API connection timeouts.

#### 🎨 [3. No-Code Email Builder & MJML Compilation Microservice](projects/3_email_builder.md)
*   **Core Tech:** Next.js, Zustand, FastAPI, MJML compiler
*   **Highlight:** A state-driven template builder compiling strict hierarchical `DesignJSON` states into fully responsive, client-compatible HTML email payloads via MJML.

#### 🚀 [4. Asynchronous Campaign Dispatcher & Distributed Worker Cluster](projects/4_campaign_dispatcher.md)
*   **Core Tech:** RabbitMQ, Redis, Celery, asyncpg, PostgreSQL server-side cursors
*   **Highlight:** High-throughput campaign worker system resolving recipient lists dynamically and locking schedules with Redis distributed locks.

##### ✉️ [5. DKIM/SPF Domain Provisioning & SES Mail Infrastructure](projects/5_domain_provisioning.md)
*   **Core Tech:** AWS SES, Route53, Boto3, FastAPI
*   **Highlight:** Automated programmatic verification of sender domains, dynamically query-generating SPF/DKIM DNS records directly using AWS Boto3.

#### 🤖 [6. AI Developer Intelligence Server & Context-Aware RAG Engine](projects/6_mcp_developer_intelligence.md)
*   **Core Tech:** FastMCP SDK, Python, Claude Desktop, PostgreSQL
*   **Highlight:** Standardized Model Context Protocol (MCP) server design exposing DB schemas, tailing application logs, and worker queue depths to AI assistants for agentic debugging.
