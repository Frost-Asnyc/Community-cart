# Community Cart frontend

A responsive React storefront with an editorial cream, navy, and orange palette,
interactive product cards, and animated 3D details.

## Run locally

```sh
npm install
npm run dev
```

The Vite server runs on port 3000. Start the Flask backend on port 5000 as well:

```sh
cd ../backend
flask db upgrade
flask run
```

The storefront loads active listings from `/api/listings`. If the database has
no active listings, it loads the public mock catalog at `/api/mock/listings`.
The mock endpoint is read-only and does not create database records.

Search, category filters, and saved finds work in the browser. Saved finds are
stored in local storage. Listing creation is still a visual placeholder.
