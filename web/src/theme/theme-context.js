import { createContext, useContext } from 'react';

/*
  Theme preference is persisted in localStorage under THEME_STORAGE_KEY. Every new
  session/refresh reads the stored preference, defaulting to 'dark' if none is found
  (or if the stored value is not one this app renders — see normalizeTheme).

  The stylesheet keys off data-theme on <html>: absent/"dark" = the dark palette in
  :root, "light" = the override block. index.html sets that attribute from the same
  key before React mounts, so a light-mode reload does not flash dark.

  The context and the hook live in this non-component module so ThemeProvider.jsx
  can stay component-only (satisfying Vite fast refresh rules).
*/
export const DEFAULT_THEME = 'dark';
export const THEME_STORAGE_KEY = 'theme';
export const THEMES = ['dark', 'light'];

/**
 * Collapse anything (stale key, hand-edited localStorage, a bad setTheme call) down
 * to a theme the stylesheet actually implements.
 */
export function normalizeTheme(value) {
  return THEMES.includes(value) ? value : DEFAULT_THEME;
}

/**
 * Helper to safely retrieve the initial theme from localStorage.
 */
export function getInitialTheme() {
  if (typeof window === 'undefined') return DEFAULT_THEME;

  try {
    return normalizeTheme(localStorage.getItem(THEME_STORAGE_KEY));
  } catch (error) {
    // Failsafe for restricted environments (e.g. strict privacy modes)
    console.warn('Failed to read theme from localStorage:', error);
  }

  return DEFAULT_THEME;
}

export const ThemeContext = createContext(null);

export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useTheme must be used inside a ThemeProvider');
  return ctx;
}
