'use client';

import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { JobRecommendation } from '@/types';
import { formatTimeAgo, formatSalary } from '@/lib/utils';
import { MapPin, Briefcase, Clock, DollarSign, TrendingUp, Sparkles } from 'lucide-react';

interface RecommendationCardProps {
  recommendation: JobRecommendation;
}

export function RecommendationCard({ recommendation }: RecommendationCardProps) {
  const { job, match_score, reasons } = recommendation;
  
  // Determine match score color
  const getMatchColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-blue-600';
    if (score >= 40) return 'text-yellow-600';
    return 'text-gray-600';
  };

  const getMatchBadgeVariant = (score: number): 'success' | 'primary' | 'warning' | 'default' => {
    if (score >= 80) return 'success';
    if (score >= 60) return 'primary';
    if (score >= 40) return 'warning';
    return 'default';
  };

  return (
    <Link href={`/jobs/${job.id}`}>
      <Card hover className="h-full transition-all duration-200 relative">
        {/* Match Score Badge */}
        <div className="absolute top-4 right-4 flex items-center gap-2">
          <div className={`text-2xl font-bold ${getMatchColor(match_score)}`}>
            {match_score}%
          </div>
          <Badge variant={getMatchBadgeVariant(match_score)} className="flex items-center gap-1">
            <TrendingUp size={14} />
            Match
          </Badge>
        </div>

        <div className="pr-24">
          <div className="flex justify-between items-start mb-3">
            <div>
              <h3 className="text-xl font-semibold text-gray-900 hover:text-primary transition-colors flex items-center gap-2">
                {job.title}
                <Sparkles size={16} className="text-primary" />
              </h3>
              <p className="text-gray-600 mt-1">{job.company_name || 'Company Name'}</p>
            </div>
            <Badge variant="primary">{job.job_type}</Badge>
          </div>

          <div className="space-y-2 mb-4">
            <div className="flex items-center text-sm text-gray-600">
              <MapPin size={16} className="mr-2" />
              {job.location}
            </div>
            <div className="flex items-center text-sm text-gray-600">
              <Briefcase size={16} className="mr-2" />
              {job.experience_level}
            </div>
            {(job.salary_min || job.salary_max) && (
              <div className="flex items-center text-sm text-gray-600">
                <DollarSign size={16} className="mr-2" />
                {formatSalary(job.salary_min, job.salary_max)}
              </div>
            )}
            <div className="flex items-center text-sm text-gray-500">
              <Clock size={16} className="mr-2" />
              {job.posted_date ? `Posted ${formatTimeAgo(job.posted_date)}` : 'Not posted yet'}
            </div>
          </div>

          <p className="text-gray-600 text-sm mb-4 line-clamp-2">
            {job.description}
          </p>

          {/* Match Reasons */}
          {reasons && reasons.length > 0 && (
            <div className="mb-4 p-3 bg-primary/5 rounded-lg border border-primary/20">
              <h4 className="text-sm font-semibold text-gray-900 mb-2 flex items-center gap-1">
                <Sparkles size={14} className="text-primary" />
                Why this matches:
              </h4>
              <ul className="space-y-1">
                {reasons.slice(0, 3).map((reason, index) => (
                  <li key={index} className="text-xs text-gray-700 flex items-start">
                    <span className="text-primary mr-2">•</span>
                    <span>{reason}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className="flex flex-wrap gap-2">
            {job.skills.slice(0, 4).map((skill) => (
              <Badge key={skill} variant="default">
                {skill}
              </Badge>
            ))}
            {job.skills.length > 4 && (
              <Badge variant="default">+{job.skills.length - 4} more</Badge>
            )}
          </div>
        </div>
      </Card>
    </Link>
  );
}








