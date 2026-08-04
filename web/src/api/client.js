const API_URL = 'http://localhost:8000';

class APIClient {
  static async request(endpoint, options = {}) {
    try {
      const response = await fetch(`${API_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API Request failed:', error);
      throw error;
    }
  }

  // Chat
  static async chat(question, studentId = null) {
    return this.request('/chat', {
      method: 'POST',
      body: JSON.stringify({ question, student_id: studentId, top_k: 5 }),
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

  // Topics
  static async getTopics() {
    return this.request('/topics');
  }

  // Mastery
  static async getMastery(studentId) {
    if (!studentId) return [];
    return this.request(`/learner/${studentId}/mastery`);
  }

  // Quiz
  static async submitQuizAttempt(studentId, payload) {
    if (!studentId) return null;
    return this.request(`/learner/${studentId}/quiz`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  static async getQuizHistory(studentId) {
    if (!studentId) return [];
    return this.request(`/learner/${studentId}/quiz`);
  }
}

export default APIClient;
