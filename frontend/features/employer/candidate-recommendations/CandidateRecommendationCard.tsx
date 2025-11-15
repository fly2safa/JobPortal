'use client';

import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { CandidateRecommendation } from '@/types';
import { formatTimeAgo } from '@/lib/utils';
import { TrendingUp, Sparkles, Mail, FileText, User, Calendar } from 'lucide-react';

interface CandidateRecommendationCardProps {
  recommendation: CandidateRecommendation;
  onViewApplication?: (applicationId: string) => void;
  onShortlist?: (applicationId: string) => void;
  onScheduleInterview?: (applicationId: string) => void;
}

export function CandidateRecommendationCard({ 
  recommendation,
  onViewApplication,
  onShortlist,
  onScheduleInterview
}: CandidateRecommendationCardProps) {
  const { 
    full_name, 
    email, 
    match_score, 
    reasons, 
    application_id, 
    application_status,
    applied_at,
    resume 
  } = recommendation;
  
  // Determine match score color
  const getMatchColor = (score: number) => {
    if (score >= 80) return 'text-green-600 dark:text-green-400';
    if (score >= 60) return 'text-blue-600 dark:text-blue-400';
    if (score >= 40) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-gray-600 dark:text-gray-400';
  };

  const getMatchBadgeVariant = (score: number): 'success' | 'primary' | 'warning' | 'default' => {
    if (score >= 80) return 'success';
    if (score >= 60) return 'primary';
    if (score >= 40) return 'warning';
    return 'default';
  };

  const getStatusBadgeVariant = (status: string) => {
    switch (status) {
      case 'shortlisted':
        return 'success';
      case 'rejected':
        return 'danger';
      case 'reviewing':
        return 'info';
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
    <Card hover className="h-full transition-all duration-200 relative">
      {/* Match Score Badge */}
      <div className="absolute top-4 right-4 flex flex-col items-end gap-2">
        <div className={`text-2xl font-bold ${getMatchColor(match_score)}`}>
          {match_score}%
        </div>
        <Badge variant={getMatchBadgeVariant(match_score)} className="flex items-center gap-1">
          <TrendingUp size={14} />
          Match
        </Badge>
      </div>

      <div className="pr-24">
        {/* Candidate Header */}
        <div className="flex items-start gap-4 mb-4">
          {/* Avatar */}
          <div className="w-16 h-16 bg-gradient-to-br from-primary to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-xl flex-shrink-0 shadow-md">
            {getInitials(full_name)}
          </div>

          <div className="flex-1">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 flex items-center gap-2">
                  {full_name}
                  <Sparkles size={16} className="text-primary" />
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 flex items-center mt-1">
                  <Mail size={14} className="mr-1" />
                  {email}
                </p>
              </div>
              <Badge variant={getStatusBadgeVariant(application_status)}>
                {application_status}
              </Badge>
            </div>

            {applied_at && (
              <p className="text-xs text-gray-500 dark:text-gray-500 flex items-center">
                <Calendar size={12} className="mr-1" />
                Applied {formatTimeAgo(applied_at)}
              </p>
            )}
          </div>
        </div>

        {/* Resume Skills */}
        {resume && resume.skills && resume.skills.length > 0 && (
          <div className="mb-4">
            <p className="text-xs font-semibold text-gray-700 dark:text-gray-300 mb-2">Skills:</p>
            <div className="flex flex-wrap gap-2">
              {resume.skills.slice(0, 6).map((skill) => (
                <Badge key={skill} variant="default" className="text-xs">
                  {skill}
                </Badge>
              ))}
              {resume.skills.length > 6 && (
                <Badge variant="default" className="text-xs">
                  +{resume.skills.length - 6} more
                </Badge>
              )}
            </div>
          </div>
        )}

        {/* Match Reasons */}
        {reasons && reasons.length > 0 && (
          <div className="mb-4 p-3 bg-primary/5 dark:bg-primary/10 rounded-lg border border-primary/20">
            <h4 className="text-sm font-semibold text-gray-900 dark:text-gray-100 mb-2 flex items-center gap-1">
              <Sparkles size={14} className="text-primary" />
              Why this candidate matches:
            </h4>
            <ul className="space-y-1">
              {reasons.slice(0, 3).map((reason, index) => (
                <li key={index} className="text-xs text-gray-700 dark:text-gray-300 flex items-start">
                  <span className="text-primary mr-2">•</span>
                  <span>{reason}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Actions */}
        <div className="flex flex-wrap gap-2 pt-2 border-t border-gray-200 dark:border-gray-700">
          {resume && resume.file_url && (
            <a
              href={resume.file_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex"
            >
              <Button variant="outline" size="sm">
                <FileText size={14} className="mr-1" />
                View Resume
              </Button>
            </a>
          )}
          
          {onViewApplication && (
            <Button 
              variant="outline" 
              size="sm"
              onClick={() => onViewApplication(application_id)}
            >
              <User size={14} className="mr-1" />
              View Application
            </Button>
          )}

          {application_status === 'reviewing' && onShortlist && (
            <Button 
              variant="primary" 
              size="sm"
              onClick={() => onShortlist(application_id)}
            >
              Shortlist
            </Button>
          )}

          {application_status === 'shortlisted' && onScheduleInterview && (
            <Button 
              variant="primary" 
              size="sm"
              onClick={() => onScheduleInterview(application_id)}
            >
              <Calendar size={14} className="mr-1" />
              Schedule Interview
            </Button>
          )}
        </div>
      </div>
    </Card>
  );
}


