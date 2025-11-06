'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card } from '@/components/ui/Card';
import { useAuthStore } from '@/store/authStore';
import apiClient from '@/lib/api';
import Link from 'next/link';

interface RegisterFormData {
  full_name: string;
  email: string;
  password: string;
  confirmPassword: string;
  role: 'job_seeker' | 'employer';
}

export function RegisterForm() {
  const router = useRouter();
  const { setAuth } = useAuthStore();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<RegisterFormData>({
    defaultValues: {
      role: 'job_seeker',
    },
  });

  const password = watch('password');

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true);
    setError('');

    try {
      // DEMO MODE: Bypass API call and use mock data
      const mockUser = {
        id: '1',
        email: data.email,
        full_name: data.full_name,
        role: data.role,
        is_active: true,
        created_at: new Date().toISOString(),
        profile: data.role === 'job_seeker' ? {
          bio: '',
          phone: '',
          location: '',
          skills: [],
          experience: [],
          education: [],
        } : {
          company_name: '',
          company_description: '',
          website: '',
          company_size: '',
          industry: '',
        }
      };
      
      const mockToken = 'demo-token-' + Date.now();
      
      setAuth(mockUser, mockToken);
      
      // Redirect based on role
      if (data.role === 'employer') {
        router.push('/employer/dashboard');
      } else {
        router.push('/dashboard');
      }
    } catch (err: any) {
      setError(err.response?.data?.error || 'Registration failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <style dangerouslySetInnerHTML={{__html: `
        .register-form input::placeholder {
          font-size: 0.875rem !important;
          font-weight: 400 !important;
        }
        .create-account-btn {
          background: linear-gradient(135deg, #075299 0%, #5a9ab3 100%);
          transition: all 0.3s ease;
        }
        .create-account-btn:hover:not(:disabled) {
          background: linear-gradient(135deg, #5a9ab3 0%, #075299 100%);
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(7, 82, 153, 0.3);
        }
        .create-account-btn:active:not(:disabled) {
          transform: translateY(0);
        }
      `}} />
      <Card className="w-full max-w-md register-form" style={{ fontFamily: 'Playfair Display, serif' }}>
        <div className="text-center mb-6" style={{ fontFamily: 'Playfair Display, serif' }}>
          <h2 className="text-3xl font-bold text-gray-900" style={{ fontFamily: 'Playfair Display, serif' }}>Create Account</h2>
          <p className="text-gray-600 mt-2" style={{ fontFamily: 'Playfair Display, serif' }}>
            Join{' '}
            <span style={{
              fontFamily: 'Playfair Display, serif',
              fontWeight: 700,
              background: 'linear-gradient(135deg, #075299 0%, #5a9ab3 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text'
            }}>TALENT</span>
            <span style={{ fontFamily: 'Dancing Script, cursive', fontWeight: 700, color: '#075299' }}>Nest</span>
            {' '}and Start Your Journey
          </p>
        </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4" style={{ fontFamily: 'Playfair Display, serif' }}>
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" style={{ fontFamily: 'Playfair Display, serif' }}>
        <div style={{ fontFamily: 'Playfair Display, serif' }}>
          <Input
            label="Full Name"
            type="text"
            placeholder="Talent Nest"
            {...register('full_name', {
              required: 'Full name is required',
              minLength: {
                value: 2,
                message: 'Name must be at least 2 characters',
              },
            })}
            error={errors.full_name?.message}
            style={{ fontFamily: 'Playfair Display, serif' }}
          />
        </div>

        <div style={{ fontFamily: 'Playfair Display, serif' }}>
          <Input
            label="Email"
            type="email"
            placeholder="Talent@example.com"
            {...register('email', {
              required: 'Email is required',
              pattern: {
                value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                message: 'Invalid email address',
              },
            })}
            error={errors.email?.message}
            style={{ fontFamily: 'Playfair Display, serif' }}
          />
        </div>

        <div style={{ fontFamily: 'Playfair Display, serif' }}>
          <Input
            label="Password"
            type="password"
            placeholder="••••••••"
            {...register('password', {
              required: 'Password is required',
              minLength: {
                value: 6,
                message: 'Password must be at least 6 characters',
              },
            })}
            error={errors.password?.message}
            style={{ fontFamily: 'Playfair Display, serif' }}
          />
        </div>

        <div style={{ fontFamily: 'Playfair Display, serif' }}>
          <Input
            label="Confirm Password"
            type="password"
            placeholder="••••••••"
            {...register('confirmPassword', {
              required: 'Please confirm your password',
              validate: (value) => value === password || 'Passwords do not match',
            })}
            error={errors.confirmPassword?.message}
            style={{ fontFamily: 'Playfair Display, serif' }}
          />
        </div>

        <div className="space-y-2" style={{ fontFamily: 'Playfair Display, serif' }}>
          <label className="block text-sm font-medium text-gray-700" style={{ fontFamily: 'Playfair Display, serif' }}>
            I am a <span className="text-red-500">*</span>
          </label>
          <div className="grid grid-cols-2 gap-4">
            <label 
              className="flex items-center justify-center space-x-2 cursor-pointer px-4 py-3 rounded-lg border border-gray-300 transition-all duration-200"
              style={{
                fontFamily: 'Playfair Display, serif'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = '#5a9ab3';
                e.currentTarget.style.backgroundColor = '#5a9ab3';
                e.currentTarget.style.color = 'white';
                e.currentTarget.style.fontFamily = 'Playfair Display, serif';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = '#d1d5db';
                e.currentTarget.style.backgroundColor = 'transparent';
                e.currentTarget.style.color = 'inherit';
                e.currentTarget.style.fontFamily = 'Playfair Display, serif';
              }}
            >
              <input
                type="radio"
                value="job_seeker"
                {...register('role', { required: true })}
                className="text-primary focus:ring-primary"
              />
              <span className="text-sm font-medium" style={{ fontFamily: 'Playfair Display, serif' }}>Job Seeker</span>
            </label>
            <label 
              className="flex items-center justify-center space-x-2 cursor-pointer px-4 py-3 rounded-lg border border-gray-300 transition-all duration-200"
              style={{
                fontFamily: 'Playfair Display, serif'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = '#5a9ab3';
                e.currentTarget.style.backgroundColor = '#5a9ab3';
                e.currentTarget.style.color = 'white';
                e.currentTarget.style.fontFamily = 'Playfair Display, serif';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = '#d1d5db';
                e.currentTarget.style.backgroundColor = 'transparent';
                e.currentTarget.style.color = 'inherit';
                e.currentTarget.style.fontFamily = 'Playfair Display, serif';
              }}
            >
              <input
                type="radio"
                value="employer"
                {...register('role', { required: true })}
                className="text-primary focus:ring-primary"
              />
              <span className="text-sm font-medium" style={{ fontFamily: 'Playfair Display, serif' }}>Employer</span>
            </label>
          </div>
        </div>

        <button 
          type="submit" 
          disabled={isLoading}
          className="create-account-btn w-full px-4 py-2 rounded-lg font-medium text-white disabled:opacity-50 disabled:cursor-not-allowed"
          style={{
            fontFamily: 'Playfair Display, serif'
          }}
        >
          {isLoading ? (
            <span className="flex items-center justify-center" style={{ fontFamily: 'Playfair Display, serif' }}>
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Loading...
            </span>
          ) : (
            'Create Account'
          )}
        </button>
      </form>

      <div className="mt-6 text-center" style={{ fontFamily: 'Playfair Display, serif' }}>
        <p className="text-sm text-gray-600" style={{ fontFamily: 'Playfair Display, serif' }}>
          Already have an account?{' '}
          <Link href="/login" className="text-primary font-medium hover:underline" style={{ fontFamily: 'Playfair Display, serif' }}>
            Sign in
          </Link>
        </p>
      </div>
    </Card>
    </>
  );
}

