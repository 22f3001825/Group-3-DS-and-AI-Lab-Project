const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/** The session JWT from POST /auth/google. It is the ONLY credential this app sends —
 *  admin calls included, since the server reads `is_admin` off the student row. */
export const TOKEN_STORAGE_KEY = 'mlt_auth_token';

/** Fired on a 401 so AuthProvider can clear the session and route to /login. */
export const UNAUTHORIZED_EVENT = 'mlt:unauthorized';

export function getToken() {
  try {
    return localStorage.getItem(TOKEN_STORAGE_KEY) || '';
  } catch {
    return '';   // strict privacy modes throw rather than returning null
  }
}

export function setToken(token) {
  try {
    if (token) localStorage.setItem(TOKEN_STORAGE_KEY, token);
    else localStorage.removeItem(TOKEN_STORAGE_KEY);
  } catch (error) {
    console.warn('Failed to persist the session token:', error);
  }
}

/* The event is deduped across a tick. Progress.jsx fires getLearnerProfile and
   getRecommendations in parallel, so an expired token produces two 401s within a
   millisecond of each other and, without this, two navigations to /login. */
let unauthorizedPending = false;

function announceUnauthorized(endpoint) {
  // Only 401, and never from /auth/* — a failed sign-in must not trigger the "your
  // session ended, sign in again" path, which would loop the login page against itself.
  if (endpoint.startsWith('/auth/')) return;
  if (unauthorizedPending) return;
  unauthorizedPending = true;
  window.dispatchEvent(new Event(UNAUTHORIZED_EVENT));
  setTimeout(() => { unauthorizedPending = false; }, 0);
}

class APIClient {
  /**
   * @param {string} endpoint
   * @param {object} options  fetch options, plus `rawBody: true` to suppress the JSON
   *   Content-Type default (FormData needs the browser to set its own multipart boundary).
   */
  static async request(endpoint, options = {}) {
    const { rawBody = false, headers: callerHeaders, ...rest } = options;

    // The merge is built AFTER the rest of the options are spread. It used to be the
    // other way round, which meant any caller passing `headers` replaced the merged
    // object wholesale and the `...options.headers` merge was dead code — so a JSON call
    // would carry its own header but lose Content-Type and 422 on the server.
    // Authorization goes in first so a caller could override it, but nothing does.
    const token = getToken();
    const headers = {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(rawBody ? {} : { 'Content-Type': 'application/json' }),
      ...callerHeaders,
    };

    let response;
    try {
      response = await fetch(`${API_URL}${endpoint}`, { ...rest, headers });
    } catch (networkError) {
      console.error('API Request failed:', networkError);
      const error = new Error('Cannot reach the API. Is the backend running on port 8000?');
      error.status = 0;
      throw error;
    }

    if (!response.ok) {
      // Callers distinguish 503 (generator unavailable) from 409 (already answered) and
      // from 409 + code "personalization_not_ready", so the status, the server's detail
      // and — when the detail is an object — its code have to survive the throw.
      let detail = '';
      try {
        const body = await response.json();
        detail = body?.detail ?? '';
      } catch { /* non-JSON error body */ }

      const isObject = detail !== null && typeof detail === 'object';
      const message = isObject ? (detail.message || `API Error: ${response.status}`) : detail;
      const error = new Error(message || `API Error: ${response.status}`);
      error.status = response.status;
      error.detail = detail;
      if (isObject && detail.code) error.code = detail.code;
      console.error('API Request failed:', error);
      // 401 means the session is gone; 403 means it is fine and this call is not allowed.
      // Signing an admin out because they touched a forbidden endpoint is the bug here.
      if (response.status === 401) announceUnauthorized(endpoint);
      throw error;
    }

    return await response.json();
  }

  // ── Auth ────────────────────────────────────────────────────────────────────

  /** Trade Google's ID token for this API's session JWT.
   *  `credential` is `credentialResponse.credential` from <GoogleLogin> — the ID token,
   *  not an OAuth access token. */
  static async loginWithGoogle(credential) {
    return this.request('/auth/google', {
      method: 'POST',
      body: JSON.stringify({ credential }),
    });
  }

  /** Who the stored token belongs to, read fresh from the server. Used to restore a
   *  session on mount, which is also how an admin demotion becomes visible. */
  static async getMe() {
    return this.request('/auth/me');
  }

  // Chat
  // `history` is short-term memory for follow-ups: recent {role, content} turns, oldest
  // first. The server trims it and condenses each answer, so send the raw turns.
  // No student id: the server takes identity from the bearer token.
  static async chat(question, sessionId = null, history = []) {
    return this.request('/chat', {
      method: 'POST',
      body: JSON.stringify({
        question,
        session_id: sessionId,
        top_k: 5,
        history,
      }),
    });
  }

  static async getChatHistory(studentId) {
    if (!studentId) return [];
    try {
      return await this.request(`/learner/${studentId}/sessions`);
    } catch {
      return [];
    }
  }

  static async getSessionMessages(sessionId) {
    if (!sessionId) return [];
    try {
      return await this.request(`/session/${sessionId}/history`);
    } catch {
      return [];
    }
  }

  // Topics & Taxonomy
  static async getTopics() {
    return this.request('/topics');
  }

  static async getTopicsByWeek(week) {
    return this.request(`/topics/week/${week}`);
  }

  // Mastery & Recommendations
  static async getMastery(studentId) {
    if (!studentId) return [];
    return this.request(`/learner/${studentId}/mastery`);
  }

  static async getRecommendations(studentId, topN = 5, forceRefresh = false) {
    if (!studentId) return null;
    return this.request(`/learner/${studentId}/recommendations?top_n=${topN}&force_refresh=${forceRefresh}`);
  }

  static async getLearnerProfile(studentId) {
    if (!studentId) return null;
    return this.request(`/learner/${studentId}/profile`);
  }

  // Quiz — two-phase: generate (no answers in the payload) then answer (graded server-side)
  static async getQuizReadiness(studentId) {
    if (!studentId) return null;
    return this.request(`/learner/${studentId}/quiz/readiness`);
  }

  static async generateQuiz(studentId, { topicId = null, difficulty = null, count = 3, questionType = 'mcq' } = {}) {
    if (!studentId) return [];
    return this.request(`/learner/${studentId}/quiz/generate`, {
      method: 'POST',
      body: JSON.stringify({
        topic_id: topicId ? parseInt(topicId, 10) : null,
        difficulty: difficulty || null,
        count,
        question_type: questionType,
      }),
    });
  }

  static async answerQuiz(studentId, attemptId, studentAnswer) {
    return this.request(`/learner/${studentId}/quiz/${attemptId}/answer`, {
      method: 'POST',
      body: JSON.stringify({ student_answer: studentAnswer }),
    });
  }

  static async getQuizHistory(studentId, { includePending = false, limit = 50 } = {}) {
    if (!studentId) return [];
    return this.request(
      `/learner/${studentId}/quiz?include_pending=${includePending}&limit=${limit}`
    );
  }

  /**
   * @deprecated Direct-write path. Use generateQuiz + answerQuiz, which also keeps the
   * answer server-side until the student commits to one.
   *
   * The server grades this itself: `payload.is_correct` is ignored, and `correct_answer`
   * is required whenever `student_answer` is sent (400 otherwise). Send `options` to have
   * the answer graded by exact match; omit them for LLM-judged short answers.
   */
  static async submitQuizAttempt(studentId, payload) {
    if (!studentId) return null;
    return this.request(`/learner/${studentId}/quiz`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  // ── Question intelligence: read side ────────────────────────────────────────
  // Signed-in students only (the Doubts page is behind login like everything else).
  // Every one of these 503s when the bank has not been built, naming the command.

  static async getQuestionStats() {
    return this.request('/questions/stats');
  }

  /** `minMemberCount` is omitted unless asked for, so the server's display policy is the
   *  one that applies — sending a default of 1 from here silently re-enabled singleton
   *  clusters no matter what the API was configured to withhold. */
  static async getQuestionClusters({ week = null, sourceType = null, minMemberCount = null, limit = 50 } = {}) {
    const params = new URLSearchParams({ limit });
    if (minMemberCount !== null) params.set('min_member_count', minMemberCount);
    if (week !== null && week !== '') params.set('week', week);
    if (sourceType) params.set('source_type', sourceType);
    return this.request(`/questions/clusters?${params}`);
  }

  static async getCluster(clusterId) {
    return this.request(`/questions/clusters/${clusterId}`);
  }

  static async getCommonDoubts(limit = 10) {
    return this.request(`/questions/common-doubts?limit=${limit}`);
  }

  static async searchQuestions(query, limit = 10) {
    return this.request(`/questions/search?q=${encodeURIComponent(query)}&limit=${limit}`);
  }

  // ── Question intelligence: admin authoring ─────────────────────────────────
  // No special header: the same bearer token carries these, and the server checks
  // `Student.is_admin` on the row rather than trusting anything the client sends.
  // Three ways to create a draft, one way to commit it. Phase A writes one draft row
  // and nothing else; commitDraft is the only call here that stores the document,
  // rebuilds the bank and queues the Qdrant work.

  /** Origin `pdf`. The ONLY multipart call — no explicit Content-Type, so the browser
   *  sets the multipart boundary itself. */
  static async extractQuestionPdf(file, metadata, allowOcr = false) {
    const form = new FormData();
    form.append('file', file);
    form.append('title', metadata.title || '');
    form.append('source_type', metadata.source_type || '');
    if (metadata.content_kind) form.append('content_kind', metadata.content_kind);
    if (metadata.week !== null && metadata.week !== undefined) form.append('week', metadata.week);
    form.append('topic_ids', (metadata.topic_ids || []).join(','));
    if (metadata.lecture_ref) form.append('lecture_ref', metadata.lecture_ref);
    if (metadata.source_note) form.append('source_note', metadata.source_note);
    form.append('allow_ocr', allowOcr ? 'true' : 'false');

    return this.request('/questions/extract', {
      method: 'POST',
      rawBody: true,
      body: form,
    });
  }

  /** Origin `paste`. */
  static async createTextDraft(markdown, metadata) {
    return this.request('/questions/drafts', {
      method: 'POST',
      body: JSON.stringify({ markdown, metadata }),
    });
  }

  /** Origin `compose`. Fields in, canonical question markdown out. */
  static async createComposedDraft(questions, metadata) {
    return this.request('/questions/drafts/compose', {
      method: 'POST',
      body: JSON.stringify({ questions, metadata }),
    });
  }

  /** Re-analyse edited text and metadata. No writes — safe to call on every edit. */
  static async previewDraft(draftId, markdown, metadata = null) {
    return this.request(`/questions/staged/${draftId}/preview`, {
      method: 'POST',
      body: JSON.stringify({ markdown, metadata }),
    });
  }

  /** Phase B. 404 unknown id, 409 already committed or stem collision without
   *  `replace`, 410 expired, 400 invalid text or metadata, 503 missing payload index. */
  static async commitDraft(draftId, markdown, metadata = null, replace = false) {
    return this.request(`/questions/staged/${draftId}/commit`, {
      method: 'POST',
      body: JSON.stringify({ markdown, metadata, replace }),
    });
  }

  static async listDrafts() {
    return this.request('/questions/staged');
  }

  static async getDraft(draftId) {
    return this.request(`/questions/staged/${draftId}`);
  }

  /** The whole rollback for Phase A. */
  static async discardDraft(draftId) {
    return this.request(`/questions/staged/${draftId}`, {
      method: 'DELETE',
    });
  }

  static async getUploads() {
    return this.request('/questions/uploads');
  }

  /** Outbox health. A relational commit succeeds even when Qdrant is unreachable, so
   *  `failed > 0` is the one thing an operator has to be able to see. */
  static async getVectorSync() {
    return this.request('/questions/sync');
  }

  /** Retry queued vector work. Idempotent; failures stay queued with their last error. */
  static async runVectorSync() {
    return this.request('/questions/sync', { method: 'POST' });
  }

  /** Full re-cluster. Cluster IDs are NOT preserved, so deep links go stale. */
  static async rebuildClusters() {
    return this.request('/questions/rebuild', { method: 'POST' });
  }

  // ── Runtime settings ────────────────────────────────────────────────────────

  /** Reranker toggle state. `endpoint_configured: false` means the server has no
   *  RERANKER_URL, so switching `enabled` on would change nothing. */
  static async getRerankerSetting() {
    return this.request('/admin/settings/reranker');
  }

  /** Turn cross-encoder reranking on or off for EVERY user. Takes effect immediately on
   *  the worker that serves this call, and within ~30s on any others. */
  static async setRerankerSetting(enabled) {
    return this.request('/admin/settings/reranker', {
      method: 'PUT',
      body: JSON.stringify({ enabled }),
    });
  }

  /** Probe the reranker's /health. Independent of the toggle — this is how you check the
   *  endpoint works BEFORE switching it on. */
  static async testReranker() {
    return this.request('/admin/settings/reranker/test', { method: 'POST' });
  }
}

export default APIClient;
