# Community AI Responder - Backend

s

A Python FastAPI backend that ingests posts from the Apify Actor
and generates AI-assisted replies for community posts.

## Features

- **Webhook Integration**: Apify Actor pushes scraped posts to backend via HTTP webhook
- **AI Response Generation**: OpenAI generates context-aware responses based on post content and category
- **Quality Scoring**: Responses are scored before being stored
- **Moderation API**: Human-in-loop approval/rejection workflow
- **Reply Bot**: Mocked Playwright automation for posting (Planned)

## Tech Stack

- **Python 3.11** (FastAPI)
- **PostgreSQL 15.x**: SQLAlchemy ORM with Alembic migrations
- **OpenAI API**: GPT-4o-mini for responses
- **Redis**: Optional (future scaling)

- **Docker**: For containerized deployment

- **Playwright**: For browser automation (reply posting)

## Prerequisites

- Python 3.11+
- PostgreSQL 15.x
- Docker and Docker Compose
- Apify CLI (for deployment)

- OpenAI API key

- Skool account credentials (for reply posting)

## Quick Start

### 1. Set up PostgreSQL

```bash
docker run -d --name community-postgres \
  -e POSTGRES_DB=community_ai \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
postgres
```

### 2. Install dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
```

Edit . `.env` with your actual values:

````

### 4. Initialize database
```bash
alembic upgrade head
````

### 5. Run the server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### Ingest Posts

- `POST /ingest-post` - Receive posts from Apify Actor webhook
  - `POST /ingest/batch` - Batch ingest multiple posts
    - `POST /post/{skool_post_id}/process` - Manually trigger processing for a specific post

    - `GET /responses/pending` - List pending AI responses awaiting moderation
    - `POST /responses/{id}/approve` - Approve a response
    - `POST /responses/{id}/reject` - Reject a response (with feedback)

    - `GET /jobs/pending` - List pending jobs
    - `POST /jobs/{id}/process` - Manually trigger job processing
    - `POST /init-db` - Initialize database tables
    - `GET /health` - Health check
    - `GET /admin/health` - Database health check

## Development

```bash
cd backend

source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Testing

```bash
pytest
```

## Docker Compose

```bash
docker compose up --build
docker compose up
```

## Environment Variables

| Variable                  | Description               | Default                                                      |
| ------------------------- | ------------------------- | ------------------------------------------------------------ |
| `DATABASE_URL`            | PostgreSQL connection URL | `postgresql://postgres:postgres@localhost:5432/community_ai` |
| `OPENAI_API_KEY`          | OpenAI API key            | Required                                                     |
| `OPENAI_MODEL`            | Model to use              | `gpt-4o-mini`                                                |
| `QUALITY_SCORE_THRESHOLD` | Minimum quality score     | `3.0`                                                        |
| `REPLY_POSTING_ENABLED`   | Enable reply bot          | `false`                                                      |
| `SKOOL_EMAIL`             | Skool login email         | Required for reply posting                                   |
| `SKOOL_PASSWORD`          | Skool login password      | Required for reply posting                                   |
| `JOB_MAX_ATTEMPTS`        | Max job retry attempts    | `3`                                                          |
| `JOB_QUEUE_POLL_INTERVAL` | Seconds between job polls | `5`                                                          |
| `POST_MAX_AGE_HOURS`      | Max post age to process   | `24`                                                         |

## Architecture

```
Apify Actor (Scraper)
        ↓
    FastAPI Webhook (/ingest-post)
        ↓
    PostgreSQL (posts → jobs → ai_responses)
        ↓
    Queue Worker (processes jobs)
        ↓
    LLM Service (generates responses)
        ↓
    Quality Scorer (validates responses)
        ↓
    Moderation API (human approval)
        ↓
    Reply Bot (posts to Skool)
```

## Database Schema

### posts

| Column        | Type         | Description                         |
| ------------- | ------------ | ----------------------------------- |
| id            | SERIAL       | Primary key                         |
| skool_post_id | TEXT         | Unique Skool post ID (indexed)      |
| title         | TEXT         | Post title                          |
| content       | TEXT         | Post content                        |
| category      | VARCHAR(100) | Post category                       |
| author        | VARCHAR(255) | Author name                         |
| post_url      | TEXT         | URL to post                         |
| reply_count   | INTEGER      | Number of replies (default 0)       |
| likes         | INTEGER      | Number of likes (default 0)         |
| created_at    | TIMESTAMP    | Post creation time                  |
| scraped_at    | TIMESTAMP    | When scraped (default NOW)          |
| processed     | BOOLEAN      | Whether job created (default FALSE) |

### ai_responses

| Column           | Type         | Description                      |
| ---------------- | ------------ | -------------------------------- |
| id               | SERIAL       | Primary key                      |
| post_id          | INTEGER      | Foreign key to posts.id          |
| response_text    | TEXT         | AI-generated response            |
| model_used       | VARCHAR(100) | LLM model used                   |
| prompt_version   | VARCHAR(50)  | Prompt template version          |
| quality_score    | FLOAT        | Response quality score           |
| status           | VARCHAR(50)  | pending/approved/rejected/posted |
| created_at       | TIMESTAMP    | When created (default NOW)       |
| approved_at      | TIMESTAMP    | When approved                    |
| posted_at        | TIMESTAMP    | When posted                      |
| rejection_reason | TEXT         | Reason for rejection             |

### jobs_queue

| Column       | Type        | Description                    |
| ------------ | ----------- | ------------------------------ |
| id           | SERIAL      | Primary key                    |
| post_id      | INTEGER     | Foreign key to posts.id        |
| job_type     | VARCHAR(50) | Type of job (generate_reply)   |
| status       | VARCHAR(50) | pending/processing/done/failed |
| attempts     | INTEGER     | Number of attempts (default 0) |
| scheduled_at | TIMESTAMP   | When scheduled (default NOW)   |
| updated_at   | TIMESTAMP   | Last update time               |

### moderation_logs

| Column      | Type         | Description                    |
| ----------- | ------------ | ------------------------------ |
| id          | SERIAL       | Primary key                    |
| response_id | INTEGER      | Foreign key to ai_responses.id |
| action      | VARCHAR(50)  | approved/rejected              |
| reviewer    | VARCHAR(255) | Reviewer name                  |
| feedback    | TEXT         | Feedback text                  |
| created_at  | TIMESTAMP    | When logged (default NOW)      |
