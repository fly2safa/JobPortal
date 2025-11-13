'use client';

import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Modal } from '@/components/ui/Modal';
import { CandidateRecommendation } from '@/types';
import { CandidateRecommendationCard } from './CandidateRecommendationCard';
import { 
  Sparkles, 
  AlertCircle, 
  RefreshCw, 
  Filter,
  Users,
  TrendingUp
} from 'lucide-react';
import apiClient from '@/lib/api';

interface CandidateRecommendationsListProps {
  jobId: string;
  jobTitle?: string;
}

export function CandidateRecommendationsList({
  jobId,
  jobTitle = 'this position',
}: CandidateRecommendationsListProps) {
  const [recommendations, setRecommendations] = useState<CandidateRecommendation[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedCandidate, setSelectedCandidate] = useState<any>(null);
  const [showModal, setShowModal] = useState(false);
  const [minScore, setMinScore] = useState(0.3);
  const [limit, setLimit] = useState(20);
  const [includeApplied, setIncludeApplied] = useState(false);

  useEffect(() => {
    fetchRecommendations();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [jobId, minScore, includeApplied]);

  const fetchRecommendations = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const params = {
        limit,
        min_score: minScore,
        include_applied: includeApplied,
      };
      
      const response = await apiClient.getCandidateRecommendations(jobId, params);
      setRecommendations(response || []);
    } catch (error: any) {
      console.error('Failed to fetch candidate recommendations:', error);
      setError(
        error.response?.data?.detail || 
        'Failed to load candidate recommendations. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleViewProfile = (candidate: any) => {
    setSelectedCandidate(candidate);
    setShowModal(true);
  };

  const getScoreDistribution = () => {
    const distribution = {
      excellent: 0, // >= 0.8
      good: 0,      // 0.6-0.79
      fair: 0,      // 0.4-0.59
      low: 0,       // < 0.4
    };

    recommendations.forEach(rec => {
      if (rec.match_score >= 0.8) distribution.excellent++;
      else if (rec.match_score >= 0.6) distribution.good++;
      else if (rec.match_score >= 0.4) distribution.fair++;
      else distribution.low++;
    });

    return distribution;
  };

  const distribution = getScoreDistribution();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
            <Sparkles className="text-white" size={24} />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900 flex items-center">
              AI-Recommended Candidates
            </h2>
            <p className="text-sm text-gray-600">
              Top matches for {jobTitle}
            </p>
          </div>
        </div>

        <Button
          variant="outline"
          size="sm"
          onClick={fetchRecommendations}
          disabled={isLoading}
        >
          <RefreshCw size={16} className={`mr-2 ${isLoading ? 'animate-spin' : ''}`} />
          Refresh
        </Button>
      </div>

      {/* Stats Cards */}
      {!isLoading && recommendations.length > 0 && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card className="text-center">
            <div className="flex items-center justify-center space-x-2 mb-2">
              <Users className="text-purple-600" size={20} />
              <p className="text-2xl font-bold text-gray-900">{recommendations.length}</p>
            </div>
            <p className="text-xs text-gray-600">Total Matches</p>
          </Card>
          
          <Card className="text-center bg-green-50 border-green-200">
            <div className="flex items-center justify-center space-x-2 mb-2">
              <TrendingUp className="text-green-600" size={20} />
              <p className="text-2xl font-bold text-green-600">{distribution.excellent}</p>
            </div>
            <p className="text-xs text-gray-600">Excellent (80%+)</p>
          </Card>
          
          <Card className="text-center bg-blue-50 border-blue-200">
            <p className="text-2xl font-bold text-blue-600 mb-2">{distribution.good}</p>
            <p className="text-xs text-gray-600">Good (60-79%)</p>
          </Card>
          
          <Card className="text-center bg-yellow-50 border-yellow-200">
            <p className="text-2xl font-bold text-yellow-600 mb-2">{distribution.fair}</p>
            <p className="text-xs text-gray-600">Fair (40-59%)</p>
          </Card>
        </div>
      )}

      {/* Filters */}
      <Card>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Filter size={16} className="text-gray-400" />
            <div>
              <label className="text-sm font-medium text-gray-700 mr-2">
                Minimum Match Score:
              </label>
              <select
                value={minScore}
                onChange={(e) => setMinScore(parseFloat(e.target.value))}
                className="text-sm border border-gray-300 rounded px-3 py-1 focus:outline-none focus:ring-2 focus:ring-primary"
              >
                <option value="0.7">70% and above</option>
                <option value="0.6">60% and above</option>
                <option value="0.5">50% and above</option>
                <option value="0.4">40% and above</option>
                <option value="0.3">30% and above</option>
              </select>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id="includeApplied"
              checked={includeApplied}
              onChange={(e) => setIncludeApplied(e.target.checked)}
              className="rounded border-gray-300 text-primary focus:ring-primary"
            />
            <label htmlFor="includeApplied" className="text-sm text-gray-700">
              Include candidates who already applied
            </label>
          </div>
        </div>
      </Card>

      {/* Error State */}
      {error && (
        <Card className="bg-red-50 border-red-200">
          <div className="flex items-center space-x-3">
            <AlertCircle className="text-red-600" size={24} />
            <div className="flex-1">
              <p className="font-semibold text-red-900">Error Loading Recommendations</p>
              <p className="text-sm text-red-700">{error}</p>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={fetchRecommendations}
              className="border-red-300 text-red-600 hover:bg-red-50"
            >
              Try Again
            </Button>
          </div>
        </Card>
      )}

      {/* Loading State */}
      {isLoading ? (
        <div className="flex flex-col items-center justify-center py-20">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-primary mb-4"></div>
          <p className="text-gray-600">Finding the best candidates...</p>
        </div>
      ) : recommendations.length === 0 ? (
        <Card className="text-center py-12">
          <Sparkles className="mx-auto text-gray-400 mb-4" size={48} />
          <p className="text-gray-600 mb-2 font-semibold">No Matching Candidates Found</p>
          <p className="text-sm text-gray-500 mb-4">
            Try adjusting the minimum match score or check back later as more candidates join.
          </p>
          {minScore > 0.3 && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => setMinScore(0.3)}
            >
              Lower Match Score Threshold
            </Button>
          )}
        </Card>
      ) : (
        <div className="grid gap-4">
          {recommendations.map((recommendation, index) => (
            <CandidateRecommendationCard
              key={`${recommendation.candidate.id}-${index}`}
              recommendation={recommendation}
              onViewProfile={handleViewProfile}
              showScore={true}
            />
          ))}
        </div>
      )}

      {/* Candidate Profile Modal */}
      {selectedCandidate && (
        <Modal
          isOpen={showModal}
          onClose={() => {
            setShowModal(false);
            setSelectedCandidate(null);
          }}
          title="Candidate Profile"
          size="lg"
        >
          <div className="space-y-6">
            {/* Basic Info */}
            <div>
              <h3 className="font-semibold text-lg mb-3">
                {selectedCandidate.first_name} {selectedCandidate.last_name}
              </h3>
              <div className="bg-gray-50 rounded-lg p-4 space-y-2">
                <p className="text-sm"><strong>Email:</strong> {selectedCandidate.email}</p>
                {selectedCandidate.phone && (
                  <p className="text-sm"><strong>Phone:</strong> {selectedCandidate.phone}</p>
                )}
                {selectedCandidate.location && (
                  <p className="text-sm"><strong>Location:</strong> {selectedCandidate.location}</p>
                )}
                {selectedCandidate.job_title && (
                  <p className="text-sm"><strong>Current Title:</strong> {selectedCandidate.job_title}</p>
                )}
                {selectedCandidate.experience_years !== undefined && (
                  <p className="text-sm"><strong>Experience:</strong> {selectedCandidate.experience_years} years</p>
                )}
              </div>
            </div>

            {/* Skills */}
            {selectedCandidate.skills && selectedCandidate.skills.length > 0 && (
              <div>
                <h3 className="font-semibold mb-2">Skills</h3>
                <div className="flex flex-wrap gap-2">
                  {selectedCandidate.skills.map((skill: string, index: number) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Education */}
            {selectedCandidate.education && (
              <div>
                <h3 className="font-semibold mb-2">Education</h3>
                <div className="bg-gray-50 rounded-lg p-4">
                  <p className="text-sm text-gray-700">{selectedCandidate.education}</p>
                </div>
              </div>
            )}

            {/* Bio */}
            {selectedCandidate.bio && (
              <div>
                <h3 className="font-semibold mb-2">About</h3>
                <div className="bg-gray-50 rounded-lg p-4 max-h-64 overflow-y-auto">
                  <p className="text-sm text-gray-700 whitespace-pre-line">
                    {selectedCandidate.bio}
                  </p>
                </div>
              </div>
            )}

            {/* Links */}
            <div className="flex flex-wrap gap-2">
              <Button
                variant="primary"
                onClick={() => window.open(`mailto:${selectedCandidate.email}`, '_blank')}
              >
                Contact Candidate
              </Button>
              {selectedCandidate.linkedin_url && (
                <Button
                  variant="outline"
                  onClick={() => window.open(selectedCandidate.linkedin_url, '_blank')}
                >
                  View LinkedIn
                </Button>
              )}
              {selectedCandidate.portfolio_url && (
                <Button
                  variant="outline"
                  onClick={() => window.open(selectedCandidate.portfolio_url, '_blank')}
                >
                  View Portfolio
                </Button>
              )}
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
}

