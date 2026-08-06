const API_URL = 'http://localhost:8000';

/** Where the admin's shared secret lives. Its presence is also what makes the /admin
 *  link render in the navbar, so ordinary students never see the route. */
const ADMIN_TOKEN_KEY = 'mlt_admin_token';

export function getAdminToken() {
  return localStorage.getItem(ADMIN_TOKEN_KEY) || '';
}

export function setAdminToken(token) {
  if (token) localStorage.setItem(ADMIN_TOKEN_KEY, token);
  else localStorage.removeItem(ADMIN_TOKEN_KEY);
}

/** Headers for an admin JSON call. Every admin endpoint needs BOTH X-Admin-Token and
 *  Content-Type: application/json — the combination the old spread order silently broke. */
function adminJson() {
  return { 'X-Admin-Token': getAdminToken() };
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
    // object wholesale and the `...options.headers` merge was dead code — so an admin
    // JSON call would carry X-Admin-Token but lose Content-Type and 422 on the server.
    const headers = { ...(rawBody ? {} : { 'Content-Type': 'application/json' }), ...callerHeaders };

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
      throw error;
    }

    return await response.json();
  }

  // Chat
  // `history` is short-term memory for follow-ups: recent {role, content} turns, oldest
  // first. The server trims it and condenses each answer, so send the raw turns.
  static async chat(question, studentId = null, sessionId = null, history = []) {
    return this.request('/chat', {
      method: 'POST',
      body: JSON.stringify({
        question,
        student_id: studentId,
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

  // ── Question intelligence: read side (open, no token) ───────────────────────
  // Every one of these 503s when the bank has not been built, naming the command.

  static async getQuestionStats() {
    return this.request('/questions/stats');
  }

  static async getQuestionClusters({ week = null, sourceType = null, minMemberCount = 1, limit = 50 } = {}) {
    const params = new URLSearchParams({ min_member_count: minMemberCount, limit });
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

  // ── Question intelligence: admin authoring (X-Admin-Token on all of these) ──
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
      headers: adminJson(),
      body: form,
    });
  }

  /** Origin `paste`. */
  static async createTextDraft(markdown, metadata) {
    return this.request('/questions/drafts', {
      method: 'POST',
      headers: adminJson(),
      body: JSON.stringify({ markdown, metadata }),
    });
  }

  /** Origin `compose`. Fields in, canonical question markdown out. */
  static async createComposedDraft(questions, metadata) {
    return this.request('/questions/drafts/compose', {
      method: 'POST',
      headers: adminJson(),
      body: JSON.stringify({ questions, metadata }),
    });
  }

  /** Re-analyse edited text and metadata. No writes — safe to call on every edit. */
  static async previewDraft(draftId, markdown, metadata = null) {
    return this.request(`/questions/staged/${draftId}/preview`, {
      method: 'POST',
      headers: adminJson(),
      body: JSON.stringify({ markdown, metadata }),
    });
  }

  /** Phase B. 404 unknown id, 409 already committed or stem collision without
   *  `replace`, 410 expired, 400 invalid text or metadata, 503 missing payload index. */
  static async commitDraft(draftId, markdown, metadata = null, replace = false) {
    return this.request(`/questions/staged/${draftId}/commit`, {
      method: 'POST',
      headers: adminJson(),
      body: JSON.stringify({ markdown, metadata, replace }),
    });
  }

  static async listDrafts() {
    return this.request('/questions/staged', { headers: adminJson() });
  }

  static async getDraft(draftId) {
    return this.request(`/questions/staged/${draftId}`, { headers: adminJson() });
  }

  /** The whole rollback for Phase A. */
  static async discardDraft(draftId) {
    return this.request(`/questions/staged/${draftId}`, {
      method: 'DELETE',
      headers: adminJson(),
    });
  }

  static async getUploads() {
    return this.request('/questions/uploads', { headers: adminJson() });
  }

  /** Outbox health. A relational commit succeeds even when Qdrant is unreachable, so
   *  `failed > 0` is the one thing an operator has to be able to see. */
  static async getVectorSync() {
    return this.request('/questions/sync', { headers: adminJson() });
  }

  /** Retry queued vector work. Idempotent; failures stay queued with their last error. */
  static async runVectorSync() {
    return this.request('/questions/sync', { method: 'POST', headers: adminJson() });
  }

  /** Full re-cluster. Cluster IDs are NOT preserved, so deep links go stale. */
  static async rebuildClusters() {
    return this.request('/questions/rebuild', { method: 'POST', headers: adminJson() });
  }
}

export default APIClient;
