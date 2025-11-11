'use client';

import { useState, useEffect } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { useAuth, useRequireRole } from '@/hooks/useAuth';
import Link from 'next/link';
import { Briefcase, Users, Calendar, TrendingUp, Eye, CheckCircle } from 'lucide-react';
import apiClient from '@/lib/api';
import { Job } from '@/types';
import { formatDate } from '@/lib/utils';

export default function EmployerDashboardPage() {
  useAuth(true);
  useRequireRole(['employer']);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    setIsLoading(true);
    setError("");
    try {
      // Check if using demo token
      const token = localStorage.getItem('access_token');
      if (token && token.startsWith('demo-token-')) {
        // Skip API calls for demo mode, use empty jobs list
        setJobs([]);
        setIsLoading(false);
        return;
      }

      const response = await apiClient.getEmployerJobs();
      setJobs(response.jobs || []);
    } catch (err) {
      setError('Could not load jobs. Try again.');
      setJobs([]);
    } finally {
      setIsLoading(false);
    }
  };

  // Calculate dynamic stats
  const activeJobsCount = jobs.filter((j) => j.status === 'active').length;
  const totalApplications = 0; // Optionally, fetch or compute from API (future improvement)

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Employer Dashboard</h1>
          <p className="text-white">Manage your job postings and review applications</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <Card>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Active Jobs</p>
                <p className="text-3xl font-bold text-gray-900">{activeJobsCount}</p>
              </div>
              <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                <Briefcase className="text-primary" size={24} />
              </div>
            </div>
          </Card>
          <Card>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Total Applications</p>
                <p className="text-3xl font-bold text-gray-900">{totalApplications}</p>
                <p className="text-sm text-green-600 mt-1">(Coming soon)</p>
              </div>
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                <Users className="text-blue-600" size={24} />
              </div>
            </div>
          </Card>
          {/* ...other stats (to review, interviews) can be similarly set up */}
        </div>

        {/* Quick Actions */}
        <Card>
          <CardTitle>Quick Actions</CardTitle>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Link href="/employer/jobs/new">
                <Button variant="primary" className="w-full justify-start" size="lg">
                  <Briefcase size={20} className="mr-3" />
                  Post New Job
                </Button>
              </Link>
              <Link href="/employer/jobs">
                <Button variant="outline" className="w-full justify-start" size="lg">
                  <Eye size={20} className="mr-3" />
                  Manage Jobs
                </Button>
              </Link>
              <Link href="/employer/interviews">
                <Button variant="outline" className="w-full justify-start" size="lg">
                  <Calendar size={20} className="mr-3" />
                  View Interviews
                </Button>
              </Link>
              <Button variant="outline" className="w-full justify-start" size="lg">
                <TrendingUp size={20} className="mr-3" />
                View Analytics
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Active Jobs (real data) */}
        <Card>
          <CardTitle>Your Active Jobs</CardTitle>
          <CardContent>
            {isLoading ? (
              <div className="py-8 text-center">Loading...</div>
            ) : error ? (
              <div className="py-8 text-center text-red-600">{error}</div>
            ) : jobs.length === 0 ? (
              <div className="py-8 text-center">You have no active job postings yet.</div>
            ) : (
              <div className="space-y-4">
                {jobs.map((job) => (
                  <div key={job.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                    <div className="flex-1">
                      <h4 className="font-semibold text-gray-900">{job.title}</h4>
                      <p className="text-sm text-gray-600">Posted {formatDate(job.posted_date)} • {job.location} • {job.status}</p>
                      <div className="flex items-center space-x-4 mt-2">
                        {/* Application stats (when available) */}
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Link href={`/employer/jobs/${job.id}/applications`}><Button variant="outline" size="sm">View Applications</Button></Link>
                      <Link href={`/employer/jobs/${job.id}/edit`}><Button variant="ghost" size="sm">Edit</Button></Link>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Recent Applications - future dynamic integration */}
        <Card>
          <CardTitle>Recent Applications</CardTitle>
          <CardContent>
            <div className="space-y-4 text-gray-500 text-center">Coming soon: See your most recent applicants here.</div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}

