'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Modal } from '@/components/ui/Modal';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Textarea } from '@/components/ui/Textarea';
import { useAuth, useRequireRole } from '@/hooks/useAuth';
import { Application } from '@/types';
import { formatDate } from '@/lib/utils';
import { Sparkles, FileText, AlertCircle } from 'lucide-react';
import apiClient from '@/lib/api';
import { CandidateCard } from '@/features/employer/applications';
import { getErrorMessage } from '@/lib/errorHandler';

export default function JobApplicationsPage() {
  useAuth(true);
  useRequireRole(['employer']);
  const params = useParams();
  const router = useRouter();
  const [applications, setApplications] = useState<Application[]>([]);
  const [selectedApplication, setSelectedApplication] = useState<Application | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [jobTitle, setJobTitle] = useState('this position');
  const [stats, setStats] = useState({
    total: 0,
    pending: 0,
    reviewing: 0,
    shortlisted: 0,
    rejected: 0,
  });
  const [showRejectModal, setShowRejectModal] = useState(false);
  const [rejectingAppId, setRejectingAppId] = useState<string | null>(null);
  const [rejectionReason, setRejectionReason] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [showScheduleModal, setShowScheduleModal] = useState(false);
  const [schedulingApplication, setSchedulingApplication] = useState<Application | null>(null);
  const [isScheduling, setIsScheduling] = useState(false);
  const [scheduleError, setScheduleError] = useState('');

  useEffect(() => {
    fetchApplications();
    fetchJobDetails();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [params.id, filter]);

  const fetchJobDetails = async () => {
    try {
      const job = await apiClient.getJob(params.id as string);
      setJobTitle(job.title || 'this position');
    } catch (error) {
      console.error('Failed to fetch job details:', error);
    }
  };

  const fetchApplications = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiClient.getJobApplications(
        params.id as string,
        filter !== 'all' ? { status_filter: filter } : undefined
      );
      setApplications(response.applications || []);
      
      // Calculate stats
      const newStats = {
        total: response.total || 0,
        pending: 0,
        reviewing: 0,
        shortlisted: 0,
        rejected: 0,
      };
      
      (response.applications || []).forEach((app: Application) => {
        if (app.status === 'pending') newStats.pending++;
        if (app.status === 'reviewing') newStats.reviewing++;
        if (app.status === 'shortlisted') newStats.shortlisted++;
        if (app.status === 'rejected') newStats.rejected++;
      });
      
      setStats(newStats);
    } catch (error: any) {
      console.error('Failed to fetch applications:', error);
      setError(error.response?.data?.detail || 'Failed to load applications');
    } finally {
      setIsLoading(false);
    }
  };

  const handleStartReview = async (applicationId: string) => {
    try {
      await apiClient.updateApplicationStatus(applicationId, 'reviewing');
      await fetchApplications();
    } catch (error: any) {
      console.error('Failed to start review:', error);
      alert(error.response?.data?.detail || 'Failed to start review');
    }
  };

  const handleShortlist = async (applicationId: string) => {
    try {
      await apiClient.shortlistApplication(applicationId);
      await fetchApplications();
    } catch (error: any) {
      console.error('Failed to shortlist application:', error);
      alert(error.response?.data?.detail || 'Failed to shortlist application');
    }
  };

  const handleRejectClick = (applicationId: string) => {
    setRejectingAppId(applicationId);
    setRejectionReason('');
    setShowRejectModal(true);
  };

  const handleRejectConfirm = async () => {
    if (!rejectingAppId) return;
    
    try {
      await apiClient.rejectApplication(rejectingAppId, rejectionReason || undefined);
      setShowRejectModal(false);
      setRejectingAppId(null);
      setRejectionReason('');
      await fetchApplications();
    } catch (error: any) {
      console.error('Failed to reject application:', error);
      alert(error.response?.data?.detail || 'Failed to reject application');
    }
  };

  const {
    register: registerSchedule,
    handleSubmit: handleSubmitSchedule,
    formState: { errors: scheduleErrors },
    reset: resetSchedule,
  } = useForm();

  const handleScheduleInterview = (applicationId: string) => {
    const application = applications.find(app => app.id === applicationId);
    if (application) {
      setSchedulingApplication(application);
      setShowScheduleModal(true);
      setScheduleError('');
      resetSchedule();
    }
  };

  const onScheduleSubmit = async (data: any) => {
    if (!schedulingApplication) return;
    
    setIsScheduling(true);
    setScheduleError('');
    
    try {
      // Format the datetime for the API
      const scheduledTime = `${data.interview_date}T${data.interview_time}:00Z`;
      
      await apiClient.scheduleInterview({
        job_id: params.id as string,
        application_id: schedulingApplication.id,
        scheduled_time: scheduledTime,
        duration_minutes: parseInt(data.duration_minutes),
        interview_type: data.interview_type,
        meeting_link: data.meeting_link || undefined,
        meeting_location: data.meeting_location || undefined,
        meeting_instructions: data.meeting_instructions || undefined,
        notes: data.notes || undefined,
      });
      
      setShowScheduleModal(false);
      setSchedulingApplication(null);
      alert('Interview scheduled successfully! Both you and the candidate have been notified.');
      await fetchApplications();
    } catch (err: any) {
      setScheduleError(getErrorMessage(err, 'Failed to schedule interview. Please try again.'));
    } finally {
      setIsScheduling(false);
    }
  };

  const filteredApplications = applications;

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Applications</h1>
          <p className="text-white">Review and manage applications for {jobTitle}</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <Card className="text-center">
            <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
            <p className="text-sm text-gray-600">Total</p>
          </Card>
          <Card className="text-center">
            <p className="text-2xl font-bold text-yellow-600">{stats.pending}</p>
            <p className="text-sm text-gray-600">Pending</p>
          </Card>
          <Card className="text-center">
            <p className="text-2xl font-bold text-blue-600">{stats.reviewing}</p>
            <p className="text-sm text-gray-600">Reviewing</p>
          </Card>
          <Card className="text-center">
            <p className="text-2xl font-bold text-green-600">{stats.shortlisted}</p>
            <p className="text-sm text-gray-600">Shortlisted</p>
          </Card>
          <Card className="text-center">
            <p className="text-2xl font-bold text-red-600">{stats.rejected}</p>
            <p className="text-sm text-gray-600">Rejected</p>
          </Card>
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
              {status === 'all' && ` (${stats.total})`}
              {status === 'pending' && ` (${stats.pending})`}
              {status === 'reviewing' && ` (${stats.reviewing})`}
              {status === 'shortlisted' && ` (${stats.shortlisted})`}
              {status === 'rejected' && ` (${stats.rejected})`}
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

        {/* Error State */}
        {error && (
          <Card className="bg-red-50 border-red-200">
            <div className="flex items-center space-x-3">
              <AlertCircle className="text-red-600" size={24} />
              <div>
                <p className="font-semibold text-red-900">Error Loading Applications</p>
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </Card>
        )}

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
              <CandidateCard
                key={application.id}
                application={application}
                onViewDetails={setSelectedApplication}
                onShortlist={handleShortlist}
                onReject={handleRejectClick}
                onStartReview={handleStartReview}
                onScheduleInterview={handleScheduleInterview}
              />
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
                <p className="text-sm"><strong>Name:</strong> {selectedApplication.applicant_name}</p>
                <p className="text-sm"><strong>Email:</strong> {selectedApplication.applicant_email}</p>
                <p className="text-sm"><strong>Applied:</strong> {formatDate(selectedApplication.applied_at)}</p>
                <p className="text-sm"><strong>Status:</strong> <Badge variant={
                  selectedApplication.status === 'shortlisted' ? 'success' :
                  selectedApplication.status === 'rejected' ? 'danger' :
                  selectedApplication.status === 'reviewing' ? 'info' : 'warning'
                }>{selectedApplication.status}</Badge></p>
              </div>
            </div>

            {selectedApplication.cover_letter && (
              <div>
                <h3 className="font-semibold mb-2">Cover Letter</h3>
                <div className="bg-gray-50 rounded-lg p-4 max-h-64 overflow-y-auto">
                  <p className="text-sm text-gray-700 whitespace-pre-line">
                    {selectedApplication.cover_letter}
                  </p>
                </div>
              </div>
            )}

            {selectedApplication.resume_url && (
              <div>
                <h3 className="font-semibold mb-2">Resume</h3>
                <a
                  href={selectedApplication.resume_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block"
                >
                  <Button variant="outline" className="w-full">
                    <FileText size={16} className="mr-2" />
                    View Resume
                  </Button>
                </a>
              </div>
            )}

            {selectedApplication.employer_notes && (
              <div>
                <h3 className="font-semibold mb-2">Employer Notes</h3>
                <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                  <p className="text-sm text-blue-800">{selectedApplication.employer_notes}</p>
                </div>
              </div>
            )}

            {selectedApplication.status === 'reviewing' && (
              <div className="flex space-x-2">
                <Button
                  variant="primary"
                  className="flex-1"
                  onClick={() => {
                    handleShortlist(selectedApplication.id);
                    setSelectedApplication(null);
                  }}
                >
                  Shortlist
                </Button>
                <Button
                  variant="outline"
                  className="flex-1 text-red-600 hover:bg-red-50 border-red-300"
                  onClick={() => {
                    setSelectedApplication(null);
                    handleRejectClick(selectedApplication.id);
                  }}
                >
                  Reject
                </Button>
              </div>
            )}
          </div>
        </Modal>
      )}

      {/* Reject Confirmation Modal */}
      {showRejectModal && (
        <Modal
          isOpen={showRejectModal}
          onClose={() => {
            setShowRejectModal(false);
            setRejectingAppId(null);
            setRejectionReason('');
          }}
          title="Reject Application"
          size="md"
        >
          <div className="space-y-4">
            <p className="text-gray-700">
              Are you sure you want to reject this application? You can optionally provide a reason.
            </p>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Rejection Reason (Optional)
              </label>
              <textarea
                value={rejectionReason}
                onChange={(e) => setRejectionReason(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                rows={4}
                placeholder="e.g., Does not meet minimum qualifications, Position filled, etc."
              />
            </div>

            <div className="flex space-x-2">
              <Button
                variant="outline"
                className="flex-1"
                onClick={() => {
                  setShowRejectModal(false);
                  setRejectingAppId(null);
                  setRejectionReason('');
                }}
              >
                Cancel
              </Button>
              <Button
                variant="primary"
                className="flex-1 bg-red-600 hover:bg-red-700"
                onClick={handleRejectConfirm}
              >
                Confirm Rejection
              </Button>
            </div>
          </div>
        </Modal>
      )}

      {/* Schedule Interview Modal */}
      {showScheduleModal && schedulingApplication && (
        <Modal
          isOpen={showScheduleModal}
          onClose={() => {
            setShowScheduleModal(false);
            setSchedulingApplication(null);
            setScheduleError('');
            resetSchedule();
          }}
          title="Schedule Interview"
          size="lg"
        >
          <form onSubmit={handleSubmitSchedule(onScheduleSubmit)} className="space-y-4">
            {scheduleError && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                {scheduleError}
              </div>
            )}

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
              <p className="text-sm text-blue-900">
                <strong>Candidate:</strong> {schedulingApplication.applicant_name}
              </p>
              <p className="text-sm text-blue-900">
                <strong>Email:</strong> {schedulingApplication.applicant_email}
              </p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <Input
                label="Interview Date"
                type="date"
                {...registerSchedule('interview_date', { 
                  required: 'Date is required',
                  validate: (value) => {
                    const selectedDate = new Date(value);
                    const today = new Date();
                    today.setHours(0, 0, 0, 0);
                    return selectedDate >= today || 'Date cannot be in the past';
                  }
                })}
                error={scheduleErrors.interview_date?.message as string}
              />

              <Select
                label="Interview Time"
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
                {...registerSchedule('interview_time', { required: 'Time is required' })}
                error={scheduleErrors.interview_time?.message as string}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <Input
                label="Duration (minutes)"
                type="number"
                placeholder="60"
                defaultValue="60"
                {...registerSchedule('duration_minutes', { 
                  required: 'Duration is required',
                  min: { value: 15, message: 'Minimum 15 minutes' },
                  max: { value: 480, message: 'Maximum 8 hours' }
                })}
                error={scheduleErrors.duration_minutes?.message as string}
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
                {...registerSchedule('interview_type', { required: 'Interview type is required' })}
                error={scheduleErrors.interview_type?.message as string}
              />
            </div>

            <Input
              label="Meeting Link (for video interviews)"
              type="url"
              placeholder="https://zoom.us/j/..."
              {...registerSchedule('meeting_link')}
              error={scheduleErrors.meeting_link?.message as string}
            />

            <Input
              label="Meeting Location (for in-person interviews)"
              type="text"
              placeholder="123 Main St, Conference Room A"
              {...registerSchedule('meeting_location')}
              error={scheduleErrors.meeting_location?.message as string}
            />

            <Textarea
              label="Meeting Instructions (Optional)"
              placeholder="Please bring your ID, park in visitor lot, etc."
              {...registerSchedule('meeting_instructions')}
              error={scheduleErrors.meeting_instructions?.message as string}
              rows={3}
            />

            <Textarea
              label="Internal Notes (Optional)"
              placeholder="These notes are for your reference only and won't be shared with the candidate."
              {...registerSchedule('notes')}
              error={scheduleErrors.notes?.message as string}
              rows={2}
            />

            <div className="flex space-x-2 pt-4">
              <Button
                type="button"
                variant="outline"
                className="flex-1"
                onClick={() => {
                  setShowScheduleModal(false);
                  setSchedulingApplication(null);
                  setScheduleError('');
                  resetSchedule();
                }}
                disabled={isScheduling}
              >
                Cancel
              </Button>
              <Button
                type="submit"
                variant="primary"
                className="flex-1"
                disabled={isScheduling}
              >
                {isScheduling ? 'Scheduling...' : 'Schedule Interview'}
              </Button>
            </div>
          </form>
        </Modal>
      )}
    </DashboardLayout>
  );
}

