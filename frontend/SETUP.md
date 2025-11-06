# TalentNest Frontend - Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Environment Configuration

Create `.env.local` file in the root directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

### 4. Build for Production

```bash
npm run build
npm run start
```

## Project Overview

TalentNest is a modern job portal with the following features:

### Completed Features

#### Authentication & Authorization
-  User registration (Job Seeker / Employer roles)
-  Login with JWT authentication
-  Protected routes with role-based access
-  Persistent auth state with Zustand

#### Job Seeker Features
-  Job search with advanced filters
-  Job detail page with apply functionality
-  Profile management
-  Resume upload
-  Application tracking
-  AI job recommendations
-  AI career assistant chatbot
-  Interview scheduling view

#### Employer Features
- Employer dashboard
- Job posting creation
- Job management (view, edit, delete)
- Application review
- Candidate filtering
- Interview scheduling

#### UI/UX
-  Responsive design (mobile, tablet, desktop)
-  Modern, clean interface
-  TalentNest branding (#075299 blue & white)
-  Smooth animations and transitions
-  Loading states
-  Error handling

## Technology Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State Management:** Zustand
- **Form Handling:** React Hook Form
- **HTTP Client:** Axios
- **Icons:** Lucide React

## File Structure

```
frontend/
├── app/                          # Next.js pages
│   ├── dashboard/               # Job seeker dashboard
│   │   ├── applications/
│   │   ├── assistant/
│   │   ├── interviews/
│   │   ├── profile/
│   │   └── recommendations/
│   ├── employer/                # Employer dashboard
│   │   ├── dashboard/
│   │   ├── interviews/
│   │   └── jobs/
│   ├── jobs/                    # Job listings
│   ├── login/
│   ├── register/
│   └── page.tsx                 # Home page
├── components/
│   ├── layout/                  # Navbar, Footer, DashboardLayout
│   └── ui/                      # Reusable components
├── features/                    # Feature-specific components
│   ├── auth/
│   └── jobs/
├── hooks/                       # Custom hooks
├── lib/                         # Utilities & API client
├── store/                       # Zustand stores
├── types/                       # TypeScript definitions
└── constants/                   # App constants
```

## Key Pages

### Public Pages
- **/** - Landing page with hero section
- **/jobs** - Job listings with filters
- **/jobs/[id]** - Job detail page
- **/login** - Login page
- **/register** - Registration page

### Job Seeker Pages (Protected)
- **/dashboard** - Job seeker dashboard
- **/dashboard/profile** - Profile management
- **/dashboard/applications** - Application tracking
- **/dashboard/recommendations** - AI job recommendations
- **/dashboard/assistant** - AI career assistant
- **/dashboard/interviews** - Interview scheduling

### Employer Pages (Protected)
- **/employer/dashboard** - Employer dashboard
- **/employer/jobs** - Job management
- **/employer/jobs/new** - Create job posting
- **/employer/jobs/[id]/applications** - Review applications
- **/employer/interviews** - Schedule interviews

## API Integration

All API calls are managed through `lib/api.ts`:

```typescript
import apiClient from '@/lib/api';

// Example usage
const jobs = await apiClient.getJobs({ query: 'developer' });
const user = await apiClient.getCurrentUser();
```

API methods include:
- Authentication (login, register)
- Jobs (CRUD operations)
- Applications (apply, track)
- Profile management
- Recommendations
- AI assistant

## State Management

Auth state is managed with Zustand:

```typescript
import { useAuthStore } from '@/store/authStore';

const { user, isAuthenticated, setAuth, logout } = useAuthStore();
```

## Custom Hooks

```typescript
// Require authentication
useAuth(true);

// Require specific role
useRequireRole(['employer']);

// Debounce values
const debouncedValue = useDebounce(value, 500);
```

## Styling

TalentNest uses a custom color palette:

```css
--primary: #075299 (TalentNest Blue)
--primary-light: #3387CF
--primary-dark: #04315B
```

Access via Tailwind classes:
- `bg-primary`
- `text-primary`
- `border-primary`

## Mock Data

For development without backend, mock data is included in page components:
- `getMockJobs()` - Sample job listings
- `getMockApplications()` - Sample applications
- `getMockRecommendations()` - Sample AI recommendations

## Deployment

### Production Build

```bash
npm run build
```

### Deploy to Vercel

```bash
vercel deploy
```

### Environment Variables for Production

```env
NEXT_PUBLIC_API_URL=https://your-backend-api.com
```

## Development Tips

1. **Hot Reload:** Changes auto-reload in development
2. **TypeScript:** Full type safety throughout
3. **Error Handling:** Check browser console for errors
4. **API Errors:** Mock data loads if API fails
5. **Auth:** Use mock credentials or register new user

## Troubleshooting

### Build Errors

```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Port Already in Use

```bash
# Use different port
PORT=3001 npm run dev
```

## Next Steps

1. Connect to backend API
2. Add real authentication
3. Implement file uploads for resumes
4. Add payment integration (if needed)
5. Add analytics tracking
6. Implement real-time notifications

## Support

For issues or questions:
- Check the main README.md
- Review the implementation plan
- Contact the development team

---

**Built with ❤️ by the TalentNest Team**

