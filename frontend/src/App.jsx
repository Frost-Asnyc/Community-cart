import { Route, Routes } from "react-router-dom";
import Header from "./components/Header.jsx";
import Browse from "./pages/Browse.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Detail from "./pages/Detail.jsx";
import ListingForm from "./pages/ListingForm.jsx";

export default function App() {
  return (
    <div className="app-shell">
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<Browse />} />
          <Route path="/browse" element={<Browse />} />
          <Route path="/listings/:listingId" element={<Detail />} />
          <Route path="/list" element={<ListingForm />} />
          <Route path="/list/:listingId/edit" element={<ListingForm />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="*" element={<Browse />} />
        </Routes>
      </main>
      <footer className="site-footer">
        <span>Community-Cart</span>
        <span>Good things, shared close to home.</span>
      </footer>
    </div>
  );
}
