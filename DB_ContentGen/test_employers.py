#!/usr/bin/env python3
"""
Test Employer Generator

Quick test to see sample employer generation.
"""

from employer_generator import EmployerGenerator

# Test with dummy API key for structure
gen = EmployerGenerator('dummy_key')

print("="*60)
print("SAMPLE EMPLOYER GENERATION")
print("="*60)
print()

print("Sample Funny Company Names:")
for i in range(10):
    name = gen.generate_funny_company_name()
    print(f"  {i+1}. {name}")

print()
print("Sample Locations:")
for i in range(5):
    location = gen.generate_location()
    print(f"  {i+1}. {location['city']}, {location['state']}")

print()
print("Sample Passwords:")
for i in range(5):
    pwd = gen.generate_password()
    print(f"  {i+1}. {pwd}")

print()
print("="*60)
print("✅ Employer generator structure looks good!")
print("="*60)

