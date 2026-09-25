import Link from 'next/link';
import Image from 'next/image';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { Card } from '@/components/ui/Card';
import { APP_NAME, APP_VERSION } from '@/constants';
import { Briefcase, Users, Sparkles } from 'lucide-react';

async function getApiVersion(): Promise<string | null> {
  try {
    const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const res = await fetch(`${base}/health`, { cache: 'no-store' });
    if (!res.ok) return null;
    const data = await res.json();
    return typeof data.version === 'string' ? data.version : null;
  } catch {
    return null;
  }
}

export default async function AboutPage() {
  const apiVersion = await getApiVersion();

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 flex flex-col">
      <Navbar />

      <main className="flex-1 max-w-3xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex items-center mb-8">
          <Image
            src="/logo-bird.png"
            alt={`${APP_NAME} bird logo`}
            width={48}
            height={48}
            className="mr-3"
          />
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100" style={{ fontFamily: 'Playfair Display, serif' }}>
              About {APP_NAME}
            </h1>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Version {APP_VERSION}
              {apiVersion && apiVersion !== APP_VERSION && ` · API ${apiVersion}`}
            </p>
          </div>
        </div>

        <Card className="mb-6">
          <p className="text-sm text-gray-700 leading-relaxed">
            {APP_NAME} is a job portal that connects job seekers with employers.
            Candidates can build a profile, upload a resume, search openings, and apply.
            Employers can post jobs, review applications, and move candidates through hiring.
            Optional AI features help with recommendations, resume parsing, cover letters,
            and a career assistant.
          </p>
        </Card>

        <div className="grid sm:grid-cols-2 gap-4 mb-6">
          <Card>
            <div className="flex items-center mb-3">
              <Users className="text-primary mr-2" size={22} />
              <h2 className="text-lg font-semibold text-gray-900">For job seekers</h2>
            </div>
            <ul className="text-sm text-gray-700 space-y-2 list-disc list-inside">
              <li>Search and filter jobs</li>
              <li>Apply with a resume and cover letter</li>
              <li>Track application status</li>
              <li>Get AI job recommendations and career help</li>
            </ul>
          </Card>
          <Card>
            <div className="flex items-center mb-3">
              <Briefcase className="text-primary mr-2" size={22} />
              <h2 className="text-lg font-semibold text-gray-900">For employers</h2>
            </div>
            <ul className="text-sm text-gray-700 space-y-2 list-disc list-inside">
              <li>Post and manage job listings</li>
              <li>Review and shortlist applicants</li>
              <li>Schedule interviews</li>
              <li>See AI-suggested candidate matches</li>
            </ul>
          </Card>
        </div>

        <Card>
          <div className="flex items-center mb-3">
            <Sparkles className="text-primary mr-2" size={22} />
            <h2 className="text-lg font-semibold text-gray-900">Built with</h2>
          </div>
          <p className="text-sm text-gray-700">
            Next.js and Tailwind CSS on the frontend, FastAPI on the backend,
            MongoDB for data, and OpenAI for optional AI features.
          </p>
        </Card>

        <p className="mt-8 text-sm text-gray-600 dark:text-gray-400">
          <Link href="/jobs" className="text-primary hover:underline">
            Browse jobs
          </Link>
          {' · '}
          <Link href="/register" className="text-primary hover:underline">
            Create an account
          </Link>
        </p>
      </main>

      <Footer />
    </div>
  );
}
