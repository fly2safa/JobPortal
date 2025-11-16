'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { PasswordInput } from '@/components/ui/PasswordInput';
import { Card } from '@/components/ui/Card';
import { useAuthStore } from '@/store/authStore';
import apiClient from '@/lib/api';
import Link from 'next/link';

interface LoginFormData {
  email: string;
  password: string;
}

export function LoginForm() {
  const router = useRouter();
  const { setAuth } = useAuthStore();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>();

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true);
    setError('');

    try {
      // Call the actual backend API
      const response = await apiClient.login(data.email, data.password);
      
      // Store authentication data
      setAuth(response.user, response.access_token);
      
      // Redirect based on user role
      if (response.user.role === 'employer') {
        router.push('/employer/dashboard');
      } else {
        router.push('/dashboard');
      }
    } catch (err: any) {
      console.error('Login error:', err);
      
      // Handle rate limit errors specifically
      if (err.isRateLimit || err.response?.status === 429) {
        const retryAfter = err.retryAfter || 60;
        setError(`Too many login attempts. Please wait ${retryAfter} seconds before trying again.`);
        return;
      }
      
      // FastAPI returns errors in 'detail' field, not 'error'
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else if (!err.response) {
        setError('Unable to connect to server. Please check if the backend is running.');
      } else {
        setError('Invalid email or password');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <style dangerouslySetInnerHTML={{__html: `
        .login-form input::placeholder {
          font-size: 0.875rem !important;
          font-weight: 400 !important;
        }
        .sign-in-btn {
          background: linear-gradient(135deg, #075299 0%, #5a9ab3 100%);
          transition: all 0.3s ease;
        }
        .sign-in-btn:hover:not(:disabled) {
          background: linear-gradient(135deg, #5a9ab3 0%, #075299 100%);
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(7, 82, 153, 0.3);
        }
        .sign-in-btn:active:not(:disabled) {
          transform: translateY(0);
        }
      `}} />
      <div style={{ fontFamily: 'Playfair Display, serif' }}>
      <Card className="w-full max-w-md login-form">
        <div className="text-center mb-6" style={{ fontFamily: 'Playfair Display, serif' }}>
          <h2 className="text-3xl text-gray-900" style={{ fontFamily: 'Playfair Display, serif', fontWeight: 400 }}>Welcome Back</h2>
          <p className="text-gray-600 mt-2" style={{ fontFamily: 'Playfair Display, serif', fontWeight: 400 }}>Sign In To Your TalentNest Account</p>
        </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4" style={{ fontFamily: 'Playfair Display, serif' }}>
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" style={{ fontFamily: 'Playfair Display, serif' }}>
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
          <PasswordInput
            label="Password"
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

        <div className="flex items-center justify-between" style={{ fontFamily: 'Playfair Display, serif' }}>
          <label className="flex items-center" style={{ fontFamily: 'Playfair Display, serif' }}>
            <input type="checkbox" className="rounded border-gray-300 text-primary focus:ring-primary" />
            <span className="ml-2 text-sm text-gray-600" style={{ fontFamily: 'Playfair Display, serif' }}>Remember Me</span>
          </label>
          <Link href="/forgot-password" className="text-sm text-primary hover:underline" style={{ fontFamily: 'Playfair Display, serif' }}>
            Forgot Password?
          </Link>
        </div>

        <button type="submit" className="sign-in-btn w-full px-4 py-2 rounded-lg font-medium text-white disabled:opacity-50 disabled:cursor-not-allowed" disabled={isLoading} style={{ fontFamily: 'Playfair Display, serif' }}>
          {isLoading ? (
            <span className="flex items-center justify-center" style={{ fontFamily: 'Playfair Display, serif' }}>
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Loading...
            </span>
          ) : (
            'Sign In'
          )}
        </button>
      </form>

      <div className="mt-6 text-center" style={{ fontFamily: 'Playfair Display, serif' }}>
        <p className="text-sm text-gray-600" style={{ fontFamily: 'Playfair Display, serif' }}>
          Don&apos;t have an account?{' '}
          <Link href="/register" className="text-primary font-medium hover:underline" style={{ fontFamily: 'Playfair Display, serif' }}>
            Sign up
          </Link>
        </p>
      </div>
    </Card>
    </div>
    </>
  );
}

