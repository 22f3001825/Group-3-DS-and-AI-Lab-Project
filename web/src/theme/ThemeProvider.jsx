import React, { useEffect, useState } from 'react';
import { ThemeContext, DEFAULT_THEME } from './theme-context';

export default function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(DEFAULT_THEME);

  // The stylesheet keys off data-theme on <html>: absent/"dark" = the dark palette
  // in :root, "light" = the override block.
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  const toggleTheme = () => setTheme((t) => (t === 'dark' ? 'light' : 'dark'));

  return (
    <ThemeContext.Provider value={{ theme, setTheme, toggleTheme, isDark: theme === 'dark' }}>
      {children}
    </ThemeContext.Provider>
  );
}
