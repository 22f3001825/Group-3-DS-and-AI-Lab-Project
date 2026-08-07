import React, { useState } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { GoogleLogin } from '@react-oauth/google';
import { Brain, AlertTriangle, ShieldCheck, Sparkles } from 'lucide-react';
import { GOOGLE_CLIENT_ID, useAuth } from '../auth/auth-context';
import { useTheme } from '../theme/theme-context';
import './Login.css';

/** Every way a sign-in can fail, said in the words that tell you what to do about it.
 *  A single "sign-in failed" would leave a rejected domain and an unconfigured server
 *  looking identical, and only one of them is the user's problem. */
function describeAuthError(error) {
  if (!error) return null;
  if (error.status === 0) {
    return 'Cannot reach the API. Make sure the FastAPI backend is running on port 8000.';
  }
  if (error.code === 'email_collision') {
    return `${error.message} Ask whoever runs this instance to clear that row's email address.`;
  }
  if (error.status === 503) {
    return `${error.message || 'Sign-in is not configured on the server.'} If this is your own instance, `
      + 'set GOOGLE_CLIENT_ID and JWT_SECRET in the repo-root .env and restart the API.';
  }
  if (error.status === 403) return error.message || 'This account is not allowed to sign in.';
  if (error.status === 401) return 'Google rejected that sign-in. Try again.';
  return error.message || 'Sign-in failed.';
}

export default function Login() {
  const { isAuthenticated, isLoading, signIn } = useAuth();
  const { isDark } = useTheme();
  const location = useLocation();
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);

  // Where the user was actually heading before RequireAuth intercepted them.
  const destination = location.state?.from?.pathname || '/';

  if (isAuthenticated) return <Navigate to={destination} replace />;

  const handleSuccess = async (credentialResponse) => {
    setError(null);
    setBusy(true);
    try {
      // `credential` is the ID TOKEN. <GoogleLogin> is used rather than useGoogleLogin()
      // precisely because the hook's OAuth access-token flow does not produce one, and
      // the whole backend design verifies this token's claims.
      await signIn(credentialResponse.credential);
    } catch (err) {
      setError(err);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="login-layout">
      <div className="login-card glass-panel">
        <div className="login-brand">
          <Brain size={30} color="var(--accent)" />
          <h1>MLT Assistant</h1>
        </div>
        <p className="login-sub">
          Your study assistant for the IIT Madras BS Degree Machine Learning Techniques
          course. Sign in with Google to keep your progress, mastery and quiz history.
        </p>

        {!GOOGLE_CLIENT_ID ? (
          <div className="login-error">
            <AlertTriangle size={16} />
            <div>
              <strong>Google sign-in is not configured in this build.</strong>
              <p>
                Set <code>VITE_GOOGLE_CLIENT_ID</code> in <code>web/.env</code> to the same
                OAuth Web client ID as <code>GOOGLE_CLIENT_ID</code> in the repo-root
                <code>.env</code>, then restart <code>npm run dev</code>.
              </p>
            </div>
          </div>
        ) : (
          <div className="login-google">
            {busy || isLoading ? (
              <div className="login-busy">
                <div className="spinner" style={{ width: 18, height: 18 }} />
                <span>Signing you in…</span>
              </div>
            ) : (
              <GoogleLogin
                onSuccess={handleSuccess}
                onError={() => setError({ status: 401 })}
                theme={isDark ? 'filled_black' : 'outline'}
                shape="pill"
                size="large"
                text="signin_with"
                useOneTap
              />
            )}
          </div>
        )}

        {error && (
          <div className="login-error">
            <AlertTriangle size={16} />
            <div>
              <strong>Could not sign you in</strong>
              <p>{describeAuthError(error)}</p>
            </div>
          </div>
        )}

        <ul className="login-points">
          <li><Sparkles size={14} /> Answers cited to lecture material, with timestamps</li>
          <li><ShieldCheck size={14} /> Your quiz history and mastery stay on your account</li>
        </ul>
      </div>
    </div>
  );
}
