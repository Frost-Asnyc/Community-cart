import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import {
  createListing,
  getCategories,
  getCurrentUser,
  getListing,
  updateListing,
} from "../api/localLoopApi.js";

const emptyForm = {
  title: "",
  price: "",
  category: "",
  description: "",
  image: "",
  location: "",
  deadline: "",
};

function toLocalDateTime(isoDate) {
  const date = new Date(isoDate);
  const local = new Date(date.getTime() - date.getTimezoneOffset() * 60_000);
  return local.toISOString().slice(0, 16);
}

function getMinimumDeadline() {
  const now = new Date();
  now.setMinutes(now.getMinutes() + 5);
  return toLocalDateTime(now.toISOString());
}

export default function ListingForm() {
  const { listingId } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState(emptyForm);
  const [categories] = useState(() => getCategories());
  const [minimumDeadline] = useState(getMinimumDeadline);
  const [loading, setLoading] = useState(Boolean(listingId));
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!listingId) return;
    try {
      const listing = getListing(listingId);
      if (!listing) {
        setError("Listing not found.");
      } else if (listing.sellerId !== getCurrentUser().id) {
        setError("You can only edit listings owned by the selected demo account.");
      } else if (listing.status !== "active" || Date.parse(listing.deadline) <= Date.now()) {
        setError("Only listings before their offer deadline can be edited.");
      } else {
        setForm({
          title: listing.title,
          price: String(listing.price),
          category: listing.category,
          description: listing.description,
          image: listing.image || "",
          location: listing.location || "",
          deadline: toLocalDateTime(listing.deadline),
        });
      }
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }, [listingId]);

  function updateField(event) {
    setForm((current) => ({ ...current, [event.target.name]: event.target.value }));
  }

  function handleSubmit(event) {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      const listingData = {
        ...form,
        deadline: new Date(form.deadline).toISOString(),
        image: form.image.trim(),
      };
      const saved = listingId
        ? updateListing(listingId, listingData)
        : createListing(listingData);
      navigate(`/listings/${saved.id}`);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return <div className="page-container status-message">Loading listing...</div>;
  }

  return (
    <div className="page-container form-page">
      <Link className="back-link" to="/dashboard">
        <span aria-hidden="true">←</span> Back to dashboard
      </Link>
      <div className="form-layout">
        <div className="form-intro">
          <p className="eyebrow">Pass something good along</p>
          <h1>{listingId ? "Edit listing" : "List an item"}</h1>
          <p>
            Set a clear asking price and a deadline. Buyers can send one private,
            sealed offer before the deadline.
          </p>
          <div className="form-note">
            <span aria-hidden="true">✳</span>
            <p>At the deadline, the highest offer wins. The earliest offer wins a tie.</p>
          </div>
        </div>
        <form className="listing-form" onSubmit={handleSubmit}>
          <label>
            Item name
            <input
              name="title"
              value={form.title}
              onChange={updateField}
              placeholder="e.g. A well-loved bookcase"
              required
              maxLength={120}
            />
          </label>
          <div className="form-row">
            <label>
              Asking price
              <span className="input-prefix">
                <span aria-hidden="true">$</span>
                <input
                  type="number"
                  name="price"
                  value={form.price}
                  onChange={updateField}
                  placeholder="0.00"
                  min="0"
                  step="0.01"
                  required
                />
              </span>
            </label>
            <label>
              Category
              <select name="category" value={form.category} onChange={updateField} required>
                <option value="" disabled>Choose a category</option>
                {categories.map((category) => (
                  <option value={category} key={category}>{category}</option>
                ))}
                {!categories.includes(form.category) && form.category && (
                  <option value={form.category}>{form.category}</option>
                )}
              </select>
            </label>
          </div>
          <label>
            Description
            <textarea
              name="description"
              value={form.description}
              onChange={updateField}
              placeholder="Describe the condition and anything a buyer should know..."
              rows="5"
              required
              maxLength={1000}
            />
          </label>
          <div className="form-row">
            <label>
              Offer deadline
              <input
                type="datetime-local"
                name="deadline"
                value={form.deadline}
                onChange={updateField}
                min={minimumDeadline}
                required
              />
            </label>
            <label>
              Neighborhood
              <input
                name="location"
                value={form.location}
                onChange={updateField}
                placeholder="e.g. Riverside"
                maxLength={60}
              />
            </label>
          </div>
          <label>
            Image URL <span className="optional-label">Optional</span>
            <input
              type="url"
              name="image"
              value={form.image}
              onChange={updateField}
              placeholder="https://..."
            />
          </label>
          {error && <p className="form-feedback error-message" role="alert">{error}</p>}
          <button className="button button-dark submit-button" type="submit" disabled={submitting}>
            {submitting ? "Saving listing..." : listingId ? "Save changes" : "Publish listing"}
            {!submitting && <span aria-hidden="true">↗</span>}
          </button>
          <p className="demo-caption">
            Demo mode: listings are saved only in this browser.
          </p>
        </form>
      </div>
    </div>
  );
}
