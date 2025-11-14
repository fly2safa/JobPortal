'use client';

import React from 'react';
import { Briefcase, MapPin, TrendingUp, CheckCircle } from 'lucide-react';
import Link from 'next/link';

interface RecommendationCardProps {
  recommendation: {
    job_id: string;
    job_title: string;
    company: string;
    match_score: number;
    match_reason: string;
    skills_alignment: string[];
    growth_potential: string;
  };
}

export const RecommendationCard: React.FC<RecommendationCardProps> = ({ recommendation }) => {
  const getMatchScoreColor = (score: number) => {
    if (score >= 90) return 'bg-green-500';
    if (score >= 75) return 'bg-blue-500';
    if (score >= 60) return 'bg-yellow-500';
    return 'bg-gray-500';
  };

  const getMatchScoreText = (score: number) => {
    if (score >= 90) return 'Excellent Match';
    if (score >= 75) return 'Great Match';
    if (score >= 60) return 'Good Match';
    return 'Fair Match';
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6 hover:bg-gray-750 transition-colors border border-gray-700">
      {/* Header with Match Score */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <Link href={`/jobs/${recommendation.job_id}`}>
            <h3 className="text-xl font-semibold text-white hover:text-primary transition-colors cursor-pointer">
              {recommendation.job_title}
            </h3>
          </Link>
          <div className="flex items-center text-gray-400 mt-1">
            <Briefcase size={16} className="mr-2" />
            <span>{recommendation.company}</span>
          </div>
        </div>
        
        <div className="flex flex-col items-end ml-4">
          <div className={`${getMatchScoreColor(recommendation.match_score)} text-white px-3 py-1 rounded-full text-sm font-bold`}>
            {recommendation.match_score}% Match
          </div>
          <span className="text-xs text-gray-400 mt-1">{getMatchScoreText(recommendation.match_score)}</span>
        </div>
      </div>

      {/* Match Reason */}
      <div className="mb-4">
        <p className="text-gray-300 text-sm leading-relaxed">
          {recommendation.match_reason}
        </p>
      </div>

      {/* Skills Alignment */}
      {recommendation.skills_alignment && recommendation.skills_alignment.length > 0 && (
        <div className="mb-4">
          <div className="flex items-center text-sm text-gray-400 mb-2">
            <CheckCircle size={16} className="mr-2 text-green-500" />
            <span className="font-medium">Your Matching Skills:</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {recommendation.skills_alignment.slice(0, 6).map((skill, index) => (
              <span
                key={index}
                className="bg-primary/20 text-primary px-3 py-1 rounded-full text-xs font-medium"
              >
                {skill}
              </span>
            ))}
            {recommendation.skills_alignment.length > 6 && (
              <span className="text-gray-400 text-xs py-1">
                +{recommendation.skills_alignment.length - 6} more
              </span>
            )}
          </div>
        </div>
      )}

      {/* Growth Potential */}
      <div className="flex items-center text-sm text-gray-400">
        <TrendingUp size={16} className="mr-2 text-blue-500" />
        <span className="font-medium mr-2">Growth Potential:</span>
        <span className="text-gray-300">{recommendation.growth_potential}</span>
      </div>

      {/* Action Button */}
      <div className="mt-4 pt-4 border-t border-gray-700">
        <Link href={`/jobs/${recommendation.job_id}`}>
          <button className="w-full bg-primary hover:bg-primary-dark text-white font-medium py-2 px-4 rounded-lg transition-colors">
            View Job Details
          </button>
        </Link>
      </div>
    </div>
  );
};

