import React, { useEffect, useState } from 'react';
import { Layers, Loader2, AlertTriangle, RefreshCw } from 'lucide-react';
import APIClient from '../api/client';
import './RetrievalSettings.css';

/* Retrieval tuning, for admins only. Previously the "Retrieval" block on /admin.
 *
 * Rendered by Settings.jsx behind `student.is_admin`, and admin-gated on the server too
 * (`require_admin` on all three /admin/settings/reranker endpoints) — hiding the card is a
 * UI courtesy, not the control. It lives behind that flag rather than being fetched
 * unconditionally because the GET is admin-gated as well: a student rendering this would
 * fire a request that 403s on every visit to Settings.
 *
 * One switch today, and it is deployment-wide, not per-account: it writes
 * `app_settings.reranker_enabled`, which every worker reads. That is why the copy says
 * "every user" — an admin flipping this on their own Settings page is changing what
 * students get.
 *
 * The test probe is deliberately independent of the toggle. "Is it on" and "can we reach
 * it" are different questions, and the point is to answer the second one BEFORE the
 * first — otherwise a bad URL is discovered from a log line after every request has
 * quietly fallen back to retrieval order. */

const RetrievalSettings = () => {
  const [reranker, setReranker] = useState(null);
  const [probe, setProbe] = useState(null);      // last "Test connection" result
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const payload = await APIClient.getRerankerSetting();
        if (!cancelled) setReranker(payload);
      } catch (err) {
        if (!cancelled) setError(err.message || 'Could not load the retrieval settings.');
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, []);

  const toggleReranker = async (enabled) => {
    setBusy(true);
    setError('');
    try {
      setReranker(await APIClient.setRerankerSetting(enabled));
    } catch (err) {
      setError(err.message || 'Could not change the reranking setting.');
    } finally {
      setBusy(false);
    }
  };

  const testReranker = async () => {
    setBusy(true);
    setError('');
    try {
      setProbe(await APIClient.testReranker());
    } catch (err) {
      setError(err.message || 'Could not reach the reranker.');
    } finally {
      setBusy(false);
    }
  };

  if (loading) {
    return (
      <section className="settings-card glass-panel">
        <div className="settings-card-header">
          <Layers size={18} color="var(--accent)" />
          <h2>Retrieval</h2>
        </div>
        <p className="rr-loading"><Loader2 size={15} className="rr-spin" /> Loading retrieval settings…</p>
      </section>
    );
  }

  return (
    <section className="settings-card glass-panel">
      <div className="settings-card-header">
        <Layers size={18} color="var(--accent)" />
        <h2>Retrieval</h2>
        <span className="rr-admin-only">Admin</span>
      </div>

      {error && <p className="rr-error"><AlertTriangle size={15} /> {error}</p>}

      {!reranker && !error && <p className="setting-desc">Unavailable.</p>}

      {reranker && (
        <div className="rr-panel">
          <label className="rr-checkbox">
            <input
              type="checkbox"
              checked={reranker.enabled}
              disabled={busy || !reranker.endpoint_configured}
              onChange={e => toggleReranker(e.target.checked)}
            />
            Cross-encoder reranking
          </label>

          <p className="setting-desc">
            Re-scores retrieved chunks against the question before the model sees them.
            Applies to <strong>every user</strong>, not just you.
          </p>

          {/* An admin can otherwise flip this on, see no change, and have no way to
              learn that the server was never given an endpoint to call. */}
          {!reranker.endpoint_configured && (
            <p className="rr-warn">
              No reranker endpoint configured. Set RERANKER_URL and RERANKER_API_KEY in
              the API's environment and restart it.
            </p>
          )}

          {reranker.enabled && reranker.last_error && (
            <p className="rr-warn">
              Last call failed, so results fell back to retrieval order:
              {' '}{reranker.last_error}
            </p>
          )}

          <button
            type="button"
            className="btn btn-secondary"
            onClick={testReranker}
            disabled={busy || !reranker.endpoint_configured}
          >
            <RefreshCw size={14} /> Test connection
          </button>

          {probe && (
            <p className={probe.ok ? 'setting-desc' : 'rr-warn'}>
              {probe.ok ? 'Reachable' : 'Failed'}
              {probe.latency_ms != null ? ` · ${probe.latency_ms} ms` : ''}
              {probe.detail ? ` · ${probe.detail}` : ''}
            </p>
          )}
        </div>
      )}
    </section>
  );
};

export default RetrievalSettings;
