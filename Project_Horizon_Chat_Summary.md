# Project Horizon — Planning Session Notes
**Date:** April 8, 2026
**Participants:** Yaga + Claude
**Source Documents:** `Project_Horizon_Scope_Document_v2.2.docx`, `project-horizon-execution-plan-v1.4-final.docx`

---

## What This Is

Project Horizon is an **internal CRM platform** for Ouranos Technologies replacing spreadsheets for the Sales and Customer Success teams. It manages deal pipelines (Farming and Hunting), contacts, companies, partner quotes, and dashboards. The stack is **Django + HTMX + PostgreSQL**, deliberately kept as a monolith to match the team's current skill level and speed toward MVP.

---

## The Three Phases

**Phase 1 — MVP (Weeks 1–12):** Core CRM. Replace spreadsheets. Deals, contacts, companies, Kanban board, audit trail, dashboard. This is the current target.

**Phase 2 — Commercial Tools (Weeks 13–20):** Quote system, multi-currency, email integration, SLA tracking, partner quote requests, mobile companion (Flutter).

**Phase 3 — Integrations & Scale (Weeks 21–28):** Multi-org support, public API with idempotency, third-party connectors, bulk operations.

---

## Step-by-Step Execution Plan (Phase 1 Focus)

### Sprint 0 — Foundation (Week 1–2)

The goal here is that every developer can clone the repo, run the project locally, and see a working page before any feature work begins.

Damy initializes the Django project at `Ouranos-Lab-Africa/project-horizon` with the full app structure (`apps/accounts`, `apps/contacts`, `apps/deals`, `apps/activities`, `apps/dashboard`, `apps/config`), settings split (`base.py`, `dev.py`, `prod.py`), ruff config in `pyproject.toml`, and `.pre-commit-config.yaml`. This must be pushed by Day 1.

Nicholas starts the Figma design system and first 4 wireframes, sharing the link by Day 2.

Every developer clones the repo, runs `pip install pre-commit && pre-commit install`, and confirms local Docker Compose works (PostgreSQL + Redis + Celery + Django dev server) by Day 3.

Marcel sets up `factory_boy` factories for Contact and Company and verifies they generate valid test data by Day 5.

---

### Sprint 1 — Contacts & Companies (Week 3–4)

Marcel owns this sprint end-to-end. The business rules are strict: contacts require unique email (DB-level constraint), companies can't be soft-deleted if they have active deals, and soft-deleting a company unlinks its contacts without cascading. Permissions must match the RBAC table — Sales Rep can create, Manager+ can edit, Admin-only can delete.

Deliverables: Company CRUD, Contact CRUD with duplicate email detection, soft delete guards, all service-layer unit tests, and integration tests covering both positive and negative permission scenarios (e.g. Viewer cannot create a contact → 403).

---

### Sprint 2 — Pipeline & Deals (Week 5–6)

This sprint has a mandatory execution sequence to manage complexity for a junior team.

**Days 1–7 (backend only):** Pipeline, Stage, StageMapping, and StageTransition models. `DealService` and `TransitionService` with `@transaction.atomic`. The model-level stage guard (`Deal.save()` raises `RuntimeError` if stage is changed directly). All backend tests must pass before any UI work begins.

**Days 5–8 (parallel):** Ridwan builds a static Kanban board with SortableJS using hardcoded data. Validates drag-and-drop UX independently. Test with 2–3 Sales users for usability feedback before wiring live data.

**Days 9–12:** Wire SortableJS `onEnd` to `POST /deals/{id}/transition/`. Handle 200 (success + HTML fragment swap) and 400 (revert card position). Deal detail template and activity log panel.

Key constraint: closing a deal is NOT a separate `/close/` endpoint — it's a transition to a terminal stage. Once a deal reaches a terminal stage (Won or Lost), no further transitions are allowed. This is enforced at three levels: DB trigger, API layer (422 response), and Django model validation.

---

### Sprint 3 — Activities, Audit Trail & Dashboard (Week 7–8)

Activity logging for every entity mutation. Dashboard aggregation with role-scoped caching (`dashboard_summary_{user_role}`, 5-minute TTL, database cache backend). `invalidate_dashboard_cache()` must be called by every service function that mutates deal data — this is the single point of cache control. PR review rotation begins: Marcel reviews frontend/template PRs, Damy continues reviewing all service, model, and permission-touching PRs.

---

### Sprint 4 — Polish & Bug Fixes (Week 9–10)

Fix all P0/P1 bugs from Ibukun's QA reports. UI consistency pass. Performance check on slow queries. User Acceptance Testing with 2–3 Sales team members. Write the deployment runbook.

---

### Hardening Buffer (Week 11–12)

This buffer is non-negotiable. Fix UAT-discovered bugs. Final security review (no debug endpoints, no hardcoded secrets, all permission checks verified). Deploy to production RHEL 9 VM with Gunicorn + Nginx. Seed production DB with real pipelines, stages, and SystemConfig (base currency + default timezone). Team walkthrough with Sales and CS stakeholders.

---

## Critical Non-Negotiables

**Stage transitions must only go through `TransitionService`.** Direct `deal.current_stage = x; deal.save()` is blocked by a model-level guard. Any PR that bypasses this is rejected.

**Every multi-write service must be `@transaction.atomic`.** Partial writes corrupt the audit trail. The three mandatory ones are `TransitionService.transition_stage()`, `DealService.create_deal()`, and `ContactService.soft_delete()`.

**Test database must be PostgreSQL, not SQLite.** DB triggers and CHECK constraints behave differently. This is enforced in the test config.

**`SystemConfig` is the single source of truth** for base currency and default timezone. SLA calculations and FX normalisation both anchor to this — never server time or hardcoded values.

**Damy is the single point of failure.** The plan explicitly calls this out. Mitigations: Marcel fully owns Contact + Company (not assists — owns), pair programming on the Pipeline engine in Sprint 1, and Damy writing one-page guides for `TransitionService` and `DealService` as bus-factor insurance.

---

## Immediate Next Actions

1. Damy initializes the repo skeleton and pushes by end of Day 1
2. Nicholas shares the Figma wireframes link by Day 2
3. Everyone clones, runs `pre-commit install`, and confirms local setup by Day 3
4. Marcel sets up `CompanyFactory` and `ContactFactory` with `factory_boy` by Day 5
5. GitHub issues created for every Sprint 0 task with assignments — Damy owns this by Day 1

---

## Full Installation List

### Docker & Infrastructure

- **Docker Desktop** — runs the entire local environment
- **Docker Compose** — orchestrates containers (PostgreSQL, Redis, Celery, Django dev server)

The following run **inside Docker** (defined in `docker-compose.yml`, not installed directly):
- PostgreSQL 15+
- Redis 7+

---

### Python & Core Backend

- **Python 3.12** — target version specified in `pyproject.toml`
- **pip** — comes with Python

**Python packages (`requirements.txt`):**

| Package | Purpose |
|---|---|
| `django` | Core framework |
| `djangorestframework` | DRF — added for Phase 2 Flutter readiness |
| `django-environ` | Loads secrets from `.env` |
| `django-dirtyfields` | Required for `Deal` model-level stage guard |
| `msal` / `django-allauth` | O365 SSO authentication |
| `celery` | Async task queue (email, SLA checker, daily jobs) |
| `redis` | Python client for Celery's Redis broker |
| `django-simple-history` | Field-level audit logging |
| `gunicorn` | WSGI server for production |

---

### Code Quality & Testing

| Tool | Purpose |
|---|---|
| `pre-commit` | Enforces ruff hooks before every git commit |
| `ruff` | Linter + formatter (replaces flake8 + black + isort) |
| `mypy` | Type checking — runs in CI |
| `pytest` | Test runner |
| `pytest-django` | Django integration for pytest |
| `factory_boy` | Test data factories |
| `Faker` | Realistic test data (used by factory_boy) |

---

### Frontend (CDN only — nothing to install)

| Library | Purpose |
|---|---|
| HTMX | Dynamic partial updates without a JS framework |
| SortableJS | Kanban drag-and-drop |
| Tailwind CSS | Utility-first styling |

All three are loaded via CDN in `base.html`. No npm, no build pipeline.

---

### Git & Workflow

- **Git** — source control
- **GitHub CLI (`gh`)** — optional, useful for managing issues and PRs from terminal

---

### Production Only (not needed locally)

- **Nginx** — reverse proxy in front of Gunicorn on the RHEL 9 VM
- **pgBouncer** — connection pooling (optional, future consideration)

---

### New Developer Setup — Step by Step

```bash
# 1. Install Docker Desktop + Python 3.12 (from their websites)

# 2. Clone the repo
git clone https://github.com/Ouranos-Lab-Africa/project-horizon
cd project-horizon

# 3. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 4. Install Python dependencies
pip install -r requirements.txt

# 5. Set up pre-commit hooks
pip install pre-commit
pre-commit install

# 6. Copy and configure environment variables
cp .env.example .env

# 7. Start Docker containers (PostgreSQL + Redis)
docker compose up -d

# 8. Run migrations
python manage.py migrate

# 9. Load seed data
python manage.py loaddata seed

# 10. Start the development server
python manage.py runserver
```

---

*End of session notes.*
