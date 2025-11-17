'use client';

import { useState, InputHTMLAttributes, forwardRef } from 'react';
import { Eye, EyeOff } from 'lucide-react';
import { cn } from '@/lib/utils';

interface PasswordInputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
  error?: string;
  helperText?: string;
  showPassword?: boolean;
  onToggleVisibility?: () => void;
}

export const PasswordInput = forwardRef<HTMLInputElement, PasswordInputProps>(
  ({ label, error, helperText, className, style, showPassword: externalShowPassword, onToggleVisibility, ...props }, ref) => {
    const [internalShowPassword, setInternalShowPassword] = useState(false);

    // Use external state if provided, otherwise use internal state
    const showPassword = externalShowPassword !== undefined ? externalShowPassword : internalShowPassword;
    
    const togglePasswordVisibility = () => {
      if (onToggleVisibility) {
        onToggleVisibility();
      } else {
        setInternalShowPassword((prev) => !prev);
      }
    };

    return (
      <div className="w-full" style={style}>
        {label && (
          <label className="block text-sm font-medium text-gray-700 mb-1" style={style}>
            {label}
            {props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        <div className="relative">
          <input
            ref={ref}
            type={showPassword ? 'text' : 'password'}
            className={cn(
              'w-full px-4 py-2 pr-10 border rounded-lg text-gray-900 focus:ring-2 focus:ring-primary focus:border-transparent hover:border-primary hover:shadow-sm transition-all duration-200',
              error ? 'border-red-500' : 'border-gray-300',
              props.disabled && 'bg-gray-100 cursor-not-allowed',
              className
            )}
            style={style}
            {...props}
          />
          <button
            type="button"
            onClick={togglePasswordVisibility}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 focus:outline-none focus:text-primary transition-colors"
            tabIndex={-1}
            aria-label={showPassword ? 'Hide password' : 'Show password'}
          >
            {showPassword ? (
              <Eye size={20} />
            ) : (
              <EyeOff size={20} />
            )}
          </button>
        </div>
        {error && (
          <p className="mt-1 text-sm text-red-600" style={style}>{error}</p>
        )}
        {helperText && !error && (
          <p className="mt-1 text-sm text-gray-500" style={style}>{helperText}</p>
        )}
      </div>
    );
  }
);

PasswordInput.displayName = 'PasswordInput';

