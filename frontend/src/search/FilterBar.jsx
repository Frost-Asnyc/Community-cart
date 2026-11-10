import CategoryFilter from "./CategoryFilter.jsx";
import SearchBar from "./SearchBar.jsx";

export default function FilterBar({
  categories,
  selectedCategory,
  onCategoryChange,
  search,
  onSearchChange,
  minPrice,
  maxPrice,
  onMinPriceChange,
  onMaxPriceChange,
}) {
  return (
    <div className="filter-bar">
      <SearchBar value={search} onChange={onSearchChange} />
      <CategoryFilter
        categories={categories}
        selected={selectedCategory}
        onChange={onCategoryChange}
      />
      <label className="price-filter">
        <span className="sr-only">Minimum price</span>
        <span aria-hidden="true">$</span>
        <input
          type="number"
          min="0"
          value={minPrice}
          onChange={(event) => onMinPriceChange(event.target.value)}
          placeholder="Min"
        />
      </label>
      <label className="price-filter">
        <span className="sr-only">Maximum price</span>
        <span aria-hidden="true">$</span>
        <input
          type="number"
          min="0"
          value={maxPrice}
          onChange={(event) => onMaxPriceChange(event.target.value)}
          placeholder="Max"
        />
      </label>
    </div>
  );
}
