import React from 'react';
import { Interview } from '@/types';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { formatDateTime } from '@/lib/utils';
import { Calendar, Clock, Video, MapPin, Phone, Users } from 'lucide-react';

interface InterviewCardProps {
  interview: Interview;
  isEmployer?: boolean;
  onJoin?: (interview: Interview) => void;
  onReschedule?: (interview: Interview) => void;
  onCancel?: (interview: Interview) => void;
  onComplete?: (interview: Interview) => void;
}

export const InterviewCard: React.FC<InterviewCardProps> = ({
  interview,
  isEmployer = false,
  onJoin,
  onReschedule,
  onCancel,
  onComplete,
}) => {
  const getStatusBadge = () => {
    switch (interview.status) {
      case 'scheduled':
      case 'rescheduled':
        return <Badge variant="success">Scheduled</Badge>;
      case 'completed':
        return <Badge variant="default">Completed</Badge>;
      case 'cancelled':
        return <Badge variant="danger">Cancelled</Badge>;
      case 'no_show':
        return <Badge variant="warning">No Show</Badge>;
      default:
        return <Badge variant="default">{interview.status}</Badge>;
    }
  };

  const getInterviewTypeIcon = () => {
    switch (interview.interview_type) {
      case 'video':
        return <Video size={16} className="mr-2" />;
      case 'phone':
        return <Phone size={16} className="mr-2" />;
      case 'in_person':
        return <MapPin size={16} className="mr-2" />;
      default:
        return <Users size={16} className="mr-2" />;
    }
  };

  const getInterviewTypeLabel = () => {
    const labels: Record<string, string> = {
      video: 'Video Call',
      phone: 'Phone Interview',
      in_person: 'In-Person',
      technical: 'Technical Interview',
      behavioral: 'Behavioral Interview',
      final: 'Final Interview',
    };
    return labels[interview.interview_type] || interview.interview_type;
  };

  const isUpcoming = interview.status === 'scheduled' || interview.status === 'rescheduled';
  const isPast = interview.status === 'completed' || interview.status === 'cancelled';

  return (
    <Card className={`border-l-4 ${isUpcoming ? 'border-primary' : 'border-gray-300'} ${isPast ? 'opacity-75' : ''}`}>
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900">
            {isEmployer ? interview.candidate_name : interview.job_title}
          </h3>
          <p className="text-sm text-gray-600">
            {isEmployer ? interview.job_title : `at ${interview.company_name}`}
          </p>
        </div>
        {getStatusBadge()}
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

        <div className="flex items-center text-sm text-gray-700">
          {getInterviewTypeIcon()}
          {getInterviewTypeLabel()}
        </div>

        {interview.meeting_link && (
          <div className="flex items-center text-sm">
            <Video size={16} className="mr-2" />
            <a
              href={interview.meeting_link}
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary hover:underline"
            >
              Join Meeting
            </a>
          </div>
        )}

        {interview.meeting_location && (
          <div className="flex items-center text-sm text-gray-700">
            <MapPin size={16} className="mr-2" />
            {interview.meeting_location}
          </div>
        )}
      </div>

      {interview.notes && isUpcoming && isEmployer && (
        <div className="bg-yellow-50 rounded-lg p-3 mb-4 border-l-4 border-yellow-400">
          <p className="text-sm font-medium text-yellow-900 mb-1">Internal Notes (Employer Only):</p>
          <p className="text-sm text-yellow-800">{interview.notes}</p>
        </div>
      )}

      {interview.meeting_instructions && isUpcoming && (
        <div className="bg-blue-50 rounded-lg p-3 mb-4 border-l-4 border-blue-400">
          <p className="text-sm font-medium text-blue-900 mb-1">Instructions:</p>
          <p className="text-sm text-blue-800">{interview.meeting_instructions}</p>
        </div>
      )}

      {interview.feedback && isPast && isEmployer && (
        <div className="bg-gray-50 rounded-lg p-3 mb-4">
          <p className="text-sm font-medium text-gray-900 mb-1">Interview Feedback (Employer Only):</p>
          <p className="text-sm text-gray-700">{interview.feedback}</p>
        </div>
      )}

      {isUpcoming && (
        <div className="flex space-x-2">
          {interview.meeting_link && onJoin && (
            <Button variant="primary" size="sm" onClick={() => onJoin(interview)}>
              <Video size={14} className="mr-1" />
              Join Interview
            </Button>
          )}
          {isEmployer && onReschedule && (
            <Button variant="outline" size="sm" onClick={() => onReschedule(interview)}>
              Reschedule
            </Button>
          )}
          {onCancel && (
            <Button 
              variant="ghost" 
              size="sm" 
              className="text-red-600 hover:text-red-700 hover:bg-red-50"
              onClick={() => onCancel(interview)}
            >
              Cancel
            </Button>
          )}
          {isEmployer && onComplete && interview.status !== 'completed' && (
            <Button variant="outline" size="sm" onClick={() => onComplete(interview)}>
              Mark Complete
            </Button>
          )}
        </div>
      )}
    </Card>
  );
};

