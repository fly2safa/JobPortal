'use client';

import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { CandidateRecommendation } from '@/types';
import { 
  User, 
  Mail, 
  MapPin, 
  Briefcase, 
  GraduationCap,
  Star,
  Sparkles,
  ExternalLink,
  FileText
} from 'lucide-react';

interface CandidateRecommendationCardProps {
  recommendation: CandidateRecommendation;
  onViewProfile?: (candidate: any) => void;
  showScore?: boolean;
}

export function CandidateRecommendationCard({
  recommendation,
  onViewProfile,
  showScore = true,
}: CandidateRecommendationCardProps) {
  const { candidate, match_score, reasons } = recommendation;

  const getInitials = (firstName: string, lastName: string) => {
    return `${firstName[0]}${lastName[0]}`.toUpperCase();
  };

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600 bg-green-100';
    if (score >= 0.6) return 'text-blue-600 bg-blue-100';
    if (score >= 0.4) return 'text-yellow-600 bg-yellow-100';
    return 'text-gray-600 bg-gray-100';
  };

  const getScoreBadge = (score: number) => {
    const percentage = Math.round(score * 100);
    return (
      <div className={`flex items-center space-x-1 px-3 py-1 rounded-full ${getScoreColor(score)}`}>
        <Star size={14} fill="currentColor" />
        <span className="text-sm font-bold">{percentage}%</span>
      </div>
    );
  };

  return (
    <Card hover className="transition-all duration-200">
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-4 flex-1">
          {/* Avatar */}
          <div className="relative">
            <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center text-white font-bold text-xl flex-shrink-0 shadow-md">
              {getInitials(candidate.first_name, candidate.last_name)}
            </div>
            {showScore && match_score >= 0.8 && (
              <div className="absolute -top-1 -right-1 w-6 h-6 bg-yellow-400 rounded-full flex items-center justify-center shadow-lg">
                <Sparkles size={14} className="text-white" />
              </div>
            )}
          </div>

          <div className="flex-1">
            {/* Header */}
            <div className="flex items-start justify-between mb-2">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                  {candidate.first_name} {candidate.last_name}
                  {showScore && getScoreBadge(match_score)}
                </h3>
                <p className="text-sm text-gray-600 flex items-center mt-1">
                  <Mail size={14} className="mr-1" />
                  {candidate.email}
                </p>
              </div>
            </div>

            {/* Profile Details */}
            <div className="space-y-2 mb-3">
              {candidate.job_title && (
                <div className="flex items-center text-sm text-gray-700">
                  <Briefcase size={14} className="mr-2 text-gray-400" />
                  <span>{candidate.job_title}</span>
                </div>
              )}
              
              {candidate.location && (
                <div className="flex items-center text-sm text-gray-700">
                  <MapPin size={14} className="mr-2 text-gray-400" />
                  <span>{candidate.location}</span>
                </div>
              )}
              
              {candidate.experience_years !== undefined && candidate.experience_years !== null && (
                <div className="flex items-center text-sm text-gray-700">
                  <User size={14} className="mr-2 text-gray-400" />
                  <span>{candidate.experience_years} years of experience</span>
                </div>
              )}
              
              {candidate.education && (
                <div className="flex items-center text-sm text-gray-700">
                  <GraduationCap size={14} className="mr-2 text-gray-400" />
                  <span>{candidate.education}</span>
                </div>
              )}
            </div>

            {/* Skills */}
            {candidate.skills && candidate.skills.length > 0 && (
              <div className="mb-3">
                <p className="text-xs font-semibold text-gray-600 mb-2">Skills:</p>
                <div className="flex flex-wrap gap-2">
                  {candidate.skills.slice(0, 6).map((skill, index) => (
                    <Badge key={index} variant="secondary" className="text-xs">
                      {skill}
                    </Badge>
                  ))}
                  {candidate.skills.length > 6 && (
                    <Badge variant="secondary" className="text-xs">
                      +{candidate.skills.length - 6} more
                    </Badge>
                  )}
                </div>
              </div>
            )}

            {/* Bio */}
            {candidate.bio && (
              <div className="mb-3 p-3 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-700 line-clamp-2">
                  {candidate.bio}
                </p>
              </div>
            )}

            {/* Match Reasons */}
            {reasons && reasons.length > 0 && (
              <div className="mb-3 p-3 bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg border border-purple-200">
                <p className="text-xs font-semibold text-purple-900 mb-2 flex items-center">
                  <Sparkles size={12} className="mr-1" />
                  Why this candidate matches:
                </p>
                <ul className="space-y-1">
                  {reasons.map((reason, index) => (
                    <li key={index} className="text-sm text-purple-800 flex items-start">
                      <span className="mr-2">•</span>
                      <span>{reason}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex flex-wrap gap-2">
              {onViewProfile && (
                <Button
                  variant="primary"
                  size="sm"
                  onClick={() => onViewProfile(candidate)}
                >
                  <User size={14} className="mr-1" />
                  View Full Profile
                </Button>
              )}
              
              {candidate.linkedin_url && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => window.open(candidate.linkedin_url, '_blank')}
                >
                  <ExternalLink size={14} className="mr-1" />
                  LinkedIn
                </Button>
              )}
              
              {candidate.portfolio_url && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => window.open(candidate.portfolio_url, '_blank')}
                >
                  <ExternalLink size={14} className="mr-1" />
                  Portfolio
                </Button>
              )}

              <Button
                variant="outline"
                size="sm"
                onClick={() => window.open(`mailto:${candidate.email}`, '_blank')}
              >
                <Mail size={14} className="mr-1" />
                Contact
              </Button>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
}

