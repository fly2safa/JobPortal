'use client';

import { useState, useEffect } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Select } from '@/components/ui/Select';
import { useAuth } from '@/hooks/useAuth';
import { APPLICATION_STATUS } from '@/constants';
import { Application } from '@/types';
import { formatDate } from '@/lib/utils';
import { ExternalLink, FileText } from 'lucide-react';
import Link from 'next/link';
import apiClient from '@/lib/api';

export default function ApplicationsPage() {
  useAuth(true);
  const [applications, setApplications] = useState<Application[]>([]);
  const [filter, setFilter] = useState('all');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.getApplications();
      setApplications(response.applications || []);
    } catch (error) {
      console.error('Failed to fetch applications:', error);
      // Show mock data for demo
      setApplications(getMockApplications());
    } finally {
      setIsLoading(false);
    }
  };

  const filteredApplications = applications.filter((app) => {
    if (filter === 'all') return true;
    return app.status === filter;
  });

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">My Applications</h1>
            <p className="text-gray-600">Track the status of your job applications</p>
          </div>
        </div>

        {/* Filter */}
        <div className="flex items-center space-x-4">
          <Select
            options={[
              { value: 'all', label: 'All Applications' },
              { value: 'pending', label: 'Pending' },
              { value: 'reviewing', label: 'Reviewing' },
              { value: 'shortlisted', label: 'Shortlisted' },
              { value: 'rejected', label: 'Rejected' },
              { value: 'accepted', label: 'Accepted' },
            ]}
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="w-64"
          />
          <span className="text-sm text-gray-600">
            {filteredApplications.length} application{filteredApplications.length !== 1 ? 's' : ''}
          </span>
        </div>

        {/* Applications List */}
        {isLoading ? (
          <div className="flex justify-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        ) : filteredApplications.length === 0 ? (
          <Card className="text-center py-12">
            <FileText className="mx-auto text-gray-400 mb-4" size={48} />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No applications yet</h3>
            <p className="text-gray-600 mb-4">Start applying to jobs to see your applications here.</p>
            <Link href="/jobs">
              <Button variant="primary">Browse Jobs</Button>
            </Link>
          </Card>
        ) : (
          <div className="space-y-4">
            {filteredApplications.map((application) => (
              <Card key={application.id} hover>
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">
                          {application.job_title}
                        </h3>
                        <p className="text-gray-600">{application.company_name}</p>
                      </div>
                      <Badge
                        variant={
                          application.status === 'accepted' ? 'success' :
                          application.status === 'rejected' ? 'danger' :
                          application.status === 'shortlisted' ? 'success' :
                          application.status === 'reviewing' ? 'info' :
                          'warning'
                        }
                      >
                        {APPLICATION_STATUS[application.status].label}
                      </Badge>
                    </div>

                    <div className="flex items-center space-x-4 text-sm text-gray-500 mb-3">
                      <span>Applied: {formatDate(application.applied_date)}</span>
                      <span>•</span>
                      <span>Updated: {formatDate(application.updated_at)}</span>
                    </div>

                    {application.cover_letter && (
                      <details className="text-sm text-gray-600 mb-3">
                        <summary className="cursor-pointer font-medium hover:text-primary">
                          View Cover Letter
                        </summary>
                        <p className="mt-2 pl-4 border-l-2 border-gray-200 whitespace-pre-line">
                          {application.cover_letter}
                        </p>
                      </details>
                    )}

                    <div className="flex space-x-2">
                      <Link href={`/jobs/${application.job_id}`}>
                        <Button variant="outline" size="sm">
                          <ExternalLink size={14} className="mr-1" />
                          View Job
                        </Button>
                      </Link>
                      {application.resume_url && (
                        <Button variant="ghost" size="sm">
                          <FileText size={14} className="mr-1" />
                          View Resume
                        </Button>
                      )}
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

function getMockApplications(): Application[] {
  return [
    {
      id: '1',
      job_id: '1',
      job_title: 'Senior Frontend Developer',
      company_name: 'TechCorp Inc.',
      user_id: 'user-1',
      resume_url: 'resume-1.pdf',
      cover_letter: 'I am excited to apply for this position...',
      status: 'reviewing',
      applied_date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
      updated_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
      id: '2',
      job_id: '2',
      job_title: 'Full Stack Engineer',
      company_name: 'StartupXYZ',
      user_id: 'user-1',
      resume_url: 'resume-1.pdf',
      status: 'shortlisted',
      applied_date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
      updated_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
      id: '3',
      job_id: '3',
      job_title: 'Product Designer',
      company_name: 'DesignCo',
      user_id: 'user-1',
      resume_url: 'resume-1.pdf',
      status: 'pending',
      applied_date: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
      updated_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
    },
  ];
}

