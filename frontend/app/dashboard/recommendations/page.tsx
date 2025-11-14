'use client';

import React, { useState, useEffect } from 'react';
import { Sparkles, RefreshCw, AlertCircle, Loader2 } from 'lucide-react';
import DashboardLayout from '@/components/layouts/DashboardLayout';
import { RecommendationCard } from '@/features/recommendations';
import { apiClient } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';

export default function RecommendationsPage() {
  useAuth(true); // Require authentication

  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [useAI, setUseAI] = useState(true);
  const [limit, setLimit] = useState(10);

  const fetchRecommendations = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiClient.getRecommendations({
        limit,
        use_ai: useAI
      });
      
      setRecommendations(response.recommendations || []);
    } catch (err: any) {
      console.error('Error fetching recommendations:', err);
      setError(err.response?.data?.detail || 'Failed to load recommendations. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const handleRefresh = () => {
    fetchRecommendations();
  };

  const handleToggleAI = () => {
    setUseAI(!useAI);
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2 flex items-center">
              <Sparkles className="mr-3 text-primary" size={32} />
              AI Job Recommendations
            </h1>
            <p className="text-gray-400">
              Personalized job matches based on your profile, skills, and experience
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

        {/* AI Toggle */}
        <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-white font-medium mb-1">AI-Powered Ranking</h3>
              <p className="text-sm text-gray-400">
                Use advanced AI to analyze and rank job matches
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
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-500/10 border border-red-500 rounded-lg p-4 flex items-start">
            <AlertCircle className="text-red-500 mr-3 flex-shrink-0 mt-0.5" size={20} />
            <div>
              <h4 className="text-red-500 font-medium mb-1">Error Loading Recommendations</h4>
              <p className="text-red-400 text-sm">{error}</p>
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="flex flex-col items-center justify-center py-12">
            <Loader2 className="animate-spin text-primary mb-4" size={48} />
            <p className="text-gray-400">Analyzing your profile and finding the best matches...</p>
          </div>
        )}

        {/* Recommendations List */}
        {!loading && !error && recommendations.length > 0 && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-white">
                {recommendations.length} Recommended {recommendations.length === 1 ? 'Job' : 'Jobs'}
              </h2>
              <span className="text-sm text-gray-400">
                {useAI ? 'AI-Powered Rankings' : 'Skill-Based Rankings'}
              </span>
            </div>
            
            <div className="grid gap-4">
              {recommendations.map((rec, index) => (
                <RecommendationCard key={rec.job_id || index} recommendation={rec} />
              ))}
            </div>
          </div>
        )}

        {/* Empty State */}
        {!loading && !error && recommendations.length === 0 && (
          <div className="bg-gray-800 rounded-lg p-12 text-center border border-gray-700">
            <Sparkles className="mx-auto text-gray-600 mb-4" size={48} />
            <h3 className="text-xl font-semibold text-white mb-2">No Recommendations Yet</h3>
            <p className="text-gray-400 mb-6 max-w-md mx-auto">
              We couldn't find any job recommendations at this time. Try updating your profile with more skills and experience to get better matches.
            </p>
            <button
              onClick={() => window.location.href = '/dashboard/profile'}
              className="bg-primary hover:bg-primary-dark text-white font-medium py-2 px-6 rounded-lg transition-colors"
            >
              Update Profile
            </button>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
