import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { GoogleOAuthProvider } from '@react-oauth/google';
import Navbar from './components/Navbar';
import { RequireAdmin, RequireAuth } from './components/RequireAuth';
import Chat from './pages/Chat';
import Quiz from './pages/Quiz';
import Progress from './pages/Progress';
import Doubts from './pages/Doubts';
import Admin from './pages/Admin';
import Settings from './pages/Settings';
import Login from './pages/Login';
import ThemeProvider from './theme/ThemeProvider';
import AuthProvider from './auth/AuthProvider';
import { GOOGLE_CLIENT_ID } from './auth/auth-context';
import './App.css';

/*
  Provider order is load-bearing:

    ThemeProvider  — outermost, so the login page is themed too and nothing flashes.
    BrowserRouter  — must wrap AuthProvider, which calls useNavigate to send an expired
                     session back to /login. This is the deliberate difference from
                     ThemeProvider, which has no reason to be inside the router.
    GoogleOAuthProvider — loads Google's script and holds the client ID for <GoogleLogin>.
    AuthProvider   — the session itself.

  Every route except /login is wrapped in <RequireAuth>; /admin adds <RequireAdmin>. The
  route guard is not the security boundary — every endpoint is — but it is what keeps the
  UI from rendering pages that can only 401.
*/
function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
          <AuthProvider>
            <div className="app-container">
              <Navbar />
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/" element={<RequireAuth><Chat /></RequireAuth>} />
                <Route path="/quiz" element={<RequireAuth><Quiz /></RequireAuth>} />
                <Route path="/progress" element={<RequireAuth><Progress /></RequireAuth>} />
                <Route path="/doubts" element={<RequireAuth><Doubts /></RequireAuth>} />
                <Route path="/settings" element={<RequireAuth><Settings /></RequireAuth>} />
                <Route path="/admin" element={<RequireAdmin><Admin /></RequireAdmin>} />
              </Routes>
            </div>
          </AuthProvider>
        </GoogleOAuthProvider>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
