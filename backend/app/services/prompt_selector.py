from typing import Optional


class PromptSelector:
    SYSTEM_PROMPT = """You are an AI assistant helping a private learning community.

Your role:
- Help users with accurate, practical responses
- Maintain a human, natural tone
- Avoid sounding robotic or generic

Strict rules:
- No generic filler phrases
- No repetition
- No disclaimers like "as an AI"
- Keep responses concise but helpful"""

    TEMPLATES = {
        "troubleshooting": """Category: Troubleshooting

User Post:
{post}

Instructions:
- Identify the core problem
- Provide clear step-by-step troubleshooting
- Suggest 1-2 likely root causes
- Ask 1 clarifying question at the end

Tone:
- Practical
- Direct
- Supportive

Output:
A structured but natural response""",

        "wins": """Category: Wins

User Post:
{post}

Instructions:
- Acknowledge the achievement
- Reinforce positive behavior
- Encourage next step

Tone:
- Energetic
- Positive
- Short

Output:
A short congratulatory message with encouragement""",

        "general": """Category: General Discussion

User Post:
{post}

Instructions:
- Add value to the discussion
- Share insight or perspective
- Avoid overexplaining

Tone:
- Conversational
- Thoughtful

Output:
A natural reply that invites engagement""",

        "progress": """Category: Progress

User Post:
{post}

Instructions:
- Acknowledge the progress shown
- Offer constructive feedback
- Suggest improvements or next steps

Tone:
- Encouraging
- Constructive

Output:
A supportive response with actionable suggestions""",
    }

    def select(self, category: Optional[str], post_content: str) -> str:
        template_key = self._normalize_category(category)
        template = self.TEMPLATES.get(template_key, self.TEMPLATES["general"])
        return self.SYSTEM_PROMPT + "\n\n" + template.format(post=post_content)

    def _normalize_category(self, category: Optional[str]) -> str:
        if not category:
            return "general"
        normalized = category.lower().strip()
        for key in self.TEMPLATES:
            if key in normalized:
                return key
        return "general"
