import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Job } from '@/types';
import { formatTimeAgo, formatSalary } from '@/lib/utils';
import { MapPin, Briefcase, Clock, DollarSign } from 'lucide-react';

interface JobCardProps {
  job: Job;
}

export function JobCard({ job }: JobCardProps) {
  return (
    <Link href={`/jobs/${job.id}`}>
      <Card hover className="h-full transition-all duration-200">
        <div className="flex justify-between items-start mb-3">
          <div>
            <h3 className="text-xl font-semibold text-gray-900 hover:text-primary transition-colors">
              {job.title}
            </h3>
            <p className="text-gray-600 mt-1">{job.company_name || 'Company Name'}</p>
          </div>
          <Badge variant="primary">{job.job_type}</Badge>
        </div>

        <div className="space-y-2 mb-4">
          <div className="flex items-center text-sm text-gray-600">
            <MapPin size={16} className="mr-2" />
            {job.location}
          </div>
          <div className="flex items-center text-sm text-gray-600">
            <Briefcase size={16} className="mr-2" />
            {job.experience_level}
          </div>
          {(job.salary_min || job.salary_max) && (
            <div className="flex items-center text-sm text-gray-600">
              <DollarSign size={16} className="mr-2" />
              {formatSalary(job.salary_min, job.salary_max)}
            </div>
          )}
          <div className="flex items-center text-sm text-gray-500">
            <Clock size={16} className="mr-2" />
            Posted {formatTimeAgo(job.posted_date)}
          </div>
        </div>

        <p className="text-gray-600 text-sm mb-4 line-clamp-2">
          {job.description}
        </p>

        <div className="flex flex-wrap gap-2">
          {job.skills.slice(0, 4).map((skill) => (
            <Badge key={skill} variant="default">
              {skill}
            </Badge>
          ))}
          {job.skills.length > 4 && (
            <Badge variant="default">+{job.skills.length - 4} more</Badge>
          )}
        </div>
      </Card>
    </Link>
  );
}

