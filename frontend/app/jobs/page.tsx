'use client';

import { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { JobCard } from '@/features/jobs/JobCard';
import { JobFilters } from '@/features/jobs/JobFilters';
import { useDebounce } from '@/hooks/useDebounce';
import apiClient from '@/lib/api';
import { Job } from '@/types';
import { Loader2 } from 'lucide-react';

export default function JobsPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filters, setFilters] = useState({
    query: '',
    location: '',
    job_type: '',
    experience_level: '',
  });

  const debouncedFilters = useDebounce(filters, 500);

  useEffect(() => {
    fetchJobs();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [debouncedFilters]);

  const fetchJobs = async () => {
    setIsLoading(true);
    try {
      const params: any = {};
      if (debouncedFilters.query) params.query = debouncedFilters.query;
      if (debouncedFilters.location) params.location = debouncedFilters.location;
      if (debouncedFilters.job_type) params.job_type = debouncedFilters.job_type;
      if (debouncedFilters.experience_level) params.experience_level = debouncedFilters.experience_level;

      const response = await apiClient.getJobs(params);
      setJobs(response.jobs || []);
    } catch (error) {
      console.error('Failed to fetch jobs:', error);
      // Show mock data for demo
      setJobs(getMockJobs());
    } finally {
      setIsLoading(false);
    }
  };

  const handleFilterChange = (name: string, value: string) => {
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  const handleClearFilters = () => {
    setFilters({
      query: '',
      location: '',
      job_type: '',
      experience_level: '',
    });
  };

  return (
    <div className="min-h-screen" style={{
      background: 'linear-gradient(135deg, #075299 0%, #5a9ab3 100%)'
    }}>
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-white mb-2" style={{ fontFamily: 'Playfair Display, serif' }}>Your Gateway to Meaningful Careers and Exceptional Talent</h1>
          <p className="text-white/90">Browse Thousands Of Job Opportunities From Top Companies</p>
        </div>

        <JobFilters
          filters={filters}
          onFilterChange={handleFilterChange}
          onClearFilters={handleClearFilters}
        />

        {isLoading ? (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="animate-spin text-primary" size={48} />
          </div>
        ) : jobs.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-gray-600 text-lg">No jobs found. Try adjusting your filters.</p>
          </div>
        ) : (
          <>
            <div className="mb-4 text-sm text-white">
              Showing {jobs.length} Job{jobs.length !== 1 ? 's' : ''}
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {jobs.map((job) => (
                <JobCard key={job.id} job={job} />
              ))}
            </div>
          </>
        )}
      </div>

      <Footer />
    </div>
  );
}

// Mock data for demo purposes
function getMockJobs(): Job[] {
  return [
    {
      id: '1',
      title: 'Senior Frontend Developer',
      description: 'We are looking for an experienced frontend developer to join our team. You will be responsible for building scalable web applications using React and TypeScript.',
      company_id: 'company-1',
      company_name: 'TechCorp Inc.',
      location: 'San Francisco, CA',
      job_type: 'full_time',
      experience_level: 'senior',
      salary_min: 120000,
      salary_max: 180000,
      skills: ['React', 'TypeScript', 'Next.js', 'Tailwind CSS'],
      requirements: '• 5+ years of experience\n• Strong React skills\n• TypeScript proficiency',
      is_remote: false,
      employer_id: 'employer-1',
      application_count: 15,
      view_count: 234,
      status: 'active',
      posted_date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
      created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
      updated_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
      id: '2',
      title: 'Full Stack Engineer',
      description: 'Join our startup as a full stack engineer. Work on cutting-edge technologies and help shape the future of our product.',
      company_id: 'company-2',
      company_name: 'StartupXYZ',
      location: 'Remote',
      job_type: 'full_time',
      experience_level: 'mid',
      salary_min: 90000,
      salary_max: 140000,
      skills: ['Node.js', 'React', 'MongoDB', 'AWS'],
      requirements: '• 3+ years of experience\n• Full stack expertise',
      is_remote: true,
      employer_id: 'employer-2',
      application_count: 23,
      view_count: 412,
      status: 'active',
      posted_date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
      created_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
      updated_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
      id: '3',
      title: 'Product Designer',
      description: 'We need a creative product designer to create beautiful and intuitive user experiences for our SaaS platform.',
      company_id: 'company-3',
      company_name: 'DesignCo',
      location: 'New York, NY',
      job_type: 'full_time',
      experience_level: 'mid',
      salary_min: 80000,
      salary_max: 120000,
      skills: ['Figma', 'UI/UX', 'Prototyping', 'Design Systems'],
      requirements: '• 3+ years of product design experience\n• Strong portfolio',
      is_remote: false,
      employer_id: 'employer-3',
      application_count: 31,
      view_count: 189,
      status: 'active',
      posted_date: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
      created_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
      updated_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
      id: '4',
      title: 'DevOps Engineer',
      description: 'Looking for a DevOps engineer to manage our cloud infrastructure and CI/CD pipelines.',
      company_id: 'company-4',
      company_name: 'CloudSystems',
      location: 'Austin, TX',
      job_type: 'full_time',
      experience_level: 'senior',
      salary_min: 130000,
      salary_max: 170000,
      skills: ['AWS', 'Docker', 'Kubernetes', 'Terraform', 'CI/CD'],
      requirements: '• 5+ years in DevOps\n• AWS certification preferred',
      is_remote: false,
      employer_id: 'employer-4',
      application_count: 19,
      view_count: 301,
      status: 'active',
      posted_date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
      created_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
      updated_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
      id: '5',
      title: 'Junior Backend Developer',
      description: 'Great opportunity for a junior developer to learn and grow in a supportive environment.',
      company_id: 'company-5',
      company_name: 'Learning Labs',
      location: 'Boston, MA',
      job_type: 'full_time',
      experience_level: 'entry',
      salary_min: 60000,
      salary_max: 80000,
      skills: ['Python', 'Django', 'PostgreSQL', 'REST API'],
      requirements: '• 1+ year of experience or strong internship\n• CS degree preferred',
      is_remote: false,
      employer_id: 'employer-5',
      application_count: 42,
      view_count: 567,
      status: 'active',
      posted_date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
      created_at: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
      updated_at: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
      id: '6',
      title: 'Data Scientist',
      description: 'Join our data team to build machine learning models and derive insights from large datasets.',
      company_id: 'company-6',
      company_name: 'DataDriven Inc.',
      location: 'Seattle, WA',
      job_type: 'full_time',
      experience_level: 'mid',
      salary_min: 110000,
      salary_max: 150000,
      skills: ['Python', 'Machine Learning', 'TensorFlow', 'SQL', 'Statistics'],
      requirements: '• 3+ years in data science\n• Masters in related field preferred',
      is_remote: true,
      employer_id: 'employer-6',
      application_count: 27,
      view_count: 445,
      status: 'active',
      posted_date: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString(),
      created_at: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString(),
      updated_at: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString(),
    },
  ];
}

