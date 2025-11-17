'use client';

import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { formatDate } from '@/lib/utils';
import { Eye, CheckCircle, X, Calendar, FileText, Mail } from 'lucide-react';

interface CandidateCardProps {
  application: any;
  onViewDetails: (application: any) => void;
  onShortlist: (id: string) => void;
  onReject: (id: string) => void;
  onStartReview: (id: string) => void;
  onScheduleInterview: (id: string) => void;
}

export function CandidateCard({
  application,
  onViewDetails,
  onShortlist,
  onReject,
  onStartReview,
  onScheduleInterview,
}: CandidateCardProps) {
  const getStatusBadgeVariant = (status: string) => {
    switch (status) {
      case 'shortlisted':
        return 'success';
      case 'rejected':
        return 'danger';
      case 'reviewing':
        return 'info';
      case 'interview':
        return 'success';
      case 'accepted':
        return 'success';
      default:
        return 'warning';
    }
  };

  const getInitials = (name: string) => {
    if (!name) return '??';
    const parts = name.split(' ');
    if (parts.length >= 2) {
      return `${parts[0][0]}${parts[1][0]}`.toUpperCase();
    }
    return name.slice(0, 2).toUpperCase();
  };

  return (
    <Card hover className="transition-all duration-200">
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-4 flex-1">
          {/* Avatar */}
          <div className="w-16 h-16 bg-gradient-to-br from-primary to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-xl flex-shrink-0 shadow-md">
            {getInitials(application.applicant_name)}
          </div>

          <div className="flex-1">
            {/* Header */}
            <div className="flex items-start justify-between mb-2">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">
                  {application.applicant_name}
                </h3>
                <p className="text-sm text-gray-600 flex items-center">
                  <Mail size={14} className="mr-1" />
                  {application.applicant_email}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  Applied {formatDate(application.applied_at || application.applied_date || application.updated_at)}
                </p>
              </div>
              <Badge variant={getStatusBadgeVariant(application.status)}>
                {application.status}
              </Badge>
            </div>

            {/* Resume Link */}
            {application.resume_url && (
              <div className="mb-3">
                <a
                  href={application.resume_url.startsWith('http') 
                    ? application.resume_url 
                    : `http://localhost:8000${application.resume_url}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-primary hover:underline flex items-center"
                >
                  <FileText size={14} className="mr-1" />
                  View Resume
                </a>
              </div>
            )}

            {/* Cover Letter Preview */}
            {application.cover_letter && (
              <div className="mb-3 p-3 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-700 line-clamp-2">
                  {application.cover_letter}
                </p>
              </div>
            )}

            {/* Employer Notes */}
            {application.employer_notes && (
              <div className="mb-3 p-3 bg-blue-50 rounded-lg border border-blue-200">
                <p className="text-xs font-semibold text-blue-900 mb-1">Employer Notes:</p>
                <p className="text-sm text-blue-800">{application.employer_notes}</p>
              </div>
            )}

            {/* Rejection Reason */}
            {application.rejection_reason && (
              <div className="mb-3 p-3 bg-red-50 rounded-lg border border-red-200">
                <p className="text-xs font-semibold text-red-900 mb-1">Rejection Reason:</p>
                <p className="text-sm text-red-800">{application.rejection_reason}</p>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex flex-wrap gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => onViewDetails(application)}
              >
                <Eye size={14} className="mr-1" />
                View Details
              </Button>

              {application.status === 'pending' && (
                <Button
                  variant="primary"
                  size="sm"
                  onClick={() => onStartReview(application.id)}
                >
                  Start Review
                </Button>
              )}

              {application.status === 'reviewing' && (
                <>
                  <Button
                    variant="primary"
                    size="sm"
                    onClick={() => onShortlist(application.id)}
                  >
                    <CheckCircle size={14} className="mr-1" />
                    Shortlist
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => onReject(application.id)}
                    className="text-red-600 hover:bg-red-50 border-red-300"
                  >
                    <X size={14} className="mr-1" />
                    Reject
                  </Button>
                </>
              )}

              {application.status === 'shortlisted' && (
                <Button
                  variant="primary"
                  size="sm"
                  onClick={() => onScheduleInterview(application.id)}
                >
                  <Calendar size={14} className="mr-1" />
                  Schedule Interview
                </Button>
              )}
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
}

