'use client';

import { useState, useEffect, useRef } from 'react';
import { useForm } from 'react-hook-form';
import { Modal } from '@/components/ui/Modal';
import { Button } from '@/components/ui/Button';
import { Textarea } from '@/components/ui/Textarea';
import { Select } from '@/components/ui/Select';
import { Card } from '@/components/ui/Card';
import apiClient from '@/lib/api';
import { Sparkles } from 'lucide-react';
import { Resume } from '@/types';
import { CoverLetterGenerator } from '@/features/assistant';
import { useAuthStore } from '@/store/authStore';

interface ApplyModalProps {
  isOpen: boolean;
  onClose: () => void;
  jobId: string;
  jobTitle: string;
  jobDescription?: string;
  companyName?: string;
  onSuccess: () => void;
}

interface ApplyFormData {
  resume_url: string;
  cover_letter: string;
}

export function ApplyModal({
  isOpen,
  onClose,
  jobId,
  jobTitle,
  jobDescription = '',
  companyName = '',
  onSuccess,
}: ApplyModalProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [isUploadingResume, setIsUploadingResume] = useState(false);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  // Get available resumes for selection, refresh after upload
  useEffect(() => {
    if (isOpen) {
      fetchResumes();
    }
  }, [isOpen]);

  const fetchResumes = async () => {
    try {
      const response = await apiClient.getResumes();
      setResumes(response.data || []);
    } catch (err) {
      setResumes([]);
    }
  };
  const [showGenerator, setShowGenerator] = useState(false);
  const { user } = useAuthStore();

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors },
  } = useForm<ApplyFormData>();

  const coverLetter = watch('cover_letter');

  const handleGenerateCoverLetter = async (data: any) => {
    const response = await apiClient.generateCoverLetter(data);
    return response.cover_letter;
  };

  const handleInsertCoverLetter = (letter: string) => {
    setValue('cover_letter', letter);
    setShowGenerator(false);
  };

  const onResumeUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setIsUploadingResume(true);
    setError("");
    try {
      const response = await apiClient.uploadResume(file);
      await fetchResumes();
      // Auto-select the newly uploaded resume
      setValue('resume_url', response.resume.file_url, { shouldValidate: true });
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to upload resume. Please try again.');
    } finally {
      setIsUploadingResume(false);
    }
  };

  const onSubmit = async (data: ApplyFormData) => {
    setIsSubmitting(true);
    setError('');

    try {
      await apiClient.applyToJob({
        job_id: jobId,
        resume_url: data.resume_url,
        cover_letter: data.cover_letter,
      });
      onSuccess();
      onClose();
    } catch (err: any) {
      // Handle rate limit errors specifically
      if (err.isRateLimit || err.response?.status === 429) {
        const retryAfter = err.retryAfter || 60;
        setError(`Too many applications submitted. Please wait ${retryAfter} seconds before applying to another job.`);
      } else {
        setError(err.response?.data?.error || err.response?.data?.detail || 'Failed to submit application. Please try again.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={`Apply for ${jobTitle}`} size="lg">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
          {error}
        </div>
      )}

      {/* Upload Resume Section */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Upload Resume
        </label>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={onResumeUpload}
          disabled={isUploadingResume || isSubmitting}
          className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:ring-2 focus:ring-primary"
        />
        {isUploadingResume && <span className="text-xs text-gray-500 mt-1 inline-block">Uploading...</span>}
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <Select
          label="Select Resume"
          options={[{ value: '', label: 'Select a resume' }, ...resumes.map((r) => ({ value: r.file_url, label: r.file_name }))]}
          {...register('resume_url', { required: 'Please select or upload a resume' })}
          error={errors.resume_url?.message}
          disabled={isUploadingResume || isSubmitting}
        />

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Cover Letter <span className="text-gray-500">(optional)</span>
          </label>

          {!showGenerator && !coverLetter && (
            <Card className="p-4 mb-3">
              <CoverLetterGenerator
                jobId={jobId}
                jobTitle={jobTitle}
                jobDescription={jobDescription}
                companyName={companyName}
                userName={user ? `${user.first_name} ${user.last_name}` : 'Applicant'}
                userSkills={user?.skills || []}
                userExperience={user?.bio}
                onGenerate={handleGenerateCoverLetter}
                onInsert={handleInsertCoverLetter}
              />
            </Card>
          )}

          {(showGenerator || coverLetter) && (
            <>
              <Textarea
                rows={8}
                placeholder="Write a cover letter to introduce yourself..."
                {...register('cover_letter')}
                error={errors.cover_letter?.message}
              />
              {coverLetter && !showGenerator && (
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowGenerator(true)}
                  className="mt-2 text-primary"
                >
                  Regenerate with AI
                </Button>
              )}
            </>
          )}
        </div>

        <div className="flex gap-3 pt-4">
          <Button type="button" variant="outline" onClick={onClose} className="flex-1">
            Cancel
          </Button>
          <Button type="submit" variant="primary" isLoading={isSubmitting} className="flex-1">
            Submit Application
          </Button>
        </div>
      </form>
    </Modal>
  );
}

