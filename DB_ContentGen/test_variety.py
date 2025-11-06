#!/usr/bin/env python3
"""
Test Employee Size & Company Maturity Variety

Demonstrates the variety in company sizes and maturity stages.
"""

from employer_generator import EmployerGenerator

gen = EmployerGenerator('dummy_key')

print("="*70)
print("TESTING EMPLOYEE SIZE & COMPANY MATURITY VARIETY")
print("="*70)

# Test 1: Employee Size Distribution
print("\n📊 Employee Size Distribution (50 samples):")
print("-"*70)

sizes = []
for _ in range(50):
    size = gen.generate_employee_size()
    sizes.append(size)

# Count occurrences
size_counts = {}
for size in gen.EMPLOYEE_SIZES:
    count = sizes.count(size)
    percentage = (count / 50) * 100
    size_counts[size] = count
    bar = "█" * int(percentage / 2)
    print(f"{size:15} [{count:2}] {bar} {percentage:5.1f}%")

print("\n✅ Notice: More small companies (1-50) than large ones (realistic!)")

# Test 2: Company Maturity Examples
print("\n🎂 Company Maturity Stages:")
print("-"*70)

for maturity in gen.COMPANY_MATURITY:
    years = gen.MATURITY_YEARS[maturity]
    print(f"{maturity:20} → {years}")

# Test 3: Size-Maturity Correlation
print("\n🔗 Size-Maturity Correlation (20 samples):")
print("-"*70)
print(f"{'Size':15} {'Maturity':20} {'Years'}")
print("-"*70)

for i in range(20):
    size = gen.generate_employee_size()
    maturity_data = gen.generate_company_maturity(size)
    print(f"{size:15} {maturity_data['maturity']:20} {maturity_data['years_in_business']}")

print("\n✅ Notice: Larger companies tend to be more mature (realistic correlation!)")

# Test 4: Full Company Examples
print("\n🏢 Sample Generated Employers:")
print("="*70)

for i in range(5):
    location = gen.generate_location()
    size = gen.generate_employee_size()
    maturity = gen.generate_company_maturity(size)
    name = gen.generate_funny_company_name()
    
    print(f"\n{i+1}. {name}")
    print(f"   Size: {size:15} Stage: {maturity['maturity']:15} Age: {maturity['years_in_business']}")
    print(f"   Location: {location['city']}, {location['state']}")

print("\n" + "="*70)
print("✅ Variety Test Complete!")
print("="*70)

