'use client';

import { useState, useRef } from 'react';
import { Button } from '@/components/ui/Button';
import { Upload, CheckCircle, AlertCircle } from 'lucide-react';
import apiClient from '@/lib/api';
import { ResumeUploadResponse } from '@/types';

interface ResumeUploadProps {
  onUploadSuccess: (response: ResumeUploadResponse) => void;
}

export function ResumeUpload({ onUploadSuccess }: ResumeUploadProps) {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<ResumeUploadResponse | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateFile = (file: File): string | null => {
    const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const validExtensions = ['.pdf', '.doc', '.docx'];
    const maxSize = 10 * 1024 * 1024; // 10MB

    // Check file type
    const fileExtension = file.name.toLowerCase().slice(file.name.lastIndexOf('.'));
    if (!validTypes.includes(file.type) && !validExtensions.includes(fileExtension)) {
      return 'Invalid file type. Please upload PDF, DOC, or DOCX files only.';
    }

    // Check file size
    if (file.size > maxSize) {
      return 'File is too large. Maximum size is 10MB.';
    }

    // Check if file is empty
    if (file.size === 0) {
      return 'File is empty. Please select a valid resume file.';
    }

    return null;
  };

  const handleFileUpload = async (file: File) => {
    setError(null);
    setSuccess(null);

    // Validate file
    const validationError = validateFile(file);
    if (validationError) {
      setError(validationError);
      return;
    }

    setIsUploading(true);

    try {
      const response = await apiClient.uploadResume(file);
      setSuccess(response);
      onUploadSuccess(response);
      
      // Clear file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }

      // Clear success message after 5 seconds
      setTimeout(() => {
        setSuccess(null);
      }, 5000);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to upload resume. Please try again.';
      setError(errorMessage);
    } finally {
      setIsUploading(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const file = e.dataTransfer.files?.[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="space-y-4">
      {/* Upload Area */}
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          dragActive
            ? 'border-primary bg-primary/5'
            : 'border-gray-300 hover:border-gray-400'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <Upload className="mx-auto text-gray-400 mb-4" size={48} />
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          Upload Your Resume
        </h3>
        <p className="text-sm text-gray-600 mb-4">
          Drag and drop your file here, or click to browse
        </p>
        <p className="text-xs text-gray-500 mb-4">
          PDF, DOC, or DOCX. Max size 10MB. Our AI will parse your resume automatically.
        </p>
        
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.doc,.docx,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
          onChange={handleFileChange}
          className="hidden"
        />
        
        <Button
          variant="primary"
          onClick={handleButtonClick}
          isLoading={isUploading}
          disabled={isUploading}
        >
          <Upload size={16} className="mr-2" />
          {isUploading ? 'Uploading...' : 'Choose File'}
        </Button>
      </div>

      {/* Success Message */}
      {success && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-start">
            <CheckCircle className="text-green-600 mt-0.5 mr-3 flex-shrink-0" size={20} />
            <div className="flex-1">
              <h4 className="text-green-900 font-medium mb-1">
                {success.message}
              </h4>
              <div className="text-sm text-green-700 space-y-1">
                <p>
                  <strong>Parsing Method:</strong>{' '}
                  <span className="capitalize">{success.resume.parsing_method}</span>
                  {success.resume.ai_used && (
                    <span className="ml-2 px-2 py-0.5 bg-green-100 text-green-800 text-xs rounded">
                      AI Enhanced
                    </span>
                  )}
                </p>
                <p>
                  <strong>Confidence:</strong>{' '}
                  {(success.resume.parsing_confidence * 100).toFixed(0)}%
                </p>
                {success.resume.skills_extracted.length > 0 && (
                  <div>
                    <strong>Skills Extracted:</strong>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {success.resume.skills_extracted.slice(0, 8).map((skill, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded"
                        >
                          {skill}
                        </span>
                      ))}
                      {success.resume.skills_extracted.length > 8 && (
                        <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded">
                          +{success.resume.skills_extracted.length - 8} more
                        </span>
                      )}
                    </div>
                  </div>
                )}
                {success.skills_synced && (
                  <p className="text-xs mt-2">
                    ✓ Skills have been synced to your profile
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-start">
            <AlertCircle className="text-red-600 mt-0.5 mr-3 flex-shrink-0" size={20} />
            <div>
              <h4 className="text-red-900 font-medium mb-1">Upload Failed</h4>
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Upload Progress */}
      {isUploading && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600 mr-3"></div>
            <div>
              <p className="text-sm text-blue-900 font-medium">Processing your resume...</p>
              <p className="text-xs text-blue-700">
                Extracting skills, experience, and education
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

