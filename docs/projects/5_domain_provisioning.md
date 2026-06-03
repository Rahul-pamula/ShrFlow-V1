# 5. DKIM/SPF Domain Provisioning & SES Mail Infrastructure

This project automates the registration, configuration, and verification of sender domains. It uses AWS Boto3 to request verification tokens, exposes DNS setups for users, and integrates bounce/complaint feedback loops via AWS SNS webhooks.

---

### Architecture Flow

```mermaid
graph TD
    classDef worker fill:#8b5cf6,stroke:#6d28d9,stroke-width:2px,color:#fff,font-weight:bold,rx:5px,ry:5px;
    classDef external fill:#ef4444,stroke:#b91c1c,stroke-width:2px,color:#fff,font-weight:bold,rx:5px,ry:5px;
    classDef api fill:#10b981,stroke:#047857,stroke-width:2px,color:#fff,font-weight:bold,rx:5px,ry:5px;
    classDef database fill:#475569,stroke:#334155,stroke-width:2px,color:#fff,font-weight:bold,rx:5px,ry:5px;

    subgraph DispatchWorker["RabbitMQ Delivery Worker"]
        RMQ[("RabbitMQ Queue")]
        Injector["CAN-SPAM / HMAC Unsub Injector"]
        SMTP["Dynamic TLS SMTP Sender"]
        DLQ[("Dead Letter Queue")]
        
        RMQ --> Injector
        Injector --> SMTP
        SMTP -.-> |"Failure / Retry 3x"| DLQ
        class RMQ worker;
        class Injector worker;
        class SMTP worker;
        class DLQ worker;
    end

    subgraph ExternalProvider["Email Delivery Provider"]
        SES["AWS SES / Mailtrap"]
        Inbox["Recipient Inbox"]
        
        SMTP --> |"Authenticates & Sends"| SES
        SES --> Inbox
        class SES external;
        class Inbox external;
    end

    subgraph FeedbackLoop["Webhook Resolution API"]
        Webhook["SES Complaint/Bounce Receiver"]
        HardBounce["Hard Bounce Isolator"]
        Spam["Spam Complaint Isolator"]
        
        SES -.-> |"Fires Event"| Webhook
        Webhook --> HardBounce
        Webhook --> Spam
        class Webhook api;
        class HardBounce api;
        class Spam api;
    end

    subgraph ContactState["Contact Integrity DB"]
        Contacts[("Contacts Table")]
        Reputation[("Tenant Reputation <br> Warmup Stats")]
        
        HardBounce --> |"Sets status=bounced"| Contacts
        Spam --> |"Sets status=unsubscribed"| Contacts
        HardBounce --> Reputation
        class Contacts database;
        class Reputation database;
    end

    classDef dualBox fill:#f8fafc,stroke:#cbd5e1,stroke-width:2px,stroke-dasharray: 4 4;
    class DispatchWorker dualBox;
    class ExternalProvider dualBox;
    class FeedbackLoop dualBox;
    class ContactState dualBox;
```

---

### Technical Highlights

1. **Programmatic SES Identity Verification:**
   When a user adds a domain, the API calls AWS SES (`verify_domain_dkim`) via the Boto3 SDK, retrieving 3 generated DKIM tokens. The platform translates these into DNS CNAME records and renders them in the UI for the user to publish.
2. **DNS Verification Checks:**
   Exposes checking endpoints (`POST /domains/{id}/verify`) to query current DNS registration entries (using boto3 `get_identity_dkim_attributes` and `get_identity_verification_attributes`) and dynamically updates domain verification states to "Verified".
3. **AWS SNS Webhook Verification Loop:**
   Ingests feedback events (Hard Bounces, Spam Complaints) sent by AWS SNS. To prevent fake events from unsubscribing contacts, the webhook parses certificates and verifies the RSA signature of the SNS message before processing.
4. **Reputation Protection & Hard Suppression:**
   Hard bounces and spam complaints are instantly moved to a permanent suppression list, preventing further dispatches to keep the domain reputation high.

---

### Core Code File Paths

*   **Domain Provisioning Router:**
    [`platform/api/routes/domains.py`](https://github.com/Rahul-pamula/ShrFlow-V1/blob/main/platform/api/routes/domains.py) — Enqueues domains in AWS SES, queries verification values, and lists active DNS tokens.
*   **Sender Identities Router:**
    [`platform/api/routes/senders.py`](https://github.com/Rahul-pamula/ShrFlow-V1/blob/main/platform/api/routes/senders.py) — Handles sender email addresses validation.
*   **SNS Webhook & Signature Validation:**
    [`platform/api/routes/webhooks.py`](https://github.com/Rahul-pamula/ShrFlow-V1/blob/main/platform/api/routes/webhooks.py) — Ingests feedback loops from SES/SNS and processes bounce/complaint events.
*   **Deliverability Repositories:**
    [`platform/api/services/reputation_engine.py`](https://github.com/Rahul-pamula/ShrFlow-V1/blob/main/platform/api/services/reputation_engine.py) — Standardizes bounce rate monitoring.
