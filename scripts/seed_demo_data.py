r"""
Seed TalentNest with demo data through the public API.

Everything is created the way a browser would create it, so passwords are
hashed by the backend, validation runs, and the ObjectId references between
users, companies, jobs, applications and resumes are all consistent.

Seeded accounts use the SEED_EMAIL_DOMAIN marker so they can be found and
removed with a single query.

Usage:
    cd backend
    $env:PYTHONUTF8='1'
    .\venv\Scripts\Activate.ps1
    python ..\scripts\seed_demo_data.py
"""
import argparse
import io
import random
import sys
import time
from typing import Any, Dict, List, Optional

import requests
from docx import Document

DEFAULT_API_URL = "http://127.0.0.1:8000/api/v1"
DEFAULT_PASSWORD = "SeedTest123!"
# example.com is IANA-reserved for documentation, so seeded addresses can never
# reach a real mailbox. Reserved TLDs such as .test are rejected by email-validator.
SEED_EMAIL_DOMAIN = "seed.example.com"

REQUEST_TIMEOUT = 60
MAX_RETRIES = 6

COMPANIES = [
    {
        "name": "Northwind Analytics",
        "industry": "Data & Analytics",
        "size": "51-200",
        "headquarters": "Seattle, WA",
        "website": "https://northwind-analytics.example.com",
        "description": (
            "Northwind Analytics builds decision-intelligence tooling for mid-market "
            "retailers, turning point-of-sale and supply-chain data into forecasts."
        ),
    },
    {
        "name": "Cobalt Health Systems",
        "industry": "Healthcare Technology",
        "size": "201-500",
        "headquarters": "Boston, MA",
        "website": "https://cobalt-health.example.com",
        "description": (
            "Cobalt Health Systems develops patient-scheduling and care-coordination "
            "software used by regional hospital networks across New England."
        ),
    },
    {
        "name": "Sierra Grid Energy",
        "industry": "Clean Energy",
        "size": "11-50",
        "headquarters": "Denver, CO",
        "website": "https://sierragrid.example.com",
        "description": (
            "Sierra Grid Energy designs monitoring hardware and software for "
            "distributed solar installations and community microgrids."
        ),
    },
    {
        "name": "Harbor Point Financial",
        "industry": "Financial Services",
        "size": "501-1000",
        "headquarters": "Charlotte, NC",
        "website": "https://harborpoint.example.com",
        "description": (
            "Harbor Point Financial provides risk modeling and compliance reporting "
            "platforms for regional banks and credit unions."
        ),
    },
]

JOB_TEMPLATES = [
    {
        "title": "Senior Backend Engineer",
        "experience_level": "senior",
        "job_type": "full_time",
        "salary": (145000, 185000),
        "years": (5, 10),
        "required_skills": ["Python", "FastAPI", "MongoDB", "Docker"],
        "preferred_skills": ["Kubernetes", "AWS", "GraphQL"],
        "description": (
            "Own the design and delivery of the services behind our core product. "
            "You will lead API design, shape our data model, and mentor engineers "
            "as the platform scales past its first million records."
        ),
        "responsibilities": (
            "Design and build REST APIs; own service reliability and on-call rotation; "
            "review code and mentor mid-level engineers; partner with product on scoping."
        ),
        "requirements": (
            "5+ years building production backend services in Python. Strong grasp of "
            "async programming, schema design, and testing. Experience operating "
            "containerized services."
        ),
    },
    {
        "title": "Frontend Engineer, React",
        "experience_level": "mid",
        "job_type": "full_time",
        "salary": (115000, 145000),
        "years": (3, 6),
        "required_skills": ["React", "TypeScript", "CSS", "Next.js"],
        "preferred_skills": ["Tailwind CSS", "Accessibility", "Testing Library"],
        "description": (
            "Build the interfaces our customers use every day. You will work closely "
            "with design to ship accessible, fast, genuinely pleasant product surfaces."
        ),
        "responsibilities": (
            "Implement new product features in React and TypeScript; improve page "
            "performance; maintain the shared component library; contribute to design reviews."
        ),
        "requirements": (
            "3+ years of professional React work with TypeScript. Comfortable with "
            "modern build tooling and component testing."
        ),
    },
    {
        "title": "Data Engineer",
        "experience_level": "mid",
        "job_type": "full_time",
        "salary": (125000, 160000),
        "years": (3, 7),
        "required_skills": ["Python", "SQL", "Airflow", "Spark"],
        "preferred_skills": ["dbt", "Snowflake", "Terraform"],
        "description": (
            "Build and operate the pipelines that move data from source systems into "
            "our analytics layer, and make that data something people actually trust."
        ),
        "responsibilities": (
            "Develop batch and streaming pipelines; define data quality checks; "
            "model warehouse tables; support analysts and data scientists."
        ),
        "requirements": (
            "Strong SQL and Python. Experience with a workflow orchestrator and a "
            "columnar warehouse. Familiarity with data modeling patterns."
        ),
    },
    {
        "title": "DevOps Engineer",
        "experience_level": "senior",
        "job_type": "full_time",
        "salary": (135000, 170000),
        "years": (4, 9),
        "required_skills": ["Kubernetes", "Terraform", "AWS", "CI/CD"],
        "preferred_skills": ["Prometheus", "Go", "Helm"],
        "description": (
            "Make shipping safe and boring. You will own our infrastructure as code, "
            "deployment pipelines, and the observability stack behind them."
        ),
        "responsibilities": (
            "Maintain Kubernetes clusters; build CI/CD pipelines; manage infrastructure "
            "with Terraform; lead incident response and postmortems."
        ),
        "requirements": (
            "4+ years in platform or infrastructure roles. Deep familiarity with a major "
            "cloud provider and container orchestration."
        ),
    },
    {
        "title": "Junior Software Engineer",
        "experience_level": "entry",
        "job_type": "full_time",
        "salary": (75000, 95000),
        "years": (0, 2),
        "required_skills": ["JavaScript", "Git", "SQL"],
        "preferred_skills": ["React", "Python", "REST APIs"],
        "description": (
            "A role built for someone early in their career. You will pair with senior "
            "engineers, ship real features from your first month, and grow quickly."
        ),
        "responsibilities": (
            "Implement well-scoped features; write tests; participate in code review; "
            "fix bugs reported by support."
        ),
        "requirements": (
            "Familiarity with at least one modern language and version control. "
            "Internship, bootcamp, or personal project experience all count."
        ),
    },
    {
        "title": "Product Designer",
        "experience_level": "mid",
        "job_type": "full_time",
        "salary": (105000, 135000),
        "years": (3, 7),
        "required_skills": ["Figma", "User Research", "Prototyping"],
        "preferred_skills": ["Design Systems", "HTML", "Motion Design"],
        "description": (
            "Shape how the product looks and feels end to end, from early research "
            "through high-fidelity design and handoff."
        ),
        "responsibilities": (
            "Run discovery interviews; produce flows and prototypes; maintain the design "
            "system; validate designs with usability testing."
        ),
        "requirements": (
            "A portfolio showing shipped product work. Comfort with research methods "
            "and close collaboration with engineers."
        ),
    },
    {
        "title": "QA Automation Engineer",
        "experience_level": "mid",
        "job_type": "contract",
        "salary": (95000, 125000),
        "years": (2, 6),
        "required_skills": ["Selenium", "Python", "Test Automation"],
        "preferred_skills": ["Playwright", "CI/CD", "Performance Testing"],
        "description": (
            "Own the automated test suites that let us release weekly without holding "
            "our breath."
        ),
        "responsibilities": (
            "Build end-to-end test coverage; maintain suites in CI; triage flaky tests; "
            "report on quality metrics."
        ),
        "requirements": (
            "Experience writing maintainable browser automation. Scripting fluency in "
            "Python or JavaScript."
        ),
    },
    {
        "title": "Machine Learning Engineer",
        "experience_level": "senior",
        "job_type": "full_time",
        "salary": (150000, 195000),
        "years": (4, 10),
        "required_skills": ["Python", "PyTorch", "Machine Learning", "MLOps"],
        "preferred_skills": ["LangChain", "Vector Databases", "AWS SageMaker"],
        "description": (
            "Take models from notebook to production, and keep them healthy once they "
            "are serving real traffic."
        ),
        "responsibilities": (
            "Train and evaluate models; build inference services; monitor drift; "
            "collaborate with data engineering on feature pipelines."
        ),
        "requirements": (
            "Strong applied ML background with production deployment experience. "
            "Comfortable owning a model end to end."
        ),
    },
]

CANDIDATES = [
    ("Amara", "Okafor", "Seattle, WA", 7, "Senior Backend Engineer",
     ["Python", "FastAPI", "MongoDB", "Docker", "AWS"],
     "M.S. Computer Science, University of Washington"),
    ("Diego", "Ramirez", "Austin, TX", 4, "Frontend Engineer",
     ["React", "TypeScript", "Next.js", "Tailwind CSS", "CSS"],
     "B.S. Computer Science, UT Austin"),
    ("Priya", "Venkatesan", "Boston, MA", 6, "Data Engineer",
     ["Python", "SQL", "Airflow", "Spark", "dbt"],
     "M.S. Data Science, Northeastern University"),
    ("Liam", "O'Connell", "Denver, CO", 9, "DevOps Engineer",
     ["Kubernetes", "Terraform", "AWS", "CI/CD", "Go"],
     "B.S. Information Systems, Colorado State University"),
    ("Mei", "Tanaka", "San Jose, CA", 1, "Junior Software Engineer",
     ["JavaScript", "Git", "SQL", "React"],
     "B.S. Software Engineering, San Jose State University"),
    ("Jonah", "Whitfield", "Charlotte, NC", 5, "Product Designer",
     ["Figma", "User Research", "Prototyping", "Design Systems"],
     "B.F.A. Interaction Design, SCAD"),
    ("Fatima", "Al-Rashid", "Chicago, IL", 3, "QA Automation Engineer",
     ["Selenium", "Python", "Test Automation", "Playwright"],
     "B.S. Computer Engineering, University of Illinois"),
    ("Ethan", "Brooks", "Remote", 8, "Machine Learning Engineer",
     ["Python", "PyTorch", "Machine Learning", "MLOps", "LangChain"],
     "Ph.D. Machine Learning, Carnegie Mellon University"),
    ("Sofia", "Marchetti", "New York, NY", 2, "Frontend Engineer",
     ["React", "TypeScript", "CSS", "Accessibility"],
     "B.A. Cognitive Science, NYU"),
    ("Marcus", "Bell", "Atlanta, GA", 6, "Backend Engineer",
     ["Python", "PostgreSQL", "Docker", "REST APIs", "Redis"],
     "B.S. Computer Science, Georgia Tech"),
    ("Hana", "Kim", "Portland, OR", 4, "Data Analyst",
     ["SQL", "Python", "Tableau", "Statistics"],
     "B.S. Statistics, University of Oregon"),
    ("Tobias", "Lindqvist", "Remote", 11, "Principal Engineer",
     ["Python", "Kubernetes", "System Design", "Go", "Terraform"],
     "M.S. Computer Science, KTH Royal Institute of Technology"),
]

COVER_LETTER = (
    "Dear {company} hiring team,\n\n"
    "I am applying for the {title} role. Over the past {years} years I have worked "
    "primarily with {skills}, most recently as a {job_title}. The scope of this role "
    "lines up closely with what I have been doing, and {company}'s work is the kind "
    "of problem I would like to spend my time on.\n\n"
    "I would welcome the chance to talk further.\n\n"
    "Best regards,\n{name}"
)


class SeedError(Exception):
    """Raised when the API rejects a request in a way we cannot recover from."""


class ApiClient:
    """Thin API wrapper that retries on rate limiting."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def request(
        self,
        method: str,
        path: str,
        token: Optional[str] = None,
        expected: int = 200,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        headers = kwargs.pop("headers", {})
        if token:
            headers["Authorization"] = f"Bearer {token}"

        for attempt in range(MAX_RETRIES):
            response = self.session.request(
                method, url, headers=headers, timeout=REQUEST_TIMEOUT, **kwargs
            )
            if response.status_code == 429:
                wait = int(response.headers.get("Retry-After", 12))
                print(f"    rate limited, waiting {wait}s "
                      f"(attempt {attempt + 1}/{MAX_RETRIES})")
                time.sleep(wait)
                continue
            if response.status_code != expected:
                raise SeedError(
                    f"{method} {path} returned {response.status_code}: {response.text[:300]}"
                )
            return response.json() if response.content else {}

        raise SeedError(f"{method} {path} still rate limited after {MAX_RETRIES} attempts")


def build_resume_docx(first: str, last: str, job_title: str, years: int,
                      skills: List[str], education: str, location: str) -> bytes:
    """Create a plain-text-friendly DOCX resume the backend parser can read."""
    document = Document()
    document.add_heading(f"{first} {last}", level=1)
    document.add_paragraph(
        f"{job_title} | {location} | "
        f"{first.lower()}.{last.lower().replace(chr(39), '')}@{SEED_EMAIL_DOMAIN}"
    )

    document.add_heading("Summary", level=2)
    document.add_paragraph(
        f"{job_title} with {years} years of professional experience. Focused on "
        f"{', '.join(skills[:3])}, with a track record of shipping production systems "
        f"and working closely with product and design partners."
    )

    document.add_heading("Skills", level=2)
    document.add_paragraph(", ".join(skills))

    document.add_heading("Experience", level=2)
    document.add_paragraph(
        f"{job_title}, Contoso Software ({max(years - 3, 1)} years)\n"
        f"Built and maintained services using {', '.join(skills[:3])}. Partnered with "
        f"cross-functional teams to deliver quarterly roadmap commitments."
    )
    document.add_paragraph(
        f"Software Engineer, Fabrikam Labs ({min(3, max(years - 1, 1))} years)\n"
        f"Contributed to core product development and improved automated test coverage."
    )

    document.add_heading("Education", level=2)
    document.add_paragraph(education)

    buffer = io.BytesIO()
    document.save(buffer)
    return buffer.getvalue()


def seed(api: ApiClient, password: str, employer_count: int, seeker_count: int,
         jobs_per_employer: int, applications_per_seeker: int,
         include_resumes: bool) -> Dict[str, int]:
    random.seed(42)
    counts = {"employers": 0, "companies": 0, "jobs": 0,
              "seekers": 0, "resumes": 0, "applications": 0}

    print("\n[1/4] Creating employers and companies")
    employers = []
    for company in COMPANIES[:employer_count]:
        slug = company["name"].split()[0].lower()
        payload = {
            "email": f"hiring@{slug}.{SEED_EMAIL_DOMAIN}",
            "password": password,
            "first_name": "Hiring",
            "last_name": company["name"].split()[0],
            "role": "employer",
            "location": company["headquarters"],
            "company_name": company["name"],
            "company_description": company["description"],
            "company_industry": company["industry"],
            "company_size": company["size"],
            "company_website": company["website"],
            "company_headquarters": company["headquarters"],
        }
        result = api.request("POST", "/auth/register", json=payload, expected=201)
        employers.append({
            "token": result["access_token"],
            "company_id": result["user"]["company_id"],
            "company_name": company["name"],
            "location": company["headquarters"],
            "email": payload["email"],
        })
        counts["employers"] += 1
        counts["companies"] += 1
        print(f"    {company['name']} <- {payload['email']}")

    print("\n[2/4] Posting jobs")
    jobs = []
    template_cycle = list(JOB_TEMPLATES)
    random.shuffle(template_cycle)
    index = 0
    for employer in employers:
        for _ in range(jobs_per_employer):
            template = template_cycle[index % len(template_cycle)]
            index += 1
            remote = random.random() < 0.3
            payload = {
                "company_id": employer["company_id"],
                "title": template["title"],
                "description": template["description"],
                "requirements": template["requirements"],
                "responsibilities": template["responsibilities"],
                "skills": template["required_skills"] + template["preferred_skills"],
                "required_skills": template["required_skills"],
                "preferred_skills": template["preferred_skills"],
                "location": "Remote" if remote else employer["location"],
                "is_remote": remote,
                "salary_min": float(template["salary"][0]),
                "salary_max": float(template["salary"][1]),
                "salary_currency": "USD",
                "job_type": template["job_type"],
                "experience_level": template["experience_level"],
                "experience_years_min": template["years"][0],
                "experience_years_max": template["years"][1],
                "benefits": ["Health insurance", "401(k) match", "Remote friendly",
                             "Learning budget"],
                "status": "active",
            }
            job = api.request("POST", "/jobs", token=employer["token"],
                              json=payload, expected=201)
            jobs.append({
                "id": job["id"],
                "title": job["title"],
                "company_name": employer["company_name"],
                "skills": template["required_skills"],
            })
            counts["jobs"] += 1
            print(f"    {job['title']} @ {employer['company_name']}")

    print("\n[3/4] Creating job seekers" + (" with resumes" if include_resumes else ""))
    seekers = []
    for first, last, location, years, job_title, skills, education in CANDIDATES[:seeker_count]:
        handle = f"{first.lower()}.{last.lower().replace(chr(39), '')}"
        payload = {
            "email": f"{handle}@{SEED_EMAIL_DOMAIN}",
            "password": password,
            "first_name": first,
            "last_name": last,
            "role": "job_seeker",
            "location": location,
            "phone": f"555-01{random.randint(10, 99)}",
        }
        result = api.request("POST", "/auth/register", json=payload, expected=201)
        token = result["access_token"]

        api.request("PUT", "/users/me", token=token, json={
            "skills": skills,
            "experience_years": years,
            "education": education,
            "job_title": job_title,
            "bio": (f"{job_title} with {years} years of experience, focused on "
                    f"{', '.join(skills[:3])}."),
            "linkedin_url": f"https://linkedin.example.com/in/{handle}",
        })

        if include_resumes:
            content = build_resume_docx(first, last, job_title, years,
                                        skills, education, location)
            try:
                api.request(
                    "POST", "/resumes/upload", token=token, expected=201,
                    files={"file": (
                        f"{handle}_resume.docx",
                        content,
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )},
                )
                counts["resumes"] += 1
            except SeedError as exc:
                print(f"    resume upload failed for {handle}: {exc}")

        seekers.append({
            "token": token, "name": f"{first} {last}", "years": years,
            "job_title": job_title, "skills": skills, "email": payload["email"],
        })
        counts["seekers"] += 1
        print(f"    {first} {last} <- {payload['email']}")

    print("\n[4/4] Submitting applications")
    for seeker in seekers:
        matches = sorted(
            jobs,
            key=lambda job: len(set(job["skills"]) & set(seeker["skills"])),
            reverse=True,
        )
        for job in matches[:applications_per_seeker]:
            letter = COVER_LETTER.format(
                company=job["company_name"], title=job["title"],
                years=seeker["years"], skills=", ".join(seeker["skills"][:3]),
                job_title=seeker["job_title"], name=seeker["name"],
            )
            try:
                api.request("POST", "/applications", token=seeker["token"],
                            json={"job_id": job["id"], "cover_letter": letter},
                            expected=201)
                counts["applications"] += 1
            except SeedError as exc:
                print(f"    application failed ({seeker['name']} -> {job['title']}): {exc}")
        print(f"    {seeker['name']} applied to {min(applications_per_seeker, len(matches))} jobs")

    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed TalentNest demo data via the API.")
    parser.add_argument("--api-url", default=DEFAULT_API_URL)
    parser.add_argument("--password", default=DEFAULT_PASSWORD)
    parser.add_argument("--employers", type=int, default=4)
    parser.add_argument("--seekers", type=int, default=12)
    parser.add_argument("--jobs-per-employer", type=int, default=3)
    parser.add_argument("--applications-per-seeker", type=int, default=3)
    parser.add_argument("--no-resumes", action="store_true")
    args = parser.parse_args()

    api = ApiClient(args.api_url)
    print(f"Target API: {api.base_url}")
    try:
        api.request("GET", "/jobs", params={"page": 1, "page_size": 1})
    except (SeedError, requests.RequestException) as exc:
        print("\nCannot reach the backend. Start it first:")
        print("    cd backend")
        print("    .\\venv\\Scripts\\Activate.ps1")
        print("    python -m uvicorn app.main:app --host 127.0.0.1 --port 8000")
        print(f"\nDetail: {exc}")
        return 1

    try:
        counts = seed(
            api, args.password, args.employers, args.seekers,
            args.jobs_per_employer, args.applications_per_seeker,
            include_resumes=not args.no_resumes,
        )
    except SeedError as exc:
        print(f"\nSeeding stopped: {exc}")
        return 1

    print("\n" + "=" * 58)
    print("Seeding complete")
    print("=" * 58)
    for label, value in counts.items():
        print(f"  {label:<14} {value}")
    print(f"\n  Password for every seeded account: {args.password}")
    print(f"  All seeded emails end in @{SEED_EMAIL_DOMAIN}")
    print("\n  Sign in as an employer:   hiring@northwind.%s" % SEED_EMAIL_DOMAIN)
    print("  Sign in as a job seeker:  amara.okafor@%s" % SEED_EMAIL_DOMAIN)
    return 0


if __name__ == "__main__":
    sys.exit(main())
