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
          // Token expired or invalid
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

  async register(data: { email: string; password: string; full_name: string; role: string }) {
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

  // Application endpoints
  async getApplications(params?: any) {
    const response = await this.client.get('/applications', { params });
    return response.data;
  }

  async applyToJob(data: { job_id: string; resume_url: string; cover_letter?: string }) {
    const response = await this.client.post('/applications', data);
    return response.data;
  }

  async updateApplicationStatus(id: string, status: string) {
    const response = await this.client.patch(`/applications/${id}/status`, { status });
    return response.data;
  }

  async getJobApplications(jobId: string) {
    const response = await this.client.get(`/jobs/${jobId}/applications`);
    return response.data;
  }

  // Profile endpoints
  async getProfile() {
    const response = await this.client.get('/users/profile');
    return response.data;
  }

  async updateProfile(data: any) {
    const response = await this.client.put('/users/profile', data);
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

  async generateCoverLetter(jobId: string) {
    const response = await this.client.post('/assistant/generate-cover-letter', { job_id: jobId });
    return response.data;
  }

  // Interview endpoints
  async getInterviews(params?: any) {
    const response = await this.client.get('/interviews', { params });
    return response.data;
  }

  async scheduleInterview(data: any) {
    const response = await this.client.post('/interviews', data);
    return response.data;
  }

  async updateInterview(id: string, data: any) {
    const response = await this.client.put(`/interviews/${id}`, data);
    return response.data;
  }
}

export const apiClient = new ApiClient();
export default apiClient;

