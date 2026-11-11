import unittest

from app.schemas import ListingSchema


class ListingSchemaTests(unittest.TestCase):
    def test_load_valid_payload(self):
        payload = {
            "title": "Desk Lamp",
            "description": "Warm light and compact form.",
            "category": "Home",
            "price": 74,
            "image": "https://example.com/lamp.jpg",
            "location": "Queens",
            "sellerId": "seller-2",
        }

        validated = ListingSchema.load(payload)

        self.assertEqual(validated["title"], "Desk Lamp")
        self.assertEqual(validated["price"], 74.0)
        self.assertEqual(validated["location"], "Queens")

    def test_load_invalid_price_raises(self):
        with self.assertRaises(ValueError):
            ListingSchema.load({
                "title": "Bad listing",
                "description": "No price",
                "category": "Misc",
                "price": "not-a-number",
            })


if __name__ == "__main__":
    unittest.main()
