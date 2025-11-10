'use client';

import { ReactNode } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Navbar } from './Navbar';
import { Footer } from './Footer';
import { Home, User, FileText, Star, MessageSquare, Calendar, Briefcase } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuthStore } from '@/store/authStore';

interface DashboardLayoutProps {
  children: ReactNode;
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const pathname = usePathname();
  const { user } = useAuthStore();

  const isJobSeeker = user?.role === 'job_seeker';

  const jobSeekerLinks = [
    { href: '/dashboard', icon: Home, label: 'Dashboard' },
    { href: '/dashboard/profile', icon: User, label: 'Profile' },
    { href: '/dashboard/applications', icon: FileText, label: 'My Applications' },
    { href: '/dashboard/recommendations', icon: Star, label: 'Recommendations' },
    { href: '/dashboard/assistant', icon: MessageSquare, label: 'AI Assistant' },
    { href: '/dashboard/interviews', icon: Calendar, label: 'Interviews' },
  ];

  const employerLinks = [
    { href: '/employer/dashboard', icon: Home, label: 'Dashboard' },
    { href: '/employer/jobs', icon: Briefcase, label: 'My Jobs' },
    { href: '/employer/jobs/new', icon: FileText, label: 'Post New Job' },
    { href: '/employer/interviews', icon: Calendar, label: 'Interviews' },
  ];

  const links = isJobSeeker ? jobSeekerLinks : employerLinks;

  return (
    <div className="min-h-screen" style={{
      background: 'linear-gradient(135deg, #075299 0%, #5a9ab3 100%)'
    }}>
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid lg:grid-cols-4 gap-8">
          {/* Sidebar */}
          <aside className="lg:col-span-1">
            <div className="bg-white rounded-lg border border-gray-200 p-4 sticky top-24">
              <nav className="space-y-1">
                {links.map((link) => {
                  const Icon = link.icon;
                  const isActive = pathname === link.href;
                  
                  return (
                    <Link
                      key={link.href}
                      href={link.href}
                      className={cn(
                        'flex items-center px-4 py-3 rounded-lg text-sm font-medium transition-colors',
                        isActive
                          ? 'bg-primary text-white'
                          : 'text-gray-700 hover:bg-gray-100'
                      )}
                    >
                      <Icon size={20} className="mr-3" />
                      {link.label}
                    </Link>
                  );
                })}
              </nav>
            </div>
          </aside>

          {/* Main Content */}
          <main className="lg:col-span-3">
            {children}
          </main>
        </div>
      </div>

      <Footer />
    </div>
  );
}

