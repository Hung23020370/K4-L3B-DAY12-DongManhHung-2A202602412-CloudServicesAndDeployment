"""CP3 — Rate limiting bằng thuật toán sliding window."""

from __future__ import annotations

import time
import uuid

from fastapi import HTTPException, status

WINDOW_SECONDS = 60


class RateLimiter:
    def __init__(self, client, limit_per_minute: int) -> None:
        self.client = client
        self.limit = limit_per_minute

    @staticmethod
    def _key(user_id: str) -> str:
        """CHO SẴN — mỗi user một key riêng."""
        return f"ratelimit:{user_id}"

    def hit_count(self, user_id: str, now: float | None = None) -> int:
        """Số request của user trong ``WINDOW_SECONDS`` giây gần nhất."""
        now = now if now is not None else time.time()
        key = self._key(user_id)

        # Xóa các entry cũ hơn cửa sổ trượt (trước now - WINDOW_SECONDS)
        self.client.zremrangebyscore(key, 0, now - WINDOW_SECONDS)

        # Đếm số lượng entry còn lại trong window
        return int(self.client.zcard(key))

    def check(self, user_id: str, now: float | None = None) -> None:
        """Cho qua nếu còn quota, ngược lại raise 429."""
        now = now if now is not None else time.time()
        key = self._key(user_id)

        # Kiểm tra trước
        count = self.hit_count(user_id, now)
        if count >= self.limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="rate limit exceeded",
                headers={"Retry-After": str(WINDOW_SECONDS)},
            )

        # Ghi nhận sau
        member = f"{now}:{uuid.uuid4().hex}"
        self.client.zadd(key, {member: now})
        self.client.expire(key, WINDOW_SECONDS)