import { NavLink } from "react-router-dom";
import { DEMO_USERS, getCurrentUser, setCurrentUser } from "../api/localLoopApi.js";

export default function Header() {
  const currentUser = getCurrentUser();

  function changeDemoUser(event) {
    try {
      setCurrentUser(event.target.value);
      window.location.reload();
    } catch (error) {
      window.alert(error.message);
    }
  }

  return (
    <header className="site-header">
      <div className="header-inner">
        <NavLink className="brand" to="/" aria-label="LocalLoop home">
          <span className="brand-mark" aria-hidden="true">↗</span>
          <span>LocalLoop</span>
        </NavLink>
        <nav className="main-nav" aria-label="Main navigation">
          <NavLink to="/browse">Browse</NavLink>
          <NavLink to="/dashboard">Dashboard</NavLink>
          <label className="demo-user-picker">
            <span className="sr-only">Demo account</span>
            <select value={currentUser.id} onChange={changeDemoUser}>
              {DEMO_USERS.map((user) => (
                <option key={user.id} value={user.id}>{user.name}</option>
              ))}
            </select>
          </label>
          <NavLink className="nav-cta" to="/list">
            <span aria-hidden="true">+</span> List an item
          </NavLink>
        </nav>
      </div>
    </header>
  );
}
