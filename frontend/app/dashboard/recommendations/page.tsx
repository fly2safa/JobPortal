'use client';

import { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { useAuth } from '@/hooks/useAuth';
import { JobRecommendation } from '@/types';
import { Bookmark, BookmarkCheck, MapPin, Calendar, ChevronDown, Search, Settings, Briefcase } from 'lucide-react';
import Image from 'next/image';
import { formatDate } from '@/lib/utils';
import Link from 'next/link';
import apiClient from '@/lib/api';

export default function RecommendationsPage() {
  useAuth(true);
  const [recommendations, setRecommendations] = useState<JobRecommendation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [savedJobs, setSavedJobs] = useState<Set<string>>(new Set());
  const [sortBy, setSortBy] = useState('updated');
  const [salaryRange, setSalaryRange] = useState([1200, 20000]);
  
  // Filter states
  const [filters, setFilters] = useState({
    workingSchedule: ['full-time', 'part-time', 'project-work'],
    employmentType: ['full-day', 'flexible-schedule', 'distant-work'],
    searchQuery: '',
    location: '',
    experience: '',
  });

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.getJobRecommendations();
      setRecommendations(response || []);
    } catch (error) {
      console.error('Failed to fetch recommendations:', error);
      setRecommendations(getMockRecommendations());
    } finally {
      setIsLoading(false);
    }
  };

  const toggleSaveJob = (jobId: string) => {
    setSavedJobs(prev => {
      const newSet = new Set(prev);
      if (newSet.has(jobId)) {
        newSet.delete(jobId);
      } else {
        newSet.add(jobId);
      }
      return newSet;
    });
  };

  const toggleFilter = (category: string, value: string) => {
    setFilters(prev => {
      const current = prev[category as keyof typeof prev] as string[];
      if (current.includes(value)) {
        return { ...prev, [category]: current.filter(v => v !== value) };
      } else {
        return { ...prev, [category]: [...current, value] };
      }
    });
  };

  const cardColors = [
    { bg: 'bg-gradient-to-br from-[#04366b] to-[#075299]', company: 'bg-[#5a9ab3]' }, // Amazon
    { bg: 'bg-gradient-to-br from-[#04366b] to-[#075299]', company: 'bg-[#5a9ab3]' }, // Google
    { bg: 'bg-gradient-to-br from-[#04366b] to-[#075299]', company: 'bg-[#5a9ab3]' }, // Dribbble
    { bg: 'bg-gradient-to-br from-[#04366b] to-[#075299]', company: 'bg-[#5a9ab3]' }, // Twitter
    { bg: 'bg-gradient-to-br from-[#04366b] to-[#075299]', company: 'bg-[#5a9ab3]' }, // Airbnb
    { bg: 'bg-gradient-to-br from-[#04366b] to-[#075299]', company: 'bg-[#5a9ab3]' }, // Apple
  ];

  const filteredRecommendations = recommendations;

  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      
      <div className="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-6">
          {/* Top Search Bar */}
          <div className="bg-gray-900 text-white rounded-2xl p-6 shadow-xl">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              {/* Search Input */}
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type="text"
                  placeholder="Designer"
                  className="w-full pl-10 pr-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:border-primary"
                  value={filters.searchQuery}
                  onChange={(e) => setFilters(prev => ({ ...prev, searchQuery: e.target.value }))}
                />
              </div>

              {/* Location */}
              <div className="relative">
                <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <select
                  className="w-full pl-10 pr-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white appearance-none focus:outline-none focus:border-primary cursor-pointer"
                  value={filters.location}
                  onChange={(e) => setFilters(prev => ({ ...prev, location: e.target.value }))}
                >
                  <option value="">Work location</option>
                  <option value="remote">Remote</option>
                  <option value="san-francisco">San Francisco, CA</option>
                  <option value="new-york">New York, NY</option>
                  <option value="austin">Austin, TX</option>
                </select>
                <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none" size={20} />
              </div>

              {/* Experience */}
              <div className="relative">
                <Briefcase className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <select
                  className="w-full pl-10 pr-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white appearance-none focus:outline-none focus:border-primary cursor-pointer"
                  value={filters.experience}
                  onChange={(e) => setFilters(prev => ({ ...prev, experience: e.target.value }))}
                >
                  <option value="">Experience</option>
                  <option value="entry">Entry Level</option>
                  <option value="mid">Mid Level</option>
                  <option value="senior">Senior Level</option>
                </select>
                <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none" size={20} />
              </div>

              {/* Per Month/Hour */}
              <div className="relative">
                <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <select
                  className="w-full pl-10 pr-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white appearance-none focus:outline-none focus:border-primary cursor-pointer"
                >
                  <option value="month">Per month</option>
                  <option value="hour">Per hour</option>
                  <option value="year">Per year</option>
                </select>
                <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none" size={20} />
              </div>
            </div>

            {/* Salary Range Slider */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm font-medium text-gray-300">Salary range</span>
                <span className="text-sm font-bold text-white">${salaryRange[0].toLocaleString()} - ${salaryRange[1].toLocaleString()}</span>
              </div>
              <div className="relative">
                <input
                  type="range"
                  min="0"
                  max="30000"
                  step="100"
                  value={salaryRange[1]}
                  onChange={(e) => setSalaryRange([salaryRange[0], parseInt(e.target.value)])}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider-thumb"
                />
                <style jsx>{`
                  .slider-thumb::-webkit-slider-thumb {
                    appearance: none;
                    width: 20px;
                    height: 20px;
                    border-radius: 50%;
                    background: #5a9ab3;
                    cursor: pointer;
                    border: 3px solid white;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                  }
                  .slider-thumb::-moz-range-thumb {
                    width: 20px;
                    height: 20px;
                    border-radius: 50%;
                    background: #5a9ab3;
                    cursor: pointer;
                    border: 3px solid white;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                  }
                `}</style>
              </div>
            </div>
          </div>

          <div className="flex gap-6">
            {/* Sidebar Filters */}
            <aside className="w-64 flex-shrink-0">
              <Card className="p-6 sticky top-24">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-bold text-gray-900" style={{ fontFamily: 'Playfair Display, serif' }}>Filters</h3>
                  <ChevronDown size={20} className="text-gray-600" />
                </div>

                {/* Working Schedule */}
                <div className="mb-6">
                  <h4 className="text-sm font-semibold text-gray-700 mb-3">Working schedule</h4>
                  <div className="space-y-2">
                    {[
                      { value: 'full-time', label: 'Full time' },
                      { value: 'part-time', label: 'Part time' },
                      { value: 'internship', label: 'Internship' },
                      { value: 'project-work', label: 'Project work' },
                      { value: 'volunteering', label: 'Volunteering' },
                    ].map(option => (
                      <label key={option.value} className="flex items-center cursor-pointer group">
                        <input
                          type="checkbox"
                          checked={filters.workingSchedule.includes(option.value)}
                          onChange={() => toggleFilter('workingSchedule', option.value)}
                          className="w-5 h-5 rounded border-gray-300 cursor-pointer checked:bg-[#075299] checked:border-[#075299] hover:border-[#5a9ab3] focus:ring-[#075299] transition-colors"
                        />
                        <span className="ml-3 text-sm text-gray-700 group-hover:text-[#075299] transition-colors">{option.label}</span>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Employment Type */}
                <div>
                  <h4 className="text-sm font-semibold text-gray-700 mb-3">Employment type</h4>
                  <div className="space-y-2">
                    {[
                      { value: 'full-day', label: 'Full day' },
                      { value: 'flexible-schedule', label: 'Flexible schedule' },
                      { value: 'shift-work', label: 'Shift work' },
                      { value: 'distant-work', label: 'Distant work' },
                      { value: 'shift-method', label: 'Shift method' },
                    ].map(option => (
                      <label key={option.value} className="flex items-center cursor-pointer group">
                        <input
                          type="checkbox"
                          checked={filters.employmentType.includes(option.value)}
                          onChange={() => toggleFilter('employmentType', option.value)}
                          className="w-5 h-5 rounded border-gray-300 cursor-pointer checked:bg-[#075299] checked:border-[#075299] hover:border-[#5a9ab3] focus:ring-[#075299] transition-colors"
                        />
                        <span className="ml-3 text-sm text-gray-700 group-hover:text-[#075299] transition-colors">{option.label}</span>
                      </label>
                    ))}
                  </div>
                </div>
              </Card>
            </aside>

            {/* Main Content */}
            <div className="flex-1">
              {/* Header */}
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-3xl font-bold text-white" style={{ fontFamily: 'Playfair Display, serif' }}>
                  Recommended jobs <span className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 text-primary text-xl font-bold ml-3">{filteredRecommendations.length}</span>
                </h2>
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-gray-600">Sort by:</span>
                  <select
                    className="px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-primary cursor-pointer"
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value)}
                  >
                    <option value="updated">Last updated</option>
                    <option value="match">Best match</option>
                    <option value="salary">Highest salary</option>
                    <option value="date">Most recent</option>
                  </select>
                  <Settings size={20} className="text-gray-600 cursor-pointer hover:text-primary transition-colors" />
                </div>
              </div>

              {/* Job Cards Grid */}
              {isLoading ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {[1, 2, 3, 4, 5, 6].map((i) => (
                    <div key={i} className="animate-pulse">
                      <div className="bg-gray-200 rounded-2xl h-80"></div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {filteredRecommendations.map((recommendation, index) => {
                    const isSaved = savedJobs.has(recommendation.job.id);
                    const color = cardColors[index % cardColors.length];
                    const companyInitial = recommendation.job.company_name?.[0] || 'C';
                    
                      return (
                        <div
                          key={recommendation.job.id}
                          className={`${color.bg} rounded-2xl p-6 relative group transition-all duration-300 hover:scale-105 cursor-pointer flex flex-col text-center`}
                          style={{
                            animation: `fadeInUp 0.5s ease-out ${index * 0.1}s both`,
                            minHeight: '420px',
                            boxShadow: '0 10px 30px rgba(0,0,0,0.3), 0 1px 8px rgba(0,0,0,0.2)',
                          }}
                          onMouseEnter={(e) => {
                            e.currentTarget.style.boxShadow = '0 20px 50px rgba(0,0,0,0.4), 0 5px 15px rgba(0,0,0,0.3)';
                          }}
                          onMouseLeave={(e) => {
                            e.currentTarget.style.boxShadow = '0 10px 30px rgba(0,0,0,0.3), 0 1px 8px rgba(0,0,0,0.2)';
                          }}
                        >
                          <style jsx>{`
                          @keyframes fadeInUp {
                            from {
                              opacity: 0;
                              transform: translateY(20px);
                            }
                            to {
                              opacity: 1;
                              transform: translateY(0);
                            }
                          }
                        `}</style>

                        {/* Bookmark */}
                        <button
                          onClick={() => toggleSaveJob(recommendation.job.id)}
                          className="absolute top-4 right-4 p-2 bg-white rounded-lg shadow-md hover:shadow-lg transition-all duration-200 z-10"
                        >
                          {isSaved ? (
                            <BookmarkCheck size={20} className="text-primary" />
                          ) : (
                            <Bookmark size={20} className="text-gray-600" />
                          )}
                        </button>

                        {/* Date */}
                        <div className="flex items-center text-sm text-white/90 mb-6">
                          <Calendar size={16} className="mr-2" />
                          {formatDate(recommendation.job.posted_date)}
                        </div>

                        {/* Company & Title */}
                        <div className="mb-4 mt-2" style={{ minHeight: '80px' }}>
                          <p className="text-lg font-medium text-white/90 mb-2">{recommendation.job.company_name}</p>
                          <h3 className="text-lg font-bold text-white mb-3" style={{ fontFamily: 'Playfair Display, serif' }}>
                            {recommendation.job.title}
                          </h3>
                        </div>

                        {/* Company Logo */}
                        <div className="flex justify-center mb-4">
                          <div 
                            className={`w-14 h-14 rounded-full ${color.company} flex items-center justify-center transition-transform duration-300 hover:scale-110 hover:-translate-y-2 cursor-pointer overflow-hidden`}
                            style={{
                              boxShadow: '0 8px 16px rgba(0,0,0,0.3), inset -2px -2px 8px rgba(0,0,0,0.3), inset 2px 2px 8px rgba(255,255,255,0.2)',
                              background: 'radial-gradient(circle at 30% 30%, rgba(255,255,255,0.3), transparent 50%), linear-gradient(135deg, #5a9ab3 0%, #3d7a92 100%)'
                            }}
                          >
                            <Image 
                              src={`/logos/${recommendation.job.company_name.toLowerCase().replace(/\s+/g, '-')}.png`}
                              alt={recommendation.job.company_name}
                              width={32}
                              height={32}
                              className="object-contain"
                              onError={(e) => {
                                // Fallback to initial if image not found
                                (e.target as HTMLImageElement).style.display = 'none';
                                const parent = (e.target as HTMLImageElement).parentElement;
                                if (parent) {
                                  parent.innerHTML = `<span class="text-white text-xl font-bold">${companyInitial}</span>`;
                                }
                              }}
                            />
                          </div>
                        </div>

                        {/* Tags */}
                        <div className="flex gap-2 justify-center mb-6" style={{ minHeight: '32px' }}>
                          <span className="px-3 py-1 bg-white/70 backdrop-blur-sm rounded-full text-xs font-medium text-gray-700 hover:bg-white hover:shadow-md transition-all duration-200 cursor-pointer flex items-center justify-center">
                            {recommendation.job.job_type}
                          </span>
                          <span className="px-3 py-1 bg-white/70 backdrop-blur-sm rounded-full text-xs font-medium text-gray-700 hover:bg-white hover:shadow-md transition-all duration-200 cursor-pointer flex items-center justify-center">
                            {recommendation.job.experience_level}
                          </span>
                          <span className="px-3 py-1 bg-white/70 backdrop-blur-sm rounded-full text-xs font-medium text-gray-700 hover:bg-white hover:shadow-md transition-all duration-200 cursor-pointer flex items-center justify-center">
                            Remote
                          </span>
                        </div>

                        {/* Salary & Button */}
                        <div className="flex items-end justify-between mt-auto">
                          <div>
                            <p className="text-xl font-bold text-white">
                              ${Math.round((recommendation.job.salary_max || 0) / 2000)}/hr
                            </p>
                            <p className="text-sm text-white/90">{recommendation.job.location}</p>
                          </div>
                          <Link href={`/jobs/${recommendation.job.id}`}>
                            <button className="px-6 py-2 bg-gray-900 text-white rounded-xl font-semibold hover:bg-gray-800 hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-2xl">
                              Details
                            </button>
                          </Link>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
      
      <Footer />
    </div>
  );
}

function getMockRecommendations(): JobRecommendation[] {
  return [
    {
      job: {
        id: '1',
        title: 'Senior UI/UX Designer',
        description: 'Design beautiful and intuitive user experiences',
        company_id: 'company-1',
        company_name: 'Amazon',
        location: 'San Francisco, CA',
        job_type: 'Part-Time',
        experience_level: 'Senior-Level',
        salary_min: 200000,
        salary_max: 250000,
        skills: ['UI Design', 'UX Research', 'Figma', 'Adobe XD'],
        requirements: ['5+ years experience'],
        status: 'active',
        posted_date: '2025-05-20',
      },
      match_score: 0.92,
      reasons: ['Perfect UI/UX match', 'Senior level experience'],
    },
    {
      job: {
        id: '2',
        title: 'Junior UI/UX Designer',
        description: 'Join our design team',
        company_id: 'company-2',
        company_name: 'Google',
        location: 'California, CA',
        job_type: 'Full-Time',
        experience_level: 'Junior-Level',
        salary_min: 120000,
        salary_max: 150000,
        skills: ['Figma', 'Sketch'],
        requirements: ['2+ years experience'],
        status: 'active',
        posted_date: '2025-02-04',
      },
      match_score: 0.85,
      reasons: ['Great for growth', 'Google culture'],
    },
    {
      job: {
        id: '3',
        title: 'Senior Motion Designer',
        description: 'Create stunning animations',
        company_id: 'company-3',
        company_name: 'Dribbble',
        location: 'New York, NY',
        job_type: 'Part-Time',
        experience_level: 'Senior-Level',
        salary_min: 220000,
        salary_max: 260000,
        skills: ['After Effects', 'Motion Graphics'],
        requirements: ['5+ years'],
        status: 'active',
        posted_date: '2025-01-29',
      },
      match_score: 0.88,
      reasons: ['Motion expertise', 'Creative freedom'],
    },
    {
      job: {
        id: '4',
        title: 'UX Designer',
        description: 'Shape user experiences',
        company_id: 'company-4',
        company_name: 'X',
        location: 'California, CA',
        job_type: 'Full-Time',
        experience_level: 'Middle-Level',
        salary_min: 100000,
        salary_max: 120000,
        skills: ['UX', 'Research'],
        requirements: ['3+ years'],
        status: 'active',
        posted_date: '2025-04-11',
      },
      match_score: 0.78,
      reasons: ['UX focus', 'Growing team'],
    },
    {
      job: {
        id: '5',
        title: 'Graphic Designer',
        description: 'Create visual content',
        company_id: 'company-5',
        company_name: 'Airbnb',
        location: 'New York, NY',
        job_type: 'Part-Time',
        experience_level: 'Senior-Level',
        salary_min: 250000,
        salary_max: 300000,
        skills: ['Photoshop', 'Illustrator'],
        requirements: ['5+ years'],
        status: 'active',
        posted_date: '2025-04-02',
      },
      match_score: 0.82,
      reasons: ['Design skills', 'Brand work'],
    },
    {
      job: {
        id: '6',
        title: 'Graphic Designer',
        description: 'Visual design excellence',
        company_id: 'company-6',
        company_name: 'Apple',
        location: 'San Francisco, CA',
        job_type: 'Part-Time',
        experience_level: 'Senior-Level',
        salary_min: 120000,
        salary_max: 140000,
        skills: ['Design', 'Branding'],
        requirements: ['4+ years'],
        status: 'active',
        posted_date: '2025-01-18',
      },
      match_score: 0.75,
      reasons: ['Apple design', 'Premium brand'],
    },
  ];
}
