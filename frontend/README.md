# LocalLoop frontend

Responsive React/Vite prototype for local second-hand listings, private sealed
offers, deadline-based winner selection, favorites, inquiries, and a personal
dashboard.

## Run locally

```sh
npm install
npm run dev
```

## Demo behavior

The app uses realistic sample listings and stores demo listings, offers,
favorites, and inquiries in browser `localStorage`. Use the account picker in
the header to switch among demo identities and try buyer and seller workflows.
Other buyers cannot see offers, and sellers see them only after the deadline.
The dashboard then shows the highest offer, using the earliest timestamp to
break a tie; buyers can always see their own offer. This is only a UI
simulation: browser storage is inspectable and does not provide real privacy or
access control. No email, authentication, or backend service is connected.

The browser data layer is in `src/api/localLoopApi.js`. Replace that module's
local-storage implementation with Flask requests when the endpoint shapes and
authentication contract are ready.
