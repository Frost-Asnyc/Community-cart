import unittest

from app.dummyjson import create_listing, delete_listing, get_listing_by_id, list_listings, update_listing


class DummyJsonStoreTests(unittest.TestCase):
    def test_listing_lifecycle(self):
        before = len(list_listings())

        created = create_listing({
            "title": "Ceramic vase",
            "description": "Handmade ceramic vase in warm beige tones.",
            "category": "Decor",
            "price": 59,
            "location": "Harbor",
            "sellerId": "seller-3",
        })

        self.assertEqual(created.title, "Ceramic vase")
        self.assertEqual(len(list_listings()), before + 1)

        fetched = get_listing_by_id(created.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.title, "Ceramic vase")

        updated = update_listing(created.id, {
            "title": "Updated ceramic vase",
            "description": "Updated description.",
            "category": "Decor",
            "price": 69,
            "location": "Harbor",
            "sellerId": "seller-3",
        })
        self.assertEqual(updated.title, "Updated ceramic vase")

        self.assertTrue(delete_listing(created.id))
        self.assertIsNone(get_listing_by_id(created.id))


if __name__ == "__main__":
    unittest.main()
