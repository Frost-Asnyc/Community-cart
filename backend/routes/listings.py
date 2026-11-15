import math

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from marshmallow import ValidationError

from extensions import db
from models import Listing
from schemas.listing_schema import ListingSchema
from services.listing_service import filter_listings, get_owned_listing, mark_sold

listings_bp = Blueprint("listings_bp", __name__, url_prefix="/api/listings")
listing_schema = ListingSchema()
listings_schema = ListingSchema(many=True)


@listings_bp.get("")
def list_listings():
    min_price, error = _price_filter("min")
    if error:
        return jsonify({"error": error}), 400

    max_price, error = _price_filter("max")
    if error:
        return jsonify({"error": error}), 400

    if min_price is not None and max_price is not None and min_price > max_price:
        return jsonify({"error": "min must not be greater than max"}), 400

    listings = filter_listings(
        category=request.args.get("category") or None,
        search=request.args.get("q") or None,
        min_price=min_price,
        max_price=max_price,
    )
    return jsonify(listings_schema.dump(listings)), 200


@listings_bp.get("/<int:listing_id>")
def get_listing(listing_id):
    listing = db.session.get(Listing, listing_id)
    if listing is None:
        return jsonify({"error": "Listing not found"}), 404
    return jsonify(listing_schema.dump(listing)), 200


@listings_bp.post("")
@login_required
def create_listing():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    try:
        listing = Listing(**listing_schema.load(data))
    except ValidationError as error:
        return jsonify({"error": "Invalid listing data", "details": error.messages}), 400

    listing.owner_id = current_user.id
    db.session.add(listing)
    db.session.commit()
    return jsonify(listing_schema.dump(listing)), 201


@listings_bp.patch("/<int:listing_id>")
@login_required
def update_listing(listing_id):
    listing = get_owned_listing(listing_id, current_user)
    if listing is None:
        return jsonify({"error": "Listing not found"}), 404

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    try:
        updates = listing_schema.load(data, partial=True)
    except ValidationError as error:
        return jsonify({"error": "Invalid listing data", "details": error.messages}), 400

    if not updates:
        return jsonify({"error": "No editable listing fields provided"}), 400

    for field, value in updates.items():
        setattr(listing, field, value)
    db.session.commit()
    return jsonify(listing_schema.dump(listing)), 200


@listings_bp.delete("/<int:listing_id>")
@login_required
def delete_listing(listing_id):
    listing = get_owned_listing(listing_id, current_user)
    if listing is None:
        return jsonify({"error": "Listing not found"}), 404

    db.session.delete(listing)
    db.session.commit()
    return jsonify({"message": "Listing deleted"}), 200


@listings_bp.patch("/<int:listing_id>/sold")
@login_required
def sell_listing(listing_id):
    listing = get_owned_listing(listing_id, current_user)
    if listing is None:
        return jsonify({"error": "Listing not found"}), 404

    listing = mark_sold(listing)
    return jsonify(listing_schema.dump(listing)), 200


def _price_filter(parameter):
    raw_value = request.args.get(parameter)
    if raw_value is None or raw_value == "":
        return None, None

    try:
        value = float(raw_value)
    except ValueError:
        return None, f"{parameter} must be a valid number"

    if not math.isfinite(value) or value < 0:
        return None, f"{parameter} must be a finite non-negative number"
    return value, None
