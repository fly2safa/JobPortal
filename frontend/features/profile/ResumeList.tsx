'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { FileText, Trash2, Eye, Download } from 'lucide-react';
import { Resume } from '@/types';
import { ParsingResults } from './ParsingResults';

interface ResumeListProps {
  resumes: Resume[];
  isLoading: boolean;
  onDelete: (resumeId: string) => void;
}

export function ResumeList({ resumes, isLoading, onDelete }: ResumeListProps) {
  const [selectedResume, setSelectedResume] = useState<Resume | null>(null);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) {
      return 'Today';
    } else if (diffDays === 1) {
      return 'Yesterday';
    } else if (diffDays < 7) {
      return `${diffDays} days ago`;
    } else if (diffDays < 30) {
      const weeks = Math.floor(diffDays / 7);
      return `${weeks} ${weeks === 1 ? 'week' : 'weeks'} ago`;
    } else if (diffDays < 365) {
      const months = Math.floor(diffDays / 30);
      return `${months} ${months === 1 ? 'month' : 'months'} ago`;
    } else {
      return date.toLocaleDateString();
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  const handleDelete = async (resumeId: string, fileName: string) => {
    if (window.confirm(`Are you sure you want to delete "${fileName}"?`)) {
      onDelete(resumeId);
    }
  };

  if (isLoading) {
    return (
      <div className="space-y-2">
        <h4 className="font-medium text-gray-900 mb-3">Uploaded Resumes</h4>
        {[1, 2].map((i) => (
          <div key={i} className="animate-pulse bg-gray-100 rounded-lg p-4 h-20"></div>
        ))}
      </div>
    );
  }

  if (resumes.length === 0) {
    return (
      <div className="text-center py-8">
        <FileText className="mx-auto text-gray-300 mb-3" size={48} />
        <h4 className="font-medium text-gray-900 mb-1">No resumes uploaded</h4>
        <p className="text-sm text-gray-600">
          Upload your first resume to get started
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h4 className="font-medium text-gray-900">
        Uploaded Resumes ({resumes.length})
      </h4>
      
      <div className="space-y-2">
        {resumes.map((resume) => (
          <div
            key={resume.id}
            className="flex items-start justify-between p-4 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <div className="flex items-start flex-1 min-w-0">
              {/* File Icon */}
              <div className="w-10 h-10 bg-red-100 rounded flex items-center justify-center flex-shrink-0">
                <FileText className="text-red-600" size={20} />
              </div>
              
              {/* File Info */}
              <div className="ml-3 flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {resume.file_name}
                  </p>
                  {resume.ai_used && (
                    <span className="px-2 py-0.5 bg-purple-100 text-purple-700 text-xs rounded flex-shrink-0">
                      AI Enhanced
                    </span>
                  )}
                </div>
                
                <div className="flex flex-wrap gap-x-3 gap-y-1 text-xs text-gray-500">
                  <span>Uploaded {formatDate(resume.created_at)}</span>
                  <span>•</span>
                  <span>{formatFileSize(resume.file_size)}</span>
                  <span>•</span>
                  <span className="capitalize">{resume.parsing_method} parsing</span>
                  <span>•</span>
                  <span>{(resume.parsing_confidence * 100).toFixed(0)}% confidence</span>
                </div>

                {/* Skills Preview */}
                {resume.skills_extracted.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {resume.skills_extracted.slice(0, 5).map((skill, index) => (
                      <span
                        key={index}
                        className="px-2 py-0.5 bg-blue-100 text-blue-700 text-xs rounded"
                      >
                        {skill}
                      </span>
                    ))}
                    {resume.skills_extracted.length > 5 && (
                      <span className="px-2 py-0.5 bg-gray-200 text-gray-700 text-xs rounded">
                        +{resume.skills_extracted.length - 5} more
                      </span>
                    )}
                  </div>
                )}

                {/* Experience & Education */}
                <div className="flex flex-wrap gap-x-3 gap-y-1 text-xs text-gray-600 mt-1">
                  {resume.experience_years && (
                    <span>📅 {resume.experience_years} years experience</span>
                  )}
                  {resume.education && (
                    <span>🎓 {resume.education}</span>
                  )}
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="flex gap-2 ml-4 flex-shrink-0">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setSelectedResume(resume)}
                title="View details"
              >
                <Eye size={16} />
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => handleDelete(resume.id, resume.file_name)}
                title="Delete"
              >
                <Trash2 size={16} className="text-red-600" />
              </Button>
            </div>
          </div>
        ))}
      </div>

      {/* Parsing Results Modal */}
      {selectedResume && (
        <ParsingResults
          resume={selectedResume}
          onClose={() => setSelectedResume(null)}
        />
      )}
    </div>
  );
}

