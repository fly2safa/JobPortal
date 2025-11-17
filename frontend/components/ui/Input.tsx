import { InputHTMLAttributes, forwardRef } from 'react';
import { cn } from '@/lib/utils';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, helperText, className, style, ...props }, ref) => {
    return (
      <div className="w-full" style={style}>
        {label && (
          <label className="block text-sm font-medium text-gray-700 mb-1" style={style}>
            {label}
            {props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        <input
          ref={ref}
          className={cn(
            'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent hover:border-primary hover:shadow-sm transition-all duration-200',
            error ? 'border-red-500' : 'border-gray-300',
            props.disabled && 'bg-gray-100 cursor-not-allowed',
            className
          )}
          style={style}
          {...props}
        />
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

Input.displayName = 'Input';

