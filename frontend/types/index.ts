// User Types
export interface User {
  id: string;
  email: string;
  full_name: string;
  role: 'job_seeker' | 'employer';
  profile?: JobSeekerProfile | EmployerProfile;
  created_at: string;
}

export interface JobSeekerProfile {
  phone?: string;
  location?: string;
  skills?: string[];
  experience_years?: number;
  education?: string;
  bio?: string;
  resume_url?: string;
}

export interface EmployerProfile {
  company_name: string;
  company_website?: string;
  company_size?: string;
  industry?: string;
  description?: string;
  logo_url?: string;
}

// Job Types
export interface Job {
  id: string;
  title: string;
  description: string;
  company_id: string;
  company_name?: string;
  location: string;
  job_type: 'full-time' | 'part-time' | 'contract' | 'internship';
  experience_level: 'entry' | 'mid' | 'senior' | 'lead';
  salary_min?: number;
  salary_max?: number;
  skills: string[];
  requirements: string[];
  benefits?: string[];
  status: 'active' | 'closed' | 'draft';
  posted_date: string;
  deadline?: string;
}

// Application Types
export interface Application {
  id: string;
  job_id: string;
  job_title?: string;
  company_name?: string;
  user_id: string;
  resume_url: string;
  cover_letter?: string;
  status: 'pending' | 'reviewing' | 'shortlisted' | 'rejected' | 'accepted';
  applied_date: string;
  updated_at: string;
}

// Resume Types
export interface Resume {
  id: string;
  user_id: string;
  file_url: string;
  file_name: string;
  file_size: number;
  
  // Parsed data
  parsed_text?: string;
  skills_extracted: string[];
  experience_years?: number;
  education?: string;
  work_experience?: string;
  summary?: string;
  
  // Parsing metadata
  parsing_method: 'algorithmic' | 'hybrid' | 'ai';
  parsing_confidence: number;
  ai_used: boolean;
  
  // Timestamps
  created_at: string;
  updated_at: string;
}

export interface ResumeUploadResponse {
  resume: Resume;
  message: string;
  skills_synced: boolean;
}

// Interview Types
export interface Interview {
  id: string;
  job_id: string;
  application_id: string;
  candidate_name?: string;
  scheduled_time: string;
  duration_minutes: number;
  meeting_link?: string;
  status: 'scheduled' | 'completed' | 'cancelled';
  notes?: string;
}

// Recommendation Types
export interface JobRecommendation {
  job: Job;
  match_score: number;
  reasons: string[];
}

export interface CandidateRecommendation {
  user_id: string;
  application_id: string;
  candidate_name: string;
  match_score: number;
  skills_match: string[];
  resume_url: string;
}

// Chat/Assistant Types
export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface Conversation {
  id: string;
  user_id: string;
  messages: Message[];
  created_date: string;
}

// Auth Types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
  role: 'job_seeker' | 'employer';
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// API Response Types
export interface ApiResponse<T> {
  data?: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// Form Types
export interface JobSearchFilters {
  query?: string;
  location?: string;
  job_type?: string[];
  experience_level?: string[];
  skills?: string[];
  salary_min?: number;
  salary_max?: number;
}

