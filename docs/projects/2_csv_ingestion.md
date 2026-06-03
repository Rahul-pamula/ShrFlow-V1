# 2. High-Volume CSV Ingestion Pipeline & Contacts Engine

This project implements a storage-first, async chunked ingestion pipeline capable of parsing gigabyte-scale contact databases without memory exhaustion or API timeouts.

---

### Architecture Flow

```mermaid
graph TD
    classDef frontend fill:#2563eb,stroke:#1d4ed8,stroke-width:2px,color:#fff,font-weight:bold,rx:5px,ry:5px;
    classDef api fill:#10b981,stroke:#047857,stroke-width:2px,color:#fff,font-weight:bold,rx:5px,ry:5px;
    classDef worker fill:#8b5cf6,stroke:#6d28d9,stroke-width:2px,color:#fff,font-weight:bold,rx:5px,ry:5px;
    classDef database fill:#475569,stroke:#334155,stroke-width:2px,color:#fff,font-weight:bold,rx:5px,ry:5px;
    classDef storage fill:#f59e0b,stroke:#b45309,stroke-width:2px,color:#fff,font-weight:bold,rx:5px,ry:5px;

    subgraph ContactsInterface["Frontend Contacts UI"]
        List[Contacts List & Search Grid]
        ImportModal[CSV / XLSX Import <br> Wizard & Mapper]
        WS[WebSocket Progress Listener]
        
        List --> ImportModal
        ImportModal --> WS
        class List frontend;
        class ImportModal frontend;
        class WS frontend;
    end

    subgraph ContactsAPI["Contacts API Gateway"]
        InitAPI[POST /import/initialize <br> Presigned URL Gen]
        ProcessAPI[POST /import/process <br> Queue Trigger]
        WSGW[WebSocket Gateway <br> Redis Sub]
        
        ImportModal --> InitAPI
        ImportModal --> |"Direct Upload"| S3[(Object Storage: S3/MinIO/Supabase)]
        ImportModal --> ProcessAPI
        WSGW --> WS
        class InitAPI api;
        class ProcessAPI api;
        class WSGW api;
        class S3 storage;
    end

    subgraph ImportWorker["RabbitMQ Data Worker"]
        Chunker[Async Stream Parser <br> Chunksize=500]
        Validator[Audit & Validation Service]
        DLQ[RabbitMQ Dead-Letter Queue]
        
        ProcessAPI --> |"Job ID"| Chunker
        Chunker --> |"Stream bytes"| S3
        Chunker --> Validator
        Validator -.-> |"Fails 3x"| DLQ
        class Chunker worker;
        class Validator worker;
        class DLQ worker;
    end

    subgraph DataLayer["Contact Storage & Audit"]
        Contacts[(Contacts Table <br> Upsert Logic)]
        Rejections[(Import Rejected Rows <br> Failure Log)]
        Redis[(Redis Pub/Sub <br> Progress Events)]
        
        Validator --> Contacts
        Validator --> Rejections
        Validator --> Redis
        Redis --> WSGW
        class Contacts database;
        class Rejections database;
        class Redis database;
        class DBLogic logic;
    end

    classDef dualBox fill:#f8fafc,stroke:#cbd5e1,stroke-width:2px,stroke-dasharray: 4 4;
    class ContactsInterface dualBox;
    class ContactsAPI dualBox;
    class ImportWorker dualBox;
    class DataLayer dualBox;
```

---

### Technical Highlights

1. **Storage-First Presigned Ingestion:**
   Rather than uploading files directly to FastAPI and risking gateway timeouts (e.g., Nginx body limits), the client requests a presigned URL (`POST /import/initialize`) and uploads raw CSVs directly to AWS S3/Object Storage.
2. **Chunked Streaming & O(1) Memory Space:**
   When enqueued via RabbitMQ, the Python worker opens a stream to the S3 object and parses the file in **batches of 500 rows** using a streaming parser. This guarantees that memory utilization stays constant (O(1)) regardless of file size (e.g. 10MB vs 2GB).
3. **Real-time Live Progress Hooks:**
   As the worker finishes each chunk, it updates job statistics and triggers a message via **Redis Pub/Sub**. The API's WebSocket connection captures these events and feeds real-time progress bars to the user interface.
4. **Deduplication and Validation:**
   Applies deduplication at database insertion boundaries using Postgres upserts on combinations of `(tenant_id, email)` while logging invalid email syntaxes to a secondary `import_rejected_rows` audit log.

---

### Core Code File Paths

*   **Ingestion Endpoint APIs:**
    [`platform/api/routes/contacts.py`](https://github.com/Rahul-pamula/ShrFlow-V1/blob/main/platform/api/routes/contacts.py) — Houses initialization and processing triggers.
*   **Import Process Orchestrator:**
    [`platform/api/services/import_service.py`](https://github.com/Rahul-pamula/ShrFlow-V1/blob/main/platform/api/services/import_service.py) — Orchestrates files, templates, and batch creations.
*   **Distributed RabbitMQ Worker:**
    [`platform/worker/import_worker.py`](https://github.com/Rahul-pamula/ShrFlow-V1/blob/main/platform/worker/import_worker.py) — Listens on RabbitMQ channels and consumes ingestion tasks.
*   **Chunked Stream Handler:**
    [`platform/worker/handlers/import_handler.py`](https://github.com/Rahul-pamula/ShrFlow-V1/blob/main/platform/worker/handlers/import_handler.py) — Streams the S3 resource, performs data conversions, runs email validations, and performs batch database insertion.
*   **CSV File Parser Utility:**
    [`platform/api/utils/file_parser.py`](https://github.com/Rahul-pamula/ShrFlow-V1/blob/main/platform/api/utils/file_parser.py) — Handles low-level column mapping and delimiter identification.
