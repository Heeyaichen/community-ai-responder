from dataclasses import dataclass
from typing import Optional, List


@dataclass
class PostContext:
    post_id: int
    category: Optional[str]
    content: Optional[str]
    author: Optional[str]
    title: Optional[str]
    community_tone: str = "helpful, concise, practical"


class ContextBuilder:
    CATEGORY_INTENTS = {
        "troubleshooting": "solve problem",
        "general": "discussion",
        "wins": "celebrate",
        "progress": "feedback",
        None: "general discussion",
    }

    def build(self, post) -> PostContext:
        return PostContext(
            post_id=post.id,
            category=post.category,
            content=post.content,
            author=post.author,
            title=post.title,
        )

    def get_intent(self, category: Optional[str]) -> str:
        return self.CATEGORY_INTENTS.get(category, "general discussion")
