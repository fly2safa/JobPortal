import { RegisterForm } from '@/features/auth/RegisterForm';
import Link from 'next/link';

export default function RegisterPage() {
  return (
    <div className="min-h-screen flex items-center justify-center p-4" style={{
      background: 'linear-gradient(135deg, #075299 0%, #5a9ab3 100%)'
    }}>
      <div className="w-full max-w-md">
        {/* Logo */}
        <Link href="/" className="flex items-center justify-center mb-8">
          <span className="text-4xl">
            <span style={{ 
              fontFamily: 'Playfair Display, serif', 
              fontWeight: 700,
              background: 'linear-gradient(135deg, #a8d5e2 0%, #ffffff 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
              textShadow: 'none'
            }}>TALENT</span>
            <span style={{ fontFamily: 'Dancing Script, cursive', fontWeight: 700, color: '#a8d5e2' }}>Nest</span>
          </span>
        </Link>

        {/* Register Form */}
        <RegisterForm />
      </div>
    </div>
  );
}

