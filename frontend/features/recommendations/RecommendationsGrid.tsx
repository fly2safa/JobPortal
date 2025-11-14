'use client';

import { JobRecommendation } from '@/types';
import { RecommendationCard } from './RecommendationCard';

interface RecommendationsGridProps {
  recommendations: JobRecommendation[];
  savedJobIds: Set<string>;
  onToggleSave: (jobId: string) => void;
  isLoading?: boolean;
}

export function RecommendationsGrid({
  recommendations,
  savedJobIds,
  onToggleSave,
  isLoading = false,
}: RecommendationsGridProps) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div key={i} className="animate-pulse">
            <div className="bg-gray-200 rounded-2xl h-96"></div>
          </div>
        ))}
      </div>
    );
  }

  if (recommendations.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="max-w-md mx-auto">
          <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg
              className="w-12 h-12 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
              />
            </svg>
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-2">
            No recommendations found
          </h3>
          <p className="text-gray-600">
            We couldn't find any job recommendations matching your criteria.
            Try adjusting your filters or update your profile with more skills and experience.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {recommendations.map((recommendation) => (
        <RecommendationCard
          key={recommendation.job.id}
          recommendation={recommendation}
          isSaved={savedJobIds.has(recommendation.job.id)}
          onToggleSave={onToggleSave}
        />
      ))}
    </div>
  );
}

