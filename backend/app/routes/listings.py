from __future__ import annotations

from flask import Blueprint, jsonify, request

from ..dummyjson import (
    create_listing,
    delete_listing,
    get_listing_by_id,
    list_listings,
    update_listing,
)
from ..schemas import ListingSchema

listings_bp = Blueprint("listings_bp", __name__, url_prefix="/api")


@listings_bp.get("/health")
def health():
    return jsonify({"status": "ok", "service": "community-cart"})


@listings_bp.get("/listings")
def get_listings():
    return jsonify({"items": [ListingSchema.dump(item) for item in list_listings()]})


@listings_bp.get("/listings/<listing_id>")
def get_listing(listing_id: str):
    listing = get_listing_by_id(listing_id)
    if listing is None:
        return jsonify({"error": "Listing not found"}), 404
    return jsonify(ListingSchema.dump(listing))


@listings_bp.post("/listings")
def post_listing():
    payload = request.get_json(silent=True) or {}
    try:
        validated = ListingSchema.load(payload)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    listing = create_listing(validated)
    return jsonify(ListingSchema.dump(listing)), 201


@listings_bp.put("/listings/<listing_id>")
def put_listing(listing_id: str):
    payload = request.get_json(silent=True) or {}
    try:
        validated = ListingSchema.load(payload)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    listing = update_listing(listing_id, validated)
    if listing is None:
        return jsonify({"error": "Listing not found"}), 404
    return jsonify(ListingSchema.dump(listing))


@listings_bp.delete("/listings/<listing_id>")
def delete_listing_route(listing_id: str):
    deleted = delete_listing(listing_id)
    if not deleted:
        return jsonify({"error": "Listing not found"}), 404
    return jsonify({"deleted": True, "id": listing_id})
