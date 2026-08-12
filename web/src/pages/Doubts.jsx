import React, { useState, useEffect, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  Layers, Search, Flame, ChevronDown, ChevronUp, AlertTriangle,
  Copy, FileText, Loader2,
} from 'lucide-react';
import APIClient from '../api/client';
import RichText from '../components/RichText';
import './Doubts.css';

/** Cluster cards, the common-doubts strip and search results all render units, so the
 *  source badge is one component. `pq`/`PYQ` are the exam sources — worth telling apart
 *  from `faq`, which holds topic explainers rather than questions students asked. */
function SourceBadge({ source }) {
  return <span className={`qi-source-badge src-${source}`}>{source}</span>;
}

function UnitCard({ unit }) {
  const [open, setOpen] = useState(false);
  const hasDetail = Boolean(unit.answer || unit.solution || (unit.options || []).length);

  return (
    <div className="qi-unit">
      <div className="qi-unit-head">
        <SourceBadge source={unit.source_type} />
        {unit.week > 0 && <span className="qi-week-tag">Week {unit.week}</span>}
        {!unit.is_canonical && (
          <span className="qi-dup-tag" title="Folded into another phrasing of the same doubt">
            <Copy size={11} /> variant
          </span>
        )}
        {unit.origin === 'admin' && <span className="qi-origin-tag">admin-added</span>}
      </div>
      {/* Everything a unit carries can contain LaTeX — the faq units are half maths by
          volume — so title, body, options and answer all go through the same renderer
          rather than only the body that happened to be noticed first. */}
      <div className="qi-unit-title"><RichText inline>{unit.title}</RichText></div>
      <RichText className="qi-unit-text">{unit.text}</RichText>
      {hasDetail && (
        <button className="qi-link-btn" onClick={() => setOpen(!open)}>
          {open ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
          {open ? 'Hide' : 'Show'} options &amp; answer
        </button>
      )}
      {open && (
        <div className="qi-unit-detail">
          {(unit.options || []).length > 0 && (
            <ul className="qi-options">
              {unit.options.map((opt, i) => (
                <li key={i}><RichText inline>{opt}</RichText></li>
              ))}
            </ul>
          )}
          {unit.answer && (
            <div className="qi-answer">
              <strong>Answer:</strong> <RichText inline>{unit.answer}</RichText>
            </div>
          )}
          {unit.solution && <RichText className="qi-solution">{unit.solution}</RichText>}
        </div>
      )}
    </div>
  );
}

/** A cluster is collapsed until opened, and members are fetched only then — the list
 *  endpoint returns summaries, so opening 236 clusters' worth of members up front would
 *  be a lot of payload for something nobody reads. */
function ClusterCard({ cluster, autoOpen }) {
  const [open, setOpen] = useState(Boolean(autoOpen));
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!open || detail || loading) return;
    setLoading(true);
    APIClient.getCluster(cluster.cluster_id)
      .then(setDetail)
      .catch(() => setDetail({ members: [] }))
      .finally(() => setLoading(false));
  }, [open, detail, loading, cluster.cluster_id]);

  return (
    <div className={`qi-cluster ${open ? 'expanded' : ''}`} id={`cluster-${cluster.cluster_id}`}>
      <button className="qi-cluster-head" onClick={() => setOpen(!open)}>
        <div className="qi-cluster-title">
          <span className="qi-cluster-name"><RichText inline>{cluster.title}</RichText></span>
          <div className="qi-cluster-meta">
            {/* Counts are deliberately never collapsed into one "size". asked_count is how
                many times somebody asked; canonical_count is how many distinct phrasings
                survived deduplication. A cluster drawn only from past papers has no
                asked_count — its members are OCR fragments of one printed question, so
                it says how much exam material it holds and makes no claim about demand. */}
            {cluster.asked_count > 0 ? (
              <span className="qi-count" title="Times this doubt was asked in the FAQs and practice sets">
                <Flame size={12} /> {cluster.asked_count} asked
              </span>
            ) : (
              <span className="qi-count subtle" title="Extracted from past papers — not a count of how many people asked">
                {cluster.member_count} from past papers
              </span>
            )}
            <span className="qi-count subtle" title="Distinct doubts after deduplication">
              {cluster.canonical_count} distinct
            </span>
            {(cluster.sources || []).map(s => <SourceBadge key={s} source={s} />)}
            {(cluster.weeks || []).length > 0 && (
              <span className="qi-week-tag">
                {cluster.weeks.length === 1 ? `Week ${cluster.weeks[0]}`
                  : `Weeks ${Math.min(...cluster.weeks)}–${Math.max(...cluster.weeks)}`}
              </span>
            )}
          </div>
        </div>
        {open ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
      </button>

      {open && (
        <div className="qi-cluster-body">
          {loading && <div className="qi-inline-loading"><Loader2 size={14} className="spin" /> Loading members…</div>}
          {detail && (detail.members || []).length === 0 && !loading && (
            <div className="qi-empty-inline">No members could be loaded for this cluster.</div>
          )}
          {(detail?.members || []).map(u => <UnitCard key={u.unit_id} unit={u} />)}
        </div>
      )}
    </div>
  );
}

const SOURCES = ['faq', 'pq', 'PYQ'];

export default function Doubts() {
  const [searchParams, setSearchParams] = useSearchParams();
  const deepLinkCluster = searchParams.get('cluster');

  const [stats, setStats] = useState(null);
  const [doubts, setDoubts] = useState([]);
  const [clusters, setClusters] = useState([]);
  const [week, setWeek] = useState('');
  const [source, setSource] = useState('');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [searching, setSearching] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // A missing bank is a 503 naming the build command, not an empty list — an empty
  // list would read as "no duplicate questions exist", which is a different claim.
  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    Promise.all([
      APIClient.getQuestionStats(),
      APIClient.getCommonDoubts(8),
    ])
      .then(([s, d]) => {
        if (cancelled) return;
        setStats(s);
        setDoubts(d);
        setError(null);
      })
      .catch(err => { if (!cancelled) setError(err); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, []);

  const loadClusters = useCallback(() => {
    APIClient.getQuestionClusters({
      week: week === '' ? null : Number(week),
      sourceType: source || null,
      limit: 60,
    })
      .then(setClusters)
      .catch(() => setClusters([]));
  }, [week, source]);

  useEffect(() => { loadClusters(); }, [loadClusters]);

  const runSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) { setResults(null); return; }
    setSearching(true);
    try {
      setResults(await APIClient.searchQuestions(query.trim(), 12));
    } catch {
      setResults([]);
    } finally {
      setSearching(false);
    }
  };

  const clearSearch = () => { setQuery(''); setResults(null); };

  // A deep link from a chat chip should land on the cluster it names, not at the top of
  // an unfiltered list. Fetching it directly means the link works even when the current
  // week/source filters would have excluded it.
  const [linked, setLinked] = useState(null);
  useEffect(() => {
    if (!deepLinkCluster) { setLinked(null); return; }
    APIClient.getCluster(deepLinkCluster).then(setLinked).catch(() => setLinked(null));
  }, [deepLinkCluster]);

  if (loading) {
    return (
      <div className="doubts-page">
        <div className="qi-loading"><Loader2 size={22} className="spin" /> Loading the question bank…</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="doubts-page">
        <div className="qi-error-panel glass-panel">
          <AlertTriangle size={22} />
          <div>
            <h3>The question bank is not available</h3>
            <p>{error.message}</p>
            <code>python src/build_question_bank.py</code>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="doubts-page">
      <header className="qi-header">
        <div className="qi-header-title">
          <Layers size={22} color="var(--accent)" />
          <div>
            <h1>AI Question Intelligence</h1>
            <p>Common doubts from the course FAQs, practice sets and past papers — deduplicated and grouped by concept.</p>
          </div>
        </div>
        {stats && (
          <div className="qi-stat-strip">
            <div className="qi-stat"><span>{stats.unit_count}</span><label>questions</label></div>
            {/* The browsable count, not the raw one — this tile sits above the list and
                promised a number the list could never show. The raw total is in the
                tooltip rather than dropped. */}
            <div
              className="qi-stat"
              title={`${stats.cluster_count} clusters exist in total; the rest either group a single question or came out of the OCR without a readable title.`}
            >
              <span>{stats.displayable_clusters ?? stats.cluster_count}</span>
              <label>concept groups</label>
            </div>
            <div className="qi-stat">
              <span>{stats.duplicate_count}</span>
              <label>duplicates folded</label>
            </div>
            <div className="qi-stat">
              <span>{(stats.duplicate_rate * 100).toFixed(1)}%</span>
              <label>duplicate rate</label>
            </div>
            {stats.admin_authored_units > 0 && (
              <div className="qi-stat accent">
                <span>{stats.admin_authored_units}</span><label>admin-added</label>
              </div>
            )}
          </div>
        )}
      </header>

      {linked && (
        <section className="qi-section">
          <h2 className="qi-section-title">Linked from chat</h2>
          <ClusterCard cluster={linked} autoOpen />
          <button className="qi-link-btn" onClick={() => setSearchParams({})}>Clear this link</button>
        </section>
      )}

      <section className="qi-section">
        <h2 className="qi-section-title"><Flame size={15} /> Most-asked doubts</h2>
        {doubts.length === 0 ? (
          <p className="qi-empty">
            No doubt has been asked more than once yet — every question in the FAQs and
            practice sets is currently distinct. Past papers are not counted here: their
            repetition is an artefact of how the scans were split, not of demand.
          </p>
        ) : (
          <div className="qi-doubt-strip">
            {doubts.map((c, i) => (
              <button
                key={c.cluster_id}
                className="qi-doubt-card"
                onClick={() => setSearchParams({ cluster: String(c.cluster_id) })}
              >
                <span className="qi-rank">#{i + 1}</span>
                <span className="qi-doubt-title"><RichText inline>{c.title}</RichText></span>
                <span className="qi-doubt-meta">
                  {c.asked_count} asked · {(c.sources || []).join(', ')}
                </span>
              </button>
            ))}
          </div>
        )}
      </section>

      <section className="qi-section">
        <div className="qi-toolbar">
          <form className="qi-search" onSubmit={runSearch}>
            <Search size={15} />
            <input
              type="text"
              value={query}
              placeholder="Search the question bank (k-means, bias-variance, kernel…)"
              onChange={e => setQuery(e.target.value)}
            />
            <button type="submit" disabled={searching}>
              {searching ? 'Searching…' : 'Search'}
            </button>
            {results && <button type="button" className="qi-ghost-btn" onClick={clearSearch}>Clear</button>}
          </form>

          <div className="qi-filters">
            <select value={source} onChange={e => setSource(e.target.value)}>
              <option value="">All sources</option>
              {SOURCES.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
            <select value={week} onChange={e => setWeek(e.target.value)}>
              <option value="">All weeks</option>
              {Array.from({ length: 12 }, (_, i) => i + 1).map(w => (
                <option key={w} value={w}>Week {w}</option>
              ))}
            </select>
          </div>
        </div>

        {results ? (
          <>
            <h2 className="qi-section-title">
              <FileText size={15} /> {results.length} match{results.length === 1 ? '' : 'es'} for “{query}”
            </h2>
            {results.length === 0 && (
              <p className="qi-empty">
                Nothing in the question bank matched. The search runs the same retriever the
                chat uses, then maps what it finds back to parsed questions — a topic covered
                only in lecture transcripts has no question unit to return.
              </p>
            )}
            <div className="qi-unit-list">
              {results.map(u => <UnitCard key={u.unit_id} unit={u} />)}
            </div>
          </>
        ) : (
          <>
            <h2 className="qi-section-title">
              Concept groups {clusters.length > 0 && <span className="qi-muted">({clusters.length})</span>}
            </h2>
            {clusters.length === 0 && (
              <p className="qi-empty">
                No group matches these filters. Groups of a single question, and groups the
                OCR left without a readable title, are not listed — search still reaches
                every question in the bank.
              </p>
            )}
            <div className="qi-cluster-list">
              {clusters.map(c => (
                <ClusterCard
                  key={c.cluster_id}
                  cluster={c}
                  autoOpen={String(c.cluster_id) === deepLinkCluster}
                />
              ))}
            </div>
          </>
        )}
      </section>
    </div>
  );
}
