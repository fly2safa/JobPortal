import axios, { AxiosInstance, AxiosError } from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: `${API_URL}/api/v1`,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add JWT token
    this.client.interceptors.request.use(
      (config) => {
        if (typeof window !== 'undefined') {
          const token = localStorage.getItem('access_token');
          if (token) {
            config.headers.Authorization = `Bearer ${token}`;
          }
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Token expired or invalid - logout user
          if (typeof window !== 'undefined') {
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            window.location.href = '/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async login(email: string, password: string) {
    const response = await this.client.post('/auth/login', { email, password });
    return response.data;
  }

  async register(data: { email: string; password: string; first_name: string; last_name: string; role: string }) {
    const response = await this.client.post('/auth/register', data);
    return response.data;
  }

  async getCurrentUser() {
    const response = await this.client.get('/auth/me');
    return response.data;
  }

  // Job endpoints
  async getJobs(params?: any) {
    const response = await this.client.get('/jobs', { params });
    return response.data;
  }

  async getJobById(id: string) {
    const response = await this.client.get(`/jobs/${id}`);
    return response.data;
  }

  async createJob(data: any) {
    const response = await this.client.post('/jobs', data);
    return response.data;
  }

  async updateJob(id: string, data: any) {
    const response = await this.client.put(`/jobs/${id}`, data);
    return response.data;
  }

  async deleteJob(id: string) {
    const response = await this.client.delete(`/jobs/${id}`);
    return response.data;
  }

  async getEmployerJobs(params?: any) {
    const response = await this.client.get('/jobs/employer/me', { params });
    return response.data;
  }

  // Application endpoints
  async getApplications(params?: any) {
    const response = await this.client.get('/applications/me', { params });
    return response.data;
  }

  async getApplicationStats() {
    const response = await this.client.get('/applications/me/stats');
    return response.data;
  }

  async applyToJob(data: { job_id: string; resume_url: string; cover_letter?: string }) {
    const response = await this.client.post('/applications', data);
    return response.data;
  }

  async updateApplicationStatus(id: string, status: string) {
    const response = await this.client.put(`/applications/${id}/status`, { status });
    return response.data;
  }

  async shortlistApplication(id: string) {
    const response = await this.client.post(`/applications/${id}/shortlist`);
    return response.data;
  }

  async rejectApplication(id: string, rejectionReason?: string) {
    const response = await this.client.post(`/applications/${id}/reject`, {
      rejection_reason: rejectionReason
    });
    return response.data;
  }

  async getJobApplications(jobId: string, params?: { status_filter?: string; page?: number; page_size?: number }) {
    const response = await this.client.get(`/applications/job/${jobId}`, { params });
    return response.data;
  }

  // Profile endpoints
  async getProfile() {
    const response = await this.client.get('/users/me');
    return response.data;
  }

  async updateProfile(data: any) {
    const response = await this.client.put('/users/me', data);
    return response.data;
  }

  // Resume endpoints
  async uploadResume(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    const response = await this.client.post('/resumes/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  async getResumes() {
    const response = await this.client.get('/resumes');
    return response.data;
  }

  async getResumeById(id: string) {
    const response = await this.client.get(`/resumes/${id}`);
    return response.data;
  }

  async deleteResume(id: string) {
    const response = await this.client.delete(`/resumes/${id}`);
    return response.data;
  }

  // Recommendations endpoints
  async getJobRecommendations() {
    const response = await this.client.get('/recommendations/jobs');
    return response.data;
  }

  async getCandidateRecommendations(jobId: string) {
    const response = await this.client.get(`/jobs/${jobId}/recommended-candidates`);
    return response.data;
  }

  // AI Assistant endpoints
  async sendMessage(message: string, conversationId?: string) {
    const response = await this.client.post('/assistant/chat', {
      message,
      conversation_id: conversationId,
    });
    return response.data;
  }

  // AI Assistant endpoints
  async chatWithAssistant(message: string, conversationId?: string) {
    const response = await this.client.post('/assistant/chat', {
      message,
      conversation_id: conversationId,
    });
    return response.data;
  }

  async getConversations(limit?: number) {
    const response = await this.client.get('/assistant/conversations', {
      params: { limit },
    });
    return response.data;
  }

  async getConversation(conversationId: string) {
    const response = await this.client.get(`/assistant/conversations/${conversationId}`);
    return response.data;
  }

  async deleteConversation(conversationId: string) {
    await this.client.delete(`/assistant/conversations/${conversationId}`);
  }

  async generateCoverLetter(data: {
    job_id: string;
    job_title: string;
    job_description: string;
    company_name: string;
    user_name: string;
    user_skills?: string[];
    user_experience?: string;
  }) {
    const response = await this.client.post('/assistant/generate-cover-letter', data);
    return response.data;
  }

  // Interview endpoints
  async getInterviews(params?: { 
    status_filter?: string;
    job_id?: string;
    application_id?: string;
    employer?: boolean;
    page?: number;
    page_size?: number;
  }) {
    const response = await this.client.get('/interviews', { params });
    return response.data;
  }

  async getInterviewById(id: string) {
    const response = await this.client.get(`/interviews/${id}`);
    return response.data;
  }

  async scheduleInterview(data: {
    job_id: string;
    application_id: string;
    scheduled_time: string;
    duration_minutes: number;
    interview_type?: string;
    meeting_link?: string;
    meeting_location?: string;
    meeting_instructions?: string;
    notes?: string;
  }) {
    const response = await this.client.post('/interviews', data);
    return response.data;
  }

  async updateInterview(id: string, data: {
    scheduled_time?: string;
    duration_minutes?: number;
    interview_type?: string;
    meeting_link?: string;
    meeting_location?: string;
    meeting_instructions?: string;
    notes?: string;
    status?: string;
    feedback?: string;
    interviewer_notes?: string;
  }) {
    const response = await this.client.put(`/interviews/${id}`, data);
    return response.data;
  }

  async rescheduleInterview(id: string, data: {
    scheduled_time: string;
    reason?: string;
  }) {
    const response = await this.client.post(`/interviews/${id}/reschedule`, data);
    return response.data;
  }

  async cancelInterview(id: string, reason?: string) {
    const response = await this.client.post(`/interviews/${id}/cancel`, {
      reason
    });
    return response.data;
  }

  async completeInterview(id: string, data: {
    feedback?: string;
    interviewer_notes?: string;
  }) {
    const response = await this.client.post(`/interviews/${id}/complete`, data);
    return response.data;
  }
}

export const apiClient = new ApiClient();
export default apiClient;

