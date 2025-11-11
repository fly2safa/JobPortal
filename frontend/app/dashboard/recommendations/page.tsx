'use client';

import { useState, useEffect } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { JobCard } from '@/features/jobs/JobCard';
import { useAuth } from '@/hooks/useAuth';
import { JobRecommendation } from '@/types';
import { Sparkles, TrendingUp } from 'lucide-react';
import apiClient from '@/lib/api';

export default function RecommendationsPage() {
  useAuth(true);
  const [recommendations, setRecommendations] = useState<JobRecommendation[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.getJobRecommendations();
      setRecommendations(response || []);
    } catch (error) {
      console.error('Failed to fetch recommendations:', error);
      // Show mock data for demo
      setRecommendations(getMockRecommendations());
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center">
            <Sparkles className="mr-3 text-yellow-500" size={32} />
            AI Job Recommendations
          </h1>
          <p className="text-gray-600">
            Personalized job matches based on your skills, experience, and preferences
          </p>
        </div>

        {/* Info Card */}
        <Card className="bg-gradient-to-r from-primary-50 to-blue-50 border-primary-200">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-primary rounded-full flex items-center justify-center flex-shrink-0">
              <TrendingUp className="text-white" size={24} />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-1">How it works</h3>
              <p className="text-sm text-gray-700">
                Our AI analyzes your profile, skills, and application history to recommend jobs that best match your qualifications.
                The match score indicates how well you align with each position.
              </p>
            </div>
          </div>
        </Card>

        {/* Recommendations */}
        {isLoading ? (
          <div className="flex justify-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        ) : recommendations.length === 0 ? (
          <Card className="text-center py-12">
            <Sparkles className="mx-auto text-gray-400 mb-4" size={48} />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No recommendations yet</h3>
            <p className="text-gray-600 mb-4">
              Complete your profile and upload your resume to get personalized job recommendations.
            </p>
            <Button variant="primary" onClick={fetchRecommendations}>
              Refresh Recommendations
            </Button>
          </Card>
        ) : (
          <div className="space-y-6">
            {recommendations.map((recommendation, index) => (
              <div key={recommendation.job.id} className="relative">
                {/* Match Score Badge */}
                <div className="absolute -top-3 -right-3 z-10 bg-green-500 text-white px-3 py-1 rounded-full text-sm font-bold shadow-lg">
                  {Math.round(recommendation.match_score * 100)}% Match
                </div>

                <Card hover className="border-2 border-primary-100">
                  <div className="grid lg:grid-cols-3 gap-6">
                    <div className="lg:col-span-2">
                      <JobCard job={recommendation.job} />
                    </div>
                    <div className="border-l border-gray-200 pl-6">
                      <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                        <Sparkles className="mr-2 text-yellow-500" size={18} />
                        Why this matches
                      </h4>
                      <ul className="space-y-2">
                        {recommendation.reasons.map((reason, idx) => (
                          <li key={idx} className="text-sm text-gray-700 flex items-start">
                            <span className="text-green-500 mr-2 mt-0.5">✓</span>
                            {reason}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </Card>
              </div>
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

function getMockRecommendations(): JobRecommendation[] {
  return [
    {
      job: {
        id: '1',
        title: 'Senior Frontend Developer',
        description: 'Build scalable web applications with React and TypeScript.',
        company_id: 'company-1',
        company_name: 'TechCorp Inc.',
        location: 'San Francisco, CA',
        job_type: 'full_time',
        experience_level: 'senior',
        salary_min: 120000,
        salary_max: 180000,
        skills: ['React', 'TypeScript', 'Next.js', 'Tailwind CSS'],
        requirements: ['5+ years experience', 'React expertise'],
        status: 'active',
        posted_date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
      },
      match_score: 0.92,
      reasons: [
        'Your React and TypeScript skills are a perfect match',
        'Your 5+ years of experience meets the requirement',
        'Located in your preferred location',
        'Salary range aligns with your expectations',
      ],
    },
    {
      job: {
        id: '2',
        title: 'Full Stack Engineer',
        description: 'Work on cutting-edge technologies in a fast-paced startup.',
        company_id: 'company-2',
        company_name: 'StartupXYZ',
        location: 'Remote',
        job_type: 'full_time',
        experience_level: 'mid',
        salary_min: 90000,
        salary_max: 140000,
        skills: ['Node.js', 'React', 'MongoDB', 'AWS'],
        requirements: ['3+ years experience'],
        status: 'active',
        posted_date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
      },
      match_score: 0.85,
      reasons: [
        'Your full-stack experience is highly relevant',
        'Remote position matches your preference',
        'Node.js and React match your skill set',
        'Startup environment aligns with your interests',
      ],
    },
  ];
}

