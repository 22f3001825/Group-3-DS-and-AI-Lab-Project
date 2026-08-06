import React, { useEffect, useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { Brain, MessageSquare, Edit3, TrendingUp, Layers, ShieldCheck } from 'lucide-react';
import { getAdminToken } from '../api/client';
import './Navbar.css';

const Navbar = () => {
  // The /admin link renders only when a token is stored, so ordinary students never see
  // it. Re-checked on navigation because signing in or out happens on the Admin page
  // itself and localStorage does not fire an event for the tab that wrote it.
  const location = useLocation();
  const [isAdmin, setIsAdmin] = useState(Boolean(getAdminToken()));

  useEffect(() => { setIsAdmin(Boolean(getAdminToken())); }, [location]);

  return (
    <nav className="navbar glass-panel">
      <div className="nav-brand">
        <Brain className="brand-icon" size={24} color="var(--accent)" />
        <span className="brand-name">MLT Assistant</span>
      </div>
      <div className="nav-links">
        <NavLink to="/" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <MessageSquare size={18} />
          <span>Chat</span>
        </NavLink>
        <NavLink to="/quiz" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <Edit3 size={18} />
          <span>Quiz</span>
        </NavLink>
        <NavLink to="/doubts" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <Layers size={18} />
          <span>Doubts</span>
        </NavLink>
        <NavLink to="/progress" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <TrendingUp size={18} />
          <span>Progress</span>
        </NavLink>
        {isAdmin && (
          <NavLink to="/admin" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            <ShieldCheck size={18} />
            <span>Admin</span>
          </NavLink>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
