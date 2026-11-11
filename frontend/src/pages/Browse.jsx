import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { getFavoriteIds, toggleFavorite } from "../api/localLoopApi.js";
import { getListings as fetchListings } from "../api/fakeStoreApi.js";
import FilterBar from "../search/FilterBar.jsx";
import ProductCard from "../components/ProductCard.jsx";

export default function Browse() {
  const [listings, setListings] = useState([]);
  const [categories, setCategories] = useState([]);
  const [favorites, setFavorites] = useState(() => getFavoriteIds());
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    fetchListings()
      .then((items) => {
        if (!active) return;
        setListings(items);
        setCategories([...new Set(items.map((listing) => listing.category))].sort());
      })
      .catch((requestError) => {
        if (active) setError(requestError.message);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  const filteredListings = useMemo(() => {
    const query = search.trim().toLowerCase();
    return listings.filter((listing) => {
      const matchesCategory =
        selectedCategory === "all" || listing.category === selectedCategory;
      const matchesSearch =
        !query ||
        listing.title.toLowerCase().includes(query) ||
        listing.description.toLowerCase().includes(query) ||
        listing.category.toLowerCase().includes(query) ||
        listing.location.toLowerCase().includes(query);
      const matchesMin = minPrice === "" || listing.price >= Number(minPrice);
      const matchesMax = maxPrice === "" || listing.price <= Number(maxPrice);
      return matchesCategory && matchesSearch && matchesMin && matchesMax;
    });
  }, [listings, search, selectedCategory, minPrice, maxPrice]);
  const featuredListing = listings[0];

  function handleFavoriteToggle(listingId) {
    try {
      const isFavorite = toggleFavorite(listingId);
      setFavorites((current) =>
        isFavorite
          ? [...current, listingId]
          : current.filter((id) => id !== listingId),
      );
      setError("");
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  return (
    <div className="page-container browse-page">
      <section className="browse-hero">
        <div className="hero-copy-block">
          <p className="eyebrow"><span className="eyebrow-line" /> A better way to buy nearby</p>
          <h1>THE GOOD<br />FINDS YOU<br /><span>HAVEN’T</span><br />FOUND YET.</h1>
          <p className="hero-copy">
            One neighborhood. A thousand second chances. Find your next favorite
            thing and make a private offer before time runs out.
          </p>
          <a className="button button-dark hero-button" href="#community-finds">
            Explore local finds <span aria-hidden="true">↗</span>
          </a>
          <div className="hero-footnote">
            <span className="hero-footnote-dot" />
            A more thoughtful way to pass things on
          </div>
        </div>
        {featuredListing && (
          <Link
            className="hero-feature"
            to={`/listings/${featuredListing.id}`}
            aria-label={`Featured listing: ${featuredListing.title}`}
          >
            <div className="hero-feature-art">
              <span className="hero-feature-sun" />
              <span className="hero-feature-mountain mountain-back" />
              <span className="hero-feature-mountain mountain-front" />
              <span className="hero-feature-item" aria-hidden="true">
                {featuredListing.artwork || "📦"}
              </span>
              <span className="hero-feature-index">LOCAL FINDS <b>001—006</b></span>
              <span className="hero-feature-side-label">OBJECTS WITH A SECOND LIFE</span>
              <span className="hero-feature-scanline" />
            </div>
            <div className="hero-feature-caption">
              <span><small>FEATURED NEAR YOU</small><strong>{featuredListing.title}</strong></span>
              <span className="hero-feature-price">${Number(featuredListing.price).toFixed(0)} <b>↗</b></span>
            </div>
          </Link>
        )}
      </section>

      <section className="catalog-section" id="community-finds">
        <div className="section-heading">
          <div>
            <p className="eyebrow"><span className="eyebrow-line" /> From around the corner</p>
            <h2>THE COMMUNITY EDITION<span className="section-index"> / 01</span></h2>
          </div>
          <p className="result-count"><b>{String(filteredListings.length).padStart(2, "0")}</b> LISTINGS</p>
        </div>
        <FilterBar
          categories={categories}
          selectedCategory={selectedCategory}
          onCategoryChange={setSelectedCategory}
          search={search}
          onSearchChange={setSearch}
          minPrice={minPrice}
          maxPrice={maxPrice}
          onMinPriceChange={setMinPrice}
          onMaxPriceChange={setMaxPrice}
        />
        <p className="browse-account-note">
          OPEN TO EVERYONE <span>·</span> No account needed to browse
          <Link to="/dashboard">Your dashboard ↗</Link>
        </p>
        {error && <p className="form-feedback error-message" role="alert">{error}</p>}
        {loading && <p className="status-message">Loading community listings...</p>}
        {filteredListings.length === 0 && !loading && !error && (
          <div className="empty-state">
            <span aria-hidden="true">⌕</span>
            <h3>No listings found</h3>
            <p>Try changing your search or price range.</p>
          </div>
        )}
        {filteredListings.length > 0 && (
          <div className="product-grid">
            {filteredListings.map((listing) => (
              <ProductCard
                key={listing.id}
                product={listing}
                favorite={favorites.includes(listing.id)}
                onFavoriteToggle={handleFavoriteToggle}
              />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
