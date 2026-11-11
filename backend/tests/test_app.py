import unittest

from app import create_app


class AppTests(unittest.TestCase):
    def test_create_app_registers_routes(self):
        app = create_app()
        self.assertTrue(app.url_map.iter_rules())
        self.assertIn("/api/health", str(app.url_map))


if __name__ == "__main__":
    unittest.main()
