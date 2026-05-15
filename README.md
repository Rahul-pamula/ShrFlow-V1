# 📧 ShrFlow — Enterprise Email Engine

> A high-performance, self-hosted, multi-tenant email marketing platform.  
> Built strictly on modern containerized architecture: **FastAPI · Next.js · RabbitMQ · AWS SES · Supabase · Docker**.

---

## 🌟 What This Project Does

ShrFlow is a **full-scale, self-hosted email marketing platform** — designed as a high-performance, open-source alternative to platforms like Mailchimp or SendGrid. 

**Core Capabilities:**
*   **Multi-tenant Architecture:** Secure workspace isolation spanning Teams and Agencies.
*   **High-Velocity Contacts Engine:** Gigabyte-scale CSV ingestion, segmentation, and deduplication handled asynchronously by RabbitMQ data workers.
*   **Visual Template Builder:** Drag-and-drop block editor compiling into responsive MJML, featuring an AI Copywriting Assistant.
*   **Campaign Orchestration:** Fine-grained dispatch throttling, scheduling, spintax merge-tags, and instant pause/cancel controls.
*   **Dual Delivery Pipeline:** Critical system emails route securely through trusted Gmail SMTP, while massive bulk marketing campaigns isolate their reputation through AWS SES.
*   **Deep Observability:** Granular audit logging, Supabase Edge Function open-tracking pixels, and real-time AWS SNS webhook bounce/complaint handling.

---

## 📸 Visual Tour

### 🖥️ Dashboard & Audience Management
![Contacts Dashboard](docs/plan/screen_shots/Screenshot%202026-05-07%20at%209.10.03%E2%80%AFAM.png)
*Real-time audience monitoring, segmentation, and health tracking.*

---

### 🎨 Design & Infrastructure
<table border="0">
  <tr>
    <td width="50%">
      <p align="center"><b>Visual Template Library</b></p>
      <img src="docs/plan/screen_shots/Screenshot%202026-05-07%20at%209.20.10%E2%80%AFAM.png" width="100%" />
    </td>
    <td width="50%">
      <p align="center"><b>Infrastructure & Senders</b></p>
      <img src="docs/plan/screen_shots/Screenshot%202026-05-07%20at%2010.09.18%E2%80%AFAM.png" width="100%" />
    </td>
  </tr>
  <tr>
    <td width="50%">
      <p align="center"><b>Enterprise Auth Shell</b></p>
      <img src="docs/plan/screen_shots/Screenshot%202026-05-07%20at%209.03.21%E2%80%AFAM.png" width="100%" />
    </td>
    <td width="50%">
      <p align="center"><b>Import Workflows</b></p>
      <img src="docs/plan/screen_shots/Screenshot%202026-05-07%20at%209.09.49%E2%80%AFAM.png" width="100%" />
    </td>
  </tr>
</table>

<details>
<summary><b>🔍 View More System Previews (Settings, Modals, Preferences)</b></summary>
<br>

| Feature | Preview |
| :--- | :--- |
| **User Preferences** | ![Preferences](docs/plan/screen_shots/Screenshot%202026-05-07%20at%2010.11.04%E2%80%AFAM.png) |
| **Batch History** | ![Import History](docs/plan/screen_shots/Screenshot%202026-05-07%20at%209.09.49%E2%80%AFAM.png) |

---
### 📖 [Explore the Full 40+ Screenshot Gallery →](docs/VISUAL_GALLERY.md)
</details>

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Next.js 14 (App Router), TypeScript, Tailwind CSS, shadcn/ui |
| **Backend API** | Python FastAPI + Uvicorn |
| **Async Workers** | Python async (aio-pika, aiosmtplib) + RabbitMQ |
| **Database** | Supabase (PostgreSQL + Edge Functions) |
| **State & Cache** | Redis (Upstash) |
| **Delivery** | Amazon SES (Campaigns) & Gmail SMTP (System Mail) |

---

## 🏗 Architecture & Design Documents

ShrFlow uses a complex asynchronous dual-pipeline architecture. Instead of cluttering the README, all technical deep-dives, RAG design patterns, and network graphs are strictly maintained in our dedicated documentation directory:

*   📘 **[Complete Architectural Overview (with diagrams)](docs/phases/shrflow_architecture.md)**
*   📋 **[Phase-by-Phase Roadmap & Execution Plan](docs/phases/phase_wise_plan.md)**

---

## 🚀 Guided Setup

We have completely deprecated manual OS installations and multi-terminal setups. **The entire platform is strictly containerized.** 

### Step 1 — System Prerequisites
You only need exactly two things installed on your computer to run this entire platform:
1.  **Git** (To clone the repository)
2.  **Docker Desktop** (To run the orchestrator)

### Step 2 — Clone the Repository
```bash
git clone <your-repo-url>
cd ShrFlow_
```

### Step 3 — Environment Variables & Database
1. Duplicate the `.env.example` file and rename it to `.env`.
2. Follow the detailed instructions in **[HANDOVER.md](HANDOVER.md)** to configure your database and run the migration scripts.

*Please refer to **.env.example** in the root directory for the full list of configuration variables.*

### Step 4 — Run the Docker Cluster
Because everything is containerized, you just spin up your Docker Desktop application and run one command to orchestrate the Frontend, FastAPI backend, and all 4 Python background workers effortlessly.

🚨 **Detailed Docker Guide:** Please read our dedicated file: **[docs/docker_notes.md](docs/docker_notes.md)** for exact operational instructions, live log streaming, and troubleshooting commands!

```bash
docker-compose up -d
```
*That's it. Never run local terminals again!*

---

## 🤝 Open Source Contributions

**ShrFlow is fully open source, and we actively welcome contributions!** 

Whether you're fixing a bug, hardening security, or building out a massive new feature (like our upcoming Stripe integration or advanced analytics), we want your Pull Requests.

### How to Contribute:
1. **Fork** the repository and clone your fork locally.
2. **Create a branch** for your feature: `git checkout -b feature/amazing-new-feature`
3. **Commit** your isolated changes: `git commit -m 'feat: added amazing new feature'`
4. **Push** your branch: `git push origin feature/amazing-new-feature`
5. **Open a Pull Request** against our `main` branch. 

Please ensure your code follows the existing PEP8 (Python) and ESLint (Next.js) standards. All PRs will be rigorously reviewed before merging into the main orchestrations. Let's build the best self-hosted email engine together!
