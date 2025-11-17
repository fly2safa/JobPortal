'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Select } from '@/components/ui/Select';
import { useAuth, useRequireRole } from '@/hooks/useAuth';
import { useAuthStore } from '@/store/authStore';
import { JOB_TYPES, EXPERIENCE_LEVELS } from '@/constants';
import apiClient from '@/lib/api';
import { Save } from 'lucide-react';

interface JobFormData {
  title: string;
  description: string;
  location: string;
  job_type: string;
  experience_level: string;
  salary_min: number;
  salary_max: number;
  skills: string;
  requirements: string;
  benefits: string;
}

export default function NewJobPage() {
  useAuth(true);
  useRequireRole(['employer']);
  const router = useRouter();
  const { user } = useAuthStore();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<JobFormData>();

  const onSubmit = async (data: JobFormData) => {
    setIsSubmitting(true);
    setError('');
    setSuccess(false);

    // Check if user has company_id
    if (!user?.company_id) {
      setError('You must be associated with a company to post jobs. Please contact support.');
      setIsSubmitting(false);
      return;
    }

    try {
      console.log('=== JOB CREATION DEBUG ===');
      console.log('Form data:', data);
      console.log('Location value:', data.location);
      console.log('Location length:', data.location?.length);
      console.log('Creating job with company_id:', user.company_id);
      
      const jobPayload = {
        title: data.title,
        description: data.description,
        location: data.location,
        job_type: data.job_type,
        experience_level: data.experience_level,
        salary_min: data.salary_min || undefined,
        salary_max: data.salary_max || undefined,
        skills: data.skills.split(',').map((s) => s.trim()).filter(Boolean),
        required_skills: data.skills.split(',').map((s) => s.trim()).filter(Boolean),
        requirements: data.requirements,
        benefits: data.benefits ? data.benefits.split('\n').filter(Boolean) : [],
        company_id: user.company_id,
        status: 'active',
      };
      
      console.log('Job payload being sent:', jobPayload);
      
      const response = await apiClient.createJob(jobPayload);
      
      console.log('Job created successfully:', response);
      setSuccess(true);
      
      // Redirect after a brief delay to show success message
      setTimeout(() => {
        router.push('/employer/jobs');
      }, 1500);
    } catch (err: any) {
      console.error('Job creation error:', err);
      console.error('Error response:', err.response);
      console.error('Error response data:', err.response?.data);
      // Handle rate limit errors specifically
      if (err.isRateLimit || err.response?.status === 429) {
        const retryAfter = err.retryAfter || 60;
        setError(`Too many job postings. Please wait ${retryAfter} seconds before posting another job.`);
      } else {
        // Handle validation errors (array of error objects)
        const errorDetail = err.response?.data?.detail;
        if (Array.isArray(errorDetail)) {
          // Extract error messages from validation error array with field names
          const errorMessages = errorDetail.map((e: any) => {
            const field = e.loc ? e.loc[e.loc.length - 1] : 'unknown';
            const msg = e.msg || JSON.stringify(e);
            return `${field}: ${msg}`;
          }).join('; ');
          setError(`Validation error: ${errorMessages}`);
          console.error('Validation errors:', errorDetail);
        } else if (typeof errorDetail === 'object' && errorDetail !== null) {
          // If detail is an object, try to extract meaningful message
          setError(errorDetail.msg || JSON.stringify(errorDetail));
        } else {
          // String error or fallback
          setError(errorDetail || 'Failed to create job. Please try again.');
        }
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6 max-w-4xl">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Post a New Job</h1>
          <p className="text-white">Fill out the details below to create your job posting</p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        {success && (
          <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
            ✅ Job posted successfully! Redirecting...
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <Card>
            <CardTitle>Basic Information</CardTitle>
            <CardContent>
              <div className="space-y-4">
                <Input
                  label="Job Title"
                  placeholder="e.g., Senior Frontend Developer"
                  {...register('title', { required: 'Job title is required' })}
                  error={errors.title?.message}
                />

                <Textarea
                  label="Job Description"
                  rows={6}
                  placeholder="Describe the role, responsibilities, and what makes this position exciting..."
                  {...register('description', { required: 'Description is required' })}
                  error={errors.description?.message}
                />

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Input
                    label="Location"
                    placeholder="e.g., San Francisco, CA or Remote"
                    {...register('location', { 
                      required: 'Location is required',
                      minLength: {
                        value: 2,
                        message: 'Location must be at least 2 characters'
                      }
                    })}
                    error={errors.location?.message}
                  />

                  <Select
                    label="Job Type"
                    options={[
                      { value: '', label: 'Select job type' },
                      ...JOB_TYPES.map((type) => ({ value: type.value, label: type.label })),
                    ]}
                    {...register('job_type', { required: 'Job type is required' })}
                    error={errors.job_type?.message}
                  />
                </div>

                <Select
                  label="Experience Level"
                  options={[
                    { value: '', label: 'Select experience level' },
                    ...EXPERIENCE_LEVELS.map((level) => ({ value: level.value, label: level.label })),
                  ]}
                  {...register('experience_level', { required: 'Experience level is required' })}
                  error={errors.experience_level?.message}
                />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardTitle>Compensation</CardTitle>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                  label="Minimum Salary"
                  type="number"
                  placeholder="80000"
                  {...register('salary_min', { valueAsNumber: true })}
                  helperText="Annual salary in USD"
                />
                <Input
                  label="Maximum Salary"
                  type="number"
                  placeholder="120000"
                  {...register('salary_max', { valueAsNumber: true })}
                  helperText="Annual salary in USD"
                />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardTitle>Requirements & Skills</CardTitle>
            <CardContent>
              <div className="space-y-4">
                <Input
                  label="Required Skills"
                  placeholder="JavaScript, React, TypeScript, Node.js (comma separated)"
                  {...register('skills', { required: 'At least one skill is required' })}
                  error={errors.skills?.message}
                  helperText="Enter skills separated by commas"
                />

                <Textarea
                  label="Requirements"
                  rows={6}
                  placeholder="• 5+ years of professional experience&#10;• Strong knowledge of React and its ecosystem&#10;• Experience with TypeScript&#10;• Bachelor's degree in Computer Science or related field"
                  {...register('requirements', { required: 'Requirements are required' })}
                  error={errors.requirements?.message}
                  helperText="Enter each requirement on a new line"
                />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardTitle>Benefits (Optional)</CardTitle>
            <CardContent>
              <Textarea
                label="Benefits & Perks"
                rows={6}
                placeholder="• Competitive salary and equity&#10;• Health, dental, and vision insurance&#10;• 401(k) with company match&#10;• Flexible PTO policy&#10;• Remote work options"
                {...register('benefits')}
                helperText="Enter each benefit on a new line"
              />
            </CardContent>
          </Card>

          <div className="flex space-x-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => router.back()}
              className="flex-1"
            >
              Cancel
            </Button>
            <Button type="submit" variant="primary" isLoading={isSubmitting} className="flex-1">
              <Save size={18} className="mr-2" />
              Publish Job
            </Button>
          </div>
        </form>
      </div>
    </DashboardLayout>
  );
}

