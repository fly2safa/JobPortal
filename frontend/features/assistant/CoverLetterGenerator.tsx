'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Sparkles, Copy, Check, Loader } from 'lucide-react';

interface CoverLetterGeneratorProps {
  jobId: string;
  jobTitle: string;
  jobDescription: string;
  companyName: string;
  userName: string;
  userSkills?: string[];
  userExperience?: string;
  onGenerate: (data: any) => Promise<string>;
  onInsert?: (coverLetter: string) => void;
}

export function CoverLetterGenerator({
  jobId,
  jobTitle,
  jobDescription,
  companyName,
  userName,
  userSkills = [],
  userExperience,
  onGenerate,
  onInsert,
}: CoverLetterGeneratorProps) {
  const [generating, setGenerating] = useState(false);
  const [coverLetter, setCoverLetter] = useState('');
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async () => {
    setGenerating(true);
    setError(null);

    try {
      const generatedLetter = await onGenerate({
        job_id: jobId,
        job_title: jobTitle,
        job_description: jobDescription,
        company_name: companyName,
        user_name: userName,
        user_skills: userSkills,
        user_experience: userExperience,
      });

      setCoverLetter(generatedLetter);
    } catch (err: any) {
      console.error('Failed to generate cover letter:', err);
      setError(
        err.response?.data?.detail ||
          'Failed to generate cover letter. Please try again or write it manually.'
      );
    } finally {
      setGenerating(false);
    }
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(coverLetter);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const handleInsert = () => {
    if (onInsert && coverLetter) {
      onInsert(coverLetter);
    }
  };

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Sparkles className="text-primary" size={20} />
          <h3 className="font-semibold text-gray-900">AI Cover Letter Generator</h3>
        </div>
        {!coverLetter && (
          <Button
            onClick={handleGenerate}
            disabled={generating}
            size="sm"
            variant="primary"
          >
            {generating ? (
              <>
                <Loader size={14} className="mr-1 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Sparkles size={14} className="mr-1" />
                Generate Cover Letter
              </>
            )}
          </Button>
        )}
      </div>

      {/* Description */}
      {!coverLetter && !error && (
        <p className="text-sm text-gray-600">
          Let AI create a personalized cover letter based on your profile and the job
          description. You can edit it before submitting your application.
        </p>
      )}

      {/* Error Message */}
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      {/* Generated Cover Letter */}
      {coverLetter && (
        <div className="space-y-3">
          <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg max-h-96 overflow-y-auto">
            <p className="text-sm text-gray-900 whitespace-pre-wrap">{coverLetter}</p>
          </div>

          <div className="flex items-center space-x-2">
            <Button onClick={handleCopy} variant="outline" size="sm">
              {copied ? (
                <>
                  <Check size={14} className="mr-1 text-green-600" />
                  Copied!
                </>
              ) : (
                <>
                  <Copy size={14} className="mr-1" />
                  Copy
                </>
              )}
            </Button>

            {onInsert && (
              <Button onClick={handleInsert} variant="primary" size="sm">
                Use This Cover Letter
              </Button>
            )}

            <Button
              onClick={handleGenerate}
              variant="outline"
              size="sm"
              disabled={generating}
            >
              {generating ? (
                <Loader size={14} className="animate-spin" />
              ) : (
                'Regenerate'
              )}
            </Button>
          </div>

          <p className="text-xs text-gray-500">
            Tip: Review and customize the cover letter to add your personal touch before
            submitting.
          </p>
        </div>
      )}
    </div>
  );
}

