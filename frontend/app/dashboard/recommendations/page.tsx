'use client';

import { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { useAuth } from '@/hooks/useAuth';
import { JobRecommendation } from '@/types';
import { Settings, RefreshCw, AlertCircle } from 'lucide-react';
import apiClient from '@/lib/api';
import { RecommendationsGrid, RecommendationsFilters } from '@/features/recommendations';

export default function RecommendationsPage() {
  useAuth(true);
  const [recommendations, setRecommendations] = useState<JobRecommendation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [savedJobs, setSavedJobs] = useState<Set<string>>(new Set());
  const [sortBy, setSortBy] = useState('match');
  const [error, setError] = useState<string | null>(null);
  
  // Filter states
  const [filters, setFilters] = useState({
    workingSchedule: [] as string[],
    employmentType: [] as string[],
    minMatchScore: 30,
  });

  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [useAI, setUseAI] = useState(true);
  const [limit, setLimit] = useState(10);

  const fetchRecommendations = async () => {
    setIsLoading(true);
    setError(null);
    try {
      // Calculate min_score from filter (convert percentage to decimal)
      const minScore = filters.minMatchScore / 100;
      
      const response = await apiClient.getJobRecommendations();
      setRecommendations(response || []);
      
      if (!response || response.length === 0) {
        setError('No recommendations available. Please update your profile with skills and experience.');
      }
    } catch (error: any) {
      console.error('Failed to fetch recommendations:', error);
      const errorMessage = error.response?.data?.detail || 'Failed to fetch recommendations. Please try again later.';
      setError(errorMessage);
      setRecommendations([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const handleFilterChange = (category: string, value: string) => {
    setFilters(prev => ({
      ...prev,
      [category]: prev[category as keyof typeof prev].includes(value)
        ? (prev[category as keyof typeof prev] as string[]).filter((v: string) => v !== value)
        : [...(prev[category as keyof typeof prev] as string[]), value]
    }));
  };

  const handleMinScoreChange = (score: number) => {
    setFilters(prev => ({
      ...prev,
      minMatchScore: score
    }));
  };

  // Apply filters to recommendations
  const filteredRecommendations = recommendations.filter(rec => {
    // Filter by minimum match score
    if (rec.match_score < filters.minMatchScore / 100) {
      return false;
    }
    
    // Filter by working schedule (job type)
    if (filters.workingSchedule.length > 0) {
      const jobTypeMatch = filters.workingSchedule.some(schedule => {
        const jobType = rec.job.job_type?.toLowerCase().replace('_', '-');
        return schedule.toLowerCase().includes(jobType) || jobType.includes(schedule.toLowerCase());
      });
      if (!jobTypeMatch) return false;
    }
    
    // Filter by employment type (remote, location)
    if (filters.employmentType.length > 0) {
      const employmentMatch = filters.employmentType.some(type => {
        if (type === 'remote' && rec.job.is_remote) return true;
        // Add more employment type matching logic as needed
        return false;
      });
      if (!employmentMatch && filters.employmentType.length > 0) return false;
    }
    
    return true;
  });

  // Sort recommendations
  const sortedRecommendations = [...filteredRecommendations].sort((a, b) => {
    switch (sortBy) {
      case 'match':
        return b.match_score - a.match_score;
      case 'salary':
        return (b.job.salary_max || 0) - (a.job.salary_max || 0);
      case 'date':
        return new Date(b.job.posted_date || b.job.created_at).getTime() - 
               new Date(a.job.posted_date || a.job.created_at).getTime();
      default:
        return b.match_score - a.match_score;
    }
  });

  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      
      <div className="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">
                Job Recommendations
              </h1>
              <p className="text-gray-600">
                AI-powered job matches based on your profile
              </p>
            </div>
            <button
              onClick={fetchRecommendations}
              disabled={isLoading}
              className="flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <RefreshCw size={18} className={isLoading ? 'animate-spin' : ''} />
              Refresh
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg flex items-start gap-3">
            <AlertCircle size={20} className="text-yellow-600 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-yellow-800 mb-1">Notice</h3>
              <p className="text-sm text-yellow-700">{error}</p>
            </div>
          </div>
        )}

        <div className="flex gap-6">
          {/* Sidebar Filters */}
          <aside className="w-64 flex-shrink-0">
            <RecommendationsFilters
              filters={filters}
              onFilterChange={handleFilterChange}
              onMinScoreChange={handleMinScoreChange}
            />
          </aside>

          {/* Main Content */}
          <div className="flex-1">
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">
                {filteredRecommendations.length} {filteredRecommendations.length === 1 ? 'Match' : 'Matches'} Found
              </h2>
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-600">Sort by:</span>
                <select
                  className="px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-primary cursor-pointer"
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                >
                  <option value="match">Best match</option>
                  <option value="salary">Highest salary</option>
                  <option value="date">Most recent</option>
                </select>
                <Settings size={20} className="text-gray-600 cursor-pointer hover:text-primary transition-colors" />
              </div>
            </div>

            {/* Recommendations Grid */}
            <RecommendationsGrid
              recommendations={sortedRecommendations}
              savedJobIds={savedJobs}
              onToggleSave={toggleSaveJob}
              isLoading={isLoading}
            />
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

