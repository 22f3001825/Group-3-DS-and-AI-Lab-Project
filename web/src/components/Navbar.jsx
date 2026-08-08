import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  Brain, MessageSquare, Edit3, TrendingUp, Layers, Settings, ShieldCheck, LogOut, User,
} from 'lucide-react';
import { useAuth } from '../auth/auth-context';
import './Navbar.css';

const Navbar = () => {
  // Identity is context now, not a localStorage re-read on every navigation: the old
  // getAdminToken() poll existed only because signing in happened on the Admin page and
  // localStorage fires no event in the tab that wrote it.
  const { isAuthenticated, isAdmin, student, signOut } = useAuth();

  // The login page is its own thing — no navigation to offer until there is a session.
  if (!isAuthenticated) return null;

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
        <NavLink to="/settings" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <Settings size={18} />
          <span>Settings</span>
        </NavLink>
        {/* Gated on the server's answer (`Student.is_admin`), not on anything stored
            locally — so the link disappears on the next request after a demotion. */}
        {isAdmin && (
          <NavLink to="/admin" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            <ShieldCheck size={18} />
            <span>Admin</span>
          </NavLink>
        )}
      </div>

      <div className="nav-account">
        <NavLink to="/settings" className="nav-avatar-link" title={student?.email || ''}>
          {student?.picture_url ? (
            <img
              className="nav-avatar"
              src={student.picture_url}
              alt=""
              referrerPolicy="no-referrer"
            />
          ) : (
            <span className="nav-avatar nav-avatar-fallback"><User size={15} /></span>
          )}
          <span className="nav-account-name">{student?.name || 'Account'}</span>
        </NavLink>
        <button className="nav-signout" onClick={signOut} title="Sign out">
          <LogOut size={16} />
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
