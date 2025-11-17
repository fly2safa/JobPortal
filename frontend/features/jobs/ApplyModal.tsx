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
  const [uploadSuccess, setUploadSuccess] = useState(false);
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
      console.log('Fetched resumes response:', response);
      // The response is already the data, not nested
      const resumeList = Array.isArray(response) ? response : (response.data || response.resumes || []);
      console.log('Resume list:', resumeList);
      setResumes(resumeList);
    } catch (err) {
      console.error('Error fetching resumes:', err);
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
    trigger,
  } = useForm<ApplyFormData>();

  const coverLetter = watch('cover_letter');
  const selectedResumeUrl = watch('resume_url');

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
    
    // Validate file type
    const validTypes = ['.pdf', '.doc', '.docx'];
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!validTypes.includes(fileExtension)) {
      setError('Please upload a PDF or Word document (.pdf, .doc, .docx)');
      return;
    }
    
    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      setError('File size must be less than 5MB');
      return;
    }
    
    setIsUploadingResume(true);
    setError("");
    setUploadSuccess(false);
    try {
      console.log('Uploading resume:', file.name);
      const response = await apiClient.uploadResume(file);
      console.log('Resume uploaded successfully:', response);
      console.log('Uploaded resume details:', response.resume);
      
      // Refresh the resume list
      await fetchResumes();
      
      // Wait a bit for state to update
      await new Promise(resolve => setTimeout(resolve, 100));
      
      // Auto-select the newly uploaded resume
      const resumeUrl = response.resume?.file_url || response.resume?.url || response.file_url;
      console.log('Trying to set resume URL:', resumeUrl);
      
      setValue('resume_url', resumeUrl, { 
        shouldValidate: true,
        shouldDirty: true,
        shouldTouch: true
      });
      
      // Trigger validation to ensure the form updates
      await trigger('resume_url');
      
      console.log('Resume auto-selected:', resumeUrl);
      console.log('Current resumes in state:', resumes);
      
      // Show success message
      setUploadSuccess(true);
      setTimeout(() => setUploadSuccess(false), 3000);
      
      // Clear the file input so user can upload the same file again if needed
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (err: any) {
      console.error('Resume upload error:', err);
      setError(err.response?.data?.detail || err.response?.data?.error || 'Failed to upload resume. Please try again.');
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
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Upload New Resume (Optional)
        </label>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={onResumeUpload}
          disabled={isUploadingResume || isSubmitting}
          className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:ring-2 focus:ring-primary p-2"
        />
        <p className="text-xs text-gray-500 mt-1">
          PDF, DOC, or DOCX (max 5MB). File will upload automatically.
        </p>
        {isUploadingResume && (
          <div className="mt-2 text-sm text-blue-600 flex items-center">
            <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Uploading resume...
          </div>
        )}
        {uploadSuccess && (
          <div className="mt-2 text-sm text-green-600 flex items-center">
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
            </svg>
            Resume uploaded and selected successfully!
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <Select
            label="Select Resume"
            options={[{ value: '', label: 'Select a resume' }, ...resumes.map((r) => ({ value: r.file_url, label: r.file_name }))]}
            {...register('resume_url', { required: 'Please select or upload a resume' })}
            error={errors.resume_url?.message}
            disabled={isUploadingResume || isSubmitting}
          />
          {selectedResumeUrl && (
            <p className="text-xs text-green-600 mt-1">
              ✓ Resume selected: {resumes.find(r => r.file_url === selectedResumeUrl)?.file_name || 'Unknown'}
            </p>
          )}
          {resumes.length === 0 && (
            <p className="text-xs text-gray-500 mt-1">
              No resumes uploaded yet. Upload one above to get started.
            </p>
          )}
        </div>

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

