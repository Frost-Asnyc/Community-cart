import pytest

from app import create_app
from config import TestingConfig
from extensions import db
from models import Listing, User


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def seller(app):
    with app.app_context():
        user = User(name="Seller", email="seller@example.com", password_hash="test")
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture
def seller_client(app, seller):
    client = app.test_client()
    with client.session_transaction() as session:
        session["_user_id"] = str(seller)
        session["_fresh"] = True
    return client


@pytest.fixture
def other_user(app, seller):
    with app.app_context():
        user = User(name="Other", email="other@example.com", password_hash="test")
        db.session.add(user)
        db.session.commit()
        return user.id


def _create_listing(app, owner_id, **overrides):
    values = {
        "title": "Desk lamp",
        "description": "A used desk lamp",
        "price": 25,
        "category": "Home",
        "owner_id": owner_id,
    }
    values.update(overrides)
    with app.app_context():
        listing = Listing(**values)
        db.session.add(listing)
        db.session.commit()
        return listing.id


def test_public_listing_filters_and_details(app, seller):
    matching_id = _create_listing(app, seller, title="Blue desk lamp", price=30)
    _create_listing(app, seller, title="Red chair", price=40, category="Furniture")
    _create_listing(app, seller, title="Green lamp", price=80)

    response = app.test_client().get(
        "/api/listings?category=Home&q=lamp&min=20&max=50"
    )

    assert response.status_code == 200
    assert [listing["id"] for listing in response.json] == [matching_id]

    detail = app.test_client().get(f"/api/listings/{matching_id}")
    assert detail.status_code == 200
    assert detail.json["title"] == "Blue desk lamp"

    missing = app.test_client().get("/api/listings/999")
    assert missing.status_code == 404


def test_create_update_mark_sold_and_delete_listing(seller_client, seller):
    response = seller_client.post(
        "/api/listings",
        json={
            "title": "Bicycle",
            "description": "Works well",
            "price": 100,
            "category": "Sports",
            "location": "North",
            "user_id": 999,
        },
    )

    assert response.status_code == 201
    listing = response.json
    listing_id = listing["id"]
    assert listing["owner_id"] == seller
    assert "user_id" not in listing

    updated = seller_client.patch(
        f"/api/listings/{listing_id}", json={"price": 90, "user_id": 999}
    )
    assert updated.status_code == 200
    assert updated.json["price"] == 90
    assert updated.json["owner_id"] == seller

    sold = seller_client.patch(f"/api/listings/{listing_id}/sold")
    assert sold.status_code == 200
    assert sold.json["status"] == "sold"

    deleted = seller_client.delete(f"/api/listings/{listing_id}")
    assert deleted.status_code == 200
    assert seller_client.get(f"/api/listings/{listing_id}").status_code == 404


def test_listing_mutations_require_auth_and_hide_non_owned_listings(
    app, seller_client, other_user
):
    listing_id = _create_listing(app, other_user)

    anonymous = app.test_client()
    assert anonymous.post("/api/listings", json={}).status_code == 401

    assert (
        seller_client.patch(f"/api/listings/{listing_id}", json={"price": 10}).status_code
        == 404
    )
    assert seller_client.delete(f"/api/listings/{listing_id}").status_code == 404
    assert seller_client.patch(f"/api/listings/{listing_id}/sold").status_code == 404


def test_listing_create_and_filter_validation(seller_client):
    invalid_listing = seller_client.post(
        "/api/listings",
        json={"title": "Incomplete", "description": "Missing required fields"},
    )
    assert invalid_listing.status_code == 400

    invalid_filter = seller_client.get("/api/listings?min=abc")
    assert invalid_filter.status_code == 400

    reversed_range = seller_client.get("/api/listings?min=20&max=10")
    assert reversed_range.status_code == 400
