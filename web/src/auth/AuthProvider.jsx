import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import APIClient, {
  TOKEN_STORAGE_KEY,
  UNAUTHORIZED_EVENT,
  getToken,
  setToken,
} from '../api/client';
import { AUTH_STATUS, AuthContext } from './auth-context';

/**
 * Holds the session: the stored JWT, the student it belongs to, and which of the three
 * states we are in. Sits INSIDE BrowserRouter (unlike ThemeProvider, which wraps it)
 * because signing out has to navigate.
 */
export function AuthProvider({ children }) {
  const navigate = useNavigate();
  // Lazy initialiser, so localStorage is read once on mount rather than every render.
  const [token, setTokenState] = useState(getToken);
  const [student, setStudent] = useState(null);
  const [status, setStatus] = useState(() => (getToken() ? AUTH_STATUS.LOADING : AUTH_STATUS.ANONYMOUS));

  const clearSession = useCallback(() => {
    setToken('');
    setTokenState('');
    setStudent(null);
    setStatus(AUTH_STATUS.ANONYMOUS);
  }, []);

  // Confirm a restored token with the server rather than trusting its contents. This is
  // also what makes a demotion or a deactivation visible within one page load, since
  // `is_admin` and `is_active` are read from the row and never from the token.
  useEffect(() => {
    if (!token) {
      setStatus(AUTH_STATUS.ANONYMOUS);
      return undefined;
    }
    let cancelled = false;
    setStatus(AUTH_STATUS.LOADING);
    APIClient.getMe()
      .then((me) => {
        if (cancelled) return;
        setStudent(me);
        setStatus(AUTH_STATUS.AUTHENTICATED);
      })
      .catch((error) => {
        if (cancelled) return;
        if (error?.status === 0) {
          // The backend is down, not the session. Dropping the token here would sign the
          // user out every time uvicorn restarts.
          setStatus(AUTH_STATUS.ANONYMOUS);
          return;
        }
        clearSession();
      });
    return () => { cancelled = true; };
  }, [token, clearSession]);

  // Any 401 from a non-/auth call means the session ended mid-use. The event is deduped
  // in client.js, so parallel requests produce one navigation.
  useEffect(() => {
    const onUnauthorized = () => {
      clearSession();
      navigate('/login', { replace: true });
    };
    window.addEventListener(UNAUTHORIZED_EVENT, onUnauthorized);
    return () => window.removeEventListener(UNAUTHORIZED_EVENT, onUnauthorized);
  }, [clearSession, navigate]);

  // Another tab signed in or out. The storage event never fires in the tab that wrote it,
  // so this only ever reacts to someone else's write.
  useEffect(() => {
    const onStorage = (event) => {
      if (event.key !== TOKEN_STORAGE_KEY) return;
      const next = event.newValue || '';
      setTokenState(next);
      if (!next) {
        setStudent(null);
        setStatus(AUTH_STATUS.ANONYMOUS);
      }
    };
    window.addEventListener('storage', onStorage);
    return () => window.removeEventListener('storage', onStorage);
  }, []);

  /** Exchange Google's ID token for a session. Throws the API error so the login page
   *  can tell 403-domain from 409-collision from 503-unconfigured. */
  const signIn = useCallback(async (credential) => {
    const result = await APIClient.loginWithGoogle(credential);
    setToken(result.access_token);
    setStudent(result.student);
    setTokenState(result.access_token);
    setStatus(AUTH_STATUS.AUTHENTICATED);
    return result.student;
  }, []);

  const signOut = useCallback(() => {
    clearSession();
    navigate('/login', { replace: true });
  }, [clearSession, navigate]);

  /** Re-read the profile — used after anything that changes it server-side. */
  const refresh = useCallback(async () => {
    const me = await APIClient.getMe();
    setStudent(me);
    return me;
  }, []);

  const value = useMemo(() => ({
    status,
    student,
    // Convenience reads. `studentId` is what the pages used to keep in localStorage
    // three separate times; there is now one source for it.
    studentId: student?.student_id || '',
    isAuthenticated: status === AUTH_STATUS.AUTHENTICATED,
    isLoading: status === AUTH_STATUS.LOADING,
    isAdmin: Boolean(student?.is_admin),
    signIn,
    signOut,
    refresh,
  }), [status, student, signIn, signOut, refresh]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export default AuthProvider;
