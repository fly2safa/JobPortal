import { LoginForm } from '@/features/auth/LoginForm';
import Link from 'next/link';
import Image from 'next/image';

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-blue-100 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        {/* Logo */}
        <Link href="/" className="flex items-center justify-center mb-6">
          <div className="flex items-center">
            <Image
              src="/logo-bird.png"
              alt="TalentNest bird logo"
              width={44}
              height={44}
              priority
              className="mr-2"
            />
            <span className="text-4xl">
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
          </div>
        </Link>

        {/* Welcome Message */}
        <div className="text-center mb-8 px-4" style={{ fontFamily: 'Playfair Display, serif' }}>
          <h1 className="text-3xl text-gray-900 mb-4" style={{ fontFamily: 'Playfair Display, serif', fontWeight: 400 }}>Welcome to Talent Nest</h1>
          <p className="text-gray-700 leading-relaxed" style={{ fontFamily: 'Playfair Display, serif', fontWeight: 400 }}>
            Your gateway to meaningful careers and exceptional talent. At Talent Nest, we connect ambitious professionals with forward-thinking employers. Whether you&apos;re seeking your next opportunity or scouting top-tier candidates, our platform is designed to help you thrive. Log in to access personalized job matches, smart hiring tools, and a community built on growth and potential.
          </p>
        </div>

        {/* Login Form */}
        <div className="max-w-md mx-auto">
          <LoginForm />
        </div>
      </div>
    </div>
  );
}

