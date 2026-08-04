import React, { useState, useEffect } from 'react';
import { CheckCircle, XCircle, RefreshCw, Flame, Trophy } from 'lucide-react';
import APIClient from '../api/client';
import './Quiz.css';

const STUDENT_KEY = 'mlt_student_id';

function ScoreCircle({ correct, total }) {
  const pct = total > 0 ? Math.round((correct / total) * 100) : 0;
  const color = pct >= 70 ? 'var(--success)' : pct >= 40 ? 'var(--warning)' : 'var(--danger)';
  return (
    <div className="score-ring" style={{ '--pct': pct, '--color': color }}>
      <span className="score-label">{pct}%</span>
    </div>
  );
}

export default function Quiz() {
  const [topics, setTopics] = useState([]);
  const [topicId, setTopicId] = useState('');
  const [difficulty, setDifficulty] = useState('medium');
  const [studentId, setStudentId] = useState(() => localStorage.getItem(STUDENT_KEY) || '');
  const [question, setQuestion] = useState(null);
  const [selected, setSelected] = useState(null);
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [correct, setCorrect] = useState(0);
  const [total, setTotal] = useState(0);
  const [streak, setStreak] = useState(0);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    APIClient.getTopics()
      .then(setTopics)
      .catch(() => setTopics([]));
    if (studentId) loadHistory(studentId);
  }, []);

  const loadHistory = async (sid) => {
    try {
      const h = await APIClient.getQuizHistory(sid);
      setHistory(h.slice(0, 8));
    } catch { /* ignore */ }
  };

  const generateQuestion = async () => {
    if (!topicId) return;
    setLoading(true);
    setQuestion(null);
    setSelected(null);
    setSubmitted(false);

    const topic = topics.find(t => String(t.id) === String(topicId));
    const topicName = topic?.name || 'Machine Learning';

    const options = [
      `${topicName} is a fundamental concept in the MLT course.`,
      `${topicName} has no practical applications in data science.`,
      `${topicName} is only relevant to deep learning and neural networks.`,
      `${topicName} was not covered in the IIT Madras MLT curriculum.`,
    ];

    setQuestion({
      text: `Which statement best describes "${topicName}"?`,
      options,
      correct: 0,
      explanation: `See Week ${topic?.week || '?'} lecture materials for a detailed explanation of ${topicName}.`,
      topicName,
      topicId: parseInt(topicId),
      difficulty,
    });
    setTotal(prev => prev + 1);
    setLoading(false);
  };

  const handleSubmit = async () => {
    if (selected === null) return;
    setSubmitted(true);
    const isCorrect = selected === question.correct;
    if (isCorrect) { setCorrect(prev => prev + 1); setStreak(prev => prev + 1); }
    else { setStreak(0); }

    if (studentId) {
      try {
        await APIClient.submitQuizAttempt(studentId, {
          topic_name: question.topicName,
          topic_id: question.topicId,
          difficulty: question.difficulty,
          question_text: question.text,
          student_answer: question.options[selected],
          correct_answer: question.options[question.correct],
          is_correct: isCorrect,
          source_chunks: [],
        });
        await loadHistory(studentId);
      } catch { /* ignore */ }
    }
  };

  const topicData = topics.find(t => String(t.id) === String(topicId));

  return (
    <div className="quiz-layout">
      {/* Sidebar */}
      <aside className="quiz-sidebar glass-panel">
        <div className="sidebar-section">
          <h3 className="sidebar-title">⚙️ Settings</h3>
          <div className="form-group">
            <label className="form-label">STUDENT ID</label>
            <input
              className="input"
              placeholder="e.g. student_001"
              value={studentId}
              onChange={e => { setStudentId(e.target.value); localStorage.setItem(STUDENT_KEY, e.target.value); }}
            />
          </div>
          <div className="form-group">
            <label className="form-label">TOPIC</label>
            <select className="input" value={topicId} onChange={e => setTopicId(e.target.value)}>
              <option value="">— Select a topic —</option>
              {topics.map(t => (
                <option key={t.id} value={t.id}>{t.name} (W{t.week})</option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">DIFFICULTY</label>
            <div className="difficulty-btns">
              {['easy', 'medium', 'hard'].map(d => (
                <button
                  key={d}
                  className={`diff-btn ${difficulty === d ? 'active' : ''}`}
                  onClick={() => setDifficulty(d)}
                >
                  {d.charAt(0).toUpperCase() + d.slice(1)}
                </button>
              ))}
            </div>
          </div>
          <button
            className="btn btn-primary"
            style={{ width: '100%', justifyContent: 'center' }}
            onClick={generateQuestion}
            disabled={!topicId || loading}
          >
            {loading ? <div className="spinner" style={{ width: 16, height: 16 }} /> : <RefreshCw size={16} />}
            Generate Question
          </button>
        </div>

        <div className="sidebar-section">
          <h3 className="sidebar-title">📜 Recent Attempts</h3>
          {history.length === 0 ? (
            <p className="empty-hint">No attempts yet</p>
          ) : (
            <div className="history-list">
              {history.map((h, i) => (
                <div key={i} className="history-item">
                  <span className="history-topic">{h.topic_name}</span>
                  <span className={`history-badge ${h.is_correct ? 'correct' : 'wrong'}`}>
                    {h.is_correct ? '✓' : '✕'}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </aside>

      {/* Main */}
      <main className="quiz-main">
        {/* Stats Banner */}
        <div className="stats-banner glass-panel">
          <ScoreCircle correct={correct} total={total} />
          <div className="stats-text">
            <div className="stats-value">{correct} / {total}</div>
            <div className="stats-sub">Session Score</div>
          </div>
          {streak >= 3 && (
            <div className="streak-badge">
              <Flame size={16} color="#F59E0B" />
              <span>{streak} Streak!</span>
            </div>
          )}
          {correct >= 5 && correct === total && (
            <div className="streak-badge gold">
              <Trophy size={16} color="#F59E0B" />
              <span>Perfect!</span>
            </div>
          )}
        </div>

        {/* Question Card */}
        {!question ? (
          <div className="quiz-empty glass-panel">
            <div className="empty-icon">📝</div>
            <h3>Ready to Practice?</h3>
            <p>Select a topic from the sidebar and click <strong>Generate Question</strong> to begin.</p>
            {topics.length === 0 && (
              <p className="api-warning">⚠️ Make sure the FastAPI backend is running on port 8000.</p>
            )}
          </div>
        ) : (
          <div className="question-card glass-panel animate-fade-in">
            <div className="question-meta">
              <span className="topic-tag">{question.topicName}</span>
              <span className={`diff-tag ${question.difficulty}`}>{question.difficulty}</span>
            </div>
            <h2 className="question-text">{question.text}</h2>

            <div className="options-list">
              {question.options.map((opt, i) => {
                let cls = 'option-btn';
                if (submitted) {
                  if (i === question.correct) cls += ' correct';
                  else if (i === selected) cls += ' wrong';
                } else if (selected === i) {
                  cls += ' selected';
                }
                return (
                  <button
                    key={i}
                    className={cls}
                    onClick={() => !submitted && setSelected(i)}
                    disabled={submitted}
                  >
                    <span className="opt-letter">{['A','B','C','D'][i]}</span>
                    {opt}
                  </button>
                );
              })}
            </div>

            {submitted && (
              <div className={`feedback-box animate-fade-in ${selected === question.correct ? 'correct' : 'wrong'}`}>
                {selected === question.correct ? (
                  <><CheckCircle size={18} /> <strong>Correct!</strong></>
                ) : (
                  <><XCircle size={18} /> <strong>Incorrect.</strong></>
                )}
                <p>{question.explanation}</p>
              </div>
            )}

            <div className="question-actions">
              {!submitted ? (
                <button
                  className="btn btn-primary"
                  onClick={handleSubmit}
                  disabled={selected === null}
                >
                  Submit Answer
                </button>
              ) : (
                <button className="btn btn-primary" onClick={generateQuestion}>
                  <RefreshCw size={16} /> Next Question
                </button>
              )}
              <button className="btn btn-ghost" onClick={generateQuestion}>Skip</button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
