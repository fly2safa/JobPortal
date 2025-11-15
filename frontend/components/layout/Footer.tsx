import Link from 'next/link';
import Image from 'next/image';
import { Mail, MapPin, Phone } from 'lucide-react';

export function Footer() {
  return (
    <footer className="bg-gray-900 dark:bg-black text-white border-t border-gray-800 dark:border-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1">
            <div className="mb-4 flex items-center">
              <Image
                src="/logo-bird.png"
                alt="TalentNest bird logo"
                width={32}
                height={32}
                priority
                className="mr-2"
              />
              <span className="text-2xl">
                <span style={{ 
                  fontFamily: 'Playfair Display, serif', 
                  fontWeight: 700,
                  background: 'linear-gradient(135deg, #5a9ab3 0%, #a8d5e2 100%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  backgroundClip: 'text'
                }}>TALENT</span>
                <span style={{ fontFamily: 'Dancing Script, cursive', fontWeight: 700 }} className="text-white dark:text-gray-100">Nest</span>
              </span>
            </div>
            <p className="text-gray-400 dark:text-gray-500 text-sm">
              Connecting talented professionals with their dream careers through AI-powered matching.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-white dark:text-gray-100">For Job Seekers</h3>
            <ul className="space-y-2 text-gray-400 dark:text-gray-500">
              <li>
                <Link href="/jobs" className="hover:text-white dark:hover:text-gray-200 transition-colors">
                  Browse Jobs
                </Link>
              </li>
              <li>
                <Link href="/dashboard/profile" className="hover:text-white dark:hover:text-gray-200 transition-colors">
                  Create Profile
                </Link>
              </li>
              <li>
                <Link href="/dashboard/applications" className="hover:text-white dark:hover:text-gray-200 transition-colors">
                  My Applications
                </Link>
              </li>
              <li>
                <Link href="/dashboard/recommendations" className="hover:text-white dark:hover:text-gray-200 transition-colors">
                  Job Recommendations
                </Link>
              </li>
            </ul>
          </div>

          {/* Employer Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-white dark:text-gray-100">For Employers</h3>
            <ul className="space-y-2 text-gray-400 dark:text-gray-500">
              <li>
                <Link href="/employer/jobs/new" className="hover:text-white dark:hover:text-gray-200 transition-colors">
                  Post a Job
                </Link>
              </li>
              <li>
                <Link href="/employer/jobs" className="hover:text-white dark:hover:text-gray-200 transition-colors">
                  Manage Jobs
                </Link>
              </li>
              <li>
                <Link href="/employer/dashboard" className="hover:text-white dark:hover:text-gray-200 transition-colors">
                  View Applications
                </Link>
              </li>
              <li>
                <Link href="/employer/interviews" className="hover:text-white dark:hover:text-gray-200 transition-colors">
                  Schedule Interviews
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-white dark:text-gray-100">Contact Us</h3>
            <ul className="space-y-2 text-gray-400 dark:text-gray-500 text-sm">
              <li className="flex items-center space-x-2">
                <Mail size={16} />
                <span>support@talentnest.com</span>
              </li>
              <li className="flex items-center space-x-2">
                <Phone size={16} />
                <span>+1 (555) 123-4567</span>
              </li>
              <li className="flex items-center space-x-2">
                <MapPin size={16} />
                <span>San Francisco, CA</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 dark:border-gray-900 mt-8 pt-8 text-center text-gray-400 dark:text-gray-500 text-sm">
          <p>&copy; {new Date().getFullYear()} TalentNest. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}

