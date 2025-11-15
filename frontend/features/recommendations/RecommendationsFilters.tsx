'use client';

import { Card } from '@/components/ui/Card';
import { ChevronDown } from 'lucide-react';

interface FilterOption {
  value: string;
  label: string;
}

interface RecommendationsFiltersProps {
  filters: {
    workingSchedule: string[];
    employmentType: string[];
    minMatchScore: number;
  };
  onFilterChange: (category: string, value: string) => void;
  onMinScoreChange: (score: number) => void;
}

const WORKING_SCHEDULE_OPTIONS: FilterOption[] = [
  { value: 'full-time', label: 'Full time' },
  { value: 'part-time', label: 'Part time' },
  { value: 'internship', label: 'Internship' },
  { value: 'project-work', label: 'Project work' },
  { value: 'contract', label: 'Contract' },
];

const EMPLOYMENT_TYPE_OPTIONS: FilterOption[] = [
  { value: 'full-day', label: 'Full day' },
  { value: 'flexible-schedule', label: 'Flexible schedule' },
  { value: 'shift-work', label: 'Shift work' },
  { value: 'remote', label: 'Remote work' },
  { value: 'hybrid', label: 'Hybrid' },
];

export function RecommendationsFilters({
  filters,
  onFilterChange,
  onMinScoreChange,
}: RecommendationsFiltersProps) {
  return (
    <Card className="p-6 sticky top-24">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-bold text-gray-900">Filters</h3>
        <ChevronDown size={20} className="text-gray-600" />
      </div>

      {/* Match Score Filter */}
      <div className="mb-6">
        <h4 className="text-sm font-semibold text-gray-700 mb-3">
          Minimum Match Score
        </h4>
        <div className="space-y-2">
          <input
            type="range"
            min="0"
            max="100"
            step="5"
            value={filters.minMatchScore}
            onChange={(e) => onMinScoreChange(parseInt(e.target.value))}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider-thumb"
          />
          <div className="flex justify-between text-sm text-gray-600">
            <span>0%</span>
            <span className="font-semibold text-primary">
              {filters.minMatchScore}%
            </span>
            <span>100%</span>
          </div>
        </div>
      </div>

      {/* Working Schedule */}
      <div className="mb-6">
        <h4 className="text-sm font-semibold text-gray-700 mb-3">
          Working schedule
        </h4>
        <div className="space-y-2">
          {WORKING_SCHEDULE_OPTIONS.map((option) => (
            <label
              key={option.value}
              className="flex items-center cursor-pointer group"
            >
              <input
                type="checkbox"
                checked={filters.workingSchedule.includes(option.value)}
                onChange={() => onFilterChange('workingSchedule', option.value)}
                className="w-5 h-5 rounded border-gray-300 cursor-pointer checked:bg-primary checked:border-primary hover:border-primary/50 focus:ring-primary transition-colors"
              />
              <span className="ml-3 text-sm text-gray-700 group-hover:text-primary transition-colors">
                {option.label}
              </span>
            </label>
          ))}
        </div>
      </div>

      {/* Employment Type */}
      <div>
        <h4 className="text-sm font-semibold text-gray-700 mb-3">
          Employment type
        </h4>
        <div className="space-y-2">
          {EMPLOYMENT_TYPE_OPTIONS.map((option) => (
            <label
              key={option.value}
              className="flex items-center cursor-pointer group"
            >
              <input
                type="checkbox"
                checked={filters.employmentType.includes(option.value)}
                onChange={() => onFilterChange('employmentType', option.value)}
                className="w-5 h-5 rounded border-gray-300 cursor-pointer checked:bg-primary checked:border-primary hover:border-primary/50 focus:ring-primary transition-colors"
              />
              <span className="ml-3 text-sm text-gray-700 group-hover:text-primary transition-colors">
                {option.label}
              </span>
            </label>
          ))}
        </div>
      </div>

      <style jsx>{`
        .slider-thumb::-webkit-slider-thumb {
          appearance: none;
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background: #075299;
          cursor: pointer;
          border: 3px solid white;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }
        .slider-thumb::-moz-range-thumb {
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background: #075299;
          cursor: pointer;
          border: 3px solid white;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }
      `}</style>
    </Card>
  );
}

