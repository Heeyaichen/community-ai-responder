from typing import Optional


class ReplyBot:
    def __init__(self, enabled: bool = False, email: str = "", password: str = ""):
        self.enabled = enabled
        self.email = email
        self.password = password

    def post_reply(self, post_url: str, response_text: str) -> bool:
        if not self.enabled:
            return self._mock_post(post_url, response_text)

        return self._playwright_post(post_url, response_text)

    def _mock_post(self, post_url: str, response_text: str) -> bool:
        print(f"[MOCK] Would post to {post_url}: {response_text[:100]}...")
        return True

    def _playwright_post(self, post_url: str, response_text: str) -> bool:
        raise NotImplementedError("Playwright posting not yet implemented")
