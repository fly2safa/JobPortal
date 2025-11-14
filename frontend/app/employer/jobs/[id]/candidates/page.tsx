'use client';

import { useParams, useRouter } from 'next/navigation';
import { useAuth, useRequireRole } from '@/hooks/useAuth';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Button } from '@/components/ui/Button';
import { CandidateRecommendationsList } from '@/features/employer/candidate-recommendations';
import { ArrowLeft } from 'lucide-react';
import { useState, useEffect } from 'react';
import apiClient from '@/lib/api';

export default function JobCandidateRecommendationsPage() {
  useAuth(true);
  useRequireRole(['employer']);
  const params = useParams();
  const router = useRouter();
  const [jobTitle, setJobTitle] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchJobDetails();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [params.id]);

  const fetchJobDetails = async () => {
    try {
      const job = await apiClient.getJobById(params.id as string);
      setJobTitle(job.title || '');
    } catch (error) {
      console.error('Failed to fetch job details:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Back Button */}
        <Button
          variant="outline"
          size="sm"
          onClick={() => router.push(`/employer/jobs/${params.id}/applications`)}
        >
          <ArrowLeft size={16} className="mr-2" />
          Back to Applications
        </Button>

        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">
            AI Candidate Recommendations
          </h1>
          <p className="text-white">
            {isLoading ? 'Loading...' : `Best matching candidates for ${jobTitle}`}
          </p>
        </div>

        {/* Recommendations List */}
        {!isLoading && (
          <CandidateRecommendationsList 
            jobId={params.id as string}
            jobTitle={jobTitle}
          />
        )}
      </div>
    </DashboardLayout>
  );
}

