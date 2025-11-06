'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { ApplyModal } from '@/features/jobs/ApplyModal';
import { useAuthStore } from '@/store/authStore';
import apiClient from '@/lib/api';
import { Job } from '@/types';
import { formatDate, formatSalary } from '@/lib/utils';
import { MapPin, Briefcase, DollarSign, Calendar, Building, Check, ArrowLeft } from 'lucide-react';
import Link from 'next/link';

export default function JobDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { isAuthenticated, user } = useAuthStore();
  const [job, setJob] = useState<Job | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showApplyModal, setShowApplyModal] = useState(false);
  const [hasApplied, setHasApplied] = useState(false);

  useEffect(() => {
    fetchJobDetails();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [params.id]);

  const fetchJobDetails = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.getJobById(params.id as string);
      setJob(response.data);
    } catch (error) {
      console.error('Failed to fetch job:', error);
      // Show mock data for demo
      setJob(getMockJob(params.id as string));
    } finally {
      setIsLoading(false);
    }
  };

  const handleApply = () => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    setShowApplyModal(true);
  };

  const handleApplicationSuccess = () => {
    setHasApplied(true);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-5xl mx-auto px-4 py-20 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
        </div>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-5xl mx-auto px-4 py-20 text-center">
          <p className="text-gray-600">Job not found</p>
          <Link href="/jobs">
            <Button variant="primary" className="mt-4">
              Browse Jobs
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Link href="/jobs" className="inline-flex items-center text-primary hover:underline mb-6">
          <ArrowLeft size={16} className="mr-1" />
          Back to Jobs
        </Link>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            <Card>
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h1 className="text-3xl font-bold text-gray-900 mb-2">{job.title}</h1>
                  <div className="flex items-center space-x-4 text-gray-600">
                    <span className="flex items-center">
                      <Building size={18} className="mr-2" />
                      {job.company_name || 'Company Name'}
                    </span>
                    <span className="flex items-center">
                      <MapPin size={18} className="mr-2" />
                      {job.location}
                    </span>
                  </div>
                </div>
                <Badge variant="primary" className="text-base">
                  {job.job_type}
                </Badge>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 py-4 border-y border-gray-200">
                <div>
                  <p className="text-sm text-gray-500 mb-1">Experience</p>
                  <p className="font-medium text-gray-900">{job.experience_level}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">Salary</p>
                  <p className="font-medium text-gray-900">{formatSalary(job.salary_min, job.salary_max)}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">Posted</p>
                  <p className="font-medium text-gray-900">{formatDate(job.posted_date)}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">Status</p>
                  <Badge variant="success">{job.status}</Badge>
                </div>
              </div>

              <div className="mt-6">
                <h2 className="text-xl font-semibold mb-3">Job Description</h2>
                <p className="text-gray-700 whitespace-pre-line">{job.description}</p>
              </div>

              <div className="mt-6">
                <h2 className="text-xl font-semibold mb-3">Requirements</h2>
                <ul className="space-y-2">
                  {job.requirements.map((req, index) => (
                    <li key={index} className="flex items-start">
                      <Check size={20} className="text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-gray-700">{req}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="mt-6">
                <h2 className="text-xl font-semibold mb-3">Required Skills</h2>
                <div className="flex flex-wrap gap-2">
                  {job.skills.map((skill) => (
                    <Badge key={skill} variant="primary">
                      {skill}
                    </Badge>
                  ))}
                </div>
              </div>

              {job.benefits && job.benefits.length > 0 && (
                <div className="mt-6">
                  <h2 className="text-xl font-semibold mb-3">Benefits</h2>
                  <ul className="space-y-2">
                    {job.benefits.map((benefit, index) => (
                      <li key={index} className="flex items-start">
                        <Check size={20} className="text-primary mr-2 mt-0.5 flex-shrink-0" />
                        <span className="text-gray-700">{benefit}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            <Card>
              {hasApplied ? (
                <div className="text-center py-4">
                  <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
                    <Check className="text-green-600" size={32} />
                  </div>
                  <h3 className="text-lg font-semibold mb-2">Application Submitted!</h3>
                  <p className="text-sm text-gray-600 mb-4">
                    Your application has been successfully submitted.
                  </p>
                  <Link href="/dashboard/applications">
                    <Button variant="outline" className="w-full">
                      View My Applications
                    </Button>
                  </Link>
                </div>
              ) : (
                <>
                  <h3 className="text-lg font-semibold mb-4">Ready to Apply?</h3>
                  <Button
                    variant="primary"
                    className="w-full mb-3"
                    onClick={handleApply}
                  >
                    Apply Now
                  </Button>
                  <Button variant="outline" className="w-full">
                    Save Job
                  </Button>
                </>
              )}
            </Card>

            <Card>
              <h3 className="text-lg font-semibold mb-4">About the Company</h3>
              <p className="text-sm text-gray-600 mb-4">
                {job.company_name} is a leading company in the industry, committed to innovation and excellence.
              </p>
              <Button variant="ghost" className="w-full">
                View Company Profile
              </Button>
            </Card>
          </div>
        </div>
      </div>

      <Footer />

      <ApplyModal
        isOpen={showApplyModal}
        onClose={() => setShowApplyModal(false)}
        jobId={job.id}
        jobTitle={job.title}
        onSuccess={handleApplicationSuccess}
      />
    </div>
  );
}

function getMockJob(id: string): Job {
  return {
    id,
    title: 'Senior Frontend Developer',
    description: 'We are looking for an experienced frontend developer to join our growing team. You will be working on building scalable, performant web applications using modern technologies like React, TypeScript, and Next.js.\n\nIn this role, you will collaborate closely with designers, product managers, and backend engineers to deliver exceptional user experiences. You will have the opportunity to shape the architecture and technical direction of our frontend systems.',
    company_id: 'company-1',
    company_name: 'TechCorp Inc.',
    location: 'San Francisco, CA (Hybrid)',
    job_type: 'full-time',
    experience_level: 'senior',
    salary_min: 120000,
    salary_max: 180000,
    skills: ['React', 'TypeScript', 'Next.js', 'Tailwind CSS', 'Git', 'REST API'],
    requirements: [
      '5+ years of professional frontend development experience',
      'Expert knowledge of React and its ecosystem',
      'Strong proficiency in TypeScript',
      'Experience with modern CSS frameworks (Tailwind, Styled Components, etc.)',
      'Understanding of web performance optimization',
      'Experience with testing frameworks (Jest, React Testing Library)',
      'Excellent communication and collaboration skills',
    ],
    benefits: [
      'Competitive salary and equity',
      'Health, dental, and vision insurance',
      '401(k) with company match',
      'Flexible PTO policy',
      'Remote work options',
      'Professional development budget',
      'Modern tech stack',
    ],
    status: 'active',
    posted_date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
  };
}

