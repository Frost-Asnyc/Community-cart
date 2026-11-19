
/*
 * DEVELOPER: Mumo
 * RESPONSIBILITY: Offers API service.
 *
 * BACKEND ENDPOINTS:
 * POST /api/listings/:listing_id/offers
 * GET  /api/listings/:listing_id/offers
 * GET  /api/listings/:listing_id/offers/mine
 * POST /api/listings/:listing_id/offers/close
 *
 * TASKS:
 * - Implement submitOffer(listingId, amount, message).
 * - Implement getListingOffers(listingId).
 * - Implement getMyOffer(listingId).
 * - Implement closeListingAuction(listingId).
 * - Handle API errors through the shared api.js.
 * - Preserve the backend response structure.
 *
 * RULES:
 * - All endpoints require authentication.
 * - Offer amounts must be greater than zero.
 * - Only listing owners can view all offers or close auctions.
 * - Do not implement a separate fetch configuration.
 */

import { get, post } from "./api";

const LISTINGS_ENDPOINT = "/api/listings";

// Submit an offer on a listing.
export function submitOffer(listingId, amount, message) {
  const offerData = { amount };

  if (message !== undefined && message !== null && message !== "") {
    offerData.message = message;
  }

  return post(
    `${LISTINGS_ENDPOINT}/${encodeURIComponent(listingId)}/offers`,
    offerData
  );
}

// Retrieve all offers on your own listing.
export function getListingOffers(listingId) {
  return get(
    `${LISTINGS_ENDPOINT}/${encodeURIComponent(listingId)}/offers`
  );
}

// Retrieve your own offer on a listing.
export function getMyOffer(listingId) {
  return get(
    `${LISTINGS_ENDPOINT}/${encodeURIComponent(listingId)}/offers/mine`
  );
}

// Close an auction and finalise its winner.
export function closeListingAuction(listingId) {
  return post(
    `${LISTINGS_ENDPOINT}/${encodeURIComponent(listingId)}/offers/close`
  );
}
