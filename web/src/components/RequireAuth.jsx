import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../auth/auth-context';
import './RequireAuth.css';

/** Blocks a route until the session is known.
 *
 *  The `isLoading` branch is the whole point: while a stored token is being confirmed
 *  with /auth/me there is no answer yet, and redirecting on "not authenticated" would
 *  flash the login page on every hard refresh and drop the requested URL — including the
 *  { topicId } router state Progress hands to Quiz.
 */
export function RequireAuth({ children }) {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) return <AuthSplash label="Restoring your session…" />;
  if (!isAuthenticated) {
    // `state.from` is what sends the user back where they were aiming after signing in.
    return <Navigate to="/login" replace state={{ from: location }} />;
  }
  return children;
}

/** Admin-only routes. Non-admins are sent to Chat rather than to /login: they ARE signed
 *  in, so a login page would be a lie and an invitation to try again. */
export function RequireAdmin({ children }) {
  const { isAuthenticated, isLoading, isAdmin } = useAuth();
  const location = useLocation();

  if (isLoading) return <AuthSplash label="Restoring your session…" />;
  if (!isAuthenticated) return <Navigate to="/login" replace state={{ from: location }} />;
  if (!isAdmin) return <Navigate to="/" replace />;
  return children;
}

function AuthSplash({ label }) {
  return (
    <div className="auth-splash">
      <div className="spinner" style={{ width: 28, height: 28 }} />
      <p>{label}</p>
    </div>
  );
}

export default RequireAuth;
