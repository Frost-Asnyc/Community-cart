const STORAGE_KEY = "localloop-demo-v1";
const USER_KEY = "localloop-demo-user";

export const DEMO_USERS = [
  { id: "demo-user", name: "Sean Diddy Holmes" },
  { id: "neighbor-1", name: "R.K Jelly" },
  { id: "neighbor-2", name: "Sam T." },
  { id: "neighbor-3", name: "Elite Epstine." },
];

export function getCurrentUser() {
  const selectedId = window.localStorage.getItem(USER_KEY);
  return DEMO_USERS.find((user) => user.id === selectedId) ?? DEMO_USERS[0];
}

export function setCurrentUser(userId) {
  if (!DEMO_USERS.some((user) => user.id === userId)) {
    throw new Error("Choose one of the available demo accounts.");
  }
  window.localStorage.setItem(USER_KEY, userId);
}

function daysFromNow(days) {
  return new Date(Date.now() + days * 24 * 60 * 60 * 1000).toISOString();
}

function initialState() {
  return {
    listings: [
      {
        id: "listing-bike",
        title: "City bike, ready for a new ride",
        description:
          "A sturdy 7-speed city bike in good working order. Recently tuned, with a front basket and lights included. Some cosmetic wear on the frame.",
        price: 85,
        category: "Sports & outdoors",
        image: "",
        artwork: "🚲",
        sellerId: "neighbor-1",
        sellerName: "R.K Jelly",
        location: "Northside",
        deadline: daysFromNow(3),
        status: "active",
        createdAt: new Date().toISOString(),
      },
      {
        id: "listing-chair",
        title: "Mid-century reading chair",
        description:
          "Comfortable vintage chair with a solid wood frame. The cushion cover has been freshly cleaned. Pickup near the library.",
        price: 60,
        category: "Home",
        image: "",
        artwork: "🪑",
        sellerId: "neighbor-2",
        sellerName: "Sam T.",
        location: "Old Town",
        deadline: daysFromNow(2),
        status: "active",
        createdAt: new Date().toISOString(),
      },
      {
        id: "listing-books",
        title: "A stack of much-loved cookbooks",
        description:
          "Eight lovely familily firendly cookbooks covering weeknight dinners, baking, and vegetarian meals. A few notes in the margins, lots of good recipes.",
        price: 18,
        category: "Books",
        image: "",
        artwork: "📚",
        sellerId: "neighbor-3",
        sellerName: "Elite Epstine.",
        location: "Riverside",
        deadline: daysFromNow(5),
        status: "active",
        createdAt: new Date().toISOString(),
      },
      {
        id: "listing-lamp",
        title: "Warm light, little desk lamp",
        description:
          "Small brass-finish lamp with a new LED bulb. Works perfectly and is just right for a reading nook or bedside table.",
        price: 12,
        category: "Home",
        image: "",
        artwork: "💡",
        sellerId: "neighbor-4",
        sellerName: "Morgan L.",
        location: "East Market",
        deadline: daysFromNow(4),
        status: "active",
        createdAt: new Date().toISOString(),
      },
      {
        id: "listing-coat",
        title: "Rain jacket for spring walks",
        description:
          "Lightweight, waterproof jacket in excellent condition. Size medium. I have outgrown it and hope someone else can put it to use.",
        price: 25,
        category: "Clothing",
        image: "",
        artwork: "🧥",
        sellerId: "neighbor-5",
        sellerName: "Casey P.",
        location: "Northside",
        deadline: daysFromNow(6),
        status: "active",
        createdAt: new Date().toISOString(),
      },
      {
        id: "listing-toys",
        title: "Wooden blocks and train set",
        description:
          "A box of wooden blocks and a small train set. All pieces are here, with normal signs of play. Great for a starter toy shelf.",
        price: 22,
        category: "Kids",
        image: "",
        artwork: "🧸",
        sellerId: "neighbor-6",
        sellerName: "Jordan W.",
        location: "West End",
        deadline: daysFromNow(7),
        status: "active",
        createdAt: new Date().toISOString(),
      },
    ],
    offers: [],
    inquiries: [],
    favoriteIds: [],
  };
}

function readState() {
  const saved = window.localStorage.getItem(STORAGE_KEY);
  if (!saved) {
    const state = initialState();
    writeState(state);
    return state;
  }

  try {
    const parsed = JSON.parse(saved);
    if (
      !Array.isArray(parsed.listings) ||
      !Array.isArray(parsed.offers) ||
      !Array.isArray(parsed.inquiries) ||
      !Array.isArray(parsed.favoriteIds)
    ) {
      throw new Error("Stored demo data has an unexpected shape.");
    }
    return parsed;
  } catch (error) {
    throw new Error(`Could not read LocalLoop demo data: ${error.message}`);
  }
}

function writeState(state) {
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (error) {
    throw new Error(`Could not save LocalLoop demo data: ${error.message}`);
  }
}

function validateListing(listing) {
  const price = Number(listing.price);
  const deadline = Date.parse(listing.deadline);
  if (!listing.title.trim() || !listing.category || !listing.description.trim()) {
    throw new Error("Add an item name, category, and description.");
  }
  if (!Number.isFinite(price) || price < 0) {
    throw new Error("Enter a valid asking price.");
  }
  if (!Number.isFinite(deadline) || deadline <= Date.now()) {
    throw new Error("Choose a future offer deadline.");
  }
}

function ensureListingCanReceiveOffers(listing) {
  if (!listing || listing.status !== "active" || Date.parse(listing.deadline) <= Date.now()) {
    throw new Error("This listing is no longer accepting offers.");
  }
  if (listing.sellerId === getCurrentUser().id) {
    throw new Error("You can’t make an offer on your own listing.");
  }
}

export function getListings() {
  return readState().listings;
}

export function cacheListings(listings) {
  const state = readState();
  for (const listing of listings) {
    const index = state.listings.findIndex((item) => item.id === listing.id);
    if (index < 0) {
      state.listings.push(listing);
      continue;
    }
    const existing = state.listings[index];
    state.listings[index] = {
      ...existing,
      ...listing,
      sellerId: existing.sellerId ?? listing.sellerId,
      sellerName: existing.sellerName ?? listing.sellerName,
      location: existing.location ?? listing.location,
      deadline: existing.deadline ?? listing.deadline,
      status: existing.status ?? listing.status,
      createdAt: existing.createdAt ?? listing.createdAt,
    };
  }
  writeState(state);
}

export function getCategories() {
  return [...new Set(getListings().map((listing) => listing.category))].sort();
}

export function getListing(listingId) {
  return readState().listings.find((listing) => listing.id === listingId) ?? null;
}

export function createListing(listing) {
  validateListing(listing);
  const state = readState();
  const created = {
    ...listing,
    id: `listing-${crypto.randomUUID()}`,
    price: Number(listing.price),
    sellerId: getCurrentUser().id,
    sellerName: getCurrentUser().name,
    location: listing.location || "Your neighborhood",
    status: "active",
    createdAt: new Date().toISOString(),
  };
  state.listings.unshift(created);
  writeState(state);
  return created;
}

export function updateListing(listingId, listing) {
  validateListing(listing);
  const state = readState();
  const index = state.listings.findIndex((item) => item.id === listingId);
  if (index < 0 || state.listings[index].sellerId !== getCurrentUser().id) {
    throw new Error("You can only edit listings you created.");
  }
  if (
    state.listings[index].status !== "active" ||
    Date.parse(state.listings[index].deadline) <= Date.now()
  ) {
    throw new Error("This listing can no longer be edited after its offer deadline.");
  }
  state.listings[index] = {
    ...state.listings[index],
    ...listing,
    price: Number(listing.price),
  };
  writeState(state);
  return state.listings[index];
}

export function deleteListing(listingId) {
  const state = readState();
  const listing = state.listings.find((item) => item.id === listingId);
  if (!listing || listing.sellerId !== getCurrentUser().id) {
    throw new Error("You can only delete listings you created.");
  }
  state.listings = state.listings.filter((item) => item.id !== listingId);
  state.offers = state.offers.filter((offer) => offer.listingId !== listingId);
  state.inquiries = state.inquiries.filter((inquiry) => inquiry.listingId !== listingId);
  state.favoriteIds = state.favoriteIds.filter((id) => id !== listingId);
  writeState(state);
}

export function markListingSold(listingId) {
  const state = readState();
  const listing = state.listings.find((item) => item.id === listingId);
  if (!listing || listing.sellerId !== getCurrentUser().id) {
    throw new Error("You can only update listings you created.");
  }
  if (listing.status !== "active" || Date.parse(listing.deadline) > Date.now()) {
    throw new Error("A listing can be marked sold after its offer deadline.");
  }
  listing.status = "sold";
  writeState(state);
  return listing;
}

export function toggleFavorite(listingId) {
  const state = readState();
  if (!state.listings.some((listing) => listing.id === listingId)) {
    throw new Error("This listing is no longer available.");
  }
  const favorite = state.favoriteIds.includes(listingId);
  state.favoriteIds = favorite
    ? state.favoriteIds.filter((id) => id !== listingId)
    : [...state.favoriteIds, listingId];
  writeState(state);
  return !favorite;
}

export function getFavoriteIds() {
  return readState().favoriteIds;
}

export function submitOffer(listingId, amount, message = "") {
  const state = readState();
  const listing = state.listings.find((item) => item.id === listingId);
  ensureListingCanReceiveOffers(listing);
  if (!Number.isFinite(Number(amount)) || Number(amount) <= 0) {
    throw new Error("Enter an offer greater than $0.");
  }
  if (
    state.offers.some(
      (offer) => offer.listingId === listingId && offer.buyerId === getCurrentUser().id,
    )
  ) {
    throw new Error("You’ve already placed a sealed offer on this listing.");
  }
  state.offers.push({
    id: `offer-${crypto.randomUUID()}`,
    listingId,
    buyerId: getCurrentUser().id,
    buyerName: getCurrentUser().name,
    amount: Number(amount),
    message: message.trim(),
    createdAt: new Date().toISOString(),
  });
  writeState(state);
}

export function submitInquiry(listingId, message) {
  const state = readState();
  const listing = state.listings.find((item) => item.id === listingId);
  if (
    !listing ||
    listing.status !== "active" ||
    Date.parse(listing.deadline) <= Date.now()
  ) {
    throw new Error("This listing is no longer available for inquiries.");
  }
  if (listing.sellerId === getCurrentUser().id) {
    throw new Error("You can’t send an inquiry to yourself.");
  }
  const trimmedMessage = message.trim();
  if (!trimmedMessage) {
    throw new Error("Write a question before sending your inquiry.");
  }
  state.inquiries.push({
    id: `inquiry-${crypto.randomUUID()}`,
    listingId,
    buyerId: getCurrentUser().id,
    buyerName: getCurrentUser().name,
    sellerId: listing.sellerId,
    sellerName: listing.sellerName,
    listingTitle: listing.title,
    message: trimmedMessage,
    createdAt: new Date().toISOString(),
  });
  writeState(state);
}

function findOfferWinner(offers) {
  return [...offers].sort(
    (first, second) =>
      second.amount - first.amount ||
      Date.parse(first.createdAt) - Date.parse(second.createdAt),
  )[0];
}

export function getDashboard() {
  const state = readState();
  const currentUser = getCurrentUser();
  const ownOffers = state.offers.filter((offer) => offer.buyerId === currentUser.id);
  const offerHistory = ownOffers.map((offer) => {
    const listing = state.listings.find((item) => item.id === offer.listingId);
    const ended = listing?.status === "sold" || Date.parse(listing?.deadline ?? "") <= Date.now();
    const winner = findOfferWinner(
      state.offers.filter((item) => item.listingId === offer.listingId),
    );
    return {
      ...offer,
      listing,
      outcome: !ended ? "pending" : winner?.id === offer.id ? "won" : "not-won",
    };
  });
  const offerNotifications = offerHistory
    .filter((offer) => offer.outcome === "not-won")
    .map((offer) => ({
      id: `notice-${offer.id}`,
      message: `Your offer on “${offer.listing?.title ?? "a listing"}” didn’t win. You can try another listing.`,
      createdAt: offer.listing?.deadline ?? offer.createdAt,
    }));

  return {
    listings: state.listings
      .filter((listing) => listing.sellerId === currentUser.id)
      .map((listing) => {
        const offers = state.offers
          .filter((offer) => offer.listingId === listing.id)
          .sort(
            (first, second) =>
              second.amount - first.amount ||
              Date.parse(first.createdAt) - Date.parse(second.createdAt),
          );
        const offerPeriodEnded =
          listing.status === "sold" || Date.parse(listing.deadline) <= Date.now();
        return {
          ...listing,
          offers: offerPeriodEnded ? offers : [],
          offerCount: offers.length,
        };
      }),
    offers: offerHistory,
    sentInquiries: state.inquiries.filter((inquiry) => inquiry.buyerId === currentUser.id),
    receivedInquiries: state.inquiries.filter((inquiry) => inquiry.sellerId === currentUser.id),
    notifications: offerNotifications,
  };
}
