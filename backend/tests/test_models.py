import unittest

from app.models import Listing


class ListingModelTests(unittest.TestCase):
    def test_listing_to_dict_uses_api_field_names(self):
        listing = Listing(
            id="listing-1",
            title="Wooden stool",
            description="Solid stool for a studio.",
            category="Furniture",
            price=42.5,
            image="https://example.com/stool.jpg",
            location="Brooklyn",
            status="active",
            seller_id="seller-1",
        )

        payload = listing.to_dict()

        self.assertEqual(payload["id"], "listing-1")
        self.assertEqual(payload["sellerId"], "seller-1")
        self.assertEqual(payload["price"], 42.5)
        self.assertIn("createdAt", payload)
        self.assertIn("deadline", payload)


if __name__ == "__main__":
    unittest.main()
