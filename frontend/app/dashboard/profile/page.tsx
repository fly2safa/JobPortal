'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Select } from '@/components/ui/Select';
import { useAuth } from '@/hooks/useAuth';
import { Upload, Save } from 'lucide-react';
import apiClient from '@/lib/api';

interface ProfileFormData {
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  location: string;
  experience_years: number;
  skills: string;
  education: string;
  bio: string;
}

export default function ProfilePage() {
  const { user } = useAuth(true);
  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  const jobSeekerProfile = user?.role === 'job_seeker' ? user.profile as any : {};

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ProfileFormData>({
    defaultValues: {
      first_name: user?.first_name || '',
      last_name: user?.last_name || '',
      email: user?.email || '',
      phone: jobSeekerProfile?.phone || '',
      location: jobSeekerProfile?.location || '',
      experience_years: jobSeekerProfile?.experience_years || 0,
      skills: jobSeekerProfile?.skills?.join(', ') || '',
      education: jobSeekerProfile?.education || '',
      bio: jobSeekerProfile?.bio || '',
    },
  });

  const onSubmit = async (data: ProfileFormData) => {
    setIsLoading(true);
    setSuccessMessage('');

    try {
      await apiClient.updateProfile({
        ...data,
        skills: data.skills.split(',').map((s) => s.trim()),
      });
      setSuccessMessage('Profile updated successfully!');
    } catch (error) {
      console.error('Failed to update profile:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">My Profile</h1>
          <p className="text-gray-600">Manage your personal information and resume</p>
        </div>

        {successMessage && (
          <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
            {successMessage}
          </div>
        )}

        {/* Profile Picture */}
        <Card>
          <CardTitle>Profile Picture</CardTitle>
          <CardContent>
            <div className="flex items-center space-x-6">
              <div className="w-24 h-24 bg-primary rounded-full flex items-center justify-center text-white text-3xl font-bold">
                {user?.first_name?.charAt(0) || 'U'}
              </div>
              <div>
                <Button variant="outline" size="sm">
                  <Upload size={16} className="mr-2" />
                  Upload Photo
                </Button>
                <p className="text-sm text-gray-500 mt-2">JPG, PNG or GIF. Max size 2MB.</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Personal Information */}
        <Card>
          <CardTitle>Personal Information</CardTitle>
          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                  label="First Name"
                  {...register('first_name', { required: 'First name is required' })}
                  error={errors.first_name?.message}
                />
                <Input
                  label="Last Name"
                  {...register('last_name', { required: 'Last name is required' })}
                  error={errors.last_name?.message}
                />
                <Input
                  label="Email"
                  type="email"
                  {...register('email', { required: 'Email is required' })}
                  error={errors.email?.message}
                  disabled
                />
                <Input
                  label="Phone"
                  type="tel"
                  placeholder="+1 (555) 123-4567"
                  {...register('phone')}
                />
                <Input
                  label="Location"
                  placeholder="City, State"
                  {...register('location')}
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Select
                  label="Years of Experience"
                  options={[
                    { value: '0', label: '0-1 years' },
                    { value: '2', label: '1-3 years' },
                    { value: '4', label: '3-5 years' },
                    { value: '6', label: '5-10 years' },
                    { value: '11', label: '10+ years' },
                  ]}
                  {...register('experience_years')}
                />
                <Input
                  label="Education"
                  placeholder="e.g., Bachelor's in Computer Science"
                  {...register('education')}
                />
              </div>

              <Input
                label="Skills"
                placeholder="JavaScript, React, Node.js, Python, etc. (comma separated)"
                {...register('skills')}
                helperText="Enter your skills separated by commas"
              />

              <Textarea
                label="Bio"
                rows={4}
                placeholder="Tell us about yourself, your experience, and career goals..."
                {...register('bio')}
              />

              <Button type="submit" variant="primary" isLoading={isLoading}>
                <Save size={16} className="mr-2" />
                Save Changes
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Resume */}
        <Card>
          <CardTitle>Resume</CardTitle>
          <CardContent>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
              <Upload className="mx-auto text-gray-400 mb-4" size={48} />
              <h3 className="text-lg font-medium text-gray-900 mb-2">Upload Your Resume</h3>
              <p className="text-sm text-gray-600 mb-4">
                PDF, DOC, or DOCX. Max size 5MB. Our AI will parse your resume automatically.
              </p>
              <Button variant="primary">
                <Upload size={16} className="mr-2" />
                Choose File
              </Button>
            </div>
            
            <div className="mt-4">
              <h4 className="font-medium text-gray-900 mb-2">Uploaded Resumes</h4>
              <div className="space-y-2">
                <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center">
                    <FileIcon />
                    <div className="ml-3">
                      <p className="text-sm font-medium text-gray-900">My Resume.pdf</p>
                      <p className="text-xs text-gray-500">Uploaded 2 days ago</p>
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    <Button variant="ghost" size="sm">View</Button>
                    <Button variant="ghost" size="sm">Delete</Button>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}

function FileIcon() {
  return (
    <div className="w-10 h-10 bg-red-100 rounded flex items-center justify-center">
      <svg className="w-6 h-6 text-red-600" fill="currentColor" viewBox="0 0 20 20">
        <path d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" />
      </svg>
    </div>
  );
}

