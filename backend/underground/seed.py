from datetime import datetime, timezone
from decimal import Decimal

from bson.decimal128 import Decimal128

from app import create_app
from extensions import db
from models import User
from underground.database import MARKETPLACE_ID, get_underground_products
from underground.schemas import underground_product_schema

DEMO_PRODUCTS = (
    {
        "seed_key": "alt-fashion-neon-jacket",
        "name": "Neon Circuit Jacket",
        "description": "A fictional reflective streetwear jacket for the demo catalogue.",
        "price": "74.50",
        "category": "Alternative Fashion",
        "subcategory": "Outerwear",
        "image": "https://placehold.co/640x800/171717/C3EA4F?text=Neon+Jacket",
        "availability": True,
    },
    {
        "seed_key": "alt-fashion-violet-bag",
        "name": "Violet Signal Crossbody",
        "description": "A fictional compact bag with a violet accent panel.",
        "price": "38.00",
        "category": "Alternative Fashion",
        "subcategory": "Bags",
        "image": "https://placehold.co/640x800/3B1A47/B6FF00?text=Violet+Bag",
        "availability": True,
    },
    {
        "seed_key": "gaming-arcade-controller",
        "name": "Arc Byte Controller",
        "description": "A fictional wireless controller concept for a demo gaming setup.",
        "price": "59.95",
        "category": "Gaming",
        "subcategory": "Accessories",
        "image": "https://placehold.co/640x800/171717/B6FF00?text=Arc+Byte",
        "availability": True,
    },
    {
        "seed_key": "gaming-void-art-print",
        "name": "Void Runner Art Print",
        "description": "An original fictional arcade-inspired art print.",
        "price": "24.00",
        "category": "Gaming",
        "subcategory": "Collectibles",
        "image": "https://placehold.co/640x800/3B1A47/C3EA4F?text=Void+Runner",
        "availability": True,
    },
    {
        "seed_key": "motorsports-pit-crew-tee",
        "name": "Nightshift Pit Crew Tee",
        "description": "A fictional motorsports-inspired graphic tee for demonstration.",
        "price": "32.00",
        "category": "Motorsports",
        "subcategory": "Apparel",
        "image": "https://placehold.co/640x800/171717/C3EA4F?text=Pit+Crew",
        "availability": True,
    },
    {
        "seed_key": "motorsports-track-notebook",
        "name": "Apex Track Notes",
        "description": "A fictional pocket notebook for recording track-day observations.",
        "price": "12.50",
        "category": "Motorsports",
        "subcategory": "Accessories",
        "image": "https://placehold.co/640x800/3B1A47/B6FF00?text=Track+Notes",
        "availability": True,
    },
    {
        "seed_key": "nightlife-neon-poster",
        "name": "Afterhours Neon Poster",
        "description": "A fictional nightlife-inspired poster; it is not an event ticket.",
        "price": "18.00",
        "category": "Nightlife & Entertainment",
        "subcategory": "Art & Posters",
        "image": "https://placehold.co/640x800/171717/B6FF00?text=Afterhours",
        "availability": True,
    },
    {
        "seed_key": "nightlife-signal-pin-set",
        "name": "Signal Glow Pin Set",
        "description": "A fictional set of enamel-style pins for the demo catalogue.",
        "price": "9.50",
        "category": "Nightlife & Entertainment",
        "subcategory": "Accessories",
        "image": "https://placehold.co/640x800/3B1A47/C3EA4F?text=Signal+Pins",
        "availability": True,
    },
    {
        "seed_key": "restricted-fictional-display-item",
        "name": "SIMULATED AGE-GATED DISPLAY ITEM",
        "description": (
            "Fictional school-demo placeholder only. Not a real product, ticket, "
            "pass, service, or offer and not available for purchase."
        ),
        "price": "0.00",
        "category": "Restricted Category Demo",
        "subcategory": "Fictional Placeholder",
        "image": "https://placehold.co/640x800/171717/C3EA4F?text=Demo+Only",
        "availability": False,
    },
)


def seed_underground_products(collection, vendor_ids, now=None):
    vendor_ids = tuple(vendor_ids)
    if not vendor_ids or any(type(vendor_id) is not int or vendor_id < 1 for vendor_id in vendor_ids):
        raise ValueError("At least one existing positive integer user ID is required.")

    created_at = now or datetime.now(timezone.utc)
    for index, seed_product in enumerate(DEMO_PRODUCTS):
        product = {
            key: value
            for key, value in seed_product.items()
            if key != "seed_key"
        }
        validated = underground_product_schema.load(
            {
                **product,
                "vendor_id": vendor_ids[index % len(vendor_ids)],
            }
        )
        validated["price"] = Decimal128(Decimal(validated["price"]))
        validated.update(
            marketplace=MARKETPLACE_ID,
            average_rating=0.0,
            seed_key=seed_product["seed_key"],
        )

        collection.update_one(
            {
                "marketplace": MARKETPLACE_ID,
                "seed_key": seed_product["seed_key"],
            },
            {
                "$set": validated,
                "$setOnInsert": {"created_at": created_at},
            },
            upsert=True,
        )

    return len(DEMO_PRODUCTS)


def seed_database():
    app = create_app()
    with app.app_context():
        vendor_ids = [
            user_id
            for (user_id,) in db.session.query(User.id).order_by(User.id).all()
        ]
        if not vendor_ids:
            raise RuntimeError(
                "Create at least one Community Cart user before seeding Underground."
            )

        count = seed_underground_products(
            get_underground_products(),
            vendor_ids,
        )
        print(f"Synchronized {count} fictional Underground demo products.")


if __name__ == "__main__":
    seed_database()
