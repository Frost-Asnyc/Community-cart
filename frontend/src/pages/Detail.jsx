import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import {
  getCurrentUser,
  getDashboard,
  getFavoriteIds,
  markListingSold,
  submitInquiry,
  submitOffer,
  toggleFavorite,
} from "../api/localLoopApi.js";
import {
  deleteListing as deleteApiListing,
  getListing as fetchListing,
} from "../api/fakeStoreApi.js";

function formatDeadline(deadline) {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(deadline));
}

export default function Detail() {
  const { listingId } = useParams();
  const navigate = useNavigate();
  const [listing, setListing] = useState(null);
  const [offer, setOffer] = useState({ amount: "", message: "" });
  const [inquiry, setInquiry] = useState("");
  const [feedback, setFeedback] = useState({ error: "", success: "" });
  const [loading, setLoading] = useState(true);
  const [isFavorite, setIsFavorite] = useState(false);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    let active = true;
    fetchListing(listingId)
      .then((item) => {
        if (!active) return;
        if (item && item.sellerId === getCurrentUser().id) {
          const ownedItem = getDashboard().listings.find((owned) => owned.id === listingId);
          setListing({ ...item, sellerOffers: ownedItem?.offers ?? [] });
        } else {
          setListing(item);
        }
        setIsFavorite(getFavoriteIds().includes(listingId));
      })
      .catch((requestError) => {
        if (active) setFeedback({ error: requestError.message, success: "" });
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [listingId]);

  if (loading) {
    return <div className="page-container status-message">Loading listing...</div>;
  }
  if (feedback.error && !listing) {
    return (
      <div className="page-container status-message error-message" role="alert">
        {feedback.error}
      </div>
    );
  }
  if (!listing) {
    return (
      <div className="page-container status-message">
        Listing not found. <Link to="/">Return to browse</Link>
      </div>
    );
  }

  const currentUser = getCurrentUser();
  const isOwner = listing.sellerId === currentUser.id;
  const isOpen = listing.status === "active" && Date.parse(listing.deadline) > Date.now();
  const closeMessage =
    listing.status === "sold" ? "This item has been marked sold." : "The offer deadline has passed.";

  function showError(error) {
    setFeedback({ error: error.message, success: "" });
  }

  function handleOfferSubmit(event) {
    event.preventDefault();
    try {
      submitOffer(listingId, offer.amount, offer.message);
      setOffer({ amount: "", message: "" });
      setFeedback({
        error: "",
        success: "Your sealed offer has been recorded. Other buyers can’t see it.",
      });
    } catch (requestError) {
      showError(requestError);
    }
  }

  function handleInquirySubmit(event) {
    event.preventDefault();
    try {
      submitInquiry(listingId, inquiry);
      setInquiry("");
      setFeedback({ error: "", success: "Your private inquiry was sent to the seller." });
    } catch (requestError) {
      showError(requestError);
    }
  }

  function handleFavoriteClick() {
    try {
      setIsFavorite(toggleFavorite(listingId));
      setFeedback({ error: "", success: "" });
    } catch (requestError) {
      showError(requestError);
    }
  }

  async function handleDelete() {
    if (!window.confirm("Delete this listing? This also removes its demo offers and inquiries.")) {
      return;
    }
    setDeleting(true);
    try {
      await deleteApiListing(listingId);
      navigate("/dashboard");
    } catch (requestError) {
      showError(requestError);
    } finally {
      setDeleting(false);
    }
  }

  function handleMarkSold() {
    try {
      setListing(markListingSold(listingId));
      setFeedback({ error: "", success: "Listing marked as sold." });
    } catch (requestError) {
      showError(requestError);
    }
  }

  return (
    <div className="page-container detail-page">
      <Link className="back-link" to="/">
        <span aria-hidden="true">←</span> Back to browse
      </Link>
      <section className="detail-layout">
        <div className="detail-image-wrap">
          {listing.image ? (
            <img src={listing.image} alt={listing.title} />
          ) : (
            <span className="detail-artwork" aria-hidden="true">{listing.artwork || "📦"}</span>
          )}
        </div>
        <div className="detail-content">
          <div className="detail-heading-row">
            <p className="eyebrow">{listing.category}</p>
            {!isOwner && (
              <button
                className={`favorite-button favorite-large${isFavorite ? " is-favorite" : ""}`}
                type="button"
                onClick={handleFavoriteClick}
                aria-label={isFavorite ? "Remove from favorites" : "Add to favorites"}
                aria-pressed={isFavorite}
              >
                {isFavorite ? "♥" : "♡"}
              </button>
            )}
          </div>
          <h1>{listing.title}</h1>
          <div className="detail-price">
            <span className="price-caption">Asking price</span> ${Number(listing.price).toFixed(2)}
          </div>
          <p className="seller-meta">
            Listed by {listing.sellerName} <span aria-hidden="true">·</span> {listing.location}
          </p>
          <p className="detail-description">{listing.description}</p>
          <div className={`deadline-panel${isOpen ? "" : " deadline-panel-closed"}`}>
            <span aria-hidden="true">{isOpen ? "◷" : "✓"}</span>
            <div>
              <strong>{isOpen ? "Private offers close" : "Offer period ended"}</strong>
              <span>{formatDeadline(listing.deadline)}</span>
            </div>
          </div>

          {feedback.error && <p className="form-feedback error-message" role="alert">{feedback.error}</p>}
          {feedback.success && <p className="form-feedback success-message" role="status">{feedback.success}</p>}

          {isOwner ? (
            <div className="owner-actions">
              <p className="demo-caption">This listing belongs to your selected demo account.</p>
              <div className="action-row">
                {listing.status === "active" && isOpen && (
                  <Link className="button button-outline" to={`/list/${listing.id}/edit`}>
                    Edit listing
                  </Link>
                )}
                {listing.status === "active" && (
                  <button className="button button-outline" type="button" onClick={handleDelete} disabled={deleting}>
                    {deleting ? "Deleting..." : "Delete"}
                  </button>
                )}
                {listing.status === "active" && !isOpen && listing.sellerOffers?.length > 0 && (
                  <button className="button button-dark" type="button" onClick={handleMarkSold}>
                    Mark as sold
                  </button>
                )}
              </div>
              {listing.status === "active" && isOpen && (
                <p className="demo-caption">You can mark this item sold after the offer deadline.</p>
              )}
              {listing.status === "active" && !isOpen && !listing.sellerOffers?.length && (
                <p className="demo-caption">No offers were made, so there is no winner to confirm.</p>
              )}
              <Link className="text-link" to="/dashboard">Manage listing and offers in your dashboard →</Link>
            </div>
          ) : isOpen ? (
            <>
              <form className="interaction-form" onSubmit={handleOfferSubmit}>
                <h2>Make a sealed offer</h2>
                <p>Only you and the seller will see your offer after the deadline.</p>
                <label>
                  Your offer
                  <span className="input-prefix">
                    <span aria-hidden="true">$</span>
                    <input
                      type="number"
                      min="0.01"
                      step="0.01"
                      required
                      value={offer.amount}
                      onChange={(event) => setOffer({ ...offer, amount: event.target.value })}
                      placeholder="0.00"
                    />
                  </span>
                </label>
                <label>
                  Note to seller <span className="optional-label">Optional</span>
                  <textarea
                    rows="2"
                    maxLength="300"
                    value={offer.message}
                    onChange={(event) => setOffer({ ...offer, message: event.target.value })}
                    placeholder="Add a short note..."
                  />
                </label>
                <button className="button button-dark detail-action" type="submit">
                  Submit private offer <span aria-hidden="true">↗</span>
                </button>
              </form>
              <form className="inquiry-form" onSubmit={handleInquirySubmit}>
                <label>
                  Have a question? Send the seller a private inquiry.
                  <textarea
                    rows="2"
                    maxLength="500"
                    required
                    value={inquiry}
                    onChange={(event) => setInquiry(event.target.value)}
                    placeholder="Ask a question about this item..."
                  />
                </label>
                <button className="text-button" type="submit">Send an inquiry</button>
              </form>
            </>
          ) : (
            <p className="closed-message">{closeMessage} Browse other items to find your next good thing.</p>
          )}
          <p className="detail-note">
            Demo mode: switch accounts in the header to try buyer and seller flows.
          </p>
        </div>
      </section>
    </div>
  );
}
