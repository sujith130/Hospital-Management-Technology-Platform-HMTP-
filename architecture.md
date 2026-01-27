# 🏥 Hospital Management Technology Platform (HMTP)

## Enterprise, Multi-Tenant, Cloud-Native Architecture

---

## 1. Purpose

This document defines the **end-to-end architecture** of the Hospital Management Technology Platform (HMTP).  
It is written to be **human-readable** and **AI-tool-friendly** (Cursor, GitHub Copilot, IDE agents, system-design tools).

The platform is designed as a **multi-hospital SaaS**, supporting clinical workflows, billing, compliance, and cloud-native scalability.

---

## 2. High-Level Architecture

### System Overview

- Frontend: Role-based dashboards (Next.js)
- Backend: FastAPI platform services
- Data: Tenant-isolated PostgreSQL
- Infra: Docker + Kubernetes + HPA
- Observability: Prometheus + Grafana

### Mermaid Diagram – High Level

```mermaid
graph TD
    UI[Next.js Frontend] -->|JWT| API[FastAPI API Gateway]
    API --> AUTH[Auth & RBAC]
    API --> PAT[Patient Service]
    API --> DOC[Doctor Service]
    API --> APP[Appointment Service]
    API --> PHARM[Pharmacy Service]
    API --> LAB[Lab Service]
    API --> BILL[Billing & Payments]
    API --> AUDIT[Audit & Compliance]
    API --> METRICS[Metrics & Observability]

    PAT --> DB[(PostgreSQL)]
    DOC --> DB
    APP --> DB
    PHARM --> DB
    LAB --> DB
    BILL --> DB
    AUDIT --> DB

    API --> REDIS[(Redis Cache)]
    METRICS --> PROM[Prometheus]
    PROM --> GRAF[Grafana]
```

---

## 3. Architectural Principles

### Platform-First Design
- Shared authentication, audit, and observability
- Independent domain modules
- Consistent REST APIs

### Tenant Isolation
- Single database
- `hospital_id` enforced on all domain entities
- Query-level isolation

### Healthcare Compliance
- Audit trails
- Role-based access
- Immutable logs

---

## 4. Module Architecture

### Application Modules

- Auth & Identity
- Patient Management
- Doctor & Availability
- Appointment Scheduling
- Pharmacy
- Laboratory
- Billing & Payments
- Insurance Claims
- Audit & Compliance
- Observability & Metrics

### Mermaid Diagram – Module Layer

```mermaid
graph LR
    AUTH[Auth]
    PAT[Patients]
    DOC[Doctors]
    APP[Appointments]
    PHARM[Pharmacy]
    LAB[Laboratory]
    BILL[Billing]
    INS[Insurance]
    AUDIT[Audit]
    OBS[Observability]

    AUTH --> PAT
    AUTH --> DOC
    AUTH --> APP
    AUTH --> PHARM
    AUTH --> LAB
    AUTH --> BILL

    APP --> BILL
    PHARM --> BILL
    LAB --> BILL
    BILL --> INS

    PAT --> AUDIT
    DOC --> AUDIT
    BILL --> AUDIT
```

---

## 5. Multi-Tenant Architecture

### Tenant Strategy

- Single PostgreSQL database
- `hospital_id` column on all domain tables
- Hospital context embedded in JWT

### Tenant Enforcement Flow

```mermaid
sequenceDiagram
    participant User
    participant API
    participant DB

    User->>API: Request with JWT
    API->>API: Extract hospital_id
    API->>DB: Query with hospital_id filter
    DB-->>API: Tenant-scoped data
    API-->>User: Response
```

Guarantee: **No cross-hospital data leakage**.

---

## 6. Authentication & Authorization

### Auth Flow

```mermaid
sequenceDiagram
    participant User
    participant API

    User->>API: Login (credentials)
    API-->>User: JWT (user_id, role, hospital_id)
    User->>API: API request + JWT
    API->>API: Validate token & RBAC
    API-->>User: Authorized response
```

### Security Characteristics
- bcrypt password hashing
- 90-minute JWT expiration
- Dependency-based RBAC

---

## 7. Core Business Workflows

### OPD Workflow

```mermaid
flowchart LR
    P[Patient Registration]
    A[Appointment Booking]
    D[Doctor Consultation]
    R[Prescription]
    B[Billing]
    PAY[Payment]

    P --> A --> D --> R --> B --> PAY
```

### Laboratory Workflow

```mermaid
flowchart LR
    T[Test Ordered]
    S[Sample Collected]
    C[Result Completed]
    V[Verified]
    D[Doctor Access]

    T --> S --> C --> V --> D
```

### Pharmacy Workflow

```mermaid
flowchart LR
    PR[Prescription]
    ST[Stock Check]
    MI[Medicine Issued]
    INV[Inventory Updated]
    BILL[Billing Sync]

    PR --> ST --> MI --> INV --> BILL
```

---

## 8. Audit & Compliance Architecture

### Audit Strategy
- Middleware-driven logging
- Immutable audit records
- Covers all sensitive operations

### Mermaid Diagram – Audit Flow

```mermaid
sequenceDiagram
    participant API
    participant AUDIT
    participant DB

    API->>AUDIT: Action metadata
    AUDIT->>DB: Store audit log
```

---

## 9. Observability & Monitoring

### Metrics Pipeline

```mermaid
graph LR
    API[FastAPI] --> PROM[Prometheus]
    PROM --> GRAF[Grafana]
```

Metrics include:
- API latency
- Error rate
- OPD traffic
- Billing throughput

---

## 10. Deployment Architecture (Kubernetes)

### Cloud-Native Stack

- Docker containers
- Kubernetes deployments
- Horizontal Pod Autoscaler (HPA)

### Mermaid Diagram – K8s Deployment

```mermaid
graph TD
    USER[Users]
    USER --> LB[Ingress / Load Balancer]
    LB --> POD1[API Pod]
    LB --> POD2[API Pod]

    POD1 --> DB[(PostgreSQL)]
    POD2 --> DB

    POD1 --> REDIS[(Redis)]
    POD2 --> REDIS
```

---

## 11. CI/CD Architecture

### Pipeline

```mermaid
graph LR
    GIT[Git Push]
    BUILD[Build & Test]
    DOCKER[Docker Image]
    DEPLOY[Kubernetes Deploy]

    GIT --> BUILD --> DOCKER --> DEPLOY
```

---

## 12. Repository Structure

```
hospital-platform/
├── backend/
│   ├── app/
│   │   ├── auth/
│   │   ├── patients/
│   │   ├── doctors/
│   │   ├── appointments/
│   │   ├── pharmacy/
│   │   ├── labs/
│   │   ├── billing/
│   │   ├── audit/
│   │   └── core/
│   └── main.py
├── frontend/
│   ├── pages/
│   ├── components/
│   └── services/
├── k8s/
├── docker-compose.yml
├── ARCHITECTURE.md
└── README.md
```

---

## 13. Final Architecture Statement

> HMTP is a **cloud-native, multi-tenant hospital management platform** designed with platform-first principles, healthcare compliance, and Kubernetes-based scalability, suitable for enterprise deployment and system design interviews.

