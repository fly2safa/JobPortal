export const BRAND_COLORS = {
  primary: '#075299',
  primaryLight: '#3387CF',
  primaryDark: '#04315B',
  white: '#FFFFFF',
} as const;

export const JOB_TYPES = [
  { value: 'full_time', label: 'Full Time' },
  { value: 'part_time', label: 'Part Time' },
  { value: 'contract', label: 'Contract' },
  { value: 'internship', label: 'Internship' },
  { value: 'temporary', label: 'Temporary' },
] as const;

export const EXPERIENCE_LEVELS = [
  { value: 'entry', label: 'Entry Level' },
  { value: 'mid', label: 'Mid Level' },
  { value: 'senior', label: 'Senior Level' },
  { value: 'lead', label: 'Lead/Principal' },
] as const;

export const APPLICATION_STATUS = {
  pending: { label: 'Pending', color: 'bg-yellow-100 text-yellow-800' },
  reviewing: { label: 'Reviewing', color: 'bg-blue-100 text-blue-800' },
  shortlisted: { label: 'Shortlisted', color: 'bg-green-100 text-green-800' },
  interview: { label: 'Interview', color: 'bg-blue-100 text-blue-800' },
  rejected: { label: 'Rejected', color: 'bg-red-100 text-red-800' },
  accepted: { label: 'Accepted', color: 'bg-purple-100 text-purple-800' },
  withdrawn: { label: 'Withdrawn', color: 'bg-gray-200 text-gray-700' },
} as const;

export const POPULAR_SKILLS = [
  'JavaScript',
  'TypeScript',
  'React',
  'Node.js',
  'Python',
  'Java',
  'SQL',
  'AWS',
  'Docker',
  'Kubernetes',
  'MongoDB',
  'PostgreSQL',
  'GraphQL',
  'REST API',
  'Git',
  'CI/CD',
  'Agile',
  'TDD',
] as const;

export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  JOBS: '/jobs',
  JOB_DETAIL: '/jobs/[id]',
  DASHBOARD: '/dashboard',
  PROFILE: '/dashboard/profile',
  APPLICATIONS: '/dashboard/applications',
  RECOMMENDATIONS: '/dashboard/recommendations',
  ASSISTANT: '/dashboard/assistant',
  INTERVIEWS: '/dashboard/interviews',
  EMPLOYER_DASHBOARD: '/employer/dashboard',
  EMPLOYER_JOBS: '/employer/jobs',
  EMPLOYER_NEW_JOB: '/employer/jobs/new',
  EMPLOYER_APPLICATIONS: '/employer/jobs/[id]/applications',
  EMPLOYER_INTERVIEWS: '/employer/interviews',
} as const;

