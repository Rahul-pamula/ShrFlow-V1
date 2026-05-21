# ShrFlow

<div class="hero">
  <img src="assets/shrflow-logo.svg" class="hero-logo no-shadow" alt="ShrFlow Logo">
  <h1>ShrFlow</h1>
  <p class="hero-sub">Enterprise Email Engine</p>
  <p class="hero-desc">Self-hosted, multi-tenant, high-performance email marketing infrastructure built for engineering teams who need full control.</p>
  <div class="hero-btns">
    <a class="btn btn-primary" href="#/introduction">Get Started →</a>
    <a class="btn btn-outline" href="#/getting-started/quick-start">Quick Start</a>
    <a class="btn btn-outline" href="https://github.com/Rahul-pamula/ShrFlow-Handover" target="_blank">GitHub ↗</a>
  </div>
  <div class="hero-pills">
    <span class="pill">⚡ FastAPI</span>
    <span class="pill">⚛️ Next.js 14</span>
    <span class="pill">🐇 RabbitMQ</span>
    <span class="pill">🐘 PostgreSQL</span>
    <span class="pill">🐳 Docker</span>
    <span class="pill">🛡️ Multi-tenant RLS</span>
  </div>
</div>

## Quick Navigation

<div class="card-grid">
  <a class="card" href="#/introduction">
    <div class="card-icon">📖</div>
    <div class="card-title">Introduction</div>
    <div class="card-desc">Architecture overview, core concepts, and system design.</div>
    <div class="card-arrow">Read more →</div>
  </a>
  <a class="card" href="#/screen-shots/README">
    <div class="card-icon">🖼️</div>
    <div class="card-title">Visual Tour</div>
    <div class="card-desc">See every screen of the platform — 22 annotated screenshots.</div>
    <div class="card-arrow">View tour →</div>
  </a>
  <a class="card" href="#/getting-started/quick-start">
    <div class="card-icon">🚀</div>
    <div class="card-title">Quick Start</div>
    <div class="card-desc">Get ShrFlow running locally in under 10 minutes.</div>
    <div class="card-arrow">Get started →</div>
  </a>
  <a class="card" href="#/getting-started/first-campaign">
    <div class="card-icon">📧</div>
    <div class="card-title">First Campaign</div>
    <div class="card-desc">Send your first email campaign end-to-end.</div>
    <div class="card-arrow">Learn how →</div>
  </a>
  <a class="card" href="#/advanced/deliverability-engine">
    <div class="card-icon">⚙️</div>
    <div class="card-title">Delivery Engine</div>
    <div class="card-desc">Dual-path RabbitMQ dispatch architecture deep-dive.</div>
    <div class="card-arrow">Explore →</div>
  </a>
  <a class="card" href="#/api-reference/authentication">
    <div class="card-icon">📡</div>
    <div class="card-title">API Reference</div>
    <div class="card-desc">Full REST API for campaigns, contacts, and authentication.</div>
    <div class="card-arrow">View API →</div>
  </a>
</div>

---

## Platform Overview

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Next.js 14 (App Router) | Campaign dashboard + analytics |
| Backend | FastAPI (Python 3.11) | REST API + business logic |
| Queue | RabbitMQ | Async campaign dispatch |
| Database | PostgreSQL + Supabase | Multi-tenant data store |
| Auth | Supabase Auth | JWT + Row-Level Security |
| Containers | Docker Compose | Local + production deployment |

---

<div class="callout info">
  <span class="callout-icon">💡</span>
  <div>New to the codebase? Start with <a href="#/introduction">Introduction</a>, then the <a href="#/screen-shots/README">Visual Tour</a> to understand the full platform before diving into code.</div>
</div>
