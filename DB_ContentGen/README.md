# TalentNest Job Candidate Generator

A Python script that generates fictitious job candidates for the TalentNest job portal using OpenAI's API.

## Features

- **Single Candidate Generation**: Provide a description and generate one candidate profile
- **Bulk Generation**: Enter a number to generate multiple candidates at once
- **AI-Powered Profiles**: Uses OpenAI to create realistic candidate information
- **Interactive CLI**: Review and accept/reject candidates individually or in bulk
- **Unique Data**: Ensures unique usernames, emails, and GitHub accounts
- **Smart Usernames**: Generates usernames based on candidate's name and skills (e.g., john.smith, sarah_connor, alex_python)
- **Persistent Storage**: Saves accepted candidates to JSON file and MongoDB
- **Database Integration**: Automatic MongoDB insertion with connection testing

## Installation

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in this directory with your credentials:
```bash
OPENAI_API_KEY=your_openai_api_key_here
project_db_url=your_database_url_here
project_db_name=your_database_name_here
```

(See `env_example.txt` for reference)

## Usage

Make sure your virtual environment is activated, then run the script:
```bash
source venv/bin/activate  # If not already activated
python candidate_generator.py
```

### Generate a Single Candidate

Enter a description when prompted:
```
👉 Your input: Senior Python developer with ML experience
```

### Generate Multiple Candidates

Enter a number when prompted:
```
👉 Your input: 5
```

Then choose to:
1. Review each candidate individually
2. Accept all candidates
3. Reject all candidates

## Candidate Fields

Each generated candidate includes:

- **firstname**: First name
- **lastname**: Last name
- **username**: Movie character username (e.g., "luke_skywalker")
- **password**: Random plaintext password
- **application**: Role/position seeking
- **phone_number**: 7-digit 555 phone number
- **email**: 10-digit number @revpro.com
- **github_account**: github.com/10-digit-number
- **skills**: List of relevant technical skills
- **experience_years**: Years of experience
- **education**: Highest degree
- **bio**: Professional bio
- **apps_submitted**: Empty array (for future use)
- **interview_status**: Null (for future use)
- **jobs_bookmarked**: Empty array (for future use)

## Output

Accepted candidates are saved to:
1. **JSON file**: `generated_candidates.json` (always created as backup)
2. **MongoDB**: Inserted into the `candidates` collection (if configured)

Each run appends new candidates to both storage locations.

## Testing MongoDB Connection

Before generating candidates, you can test your MongoDB connection:

```bash
source venv/bin/activate
python test_mongodb.py
```

This will verify your database credentials and show existing collections.

## Example Output

```
📋 Name:             Sarah Connor
👤 Username:         sarah.connor (generated from name)
🔑 Password:         Tech847!
💼 Application:      Senior Software Engineer
📞 Phone:            555-7392
📧 Email:            1234567890@revpro.com
💻 GitHub:           github.com/9876543210
🛠️  Skills:           Python, Machine Learning, TensorFlow, AWS, Docker
📊 Experience:       8 years
🎓 Education:        Master's in Computer Science
📝 Bio:              Experienced software engineer specializing in machine learning...
```

### Username Generation Patterns

Usernames are generated using these patterns (in order of preference):
1. `firstname.lastname` (e.g., john.smith)
2. `firstname_lastname` (e.g., sarah_connor)
3. `firstnamelastname` (e.g., alexjohnson)
4. `firstinitiallastname` (e.g., jsmith)
5. `firstname_skill` (e.g., alex_python, maria_data)
6. `skill_lastname` (e.g., python_smith)
7. `firstname_lastnameNN` (with numbers if all patterns taken)

## Notes

- The script uses GPT-4o-mini for cost-effective candidate generation
- Usernames are intelligently generated based on the candidate's name and skills
- All contact information is fictitious and follows specified formats
- The script includes fallback generation if OpenAI API fails
- Usernames are guaranteed to be unique across all generated candidates

