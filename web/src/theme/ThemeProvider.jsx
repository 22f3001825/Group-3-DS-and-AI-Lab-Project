import React, { useCallback, useEffect, useLayoutEffect, useMemo, useState } from 'react';
import {
  ThemeContext,
  getInitialTheme,
  normalizeTheme,
  THEME_STORAGE_KEY,
} from './theme-context';

export function ThemeProvider({ children }) {
  // Pass the function reference to lazy-initialize state only once on mount
  const [theme, setThemeState] = useState(getInitialTheme);

  // Everything visual keys off data-theme on <html>; without this the stored value
  // is remembered but nothing repaints. Layout effect so the attribute lands before
  // the browser paints the new state.
  useLayoutEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  useEffect(() => {
    try {
      localStorage.setItem(THEME_STORAGE_KEY, theme);
    } catch (error) {
      console.warn('Failed to save theme to localStorage:', error);
    }
  }, [theme]);

  // Another tab changed the preference. The storage event does not fire in the tab
  // that wrote it, so this only ever reacts to someone else's write.
  useEffect(() => {
    const onStorage = (event) => {
      if (event.key !== THEME_STORAGE_KEY) return;
      setThemeState(normalizeTheme(event.newValue));
    };
    window.addEventListener('storage', onStorage);
    return () => window.removeEventListener('storage', onStorage);
  }, []);

  // Normalize on the way in so a bad value can never be persisted or written to the DOM.
  const setTheme = useCallback((next) => {
    setThemeState((prev) => normalizeTheme(typeof next === 'function' ? next(prev) : next));
  }, []);

  const toggleTheme = useCallback(() => {
    setThemeState((prev) => (prev === 'dark' ? 'light' : 'dark'));
  }, []);

  const value = useMemo(
    () => ({ theme, setTheme, toggleTheme, isDark: theme === 'dark' }),
    [theme, setTheme, toggleTheme],
  );

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export default ThemeProvider;
