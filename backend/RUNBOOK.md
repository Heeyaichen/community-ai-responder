# Community AI Responder - Deployment Runbook

s

## 1. Local Development Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 15.x
- Docker and Docker Compose
- Apify CLI
- OpenAI API key

- Skool account credentials (for reply posting)

### Initial Setup

```bash
docker compose up --build

docker compose up -d postgres redis

docker compose exec -it postgres psql -U postgres -c "CREATE DATABASE community_ai;"
```

### Install Backend Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

````

### Initialize Database
```bash
alembic upgrade head
````

### Run the Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 2. Apify Actor Development

### Local Testing

```bash
npm start
```

### Deploy to Apify

```bash
npx apify login
npx apify push
```

### Configure Webhook

1. Get your backend URL (for local testing, use ngrok)
2. Set `ADMIN_WEBHOOK_URL` in the Apify Actor environment:
   - Format: `https://your-ngrok-url.ngrok.io/ingest/post`
3. Run the Actor to test the webhook integration

4. Verify posts appear in database
5. Check queue worker is processing jobs
6. Review AI responses in moderation UI

## 3. End-to-End Testing

### Simulate Post In Database

```sql
INSERT INTO posts (skool_post_id, title, content, category, author, post_url, reply_count, created_at)
VALUES (
    'test-post-001',
    'Test Post',
    'This is a test post with a question about deployment.',
    'troubleshooting',
    'test_user',
    'https://skool.com/test-post-001',
    0,
    NOW()
);
```

### Check Job Processing

```bash
curl http://localhost:8000/jobs/pending
```

### Wait for job processing (5-10 seconds)

### Verify AI response generated

```bash
curl http://localhost:8000/responses/pending
```

### Moderate response

```bash
curl -X POST http://localhost:8000/responses/{response_id}/approve \
  -H "Content-Type: application/json" \
  -d '{"reviewer": "test_user"}'
```

### Post reply (simulated)

```bash
curl -X POST http://localhost:8000/admin/post-reply \
  -H "Content-Type: application/json" \
  -d '{
    "post_url": "https://skool.com/test-post-001",
    "response_text": "Great question! Here are some steps to help..."
  }'
```

## 4. Production Deployment

### Environment Variables

| Variable                  | Description               | Default                                                     |
| ------------------------- | ------------------------- | ----------------------------------------------------------- |
| `DATABASE_URL`            | PostgreSQL connection URL | `postgresql://postgres:postgres@postgres:5432/community_ai` |
| `REDIS_URL`               | Redis connection URL      | `redis://localhost:6379`                                    |
| `OPENAI_API_KEY`          | OpenAI API key            | Required                                                    |
| `OPENAI_MODEL`            | Model to use              | `gpt-4o-mini`                                               |
| `QUALITY_SCORE_THRESHOLD` | Minimum quality score     | `3.0`                                                       |
| `REPLY_POSTING_ENABLED`   | Enable reply bot          | `false`                                                     |
| `SKOOL_EMAIL`             | Skool login email         | Required for reply posting                                  |
| `SKOOL_PASSWORD`          | Skool login password      | Required for reply posting                                  |
| `JOB_MAX_ATTEMPTS`        | Max job retry attempts    | `3`                                                         |
| `JOB_QUEUE_POLL_INTERVAL` | Seconds between job polls | `5`                                                         |
| `POST_MAX_AGE_HOURS`      | Max post age to process   | `24`                                                        |

### Deployment Steps

1. Deploy PostgreSQL and Redis (or use managed services)
2. Build and push Docker image
3. Run database migrations
4. Start the API server
5. Start queue worker
6. Enable reply posting (set `REPLY_POSTING_ENABLED=true`)
7. Monitor and logs

8. Scale based on usage

9. Schedule periodic scraping (cron)

10. Monitor AI response quality
11. Gradual automation (after quality metrics are good)

### Monitoring

#### Logs

- Application logs: `logs/` directory (JSON lines)
- Database query logs: PostgreSQL slow query logs
- External API logs: HTTP request/response logs

#### Metrics

- Posts processed per hour
- Response approval rate
- Response rejection rate
- Average response time
- Queue depth

- Error rate

#### Alerts

- Failed jobs
- Low quality responses
- High error rate

### Health Checks

```bash
curl http://localhost:8000/health
curl http://localhost:8000/admin/health
```

### Database Verification

```sql
SELECT COUNT(*) FROM posts WHERE reply_count = 0;
SELECT COUNT(*) FROM ai_responses WHERE status = 'pending';
SELECT COUNT(*) FROM jobs_queue WHERE status = 'pending';
```

## 5. Safety & Rate Limiting

### Bot Detection Prevention

- Random delays between posts (5-15 seconds)
- Limit posts per hour
- Use human-like typing patterns
- Vary reply content
- Never post identical replies

### Rate Limits

- Max 100 posts per hour
- Max 50 replies per hour
- Minimum 30 second delay between posts

- 31-60 second delay between retries

### Account Safety

- Use separate bot account
- Clear bot identification in profile
- Never share credentials

- Monitor for unusual activity patterns
