export default function CategoryFilter({
  categories,
  selected,
  onChange,
}) {
  return (
    <label className="category-select">
      <span className="sr-only">Filter by category</span>
      <select value={selected} onChange={(event) => onChange(event.target.value)}>
        <option value="all">All categories</option>
        {categories.map((category) => (
          <option value={category} key={category}>
            {category}
          </option>
        ))}
      </select>
      <span className="select-chevron" aria-hidden="true">
        ▾
      </span>
    </label>
  );
}
