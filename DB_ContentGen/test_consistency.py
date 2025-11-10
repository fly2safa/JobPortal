#!/usr/bin/env python3
"""
Test Company Name Consistency and Industry Variety

This test verifies:
1. Company name in the field matches the name used in the description
2. No job portal/recruiting companies are generated
3. Industry variety across multiple generations
"""

import os
from dotenv import load_dotenv
from employer_generator import EmployerGenerator

# Load environment
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    print("❌ OPENAI_API_KEY not found in .env")
    exit(1)

print("="*60)
print("TESTING COMPANY NAME CONSISTENCY & INDUSTRY VARIETY")
print("="*60)
print("\nGenerating 5 sample employers...\n")

gen = EmployerGenerator(api_key)

employers = []
for i in range(5):
    print(f"Generating employer {i+1}/5...")
    employer = gen.generate_employer_with_ai(f"Sample company {i+1}")
    employers.append(employer)

print("\n" + "="*60)
print("RESULTS")
print("="*60)

# Check consistency
print("\n✅ Consistency Check:")
for i, emp in enumerate(employers, 1):
    name = emp['company_name']
    desc = emp['company_description']
    
    # Check if first word of company name appears in description
    first_word = name.split()[0]
    if first_word in desc:
        print(f"{i}. ✅ {name}")
        print(f"   Description mentions: '{first_word}'")
    else:
        print(f"{i}. ⚠️  {name}")
        print(f"   Description: {desc[:50]}...")

# Check for job portal companies
print("\n✅ Job Portal Check:")
job_words = ['job', 'hire', 'recruit', 'talent', 'career', 'employment']
job_portal_count = 0

for i, emp in enumerate(employers, 1):
    name_lower = emp['company_name'].lower()
    desc_lower = emp['company_description'].lower()
    
    found_words = [word for word in job_words if word in name_lower or word in desc_lower]
    
    if found_words:
        print(f"{i}. ⚠️  {emp['company_name']} - Contains: {', '.join(found_words)}")
        job_portal_count += 1
    else:
        print(f"{i}. ✅ {emp['company_name']} - No job portal keywords")

# Check industry variety
print("\n✅ Industry Variety:")
industries = [emp['industry'] for emp in employers]
unique_industries = set(industries)

for i, emp in enumerate(employers, 1):
    print(f"{i}. {emp['company_name']:30} - {emp['industry']}")

print(f"\nUnique Industries: {len(unique_industries)}/{len(employers)}")
if len(unique_industries) >= 3:
    print("✅ Good variety!")
elif len(unique_industries) >= 2:
    print("⚠️  Moderate variety")
else:
    print("❌ Poor variety - all same industry")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"Job Portal Companies: {job_portal_count}/5")
print(f"Unique Industries: {len(unique_industries)}/5")
print("="*60)

