# 6. AI Developer Intelligence Server & Context-Aware RAG Engine

This project maps the strategic design and architectural blueprint for integrating a Model Context Protocol (MCP) server and RAG engine directly into the platform core to automate developer auditing, testing, and debugging.

---

### Architecture Flow

```mermaid
graph TD
    classDef mcp fill:#8b5cf6,stroke:#6d28d9,stroke-width:2px,color:#fff,font-weight:bold,rx:10px,ry:10px;
    classDef logic fill:#10b981,stroke:#047857,stroke-width:2px,color:#fff,font-weight:bold,rx:5px,ry:5px;
    classDef client fill:#3b82f6,stroke:#1d4ed8,stroke-width:2px,color:#fff,font-weight:bold,rx:10px,ry:10px;
    classDef storage fill:#475569,stroke:#334155,stroke-width:2px,color:#fff,rx:5px,ry:5px;

    AIClient([AI Client / Agent]) --> |"Talks via stdio/SSE"| MCPServer[ShrFlow MCP Server]
    class AIClient client;
    class MCPServer mcp;

    subgraph MCPLayer["MCP Interface Layer"]
        Tools[MCP Tools: DB, Logs, Workers]
        Resources[MCP Resources: Docs, Plans]
        MCPServer --> Tools
        MCPServer --> Resources
        class Tools mcp;
        class Resources mcp;
    end

    subgraph AppInternal["App Internal Logic"]
        DBLogic[Database / RLS Manager]
        LogLogic[Log Tailing Service]
        QueueLogic[RabbitMQ / Redis Monitor]
        
        Tools --> DBLogic
        Tools --> LogLogic
        Tools --> QueueLogic
        class DBLogic logic;
        class LogLogic logic;
        class QueueLogic logic;
    end

    subgraph Persistence["Data & State"]
        PG[(PostgreSQL / Supabase)]
        Redis[(Redis State)]
        Docs[(Project Roadmap)]
        
        DBLogic --> PG
        LogLogic --> Docs
        QueueLogic --> Redis
        class PG storage;
        class Redis storage;
        class Docs storage;
    end
```

---

### Technical Highlights

1. **Standardized Model Context Protocol (MCP) Bridge:**
   Exposes internal app boundaries (database connections, Celery statuses, and log files) over a standard stdio/SSE bridge. This permits AI clients (like Claude Desktop or autonomous agents) to safely read and debug live infrastructure.
2. **Context-Aware RAG Engine:**
   Implements resource loaders exposing project plans (`phase_wise_plan.md`) and database schemas as live vector-search indices, helping the AI understand design constraints when suggesting edits.
3. **Infrastructure Telemetry Tools:**
   Exposes diagnostic tools:
   *   `db_inspector`: List tables, details columns, and validates PostgreSQL RLS security properties.
   *   `worker_monitor`: Queries RabbitMQ queue depths and lists active Redis distributed campaign locks.
   *   `audit_viewer`: Queries immutable `audit_logs` entries to track operational faults chronologically.

---

### Core Code File Paths

*   **Phase 1.9 MCP Strategic Specification:**
    [`docs/plan/phase_wise_plan.md`](https://github.com/Rahul-pamula/ShrFlow-V1/blob/main/docs/plan/phase_wise_plan.md#L628-L705) — Outlines the architecture plan, tool listings, and validation routines.
*   **System Developer Intelligence Overview:**
    [`docs/plan/overview.md`](https://github.com/Rahul-pamula/ShrFlow-V1/blob/main/docs/plan/overview.md#L393-L436) — Breaks down Phase 1.9's integration architecture flow and gaps.
