import { createContext, useContext } from 'react';

/*
  Theme lives in UI state only — deliberately not in localStorage and not on the
  server. Every session (and every refresh) starts on dark; the switch on /settings
  is the only thing that changes it, and the change dies with the tab.

  The context and the hook live in this non-component module so ThemeProvider.jsx
  can stay component-only (Vite fast refresh requires that).
*/
export const DEFAULT_THEME = 'dark';

export const ThemeContext = createContext(null);

export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useTheme must be used inside a ThemeProvider');
  return ctx;
}
