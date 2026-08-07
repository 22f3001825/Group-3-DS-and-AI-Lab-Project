import { createContext, useContext } from 'react';

/*
  Session state lives in localStorage under the key `client.js` owns (TOKEN_STORAGE_KEY),
  so exactly one module decides what a stored session is and the request layer can attach
  the bearer without importing React.

  The context and the hook live in this non-component module for the same reason the
  theme's do: a .jsx file exporting non-components breaks Vite fast refresh.

  `status` is deliberately three-valued rather than a boolean. On a hard refresh the
  provider has a token in localStorage but has not yet confirmed it with /auth/me, and a
  RequireAuth that treats "not yet authenticated" as "anonymous" redirects to /login for a
  frame — losing the requested URL and, with it, the { topicId } router state Progress
  passes to Quiz. 'loading' is what stops that.
*/
export const AUTH_STATUS = {
  LOADING: 'loading',
  AUTHENTICATED: 'authenticated',
  ANONYMOUS: 'anonymous',
};

export const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || '';

export const AuthContext = createContext(null);

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside an AuthProvider');
  return ctx;
}
