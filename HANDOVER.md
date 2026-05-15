# ShrFlow Handover Guide

Welcome to the ShrFlow Email Engine Platform. This repository contains the core infrastructure, API, and worker services for high-scale email orchestration.

## Repository Structure

*   `platform/api`: FastAPI backend for managing campaigns, contacts, and domains.
*   `platform/worker`: Python Celery workers for processing email dispatch jobs.
*   `migrations/`: Full versioned history of the database schema.
*   `scripts/`: Automation tools for deployment and database management.
*   `docker-compose.yml`: Local development environment setup.

## Getting Started

### 1. Environment Configuration
Copy the example environment file and fill in your Supabase, Redis, and RabbitMQ credentials:
```bash
cp .env.example .env
```

### 2. Database Setup
Ensure your Supabase/PostgreSQL instance is running, then apply the migrations. We have provided a utility script to apply all migrations in sequence:

```bash
python3 scripts/apply_all_migrations.py
```

### 3. Row Level Security (RLS)
To enforce multi-tenant isolation, apply the RLS policies:
```bash
python3 scripts/apply_rls.py
```

### 4. Supabase Edge Functions
The tracking pixel logic is handled by a Supabase Edge Function. To deploy it:
```bash
# Ensure you are logged into Supabase CLI
supabase functions deploy track --project-ref your-project-ref
```

### 5. Seeding Initial Data
Once the database and RLS are configured, you can seed the initial marketing templates and development data:
```bash
# Seed initial MJML templates
python3 scripts/seed_templates.py

# Seed development test data (optional)
python3 scripts/seed_dev_data.py
```

### 5. Running Locally
Start the entire stack using Docker:
```bash
docker-compose up --build
```

This will launch:
*   **API** at `http://localhost:8000`
*   **Worker** for background processing
*   **RabbitMQ** & **Redis** for signaling/state

## Handover Alignment
Note: The migration `055_handover_alignment.sql` has been included to ensure the schema matches the target enterprise delivery requirements exactly.

## Contact & Support
For architectural questions, refer to the documentation in the `/docs` folder.
