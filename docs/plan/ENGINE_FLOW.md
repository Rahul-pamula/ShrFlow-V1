# ShrFlow — Technical Engine Flow & Architecture

> **Purpose:** This document is the primary technical onboarding guide for developers. It explains the "Why" and "How" of the system, organized by the actual lifecycle of an email campaign rather than project phases.

---

## 1. The Foundation: Multi-Tenant Isolation
**Why:** In a multi-tenant SaaS, the biggest risk is "Data Leakage" (Tenant A seeing Tenant B's data).
**How:**
*   **The "Restaurant Kitchen" Model:** Every tenant has their own "station" (Data Isolation).
*   **Row Level Security (RLS):** We don't rely on developers remembering `WHERE tenant_id = ...`. Instead, the database itself enforces isolation at the session level using `SET LOCAL app.current_tenant_id`. (Deep-dive: **Phase 1.7**)
*   **Dual Email Engine:**
    *   **System Pipeline (Gmail SMTP):** Used as a **temporary development baseline** for critical OTPs and Invites. (Recommendation: Migrate to a dedicated AWS SES production identity for high-volume platform alerts).
    *   **Campaign Pipeline (AWS SES):** Isolated reputation per tenant. If one tenant spams, only *their* domain is blacklisted, never our platform.

---

## 2. Audience Ingestion: Handling Scale
**Why:** Uploading 100k+ contacts via a standard API will cause timeouts and Out-of-Memory (OOM) crashes.
**How:**
*   **S3-First Streaming:** The UI gets a pre-signed URL to upload directly to S3. The API never touches the heavy bytes.
*   **RabbitMQ Worker Cluster:** An async `import_worker` pulls the file from S3 and parses it in chunks.
*   **Deduplication:** We use PostgreSQL `ON CONFLICT` logic to merge data instead of creating duplicates. (Deep-dive: **Phase 2**)

---

## 3. Creative Suite: The Template Engine & AI
**Why:** Email HTML is "broken" by default, and crafting high-converting content is a bottleneck for users.
**How:**
*   **DesignJSON Source of Truth:** We save a structured JSON object, not messy HTML.
*   **MJML Compilation:** The backend compiles JSON into MJML, then into highly compatible nested-table HTML.
*   **AI Copywriting Assistant:** Integrated LLM support for generating subject lines and body copy based on tenant-specific contexts.
*   **AI & Personalization (RAG):** Future-proofed with a vector-embedding pipeline (Phase 10.5) that allows the AI to "read" past successful campaigns to suggest better content. (Deep-dive: **Phase 10.5**)
*   **The Validation Gateway:** Before a campaign can even be saved, the "Safety Check" scans for missing unsubscribe links and Gmail's 102KB clipping limit.

---

## 4. Campaign Orchestration: The "Heart" of the Engine
**Why:** A campaign is a complex state machine that must be resumable if a server restarts.
**How:**
*   **Content Snapshotting:** The moment a campaign is "Sent," we freeze the template. This prevents a user from editing a template *while* the email is mid-flight.
*   **The Fan-out:** We don't push 100k emails to the queue at once. We stream the recipient list and push "Task IDs" into RabbitMQ.
*   **A/B Testing Architecture:** Support for multiple variants (Variant A/B) per campaign, each with its own `snapshot_id`, allowing for split-testing subject lines and content. (Deep-dive: **Phase 17**)
*   **State Machine:**
    *   `DRAFT` → `SCHEDULED` → `SENDING` → `COMPLETED`
    *   Includes `PAUSED` and `CANCELLED` for real-time control.

---

## 5. Governance & Enterprise Controls (Platform RBAC)
**Why:** Large companies need complex permissions (Admin can see everything, Creator can only draft).
**How:**
*   **Dual-Layer RBAC:**
    *   **Platform Level:** Super-admins managing all tenants, billing, and infrastructure.
    *   **Tenant Level:** Granular workspace permissions (`can('edit_campaign')`) enforced at the API level.
*   **Franchise Governance:** A "Parent-Child" tenant model. A Parent can push templates and "Master Audiences" down to child branches. (Deep-dive: **Phase 15**)
*   **Audit Logging:** Every destructive action (Delete, Send, Change Role) is recorded in an immutable log for security audits.

---

## 6. The Sending Pipeline: Deliverability & Protection
**Why:** Sending too fast gets you blocked; sending too slow makes the user unhappy.
**How:**
*   **Persistent SMTP Sessions:** We reuse connections to AWS SES to avoid the "Handshake Penalty" (1s per email down to 50ms).
*   **Backpressure:** RabbitMQ prefetch limits ensure workers don't get overwhelmed.
*   **The Kill Switch:** Every worker checks Redis before sending. If you click "Pause" in the dashboard, the workers stop in milliseconds.

---

## 7. Analytics & Insights: Truthful Observability
**Why:** Bots (Apple MPP, Security Scanners) "open" every email, making stats look fake.
**How:**
*   **Engagement Intelligence:** We use User-Agent heuristics to flag "Bot Opens" and hide them from the vanity metrics.
*   **HMAC Signing:** All tracking pixels and click-links are cryptographically signed to prevent "Link Probing" from inflating stats.

---

## 8. Monetization: Billing & Enforcement
**Why:** We must stop users from sending more than they paid for.
**How:**
*   **Plan Enforcement:** A middleware that checks usage counters before allowing a campaign to start.
*   **Stripe Integration:** Unified billing and subscription management tied directly to the tenant's limits.

---

## 9. Developer Intelligence: The MCP Framework
**Why:** Modern development teams need AI assistance that actually understands the live system state.
**How:**
*   **Model Context Protocol (MCP):** A standardized server (`scripts/mcp/`) that allows AI agents to safely "talk" to the database, inspect logs, and audit the schema. (Deep-dive: **Phase 1.9**)
*   **Why we want this:** It reduces developer onboarding time from weeks to days by allowing an AI to answer complex architectural questions about the live code.

---

## 10. System Evolution: Scale & Microservices
**Why:** A monolithic API becomes a bottleneck at 10M+ emails.
**How:**
*   **Service Decomposition:** The platform is designed to be "split" into microservices (see `platform/services/`).
*   **Template Service:** A dedicated Node.js service for heavy MJML compilation.
*   **Worker Isolation:** Each worker (Sender, Importer, Scheduler) runs in its own container, allowing for independent scaling based on CPU/Memory load.
