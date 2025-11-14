'use client';

import { useState, useEffect } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Modal } from '@/components/ui/Modal';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Select } from '@/components/ui/Select';
import { useAuth, useRequireRole } from '@/hooks/useAuth';
import { Interview } from '@/types';
import { InterviewCard, InterviewCalendar } from '@/features/interviews';
import { Calendar as CalendarIcon, Plus, List } from 'lucide-react';
import { useForm } from 'react-hook-form';
import apiClient from '@/lib/api';

interface ScheduleInterviewForm {
  job_id: string;
  application_id: string;
  scheduled_time: string;
  duration_minutes: number;
  interview_type: string;
  meeting_link: string;
  meeting_location: string;
  meeting_instructions: string;
  notes: string;
}

interface RescheduleForm {
  reschedule_date: string;
  reschedule_time: string;
  reason: string;
}

export default function EmployerInterviewsPage() {
  useAuth(true);
  useRequireRole(['employer']);
  const [interviews, setInterviews] = useState<Interview[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'list' | 'calendar'>('list');
  const [showScheduleModal, setShowScheduleModal] = useState(false);
  const [showRescheduleModal, setShowRescheduleModal] = useState(false);
  const [showCancelModal, setShowCancelModal] = useState(false);
  const [showCompleteModal, setShowCompleteModal] = useState(false);
  const [selectedInterview, setSelectedInterview] = useState<Interview | null>(null);
  const [cancelReason, setCancelReason] = useState('');
  const [feedback, setFeedback] = useState('');

  const { register, handleSubmit, reset } = useForm<ScheduleInterviewForm>();
  const { register: registerReschedule, handleSubmit: handleSubmitReschedule, reset: resetReschedule } = useForm<RescheduleForm>();

  useEffect(() => {
    fetchInterviews();
  }, []);

  const fetchInterviews = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.getInterviews({ employer: true });
      setInterviews(response.interviews || response || []);
    } catch (error) {
      console.error('Failed to fetch interviews:', error);
      setInterviews(getMockInterviews());
    } finally {
      setIsLoading(false);
    }
  };

  const handleScheduleInterview = async (data: ScheduleInterviewForm) => {
    try {
      await apiClient.scheduleInterview(data);
      setShowScheduleModal(false);
      reset();
      fetchInterviews();
    } catch (error) {
      console.error('Failed to schedule interview:', error);
    }
  };

  const handleJoinInterview = (interview: Interview) => {
    if (interview.meeting_link) {
      window.open(interview.meeting_link, '_blank');
    }
  };

  const handleRescheduleInterview = (interview: Interview) => {
    setSelectedInterview(interview);
    setShowRescheduleModal(true);
  };

  const confirmReschedule = async (data: RescheduleForm) => {
    if (!selectedInterview) return;

    try {
      // Combine date and time into ISO format
      const scheduledDateTime = `${data.reschedule_date}T${data.reschedule_time}:00`;
      
      await apiClient.rescheduleInterview(selectedInterview.id, {
        scheduled_time: scheduledDateTime,
        reason: data.reason
      });
      setShowRescheduleModal(false);
      resetReschedule();
      setSelectedInterview(null);
      fetchInterviews();
    } catch (error) {
      console.error('Failed to reschedule interview:', error);
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

  const handleCompleteInterview = (interview: Interview) => {
    setSelectedInterview(interview);
    setShowCompleteModal(true);
  };

  const confirmCompleteInterview = async () => {
    if (!selectedInterview) return;

    try {
      await apiClient.completeInterview(selectedInterview.id, { feedback });
      setShowCompleteModal(false);
      setFeedback('');
      setSelectedInterview(null);
      fetchInterviews();
    } catch (error) {
      console.error('Failed to complete interview:', error);
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
            <p className="text-white">Manage and schedule interviews with candidates</p>
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
            <Button variant="primary" onClick={() => setShowScheduleModal(true)}>
              <Plus size={18} className="mr-2" />
              Schedule Interview
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
                  <p className="text-gray-600 mb-4">No upcoming interviews scheduled</p>
                  <Button variant="primary" onClick={() => setShowScheduleModal(true)}>
                    Schedule Interview
                  </Button>
                </Card>
              ) : (
                <div className="space-y-4">
                  {upcomingInterviews.map((interview) => (
                    <InterviewCard
                      key={interview.id}
                      interview={interview}
                      isEmployer={true}
                      onJoin={handleJoinInterview}
                      onReschedule={handleRescheduleInterview}
                      onCancel={handleCancelInterview}
                      onComplete={handleCompleteInterview}
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
                      isEmployer={true}
                    />
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {/* Schedule Interview Modal */}
      <Modal
        isOpen={showScheduleModal}
        onClose={() => setShowScheduleModal(false)}
        title="Schedule Interview"
        size="lg"
      >
        <form onSubmit={handleSubmit(handleScheduleInterview)} className="space-y-4">
          <Input
            label="Job ID"
            placeholder="Enter job ID"
            {...register('job_id', { required: true })}
          />

          <Input
            label="Application ID"
            placeholder="Enter application ID"
            {...register('application_id', { required: true })}
          />

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

          <Select
            label="Interview Type"
            options={[
              { value: 'video', label: 'Video Interview' },
              { value: 'phone', label: 'Phone Interview' },
              { value: 'in_person', label: 'In-Person' },
              { value: 'technical', label: 'Technical Interview' },
              { value: 'behavioral', label: 'Behavioral Interview' },
              { value: 'final', label: 'Final Interview' }
            ]}
            {...register('interview_type')}
          />

          <Input
            label="Meeting Link"
            placeholder="https://meet.google.com/..."
            {...register('meeting_link')}
          />

          <Input
            label="Meeting Location (for in-person)"
            placeholder="Office address or location"
            {...register('meeting_location')}
          />

          <Textarea
            label="Meeting Instructions"
            rows={2}
            placeholder="Instructions for joining or finding the interview location..."
            {...register('meeting_instructions')}
          />

          <Textarea
            label="Notes"
            rows={3}
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
              Schedule Interview
            </Button>
          </div>
        </form>
      </Modal>

      {/* Reschedule Interview Modal */}
      <Modal
        isOpen={showRescheduleModal}
        onClose={() => {
          setShowRescheduleModal(false);
          resetReschedule();
          setSelectedInterview(null);
        }}
        title="Reschedule Interview"
        size="md"
      >
        <form onSubmit={handleSubmitReschedule(confirmReschedule)} className="space-y-4">
          <p className="text-gray-700">
            Reschedule interview with <strong>{selectedInterview?.candidate_name}</strong>
          </p>

          <div className="grid grid-cols-2 gap-4">
            <Input
              label="New Date"
              type="date"
              {...registerReschedule('reschedule_date', { 
                required: 'Date is required',
                validate: (value) => {
                  const selectedDate = new Date(value);
                  const today = new Date();
                  today.setHours(0, 0, 0, 0);
                  return selectedDate >= today || 'Date cannot be in the past';
                }
              })}
            />

            <Select
              label="New Time"
              options={[
                { value: '', label: 'Select time' },
                ...Array.from({ length: 96 }, (_, i) => {
                  const hours = Math.floor(i / 4);
                  const minutes = (i % 4) * 15;
                  const time = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
                  const period = hours < 12 ? 'AM' : 'PM';
                  const displayHours = hours === 0 ? 12 : hours > 12 ? hours - 12 : hours;
                  const displayTime = `${displayHours}:${minutes.toString().padStart(2, '0')} ${period}`;
                  return { value: time, label: displayTime };
                })
              ]}
              {...registerReschedule('reschedule_time', { required: 'Time is required' })}
            />
          </div>

          <Textarea
            label="Reason for Rescheduling"
            rows={3}
            placeholder="Please provide a reason for rescheduling..."
            {...registerReschedule('reason')}
          />

          <div className="flex space-x-2 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => {
                setShowRescheduleModal(false);
                resetReschedule();
                setSelectedInterview(null);
              }}
              className="flex-1"
            >
              Cancel
            </Button>
            <Button type="submit" variant="primary" className="flex-1">
              Reschedule
            </Button>
          </div>
        </form>
      </Modal>

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
            Are you sure you want to cancel the interview with <strong>{selectedInterview?.candidate_name}</strong>? 
            The candidate will be notified.
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

      {/* Complete Interview Modal */}
      <Modal
        isOpen={showCompleteModal}
        onClose={() => {
          setShowCompleteModal(false);
          setFeedback('');
          setSelectedInterview(null);
        }}
        title="Complete Interview"
        size="md"
      >
        <div className="space-y-4">
          <p className="text-gray-700">
            Mark interview with <strong>{selectedInterview?.candidate_name}</strong> as completed.
          </p>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Interview Feedback (optional)
            </label>
            <textarea
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              rows={4}
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
              placeholder="Add your feedback about the interview..."
            />
          </div>

          <div className="flex space-x-2 pt-4">
            <Button
              variant="outline"
              onClick={() => {
                setShowCompleteModal(false);
                setFeedback('');
                setSelectedInterview(null);
              }}
              className="flex-1"
            >
              Cancel
            </Button>
            <Button
              variant="primary"
              onClick={confirmCompleteInterview}
              className="flex-1"
            >
              Mark Complete
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

