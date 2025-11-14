'use client';

import React, { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { Users, RefreshCw, AlertCircle, Loader2, Filter } from 'lucide-react';
import DashboardLayout from '@/components/layouts/DashboardLayout';
import { CandidateRankingCard } from '@/features/employer/candidates';
import { apiClient } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';

export default function CandidateRecommendationsPage() {
  useAuth(true); // Require authentication
  const params = useParams();
  const jobId = params.id as string;

  const [candidates, setCandidates] = useState<any[]>([]);
  const [jobTitle, setJobTitle] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [useAI, setUseAI] = useState(true);
  const [applicantsOnly, setApplicantsOnly] = useState(false);
  const [limit, setLimit] = useState(10);

  const fetchCandidates = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiClient.getRecommendedCandidates(jobId, {
        limit,
        use_ai: useAI,
        applicants_only: applicantsOnly
      });
      
      setCandidates(response.rankings || []);
      setJobTitle(response.job_title || '');
    } catch (err: any) {
      console.error('Error fetching candidate recommendations:', err);
      setError(err.response?.data?.detail || 'Failed to load candidate recommendations. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (jobId) {
      fetchCandidates();
    }
  }, [jobId]);

  const handleRefresh = () => {
    fetchCandidates();
  };

  const handleToggleAI = () => {
    setUseAI(!useAI);
  };

  const handleToggleApplicantsOnly = () => {
    setApplicantsOnly(!applicantsOnly);
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2 flex items-center">
              <Users className="mr-3 text-primary" size={32} />
              AI Candidate Recommendations
            </h1>
            <p className="text-gray-400">
              {jobTitle ? `For: ${jobTitle}` : 'Intelligent candidate rankings based on job requirements'}
            </p>
          </div>
          
          <button
            onClick={handleRefresh}
            disabled={loading}
            className="bg-primary hover:bg-primary-dark text-white font-medium py-2 px-4 rounded-lg transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <RefreshCw size={18} className={`mr-2 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </div>

        {/* Filters */}
        <div className="bg-gray-800 rounded-lg p-4 border border-gray-700 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-white font-medium mb-1">AI-Powered Ranking</h3>
              <p className="text-sm text-gray-400">
                Use advanced AI to analyze and rank candidates
              </p>
            </div>
            <button
              onClick={handleToggleAI}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                useAI ? 'bg-primary' : 'bg-gray-600'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  useAI ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>

          <div className="flex items-center justify-between pt-4 border-t border-gray-700">
            <div>
              <h3 className="text-white font-medium mb-1 flex items-center">
                <Filter size={16} className="mr-2" />
                Applicants Only
              </h3>
              <p className="text-sm text-gray-400">
                Only rank candidates who have already applied
              </p>
            </div>
            <button
              onClick={handleToggleApplicantsOnly}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                applicantsOnly ? 'bg-primary' : 'bg-gray-600'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  applicantsOnly ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-500/10 border border-red-500 rounded-lg p-4 flex items-start">
            <AlertCircle className="text-red-500 mr-3 flex-shrink-0 mt-0.5" size={20} />
            <div>
              <h4 className="text-red-500 font-medium mb-1">Error Loading Candidates</h4>
              <p className="text-red-400 text-sm">{error}</p>
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="flex flex-col items-center justify-center py-12">
            <Loader2 className="animate-spin text-primary mb-4" size={48} />
            <p className="text-gray-400">Analyzing candidates and calculating match scores...</p>
          </div>
        )}

        {/* Candidates List */}
        {!loading && !error && candidates.length > 0 && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-white">
                Top {candidates.length} {candidates.length === 1 ? 'Candidate' : 'Candidates'}
              </h2>
              <span className="text-sm text-gray-400">
                {useAI ? 'AI-Powered Rankings' : 'Skill-Based Rankings'}
                {applicantsOnly && ' • Applicants Only'}
              </span>
            </div>
            
            <div className="grid gap-4">
              {candidates.map((candidate, index) => (
                <CandidateRankingCard 
                  key={candidate.candidate_id || index} 
                  candidate={candidate}
                  rank={index + 1}
                />
              ))}
            </div>
          </div>
        )}

        {/* Empty State */}
        {!loading && !error && candidates.length === 0 && (
          <div className="bg-gray-800 rounded-lg p-12 text-center border border-gray-700">
            <Users className="mx-auto text-gray-600 mb-4" size={48} />
            <h3 className="text-xl font-semibold text-white mb-2">No Candidates Found</h3>
            <p className="text-gray-400 mb-6 max-w-md mx-auto">
              {applicantsOnly 
                ? "No applicants found for this job yet. Try disabling 'Applicants Only' to see potential candidates from the talent pool."
                : "We couldn't find any matching candidates at this time. Try adjusting your job requirements or check back later."}
            </p>
            {applicantsOnly && (
              <button
                onClick={handleToggleApplicantsOnly}
                className="bg-primary hover:bg-primary-dark text-white font-medium py-2 px-6 rounded-lg transition-colors"
              >
                View All Candidates
              </button>
            )}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

