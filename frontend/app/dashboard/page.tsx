'use client';

import { useEffect, useState } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/hooks/useAuth';
import Link from 'next/link';
import { Briefcase, FileText, Star, TrendingUp, Clock } from 'lucide-react';
import { apiClient } from '@/lib/api';

export default function DashboardPage() {
  useAuth(true);

  const [stats, setStats] = useState({ 
    total: 0, 
    pending: 0,
    reviewing: 0, 
    shortlisted: 0,
    interview: 0,
    rejected: 0,
    accepted: 0,
    withdrawn: 0
  });
  const [recentApplications, setRecentApplications] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const statsData = await apiClient.getApplicationStats();
        setStats(statsData);
        
        const appsResponse = await apiClient.getApplications({ page: 1, page_size: 3 });
        setRecentApplications(appsResponse.applications || []);
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardData();
  }, []);

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
                <p className="text-3xl font-bold text-gray-900">
                  {loading ? '...' : stats.total}
                </p>
                <p className="text-sm text-green-600 mt-1">Total applications</p>
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
                <p className="text-3xl font-bold text-gray-900">
                  {loading ? '...' : (stats.reviewing + stats.shortlisted)}
                </p>
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
                <p className="text-3xl font-bold text-gray-900">
                  {loading ? '...' : stats.interview}
                </p>
                <p className="text-sm text-purple-600 mt-1">Scheduled</p>
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
              {loading ? (
                <div className="text-center py-4 text-gray-500">Loading applications...</div>
              ) : recentApplications.length > 0 ? (
                recentApplications.map((app) => (
                  <div key={app.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div>
                      <h4 className="font-semibold text-gray-900">{app.job?.title || 'Unknown Position'}</h4>
                      <p className="text-sm text-gray-600">
                        {app.job?.company?.name || 'Unknown Company'} • {app.job?.location || 'Location N/A'}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        Applied {new Date(app.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="text-right">
                      <span className={`inline-block px-3 py-1 text-xs font-medium rounded-full ${
                        app.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                        app.status === 'reviewing' ? 'bg-blue-100 text-blue-800' :
                        app.status === 'accepted' ? 'bg-green-100 text-green-800' :
                        app.status === 'rejected' ? 'bg-red-100 text-red-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {app.status?.charAt(0).toUpperCase() + app.status?.slice(1) || 'Pending'}
                      </span>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <p>No applications yet</p>
                  <Link href="/jobs">
                    <Button variant="outline" className="mt-4">
                      Browse Jobs
                    </Button>
                  </Link>
                </div>
              )}
            </div>
            {recentApplications.length > 0 && (
              <Link href="/dashboard/applications">
                <Button variant="ghost" className="w-full mt-4">
                  View All Applications
                </Button>
              </Link>
            )}
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}

