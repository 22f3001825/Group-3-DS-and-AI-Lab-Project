import React, { useState, useEffect } from 'react';
import { User, RefreshCw, BookOpen, CheckCircle, AlertCircle } from 'lucide-react';
import APIClient from '../api/client';
import './Progress.css';

const STUDENT_KEY = 'mlt_student_id';

function MasteryBar({ score }) {
  const pct = Math.round(score * 100);
  let color = 'var(--success)';
  if (pct < 40) color = 'var(--danger)';
  else if (pct < 70) color = 'var(--warning)';
  return (
    <div className="mastery-bar-wrap">
      <div className="mastery-bar-fill" style={{ width: `${pct}%`, background: color }} />
    </div>
  );
}

export default function Progress() {
  const [studentId, setStudentId] = useState(() => localStorage.getItem(STUDENT_KEY) || '');
  const [input, setInput] = useState(studentId);
  const [mastery, setMastery] = useState([]);
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    if (studentId) loadDashboard(studentId);
  }, []);

  const loadDashboard = async (sid) => {
    setLoading(true);
    setLoaded(false);
    try {
      const [m, q] = await Promise.all([
        APIClient.getMastery(sid).catch(() => []),
        APIClient.getQuizHistory(sid).catch(() => []),
      ]);
      setMastery(m);
      setQuizzes(q);
      setLoaded(true);
    } catch {
      setMastery([]);
      setQuizzes([]);
    } finally {
      setLoading(false);
    }
  };

  const handleLoad = (e) => {
    e.preventDefault();
    const sid = input.trim();
    if (!sid) return;
    setStudentId(sid);
    localStorage.setItem(STUDENT_KEY, sid);
    loadDashboard(sid);
  };

  const avgMastery = mastery.length > 0
    ? Math.round(mastery.reduce((s, t) => s + t.mastery_score, 0) / mastery.length * 100)
    : 0;

  const weakTopics = mastery.filter(t => t.mastery_score < 0.6).slice(0, 3);
  const strongTopics = mastery.filter(t => t.mastery_score >= 0.7);

  return (
    <div className="progress-layout">
      {/* Header */}
      <div className="progress-header">
        <div>
          <h1 className="page-title">📊 Learning Progress</h1>
          <p className="page-subtitle">Track your mastery across all MLT course topics</p>
        </div>
        <form onSubmit={handleLoad} className="student-form">
          <input
            className="input"
            placeholder="Student ID"
            value={input}
            onChange={e => setInput(e.target.value)}
            style={{ width: 200 }}
          />
          <button className="btn btn-primary" type="submit" disabled={loading}>
            {loading ? <div className="spinner" style={{ width: 16, height: 16 }} /> : <RefreshCw size={16} />}
            Load
          </button>
        </form>
      </div>

      {!loaded && !loading ? (
        <div className="progress-empty glass-panel">
          <User size={48} color="var(--text-muted)" />
          <h3>Enter Your Student ID</h3>
          <p>Type your student ID above and click <strong>Load</strong> to see your progress.</p>
        </div>
      ) : loading ? (
        <div className="progress-empty glass-panel">
          <div className="spinner" style={{ width: 32, height: 32 }} />
          <p>Loading your progress…</p>
        </div>
      ) : (
        <>
          {/* Stats Row */}
          <div className="stats-row">
            <div className="stat-card glass-panel">
              <div className="stat-num">{quizzes.length}</div>
              <div className="stat-label">Quizzes Taken</div>
            </div>
            <div className="stat-card glass-panel">
              <div className="stat-num">{avgMastery}%</div>
              <div className="stat-label">Avg Mastery</div>
            </div>
            <div className="stat-card glass-panel">
              <div className="stat-num">{mastery.length}</div>
              <div className="stat-label">Topics Tested</div>
            </div>
            <div className="stat-card glass-panel">
              <div className="stat-num">{quizzes.filter(q => q.is_correct).length}</div>
              <div className="stat-label">Correct Answers</div>
            </div>
          </div>

          {/* Recommendations */}
          {weakTopics.length > 0 && (
            <div className="rec-card glass-panel">
              <div className="rec-header">
                <AlertCircle size={18} color="var(--warning)" />
                <h3>Knowledge Gaps Detected</h3>
              </div>
              <p className="rec-sub">Focus on these topics to improve your overall score:</p>
              <div className="rec-topics">
                {weakTopics.map((t, i) => (
                  <div key={i} className="rec-topic-chip">
                    <span>{t.topic_name}</span>
                    <span className="chip-score" style={{ color: 'var(--warning)' }}>
                      {Math.round(t.mastery_score * 100)}%
                    </span>
                  </div>
                ))}
              </div>
              <p className="mayank-note">
                🔧 <strong>For Mayank:</strong> The <code>/learner/{'{id}'}/mastery</code> endpoint returns topics sorted by score (weakest first). Use this for the Recommendation Engine.
              </p>
            </div>
          )}

          {strongTopics.length > 0 && (
            <div className="strong-card glass-panel">
              <div className="rec-header">
                <CheckCircle size={18} color="var(--success)" />
                <h3>Strong Topics ({strongTopics.length})</h3>
              </div>
              <div className="rec-topics">
                {strongTopics.map((t, i) => (
                  <div key={i} className="rec-topic-chip strong">
                    <span>{t.topic_name}</span>
                    <span className="chip-score" style={{ color: 'var(--success)' }}>
                      {Math.round(t.mastery_score * 100)}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Mastery Grid */}
          <div className="mastery-section">
            <h2 className="section-title">
              <BookOpen size={18} /> Topic Mastery
            </h2>
            {mastery.length === 0 ? (
              <div className="progress-empty glass-panel" style={{ padding: '40px' }}>
                <p>No mastery data yet. Take some quizzes first!</p>
              </div>
            ) : (
              <div className="mastery-grid">
                {mastery.map((t, i) => {
                  const pct = Math.round(t.mastery_score * 100);
                  let scoreColor = 'var(--success)';
                  if (pct < 40) scoreColor = 'var(--danger)';
                  else if (pct < 70) scoreColor = 'var(--warning)';
                  return (
                    <div key={i} className="mastery-card glass-panel animate-fade-in">
                      <div className="mastery-card-header">
                        <span className="mastery-topic-name">{t.topic_name}</span>
                        <span className="mastery-pct" style={{ color: scoreColor }}>{pct}%</span>
                      </div>
                      <MasteryBar score={t.mastery_score} />
                      <div className="mastery-card-meta">
                        <span>Attempts: {t.attempts}</span>
                        <span>{t.last_tested ? new Date(t.last_tested).toLocaleDateString() : 'N/A'}</span>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}
