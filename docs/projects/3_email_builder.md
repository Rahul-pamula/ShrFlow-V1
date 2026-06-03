# 3. No-Code Email Builder & MJML Compilation Microservice

This project implements a state-driven layout engine, providing a responsive visual design editor for creating email layouts and compiling them server-side into stable, multi-client responsive HTML payloads via MJML.

---

### Architecture Flow

```mermaid
graph TD
    classDef frontend fill:#2563eb,stroke:#1d4ed8,stroke-width:2px,color:#fff,font-weight:bold,rx:5px,ry:5px;
    classDef engine fill:#10b981,stroke:#047857,stroke-width:2px,color:#fff,font-weight:bold,rx:5px,ry:5px;
    classDef worker fill:#8b5cf6,stroke:#6d28d9,stroke-width:2px,color:#fff,font-weight:bold,rx:5px,ry:5px;
    classDef dbClass fill:#475569,stroke:#334155,stroke-width:2px,color:#fff,font-weight:bold,rx:5px,ry:5px;

    subgraph DesignStudio["Frontend Design Studio"]
        Sidebar["Elements & Templates Sidebar"]
        Store[("Centralized Design Store <br> Zustand / Redux")]
        Canvas["Reactive Canvas Renderer"]
        
        Sidebar --> |"Dispatch Action"| Store
        Store --> |"Reactive Update"| Canvas
        class Sidebar frontend;
        class Store frontend;
        class Canvas frontend;
    end

    subgraph ProcessingLayer["Template Processing Engine"]
        API["Template Service API"]
        Compiler["MJML compiler <br> JSON > HTML"]
        Validator["Layout Validation Service"]
        
        Store -.-> |"Save design_json"| API
        API --> Validator
        Validator --> Compiler
        class API engine;
        class Compiler engine;
        class Validator engine;
    end

    subgraph AsyncOperations["Async Background Workers"]
        Thumbnail["Thumbnail Worker <br> Puppeteer / Headless"]
        Versioning["Version Snapshot Service"]
        Assets["Asset Manager <br> S3 / CDN"]
        
        API --> |"Enqueue"| Thumbnail
        API --> Versioning
        Compiler --> Assets
        class Thumbnail worker;
        class Versioning worker;
        class Assets worker;
    end

    subgraph PersistenceLayer["Storage"]
        DB[("PostgreSQL <br> design_json + HTML")]
        S3Storage[("S3 Object Storage")]
        
        API --> DB
        Assets --> S3Storage
        class DB dbClass;
        class S3Storage dbClass;
    end

    classDef dualBox fill:#f8fafc,stroke:#cbd5e1,stroke-width:2px,stroke-dasharray: 4 4;
    class DesignStudio dualBox;
    class ProcessingLayer dualBox;
    class AsyncOperations dualBox;
    class PersistenceLayer dualBox;
```

---

### Technical Highlights

1. **DesignJSON as Single Source of Truth:**
   The builder stores structure as a tree containing `Rows -> Columns -> Blocks`. Absolute canvas-style positioning is forbidden. This flow-based layout design ensures 100% rendering stability across historically problematic email clients (like Microsoft Outlook).
2. **State-Driven Zustand Client Store:**
   Uses a centralized Zustand store on the client, turning every drag-and-drop or property edit into an immutable JSON tree mutation, entirely eliminating typical DOM-syncing bugs.
3. **Stateless MJML Compilation Microservice:**
   Translates custom blocks (e.g., text, images, buttons, spacer grids) into MJML XML schemas, which are then compiled server-side to generate minified, CSS-inlined, and client-compatible HTML.
4. **Pre-Send HTML Constraints checks:**
   Performs pre-validation audits, checking if the final HTML file exceeds the strict Gmail 102KB clipping threshold and verifying that merge tags (personalization tokens) have fallback defaults.

---

### Core Code File Paths

*   **MJML Compilation & Rendering Service:**
    [`platform/api/services/compile_service.py`](https://github.com/Rahul-pamula/ShrFlow-V1/blob/main/platform/api/services/compile_service.py) — Contains JSON-to-MJML translator structures and calls the MJML compilation binaries.
*   **Template Core Operations Service:**
    [`platform/api/services/template_service.py`](https://github.com/Rahul-pamula/ShrFlow-V1/blob/main/platform/api/services/template_service.py) — Handles database storage of layout configurations.
*   **Template Deconstruction & Decoupled Work:**
    [`platform/services/template_service/`](https://github.com/Rahul-pamula/ShrFlow-V1/tree/main/platform/services/template_service) — Contains microservice decomposition utilities for template isolated operations.
*   **MJML Parser Unit Tests:**
    [`platform/api/test_mjml.py`](https://github.com/Rahul-pamula/ShrFlow-V1/blob/main/platform/api/test_mjml.py) — Validates syntax outputs and compilation guarantees.
*   **Frontend Design Studio Shell:**
    [`platform/client/src/app/templates/[id]/block/ProjectsDashboard.tsx`](https://github.com/Rahul-pamula/ShrFlow-V1/blob/main/platform/client/src/app/templates/[id]/block/ProjectsDashboard.tsx) — Implements visual layout grids and blocks list.
