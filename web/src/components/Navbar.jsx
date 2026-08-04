import React from 'react';
import { NavLink } from 'react-router-dom';
import { Brain, MessageSquare, Edit3, TrendingUp } from 'lucide-react';
import './Navbar.css';

const Navbar = () => {
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
        <NavLink to="/progress" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <TrendingUp size={18} />
          <span>Progress</span>
        </NavLink>
      </div>
    </nav>
  );
};

export default Navbar;
