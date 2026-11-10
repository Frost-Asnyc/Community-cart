export default function SearchBar({ value, onChange }) {
  return (
    <label className="search-field">
      <span className="search-icon" aria-hidden="true">
        ⌕
      </span>
      <span className="sr-only">Search items</span>
      <input
        type="search"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder="Search for something you need..."
      />
      {value && (
        <button
          className="clear-search"
          type="button"
          onClick={() => onChange("")}
          aria-label="Clear search"
        >
          ×
        </button>
      )}
    </label>
  );
}
