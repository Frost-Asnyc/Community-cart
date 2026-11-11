import {
  cacheListings,
  deleteListing as removeCachedListing,
  getCurrentUser,
  getListings as getCachedListings,
  updateListing as updateCachedListing,
} from "./localLoopApi.js";

const PRODUCTS_URL = "https://fakestoreapi.com/products";
const OVERLAY_KEY = "localloop-fakestore-overlays-v1";
const DAY_IN_MS = 24 * 60 * 60 * 1000;

async function request(path = "", options = {}) {
  let response;
  try {
    response = await fetch(`${PRODUCTS_URL}${path}`, {
      ...options,
      headers: {
        ...(options.body ? { "Content-Type": "application/json" } : {}),
        ...options.headers,
      },
    });
  } catch (error) {
    throw new Error(`Could not reach the Fake Store API: ${error.message}`);
  }

  if (!response.ok) {
    throw new Error(`Fake Store API request failed (${response.status} ${response.statusText}).`);
  }
  if (response.status === 204) return null;

  const body = await response.text();
  if (!body) return null;
  try {
    return JSON.parse(body);
  } catch (error) {
    throw new Error(`Fake Store API returned invalid JSON: ${error.message}`);
  }
}

function readOverlays() {
  let saved;
  try {
    saved = window.localStorage.getItem(OVERLAY_KEY);
  } catch (error) {
    throw new Error(`Could not read Fake Store demo changes: ${error.message}`);
  }
  if (!saved) return { listings: [], deletedApiIds: [] };

  try {
    const parsed = JSON.parse(saved);
    if (!Array.isArray(parsed.listings) || !Array.isArray(parsed.deletedApiIds)) {
      throw new Error("Stored changes have an unexpected shape.");
    }
    return parsed;
  } catch (error) {
    throw new Error(`Could not read Fake Store demo changes: ${error.message}`);
  }
}

function writeOverlays(overlays) {
  try {
    window.localStorage.setItem(OVERLAY_KEY, JSON.stringify(overlays));
  } catch (error) {
    throw new Error(`Could not save Fake Store demo changes: ${error.message}`);
  }
}

function validateProduct(product) {
  const price = Number(product.price);
  if (!product.title?.trim() || !product.category || !product.description?.trim()) {
    throw new Error("Add an item name, category, and description.");
  }
  if (!Number.isFinite(price) || price < 0) {
    throw new Error("Enter a valid asking price.");
  }
  if (!Number.isFinite(Date.parse(product.deadline)) || Date.parse(product.deadline) <= Date.now()) {
    throw new Error("Choose a future offer deadline.");
  }
}

function productPayload(listing) {
  return {
    title: listing.title.trim(),
    price: Number(listing.price),
    description: listing.description.trim(),
    image: listing.image?.trim() || "",
    category: listing.category,
  };
}

function mapProduct(product, metadata = {}, cachedListings = getCachedListings()) {
  if (!product || product.id === undefined || !product.title || !product.category) {
    throw new Error("Fake Store API returned a product with an unexpected shape.");
  }
  const apiId = String(product.apiId ?? product.id);
  const cached = cachedListings.find((listing) => listing.id === String(product.id));
  const fallbackDeadline = new Date(Date.now() + 7 * DAY_IN_MS).toISOString();
  return {
    id: String(metadata.id ?? product.id),
    apiId,
    title: product.title,
    price: Number(product.price),
    description: product.description ?? "",
    category: product.category,
    image: product.image ?? "",
    sellerId: metadata.sellerId ?? cached?.sellerId ?? `fake-store-${apiId}`,
    sellerName: metadata.sellerName ?? cached?.sellerName ?? "Fake Store community member",
    location: metadata.location ?? cached?.location ?? "Community demo",
    deadline: metadata.deadline ?? cached?.deadline ?? fallbackDeadline,
    status: metadata.status ?? cached?.status ?? "active",
    createdAt: metadata.createdAt ?? cached?.createdAt ?? new Date().toISOString(),
    source: "fake-store",
  };
}

function saveOverlay(listing) {
  const overlays = readOverlays();
  const index = overlays.listings.findIndex((item) => item.id === listing.id);
  if (index < 0) {
    overlays.listings.unshift(listing);
  } else {
    overlays.listings[index] = listing;
  }
  overlays.deletedApiIds = overlays.deletedApiIds.filter((id) => id !== listing.apiId);
  writeOverlays(overlays);
}

function ensureListingCanBeManaged(listing) {
  if (!listing || listing.sellerId !== getCurrentUser().id) {
    throw new Error("You can only manage listings you created.");
  }
  if (listing.status !== "active" || Date.parse(listing.deadline) <= Date.now()) {
    throw new Error("This listing can no longer be changed after its offer deadline.");
  }
}

export async function getListings() {
  const products = await request("?limit=20");
  if (!Array.isArray(products)) {
    throw new Error("Fake Store API returned an unexpected product list.");
  }

  const overlays = readOverlays();
  const cachedListings = getCachedListings();
  const legacyListings = cachedListings.filter((listing) => listing.source !== "fake-store");
  const cachedById = new Map(cachedListings.map((listing) => [listing.id, listing]));
  const hiddenApiIds = new Set(overlays.deletedApiIds);
  const overlaidApiIds = new Set(overlays.listings.map((listing) => listing.apiId));
  const productsById = products
    .filter((product) => !hiddenApiIds.has(String(product.id)) && !overlaidApiIds.has(String(product.id)))
    .map((product) => mapProduct(product, {}, cachedListings));
  const overlayListings = overlays.listings.map((listing) => ({
    ...listing,
    status: cachedById.get(listing.id)?.status ?? listing.status,
  }));
  const listings = [...overlayListings, ...productsById, ...legacyListings];
  cacheListings(listings);
  return listings;
}

export async function getListing(listingId) {
  const cached = getCachedListings().find((listing) => listing.id === listingId);
  if (cached && cached.source !== "fake-store") return cached;

  const overlays = readOverlays();
  const overlay = overlays.listings.find((listing) => listing.id === listingId);
  if (overlay) {
    return {
      ...overlay,
      status: cached?.status ?? overlay.status,
    };
  }
  if (overlays.deletedApiIds.includes(String(listingId))) return null;

  const product = await request(`/${encodeURIComponent(listingId)}`);
  if (!product) return null;
  const listing = mapProduct(product);
  cacheListings([listing]);
  return listing;
}

export async function createListing(listing) {
  validateProduct(listing);
  const user = getCurrentUser();
  const payload = productPayload(listing);
  const product = await request("", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  if (!product || product.id === undefined) {
    throw new Error("Fake Store API did not return the created product.");
  }

  const created = mapProduct(
    { ...payload, ...product, apiId: product.id },
    {
      id: `local-${crypto.randomUUID()}`,
      sellerId: user.id,
      sellerName: user.name,
      location: listing.location?.trim() || "Your neighborhood",
      deadline: listing.deadline,
      createdAt: new Date().toISOString(),
    },
  );
  saveOverlay(created);
  cacheListings([created]);
  return created;
}

export async function updateListing(listingId, listing) {
  validateProduct(listing);
  const existing = await getListing(listingId);
  ensureListingCanBeManaged(existing);

  if (existing.source !== "fake-store") {
    return updateCachedListing(listingId, listing);
  }

  const payload = productPayload(listing);
  const product = await request(`/${encodeURIComponent(existing.apiId)}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
  if (!product || product.id === undefined) {
    throw new Error("Fake Store API did not return the updated product.");
  }

  const updated = mapProduct(
    { ...payload, ...product, apiId: existing.apiId },
    {
      ...existing,
      id: existing.id,
      apiId: existing.apiId,
      deadline: listing.deadline,
      location: listing.location?.trim() || "Your neighborhood",
    },
  );
  saveOverlay(updated);
  cacheListings([updated]);
  return updated;
}

export async function deleteListing(listingId) {
  const existing = await getListing(listingId);
  ensureListingCanBeManaged(existing);
  if (existing.source !== "fake-store") {
    removeCachedListing(existing.id);
    return;
  }

  await request(`/${encodeURIComponent(existing.apiId)}`, { method: "DELETE" });

  const overlays = readOverlays();
  overlays.listings = overlays.listings.filter((listing) => listing.id !== existing.id);
  if (!overlays.deletedApiIds.includes(existing.apiId)) {
    overlays.deletedApiIds.push(existing.apiId);
  }
  writeOverlays(overlays);
  removeCachedListing(existing.id);
}
