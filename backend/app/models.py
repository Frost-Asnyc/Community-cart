from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any


@dataclass
class Listing:
    id: str
    title: str
    description: str
    category: str
    price: float
    image: str = ""
    location: str = "Remote"
    status: str = "active"
    seller_id: str = "demo-user"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    deadline: str = field(
        default_factory=lambda: (datetime.now(timezone.utc) + timedelta(days=3)).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "price": float(self.price),
            "image": self.image,
            "location": self.location,
            "status": self.status,
            "sellerId": self.seller_id,
            "createdAt": self.created_at,
            "deadline": self.deadline,
        }
