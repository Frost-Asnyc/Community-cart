# Community Cart

A local community marketplace API where users buy, sell, and make private sealed offers on second-hand items nearby.

Built with **Flask + SQLAlchemy + Marshmallow + Flask-Login**. Interactive API docs at `/apidocs` (Swagger UI). 68 automated tests.

---

## Setup

All commands run from **`client-with-sessions/backend/`**.

### 1. Clone and enter the project

```bash
git clone https://github.com/VincentKulankash/Community-cart.git
cd Community-cart/client-with-sessions/backend


### 2. Create a virtual environment
bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate


### 3. Install dependencies
bash
pip install -r requirements.txt


### 4. Configure environment variables
bash
cp .env.example .env
Open .env and fill in:

env
SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_hex(32))">
DATABASE_URL=sqlite:///app.db
MAILTRAP_USERNAME=<from mailtrap.io sandbox>
MAILTRAP_PASSWORD=<from mailtrap.io sandbox>
MAILTRAP_SERVER=sandbox.smtp.mailtrap.io
MAILTRAP_PORT=587
Get Mailtrap credentials at mailtrap.io → Email Sandbox → SMTP Settings.

### 5. Run migrations
bash
flask db upgrade
### 6. Seed sample data (optional but recommended)
bash
python seed.py
Creates 5 users, 20 listings, 5 favorites, 3 inquiries, 3 offers. All seeded users share the password CommunityCart2026!. First user: maya.chen@example.com.

### 7. Start the server
bash
flask run
API: http://127.0.0.1:5000

Swagger UI: http://127.0.0.1:5000/apidocs

Running tests
bash
pytest -v
68 tests use an in-memory SQLite database — your real app.db is untouched.

Production start
bash
gunicorn "app:create_app()" --bind 0.0.0.0:5000
The Procfile and runtime.txt in the backend folder are ready for Render deployment.

