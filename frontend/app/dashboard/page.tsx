'use client';

import { useEffect } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/hooks/useAuth';
import Link from 'next/link';
import { Briefcase, FileText, Star, TrendingUp, Clock } from 'lucide-react';

export default function DashboardPage() {
  useAuth(true);

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
          <p className="text-gray-600">Welcome back! Here&apos;s your job search overview.</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Applications Sent</p>
                <p className="text-3xl font-bold text-gray-900">12</p>
                <p className="text-sm text-green-600 mt-1">+3 this week</p>
              </div>
              <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                <FileText className="text-primary" size={24} />
              </div>
            </div>
          </Card>

          <Card>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">In Review</p>
                <p className="text-3xl font-bold text-gray-900">5</p>
                <p className="text-sm text-blue-600 mt-1">Active applications</p>
              </div>
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                <Clock className="text-blue-600" size={24} />
              </div>
            </div>
          </Card>

          <Card>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Interviews</p>
                <p className="text-3xl font-bold text-gray-900">2</p>
                <p className="text-sm text-purple-600 mt-1">Upcoming</p>
              </div>
              <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center">
                <Star className="text-purple-600" size={24} />
              </div>
            </div>
          </Card>
        </div>

        {/* Quick Actions */}
        <Card>
          <CardTitle>Quick Actions</CardTitle>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Link href="/jobs">
                <Button variant="outline" className="w-full justify-start" size="lg">
                  <Briefcase size={20} className="mr-3" />
                  Browse Jobs
                </Button>
              </Link>
              <Link href="/dashboard/recommendations">
                <Button variant="outline" className="w-full justify-start" size="lg">
                  <Star size={20} className="mr-3" />
                  View Recommendations
                </Button>
              </Link>
              <Link href="/dashboard/profile">
                <Button variant="outline" className="w-full justify-start" size="lg">
                  <FileText size={20} className="mr-3" />
                  Update Profile
                </Button>
              </Link>
              <Link href="/dashboard/assistant">
                <Button variant="outline" className="w-full justify-start" size="lg">
                  <TrendingUp size={20} className="mr-3" />
                  AI Career Assistant
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>

        {/* Recent Applications */}
        <Card>
          <CardTitle>Recent Applications</CardTitle>
          <CardContent>
            <div className="space-y-4">
              {[1, 2, 3].map((i) => (
                <div key={i} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div>
                    <h4 className="font-semibold text-gray-900">Senior Frontend Developer</h4>
                    <p className="text-sm text-gray-600">TechCorp Inc. • San Francisco, CA</p>
                    <p className="text-xs text-gray-500 mt-1">Applied 2 days ago</p>
                  </div>
                  <div className="text-right">
                    <span className="inline-block px-3 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">
                      Reviewing
                    </span>
                  </div>
                </div>
              ))}
            </div>
            <Link href="/dashboard/applications">
              <Button variant="ghost" className="w-full mt-4">
                View All Applications
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}

