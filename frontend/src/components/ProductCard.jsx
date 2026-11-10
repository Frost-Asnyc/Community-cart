import { Link } from "react-router-dom";

function deadlineLabel(deadline) {
  const remaining = Date.parse(deadline) - Date.now();
  if (remaining <= 0) return "Offers closed";
  const hours = Math.ceil(remaining / (60 * 60 * 1000));
  if (hours < 24) return `${hours}h left`;
  const days = Math.ceil(hours / 24);
  return `${days} days left`;
}

export default function ProductCard({ product, favorite, onFavoriteToggle }) {
  const closed = product.status !== "active" || Date.parse(product.deadline) <= Date.now();

  return (
    <article className={`product-card${closed ? " product-card-closed" : ""}`}>
      <Link
        className="product-image-link"
        to={`/listings/${product.id}`}
        aria-label={`View ${product.title}`}
      >
        <div className="product-image-wrap">
          {product.image ? (
            <img src={product.image} alt="" loading="lazy" />
          ) : (
            <span className="product-artwork" aria-hidden="true">{product.artwork || "📦"}</span>
          )}
          {product.status !== "active" && <span className="listing-status-pill">Sold</span>}
        </div>
      </Link>
      <div className="product-card-content">
        <div className="card-meta">
          <p className="product-category">{product.category}</p>
          <button
            className={`favorite-button${favorite ? " is-favorite" : ""}`}
            type="button"
            onClick={() => onFavoriteToggle(product.id)}
            aria-label={favorite ? "Remove from favorites" : "Add to favorites"}
            aria-pressed={favorite}
          >
            {favorite ? "♥" : "♡"}
          </button>
        </div>
        <h2>
          <Link to={`/listings/${product.id}`}>{product.title}</Link>
        </h2>
        <div className="product-card-bottom">
          <span>
            <span className="price-caption">Asking</span>
            <span className="product-price">${Number(product.price).toFixed(2)}</span>
          </span>
          <span className={`deadline-chip${closed ? " deadline-closed" : ""}`}>
            {deadlineLabel(product.deadline)}
          </span>
        </div>
        <p className="product-location">{product.location}</p>
      </div>
    </article>
  );
}
