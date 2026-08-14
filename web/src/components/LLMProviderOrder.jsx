import React, { useCallback, useEffect, useRef, useState } from 'react';
import {
  Cpu, GripVertical, ChevronUp, ChevronDown, Loader2, AlertTriangle, Check, RotateCcw,
} from 'lucide-react';
import APIClient from '../api/client';
import './LLMProviderOrder.css';

/* The LLM failover hierarchy, for admins only.
 *
 * Rendered by Settings.jsx behind `student.is_admin`, and admin-gated on the server too —
 * hiding the card is a UI courtesy, `require_admin` is the actual control.
 *
 * Two ways to reorder, deliberately: drag for speed, and the arrow buttons because a
 * keyboard or a touch screen cannot use HTML5 drag-and-drop at all. Both drive the same
 * `move()`, so there is one reordering rule to reason about.
 *
 * Nothing is saved until Save is pressed. Reordering a live failover chain is not a
 * preview-able change — every intermediate order an autosave wrote would briefly be the
 * one real users' requests followed. */

/** Formats the server's ISO timestamp; a never-saved setting has none. */
function formatWhen(value) {
  if (!value) return null;
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return null;
  return date.toLocaleString(undefined, {
    year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit',
  });
}

const sameOrder = (a, b) => a.length === b.length && a.every((id, i) => id === b[i]);

const LLMProviderOrder = () => {
  const [providers, setProviders] = useState([]);   // working copy, in display order
  const [savedOrder, setSavedOrder] = useState([]); // what the server last confirmed
  const [meta, setMeta] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [savedNote, setSavedNote] = useState('');
  const [dragIndex, setDragIndex] = useState(null);

  // Announced to screen readers after a move — the visual cue is a row changing place,
  // which a screen reader user gets nothing from.
  const [liveMessage, setLiveMessage] = useState('');
  const noteTimer = useRef(null);

  const applyPayload = useCallback((payload) => {
    // `providers` arrives in hierarchy order, so the server's order and the rendered list
    // cannot disagree about what "first" means.
    setProviders(payload.providers || []);
    setSavedOrder(payload.order || []);
    setMeta(payload);
  }, []);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const payload = await APIClient.getLLMProviderOrder();
        if (!cancelled) applyPayload(payload);
      } catch (err) {
        if (!cancelled) setError(err.message || 'Could not load the provider order.');
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, [applyPayload]);

  useEffect(() => () => clearTimeout(noteTimer.current), []);

  const move = (from, to) => {
    if (to < 0 || to >= providers.length || from === to) return;
    const next = [...providers];
    const [row] = next.splice(from, 1);
    next.splice(to, 0, row);
    setProviders(next);
    setSavedNote('');
    setLiveMessage(`${row.label} moved to position ${to + 1} of ${next.length}.`);
  };

  const currentOrder = providers.map(p => p.id);
  const dirty = savedOrder.length > 0 && !sameOrder(currentOrder, savedOrder);

  const save = async () => {
    setSaving(true);
    setError('');
    try {
      const payload = await APIClient.setLLMProviderOrder(currentOrder);
      applyPayload(payload);
      setSavedNote('Saved. Every new request follows this order.');
      clearTimeout(noteTimer.current);
      noteTimer.current = setTimeout(() => setSavedNote(''), 6000);
    } catch (err) {
      setError(err.message || 'Could not save the provider order.');
    } finally {
      setSaving(false);
    }
  };

  const reset = () => {
    // Re-derive from the working copy rather than refetching: savedOrder and providers
    // came from the same payload, so this restores exactly what the server confirmed.
    const byId = Object.fromEntries(providers.map(p => [p.id, p]));
    setProviders(savedOrder.map(id => byId[id]).filter(Boolean));
    setSavedNote('');
    setError('');
  };

  if (loading) {
    return (
      <section className="settings-card glass-panel">
        <div className="settings-card-header">
          <Cpu size={18} color="var(--accent)" />
          <h2>LLM providers</h2>
        </div>
        <p className="llm-loading"><Loader2 size={15} className="llm-spin" /> Loading the provider hierarchy…</p>
      </section>
    );
  }

  const updatedWhen = formatWhen(meta?.updated_at);

  return (
    <section className="settings-card glass-panel">
      <div className="settings-card-header">
        <Cpu size={18} color="var(--accent)" />
        <h2>LLM providers</h2>
        <span className="llm-admin-only">Admin</span>
      </div>

      <p className="setting-desc llm-intro">
        The order every answer is generated in: the first provider that responds wins, and the
        next one down is tried when it is rate-limited, unauthorized or unreachable. This applies
        to <strong>all users</strong>. An answer already being generated finishes on the provider
        it started with — the new order takes effect from the next request.
      </p>

      {error && (
        <p className="llm-error"><AlertTriangle size={15} /> {error}</p>
      )}

      <ol className="llm-list">
        {providers.map((provider, index) => (
          <li
            key={provider.id}
            className={`llm-row ${dragIndex === index ? 'dragging' : ''} ${provider.configured ? '' : 'unconfigured'}`}
            draggable
            onDragStart={(e) => {
              setDragIndex(index);
              e.dataTransfer.effectAllowed = 'move';
              // Firefox ignores a drag that sets no data.
              e.dataTransfer.setData('text/plain', provider.id);
            }}
            onDragOver={(e) => {
              e.preventDefault();          // without this the drop never fires
              e.dataTransfer.dropEffect = 'move';
              if (dragIndex !== null && dragIndex !== index) {
                move(dragIndex, index);
                setDragIndex(index);       // the dragged row is now here
              }
            }}
            onDragEnd={() => setDragIndex(null)}
            onDrop={(e) => { e.preventDefault(); setDragIndex(null); }}
          >
            <GripVertical size={16} className="llm-grip" aria-hidden="true" />
            <span className="llm-rank">{index + 1}</span>

            <div className="llm-copy">
              <span className="llm-name">
                {provider.label}
                {index === 0 && <b className="llm-chip llm-chip-primary">Primary</b>}
                {!provider.configured && (
                  <b className="llm-chip llm-chip-warn">
                    <AlertTriangle size={11} /> Not configured
                  </b>
                )}
              </span>
              <span className="llm-detail">
                {provider.configured
                  ? `${provider.key_count} key${provider.key_count === 1 ? '' : 's'} · ${(provider.models || []).join(', ')}`
                  /* Ranking a provider with no key is allowed — it is how a deployment
                     prepares for a key it is about to add — so this says what is missing
                     rather than blocking the save. */
                  : `Skipped until ${provider.config_hint} is set`}
              </span>
            </div>

            <div className="llm-move">
              <button
                type="button"
                className="llm-move-btn"
                aria-label={`Move ${provider.label} up`}
                disabled={index === 0}
                onClick={() => move(index, index - 1)}
              >
                <ChevronUp size={15} />
              </button>
              <button
                type="button"
                className="llm-move-btn"
                aria-label={`Move ${provider.label} down`}
                disabled={index === providers.length - 1}
                onClick={() => move(index, index + 1)}
              >
                <ChevronDown size={15} />
              </button>
            </div>
          </li>
        ))}
      </ol>

      <p className="llm-live" role="status" aria-live="polite">{liveMessage}</p>

      <div className="llm-actions">
        <button
          type="button"
          className="btn btn-primary"
          disabled={!dirty || saving}
          onClick={save}
        >
          {saving ? <><Loader2 size={15} className="llm-spin" /> Saving…</> : <><Check size={15} /> Save order</>}
        </button>
        <button type="button" className="btn btn-ghost" disabled={!dirty || saving} onClick={reset}>
          <RotateCcw size={14} /> Reset
        </button>

        <span className="llm-status">
          {savedNote && <span className="llm-saved"><Check size={13} /> {savedNote}</span>}
          {!savedNote && dirty && <span className="llm-dirty">Unsaved changes</span>}
          {!savedNote && !dirty && meta?.source === 'admin' && updatedWhen && (
            <>Set by {meta.updated_by || 'an admin'} · {updatedWhen}</>
          )}
          {!savedNote && !dirty && meta?.source === 'environment' && (
            <>Following <code>LLM_PROVIDER={meta.env_default}</code> — saving here overrides it.</>
          )}
        </span>
      </div>
    </section>
  );
};

export default LLMProviderOrder;
