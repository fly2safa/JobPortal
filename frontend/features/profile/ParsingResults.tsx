'use client';

import { Resume } from '@/types';
import { X, FileText, Briefcase, GraduationCap, Award, Brain } from 'lucide-react';
import { Button } from '@/components/ui/Button';

interface ParsingResultsProps {
  resume: Resume;
  onClose: () => void;
}

export function ParsingResults({ resume, onClose }: ParsingResultsProps) {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <div>
            <h2 className="text-xl font-bold text-gray-900">Resume Details</h2>
            <p className="text-sm text-gray-600 mt-1">{resume.file_name}</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* Parsing Metadata */}
          <div className="bg-gray-50 rounded-lg p-4">
            <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
              <Brain className="mr-2" size={16} />
              Parsing Information
            </h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-xs text-gray-600">Method</p>
                <p className="text-sm font-medium text-gray-900 capitalize">
                  {resume.parsing_method}
                  {resume.ai_used && (
                    <span className="ml-2 px-2 py-0.5 bg-purple-100 text-purple-700 text-xs rounded">
                      AI Enhanced
                    </span>
                  )}
                </p>
              </div>
              <div>
                <p className="text-xs text-gray-600">Confidence</p>
                <p className="text-sm font-medium text-gray-900">
                  {(resume.parsing_confidence * 100).toFixed(0)}%
                </p>
              </div>
              <div>
                <p className="text-xs text-gray-600">Uploaded</p>
                <p className="text-sm font-medium text-gray-900">
                  {formatDate(resume.created_at)}
                </p>
              </div>
              <div>
                <p className="text-xs text-gray-600">File Size</p>
                <p className="text-sm font-medium text-gray-900">
                  {(resume.file_size / (1024 * 1024)).toFixed(2)} MB
                </p>
              </div>
            </div>
          </div>

          {/* Skills */}
          {resume.skills_extracted.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
                <Award className="mr-2" size={16} />
                Skills Extracted ({resume.skills_extracted.length})
              </h3>
              <div className="flex flex-wrap gap-2">
                {resume.skills_extracted.map((skill, index) => (
                  <span
                    key={index}
                    className="px-3 py-1.5 bg-blue-100 text-blue-700 text-sm rounded-full"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Experience */}
          {resume.experience_years !== undefined && resume.experience_years !== null && (
            <div>
              <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
                <Briefcase className="mr-2" size={16} />
                Experience
              </h3>
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-sm text-gray-900">
                  <strong>{resume.experience_years} years</strong> of professional experience
                </p>
                {resume.work_experience && (
                  <p className="text-sm text-gray-700 mt-2">{resume.work_experience}</p>
                )}
              </div>
            </div>
          )}

          {/* Education */}
          {resume.education && (
            <div>
              <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
                <GraduationCap className="mr-2" size={16} />
                Education
              </h3>
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-sm text-gray-900">{resume.education}</p>
              </div>
            </div>
          )}

          {/* Summary */}
          {resume.summary && (
            <div>
              <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
                <FileText className="mr-2" size={16} />
                Professional Summary
              </h3>
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-sm text-gray-700 leading-relaxed">{resume.summary}</p>
              </div>
            </div>
          )}

          {/* Work Experience (detailed) */}
          {resume.work_experience && !resume.summary && (
            <div>
              <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
                <FileText className="mr-2" size={16} />
                Work History
              </h3>
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-sm text-gray-700 leading-relaxed">
                  {resume.work_experience}
                </p>
              </div>
            </div>
          )}

          {/* No Data Message */}
          {!resume.skills_extracted.length &&
            !resume.experience_years &&
            !resume.education &&
            !resume.summary &&
            !resume.work_experience && (
              <div className="text-center py-8">
                <FileText className="mx-auto text-gray-300 mb-3" size={48} />
                <p className="text-gray-600">
                  No detailed information was extracted from this resume.
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  You may need to update your profile manually.
                </p>
              </div>
            )}
        </div>

        {/* Footer */}
        <div className="flex justify-end gap-3 p-6 border-t bg-gray-50">
          <Button variant="outline" onClick={onClose}>
            Close
          </Button>
        </div>
      </div>
    </div>
  );
}

