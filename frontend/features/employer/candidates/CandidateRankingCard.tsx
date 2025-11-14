'use client';

import React from 'react';
import { User, Briefcase, Award, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';

interface CandidateRankingCardProps {
  candidate: {
    candidate_id: string;
    candidate_name: string;
    current_role: string;
    match_score: number;
    match_reason: string;
    skills_match: {
      matched: string[];
      missing: string[];
      additional: string[];
    };
    experience_relevance: string;
    concerns: string;
  };
  rank: number;
}

export const CandidateRankingCard: React.FC<CandidateRankingCardProps> = ({ candidate, rank }) => {
  const getMatchScoreColor = (score: number) => {
    if (score >= 90) return 'bg-green-500';
    if (score >= 75) return 'bg-blue-500';
    if (score >= 60) return 'bg-yellow-500';
    return 'bg-orange-500';
  };

  const getMatchScoreTextColor = (score: number) => {
    if (score >= 90) return 'text-green-500';
    if (score >= 75) return 'text-blue-500';
    if (score >= 60) return 'text-yellow-500';
    return 'text-orange-500';
  };

  const getRankBadgeColor = (rank: number) => {
    if (rank === 1) return 'bg-yellow-500 text-gray-900';
    if (rank === 2) return 'bg-gray-400 text-gray-900';
    if (rank === 3) return 'bg-orange-600 text-white';
    return 'bg-gray-700 text-gray-300';
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 hover:border-primary/50 transition-colors">
      {/* Header with Rank and Match Score */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-start space-x-4">
          {/* Rank Badge */}
          <div className={`${getRankBadgeColor(rank)} w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg flex-shrink-0`}>
            {rank}
          </div>
          
          {/* Candidate Info */}
          <div className="flex-1">
            <h3 className="text-xl font-semibold text-white flex items-center">
              <User size={20} className="mr-2 text-gray-400" />
              {candidate.candidate_name}
            </h3>
            <div className="flex items-center text-gray-400 mt-1">
              <Briefcase size={16} className="mr-2" />
              <span>{candidate.current_role}</span>
            </div>
          </div>
        </div>
        
        {/* Match Score */}
        <div className="flex flex-col items-end ml-4">
          <div className={`${getMatchScoreColor(candidate.match_score)} text-white px-4 py-2 rounded-lg text-lg font-bold`}>
            {candidate.match_score}%
          </div>
          <span className={`text-sm font-medium mt-1 ${getMatchScoreTextColor(candidate.match_score)}`}>
            Match Score
          </span>
        </div>
      </div>

      {/* Match Reason */}
      <div className="mb-4 bg-gray-750 rounded-lg p-4">
        <h4 className="text-sm font-medium text-gray-400 mb-2">Why This Candidate?</h4>
        <p className="text-gray-300 text-sm leading-relaxed">
          {candidate.match_reason}
        </p>
      </div>

      {/* Skills Match */}
      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-400 mb-3">Skills Analysis</h4>
        
        {/* Matched Skills */}
        {candidate.skills_match.matched.length > 0 && (
          <div className="mb-3">
            <div className="flex items-center text-xs text-green-500 mb-2">
              <CheckCircle size={14} className="mr-1" />
              <span className="font-medium">Matching Skills ({candidate.skills_match.matched.length})</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {candidate.skills_match.matched.map((skill, index) => (
                <span
                  key={index}
                  className="bg-green-500/20 text-green-400 px-2 py-1 rounded text-xs font-medium"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Missing Skills */}
        {candidate.skills_match.missing.length > 0 && (
          <div className="mb-3">
            <div className="flex items-center text-xs text-red-500 mb-2">
              <XCircle size={14} className="mr-1" />
              <span className="font-medium">Missing Skills ({candidate.skills_match.missing.length})</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {candidate.skills_match.missing.map((skill, index) => (
                <span
                  key={index}
                  className="bg-red-500/20 text-red-400 px-2 py-1 rounded text-xs font-medium"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Additional Skills */}
        {candidate.skills_match.additional.length > 0 && (
          <div>
            <div className="flex items-center text-xs text-blue-500 mb-2">
              <Award size={14} className="mr-1" />
              <span className="font-medium">Bonus Skills ({candidate.skills_match.additional.length})</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {candidate.skills_match.additional.slice(0, 5).map((skill, index) => (
                <span
                  key={index}
                  className="bg-blue-500/20 text-blue-400 px-2 py-1 rounded text-xs font-medium"
                >
                  {skill}
                </span>
              ))}
              {candidate.skills_match.additional.length > 5 && (
                <span className="text-gray-400 text-xs py-1">
                  +{candidate.skills_match.additional.length - 5} more
                </span>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Experience Relevance */}
      <div className="mb-4 flex items-start text-sm">
        <Briefcase size={16} className="mr-2 text-gray-400 flex-shrink-0 mt-0.5" />
        <div>
          <span className="text-gray-400 font-medium">Experience: </span>
          <span className="text-gray-300">{candidate.experience_relevance}</span>
        </div>
      </div>

      {/* Concerns */}
      {candidate.concerns && candidate.concerns.toLowerCase() !== 'none' && (
        <div className="mb-4 bg-orange-500/10 border border-orange-500/30 rounded-lg p-3 flex items-start">
          <AlertTriangle size={16} className="text-orange-500 mr-2 flex-shrink-0 mt-0.5" />
          <div>
            <span className="text-orange-500 font-medium text-sm">Potential Concerns: </span>
            <span className="text-orange-400 text-sm">{candidate.concerns}</span>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex gap-3 pt-4 border-t border-gray-700">
        <button className="flex-1 bg-primary hover:bg-primary-dark text-white font-medium py-2 px-4 rounded-lg transition-colors">
          View Profile
        </button>
        <button className="flex-1 bg-gray-700 hover:bg-gray-600 text-white font-medium py-2 px-4 rounded-lg transition-colors">
          Contact Candidate
        </button>
      </div>
    </div>
  );
};

