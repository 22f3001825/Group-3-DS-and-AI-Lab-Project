import React, { useState, useRef, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { Send, User, Bot, BookOpen, ChevronDown, ChevronUp, Clock, Zap, Video } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import APIClient from '../api/client';
import './Chat.css';

const STUDENT_KEY = 'mlt_student_id';

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
            <div className="prose assistant-text">
              <ReactMarkdown>{msg.content}</ReactMarkdown>
            </div>
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
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hi! I'm your **MLT Course Assistant**. I can answer questions about Machine Learning, AI, Statistics, and all topics covered in the IIT Madras MLT course with precise lecture timestamps and citation navigation. What would you like to learn today?",
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [studentId, setStudentId] = useState(() => localStorage.getItem(STUDENT_KEY) || 'student_001');
  const [editingId, setEditingId] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  useEffect(() => {
    if (location.state?.initialPrompt) {
      setInput(location.state.initialPrompt);
    }
  }, [location.state]);

  const handleSetId = (e) => {
    e.preventDefault();
    localStorage.setItem(STUDENT_KEY, studentId.trim());
    setEditingId(false);
  };

  const sendMessage = async () => {
    const question = input.trim();
    if (!question || loading) return;

    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: question }]);
    setLoading(true);

    try {
      const result = await APIClient.chat(question, studentId || null);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: result.answer,
        sources: result.sources,
        provider: result.provider_used,
      }]);
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '⚠️ Could not reach the backend. Make sure FastAPI is running on port 8000.',
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
          <h3 className="sidebar-title">👤 Session</h3>
          {editingId ? (
            <form onSubmit={handleSetId} className="id-form">
              <input
                className="input"
                placeholder="Student ID"
                value={studentId}
                onChange={e => setStudentId(e.target.value)}
                autoFocus
              />
              <button className="btn btn-primary" type="submit" style={{ width: '100%' }}>Save</button>
            </form>
          ) : (
            <div className="student-id-display" onClick={() => setEditingId(true)}>
              {studentId ? (
                <><User size={14} /> <span>{studentId}</span></>
              ) : (
                <span className="text-muted">Click to set Student ID</span>
              )}
            </div>
          )}
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
