import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  User, RefreshCw, BookOpen, CheckCircle, AlertTriangle,
  Clock, ArrowRight, Brain, Target, Award, Sparkles, MessageSquare
} from 'lucide-react';
import APIClient from '../api/client';
import { useAuth } from '../auth/auth-context';
import './Progress.css';

function MasteryProgressBar({ score }) {
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

function getStatusBadge(status) {
  switch (status) {
    case 'weak':
      return <span className="status-badge weak">🔴 Weak (&lt;40%)</span>;
    case 'developing':
      return <span className="status-badge developing">🟡 Developing (40-69%)</span>;
    case 'strong':
      return <span className="status-badge strong">🟢 Mastered (≥70%)</span>;
    case 'decaying':
      return <span className="status-badge decaying">⏳ Needs Review (Decaying)</span>;
    case 'explored':
      return <span className="status-badge explored">🔵 Explored in Chat</span>;
    default:
      return <span className="status-badge untested">⚪ Untested</span>;
  }
}

export default function Progress() {
  const navigate = useNavigate();
  // Identity comes from the session. The "Change ID" box that used to live in this
  // header was the whole of the old access control — typing any id read that person's
  // profile — and the server now refuses a path id that is not the caller's.
  const { studentId, student } = useAuth();
  const [profile, setProfile] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [loaded, setLoaded] = useState(false);
  const [selectedTopic, setSelectedTopic] = useState(null);

  const loadDashboard = useCallback(async (sid, forceRefresh = false) => {
    // The full-page spinner is for the initial load; a forced refresh only spins its
    // own button so the dashboard underneath stays readable.
    if (forceRefresh) setRefreshing(true);
    else setLoading(true);

    try {
      const [profData, recData] = await Promise.all([
        APIClient.getLearnerProfile(sid).catch(() => null),
        APIClient.getRecommendations(sid, 5, forceRefresh).catch(() => null),
      ]);
      if (profData) setProfile(profData);
      if (recData) setRecommendations(recData);
      setLoaded(true);
    } catch (err) {
      console.error('Failed to load dashboard:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    if (studentId) loadDashboard(studentId, false);
  }, [studentId, loadDashboard]);

  const handleForceRefresh = () => {
    if (studentId) {
      loadDashboard(studentId, true);
    }
  };

  const handleStartQuiz = (topicId) => {
    navigate('/quiz', { state: { topicId: String(topicId) } });
  };

  const handleAskTutor = (topicName) => {
    navigate('/', { state: { initialPrompt: `Can you explain ${topicName} with a clear intuition and example?` } });
  };

  const studyPlan = recommendations?.study_plan || [];
  const strengths = recommendations?.strengths || [];
  const decaying = recommendations?.decaying_topics || [];
  const weeks = profile?.weeks || [];

  return (
    <div className="progress-layout">
      {/* Header */}
      <div className="progress-header">
        <div>
          <h1 className="page-title">📊 Learning Intelligence &amp; Mastery</h1>
          <p className="page-subtitle">
            Elo-based Knowledge Tracing &amp; Adaptive Gap Remediation
          </p>
        </div>
        <div className="header-controls">
          <span className="progress-account">
            <User size={15} /> {student?.name || student?.email || 'Signed in'}
          </span>
          <button
            className="btn btn-primary"
            onClick={handleForceRefresh}
            disabled={loading || refreshing}
            title="Recalculate study recommendations with AI"
          >
            {refreshing ? (
              <div className="spinner" style={{ width: 15, height: 15 }} />
            ) : (
              <RefreshCw size={15} />
            )}
            Refresh Plan
          </button>
        </div>
      </div>

      {!loaded && loading ? (
        <div className="progress-empty glass-panel">
          <div className="spinner" style={{ width: 32, height: 32 }} />
          <p>Analyzing course knowledge graph &amp; loading learner profile…</p>
        </div>
      ) : !loaded ? (
        <div className="progress-empty glass-panel">
          <AlertTriangle size={48} color="var(--text-muted)" />
          <h3>Could not load your profile</h3>
          <p>Make sure the FastAPI backend is running on port 8000, then hit <strong>Refresh Plan</strong>.</p>
        </div>
      ) : (
        <>
          {/* Key Metrics Overview */}
          <div className="stats-row">
            <div className="stat-card glass-panel">
              <div className="stat-num">{recommendations?.overall_mastery_pct ?? 0}%</div>
              <div className="stat-label">Overall Course Mastery</div>
            </div>
            <div className="stat-card glass-panel">
              <div className="stat-num">
                {recommendations?.total_topics_tested ?? 0} <span className="stat-subnum">/ {recommendations?.total_topics ?? 48}</span>
              </div>
              <div className="stat-label">Syllabus Coverage ({recommendations?.coverage_pct ?? 0}%)</div>
            </div>
            <div className="stat-card glass-panel">
              <div className="stat-num">{profile?.total_quizzes_taken ?? 0}</div>
              <div className="stat-label">Quizzes Completed</div>
            </div>
            <div className="stat-card glass-panel">
              <div className="stat-num">{profile?.quiz_accuracy_pct ?? 0}%</div>
              <div className="stat-label">Quiz Accuracy Rate</div>
            </div>
          </div>

          {/* Layer 3: Personalized Study Plan */}
          <section className="study-plan-section">
            <div className="section-header-row">
              <h2 className="section-title">
                <Brain size={20} color="var(--accent)" /> Personalized Study Roadmap
              </h2>
              <div className="section-header-tags">
                {recommendations?.llm_provider_used && recommendations.llm_provider_used !== 'none' && (
                  <span className="ai-advisor-tag">
                    <Sparkles size={13} /> AI Advice via {recommendations.llm_provider_used}
                  </span>
                )}
              </div>
            </div>

            {studyPlan.length === 0 ? (
              <div className="all-mastered-box glass-panel">
                <Award size={36} color="var(--success)" />
                <div>
                  <h3>Outstanding Mastery!</h3>
                  <p>You have demonstrated solid understanding across tested topics. Maintain your streak by doing occasional refresher quizzes.</p>
                </div>
              </div>
            ) : (
              <div className="study-cards-grid">
                {studyPlan.map((item, idx) => {
                  const scorePct = Math.round(item.effective_score * 100);
                  return (
                    <div key={idx} className="study-card glass-panel animate-fade-in">
                      <div className="study-card-top">
                        <div className="study-card-badge-row">
                          <span className="priority-pill">Priority #{idx + 1}</span>
                          <span className="week-pill">Week {item.week}</span>
                          {getStatusBadge(item.status)}
                        </div>
                        <h3 className="study-topic-title">{item.topic_name}</h3>
                      </div>

                      {/* Prerequisite Alert */}
                      {item.has_prerequisite_gap && (
                        <div className="prereq-alert">
                          <AlertTriangle size={15} color="var(--warning)" />
                          <span>
                            <strong>Prerequisite Gap:</strong> Review <em>{item.unmet_prerequisites.join(', ')}</em> first before advancing.
                          </span>
                        </div>
                      )}

                      {/* Score & Progress */}
                      <div className="study-score-section">
                        <div className="study-score-text">
                          <span>Mastery Rating:</span>
                          <strong>{scorePct}% (Elo: {item.elo_rating > 0 ? `+${item.elo_rating}` : item.elo_rating})</strong>
                        </div>
                        <MasteryProgressBar score={item.effective_score} />
                      </div>

                      {/* LLM Pedagogical Advice */}
                      {item.llm_advice && (
                        <div className="study-advice-box">
                          <p>{item.llm_advice}</p>
                        </div>
                      )}

                      {/* Actions */}
                      <div className="study-card-actions">
                        <button
                          className="btn btn-primary btn-sm"
                          onClick={() => handleStartQuiz(item.topic_id)}
                        >
                          <Target size={14} /> Practice Quiz
                        </button>
                        <button
                          className="btn btn-ghost btn-sm"
                          onClick={() => handleAskTutor(item.topic_name)}
                        >
                          <MessageSquare size={14} /> Ask in Chat
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </section>

          {/* Strengths & Decaying Retention Row */}
          <div className="dual-cards-row">
            {/* Decaying Topics (Spaced Repetition) */}
            {decaying.length > 0 && (
              <div className="retention-card glass-panel">
                <div className="card-sub-header">
                  <Clock size={18} color="var(--warning)" />
                  <h3>Spaced Repetition Refresher Due</h3>
                </div>
                <p className="card-sub-desc">These topics haven't been tested recently and are decaying:</p>
                <div className="decay-list">
                  {decaying.map((d, i) => (
                    <div key={i} className="decay-item">
                      <span>{d.topic_name} (W{d.week})</span>
                      <button
                        className="btn-link"
                        onClick={() => handleStartQuiz(d.topic_id)}
                      >
                        Refresher Quiz <ArrowRight size={12} />
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Strengths */}
            {strengths.length > 0 && (
              <div className="strengths-card glass-panel">
                <div className="card-sub-header">
                  <CheckCircle size={18} color="var(--success)" />
                  <h3>Mastered Concepts ({strengths.length})</h3>
                </div>
                <div className="strengths-tags">
                  {strengths.map((s, i) => (
                    <span key={i} className="strength-chip">
                      ✓ {s.topic_name} ({Math.round(s.effective_score * 100)}%)
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* 12-Week Topic Mastery Matrix */}
          <section className="matrix-section">
            <h2 className="section-title">
              <BookOpen size={20} /> 12-Week Course Syllabus Matrix (All 48 Topics)
            </h2>
            <div className="weeks-matrix-container glass-panel">
              {weeks.map((w) => (
                <div key={w.week} className="week-matrix-row">
                  <div className="week-matrix-label">
                    <span className="week-num">Week {w.week}</span>
                    <span className="week-avg">{w.average_mastery_pct}% avg</span>
                  </div>
                  <div className="week-topics-chips">
                    {w.topics.map((t) => {
                      const pct = Math.round(t.effective_score * 100);
                      let statusClass = `chip-${t.status}`;
                      return (
                        <button
                          key={t.topic_id}
                          className={`matrix-topic-btn ${statusClass}`}
                          onClick={() => setSelectedTopic(t)}
                          title={`${t.topic_name}: ${pct}% mastery (${t.attempts} attempts)`}
                        >
                          <span className="btn-topic-title">{t.topic_name}</span>
                          <span className="btn-topic-score">{t.attempts > 0 ? `${pct}%` : '—'}</span>
                        </button>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Topic Detail Modal / Card if selected */}
          {selectedTopic && (
            <div className="topic-modal-overlay" onClick={() => setSelectedTopic(null)}>
              <div className="topic-modal glass-panel" onClick={e => e.stopPropagation()}>
                <div className="modal-header">
                  <div>
                    <span className="modal-week">Week {selectedTopic.week}</span>
                    <h3>{selectedTopic.topic_name}</h3>
                  </div>
                  {getStatusBadge(selectedTopic.status)}
                </div>
                <p className="modal-desc">{selectedTopic.description}</p>

                <div className="modal-stats-grid">
                  <div>
                    <label>Mastery Score</label>
                    <div className="modal-stat-val">{Math.round(selectedTopic.effective_score * 100)}%</div>
                  </div>
                  <div>
                    <label>Elo Skill Rating</label>
                    <div className="modal-stat-val">{selectedTopic.elo_rating}</div>
                  </div>
                  <div>
                    <label>Quiz Attempts</label>
                    <div className="modal-stat-val">{selectedTopic.attempts}</div>
                  </div>
                  <div>
                    <label>Chat Interactions</label>
                    <div className="modal-stat-val">{selectedTopic.chat_interactions}</div>
                  </div>
                </div>

                {selectedTopic.prerequisites && selectedTopic.prerequisites.length > 0 && (
                  <div className="modal-prereqs">
                    <strong>Prerequisites: </strong>
                    <span>Topic IDs [{selectedTopic.prerequisites.join(', ')}]</span>
                  </div>
                )}

                <div className="modal-actions">
                  <button
                    className="btn btn-primary"
                    onClick={() => {
                      setSelectedTopic(null);
                      handleStartQuiz(selectedTopic.topic_id);
                    }}
                  >
                    Take Quiz on this Topic
                  </button>
                  <button
                    className="btn btn-ghost"
                    onClick={() => {
                      setSelectedTopic(null);
                      handleAskTutor(selectedTopic.topic_name);
                    }}
                  >
                    Ask Tutor in Chat
                  </button>
                  <button className="btn btn-ghost" onClick={() => setSelectedTopic(null)}>
                    Close
                  </button>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
