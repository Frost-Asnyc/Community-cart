import { useState } from "react";
import { Link } from "react-router-dom";
import {
  getCurrentUser,
  getDashboard,
  getFavoriteIds,
  getListings,
  toggleFavorite,
} from "../api/localLoopApi.js";

function formatPrice(amount) {
  return `$${Number(amount).toFixed(2)}`;
}

function formatDate(isoDate) {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(isoDate));
}

function offerStatusLabel(outcome) {
  if (outcome === "won") return "You won";
  if (outcome === "not-won") return "Not selected";
  return "Waiting for deadline";
}

function DashboardSection({ title, count, children, emptyText }) {
  return (
    <section className="dashboard-section">
      <div className="dashboard-section-heading">
        <h2>{title}</h2>
        <span>{count}</span>
      </div>
      {count ? children : <p className="dashboard-empty">{emptyText}</p>}
    </section>
  );
}

export default function Dashboard() {
  const [dashboard] = useState(() => getDashboard());
  const [favorites, setFavorites] = useState(() => {
    const favoriteIds = getFavoriteIds();
    return getListings().filter((listing) => favoriteIds.includes(listing.id));
  });
  const [error, setError] = useState("");

  function removeFavorite(listingId) {
    try {
      toggleFavorite(listingId);
      setFavorites((current) => current.filter((listing) => listing.id !== listingId));
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  const activeOffers = dashboard.offers.filter((offer) => offer.outcome === "pending");
  const completedOffers = dashboard.offers.filter((offer) => offer.outcome !== "pending");

  return (
    <div className="page-container dashboard-page">
      <div className="dashboard-hero">
        <div>
          <p className="eyebrow">Your LocalLoop</p>
          <h1>My dashboard</h1>
          <p>Hi, {getCurrentUser().name}. Keep track of your listings and private activity.</p>
        </div>
        <Link className="button button-dark" to="/list">
          <span aria-hidden="true">+</span> List an item
        </Link>
      </div>

      <div className="demo-banner">
        <span aria-hidden="true">ⓘ</span>
        <p>
          You’re using a local demo account. Switch identities from the header to
          try the buyer and seller flows; there is no authentication or email service yet.
        </p>
      </div>
      {error && <p className="form-feedback error-message" role="alert">{error}</p>}

      <div className="dashboard-grid">
        <DashboardSection
          title="My listings"
          count={dashboard.listings.length}
          emptyText="You haven’t listed anything yet."
        >
          <div className="dashboard-list">
            {dashboard.listings.map((listing) => {
              const ended =
                listing.status === "sold" || Date.parse(listing.deadline) <= Date.now();
              const winner = listing.offers[0];
              return (
                <article className="dashboard-listing" key={listing.id}>
                  <div className="dashboard-listing-main">
                    <span className="dashboard-artwork" aria-hidden="true">
                      {listing.artwork || "📦"}
                    </span>
                    <div>
                      <Link to={`/listings/${listing.id}`} className="dashboard-item-title">
                        {listing.title}
                      </Link>
                      <p>
                        {formatPrice(listing.price)} ·{" "}
                        {listing.status === "sold" ? "Sold" : ended ? "Offer period ended" : "Accepting offers"}
                      </p>
                    </div>
                  </div>
                  {ended && listing.offers.length > 0 ? (
                    <div className="winner-panel">
                      <strong>Highest offer: {formatPrice(winner.amount)}</strong>
                      <span>
                        {winner.buyerName} · placed {formatDate(winner.createdAt)}
                      </span>
                    </div>
                  ) : !ended ? (
                    <p className="sealed-note">Offers are sealed until {formatDate(listing.deadline)}.</p>
                  ) : (
                    <p className="sealed-note">No offers were placed before the deadline.</p>
                  )}
                  <Link className="text-link" to={`/listings/${listing.id}`}>
                    Manage listing →
                  </Link>
                </article>
              );
            })}
          </div>
        </DashboardSection>

        <DashboardSection
          title="My offers"
          count={dashboard.offers.length}
          emptyText="Offers you place will appear here."
        >
          <div className="dashboard-list">
            {activeOffers.map((offer) => (
              <article className="activity-row" key={offer.id}>
                <div>
                  <Link to={`/listings/${offer.listingId}`} className="dashboard-item-title">
                    {offer.listing?.title ?? "Listing unavailable"}
                  </Link>
                  <p>Your private offer: {formatPrice(offer.amount)}</p>
                </div>
                <span className="status-pill status-pending">{offerStatusLabel(offer.outcome)}</span>
              </article>
            ))}
            {completedOffers.map((offer) => (
              <article className="activity-row" key={offer.id}>
                <div>
                  <Link to={`/listings/${offer.listingId}`} className="dashboard-item-title">
                    {offer.listing?.title ?? "Listing unavailable"}
                  </Link>
                  <p>Your offer: {formatPrice(offer.amount)}</p>
                </div>
                <span
                  className={`status-pill ${offer.outcome === "won" ? "status-won" : "status-closed"}`}
                >
                  {offerStatusLabel(offer.outcome)}
                </span>
              </article>
            ))}
          </div>
        </DashboardSection>

        <DashboardSection
          title="Favorites"
          count={favorites.length}
          emptyText="Save a listing to come back to it later."
        >
          <div className="dashboard-list">
            {favorites.map((listing) => (
              <article className="activity-row" key={listing.id}>
                <Link to={`/listings/${listing.id}`} className="dashboard-item-title">
                  {listing.title}
                </Link>
                <button className="text-button" onClick={() => removeFavorite(listing.id)}>
                  Remove
                </button>
              </article>
            ))}
          </div>
        </DashboardSection>

        <DashboardSection
          title="Inquiries"
          count={dashboard.sentInquiries.length + dashboard.receivedInquiries.length}
          emptyText="Your private questions and seller replies will appear here."
        >
          <div className="dashboard-list">
            {dashboard.receivedInquiries.map((inquiry) => (
              <article className="inquiry-card" key={inquiry.id}>
                <p className="inquiry-direction">From {inquiry.buyerName}</p>
                <p>“{inquiry.message}”</p>
                <Link to={`/listings/${inquiry.listingId}`} className="text-link">
                  {inquiry.listingTitle}
                </Link>
              </article>
            ))}
            {dashboard.sentInquiries.map((inquiry) => (
              <article className="inquiry-card" key={inquiry.id}>
                <p className="inquiry-direction">Sent to {inquiry.sellerName}</p>
                <p>“{inquiry.message}”</p>
                <Link to={`/listings/${inquiry.listingId}`} className="text-link">
                  View listing
                </Link>
              </article>
            ))}
          </div>
        </DashboardSection>

        <DashboardSection
          title="Notifications"
          count={dashboard.notifications.length}
          emptyText="You’re all caught up."
        >
          <div className="dashboard-list">
            {dashboard.notifications.map((notification) => (
              <article className="notification-row" key={notification.id}>
                <span aria-hidden="true">✉</span>
                <p>{notification.message}</p>
              </article>
            ))}
            {dashboard.notifications.length > 0 && (
              <p className="demo-caption">Demo notification only. Outbid email is not connected.</p>
            )}
          </div>
        </DashboardSection>
      </div>
    </div>
  );
}
