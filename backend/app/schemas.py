from __future__ import annotations

from typing import Any


class ListingSchema:
    @staticmethod
    def load(data: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(data, dict):
            raise ValueError("Listing payload must be a JSON object.")

        title = str(data.get("title", "")).strip()
        description = str(data.get("description", "")).strip()
        category = str(data.get("category", "")).strip()
        price = data.get("price")

        if not title:
            raise ValueError("title is required.")
        if not description:
            raise ValueError("description is required.")
        if not category:
            raise ValueError("category is required.")
        try:
            numeric_price = float(price)
        except (TypeError, ValueError):
            raise ValueError("price must be a valid number.") from None

        return {
            "title": title,
            "description": description,
            "category": category,
            "price": numeric_price,
            "image": str(data.get("image") or ""),
            "location": str(data.get("location") or "Remote"),
            "status": str(data.get("status") or "active"),
            "sellerId": str(data.get("sellerId") or "demo-user"),
        }

    @staticmethod
    def dump(listing: Any) -> dict[str, Any]:
        if hasattr(listing, "to_dict"):
            return listing.to_dict()
        return dict(listing)


class ValidationError(ValueError):
    pass
