# TalentNest Frontend

## Overview

TalentNest is an AI-powered job portal application that connects job seekers with employers. This is the frontend application built with Next.js 14, TypeScript, and Tailwind CSS.

## Features

### For Job Seekers
-  **Job Search** - Browse and search thousands of job listings
-  **AI-Powered Recommendations** - Get personalized job matches based on your profile
-  **Application Tracking** - Track all your job applications in one place
-  **Profile Management** - Build and manage your professional profile
-  **Resume Upload** - Upload and manage multiple resumes
-  **AI Career Assistant** - Get career advice and tips from AI
-  **Interview Management** - Track and manage your interviews

### For Employers
-  **Job Posting** - Create and manage job listings
-  **Application Review** - Review and filter candidate applications
-  **AI Candidate Matching** - Get AI-recommended top candidates
-  **Interview Scheduling** - Schedule and manage interviews
-  **Dashboard Analytics** - Track job performance and applications

## Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State Management:** Zustand
- **Form Handling:** React Hook Form
- **HTTP Client:** Axios
- **Icons:** Lucide React

## Getting Started

### Prerequisites

- Node.js 18+ installed
- npm or yarn package manager

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create `.env.local` file:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── dashboard/         # Job seeker dashboard pages
│   ├── employer/          # Employer dashboard pages
│   ├── jobs/              # Job listing and detail pages
│   ├── login/             # Login page
│   ├── register/          # Registration page
│   └── page.tsx           # Home/landing page
├── components/            # Reusable UI components
│   ├── layout/           # Layout components (Navbar, Footer, etc.)
│   └── ui/               # UI components (Button, Input, Card, etc.)
├── features/             # Feature-specific components
│   ├── auth/            # Authentication components
│   └── jobs/            # Job-related components
├── hooks/               # Custom React hooks
├── lib/                 # Utilities and API client
├── store/               # Zustand state management
├── types/               # TypeScript type definitions
└── constants/           # App constants

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Brand Colors

- **Primary:** #075299 (TalentNest Blue)
- **Primary Light:** #3387CF
- **Primary Dark:** #04315B
- **White:** #FFFFFF

## Key Features Implementation

### Authentication
- JWT-based authentication
- Role-based access (Job Seeker / Employer)
- Protected routes with middleware

### Job Search
- Advanced filtering (location, type, experience level)
- Real-time search with debouncing
- Responsive job cards

### AI Features
- Job recommendations
- Candidate matching
- Cover letter generation
- Career assistant chatbot

### Responsive Design
- Mobile-first approach
- Tablet and desktop optimized
- Smooth animations and transitions

## API Integration

The frontend connects to the FastAPI backend at `NEXT_PUBLIC_API_URL`. All API calls are centralized in `lib/api.ts` with automatic JWT token injection.

## Contributing

1. Create a feature branch from `dev`
2. Make your changes
3. Submit a pull request to `dev`
4. Ensure all tests pass and code is linted

## License

Copyright © 2025 TalentNest. All rights reserved.

