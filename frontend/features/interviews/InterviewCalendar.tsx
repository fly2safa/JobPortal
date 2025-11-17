import React, { useState, useMemo } from 'react';
import { Interview } from '@/types';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { ChevronLeft, ChevronRight, Calendar as CalendarIcon } from 'lucide-react';

interface InterviewCalendarProps {
  interviews: Interview[];
  onDateSelect?: (date: Date) => void;
  onInterviewClick?: (interview: Interview) => void;
}

export const InterviewCalendar: React.FC<InterviewCalendarProps> = ({
  interviews,
  onDateSelect,
  onInterviewClick,
}) => {
  const [currentDate, setCurrentDate] = useState(new Date());

  // Get calendar data
  const calendarData = useMemo(() => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    
    // First day of the month
    const firstDay = new Date(year, month, 1);
    const startingDayOfWeek = firstDay.getDay();
    
    // Last day of the month
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    
    // Days from previous month
    const prevMonthLastDay = new Date(year, month, 0).getDate();
    const prevMonthDays = Array.from(
      { length: startingDayOfWeek },
      (_, i) => prevMonthLastDay - startingDayOfWeek + i + 1
    );
    
    // Days in current month
    const currentMonthDays = Array.from({ length: daysInMonth }, (_, i) => i + 1);
    
    // Days from next month to fill the grid
    const totalDays = prevMonthDays.length + currentMonthDays.length;
    const nextMonthDays = Array.from(
      { length: (7 - (totalDays % 7)) % 7 },
      (_, i) => i + 1
    );
    
    return {
      prevMonthDays,
      currentMonthDays,
      nextMonthDays,
      year,
      month,
    };
  }, [currentDate]);

  // Group interviews by date
  const interviewsByDate = useMemo(() => {
    const grouped: Record<string, Interview[]> = {};
    
    interviews.forEach((interview) => {
      const date = new Date(interview.scheduled_time);
      const dateKey = `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`;
      
      if (!grouped[dateKey]) {
        grouped[dateKey] = [];
      }
      grouped[dateKey].push(interview);
    });
    
    return grouped;
  }, [interviews]);

  const getInterviewsForDate = (day: number, isCurrentMonth: boolean) => {
    if (!isCurrentMonth) return [];
    
    const dateKey = `${calendarData.year}-${calendarData.month}-${day}`;
    return interviewsByDate[dateKey] || [];
  };

  const handlePrevMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1));
  };

  const handleNextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1));
  };

  const handleToday = () => {
    setCurrentDate(new Date());
  };

  const isToday = (day: number) => {
    const today = new Date();
    return (
      day === today.getDate() &&
      calendarData.month === today.getMonth() &&
      calendarData.year === today.getFullYear()
    );
  };

  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  return (
    <Card className="p-6">
      {/* Calendar Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-900">
          {monthNames[calendarData.month]} {calendarData.year}
        </h2>
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm" onClick={handleToday}>
            <CalendarIcon size={16} className="mr-1" />
            Today
          </Button>
          <Button variant="outline" size="sm" onClick={handlePrevMonth}>
            <ChevronLeft size={16} />
          </Button>
          <Button variant="outline" size="sm" onClick={handleNextMonth}>
            <ChevronRight size={16} />
          </Button>
        </div>
      </div>

      {/* Day Names */}
      <div className="grid grid-cols-7 gap-2 mb-2">
        {dayNames.map((day) => (
          <div
            key={day}
            className="text-center text-sm font-semibold text-gray-600 py-2"
          >
            {day}
          </div>
        ))}
      </div>

      {/* Calendar Grid */}
      <div className="grid grid-cols-7 gap-2">
        {/* Previous month days */}
        {calendarData.prevMonthDays.map((day, index) => (
          <div
            key={`prev-${index}`}
            className="aspect-square p-2 text-center text-gray-400 bg-gray-50 rounded-lg"
          >
            <div className="text-sm">{day}</div>
          </div>
        ))}

        {/* Current month days */}
        {calendarData.currentMonthDays.map((day) => {
          const dayInterviews = getInterviewsForDate(day, true);
          const hasInterviews = dayInterviews.length > 0;
          const isTodayDate = isToday(day);

          return (
            <div
              key={day}
              className={`aspect-square p-2 rounded-lg cursor-pointer transition-colors ${
                isTodayDate
                  ? 'bg-primary text-white font-bold'
                  : hasInterviews
                  ? 'bg-blue-50 hover:bg-blue-100'
                  : 'bg-white hover:bg-gray-50'
              } border ${isTodayDate ? 'border-primary' : 'border-gray-200'}`}
              onClick={() => {
                const date = new Date(calendarData.year, calendarData.month, day);
                onDateSelect?.(date);
              }}
            >
              <div className={`text-sm mb-1 ${isTodayDate ? 'text-white' : 'text-gray-900'}`}>
                {day}
              </div>
              {hasInterviews && (
                <div className="space-y-1">
                  {dayInterviews.slice(0, 2).map((interview, idx) => (
                    <div
                      key={interview.id}
                      className={`text-xs px-1 py-0.5 rounded truncate ${
                        isTodayDate
                          ? 'bg-white text-primary'
                          : interview.status === 'scheduled'
                          ? 'bg-green-100 text-green-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                      onClick={(e) => {
                        e.stopPropagation();
                        onInterviewClick?.(interview);
                      }}
                      title={interview.candidate_name || interview.job_title}
                    >
                      {new Date(interview.scheduled_time).toLocaleTimeString('en-US', {
                        hour: 'numeric',
                        minute: '2-digit',
                        hour12: true,
                      })}
                    </div>
                  ))}
                  {dayInterviews.length > 2 && (
                    <div className={`text-xs px-1 ${isTodayDate ? 'text-white' : 'text-gray-600'}`}>
                      +{dayInterviews.length - 2} more
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}

        {/* Next month days */}
        {calendarData.nextMonthDays.map((day, index) => (
          <div
            key={`next-${index}`}
            className="aspect-square p-2 text-center text-gray-400 bg-gray-50 rounded-lg"
          >
            <div className="text-sm">{day}</div>
          </div>
        ))}
      </div>

      {/* Legend */}
      <div className="flex items-center justify-center space-x-4 mt-6 pt-4 border-t">
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-primary rounded"></div>
          <span className="text-sm text-gray-600">Today</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-blue-50 border border-blue-200 rounded"></div>
          <span className="text-sm text-gray-600">Has Interviews</span>
        </div>
      </div>
    </Card>
  );
};

