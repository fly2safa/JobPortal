'use client';

import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Button } from '@/components/ui/Button';
import { JOB_TYPES, EXPERIENCE_LEVELS } from '@/constants';
import { Search, X } from 'lucide-react';

interface JobFiltersProps {
  filters: {
    query: string;
    location: string;
    job_type: string;
    experience_level: string;
  };
  onFilterChange: (name: string, value: string) => void;
  onClearFilters: () => void;
}

export function JobFilters({ filters, onFilterChange, onClearFilters }: JobFiltersProps) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="lg:col-span-2">
          <Input
            placeholder="Search jobs by title, skills..."
            value={filters.query}
            onChange={(e) => onFilterChange('query', e.target.value)}
            className="w-full"
          />
        </div>
        
        <Input
          placeholder="Location"
          value={filters.location}
          onChange={(e) => onFilterChange('location', e.target.value)}
        />

        <Select
          options={[
            { value: '', label: 'All Job Types' },
            ...JOB_TYPES.map((type) => ({ value: type.value, label: type.label })),
          ]}
          value={filters.job_type}
          onChange={(e) => onFilterChange('job_type', e.target.value)}
        />

        <Select
          options={[
            { value: '', label: 'All Experience Levels' },
            ...EXPERIENCE_LEVELS.map((level) => ({ value: level.value, label: level.label })),
          ]}
          value={filters.experience_level}
          onChange={(e) => onFilterChange('experience_level', e.target.value)}
        />

        <Button
          variant="outline"
          onClick={onClearFilters}
          className="flex items-center justify-center"
        >
          <X size={16} className="mr-2" />
          Clear Filters
        </Button>
      </div>
    </div>
  );
}

