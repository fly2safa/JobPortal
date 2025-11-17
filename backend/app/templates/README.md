# Email Templates

This directory contains professional email templates for various notifications sent by the JobPortal application.

## Available Templates

### 1. Application Submitted
**Function:** `application_submitted_template(data)`

Sent when a job seeker successfully submits an application.

**Required Data:**
- `applicant_name`: Full name of the applicant
- `job_title`: Title of the job position
- `company_name`: Name of the hiring company

**Features:**
- Confirmation of successful submission
- Application details summary
- Next steps information
- Professional styling with company branding

---

### 2. Application Status Update
**Function:** `application_status_update_template(data)`

Sent when an employer updates the status of an application.

**Required Data:**
- `applicant_name`: Full name of the applicant
- `job_title`: Title of the job position
- `company_name`: Name of the hiring company
- `new_status`: New status (reviewing, shortlisted, interview, rejected, accepted)

**Features:**
- Color-coded status indicators
- Status-specific messaging
- Emoji icons for visual appeal
- Application details summary

**Supported Statuses:**
- `reviewing` 🔍 - Application under review
- `shortlisted` ⭐ - Shortlisted for consideration
- `interview` 📅 - Interview invitation
- `rejected` ❌ - Application not selected
- `accepted` ✅ - Job offer extended

---

### 3. Job Alert
**Function:** `job_alert_template(data)`

Sent when a new job matches a user's profile and preferences.

**Required Data:**
- `user_name`: Full name of the user
- `job_title`: Title of the job position
- `company_name`: Name of the hiring company
- `job_location`: Location of the job
- `job_id`: Unique identifier for the job
- `job_url` (optional): Direct URL to job details

**Features:**
- Eye-catching design to grab attention
- Direct link to job details
- Urgency messaging
- Skills/preferences match indication

---

### 4. Welcome Email
**Function:** `welcome_email_template(data)`

Sent when a new user registers on the platform.

**Required Data:**
- `user_name`: Full name of the new user
- `user_role`: User role (job_seeker or employer)

**Features:**
- Warm welcome message
- Role-specific benefits list
- Call-to-action to dashboard
- Getting started guidance

**Role-Specific Content:**
- **Job Seeker**: Focus on finding jobs, recommendations, resume upload
- **Employer**: Focus on posting jobs, finding candidates, managing applications

---

## Template Structure

All templates use a consistent base structure with:

### Header
- JobPortal branding
- Gradient background (blue theme)
- Tagline: "Connecting Talent with Opportunity"

### Content Area
- Clean, white background
- Responsive design (600px width)
- Professional typography
- Color-coded sections

### Footer
- Company information
- Copyright notice
- Automated message disclaimer

## Styling Guidelines

### Colors
- **Primary Blue**: `#2563eb` - Main brand color
- **Dark Blue**: `#1d4ed8` - Gradient accent
- **Success Green**: `#22c55e` - Positive actions
- **Warning Orange**: `#f59e0b` - Alerts
- **Error Red**: `#ef4444` - Rejections
- **Text Gray**: `#374151` - Body text
- **Light Gray**: `#6b7280` - Secondary text

### Typography
- **Headings**: Arial, Helvetica, sans-serif
- **H1**: 28px, bold, white (header)
- **H2**: 24px, bold, dark gray
- **H3**: 18-20px, bold, dark gray
- **Body**: 16px, regular, gray
- **Small**: 12-14px, regular, light gray

### Layout
- **Max Width**: 600px (optimal for email clients)
- **Padding**: Generous spacing for readability
- **Border Radius**: 4-8px for modern look
- **Box Shadow**: Subtle shadows for depth

## Usage Example

```python
from app.templates.email_templates import application_submitted_template
from app.services.email_service import email_service

# Prepare data
data = {
    "applicant_name": "John Doe",
    "job_title": "Senior Software Engineer",
    "company_name": "TechCorp Inc."
}

# Get template
template = application_submitted_template(data)

# Send email
await email_service.send_email(
    to_email="john.doe@example.com",
    subject=f"Application Submitted: {data['job_title']}",
    html_content=template['html'],
    text_content=template['text']
)
```

## Email Client Compatibility

Templates are designed to work across major email clients:

✅ **Supported:**
- Gmail (Web, iOS, Android)
- Outlook (Desktop, Web, Mobile)
- Apple Mail (macOS, iOS)
- Yahoo Mail
- ProtonMail
- Thunderbird

### Compatibility Features:
- Table-based layout (most compatible)
- Inline CSS styles
- Plain text fallback
- Responsive design
- No external dependencies

## Best Practices

1. **Always provide both HTML and text versions**
   - HTML for modern clients
   - Text for accessibility and fallback

2. **Keep it concise**
   - Clear subject lines
   - Scannable content
   - Single call-to-action

3. **Test before deploying**
   - Preview in multiple clients
   - Check mobile rendering
   - Verify all links work

4. **Personalization**
   - Use recipient's name
   - Include relevant details
   - Make it feel personal, not automated

5. **Accessibility**
   - High contrast text
   - Clear hierarchy
   - Descriptive link text
   - Alt text for images (if added)

## Customization

To customize templates:

1. **Colors**: Update color values in the template functions
2. **Branding**: Modify the base template header
3. **Content**: Edit template functions directly
4. **New Templates**: Follow existing pattern and add to `email_templates.py`

## Future Enhancements

Potential improvements:
- [ ] Interview scheduling email
- [ ] Password reset email
- [ ] Weekly job digest
- [ ] Application reminder
- [ ] Company profile update notification
- [ ] Resume parsing completion
- [ ] AI recommendation summary

## Support

For questions or issues with email templates, contact the development team or refer to the main project documentation.



