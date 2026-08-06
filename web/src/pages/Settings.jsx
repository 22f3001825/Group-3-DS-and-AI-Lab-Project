import React from 'react';
import { Moon, Sun, Palette, Info } from 'lucide-react';
import { useTheme } from '../theme/theme-context';
import './Settings.css';

const Settings = () => {
  const { theme, toggleTheme, isDark } = useTheme();

  return (
    <div className="settings-layout">
      <div className="settings-header">
        <div>
          <h1 className="page-title">Settings</h1>
          <p className="page-subtitle">Appearance preferences for this browser tab.</p>
        </div>
      </div>

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
            This preference is not saved anywhere — it lives in the page's state only. Reloading
            or opening a new tab starts you back on dark mode.
          </span>
        </div>
      </section>

      <p className="settings-footnote">Active theme: <strong>{theme}</strong></p>
    </div>
  );
};

export default Settings;
