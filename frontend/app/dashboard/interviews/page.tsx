'use client';

import { useState, useEffect } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/hooks/useAuth';
import { Interview } from '@/types';
import { formatDateTime } from '@/lib/utils';
import { Calendar, Clock, Video, MapPin } from 'lucide-react';
import apiClient from '@/lib/api';

export default function InterviewsPage() {
  useAuth(true);
  const [interviews, setInterviews] = useState<Interview[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchInterviews();
  }, []);

  const fetchInterviews = async () => {
    setIsLoading(true);
    try {
      // Check if using demo token
      const token = localStorage.getItem('access_token');
      if (token && token.startsWith('demo-token-')) {
        // Use mock data for demo mode
        setInterviews(getMockInterviews());
        setIsLoading(false);
        return;
      }

      const response = await apiClient.getInterviews();
      setInterviews(response || []);
    } catch (error) {
      console.error('Failed to fetch interviews:', error);
      // Show mock data for demo
      setInterviews(getMockInterviews());
    } finally {
      setIsLoading(false);
    }
  };

  const upcomingInterviews = interviews.filter((i) => i.status === 'scheduled');
  const pastInterviews = interviews.filter((i) => i.status === 'completed' || i.status === 'cancelled');

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Interviews</h1>
          <p className="text-white">Manage your upcoming and past interviews</p>
        </div>

        {/* Upcoming Interviews */}
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Upcoming Interviews</h2>
          {isLoading ? (
            <div className="flex justify-center py-10">
              <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary"></div>
            </div>
          ) : upcomingInterviews.length === 0 ? (
            <Card className="text-center py-10">
              <Calendar className="mx-auto text-gray-400 mb-3" size={48} />
              <p className="text-gray-600">No upcoming interviews</p>
            </Card>
          ) : (
            <div className="space-y-4">
              {upcomingInterviews.map((interview) => (
                <Card key={interview.id} className="border-l-4 border-primary">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900">
                            Interview Scheduled
                          </h3>
                          <p className="text-gray-600">{interview.candidate_name || 'Position'}</p>
                        </div>
                        <Badge variant="success">Scheduled</Badge>
                      </div>

                      <div className="space-y-2 mb-4">
                        <div className="flex items-center text-sm text-gray-700">
                          <Calendar size={16} className="mr-2" />
                          {formatDateTime(interview.scheduled_time)}
                        </div>
                        <div className="flex items-center text-sm text-gray-700">
                          <Clock size={16} className="mr-2" />
                          Duration: {interview.duration_minutes} minutes
                        </div>
                        {interview.meeting_link && (
                          <div className="flex items-center text-sm text-gray-700">
                            <Video size={16} className="mr-2" />
                            <a
                              href={interview.meeting_link}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-primary hover:underline"
                            >
                              Join Video Call
                            </a>
                          </div>
                        )}
                      </div>

                      {interview.notes && (
                        <div className="bg-gray-50 rounded-lg p-3 mb-4">
                          <p className="text-sm text-gray-700">{interview.notes}</p>
                        </div>
                      )}

                      <div className="flex space-x-2">
                        {interview.meeting_link && (
                          <Button variant="primary" size="sm">
                            <Video size={14} className="mr-1" />
                            Join Interview
                          </Button>
                        )}
                        <Button variant="outline" size="sm">
                          Add to Calendar
                        </Button>
                      </div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>

        {/* Past Interviews */}
        {pastInterviews.length > 0 && (
          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Past Interviews</h2>
            <div className="space-y-4">
              {pastInterviews.map((interview) => (
                <Card key={interview.id} className="opacity-75">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900">
                            {interview.candidate_name || 'Interview'}
                          </h3>
                        </div>
                        <Badge variant={interview.status === 'completed' ? 'default' : 'danger'}>
                          {interview.status}
                        </Badge>
                      </div>

                      <div className="flex items-center text-sm text-gray-600">
                        <Calendar size={16} className="mr-2" />
                        {formatDateTime(interview.scheduled_time)}
                      </div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

function getMockInterviews(): Interview[] {
  const now = Date.now();
  return [
    {
      id: '1',
      job_id: 'job-1',
      application_id: 'app-1',
      candidate_name: 'Senior Frontend Developer at TechCorp',
      scheduled_time: new Date(now + 2 * 24 * 60 * 60 * 1000).toISOString(),
      duration_minutes: 60,
      meeting_link: 'https://meet.google.com/abc-defg-hij',
      status: 'scheduled',
      notes: 'First round technical interview. Be prepared to discuss your React experience and solve coding challenges.',
    },
    {
      id: '2',
      job_id: 'job-2',
      application_id: 'app-2',
      candidate_name: 'Full Stack Engineer at StartupXYZ',
      scheduled_time: new Date(now + 5 * 24 * 60 * 60 * 1000).toISOString(),
      duration_minutes: 45,
      meeting_link: 'https://zoom.us/j/123456789',
      status: 'scheduled',
      notes: 'Behavioral interview with the hiring manager. Review the company culture and prepare questions.',
    },
  ];
}

