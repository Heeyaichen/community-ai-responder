test_sql
 test_sql.py
```sql
-- Get counts by status
SELECT 
    id,
    skool_post_id,
    reply_count,
    processed,
    scraped_at,
FROM posts 
WHERE reply_count = 0
ORDER by scraped_at DESC;

SELECT id, category, content, author, post_url
from ai_responses ar
where response_id = ai_responses.id
and post_id = ai_responses.post_id
order by ai_responses.id;
