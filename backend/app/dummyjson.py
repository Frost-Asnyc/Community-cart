from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Listing

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "dummy_products.json"


def _default_seed() -> list[dict[str, Any]]:
    return [
        {
            "id": "listing-bike",
            "title": "City bike, ready for a new ride",
            "description": "A sturdy 7-speed city bike in good condition for daily commuting and weekend rides.",
            "category": "Cycling",
            "price": 220,
            "image": "https://images.unsplash.com/photo-1541625602330-2277a4c46182?auto=format&fit=crop&w=900&q=80",
            "location": "Northridge",
            "status": "active",
            "sellerId": "demo-seller",
        },
        {
            "id": "listing-lamp",
            "title": "Mid-century desk lamp",
            "description": "Warm ambient light, solid base, and a compact silhouette that fits a small studio.",
            "category": "Home",
            "price": 48,
            "image": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80",
            "location": "Downtown",
            "status": "active",
            "sellerId": "demo-seller",
        },
        {
            "id": "listing-chair",
            "title": "Oak accent chair",
            "description": "A lightly used accent chair with a clean silhouette and comfortable neutral upholstery.",
            "category": "Furniture",
            "price": 90,
            "image": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80",
            "location": "Oak Park",
            "status": "active",
            "sellerId": "demo-seller",
        },
        {
            "id": "listing-camera",
            "title": "Film camera bundle",
            "description": "Compact camera, spare rolls, and a simple strap for casual photo outings.",
            "category": "Electronics",
            "price": 310,
            "image": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=900&q=80",
            "location": "Silver Lake",
            "status": "active",
            "sellerId": "demo-seller",
        },
    ]


def _load_seed_data() -> list[dict[str, Any]]:
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text(json.dumps(_default_seed(), indent=2), encoding="utf-8")
    with DATA_FILE.open("r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


STORE = [
    Listing(
        id=item["id"],
        title=item["title"],
        description=item["description"],
        category=item["category"],
        price=float(item["price"]),
        image=item.get("image", ""),
        location=item.get("location", "Remote"),
        status=item.get("status", "active"),
        seller_id=item.get("sellerId", "demo-user"),
    )
    for item in _load_seed_data()
]


def list_listings() -> list[Listing]:
    return STORE.copy()


def get_listing_by_id(listing_id: str) -> Listing | None:
    for item in STORE:
        if item.id == listing_id:
            return item
    return None


def create_listing(payload: dict[str, Any]) -> Listing:
    listing = Listing(
        id=payload.get("id") or f"listing-{len(STORE) + 1}",
        title=payload["title"],
        description=payload["description"],
        category=payload["category"],
        price=float(payload["price"]),
        image=payload.get("image", ""),
        location=payload.get("location", "Remote"),
        status=payload.get("status", "active"),
        seller_id=payload.get("sellerId", "demo-user"),
    )
    STORE.insert(0, listing)
    return listing


def update_listing(listing_id: str, payload: dict[str, Any]) -> Listing | None:
    item = get_listing_by_id(listing_id)
    if item is None:
        return None
    item.title = payload.get("title", item.title)
    item.description = payload.get("description", item.description)
    item.category = payload.get("category", item.category)
    item.price = float(payload.get("price", item.price))
    item.image = payload.get("image", item.image)
    item.location = payload.get("location", item.location)
    item.status = payload.get("status", item.status)
    item.seller_id = payload.get("sellerId", item.seller_id)
    return item


def delete_listing(listing_id: str) -> bool:
    for index, item in enumerate(STORE):
        if item.id == listing_id:
            del STORE[index]
            return True
    return False
