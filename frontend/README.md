# LocalLoop frontend

Responsive React/Vite prototype for local second-hand listings, private sealed
offers, deadline-based winner selection, favorites, inquiries, and a personal
dashboard.

## Run locally

```sh
npm install
npm run dev
```

## Phase 1: Fake Store API

Browse and listing details load products from
[Fake Store API](https://fakestoreapi.com/). Creating, editing, and deleting
products call its corresponding endpoints. Fake Store API simulates writes
instead of persisting them, so the frontend keeps those changes in browser
`localStorage` for this demo. Existing local sample listings remain available.

Offers, favorites, inquiries, demo identities, and LocalLoop-only listing
metadata (such as neighborhood and offer deadline) still use browser storage.
This is not real authentication or private sealed-offer storage: browser data
is inspectable, and there is no email service or Flask backend connection yet.
Phase 2 will replace the API adapter with the agreed Flask endpoint contract.
