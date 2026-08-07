import React from 'react';
import { Moon, Sun, Palette, Info, User, LogOut, ShieldCheck } from 'lucide-react';
import { useTheme } from '../theme/theme-context';
import { useAuth } from '../auth/auth-context';
import './Settings.css';

/** Dates arrive as ISO strings from FastAPI; a missing one is normal (a row that has
 *  never been signed into), so it renders as an em dash rather than "Invalid Date". */
function formatDate(value) {
  if (!value) return '—';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '—';
  return date.toLocaleString(undefined, {
    year: 'numeric', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });
}

const Settings = () => {
  const { theme, toggleTheme, isDark } = useTheme();
  const { student, signOut } = useAuth();

  return (
    <div className="settings-layout">
      <div className="settings-header">
        <div>
          <h1 className="page-title">Settings</h1>
          <p className="page-subtitle">Your account, and appearance preferences remembered in this browser.</p>
        </div>
      </div>

      <section className="settings-card glass-panel">
        <div className="settings-card-header">
          <User size={18} color="var(--accent)" />
          <h2>Account</h2>
        </div>

        <div className="account-identity">
          {student?.picture_url ? (
            <img className="account-avatar" src={student.picture_url} alt="" referrerPolicy="no-referrer" />
          ) : (
            <span className="account-avatar account-avatar-fallback"><User size={22} /></span>
          )}
          <div className="account-names">
            <strong>{student?.name || 'Student'}</strong>
            <span>{student?.email}</span>
            {student?.is_admin && (
              <span className="account-admin-chip"><ShieldCheck size={12} /> Administrator</span>
            )}
          </div>
        </div>

        {/* Everything here is Google's, refreshed at each sign-in — this app does not own
            your name or your picture, so there is nothing to edit. */}
        <dl className="account-facts">
          <div><dt>Member since</dt><dd>{formatDate(student?.created_at)}</dd></div>
          <div><dt>Last sign-in</dt><dd>{formatDate(student?.last_login_at)}</dd></div>
          <div><dt>Sign-ins</dt><dd>{student?.login_count ?? 0}</dd></div>
        </dl>

        <div className="settings-note">
          <Info size={14} />
          <span>
            Signed in with Google. Your name, email and picture come from your Google account
            and are refreshed each time you sign in.
          </span>
        </div>

        <button type="button" className="btn btn-ghost account-signout" onClick={signOut}>
          <LogOut size={15} /> Sign out
        </button>
      </section>

      <section className="settings-card glass-panel">
        <div className="settings-card-header">
          <Palette size={18} color="var(--accent)" />
          <h2>Appearance</h2>
        </div>

        <div className="setting-row">
          <div className="setting-copy">
            <label htmlFor="theme-switch" className="setting-name">
              Dark mode
            </label>
            <p className="setting-desc">
              Turn this off for the light theme — white cards on a soft grey page, styled after
              the IITM Study portal.
            </p>
          </div>

          <button
            id="theme-switch"
            type="button"
            role="switch"
            aria-checked={isDark}
            aria-label="Dark mode"
            className={`theme-switch ${isDark ? 'on' : 'off'}`}
            onClick={toggleTheme}
          >
            <span className="theme-switch-track">
              <span className="theme-switch-thumb">
                {isDark ? <Moon size={12} /> : <Sun size={12} />}
              </span>
            </span>
          </button>
        </div>

        <div className="theme-preview-row">
          <button
            type="button"
            className={`theme-preview ${isDark ? 'active' : ''}`}
            onClick={() => isDark || toggleTheme()}
          >
            <span className="preview-swatch preview-dark">
              <span className="swatch-bar" />
              <span className="swatch-line" />
              <span className="swatch-line short" />
            </span>
            <span className="preview-name">
              <Moon size={13} /> Dark
            </span>
          </button>

          <button
            type="button"
            className={`theme-preview ${!isDark ? 'active' : ''}`}
            onClick={() => isDark && toggleTheme()}
          >
            <span className="preview-swatch preview-light">
              <span className="swatch-bar" />
              <span className="swatch-line" />
              <span className="swatch-line short" />
            </span>
            <span className="preview-name">
              <Sun size={13} /> Light
            </span>
          </button>
        </div>

        <div className="settings-note">
          <Info size={14} />
          <span>
            This preference is saved in your browser, so reloading or opening a new tab keeps
            the theme you picked. It is stored per browser, not on your account.
          </span>
        </div>
      </section>

      <p className="settings-footnote">Active theme: <strong>{theme}</strong></p>
    </div>
  );
};

export default Settings;
