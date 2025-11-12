'use client';

import { useState, useEffect } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Modal } from '@/components/ui/Modal';
import { useAuth } from '@/hooks/useAuth';
import { Interview } from '@/types';
import { InterviewCard, InterviewCalendar } from '@/features/interviews';
import { Calendar as CalendarIcon, List } from 'lucide-react';
import apiClient from '@/lib/api';

export default function InterviewsPage() {
  useAuth(true);
  const [interviews, setInterviews] = useState<Interview[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'list' | 'calendar'>('list');
  const [showCancelModal, setShowCancelModal] = useState(false);
  const [selectedInterview, setSelectedInterview] = useState<Interview | null>(null);
  const [cancelReason, setCancelReason] = useState('');

  useEffect(() => {
    fetchInterviews();
  }, []);

  const fetchInterviews = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.getInterviews();
      setInterviews(response.interviews || response || []);
    } catch (error) {
      console.error('Failed to fetch interviews:', error);
      // Show mock data for demo
      setInterviews(getMockInterviews());
    } finally {
      setIsLoading(false);
    }
  };

  const handleJoinInterview = (interview: Interview) => {
    if (interview.meeting_link) {
      window.open(interview.meeting_link, '_blank');
    }
  };

  const handleCancelInterview = (interview: Interview) => {
    setSelectedInterview(interview);
    setShowCancelModal(true);
  };

  const confirmCancelInterview = async () => {
    if (!selectedInterview) return;

    try {
      await apiClient.cancelInterview(selectedInterview.id, cancelReason);
      setShowCancelModal(false);
      setCancelReason('');
      setSelectedInterview(null);
      fetchInterviews();
    } catch (error) {
      console.error('Failed to cancel interview:', error);
    }
  };

  const upcomingInterviews = interviews.filter((i) => i.status === 'scheduled' || i.status === 'rescheduled');
  const pastInterviews = interviews.filter((i) => i.status === 'completed' || i.status === 'cancelled' || i.status === 'no_show');

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Interviews</h1>
            <p className="text-white">Manage your upcoming and past interviews</p>
          </div>
          <div className="flex space-x-2">
            <Button
              variant={viewMode === 'list' ? 'primary' : 'outline'}
              onClick={() => setViewMode('list')}
            >
              <List size={18} className="mr-2" />
              List
            </Button>
            <Button
              variant={viewMode === 'calendar' ? 'primary' : 'outline'}
              onClick={() => setViewMode('calendar')}
            >
              <CalendarIcon size={18} className="mr-2" />
              Calendar
            </Button>
          </div>
        </div>

        {isLoading ? (
          <div className="flex justify-center py-10">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary"></div>
          </div>
        ) : viewMode === 'calendar' ? (
          <InterviewCalendar
            interviews={interviews}
            onDateSelect={(date) => {
              console.log('Selected date:', date);
              setViewMode('list');
            }}
            onInterviewClick={(interview) => {
              console.log('Selected interview:', interview);
            }}
          />
        ) : (
          <>
            {/* Upcoming Interviews */}
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Upcoming Interviews</h2>
              {upcomingInterviews.length === 0 ? (
                <Card className="text-center py-10">
                  <CalendarIcon className="mx-auto text-gray-400 mb-3" size={48} />
                  <p className="text-gray-600">No upcoming interviews</p>
                </Card>
              ) : (
                <div className="space-y-4">
                  {upcomingInterviews.map((interview) => (
                    <InterviewCard
                      key={interview.id}
                      interview={interview}
                      isEmployer={false}
                      onJoin={handleJoinInterview}
                      onCancel={handleCancelInterview}
                    />
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
                    <InterviewCard
                      key={interview.id}
                      interview={interview}
                      isEmployer={false}
                    />
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {/* Cancel Interview Modal */}
      <Modal
        isOpen={showCancelModal}
        onClose={() => {
          setShowCancelModal(false);
          setCancelReason('');
          setSelectedInterview(null);
        }}
        title="Cancel Interview"
        size="md"
      >
        <div className="space-y-4">
          <p className="text-gray-700">
            Are you sure you want to cancel this interview? The employer will be notified.
          </p>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Reason for cancellation (optional)
            </label>
            <textarea
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              rows={3}
              value={cancelReason}
              onChange={(e) => setCancelReason(e.target.value)}
              placeholder="Please provide a reason..."
            />
          </div>

          <div className="flex space-x-2 pt-4">
            <Button
              variant="outline"
              onClick={() => {
                setShowCancelModal(false);
                setCancelReason('');
                setSelectedInterview(null);
              }}
              className="flex-1"
            >
              Keep Interview
            </Button>
            <Button
              variant="primary"
              onClick={confirmCancelInterview}
              className="flex-1 bg-red-600 hover:bg-red-700"
            >
              Cancel Interview
            </Button>
          </div>
        </div>
      </Modal>
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

