// User Types
export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'job_seeker' | 'employer';
  // Profile fields are directly on user object (not nested in profile)
  phone?: string;
  location?: string;
  skills?: string[];
  experience_years?: number;
  education?: string;
  bio?: string;
  linkedin_url?: string;
  portfolio_url?: string;
  company_id?: string;
  job_title?: string;
  is_active?: boolean;
  is_verified?: boolean;
  created_at: string;
  updated_at?: string;
  last_login?: string;
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
  requirements?: string;  // String format from backend
  responsibilities?: string;
  
  skills: string[];
  required_skills?: string[];
  preferred_skills?: string[];
  
  location: string;
  is_remote: boolean;
  
  company_id: string;
  company_name: string;
  employer_id: string;
  
  salary_min?: number;
  salary_max?: number;
  salary_currency?: string;
  
  job_type: 'full_time' | 'part_time' | 'contract' | 'internship' | 'temporary';
  experience_level: 'entry' | 'junior' | 'mid' | 'senior' | 'lead' | 'executive';
  experience_years_min?: number;
  experience_years_max?: number;
  
  status: 'draft' | 'active' | 'closed' | 'archived';
  posted_date?: string;
  closing_date?: string;
  
  application_count: number;
  view_count: number;
  
  benefits?: string[];
  application_instructions?: string;
  
  created_at: string;
  updated_at: string;
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
  first_name: string;
  last_name: string;
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

