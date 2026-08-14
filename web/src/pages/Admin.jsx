import React, { useState, useEffect, useCallback, useRef } from 'react';
import {
  ShieldCheck, Upload, ClipboardPaste, ListPlus, FileText, Layers, RefreshCw,
  RotateCcw, Trash2, Check, AlertTriangle, Plus, X, Loader2, Info,
} from 'lucide-react';
import APIClient from '../api/client';
import { useAuth } from '../auth/auth-context';
import './Admin.css';

/* Mirrors QI_ADMIN_SOURCE_TYPES in src/config.py. The value is not cosmetic: pq/PYQ are
   ranked ahead of explanatory sources by the quiz generator, so filing prose there would
   hand it exam-material privilege. The server rejects a mismatch either way; this copy
   is only so the UI can disable the Compose tab rather than fail at submit. */
const SOURCE_KINDS = { pq: 'questions', PYQ: 'questions', faq: 'prose', notes: 'prose' };

const EMPTY_META = {
  title: '',
  source_type: 'pq',
  content_kind: null,
  week: 0,
  topic_ids: [],
  lecture_ref: '',
  source_note: '',
};

const EMPTY_QUESTION = { statement: '', options: ['', ''], answerIndex: 0, answer: '', solution: '', marks: null };

/** The metadata form — one component, all three tabs, and the review pane too.
 *  Editable at review because the preview is frequently what reveals the right value:
 *  a pq draft that parses to 0 units and reads like OCR output is a PYQ. */
function MetadataForm({ meta, onChange, topics, disabled, errorField }) {
  const [topicFilter, setTopicFilter] = useState('');

  const set = (patch) => onChange({ ...meta, ...patch });

  const toggleTopic = (id) => {
    const has = meta.topic_ids.includes(id);
    set({ topic_ids: has ? meta.topic_ids.filter(t => t !== id) : [...meta.topic_ids, id] });
  };

  const visible = topics.filter(t => {
    if (!topicFilter.trim()) return true;
    const q = topicFilter.toLowerCase();
    return t.name.toLowerCase().includes(q) || String(t.week).includes(q);
  });

  return (
    <div className="ad-meta-form">
      <div className="ad-field-row">
        <label className={`ad-field ${errorField === 'title' ? 'has-error' : ''}`}>
          <span>Title <em>required</em></span>
          <input
            className="input"
            value={meta.title}
            disabled={disabled}
            placeholder="Week 5 Practice Set"
            onChange={e => set({ title: e.target.value })}
          />
        </label>

        <label className={`ad-field ${errorField === 'source_type' ? 'has-error' : ''}`}>
          <span>Source type <em>required</em></span>
          <select
            className="input"
            value={meta.source_type}
            disabled={disabled}
            onChange={e => set({ source_type: e.target.value, content_kind: null })}
          >
            {Object.entries(SOURCE_KINDS).map(([st, kind]) => (
              <option key={st} value={st}>{st} — {kind}</option>
            ))}
          </select>
        </label>
      </div>

      <div className="ad-field-row">
        <label className={`ad-field ${errorField === 'week' ? 'has-error' : ''}`}>
          <span>Week <em>required</em></span>
          <select
            className="input"
            value={meta.week}
            disabled={disabled}
            onChange={e => set({ week: Number(e.target.value) })}
          >
            {/* 0 is a wildcard, not "unknown" — the quiz week filter treats it as
                matching every topic, so filing here makes content eligible for every
                quiz rather than none. Labelled as what it does. */}
            <option value={0}>0 — any week (matches every topic filter)</option>
            {Array.from({ length: 12 }, (_, i) => i + 1).map(w => (
              <option key={w} value={w}>Week {w}</option>
            ))}
          </select>
        </label>

        <label className="ad-field">
          <span>Lecture reference <em>optional</em></span>
          <input
            className="input"
            value={meta.lecture_ref || ''}
            disabled={disabled}
            placeholder="Week 5, Lecture 3"
            onChange={e => set({ lecture_ref: e.target.value })}
          />
        </label>
      </div>

      <div className={`ad-field ${errorField === 'topic_ids' ? 'has-error' : ''}`}>
        <span>
          Taxonomy topics <em>optional</em>
          {meta.topic_ids.length > 0 && <b className="ad-chosen">{meta.topic_ids.length} selected</b>}
        </span>
        <input
          className="input ad-topic-filter"
          value={topicFilter}
          disabled={disabled}
          placeholder="Filter 48 topics by name or week…"
          onChange={e => setTopicFilter(e.target.value)}
        />
        <div className="ad-topic-grid">
          {visible.map(t => (
            <button
              type="button"
              key={t.id}
              disabled={disabled}
              className={`ad-topic-chip ${meta.topic_ids.includes(t.id) ? 'on' : ''}`}
              onClick={() => toggleTopic(t.id)}
            >
              <span className="ad-topic-week">W{t.week}</span> {t.name}
            </button>
          ))}
          {visible.length === 0 && <span className="ad-muted">No topic matches that filter.</span>}
        </div>
      </div>

      <label className="ad-field">
        <span>Source note <em>optional</em></span>
        <input
          className="input"
          value={meta.source_note || ''}
          disabled={disabled}
          placeholder="Where this came from — recorded in the manifest, never embedded"
          onChange={e => set({ source_note: e.target.value })}
        />
      </label>
    </div>
  );
}

/** One authored question. The correct answer is picked by radio *over the option list*,
 *  which is what makes the "answer must be one of the options" rule unbreakable in the
 *  UI rather than merely validated at the API. */
function QuestionEditor({ index, question, onChange, onRemove, canRemove }) {
  const shortAnswer = question.options.length === 0;

  const setOption = (i, value) => {
    const options = [...question.options];
    options[i] = value;
    onChange({ ...question, options });
  };

  const removeOption = (i) => {
    const options = question.options.filter((_, j) => j !== i);
    const answerIndex = question.answerIndex >= options.length ? 0 : question.answerIndex;
    onChange({ ...question, options, answerIndex });
  };

  return (
    <div className="ad-question-card">
      <div className="ad-question-head">
        <strong>Question {index + 1}</strong>
        <div className="ad-question-actions">
          <button
            type="button"
            className="ad-toggle"
            onClick={() => onChange({
              ...question,
              options: shortAnswer ? ['', ''] : [],
              answer: '',
              answerIndex: 0,
            })}
          >
            {shortAnswer ? 'Make it MCQ' : 'Make it short answer'}
          </button>
          {canRemove && (
            <button type="button" className="ad-icon-btn danger" onClick={onRemove}>
              <X size={14} />
            </button>
          )}
        </div>
      </div>

      <textarea
        className="input ad-statement"
        rows={3}
        value={question.statement}
        placeholder="Statement — the question as a student reads it"
        onChange={e => onChange({ ...question, statement: e.target.value })}
      />

      {shortAnswer ? (
        <label className="ad-field">
          <span>Expected answer</span>
          <textarea
            className="input"
            rows={2}
            value={question.answer}
            placeholder="What a correct answer contains. Graded by the LLM judge, not by exact match."
            onChange={e => onChange({ ...question, answer: e.target.value })}
          />
          <small>No options means short answer — the same shape rule the grader uses.</small>
        </label>
      ) : (
        <div className="ad-options">
          <span className="ad-options-label">Options — select the correct one</span>
          {question.options.map((opt, i) => (
            <div className="ad-option-row" key={i}>
              <input
                type="radio"
                name={`answer-${index}`}
                checked={question.answerIndex === i}
                onChange={() => onChange({ ...question, answerIndex: i })}
              />
              <input
                className="input"
                value={opt}
                placeholder={`Option ${String.fromCharCode(97 + i)}`}
                onChange={e => setOption(i, e.target.value)}
              />
              {question.options.length > 2 && (
                <button type="button" className="ad-icon-btn" onClick={() => removeOption(i)}>
                  <X size={13} />
                </button>
              )}
            </div>
          ))}
          <button
            type="button"
            className="ad-inline-btn"
            onClick={() => onChange({ ...question, options: [...question.options, ''] })}
          >
            <Plus size={13} /> Add option
          </button>
        </div>
      )}

      <label className="ad-field">
        <span>Solution <em>optional but encouraged</em></span>
        <textarea
          className="input"
          rows={2}
          value={question.solution || ''}
          placeholder="Worked explanation — parsed into the bank and surfaced on the Question Bank page"
          onChange={e => onChange({ ...question, solution: e.target.value })}
        />
      </label>
    </div>
  );
}

export default function Admin() {
  // There is no token panel here any more. Reaching this page at all means RequireAdmin
  // saw `is_admin` on the signed-in student, and the same bearer token carries every
  // call below — the shared secret survives only as an ops/curl fallback on the server.
  const { student } = useAuth();
  const [topics, setTopics] = useState([]);
  const [tab, setTab] = useState('pdf');
  const [meta, setMeta] = useState(EMPTY_META);
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);

  // Phase A inputs
  const [file, setFile] = useState(null);
  const [allowOcr, setAllowOcr] = useState(false);
  const [pasted, setPasted] = useState(() => sessionStorage.getItem('mlt_admin_paste') || '');
  const [questions, setQuestions] = useState([{ ...EMPTY_QUESTION }]);

  // Review state. The working copy lives here, not on the server: losing it costs a
  // re-analysis, not a re-extraction, since original.md is on disk.
  const [draft, setDraft] = useState(null);
  const [markdown, setMarkdown] = useState('');
  const [analysedFor, setAnalysedFor] = useState(null);   // {markdown, meta} last analysed
  const [replace, setReplace] = useState(false);
  const [confirmZero, setConfirmZero] = useState(false);

  const [result, setResult] = useState(null);
  const [staged, setStaged] = useState([]);
  const [uploads, setUploads] = useState([]);
  const [sync, setSync] = useState(null);
  const [reranker, setReranker] = useState(null);
  const [probe, setProbe] = useState(null);   // last "Test connection" result
  const originalRef = useRef('');

  const kind = SOURCE_KINDS[meta.source_type] || 'prose';
  const composeAllowed = kind === 'questions';

  useEffect(() => { APIClient.getTopics().then(setTopics).catch(() => setTopics([])); }, []);

  const refreshLists = useCallback(() => {
    APIClient.listDrafts().then(setStaged).catch(() => setStaged([]));
    APIClient.getUploads().then(setUploads).catch(() => setUploads([]));
    // A commit succeeds even when Qdrant is down, which is the right trade only if the
    // resulting queue is visible somewhere other than the server log.
    APIClient.getVectorSync().then(setSync).catch(() => setSync(null));
    APIClient.getRerankerSetting().then(setReranker).catch(() => setReranker(null));
  }, []);

  useEffect(() => { refreshLists(); }, [refreshLists]);

  // Choosing a prose source type must visibly disable Compose rather than fail at submit.
  useEffect(() => {
    if (tab === 'compose' && !composeAllowed) setTab('paste');
  }, [tab, composeAllowed]);

  // The paste tab holds the only copy of something a human typed, so it survives a
  // reload until the draft is created. The other two origins have a file or a form.
  useEffect(() => { sessionStorage.setItem('mlt_admin_paste', pasted); }, [pasted]);

  const enterReview = (preview) => {
    setDraft(preview);
    setMarkdown(preview.markdown);
    originalRef.current = preview.markdown;
    setAnalysedFor({ markdown: preview.markdown, meta: JSON.stringify(meta) });
    setReplace(false);
    setConfirmZero(false);
    setResult(null);
    refreshLists();
  };

  const payloadMeta = () => ({
    ...meta,
    lecture_ref: meta.lecture_ref || null,
    source_note: meta.source_note || null,
    content_kind: meta.content_kind || null,
  });

  const guard = async (fn) => {
    setError(null);
    setBusy(true);
    try { await fn(); }
    catch (err) { setError(err); }
    finally { setBusy(false); }
  };

  const createPdfDraft = () => guard(async () => {
    if (!file) throw Object.assign(new Error('Choose a PDF first.'), { status: 400 });
    enterReview(await APIClient.extractQuestionPdf(file, payloadMeta(), allowOcr));
  });

  const createPasteDraft = () => guard(async () => {
    enterReview(await APIClient.createTextDraft(pasted, payloadMeta()));
    sessionStorage.removeItem('mlt_admin_paste');
  });

  const createComposedDraft = () => guard(async () => {
    const payload = questions.map(q => ({
      statement: q.statement,
      options: q.options.filter(o => o.trim()),
      answer: q.options.length ? (q.options[q.answerIndex] || '') : q.answer,
      solution: q.solution || null,
      marks: q.marks,
    }));
    enterReview(await APIClient.createComposedDraft(payload, payloadMeta()));
  });

  const reanalyse = () => guard(async () => {
    const preview = await APIClient.previewDraft(draft.draft_id, markdown, payloadMeta());
    setDraft(preview);
    setAnalysedFor({ markdown, meta: JSON.stringify(meta) });
    setConfirmZero(false);
  });

  const commit = () => guard(async () => {
    const out = await APIClient.commitDraft(draft.draft_id, markdown, payloadMeta(), replace);
    setResult(out);
    setDraft(null);
    setMarkdown('');
    setFile(null);
    setPasted('');
    setQuestions([{ ...EMPTY_QUESTION }]);
    setMeta(EMPTY_META);
    refreshLists();
  });

  const discard = () => guard(async () => {
    if (!window.confirm('Discard this draft? Nothing has been written yet, so this is the whole rollback.')) return;
    await APIClient.discardDraft(draft.draft_id);
    setDraft(null);
    setMarkdown('');
    refreshLists();
  });

  const resumeDraft = (draftId) => guard(async () => {
    const preview = await APIClient.getDraft(draftId);
    setMeta({
      title: preview.resolved_metadata.title,
      source_type: preview.resolved_metadata.source_type,
      content_kind: preview.resolved_metadata.content_kind,
      week: preview.resolved_metadata.week,
      topic_ids: preview.resolved_metadata.topic_ids || [],
      lecture_ref: preview.resolved_metadata.lecture_ref || '',
      source_note: '',
    });
    setDraft(preview);
    setMarkdown(preview.markdown);
    originalRef.current = preview.markdown;
    setAnalysedFor({ markdown: preview.markdown, meta: null });
  });

  const rebuild = () => guard(async () => {
    if (!window.confirm(
      'Rebuild re-clusters the whole bank. Cluster IDs are NOT preserved, so existing /doubts links go stale. Continue?'
    )) return;
    const stats = await APIClient.rebuildClusters();
    setResult({ rebuild: stats });
    refreshLists();
  });

  const retrySync = () => guard(async () => {
    setSync(await APIClient.runVectorSync());
  });

  const toggleReranker = (enabled) => guard(async () => {
    setReranker(await APIClient.setRerankerSetting(enabled));
  });

  // Separate from the toggle on purpose: an admin should be able to confirm the endpoint
  // answers before switching it on for every student.
  const testReranker = () => guard(async () => {
    setProbe(await APIClient.testReranker());
  });

  // ── Gates ─────────────────────────────────────────────────────────────────
  const analysisIsCurrent = Boolean(
    analysedFor && analysedFor.markdown === markdown && analysedFor.meta === JSON.stringify(meta)
  );
  const unitCount = draft?.unit_preview?.length ?? 0;
  const resolvedKind = draft?.resolved_metadata?.content_kind || kind;
  const zeroUnitsMatters = resolvedKind === 'questions' && unitCount === 0;
  const commitBlocked = busy || !analysisIsCurrent || (zeroUnitsMatters && !confirmZero);

  return (
    <div className="admin-page">
      <header className="ad-header">
        <div className="ad-header-title">
          <ShieldCheck size={22} color="var(--accent)" />
          <div>
            <h1>Content authoring</h1>
            <p>
              Draft → review → commit.
            </p>
          </div>
        </div>
        <span className="ad-signed-in" title={student?.email || ''}>
          <ShieldCheck size={14} /> {student?.name || student?.email}
        </span>
      </header>

      {error && (
        <div className="ad-error">
          <AlertTriangle size={16} />
          <div>
            <strong>{errorHeadline(error)}</strong>
            <p>{error.message}</p>
          </div>
          <button className="ad-icon-btn" onClick={() => setError(null)}><X size={14} /></button>
        </div>
      )}

      {result && <ResultPanel result={result} onDismiss={() => setResult(null)} />}

      {!draft ? (
        <div className="ad-create-layout">
          <section className="ad-panel">
            <div className="ad-tabs">
              <button className={tab === 'pdf' ? 'on' : ''} onClick={() => setTab('pdf')}>
                <Upload size={14} /> Upload PDF
              </button>
              <button className={tab === 'paste' ? 'on' : ''} onClick={() => setTab('paste')}>
                <ClipboardPaste size={14} /> Paste text
              </button>
              <button
                className={tab === 'compose' ? 'on' : ''}
                disabled={!composeAllowed}
                title={composeAllowed ? '' : `${meta.source_type} takes prose, not exam-shaped questions`}
                onClick={() => setTab('compose')}
              >
                <ListPlus size={14} /> Compose questions
              </button>
            </div>

            {tab === 'pdf' && (
              <div className="ad-tab-body">
                
                <input
                  type="file"
                  accept="application/pdf,.pdf"
                  className="input"
                  onChange={e => {
                    const f = e.target.files?.[0] || null;
                    setFile(f);
                    if (f && !meta.title) setMeta(m => ({ ...m, title: f.name.replace(/\.pdf$/i, '') }));
                  }}
                />
                <label className="ad-checkbox">
                  <input type="checkbox" checked={allowOcr} onChange={e => setAllowOcr(e.target.checked)} />
                  Allow OCR when the PDF has no text layer (slow — minutes on a large scan)
                </label>
                <button className="btn btn-primary" onClick={createPdfDraft} disabled={busy || !file}>
                  {busy ? <Loader2 size={15} className="spin" /> : <Upload size={15} />} Extract &amp; review
                </button>
              </div>
            )}

            {tab === 'paste' && (
              <div className="ad-tab-body">
                <p className="ad-hint">
                  A paragraph of course prose, a corrected explanation, or a recurring forum
                  doubt transcribed by hand. Not cleaned — what you write is what gets stored.
                </p>
                <textarea
                  className="input ad-paste-area"
                  rows={14}
                  value={pasted}
                  placeholder="# Heading&#10;&#10;Markdown content…"
                  onChange={e => setPasted(e.target.value)}
                />
                <div className="ad-charcount">{pasted.length.toLocaleString()} chars</div>
                <button className="btn btn-primary" onClick={createPasteDraft} disabled={busy || !pasted.trim()}>
                  {busy ? <Loader2 size={15} className="spin" /> : <FileText size={15} />} Create draft
                </button>
              </div>
            )}

            {tab === 'compose' && (
              <div className="ad-tab-body">
                <p className="ad-hint">
                  Fields in, canonical question markdown out — rendered by the same module
                  that parses it, so a composed question cannot fail to reach the bank.
                </p>
                {questions.map((q, i) => (
                  <QuestionEditor
                    key={i}
                    index={i}
                    question={q}
                    canRemove={questions.length > 1}
                    onChange={next => setQuestions(qs => qs.map((old, j) => (j === i ? next : old)))}
                    onRemove={() => setQuestions(qs => qs.filter((_, j) => j !== i))}
                  />
                ))}
                <button
                  className="ad-inline-btn"
                  onClick={() => setQuestions(qs => [...qs, { ...EMPTY_QUESTION, options: ['', ''] }])}
                >
                  <Plus size={14} /> Add question
                </button>
                <button className="btn btn-primary" onClick={createComposedDraft} disabled={busy}>
                  {busy ? <Loader2 size={15} className="spin" /> : <ListPlus size={15} />}
                  Render &amp; review
                </button>
              </div>
            )}

            <div className="ad-divider" />
            <MetadataForm
              meta={meta}
              onChange={setMeta}
              topics={topics}
              errorField={error?.code === 'bad_topic_ids' ? 'topic_ids' : fieldFromCode(error?.code)}
            />
          </section>

          <aside className="ad-side">
            <h3>Pending reviews</h3>
            {staged.length === 0 && <p className="ad-muted">Nothing pending.</p>}
            {staged.map(d => (
              <button key={d.draft_id} className="ad-staged-row" onClick={() => resumeDraft(d.draft_id)}>
                <span className={`ad-origin origin-${d.origin}`}>{d.origin}</span>
                <span className="ad-staged-title">{d.title || d.filename || d.draft_id}</span>
                <span className="ad-muted">{d.source_type} · week {d.week}</span>
              </button>
            ))}

            <div className="ad-divider" />
            <h3>Contributions</h3>
            {uploads.length === 0 && <p className="ad-muted">Nothing committed yet.</p>}
            {uploads.slice().reverse().slice(0, 8).map((u, i) => (
              <div key={i} className="ad-upload-row">
                <span className={`ad-origin origin-${u.origin}`}>{u.origin}</span>
                <span className="ad-staged-title">{u.resolved_metadata?.title || u.filename}</span>
                <span className="ad-muted">
                  {u.chunks_added} chunks · {u.units_classified} units{u.edited ? ' · edited' : ''}
                </span>
              </div>
            ))}
            <div className="ad-divider" />
            <h3>Vector sync</h3>
            {!sync && <p className="ad-muted">Unavailable.</p>}
            {sync && (
              <div className={`ad-sync ${sync.failed ? 'ad-sync-bad' : ''}`}>
                <p className="ad-muted">
                  {sync.synced} synced · {sync.pending} pending · {sync.failed} failed
                  {sync.units_pending_vectors ? ` · ${sync.units_pending_vectors} units awaiting vectors` : ''}
                </p>
                {sync.failed > 0 && (
                  <>
                    <p className="ad-warn-text">
                      Contributions are stored and browsable; their vectors are queued.
                      {sync.last_error ? ` Last error: ${sync.last_error}` : ''}
                    </p>
                    <button className="btn btn-secondary" onClick={retrySync} disabled={busy}>
                      <RefreshCw size={14} /> Retry queued vectors
                    </button>
                  </>
                )}
              </div>
            )}

            <button className="btn btn-secondary ad-rebuild" onClick={rebuild} disabled={busy}>
              <RefreshCw size={14} /> Rebuild clusters
            </button>

            <h3>Retrieval</h3>
            {!reranker && <p className="ad-muted">Unavailable.</p>}
            {reranker && (
              <div className="ad-rerank">
                <label className="ad-checkbox">
                  <input
                    type="checkbox"
                    checked={reranker.enabled}
                    disabled={busy || !reranker.endpoint_configured}
                    onChange={e => toggleReranker(e.target.checked)}
                  />
                  Cross-encoder reranking
                </label>

                <p className="ad-muted">
                  Re-scores retrieved chunks against the question before the model sees
                  them. Applies to every user, not just you.
                </p>

                {/* An admin can otherwise flip this on, see no change, and have no way to
                    learn that the server was never given an endpoint to call. */}
                {!reranker.endpoint_configured && (
                  <p className="ad-warn-text">
                    No reranker endpoint configured. Set RERANKER_URL and
                    RERANKER_API_KEY in the API's environment and restart it.
                  </p>
                )}

                {reranker.enabled && reranker.last_error && (
                  <p className="ad-warn-text">
                    Last call failed, so results fell back to retrieval order:
                    {' '}{reranker.last_error}
                  </p>
                )}

                <button
                  className="btn btn-secondary"
                  onClick={testReranker}
                  disabled={busy || !reranker.endpoint_configured}
                >
                  <RefreshCw size={14} /> Test connection
                </button>

                {probe && (
                  <p className={probe.ok ? 'ad-muted' : 'ad-warn-text'}>
                    {probe.ok ? 'Reachable' : 'Failed'}
                    {probe.latency_ms != null ? ` · ${probe.latency_ms} ms` : ''}
                    {probe.detail ? ` · ${probe.detail}` : ''}
                  </p>
                )}
              </div>
            )}
          </aside>
        </div>
      ) : (
        <div className="ad-review">
          <div className="ad-review-bar">
            <div>
              <span className={`ad-origin origin-${draft.origin}`}>{draft.origin}</span>
              <strong className="ad-review-title">
                {draft.resolved_metadata.stem} → {draft.resolved_metadata.source_type} (stored)
              </strong>
            </div>
            <div className="ad-review-actions">
              <button className="btn btn-ghost" onClick={() => { setMarkdown(originalRef.current); }}>
                <RotateCcw size={14} /> Restore original
              </button>
              <button className="btn btn-ghost danger" onClick={discard}>
                <Trash2 size={14} /> Discard
              </button>
            </div>
          </div>

          {(draft.warnings || []).map((w, i) => (
            <div className="ad-warning" key={i}><Info size={15} /> {w}</div>
          ))}

          {draft.collision?.collides && (
            <div className={`ad-warning ${draft.collision.replaceable ? '' : 'fatal'}`}>
              <AlertTriangle size={15} />
              <div>
                <strong>
                  The stem <code>{draft.resolved_metadata.stem}</code> is already taken
                  {draft.collision.existing_path ? ` by ${draft.collision.existing_path}` : ''}.
                </strong>
                {draft.collision.replaceable ? (
                  <label className="ad-checkbox">
                    <input type="checkbox" checked={replace} onChange={e => setReplace(e.target.checked)} />
                    Replace the existing file and delete its superseded vectors
                  </label>
                ) : (
                  <p>
                    That file belongs to a different source folder, so commit will be refused.
                    Replacing does not authorise overwriting another source&apos;s material — rename
                    the title instead.
                  </p>
                )}
              </div>
            </div>
          )}

          <div className="ad-review-grid">
            <div className="ad-editor-pane">
              <div className="ad-pane-head">
                <span>Draft markdown</span>
                <span className="ad-muted">{markdown.length.toLocaleString()} chars</span>
              </div>
              <textarea
                className="ad-editor"
                value={markdown}
                spellCheck={false}
                onChange={e => setMarkdown(e.target.value)}
              />
              <div className="ad-pane-foot">
                <button className="btn btn-secondary" onClick={reanalyse} disabled={busy || analysisIsCurrent}>
                  {busy ? <Loader2 size={14} className="spin" /> : <RefreshCw size={14} />}
                  {analysisIsCurrent ? 'Analysis is current' : 'Re-analyse'}
                </button>
                <button className="btn btn-primary" onClick={commit} disabled={commitBlocked}>
                  <Check size={15} /> Commit
                </button>
              </div>
              {!analysisIsCurrent && (
                <p className="ad-gate-note">
                  Commit is disabled until the current text <em>and</em> metadata have been
                  analysed — nobody commits a version they have not seen analysed.
                </p>
              )}
              {analysisIsCurrent && zeroUnitsMatters && (
                <label className="ad-checkbox warn">
                  <input type="checkbox" checked={confirmZero} onChange={e => setConfirmZero(e.target.checked)} />
                  This parses to <b>0 questions</b>. The chunks still improve retrieval, but the
                  bank gains nothing. Commit anyway.
                </label>
              )}
            </div>

            <div className="ad-analysis-pane">
              <div className="ad-resolved">
                <h4>What will actually be written</h4>
                <dl>
                  <div><dt>stem</dt><dd>{draft.resolved_metadata.stem}</dd></div>
                  <div><dt>source</dt><dd>{draft.resolved_metadata.source_type} ({draft.resolved_metadata.content_kind})</dd></div>
                  <div><dt>week</dt><dd>{draft.resolved_metadata.week}{draft.resolved_metadata.week === 0 ? ' (any)' : ''}</dd></div>
                  <div>
                    <dt>topic_tags</dt>
                    <dd>
                      {(draft.resolved_metadata.topic_tags || []).length
                        ? draft.resolved_metadata.topic_tags.join(', ')
                        : '—'}
                      {(draft.resolved_metadata.topic_ids || []).length > 0 && (
                        <em className="ad-asserted"> asserted</em>
                      )}
                    </dd>
                  </div>
                  {draft.pages != null && <div><dt>pages</dt><dd>{draft.pages}{draft.ocr_used ? ' (OCR)' : ''}</dd></div>}
                </dl>
              </div>

              <MetadataForm meta={meta} onChange={setMeta} topics={topics} />

              <div className="ad-preview-block">
                <h4>
                  <Layers size={14} /> Chunks ({draft.chunk_preview.length})
                </h4>
                <p className="ad-muted">
                  A 384-char split with 50-char overlap. A chunk that ends mid-question is a
                  question separated from its options — insert a break to fix it.
                </p>
                <div className="ad-scroll">
                  {draft.chunk_preview.map(c => (
                    <div className="ad-chunk" key={c.doc_id}>
                      <div className="ad-chunk-head">
                        <code>{c.doc_id}</code><span className="ad-muted">{c.char_count} chars</span>
                      </div>
                      <p>{c.text}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="ad-preview-block">
                <h4><FileText size={14} /> Question units ({unitCount})</h4>
                {resolvedKind === 'prose' ? (
                  <p className="ad-muted">
                    This is prose, so zero question units is the expected outcome — it
                    contributes chunks by design, not bank entries.
                  </p>
                ) : unitCount === 0 ? (
                  <p className="ad-warn-text">
                    Nothing parsed. For a PDF that means the extraction lost its heading
                    structure; for pasted text it means the markdown does not carry the
                    shape the parser needs (Compose is the answer to that).
                  </p>
                ) : (
                  <div className="ad-scroll">
                    {draft.unit_preview.map((u, i) => (
                      <div className="ad-unit" key={i}>
                        <strong>{u.title}</strong>
                        <span className="ad-muted">
                          {u.option_count > 0 ? `${u.option_count} options` : 'short answer'}
                          {u.has_answer ? ' · has answer' : ' · no answer'}
                        </span>
                        <p>{u.text}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {draft.cleaning_stats && (
                <div className="ad-preview-block">
                  <h4>Cleaning</h4>
                  <pre className="ad-stats">{JSON.stringify(draft.cleaning_stats, null, 1)}</pre>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/* 409 has two causes and they call for opposite responses — one is "someone already did
   this", the other is "confirm you mean to replace". Naming them apart matters more than
   the status code does. */
function errorHeadline(error) {
  if (error.code === 'already_committed') return 'Already committed';
  if (error.code === 'stem_collision') return 'That name is taken';
  if (error.code === 'cross_source_collision') return 'Name collides with another source';
  if (error.code === 'draft_expired') return 'Draft expired';
  if (error.code === 'missing_payload_index') return 'Missing Qdrant payload index';
  switch (error.status) {
    case 401: return 'Your session has expired';
    case 403: return 'This account is not an administrator';
    case 400: return 'Rejected';
    case 409: return 'Conflict';
    case 410: return 'Draft expired';
    case 429: return 'Too many pending reviews';
    case 503: return 'Unavailable';
    default: return 'Request failed';
  }
}

function fieldFromCode(code) {
  if (code === 'missing_title' || code === 'bad_title') return 'title';
  if (code === 'bad_source_type') return 'source_type';
  if (code === 'bad_week') return 'week';
  if (code === 'bad_topic_ids' || code === 'topic_ids_required') return 'topic_ids';
  return null;
}

function ResultPanel({ result, onDismiss }) {
  if (result.rebuild) {
    return (
      <div className="ad-result">
        <Check size={18} />
        <div>
          <strong>Rebuilt.</strong>{' '}
          {result.rebuild.unit_count} units, {result.rebuild.cluster_count} clusters,{' '}
          {result.rebuild.duplicate_count} duplicates folded.
        </div>
        <button className="ad-icon-btn" onClick={onDismiss}><X size={14} /></button>
      </div>
    );
  }
  return (
    <div className="ad-result">
      <Check size={18} />
      <div>
        <strong>
          Committed as {result.resolved_metadata?.stem} ({result.resolved_metadata?.source_type})
        </strong>
        <p>
          {result.chunks_added} chunks appended · {result.units_classified} units classified ·{' '}
          {result.duplicates_matched} matched an existing duplicate group ·{' '}
          {result.clusters_joined} joined an existing cluster · {result.clusters_created} new
          {result.edited ? ` · edited (+${result.chars_added}/−${result.chars_removed} chars)` : ''}
        </p>
        {(result.warnings || []).map((w, i) => <p key={i} className="ad-warn-text">{w}</p>)}
      </div>
      <button className="ad-icon-btn" onClick={onDismiss}><X size={14} /></button>
    </div>
  );
}
