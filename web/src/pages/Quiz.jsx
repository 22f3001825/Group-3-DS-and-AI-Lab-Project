import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import {
  CheckCircle, XCircle, RefreshCw, Flame, Trophy, Target, BookOpen,
  AlertTriangle, TrendingUp, TrendingDown, Lock, Sparkles,
} from 'lucide-react';
import APIClient from '../api/client';
import './Quiz.css';

const STUDENT_KEY = 'mlt_student_id';
const BATCH_SIZE = 3;

function ScoreCircle({ correct, total }) {
  const pct = total > 0 ? Math.round((correct / total) * 100) : 0;
  const color = pct >= 70 ? 'var(--success)' : pct >= 40 ? 'var(--warning)' : 'var(--danger)';
  return (
    <div className="score-ring" style={{ '--pct': pct, '--color': color }}>
      <span className="score-label">{pct}%</span>
    </div>
  );
}

/** The visible proof of personalization: why this topic, in the system's own words.
 *  Personalized targeting draws only from topics already attempted, so there is no
 *  'diagnostic' or 'unexplored' case to render. */
function reasonText(q) {
  const blocked = (q.unmet_prerequisites || [])[0];
  const tail = blocked ? ` ${blocked} is still shaky, so expect it to come up.` : '';
  switch (q.reason) {
    case 'weak':
      return `Practising ${q.topic_name} — of the topics you have attempted, this is the weakest.${tail}`;
    case 'developing':
      return `Practising ${q.topic_name} — you are close, this should push it over the line.${tail}`;
    case 'decaying':
      return `Refresher on ${q.topic_name} — it has been a while since you last practised it.`;
    case 'cached':
      return `Revisiting an earlier question on ${q.topic_name} — the generator was unavailable, so nothing new was invented.`;
    case 'selected':
    default:
      return `You picked ${q.topic_name}.`;
  }
}

function describeError(err) {
  if (err?.code === 'personalization_not_ready') {
    const done = err.detail?.attempts_completed ?? 0;
    const need = err.detail?.required_attempts ?? 0;
    return `Your personalised quiz is not unlocked yet — ${done} of ${need} topic-quiz questions answered. Pick a topic below to keep going.`;
  }
  if (err?.status === 503) {
    return 'The question generator is unavailable right now — no LLM provider could be reached. Nothing was made up; try again in a moment.';
  }
  if (err?.status === 409) {
    return 'That question has already been answered. Move on to the next one.';
  }
  if (err?.status === 0) {
    return 'Cannot reach the API. Make sure the FastAPI backend is running on port 8000.';
  }
  return err?.message || 'Something went wrong.';
}

function SourceChip({ source }) {
  return (
    <span className="quiz-source-chip">
      <BookOpen size={12} />
      {source.label}
      {source.chunk_index !== null && source.chunk_index !== undefined && (
        <em>#{source.chunk_index}</em>
      )}
    </span>
  );
}

export default function Quiz() {
  const location = useLocation();
  const [topics, setTopics] = useState([]);
  const [topicId, setTopicId] = useState(() => location.state?.topicId || '');
  const [difficulty, setDifficulty] = useState('auto');
  const [questionType, setQuestionType] = useState('mcq');
  const [studentId, setStudentId] = useState(() => localStorage.getItem(STUDENT_KEY) || 'student_001');

  const [buffer, setBuffer] = useState([]);
  const [index, setIndex] = useState(0);
  const [lastUsedTopic, setLastUsedTopic] = useState(false);

  const [selected, setSelected] = useState(null);      // option text, not position
  const [written, setWritten] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [grading, setGrading] = useState(false);
  const [error, setError] = useState(null);

  const [correct, setCorrect] = useState(0);
  const [total, setTotal] = useState(0);
  const [streak, setStreak] = useState(0);
  const [history, setHistory] = useState([]);
  const [readiness, setReadiness] = useState(null);
  const [justUnlocked, setJustUnlocked] = useState(false);
  const deepLinkHandled = useRef(false);
  const wasReady = useRef(false);

  const question = buffer[index] || null;
  const ready = readiness?.ready ?? false;

  const loadHistory = useCallback(async (sid) => {
    try {
      const h = await APIClient.getQuizHistory(sid, { limit: 8 });
      setHistory(h);
    } catch (err) {
      setError(describeError(err));
    }
  }, []);

  /** Grading is the only thing that can move readiness, so this is called on mount
   *  and after every graded answer. */
  const loadReadiness = useCallback(async (sid) => {
    try {
      const r = await APIClient.getQuizReadiness(sid);
      setReadiness(r);
      if (r?.ready && !wasReady.current) setJustUnlocked(true);
      wasReady.current = !!r?.ready;
    } catch { /* readiness is advisory — the generate call is the real gate */ }
  }, []);

  useEffect(() => {
    APIClient.getTopics()
      .then((data) => {
        setTopics(data);
        if (location.state?.topicId) setTopicId(String(location.state.topicId));
      })
      .catch((err) => { setTopics([]); setError(describeError(err)); });
  }, [location.state]);

  useEffect(() => {
    if (!studentId) return;
    // A different student starts from their own progress, not the last one's.
    wasReady.current = false;
    setJustUnlocked(false);
    loadHistory(studentId);
    loadReadiness(studentId);
  }, [studentId, loadHistory, loadReadiness]);

  const runGenerate = async (useTopic) => {
    setLoading(true);
    setError(null);
    setResult(null);
    setSelected(null);
    setWritten('');
    setLastUsedTopic(useTopic);
    try {
      const generated = await APIClient.generateQuiz(studentId, {
        topicId: useTopic ? topicId : null,
        difficulty: difficulty === 'auto' ? null : difficulty,
        count: BATCH_SIZE,
        questionType,
      });
      if (!generated.length) throw new Error('The generator returned no usable questions.');
      setBuffer(generated);
      setIndex(0);
    } catch (err) {
      setBuffer([]);
      setError(describeError(err));
    } finally {
      setLoading(false);
    }
  };

  // Arriving from Progress's "practise this" link: quiz that topic straight away.
  useEffect(() => {
    if (!deepLinkHandled.current && location.state?.topicId && topicId && studentId) {
      deepLinkHandled.current = true;
      runGenerate(true);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location.state, topicId, studentId]);

  const handleSubmit = async () => {
    const answer = question.question_type === 'mcq' ? selected : written.trim();
    if (!answer) return;
    setGrading(true);
    setError(null);
    try {
      const graded = await APIClient.answerQuiz(studentId, question.attempt_id, answer);
      setResult(graded);
      // The session counter moves on a graded answer — not on generation, and not on skip.
      setTotal((t) => t + 1);
      if (graded.is_correct) {
        setCorrect((c) => c + 1);
        setStreak((s) => s + 1);
      } else {
        setStreak(0);
      }
      await loadHistory(studentId);
      await loadReadiness(studentId);
    } catch (err) {
      setError(describeError(err));
    } finally {
      setGrading(false);
    }
  };

  /** Walk the buffer; regenerate only when it is exhausted. */
  const handleNext = () => {
    setResult(null);
    setSelected(null);
    setWritten('');
    setError(null);
    if (index + 1 < buffer.length) {
      setIndex(index + 1);
    } else {
      runGenerate(lastUsedTopic);
    }
  };

  const masteryDelta = result?.mastery
    ? Math.round(((result.mastery.after ?? 0) - (result.mastery.before ?? 0)) * 100)
    : 0;

  const personalisedSection = (
    <div className="sidebar-section" key="personalised">
      <h3 className="sidebar-title">🎯 Personalised</h3>
      <button
        className={`btn ${ready ? 'btn-primary' : 'btn-ghost'}`}
        style={{ width: '100%', justifyContent: 'center' }}
        onClick={() => { setJustUnlocked(false); runGenerate(false); }}
        disabled={loading || !studentId || !ready}
      >
        {loading && ready
          ? <div className="spinner" style={{ width: 16, height: 16 }} />
          : ready ? <Target size={16} /> : <Lock size={16} />}
        My Personalised Quiz
      </button>

      {ready ? (
        <p className="sidebar-hint">
          Targets the weakest of the {readiness.topics_attempted} topic
          {readiness.topics_attempted === 1 ? '' : 's'} you have practised, written from the
          course material.
        </p>
      ) : (
        <>
          <div className="unlock-progress">
            <div
              className="unlock-bar"
              style={{
                '--pct': readiness
                  ? Math.min(100, Math.round((readiness.attempts_completed / Math.max(1, readiness.required_attempts)) * 100))
                  : 0,
              }}
            />
          </div>
          <p className="sidebar-hint">
            Unlocks after {readiness?.required_attempts ?? '…'} topic-quiz questions —
            {' '}<strong>{readiness?.attempts_completed ?? 0} of {readiness?.required_attempts ?? '…'}</strong> done
            {readiness?.remaining_topics > 0 && (
              <> across {readiness.required_topics} topics ({readiness.topics_attempted} so far)</>
            )}.
          </p>
        </>
      )}
    </div>
  );

  const topicSection = (
    <div className="sidebar-section" key="topic">
      <h3 className="sidebar-title">{ready ? '⚙️ Override' : '📚 Topic Quiz'}</h3>
      <div className="form-group">
        <label className="form-label">TOPIC</label>
        <select className="input" value={topicId} onChange={(e) => setTopicId(e.target.value)}>
          <option value="">— Select a topic —</option>
          {topics.map((t) => (
            <option key={t.id} value={t.id}>{t.name} (W{t.week})</option>
          ))}
        </select>
      </div>
      <div className="form-group">
        <label className="form-label">DIFFICULTY</label>
        <div className="difficulty-btns">
          {['auto', 'easy', 'medium', 'hard'].map((d) => (
            <button
              key={d}
              className={`diff-btn ${difficulty === d ? 'active' : ''}`}
              onClick={() => setDifficulty(d)}
            >
              {d === 'auto' ? 'Auto' : d.charAt(0).toUpperCase() + d.slice(1)}
            </button>
          ))}
        </div>
      </div>
      <div className="form-group">
        <label className="form-label">FORMAT</label>
        <div className="difficulty-btns">
          {[['mcq', 'Multiple choice'], ['short_answer', 'Short answer']].map(([value, label]) => (
            <button
              key={value}
              className={`diff-btn ${questionType === value ? 'active' : ''}`}
              onClick={() => setQuestionType(value)}
            >
              {label}
            </button>
          ))}
        </div>
      </div>
      <button
        className={`btn ${ready ? 'btn-ghost' : 'btn-primary'}`}
        style={{ width: '100%', justifyContent: 'center' }}
        onClick={() => runGenerate(true)}
        disabled={!topicId || loading}
      >
        {loading && !ready
          ? <div className="spinner" style={{ width: 16, height: 16 }} />
          : <RefreshCw size={16} />}
        Quiz this topic
      </button>
    </div>
  );

  return (
    <div className="quiz-layout">
      {/* Sidebar */}
      <aside className="quiz-sidebar glass-panel">
        <div className="sidebar-section">
          <h3 className="sidebar-title">👤 Student</h3>
          <div className="form-group">
            <label className="form-label">STUDENT ID</label>
            <input
              className="input"
              placeholder="e.g. student_001"
              value={studentId}
              onChange={(e) => { setStudentId(e.target.value); localStorage.setItem(STUDENT_KEY, e.target.value); }}
            />
          </div>
        </div>

        {/* Before unlocking, the topic quiz is the way in — and the way to unlock. */}
        {ready ? [personalisedSection, topicSection] : [topicSection, personalisedSection]}

        <div className="sidebar-section">
          <h3 className="sidebar-title">📜 Recent Attempts</h3>
          {history.length === 0 ? (
            <p className="empty-hint">No attempts yet</p>
          ) : (
            <div className="history-list">
              {history.map((h) => (
                <div key={h.attempt_id} className="history-item">
                  <span className="history-topic">{h.topic_name}</span>
                  <span className={`history-badge ${h.is_correct === null ? 'pending' : h.is_correct ? 'correct' : 'wrong'}`}>
                    {h.is_correct === null ? '·' : h.is_correct ? '✓' : '✕'}
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
              <Flame size={16} color="var(--warning)" />
              <span>{streak} Streak!</span>
            </div>
          )}
          {correct >= 5 && correct === total && (
            <div className="streak-badge gold">
              <Trophy size={16} color="var(--warning)" />
              <span>Perfect!</span>
            </div>
          )}
        </div>

        {justUnlocked && (
          <div className="quiz-unlocked glass-panel animate-fade-in">
            <Sparkles size={18} />
            <span>
              <strong>Personalised practice unlocked.</strong> You have practised enough for the
              system to rank your gaps — <em>My Personalised Quiz</em> now targets the weakest of
              the {readiness?.topics_attempted} topic{readiness?.topics_attempted === 1 ? '' : 's'} you
              have attempted.
            </span>
            <button className="btn btn-ghost" onClick={() => setJustUnlocked(false)}>Got it</button>
          </div>
        )}

        {error && (
          <div className="quiz-error glass-panel animate-fade-in">
            <AlertTriangle size={18} />
            <span>{error}</span>
          </div>
        )}

        {/* Question Card */}
        {!question ? (
          <div className="quiz-empty glass-panel">
            <div className="empty-icon">{ready ? '🎯' : '📚'}</div>
            <h3>Ready to Practice?</h3>
            {ready ? (
              <p>
                Hit <strong>My Personalised Quiz</strong> — the system picks the weakest of the
                topics you have practised and writes the questions from the course material.
              </p>
            ) : (
              <p>
                Pick a topic and hit <strong>Quiz this topic</strong>. After{' '}
                {readiness?.required_attempts ?? 3} answered questions,{' '}
                <strong>My Personalised Quiz</strong> unlocks and starts choosing topics for you
                from what you have practised.
              </p>
            )}
            {topics.length === 0 && (
              <p className="api-warning">⚠️ Make sure the FastAPI backend is running on port 8000.</p>
            )}
          </div>
        ) : (
          <div className="question-card glass-panel animate-fade-in">
            <div className={`reason-banner reason-${question.reason}`}>
              <Target size={14} />
              <span>{reasonText(question)}</span>
            </div>

            <div className="question-meta">
              <span className="topic-tag">{question.topic_name}</span>
              <span className={`diff-tag ${question.difficulty}`}>{question.difficulty}</span>
              {question.week > 0 && <span className="week-chip">Week {question.week}</span>}
              <span className="q-counter">{index + 1} / {buffer.length}</span>
            </div>

            <h2 className="question-text">{question.question_text}</h2>

            {question.question_type === 'mcq' ? (
              <div className="options-list">
                {question.options.map((opt, i) => {
                  let cls = 'option-btn';
                  if (result) {
                    if (opt === result.correct_answer) cls += ' correct';
                    else if (opt === selected) cls += ' wrong';
                  } else if (selected === opt) {
                    cls += ' selected';
                  }
                  return (
                    <button
                      key={opt}
                      className={cls}
                      onClick={() => !result && setSelected(opt)}
                      disabled={!!result || grading}
                    >
                      <span className="opt-letter">{['A', 'B', 'C', 'D'][i]}</span>
                      {opt}
                    </button>
                  );
                })}
              </div>
            ) : (
              <textarea
                className="input short-answer-box"
                rows={5}
                placeholder="Answer in 2-4 sentences…"
                value={written}
                onChange={(e) => setWritten(e.target.value)}
                disabled={!!result || grading}
              />
            )}

            {result && (
              <div className={`feedback-box animate-fade-in ${result.is_correct ? 'correct' : 'wrong'}`}>
                {result.is_correct ? (
                  <><CheckCircle size={18} /> <strong>Correct!</strong></>
                ) : (
                  <><XCircle size={18} /> <strong>Incorrect.</strong></>
                )}
                {question.question_type === 'short_answer' && (
                  <>
                    <span className="judge-score">Score: {Math.round((result.llm_score ?? 0) * 100)}%</span>
                    <p>{result.feedback}</p>
                    <p><strong>Reference answer:</strong> {result.correct_answer}</p>
                  </>
                )}
                <p>{result.explanation}</p>

                <div className="mastery-delta">
                  {masteryDelta >= 0 ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
                  <span>
                    {question.topic_name} mastery {Math.round((result.mastery.before ?? 0) * 100)}%
                    {' → '}
                    {Math.round((result.mastery.after ?? 0) * 100)}%
                    {' '}({masteryDelta >= 0 ? '+' : ''}{masteryDelta} pts, Elo {Math.round(result.mastery.elo ?? 0)})
                  </span>
                </div>

                {result.sources?.length > 0 && (
                  <div className="quiz-sources">
                    <span className="quiz-sources-label">Written from:</span>
                    {result.sources.map((s) => <SourceChip key={s.doc_id} source={s} />)}
                  </div>
                )}
              </div>
            )}

            <div className="question-actions">
              {!result ? (
                <button
                  className="btn btn-primary"
                  onClick={handleSubmit}
                  disabled={grading || (question.question_type === 'mcq' ? selected === null : !written.trim())}
                >
                  {grading ? <div className="spinner" style={{ width: 16, height: 16 }} /> : null}
                  Submit Answer
                </button>
              ) : (
                <button className="btn btn-primary" onClick={handleNext} disabled={loading}>
                  <RefreshCw size={16} /> Next Question
                </button>
              )}
              <button className="btn btn-ghost" onClick={handleNext} disabled={loading || grading}>
                Skip
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
