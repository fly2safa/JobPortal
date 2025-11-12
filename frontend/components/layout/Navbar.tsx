'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { useAuthStore } from '@/store/authStore';
import { User, LogOut, Home, FileText, MessageSquare, Calendar } from 'lucide-react';
import { useState, useEffect, useRef } from 'react';
import apiClient from '@/lib/api';

export function Navbar() {
  const pathname = usePathname();
  const router = useRouter();
  const { isAuthenticated, user, logout, _hasHydrated, updateUser } = useAuthStore();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const hasRefreshedUser = useRef(false);

  // Refresh user data if first_name or last_name is missing (only once after hydration)
  useEffect(() => {
    const refreshUserData = async () => {
      if (_hasHydrated && isAuthenticated && user && (!user.first_name || !user.last_name) && !hasRefreshedUser.current) {
        hasRefreshedUser.current = true;
        try {
          const freshUserData = await apiClient.getCurrentUser();
          updateUser(freshUserData);
        } catch (error) {
          console.error('Failed to refresh user data:', error);
        }
      }
    };

    refreshUserData();
  }, [_hasHydrated, isAuthenticated, user, updateUser]);

  // Get display name for user
  const getUserDisplayName = () => {
    if (!user) return 'User';
    
    // Try first_name and last_name
    if (user.first_name && user.last_name) {
      return `${user.first_name} ${user.last_name}`;
    }
    
    // Try just first_name
    if (user.first_name) {
      return user.first_name;
    }
    
    // Fall back to email
    return user.email || 'User';
  };

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  const isActive = (path: string) => pathname === path;

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center">
              <span className="text-2xl">
                <span style={{ 
                  fontFamily: 'Playfair Display, serif', 
                  fontWeight: 700,
                  background: 'linear-gradient(135deg, #075299 0%, #5a9ab3 100%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  backgroundClip: 'text'
                }}>TALENT</span>
                <span style={{ fontFamily: 'Dancing Script, cursive', fontWeight: 700 }} className="text-primary">Nest</span>
              </span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-4">
            <Link
              href="/jobs"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/jobs')
                  ? 'text-primary bg-primary-50'
                  : 'text-gray-700 hover:text-primary hover:bg-gray-50'
              }`}
            >
              Find Jobs
            </Link>

            {isAuthenticated ? (
              <>
                {user?.role === 'job_seeker' ? (
                  <>
                    <Link
                      href="/dashboard"
                      className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                        isActive('/dashboard')
                          ? 'text-primary bg-primary-50'
                          : 'text-gray-700 hover:text-primary hover:bg-gray-50'
                      }`}
                    >
                      Dashboard
                    </Link>
                    <Link
                      href="/dashboard/applications"
                      className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                        isActive('/dashboard/applications')
                          ? 'text-primary bg-primary-50'
                          : 'text-gray-700 hover:text-primary hover:bg-gray-50'
                      }`}
                    >
                      My Applications
                    </Link>
                  </>
                ) : (
                  <>
                    <Link
                      href="/employer/dashboard"
                      className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                        isActive('/employer/dashboard')
                          ? 'text-primary bg-primary-50'
                          : 'text-gray-700 hover:text-primary hover:bg-gray-50'
                      }`}
                    >
                      Dashboard
                    </Link>
                    <Link
                      href="/employer/jobs"
                      className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                        isActive('/employer/jobs')
                          ? 'text-primary bg-primary-50'
                          : 'text-gray-700 hover:text-primary hover:bg-gray-50'
                      }`}
                    >
                      My Jobs
                    </Link>
                  </>
                )}
                
                <div className="flex items-center space-x-2 border-l pl-4 ml-2">
                  <span className="text-sm text-gray-700 font-medium">
                    {getUserDisplayName()}
                  </span>
                  <Button variant="ghost" size="sm" onClick={handleLogout}>
                    <LogOut size={16} className="mr-1" />
                    Logout
                  </Button>
                </div>
              </>
            ) : (
              <div className="flex items-center space-x-2">
                <Link href="/login">
                  <Button variant="ghost" size="sm">
                    Login
                  </Button>
                </Link>
                <Link href="/register">
                  <Button variant="primary" size="sm">
                    Sign Up
                  </Button>
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="text-gray-700 hover:text-primary p-2"
            >
              <svg
                className="h-6 w-6"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                {mobileMenuOpen ? (
                  <path d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-gray-200">
          <div className="px-2 pt-2 pb-3 space-y-1">
            <Link
              href="/jobs"
              className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-primary hover:bg-gray-50"
            >
              Find Jobs
            </Link>
            {isAuthenticated ? (
              <>
                <div className="px-3 py-2 text-sm font-medium text-gray-900 border-b border-gray-200">
                  {getUserDisplayName()}
                </div>
                <Link
                  href={user?.role === 'job_seeker' ? '/dashboard' : '/employer/dashboard'}
                  className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-primary hover:bg-gray-50"
                >
                  Dashboard
                </Link>
                <button
                  onClick={handleLogout}
                  className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-primary hover:bg-gray-50"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  href="/login"
                  className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-primary hover:bg-gray-50"
                >
                  Login
                </Link>
                <Link
                  href="/register"
                  className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-primary hover:bg-gray-50"
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}

