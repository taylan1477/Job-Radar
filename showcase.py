"""
Job Radar Project - Clean Code Showcase
Run this script to see the professional scoring service in action.

This module demonstrates:
- Strong Type Hinting
- Pydantic Data Validation
- Unit Testing (run via 'pytest tests/test_scoring_service.py')
- Service-Oriented Architecture
"""

import sys
import io
from models import Job
from scoring_service import ScoringService

# Fix Windows console encoding if needed
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

def run_showcase():
    service = ScoringService()
    
    samples = [
        Job(
            title="Senior Unity Developer",
            company="Global Game Studio",
            location="Remote / Ankara",
            summary="Looking for someone with 5+ years experience in C# and Unity.",
            description="Focus on clean code, architecture and performance optimization."
        ),
        Job(
            title="Software Engineer",
            company="Sezzle",
            location="Remote",
            summary="Junior Backend role for modern web apps.",
            description="Tech stack: Python, FastAPI, AWS. No specific seniority required."
        ),
        Job(
            title="Backend Developer (US only)",
            company="Strict Corp",
            location="US-Based",
            summary="Must be authorized to work in the US.",
            description="Legacy systems maintenance."
        )
    ]
    
    print("="*60)
    print("JOB RADAR - PROFESSIONAL SCORING SHOWCASE")
    print("="*60)
    
    for i, raw_job in enumerate(samples, 1):
        processed = service.process_job(raw_job)
        
        print(f"\n[{i}] {processed.title} @ {processed.company}")
        print(f"    {'Field':<15}: {processed.detected_field.value}")
        print(f"    {'Location':<15}: {processed.detected_location.value}")
        print(f"    {'Seniority':<15}: {processed.detected_level.value}")
        print(f"    {'Score':<15}: {processed.total_score}")
        
        if processed.is_restricted:
            print(f"    ⚠️  RESTRICTED: {processed.restricted_reason}")
            
    print("\n" + "="*60)
    print("Documentation: See tests/test_scoring_service.py for unit tests.")
    print("="*60)

if __name__ == "__main__":
    run_showcase()
