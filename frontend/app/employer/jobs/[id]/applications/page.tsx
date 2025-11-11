'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Modal } from '@/components/ui/Modal';
import { useAuth, useRequireRole } from '@/hooks/useAuth';
import { Application } from '@/types';
import { formatDate } from '@/lib/utils';
import { Eye, CheckCircle, X, Calendar, FileText, Mail, Sparkles } from 'lucide-react';
import apiClient from '@/lib/api';

export default function JobApplicationsPage() {
  useAuth(true);
  useRequireRole(['employer']);
  const params = useParams();
  const [applications, setApplications] = useState<Application[]>([]);
  const [selectedApplication, setSelectedApplication] = useState<Application | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchApplications();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [params.id]);

  const fetchApplications = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.getJobApplications(params.id as string);
      setApplications(response.applications || []);
    } catch (error) {
      console.error('Failed to fetch applications:', error);
      // Show mock data for demo
      setApplications(getMockApplications());
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpdateStatus = async (applicationId: string, status: string) => {
    try {
      await apiClient.updateApplicationStatus(applicationId, status);
      setApplications(
        applications.map((app) =>
          app.id === applicationId ? { ...app, status: status as any } : app
        )
      );
    } catch (error) {
      console.error('Failed to update application status:', error);
    }
  };

  const filteredApplications = applications.filter((app) => {
    if (filter === 'all') return true;
    return app.status === filter;
  });

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Applications</h1>
          <p className="text-white">Review and manage applications for Senior Frontend Developer</p>
        </div>

        {/* Filters */}
        <div className="flex items-center space-x-2 overflow-x-auto pb-2">
          {['all', 'pending', 'reviewing', 'shortlisted', 'rejected'].map((status) => (
            <button
              key={status}
              onClick={() => setFilter(status)}
              className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-colors ${
                filter === status
                  ? 'bg-primary text-white'
                  : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
              }`}
            >
              {status.charAt(0).toUpperCase() + status.slice(1)}
              {status === 'all' && ` (${applications.length})`}
            </button>
          ))}
        </div>

        {/* AI Recommendations */}
        <Card className="bg-gradient-to-r from-purple-50 to-blue-50 border-purple-200">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-purple-500 rounded-full flex items-center justify-center flex-shrink-0">
              <Sparkles className="text-white" size={24} />
            </div>
            <div className="flex-1">
              <h3 className="font-semibold text-gray-900 mb-1">AI-Recommended Candidates</h3>
              <p className="text-sm text-gray-700 mb-3">
                Based on job requirements, these candidates are the best matches
              </p>
              <Button variant="outline" size="sm">
                View Top Matches
              </Button>
            </div>
          </div>
        </Card>

        {/* Applications List */}
        {isLoading ? (
          <div className="flex justify-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        ) : filteredApplications.length === 0 ? (
          <Card className="text-center py-12">
            <p className="text-gray-600">No applications yet for this filter.</p>
          </Card>
        ) : (
          <div className="grid gap-4">
            {filteredApplications.map((application) => (
              <Card key={application.id} hover>
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-4 flex-1">
                    <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center text-white font-bold text-xl flex-shrink-0">
                      {application.user_id.slice(0, 2).toUpperCase()}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900">
                            Candidate {application.id.slice(-4)}
                          </h3>
                          <p className="text-sm text-gray-600">
                            Applied {formatDate(application.applied_date)}
                          </p>
                        </div>
                        <Badge
                          variant={
                            application.status === 'shortlisted' ? 'success' :
                            application.status === 'rejected' ? 'danger' :
                            application.status === 'reviewing' ? 'info' :
                            'warning'
                          }
                        >
                          {application.status}
                        </Badge>
                      </div>

                      <div className="flex flex-wrap gap-2 mb-3">
                        <Badge variant="default">React</Badge>
                        <Badge variant="default">TypeScript</Badge>
                        <Badge variant="default">5+ years</Badge>
                        <Badge variant="success">92% Match</Badge>
                      </div>

                      <div className="flex space-x-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => setSelectedApplication(application)}
                        >
                          <Eye size={14} className="mr-1" />
                          View Details
                        </Button>
                        {application.status === 'pending' && (
                          <Button
                            variant="primary"
                            size="sm"
                            onClick={() => handleUpdateStatus(application.id, 'reviewing')}
                          >
                            Start Review
                          </Button>
                        )}
                        {application.status === 'reviewing' && (
                          <>
                            <Button
                              variant="primary"
                              size="sm"
                              onClick={() => handleUpdateStatus(application.id, 'shortlisted')}
                            >
                              <CheckCircle size={14} className="mr-1" />
                              Shortlist
                            </Button>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => handleUpdateStatus(application.id, 'rejected')}
                            >
                              <X size={14} className="mr-1" />
                              Reject
                            </Button>
                          </>
                        )}
                        {application.status === 'shortlisted' && (
                          <Button variant="primary" size="sm">
                            <Calendar size={14} className="mr-1" />
                            Schedule Interview
                          </Button>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Application Detail Modal */}
      {selectedApplication && (
        <Modal
          isOpen={!!selectedApplication}
          onClose={() => setSelectedApplication(null)}
          title="Application Details"
          size="lg"
        >
          <div className="space-y-6">
            <div>
              <h3 className="font-semibold mb-2">Candidate Information</h3>
              <div className="bg-gray-50 rounded-lg p-4 space-y-2">
                <p className="text-sm"><strong>Applied:</strong> {formatDate(selectedApplication.applied_date)}</p>
                <p className="text-sm"><strong>Status:</strong> {selectedApplication.status}</p>
                <p className="text-sm"><strong>Email:</strong> candidate@example.com</p>
              </div>
            </div>

            {selectedApplication.cover_letter && (
              <div>
                <h3 className="font-semibold mb-2">Cover Letter</h3>
                <div className="bg-gray-50 rounded-lg p-4">
                  <p className="text-sm text-gray-700 whitespace-pre-line">
                    {selectedApplication.cover_letter}
                  </p>
                </div>
              </div>
            )}

            <div>
              <h3 className="font-semibold mb-2">Resume</h3>
              <Button variant="outline" className="w-full">
                <FileText size={16} className="mr-2" />
                View Resume
              </Button>
            </div>

            <div className="flex space-x-2">
              <Button
                variant="primary"
                className="flex-1"
                onClick={() => handleUpdateStatus(selectedApplication.id, 'shortlisted')}
              >
                <CheckCircle size={16} className="mr-2" />
                Shortlist
              </Button>
              <Button variant="outline" className="flex-1">
                <Mail size={16} className="mr-2" />
                Send Message
              </Button>
            </div>
          </div>
        </Modal>
      )}
    </DashboardLayout>
  );
}

function getMockApplications(): Application[] {
  return [
    {
      id: 'app-1',
      job_id: 'job-1',
      user_id: 'user-1',
      resume_url: 'resume-1.pdf',
      cover_letter: 'I am excited to apply for this position. With over 5 years of experience in React development...',
      status: 'pending',
      applied_date: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
      updated_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
      id: 'app-2',
      job_id: 'job-1',
      user_id: 'user-2',
      resume_url: 'resume-2.pdf',
      status: 'reviewing',
      applied_date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
      updated_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
      id: 'app-3',
      job_id: 'job-1',
      user_id: 'user-3',
      resume_url: 'resume-3.pdf',
      status: 'shortlisted',
      applied_date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
      updated_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
    },
  ];
}

