import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { Search, Briefcase, Users, Zap, Target, TrendingUp, Award, Clock } from 'lucide-react';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-white">
      <Navbar />

      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-primary to-primary-600 text-white overflow-hidden">
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
                Find Your Dream Job with{' '}
                <span className="text-yellow-300">AI-Powered</span> Matching
              </h1>
              <p className="text-xl mb-8 text-blue-100">
                Connect with top employers and discover opportunities tailored to your skills and experience.
                TalentNest uses advanced AI to match you with your perfect role.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Link href="/jobs">
                  <Button variant="secondary" size="lg" className="w-full sm:w-auto bg-white text-primary hover:bg-gray-100">
                    <Search size={20} className="mr-2" />
                    Browse Jobs
                  </Button>
                </Link>
                <Link href="/register">
                  <Button variant="outline" size="lg" className="w-full sm:w-auto border-white text-white hover:bg-white hover:text-primary">
                    Get Started Free
                  </Button>
                </Link>
              </div>
              <div className="mt-8 flex items-center gap-8 text-sm">
                <div>
                  <div className="text-3xl font-bold">10K+</div>
                  <div className="text-blue-100">Active Jobs</div>
                </div>
                <div>
                  <div className="text-3xl font-bold">50K+</div>
                  <div className="text-blue-100">Job Seekers</div>
                </div>
                <div>
                  <div className="text-3xl font-bold">2K+</div>
                  <div className="text-blue-100">Companies</div>
                </div>
              </div>
            </div>
            <div className="hidden md:block">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-yellow-400 to-pink-400 rounded-lg blur-3xl opacity-30"></div>
                <div className="relative bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
                  <div className="space-y-4">
                    <div className="bg-white/20 backdrop-blur rounded-lg p-4 animate-pulse">
                      <div className="h-4 bg-white/40 rounded w-3/4 mb-2"></div>
                      <div className="h-3 bg-white/30 rounded w-1/2"></div>
                    </div>
                    <div className="bg-white/20 backdrop-blur rounded-lg p-4 animate-pulse delay-100">
                      <div className="h-4 bg-white/40 rounded w-2/3 mb-2"></div>
                      <div className="h-3 bg-white/30 rounded w-3/4"></div>
                    </div>
                    <div className="bg-white/20 backdrop-blur rounded-lg p-4 animate-pulse delay-200">
                      <div className="h-4 bg-white/40 rounded w-5/6 mb-2"></div>
                      <div className="h-3 bg-white/30 rounded w-2/3"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Why Choose TalentNest?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              We combine cutting-edge AI technology with a user-friendly platform to revolutionize job hunting.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <Card hover className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Zap className="text-primary" size={32} />
              </div>
              <h3 className="text-xl font-semibold mb-2">AI-Powered Matching</h3>
              <p className="text-gray-600">
                Our advanced algorithms analyze your profile and match you with the most relevant opportunities.
              </p>
            </Card>

            <Card hover className="text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Target className="text-green-600" size={32} />
              </div>
              <h3 className="text-xl font-semibold mb-2">Personalized Recommendations</h3>
              <p className="text-gray-600">
                Get job suggestions tailored to your skills, experience, and career goals.
              </p>
            </Card>

            <Card hover className="text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Clock className="text-purple-600" size={32} />
              </div>
              <h3 className="text-xl font-semibold mb-2">Fast Application Process</h3>
              <p className="text-gray-600">
                Apply to multiple jobs with one click. Upload your resume once and use it everywhere.
              </p>
            </Card>

            <Card hover className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="text-blue-600" size={32} />
              </div>
              <h3 className="text-xl font-semibold mb-2">Top Employers</h3>
              <p className="text-gray-600">
                Connect with leading companies across various industries looking for talented professionals.
              </p>
            </Card>

            <Card hover className="text-center">
              <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Award className="text-yellow-600" size={32} />
              </div>
              <h3 className="text-xl font-semibold mb-2">Career Growth</h3>
              <p className="text-gray-600">
                Access resources, tips, and insights to help you advance your career and land your dream job.
              </p>
            </Card>

            <Card hover className="text-center">
              <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="text-red-600" size={32} />
              </div>
              <h3 className="text-xl font-semibold mb-2">Real-Time Updates</h3>
              <p className="text-gray-600">
                Get instant notifications about new opportunities, application status, and interview invites.
              </p>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-xl text-gray-600">
              Get started in 3 simple steps
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-12">
            <div className="text-center">
              <div className="w-20 h-20 bg-primary rounded-full flex items-center justify-center text-white text-3xl font-bold mx-auto mb-4">
                1
              </div>
              <h3 className="text-xl font-semibold mb-2">Create Your Profile</h3>
              <p className="text-gray-600">
                Sign up and build your professional profile. Upload your resume and let our AI parse your skills.
              </p>
            </div>

            <div className="text-center">
              <div className="w-20 h-20 bg-primary rounded-full flex items-center justify-center text-white text-3xl font-bold mx-auto mb-4">
                2
              </div>
              <h3 className="text-xl font-semibold mb-2">Get Matched</h3>
              <p className="text-gray-600">
                Our AI analyzes your profile and recommends the best job opportunities that match your qualifications.
              </p>
            </div>

            <div className="text-center">
              <div className="w-20 h-20 bg-primary rounded-full flex items-center justify-center text-white text-3xl font-bold mx-auto mb-4">
                3
              </div>
              <h3 className="text-xl font-semibold mb-2">Apply & Connect</h3>
              <p className="text-gray-600">
                Apply to jobs with one click and track your applications. Get interview invites and land your dream job.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-primary to-primary-600 text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to Start Your Journey?
          </h2>
          <p className="text-xl mb-8 text-blue-100">
            Join thousands of professionals who found their dream jobs through TalentNest.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/register?role=job_seeker">
              <Button variant="secondary" size="lg" className="w-full sm:w-auto bg-white text-primary hover:bg-gray-100">
                I&apos;m Looking for a Job
              </Button>
            </Link>
            <Link href="/register?role=employer">
              <Button variant="outline" size="lg" className="w-full sm:w-auto border-white text-white hover:bg-white hover:text-primary">
                I&apos;m Hiring Talent
              </Button>
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}

