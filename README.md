# Smart Email Manager (`email-manager`)

Smart Email Manager is a full-stack web application that connects to **AGY containers** to intelligently analyze inboxes, clean old or useless emails, and group conversations by topic.

## Core Capabilities

1. **AGY Container Email Analysis**: Dispatches email metadata and content batches to isolated AGY container workers (`AgyContainerAnalyzerAdapter`) for semantic classification, urgency scoring, and executive thread summaries.
2. **Smart Inbox Cleanup**: Automatically flags stale newsletters, expired promotional campaigns, and read low-priority notifications with actionable `keep`, `archive`, or `delete` recommendations.
3. **Topic Clustering**: Groups related messages into structured topic clusters (`Work & Projects`, `Finance & Billing`, `Security & Account`, `Promotions & Newsletters`, `General Updates`).

## Layered Service Architecture

```text
backend/
├── api/             # FastAPI HTTP routes (routes.py) and Pydantic v2 DTOs (dto.py)
├── application/     # Use-case orchestration (EmailManagementService)
├── domain/          # Pure entities, value objects, and EmailAnalyzerPort ABC
├── infrastructure/  # AgyContainerAnalyzerAdapter for AGY container communication
├── injection/       # Composition root wiring ports to concrete adapters
├── config/          # Typed Settings leaf module
├── utils/           # Stateless subject normalization and preview truncation helpers
└── main.py          # FastAPI application entrypoint
frontend/            # React + Vite web UI
tests/               # In-process unit and API route integration tests
```

## Running Tests

```bash
pytest
```

## Companion Documentation & E2E Repository

Product documentation (PRD, SDD, Day-0 User Guide), the local `docker-compose.yml` multi-container environment, and BDD E2E acceptance suites are maintained in the companion [`email-manager-docs`](https://github.com/lumenconsultancyae/email-manager-docs) repository.
