import { LoginForm } from '@/features/auth/LoginForm';
import { Briefcase } from 'lucide-react';
import Link from 'next/link';

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-blue-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <Link href="/" className="flex items-center justify-center space-x-2 mb-8">
          <div className="w-12 h-12 bg-primary rounded-lg flex items-center justify-center">
            <Briefcase className="text-white" size={28} />
          </div>
          <span className="text-3xl font-bold text-primary">TalentNest</span>
        </Link>

        {/* Login Form */}
        <LoginForm />
      </div>
    </div>
  );
}

