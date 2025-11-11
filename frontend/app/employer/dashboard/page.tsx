'use client';

import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { useAuth, useRequireRole } from '@/hooks/useAuth';
import Link from 'next/link';
import { Briefcase, Users, Calendar, TrendingUp, Eye, CheckCircle } from 'lucide-react';

export default function EmployerDashboardPage() {
  useAuth(true);
  useRequireRole(['employer']);

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Employer Dashboard</h1>
          <p className="text-white">Manage your job postings and review applications</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <Card>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Active Jobs</p>
                <p className="text-3xl font-bold text-gray-900">8</p>
              </div>
              <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                <Briefcase className="text-primary" size={24} />
              </div>
            </div>
          </Card>

          <Card>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Total Applications</p>
                <p className="text-3xl font-bold text-gray-900">156</p>
                <p className="text-sm text-green-600 mt-1">+12 this week</p>
              </div>
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                <Users className="text-blue-600" size={24} />
              </div>
            </div>
          </Card>

          <Card>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">To Review</p>
                <p className="text-3xl font-bold text-gray-900">23</p>
              </div>
              <div className="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center">
                <Eye className="text-yellow-600" size={24} />
              </div>
            </div>
          </Card>

          <Card>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Interviews</p>
                <p className="text-3xl font-bold text-gray-900">5</p>
                <p className="text-sm text-purple-600 mt-1">This week</p>
              </div>
              <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center">
                <Calendar className="text-purple-600" size={24} />
              </div>
            </div>
          </Card>
        </div>

        {/* Quick Actions */}
        <Card>
          <CardTitle>Quick Actions</CardTitle>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Link href="/employer/jobs/new">
                <Button variant="primary" className="w-full justify-start" size="lg">
                  <Briefcase size={20} className="mr-3" />
                  Post New Job
                </Button>
              </Link>
              <Link href="/employer/jobs">
                <Button variant="outline" className="w-full justify-start" size="lg">
                  <Eye size={20} className="mr-3" />
                  Manage Jobs
                </Button>
              </Link>
              <Link href="/employer/interviews">
                <Button variant="outline" className="w-full justify-start" size="lg">
                  <Calendar size={20} className="mr-3" />
                  View Interviews
                </Button>
              </Link>
              <Button variant="outline" className="w-full justify-start" size="lg">
                <TrendingUp size={20} className="mr-3" />
                View Analytics
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Active Jobs */}
        <Card>
          <CardTitle>Your Active Jobs</CardTitle>
          <CardContent>
            <div className="space-y-4">
              {[1, 2, 3].map((i) => (
                <div key={i} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                  <div className="flex-1">
                    <h4 className="font-semibold text-gray-900">Senior Frontend Developer</h4>
                    <p className="text-sm text-gray-600">Posted 5 days ago • 24 applications</p>
                    <div className="flex items-center space-x-4 mt-2">
                      <span className="text-xs text-gray-500">8 New • 12 Reviewing • 4 Shortlisted</span>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Link href={`/employer/jobs/${i}/applications`}>
                      <Button variant="outline" size="sm">
                        View Applications
                      </Button>
                    </Link>
                    <Link href={`/employer/jobs/${i}/edit`}>
                      <Button variant="ghost" size="sm">
                        Edit
                      </Button>
                    </Link>
                  </div>
                </div>
              ))}
            </div>
            <Link href="/employer/jobs">
              <Button variant="ghost" className="w-full mt-4">
                View All Jobs
              </Button>
            </Link>
          </CardContent>
        </Card>

        {/* Recent Applications */}
        <Card>
          <CardTitle>Recent Applications</CardTitle>
          <CardContent>
            <div className="space-y-4">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="flex items-center justify-between p-4 border-b border-gray-200 last:border-0">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-primary rounded-full flex items-center justify-center text-white font-bold text-lg">
                      JD
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900">John Doe</h4>
                      <p className="text-sm text-gray-600">Applied for Senior Frontend Developer</p>
                      <p className="text-xs text-gray-500">2 hours ago</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Button variant="outline" size="sm">
                      View Profile
                    </Button>
                    <Button variant="primary" size="sm">
                      <CheckCircle size={14} className="mr-1" />
                      Review
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}

