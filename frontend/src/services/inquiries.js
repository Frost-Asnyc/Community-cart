
/*
 * DEVELOPER: Mumo
 * RESPONSIBILITY: Inquiries API service.
 *
 * BACKEND ENDPOINTS:
 * POST /api/listings/:listing_id/inquiries
 * GET  /api/listings/:listing_id/inquiries
 * GET  /api/inquiries/sent
 *
 * TASKS:
 * - Implement sendInquiry(listingId, message).
 * - Implement getListingInquiries(listingId).
 * - Implement getSentInquiries().
 * - Handle API errors through the shared api.js.
 * - Preserve the backend response structure.
 *
 * RULES:
 * - All endpoints require authentication.
 * - Users cannot inquire about their own listings.
 * - Only listing owners can view inquiries on their listings.
 * - Do not implement a separate fetch configuration.
 */

import { get, post } from "./api";

const LISTINGS_ENDPOINT = "/api/listings";
const INQUIRIES_ENDPOINT = "/api/inquiries";

// Send an inquiry to a listing's seller.
export function sendInquiry(listingId, message) {
  return post(
    `${LISTINGS_ENDPOINT}/${encodeURIComponent(listingId)}/inquiries`,
    { message }
  );
}

// Retrieve inquiries received on your own listing.
export function getListingInquiries(listingId) {
  return get(
    `${LISTINGS_ENDPOINT}/${encodeURIComponent(listingId)}/inquiries`
  );
}

// Retrieve inquiries you have sent to other sellers.
export function getSentInquiries() {
  return get(`${INQUIRIES_ENDPOINT}/sent`);
}
