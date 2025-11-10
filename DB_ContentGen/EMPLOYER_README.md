# TalentNest Employer Generator

A Python script that generates fictitious employer/company profiles for the TalentNest job portal using OpenAI's API.

## Features

- **Single Employer Generation**: Provide a description and generate one employer profile
- **Bulk Generation**: Enter a number to generate multiple employers at once
- **AI-Powered Profiles**: Uses OpenAI to create realistic company information
- **Interactive CLI**: Review and accept/reject employers individually or in bulk
- **Funny Company Names**: Creative and humorous company names (e.g., "Quantum Penguin Systems", "TurboPhoenix")
- **Real US Locations**: Uses actual US cities and states
- **Persistent Storage**: Saves accepted employers to JSON file and MongoDB
- **Database Integration**: Automatic MongoDB insertion into "Employers" collection

## Installation

Uses the same virtual environment as the candidate generator:

```bash
cd /home/jason/Python/AzNext_VibeCoding/JobPortal/DB_ContentGen
source venv/bin/activate  # Should already have all dependencies
```

## Usage

```bash
source venv/bin/activate
python employer_generator.py
```

### Generate a Single Employer

Enter a description when prompted:
```
👉 Your input: Tech startup focused on AI and machine learning
```

### Generate Multiple Employers

Enter a number when prompted:
```
👉 Your input: 10
```

Then choose to:
1. Review each individually
2. Accept all
3. Reject all

## Employer Fields

Each generated employer includes:

- **company_name**: Funny/creative company name (e.g., "Quantum Llama Inc")
- **password**: Random plaintext password
- **company_description**: 2-3 sentence description of the company
- **industry**: Primary industry (Technology, Healthcare, Finance, etc.)
- **employee_size**: Company size range ("1-10", "11-50", "51-200", etc.) - weighted distribution
- **company_maturity**: Stage of company (Startup, Growth Stage, Established, etc.)
- **years_in_business**: Age range corresponding to maturity (e.g., "4-8 years")
- **location**: Full location string (e.g., "San Francisco, CA")
- **city**: City name
- **state**: State abbreviation

## Example Output

```
🏢 Company Name:     Quantum Penguin Systems
🔑 Password:         Company847!
📋 Description:      An innovative tech company specializing in AI-powered 
                     solutions for enterprise clients. We focus on machine 
                     learning and data analytics.
🏭 Industry:         Technology
👥 Employee Size:    51-200
🎂 Company Stage:    Growth Stage (4-8 years)
📍 Location:         San Francisco, CA
```

## Funny Company Name Patterns

Company names are generated using:
- **Adjectives**: Quantum, Digital, Mega, Super, Ultra, Hyper, Cyber, Meta, etc.
- **Nouns**: Llama, Penguin, Unicorn, Dragon, Phoenix, Ninja, Robot, etc.
- **Suffixes**: Inc, Corp, LLC, Ltd, Systems, Solutions, Technologies, etc.

Examples:
- `Quantum Penguin Systems`
- `TurboPhoenix`
- `Ninja Technologies`
- `Cyber Unicorn LLC`
- `Mega Dragon Corp`

## Industries Supported

Technology, Healthcare, Finance, E-commerce, Education, Manufacturing, Retail, 
Consulting, Media & Entertainment, Real Estate, Transportation, Telecommunications, 
Energy, Hospitality, Agriculture, Construction, Automotive

## Employee Size Ranges (Weighted Distribution)

Company sizes follow a realistic distribution with more small companies:

- **1-10** (25%) - Most common
- **11-50** (30%) - Very common
- **51-200** (20%) - Common
- **201-500** (12%) - Moderate
- **501-1000** (8%) - Less common
- **1001-5000** (3%) - Rare
- **5001-10000** (1.5%) - Very rare
- **10000+** (0.5%) - Extremely rare

## Company Maturity Stages

Companies are assigned a maturity stage that correlates with their size:

- **Startup** (0-2 years) - Just getting started
- **Early Stage** (2-4 years) - Finding product-market fit
- **Growth Stage** (4-8 years) - Rapid expansion
- **Established** (8-15 years) - Proven business model
- **Mature** (15-25 years) - Market leader
- **Enterprise** (25-40 years) - Large-scale operations
- **Legacy** (40-75 years) - Long-standing institution
- **Industry Leader** (75+ years) - Historic company

**Correlation**: Larger companies (500+ employees) tend to be more mature (Established-Enterprise), while smaller companies (1-50) are typically Startups or Early Stage.

## Output

Accepted employers are saved to:
1. **JSON file**: `generated_employers.json` (always created as backup)
2. **MongoDB**: Inserted into the `Employers` collection (if configured)

## Testing

Test the company name generator:
```bash
python test_employers.py
```

This will show sample company names, locations, and passwords.

## MongoDB Collection

**Database**: Uses `project_db_name` from `.env`  
**Collection**: `Employers` (capital E)

## Notes

- Uses the same `.env` configuration as candidate generator
- Company names are guaranteed to be unique within each session
- All data is fictitious and generated for testing purposes
- The script uses GPT-4o-mini for cost-effective generation
- Includes 30 major US cities for realistic locations

