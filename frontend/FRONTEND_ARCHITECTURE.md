# TalentNest Frontend Architecture

## 🏗️ Visual System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           TALENTNEST FRONTEND                                │
│                     Next.js 14 (App Router) + TypeScript                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
            ┌───────▼────────┐                 ┌───────▼────────┐
            │  PUBLIC PAGES  │                 │ PROTECTED PAGES │
            └───────┬────────┘                 └───────┬─────────┘
                    │                                   │
        ┌───────────┼───────────┐          ┌───────────┼────────────┐
        │           │           │          │           │            │
    ┌───▼───┐   ┌──▼──┐    ┌──▼──┐   ┌───▼────┐  ┌──▼────┐   ┌───▼────┐
    │ Home  │   │Login│    │Jobs │   │Job     │  │Employer│   │Profile │
    │ Page  │   │/Reg │    │List │   │Seeker  │  │Dashboard│  │ Mgmt  │
    └───────┘   └─────┘    └─────┘   │Dashboard│ └────────┘   └────────┘
                                      └─────────┘
```

---

## 📁 Project Structure

```
frontend/
│
├── 📱 app/                          # Next.js App Router Pages
│   ├── page.tsx                     # Landing Page (Home)
│   ├── login/                       # Authentication
│   ├── register/                    # User Registration
│   ├── jobs/                        # Job Listings & Details
│   │   ├── page.tsx                 # Job Search Page
│   │   └── [id]/page.tsx           # Job Detail + Apply
│   │
│   ├── dashboard/                   # Job Seeker Dashboard
│   │   ├── page.tsx                 # Main Dashboard
│   │   ├── applications/            # Application Tracking
│   │   ├── recommendations/         # AI Job Recommendations
│   │   ├── profile/                 # Profile Management
│   │   ├── assistant/               # AI Career Assistant
│   │   └── interviews/              # Interview Scheduling
│   │
│   └── employer/                    # Employer Portal
│       ├── dashboard/               # Employer Dashboard
│       ├── jobs/                    # Job Management
│       │   ├── page.tsx            # Job List
│       │   ├── new/                # Create Job
│       │   └── [id]/
│       │       ├── edit/           # Edit Job
│       │       └── applications/   # Review Applications
│       └── interviews/              # Interview Management
│
├── 🎨 components/                   # Reusable Components
│   ├── layout/                      # Layout Components
│   │   ├── Navbar.tsx              # Navigation Bar
│   │   ├── Footer.tsx              # Footer
│   │   └── DashboardLayout.tsx     # Dashboard Wrapper
│   │
│   └── ui/                          # UI Component Library
│       ├── Button.tsx              # Custom Button
│       ├── Card.tsx                # Card Container
│       ├── Badge.tsx               # Status Badges
│       ├── Modal.tsx               # Modal Dialog
│       ├── Input.tsx               # Form Input
│       ├── Select.tsx              # Dropdown Select
│       └── Textarea.tsx            # Text Area
│
├── ✨ features/                     # Feature-Specific Components
│   ├── auth/                        # Authentication Features
│   │   ├── LoginForm.tsx           # Login Form
│   │   └── RegisterForm.tsx        # Registration Form
│   │
│   ├── jobs/                        # Job Features
│   │   ├── JobCard.tsx             # Job Display Card
│   │   ├── JobFilters.tsx          # Search Filters
│   │   └── ApplyModal.tsx          # Application Modal
│   │
│   ├── employer/                    # Employer Features
│   │   └── candidate-recommendations/
│   │       └── CandidateRecommendations.tsx
│   │
│   └── profile/                     # Profile Features
│       ├── ResumeUpload.tsx        # Resume Upload
│       ├── ResumeList.tsx          # Resume Management
│       └── ParsingResults.tsx      # Resume Parsing Display
│
├── 🔧 lib/                          # Utilities & Helpers
│   ├── api.ts                       # API Client (Axios)
│   └── utils.ts                     # Helper Functions
│
├── 🎯 hooks/                        # Custom React Hooks
│   ├── useAuth.ts                   # Authentication Hook
│   └── useDebounce.ts              # Debounce Hook
│
├── 💾 store/                        # State Management
│   └── authStore.ts                # Zustand Auth Store
│
├── 📝 types/                        # TypeScript Definitions
│   └── index.ts                     # All Type Definitions
│
└── 🎨 constants/                    # App Constants
    └── index.ts                     # Constants & Enums
```

---

## 🔄 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                              │
│                    (React Components + Tailwind CSS)                     │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Custom Hooks   │
                    │  - useAuth      │
                    │  - useDebounce  │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────┐
│  Zustand Store │  │   React Hook    │  │   Local     │
│  (Auth State)  │  │   Form (Forms)  │  │   State     │
└───────┬────────┘  └────────┬────────┘  └──────┬──────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   API Client    │
                    │   (Axios)       │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Backend API    │
                    │  (FastAPI)      │
                    └─────────────────┘
```

---

## 🎨 Design System

### Color Palette
```
Primary Colors:
├── Primary Blue:      #075299  (TalentNest Brand)
├── Primary Light:     #5a9ab3  (Accents & Highlights)
├── Primary Dark:      #04366b  (Depth & Shadows)
└── White:             #FFFFFF  (Backgrounds)

Status Colors:
├── Success Green:     #10B981  (Approved, Active)
├── Warning Yellow:    #F59E0B  (Pending, Review)
├── Danger Red:        #EF4444  (Rejected, Error)
└── Info Blue:         #3B82F6  (Information)

Neutral Colors:
├── Gray 900:          #111827  (Primary Text)
├── Gray 600:          #4B5563  (Secondary Text)
├── Gray 300:          #D1D5DB  (Borders)
└── Gray 50:           #F9FAFB  (Backgrounds)
```

### Typography
```
Font Family:
├── Primary:    'Playfair Display', serif  (Headings, Brand)
├── Accent:     'Dancing Script', cursive  (Logo Accent)
└── Body:       System UI, sans-serif      (Body Text)

Font Sizes:
├── xs:   0.75rem   (12px)
├── sm:   0.875rem  (14px)
├── base: 1rem      (16px)
├── lg:   1.125rem  (18px)
├── xl:   1.25rem   (20px)
├── 2xl:  1.5rem    (24px)
└── 3xl:  1.875rem  (30px)
```

### Spacing System (Tailwind)
```
├── 1:  0.25rem  (4px)
├── 2:  0.5rem   (8px)
├── 3:  0.75rem  (12px)
├── 4:  1rem     (16px)
├── 6:  1.5rem   (24px)
└── 8:  2rem     (32px)
```

---

## 🎭 UI/UX Features

### Visual Effects
```
┌─────────────────────────────────────────────────────────────┐
│ Glassmorphism                                                │
│ ├── backdrop-blur-sm:  Subtle blur effect                   │
│ ├── bg-white/70:       70% opacity backgrounds              │
│ └── Used in: Recommendation cards, overlays                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Hover Interactions                                           │
│ ├── hover:scale-105:    Scale up on hover                   │
│ ├── hover:shadow-lg:    Enhanced shadows                    │
│ ├── hover:bg-gray-50:   Background color change             │
│ └── transition-all:     Smooth transitions                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Animations                                                   │
│ ├── fadeInUp:          Cards fade in from bottom            │
│ ├── spin:              Loading spinners                     │
│ └── Custom keyframes:  Smooth entrance animations           │
└─────────────────────────────────────────────────────────────┘
```

### Responsive Design
```
Breakpoints:
├── sm:  640px   (Mobile Landscape)
├── md:  768px   (Tablet)
├── lg:  1024px  (Desktop)
└── xl:  1280px  (Large Desktop)

Mobile-First Approach:
└── All components designed for mobile first, then enhanced for larger screens
```

---

## 🔐 Authentication Flow

```
┌─────────────┐
│   Landing   │
│    Page     │
└──────┬──────┘
       │
       ├─────────────┐
       │             │
┌──────▼──────┐  ┌──▼────────┐
│   Login     │  │  Register │
└──────┬──────┘  └──┬────────┘
       │            │
       └─────┬──────┘
             │
      ┌──────▼───────┐
      │  Auth Store  │
      │  (Zustand)   │
      └──────┬───────┘
             │
      ┌──────▼───────┐
      │  JWT Token   │
      │  Saved to    │
      │  LocalStorage│
      └──────┬───────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼──────────┐  ┌──▼──────────┐
│  Job Seeker  │  │  Employer   │
│  Dashboard   │  │  Dashboard  │
└──────────────┘  └─────────────┘
```

---

## 🚀 Key Features by User Role

### Job Seeker Journey
```
1. Browse Jobs
   └── Search, Filter, Sort
       └── View Job Details
           └── Apply (Upload Resume + Cover Letter)
               └── Track Application Status
                   └── View AI Recommendations
                       └── Schedule Interviews
```

### Employer Journey
```
1. Post New Job
   └── Manage Job Listings
       └── Review Applications
           └── View AI-Matched Candidates
               └── Update Application Status
                   └── Schedule Interviews
```

---

## 📊 State Management Strategy

```
┌─────────────────────────────────────────────────────────────┐
│ Global State (Zustand)                                       │
│ ├── User Authentication                                      │
│ ├── User Profile Data                                        │
│ └── JWT Token                                                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Local Component State (useState)                             │
│ ├── Form Data                                                │
│ ├── Loading States                                           │
│ ├── Error Messages                                           │
│ └── UI Toggles (modals, dropdowns)                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Server State (React Hook Form + API)                         │
│ ├── Jobs Data                                                │
│ ├── Applications Data                                        │
│ ├── Recommendations Data                                     │
│ └── User Profile Updates                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔌 API Integration

### API Client Structure
```typescript
class ApiClient {
  // Authentication
  ├── login()
  ├── register()
  └── getCurrentUser()
  
  // Jobs
  ├── getJobs()
  ├── getJobById()
  ├── createJob()
  ├── updateJob()
  └── deleteJob()
  
  // Applications
  ├── getApplications()
  ├── applyToJob()
  ├── updateApplicationStatus()
  └── getJobApplications()
  
  // Resume
  ├── uploadResume()
  ├── getResumes()
  └── deleteResume()
  
  // AI Features
  ├── getJobRecommendations()
  ├── getCandidateRecommendations()
  └── generateCoverLetter()
}
```

---

## 🎯 Performance Optimizations

```
✓ Next.js 14 App Router for optimal performance
✓ Server-Side Rendering (SSR) for SEO
✓ Code Splitting by route
✓ Image Optimization with next/image
✓ Lazy Loading for modals and heavy components
✓ Debounced search inputs
✓ Optimized re-renders with React.memo where needed
✓ Efficient state management with Zustand
```

---

## 🛡️ Security Features

```
✓ JWT-based authentication
✓ Protected routes with useAuth hook
✓ Role-based access control (Job Seeker vs Employer)
✓ Secure API calls with Authorization headers
✓ Input validation on all forms
✓ XSS protection through React's built-in escaping
✓ HTTPS-only in production
```

---

## 📱 Responsive Design Strategy

```
Mobile First (< 640px)
├── Single column layouts
├── Stacked navigation
├── Touch-optimized buttons
└── Simplified forms

Tablet (768px - 1024px)
├── Two-column grids
├── Expanded navigation
└── Side-by-side forms

Desktop (> 1024px)
├── Multi-column layouts
├── Full navigation bar
├── Advanced filtering
└── Rich data displays
```

---

## 🎨 Component Hierarchy

```
App
├── Navbar (Global)
│   ├── Logo
│   ├── Navigation Links
│   └── User Menu
│
├── Page Content
│   ├── DashboardLayout (Protected Pages)
│   │   ├── Sidebar
│   │   └── Main Content Area
│   │
│   └── Public Layout (Public Pages)
│       └── Full Width Content
│
└── Footer (Global)
    ├── Links
    ├── Social Media
    └── Copyright
```

---

## 📈 Future Enhancements

```
Planned Features:
├── Real-time notifications (WebSockets)
├── Advanced analytics dashboard
├── Video interview integration
├── Chat/messaging system
├── Calendar integration
├── Multi-language support
└── Dark mode toggle
```

---

## 🔧 Development Tools

```
Core Technologies:
├── Next.js 14          (React Framework)
├── TypeScript          (Type Safety)
├── Tailwind CSS        (Styling)
├── Zustand             (State Management)
├── React Hook Form     (Form Handling)
├── Axios               (HTTP Client)
└── Lucide React        (Icons)

Development Tools:
├── ESLint              (Code Linting)
├── Prettier            (Code Formatting)
├── Git                 (Version Control)
└── VS Code             (IDE)
```

---

**Built by Erica Harrison with precision and care for the TalentNest Job Portal**  
*Frontend Architecture v1.0*

