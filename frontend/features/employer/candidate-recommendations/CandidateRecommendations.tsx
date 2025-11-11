import { useState, useEffect } from 'react';
import apiClient from '@/lib/api';
import { CandidateRecommendation } from '@/types';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Sparkles, User } from 'lucide-react';

interface CandidateRecommendationsProps {
  jobId: string;
}

export default function CandidateRecommendations({ jobId }: CandidateRecommendationsProps) {
  const [candidates, setCandidates] = useState<CandidateRecommendation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!jobId) return;
    fetchCandidates();
    // eslint-disable-next-line
  }, [jobId]);

  const fetchCandidates = async () => {
    setIsLoading(true);
    setError("");
    try {
      const response = await apiClient.getCandidateRecommendations(jobId);
      setCandidates(response.data || []);
    } catch (err) {
      setError("Could not load candidate recommendations. Please try again later.");
      setCandidates([]);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <Card className="flex justify-center py-8 bg-gradient-to-r from-purple-50 to-blue-50 border-purple-200">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary" />
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="bg-gradient-to-r from-purple-50 to-blue-50 border-purple-200 text-center py-8">
        <div className="text-red-600">{error}</div>
      </Card>
    );
  }

  if (candidates.length === 0) {
    return (
      <Card className="bg-gradient-to-r from-purple-50 to-blue-50 border-purple-200 text-center py-8">
        <p className="text-gray-600">No AI-recommended candidates for this job yet.</p>
      </Card>
    );
  }

  return (
    <Card className="bg-gradient-to-r from-purple-50 to-blue-50 border-purple-200">
      <div className="flex items-start space-x-4 mb-6">
        <div className="w-12 h-12 bg-purple-500 rounded-full flex flex-shrink-0 items-center justify-center">
          <Sparkles className="text-white" size={24} />
        </div>
        <div className="flex-1">
          <h3 className="font-semibold text-gray-900 mb-1">Top AI-Recommended Candidates</h3>
          <p className="text-sm text-gray-700 mb-1">Based on your job requirements, these are ranked as the best matches for this role:</p>
        </div>
      </div>
      <div className="grid md:grid-cols-2 gap-4">
        {candidates.map((c, i) => (
          <div key={c.application_id} className="bg-white rounded-lg shadow p-6 flex gap-4 items-center border border-gray-200">
            <div className="w-14 h-14 flex-shrink-0 bg-gray-100 border border-primary rounded-full flex items-center justify-center text-primary text-xl">
              <User size={28} />
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <h4 className="font-semibold text-gray-900">{c.candidate_name}</h4>
                <Badge variant="success">{Math.round(c.match_score * 100)}% Match</Badge>
              </div>
              <div className="flex flex-wrap gap-2 mb-1">
                {c.skills_match?.map(skill => (
                  <Badge key={skill} variant="default">{skill}</Badge>
                ))}
              </div>
              <div className="text-xs text-gray-600">Application ID: {c.application_id}</div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}
