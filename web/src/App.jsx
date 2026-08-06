import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Chat from './pages/Chat';
import Quiz from './pages/Quiz';
import Progress from './pages/Progress';
import Doubts from './pages/Doubts';
import Admin from './pages/Admin';
import Settings from './pages/Settings';
import ThemeProvider from './theme/ThemeProvider';
import './App.css';

function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <div className="app-container">
          <Navbar />
          <Routes>
            <Route path="/" element={<Chat />} />
            <Route path="/quiz" element={<Quiz />} />
            <Route path="/progress" element={<Progress />} />
            <Route path="/doubts" element={<Doubts />} />
            <Route path="/settings" element={<Settings />} />
            {/* Unlisted in the navbar unless a token is stored. The route itself is not the
                guard — every admin endpoint is, and it 503s when ADMIN_TOKEN is unset. */}
            <Route path="/admin" element={<Admin />} />
          </Routes>
        </div>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
