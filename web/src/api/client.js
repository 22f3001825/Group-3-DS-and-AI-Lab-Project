const API_URL = 'http://localhost:8000';

class APIClient {
  static async request(endpoint, options = {}) {
    let response;
    try {
      response = await fetch(`${API_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });
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
  static async chat(question, studentId = null, sessionId = null) {
    return this.request('/chat', {
      method: 'POST',
      body: JSON.stringify({ question, student_id: studentId, session_id: sessionId, top_k: 5 }),
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
}

export default APIClient;
