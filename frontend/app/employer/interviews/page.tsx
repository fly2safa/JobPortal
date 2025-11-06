'use client';

import { useState, useEffect } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Modal } from '@/components/ui/Modal';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { useAuth, useRequireRole } from '@/hooks/useAuth';
import { Interview } from '@/types';
import { formatDateTime } from '@/lib/utils';
import { Calendar, Plus, Video, Edit, X } from 'lucide-react';
import { useForm } from 'react-hook-form';
import apiClient from '@/lib/api';

interface ScheduleInterviewForm {
  scheduled_time: string;
  duration_minutes: number;
  meeting_link: string;
  notes: string;
}

export default function EmployerInterviewsPage() {
  useAuth(true);
  useRequireRole(['employer']);
  const [interviews, setInterviews] = useState<Interview[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showScheduleModal, setShowScheduleModal] = useState(false);

  const { register, handleSubmit, reset } = useForm<ScheduleInterviewForm>();

  useEffect(() => {
    fetchInterviews();
  }, []);

  const fetchInterviews = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.getInterviews({ employer: true });
      setInterviews(response.data || []);
    } catch (error) {
      console.error('Failed to fetch interviews:', error);
      setInterviews(getMockInterviews());
    } finally {
      setIsLoading(false);
    }
  };

  const handleScheduleInterview = async (data: ScheduleInterviewForm) => {
    try {
      await apiClient.scheduleInterview({
        ...data,
        job_id: 'job-1',
        application_id: 'app-1',
      });
      setShowScheduleModal(false);
      reset();
      fetchInterviews();
    } catch (error) {
      console.error('Failed to schedule interview:', error);
    }
  };

  const upcomingInterviews = interviews.filter((i) => i.status === 'scheduled');
  const pastInterviews = interviews.filter((i) => i.status === 'completed' || i.status === 'cancelled');

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Interviews</h1>
            <p className="text-gray-600">Manage and schedule interviews with candidates</p>
          </div>
          <Button variant="primary" onClick={() => setShowScheduleModal(true)}>
            <Plus size={18} className="mr-2" />
            Schedule Interview
          </Button>
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
              <p className="text-gray-600 mb-4">No upcoming interviews scheduled</p>
              <Button variant="primary" onClick={() => setShowScheduleModal(true)}>
                Schedule Interview
              </Button>
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
                            {interview.candidate_name}
                          </h3>
                          <p className="text-sm text-gray-600">
                            {formatDateTime(interview.scheduled_time)}
                          </p>
                        </div>
                        <Badge variant="success">Scheduled</Badge>
                      </div>

                      <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
                        <span>Duration: {interview.duration_minutes} minutes</span>
                        {interview.meeting_link && (
                          <>
                            <span>•</span>
                            <a
                              href={interview.meeting_link}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-primary hover:underline flex items-center"
                            >
                              <Video size={14} className="mr-1" />
                              Join Meeting
                            </a>
                          </>
                        )}
                      </div>

                      {interview.notes && (
                        <div className="bg-gray-50 rounded-lg p-3 mb-3 text-sm text-gray-700">
                          {interview.notes}
                        </div>
                      )}

                      <div className="flex space-x-2">
                        {interview.meeting_link && (
                          <Button variant="primary" size="sm">
                            <Video size={14} className="mr-1" />
                            Start Interview
                          </Button>
                        )}
                        <Button variant="outline" size="sm">
                          <Edit size={14} className="mr-1" />
                          Reschedule
                        </Button>
                        <Button variant="ghost" size="sm" className="text-red-600">
                          <X size={14} className="mr-1" />
                          Cancel
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
                  <div className="flex justify-between items-center">
                    <div>
                      <h3 className="font-semibold text-gray-900">{interview.candidate_name}</h3>
                      <p className="text-sm text-gray-600">{formatDateTime(interview.scheduled_time)}</p>
                    </div>
                    <Badge variant={interview.status === 'completed' ? 'success' : 'default'}>
                      {interview.status}
                    </Badge>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Schedule Interview Modal */}
      <Modal
        isOpen={showScheduleModal}
        onClose={() => setShowScheduleModal(false)}
        title="Schedule Interview"
        size="md"
      >
        <form onSubmit={handleSubmit(handleScheduleInterview)} className="space-y-4">
          <Input
            label="Date & Time"
            type="datetime-local"
            {...register('scheduled_time', { required: true })}
          />

          <Input
            label="Duration (minutes)"
            type="number"
            defaultValue={60}
            {...register('duration_minutes', { required: true, valueAsNumber: true })}
          />

          <Input
            label="Meeting Link"
            placeholder="https://meet.google.com/..."
            {...register('meeting_link')}
          />

          <Textarea
            label="Notes"
            rows={4}
            placeholder="Add any notes or preparation instructions for the interview..."
            {...register('notes')}
          />

          <div className="flex space-x-2 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => setShowScheduleModal(false)}
              className="flex-1"
            >
              Cancel
            </Button>
            <Button type="submit" variant="primary" className="flex-1">
              Schedule
            </Button>
          </div>
        </form>
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
      candidate_name: 'John Doe - Senior Frontend Developer',
      scheduled_time: new Date(now + 1 * 24 * 60 * 60 * 1000).toISOString(),
      duration_minutes: 60,
      meeting_link: 'https://meet.google.com/abc-defg-hij',
      status: 'scheduled',
      notes: 'Technical interview focusing on React and TypeScript',
    },
    {
      id: '2',
      job_id: 'job-1',
      application_id: 'app-2',
      candidate_name: 'Jane Smith - Product Manager',
      scheduled_time: new Date(now + 3 * 24 * 60 * 60 * 1000).toISOString(),
      duration_minutes: 45,
      meeting_link: 'https://zoom.us/j/123456789',
      status: 'scheduled',
      notes: 'Behavioral interview with team',
    },
  ];
}

