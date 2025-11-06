'use client';

import { useState, useEffect } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { useAuth, useRequireRole } from '@/hooks/useAuth';
import { Job } from '@/types';
import { formatDate } from '@/lib/utils';
import { Plus, Eye, Edit, Trash2, Users, Briefcase } from 'lucide-react';
import Link from 'next/link';
import apiClient from '@/lib/api';

export default function EmployerJobsPage() {
  useAuth(true);
  useRequireRole(['employer']);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.getJobs({ employer: true });
      setJobs(response.data || []);
    } catch (error) {
      console.error('Failed to fetch jobs:', error);
      // Show mock data for demo
      setJobs(getMockEmployerJobs());
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteJob = async (jobId: string) => {
    if (!confirm('Are you sure you want to delete this job?')) return;

    try {
      await apiClient.deleteJob(jobId);
      setJobs(jobs.filter((job) => job.id !== jobId));
    } catch (error) {
      console.error('Failed to delete job:', error);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">My Job Postings</h1>
            <p className="text-gray-600">Manage and track your job listings</p>
          </div>
          <Link href="/employer/jobs/new">
            <Button variant="primary">
              <Plus size={18} className="mr-2" />
              Post New Job
            </Button>
          </Link>
        </div>

        {isLoading ? (
          <div className="flex justify-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        ) : jobs.length === 0 ? (
          <Card className="text-center py-12">
            <Briefcase className="mx-auto text-gray-400 mb-4" size={48} />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No job postings yet</h3>
            <p className="text-gray-600 mb-4">Create your first job posting to start receiving applications.</p>
            <Link href="/employer/jobs/new">
              <Button variant="primary">
                <Plus size={18} className="mr-2" />
                Post Your First Job
              </Button>
            </Link>
          </Card>
        ) : (
          <div className="space-y-4">
            {jobs.map((job) => (
              <Card key={job.id} hover>
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <h3 className="text-xl font-semibold text-gray-900">{job.title}</h3>
                        <p className="text-gray-600 mt-1">{job.location} • {job.job_type}</p>
                      </div>
                      <Badge variant={job.status === 'active' ? 'success' : 'default'}>
                        {job.status}
                      </Badge>
                    </div>

                    <div className="grid grid-cols-3 gap-4 py-3 mb-4 border-y border-gray-200">
                      <div>
                        <p className="text-sm text-gray-500">Posted</p>
                        <p className="font-medium text-gray-900">{formatDate(job.posted_date)}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500">Applications</p>
                        <p className="font-medium text-gray-900">24</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500">Views</p>
                        <p className="font-medium text-gray-900">342</p>
                      </div>
                    </div>

                    <div className="flex flex-wrap gap-2 mb-4">
                      {job.skills.slice(0, 5).map((skill) => (
                        <Badge key={skill} variant="default">
                          {skill}
                        </Badge>
                      ))}
                    </div>

                    <div className="flex space-x-2">
                      <Link href={`/employer/jobs/${job.id}/applications`}>
                        <Button variant="primary" size="sm">
                          <Users size={14} className="mr-1" />
                          View Applications (24)
                        </Button>
                      </Link>
                      <Link href={`/jobs/${job.id}`} target="_blank">
                        <Button variant="outline" size="sm">
                          <Eye size={14} className="mr-1" />
                          Preview
                        </Button>
                      </Link>
                      <Link href={`/employer/jobs/${job.id}/edit`}>
                        <Button variant="outline" size="sm">
                          <Edit size={14} className="mr-1" />
                          Edit
                        </Button>
                      </Link>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleDeleteJob(job.id)}
                        className="text-red-600 hover:text-red-700 hover:bg-red-50"
                      >
                        <Trash2 size={14} className="mr-1" />
                        Delete
                      </Button>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

function getMockEmployerJobs(): Job[] {
  return [
    {
      id: '1',
      title: 'Senior Frontend Developer',
      description: 'Looking for an experienced frontend developer...',
      company_id: 'company-1',
      location: 'San Francisco, CA',
      job_type: 'full-time',
      experience_level: 'senior',
      salary_min: 120000,
      salary_max: 180000,
      skills: ['React', 'TypeScript', 'Next.js', 'Tailwind CSS'],
      requirements: ['5+ years experience'],
      status: 'active',
      posted_date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
      id: '2',
      title: 'Product Manager',
      description: 'Seeking a product manager to lead our initiatives...',
      company_id: 'company-1',
      location: 'Remote',
      job_type: 'full-time',
      experience_level: 'mid',
      salary_min: 100000,
      salary_max: 150000,
      skills: ['Product Management', 'Agile', 'User Research', 'Analytics'],
      requirements: ['3+ years PM experience'],
      status: 'active',
      posted_date: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString(),
    },
  ];
}

