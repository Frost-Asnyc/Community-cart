import { ArrowUpRight, ImageOff, Star } from "lucide-react";

function formatPrice(price) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 2,
  }).format(price);
}

export default function UndergroundProductCard({ product, onSelect }) {
  return (
    <article className="underground-product-card">
      <button
        className="underground-product-image"
        type="button"
        onClick={() => onSelect(product)}
        aria-label={`View ${product.name}`}
      >
        {product.image ? (
          <img
            src={product.image}
            alt=""
            loading="lazy"
            onError={(event) => {
              event.currentTarget.hidden = true;
              event.currentTarget.nextElementSibling.hidden = false;
            }}
          />
        ) : null}
        <span
          className="underground-image-fallback"
          hidden={Boolean(product.image)}
          aria-hidden="true"
        >
          <ImageOff size={25} />
          <span>NO SIGNAL</span>
        </span>
        <span className="underground-product-index" aria-hidden="true">
          CC / UG
        </span>
        <span
          className={
            product.availability
              ? "underground-stock-tag"
              : "underground-stock-tag is-unavailable"
          }
        >
          {product.availability ? "AVAILABLE" : "DEMO ONLY"}
        </span>
      </button>

      <div className="underground-product-info">
        <div className="underground-product-meta">
          <span>{product.category}</span>
          {product.average_rating > 0 && (
            <span className="underground-rating">
              <Star size={13} fill="currentColor" aria-hidden="true" />
              {product.average_rating.toFixed(1)}
            </span>
          )}
        </div>
        <button
          className="underground-product-title"
          type="button"
          onClick={() => onSelect(product)}
        >
          {product.name} <ArrowUpRight size={16} aria-hidden="true" />
        </button>
        <div className="underground-product-bottom">
          <span className="underground-product-price">
            {formatPrice(product.price)}
          </span>
          <button
            className="underground-view-button"
            type="button"
            onClick={() => onSelect(product)}
            aria-label={`See details for ${product.name}`}
          >
            View find
          </button>
        </div>
      </div>
    </article>
  );
}
