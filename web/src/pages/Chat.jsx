import React, { useState, useRef, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Send, User, Bot, BookOpen, ChevronDown, ChevronUp, Clock, Zap, Video, Layers } from 'lucide-react';
import APIClient from '../api/client';
import RichText from '../components/RichText';
import { useAuth } from '../auth/auth-context';
import './Chat.css';

// Messages sent back as conversation memory — 3 exchanges, matching CHAT_MEMORY_TURNS in
// src/config.py. The server trims to its own limit regardless; this just avoids uploading
// a whole session's answers on every message.
const MEMORY_MESSAGES = 6;

function SourceChip({ source, index }) {
  const [open, setOpen] = useState(false);
  const meta = source.metadata || {};
  const lectureTitle = meta.lecture_title || meta.h1 || `Context ${index + 1}`;
  const timestamp = meta.timestamp;
  const week = meta.week;

  return (
    <div className={`source-chip ${open ? 'expanded' : ''}`}>
      <button className="source-chip-header" onClick={() => setOpen(!open)}>
        <BookOpen size={13} />
        <span className="source-title-text">
          {meta.formatted_ref || (week ? `Week ${week}: ${lectureTitle}` : lectureTitle)}
        </span>
        {open ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
      </button>
      {open && (
        <div className="source-chip-body">
          <div className="source-meta">
            <span className="source-type-tag">{meta.source_type || 'Lecture Material'}</span>
            {week && <span className="week-tag">Week {week}</span>}
            {timestamp && (
              <span className="timestamp-tag">
                <Clock size={11} /> Timestamp: {timestamp}
              </span>
            )}
            {lectureTitle && (
              <span className="lecture-tag">
                <Video size={11} /> {lectureTitle}
              </span>
            )}
          </div>
          <p>{source.text?.slice(0, 320)}{source.text?.length > 320 ? '…' : ''}</p>
        </div>
      )}
    </div>
  );
}

function Message({ msg }) {
  const isUser = msg.role === 'user';
  return (
    <div className={`message-row ${isUser ? 'user' : 'assistant'} animate-fade-in`}>
      <div className="message-avatar">
        {isUser ? <User size={16} /> : <Bot size={16} />}
      </div>
      <div className="message-bubble">
        {isUser ? (
          <p className="user-text">{msg.content}</p>
        ) : (
          <>
            {/* `build_prompt` mandates a Math section, and the retrieved context it
                works from is written in `\(...\)` / `\[...\]` — so answers carry the
                same LaTeX the question bank does and need the same renderer. */}
            <RichText className="prose assistant-text">{msg.content}</RichText>
            {msg.provider && (
              <div className="provider-tag">
                <Zap size={11} /> via {msg.provider}
              </div>
            )}
            {msg.sources && msg.sources.length > 0 && (
              <div className="sources-row">
                <div className="sources-label">📚 Cited Lecture Sources &amp; Timestamps:</div>
                {msg.sources.map((s, i) => <SourceChip key={i} source={s} index={i} />)}
              </div>
            )}
            {msg.related && msg.related.length > 0 && (
              <div className="related-row">
                <div className="sources-label">🔗 Students also asked:</div>
                {msg.related.map(r => (
                  <Link key={r.unit_id} className="related-chip" to={`/doubts?cluster=${r.cluster_id}`}>
                    <Layers size={12} />
                    <span>{r.title}</span>
                    {r.member_count > 1 && <em>×{r.member_count}</em>}
                  </Link>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

function TypingIndicator() {
  return (
    <div className="message-row assistant animate-fade-in">
      <div className="message-avatar"><Bot size={16} /></div>
      <div className="message-bubble typing-bubble">
        <span className="dot" /><span className="dot" /><span className="dot" />
      </div>
    </div>
  );
}

export default function Chat() {
  const location = useLocation();
  // One source of identity for the whole app. There is no editable student-ID box any
  // more: the server takes the id from the bearer token and ignores anything else.
  const { student } = useAuth();
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hi! I'm your **MLT Course Assistant**. I can answer questions about Machine Learning, AI, Statistics, and all topics covered in the IIT Madras MLT course with precise lecture timestamps and citation navigation. What would you like to learn today?",
      // Not part of the conversation — never sent back as memory.
      synthetic: true,
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  useEffect(() => {
    if (location.state?.initialPrompt) {
      setInput(location.state.initialPrompt);
    }
  }, [location.state]);

  const sendMessage = async () => {
    const question = input.trim();
    if (!question || loading) return;

    // Built from the state captured before this question is appended, so the current
    // question is not duplicated into its own memory.
    const history = messages
      .filter(m => !m.synthetic)
      .slice(-MEMORY_MESSAGES)
      .map(({ role, content }) => ({ role, content }));

    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: question }]);
    setLoading(true);

    try {
      const result = await APIClient.chat(question, null, history);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: result.answer,
        sources: result.sources,
        provider: result.provider_used,
        // Defaulted server-side, so an unbuilt question bank is indistinguishable from
        // "nothing related" rather than being an error the chat has to handle.
        related: result.related_questions || [],
      }]);
    } catch {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '⚠️ Could not reach the backend. Make sure FastAPI is running on port 8000.',
        synthetic: true,
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const suggestions = [
    'What is Principal Component Analysis and where is it covered in lectures?',
    'Explain Gradient Descent step by step with lecture citations',
    'What is the Bias-Variance Tradeoff in machine learning?',
    'How does Singular Value Decomposition (SVD) relate to PCA?',
  ];

  return (
    <div className="chat-layout">
      {/* Sidebar */}
      <aside className="chat-sidebar glass-panel">
        <div className="sidebar-section">
          <h3 className="sidebar-title">👤 Signed in</h3>
          <div className="student-id-display">
            <User size={14} /> <span>{student?.name || student?.email || 'Student'}</span>
          </div>
        </div>

        <div className="sidebar-section">
          <h3 className="sidebar-title">💡 Try Asking</h3>
          <div className="suggestions">
            {suggestions.map((s, i) => (
              <button
                key={i}
                className="suggestion-btn"
                onClick={() => setInput(s)}
              >
                {s}
              </button>
            ))}
          </div>
        </div>
      </aside>

      {/* Main Chat */}
      <main className="chat-main">
        <div className="messages-container">
          {messages.map((msg, i) => <Message key={i} msg={msg} />)}
          {loading && <TypingIndicator />}
          <div ref={bottomRef} />
        </div>

        <div className="chat-input-area glass-panel">
          <textarea
            className="chat-textarea"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask anything about the MLT course…"
            rows={1}
            disabled={loading}
          />
          <button
            className="btn btn-primary send-btn"
            onClick={sendMessage}
            disabled={loading || !input.trim()}
          >
            {loading ? <div className="spinner" style={{ width: 16, height: 16 }} /> : <Send size={18} />}
          </button>
        </div>
      </main>
    </div>
  );
}
