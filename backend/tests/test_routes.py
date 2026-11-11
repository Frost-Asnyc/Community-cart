import unittest

from app import create_app


class RouteTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_health_route(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_listings_route_returns_items(self):
        response = self.client.get("/api/listings")
        self.assertEqual(response.status_code, 200)
        self.assertIn("items", response.get_json())

    def test_create_listing_route(self):
        payload = {
            "title": "Canvas print",
            "description": "Bright abstract artwork with warm colors.",
            "category": "Art",
            "price": 120,
            "location": "West End",
            "sellerId": "seller-5",
        }

        response = self.client.post("/api/listings", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["title"], "Canvas print")

    def test_invalid_payload_route(self):
        response = self.client.post("/api/listings", json={
            "title": "Bad",
            "description": "Missing price",
            "category": "Art",
            "price": "abc",
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())


if __name__ == "__main__":
    unittest.main()
