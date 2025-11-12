'use client';

import { JobRecommendation } from '@/types';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Bookmark, BookmarkCheck, MapPin, Calendar, Briefcase, DollarSign } from 'lucide-react';
import { formatDate } from '@/lib/utils';
import Link from 'next/link';

interface RecommendationCardProps {
  recommendation: JobRecommendation;
  isSaved?: boolean;
  onToggleSave?: (jobId: string) => void;
}

export function RecommendationCard({
  recommendation,
  isSaved = false,
  onToggleSave,
}: RecommendationCardProps) {
  const { job, match_score, reasons } = recommendation;

  // Convert match score to percentage for display
  const matchPercentage = Math.round(match_score * 100);

  // Determine match quality color
  const getMatchColor = () => {
    if (match_score >= 0.8) return 'text-green-600 bg-green-50';
    if (match_score >= 0.6) return 'text-blue-600 bg-blue-50';
    return 'text-yellow-600 bg-yellow-50';
  };

  return (
    <Card className="p-6 hover:shadow-lg transition-all duration-300 relative">
      {/* Bookmark Button */}
      {onToggleSave && (
        <button
          onClick={() => onToggleSave(job.id)}
          className="absolute top-4 right-4 p-2 hover:bg-gray-100 rounded-lg transition-colors z-10"
          aria-label={isSaved ? 'Unsave job' : 'Save job'}
        >
          {isSaved ? (
            <BookmarkCheck size={20} className="text-primary" />
          ) : (
            <Bookmark size={20} className="text-gray-400" />
          )}
        </button>
      )}

      {/* Match Score Badge */}
      <div className="mb-4">
        <Badge className={`${getMatchColor()} font-semibold`}>
          {matchPercentage}% Match
        </Badge>
      </div>

      {/* Job Title and Company */}
      <div className="mb-4">
        <h3 className="text-xl font-bold text-gray-900 mb-2">
          {job.title}
        </h3>
        <p className="text-lg text-gray-700 font-medium">
          {job.company_name}
        </p>
      </div>

      {/* Job Details */}
      <div className="space-y-2 mb-4">
        <div className="flex items-center text-gray-600">
          <MapPin size={16} className="mr-2" />
          <span className="text-sm">
            {job.location} {job.is_remote && '• Remote'}
          </span>
        </div>
        
        <div className="flex items-center text-gray-600">
          <Briefcase size={16} className="mr-2" />
          <span className="text-sm">
            {job.job_type.replace('_', ' ')} • {job.experience_level}
          </span>
        </div>

        {job.salary_max && (
          <div className="flex items-center text-gray-600">
            <DollarSign size={16} className="mr-2" />
            <span className="text-sm">
              {job.salary_min ? `$${job.salary_min.toLocaleString()} - ` : ''}
              ${job.salary_max.toLocaleString()}/{job.salary_currency || 'USD'}
            </span>
          </div>
        )}

        <div className="flex items-center text-gray-600">
          <Calendar size={16} className="mr-2" />
          <span className="text-sm">
            Posted {formatDate(job.posted_date || job.created_at)}
          </span>
        </div>
      </div>

      {/* Match Reasons */}
      {reasons && reasons.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-semibold text-gray-700 mb-2">
            Why this matches:
          </h4>
          <ul className="space-y-1">
            {reasons.map((reason, index) => (
              <li
                key={index}
                className="text-sm text-gray-600 flex items-start"
              >
                <span className="text-primary mr-2">•</span>
                <span>{reason}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Skills Tags */}
      {job.skills && job.skills.length > 0 && (
        <div className="mb-4">
          <div className="flex flex-wrap gap-2">
            {job.skills.slice(0, 4).map((skill, index) => (
              <Badge
                key={index}
                variant="secondary"
                className="text-xs"
              >
                {skill}
              </Badge>
            ))}
            {job.skills.length > 4 && (
              <Badge variant="secondary" className="text-xs">
                +{job.skills.length - 4} more
              </Badge>
            )}
          </div>
        </div>
      )}

      {/* View Details Button */}
      <Link href={`/jobs/${job.id}`} className="block">
        <button className="w-full py-2 px-4 bg-primary text-white rounded-lg font-semibold hover:bg-primary/90 transition-colors">
          View Details
        </button>
      </Link>
    </Card>
  );
}

