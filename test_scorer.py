"""Scorer unit testi"""
from scorer import score_job

# Test 1: Junior Unity Developer, Remote, Ankara
j = score_job({
    "title": "Junior Unity Developer",
    "summary": "Remote game development position in Ankara",
    "company": "GameCo",
    "link": "http://example.com",
    "published": "2026-01-01",
    "source": "test",
})
print(f"Test 1: Field={j['field']}, Location={j['location']}, Level={j['level']}, Score={j['total_score']}")
assert j["field"] == "gamedev", f"Expected gamedev, got {j['field']}"
assert j["location"] == "ankara", f"Expected ankara, got {j['location']}"
assert j["level"] == "junior", f"Expected junior, got {j['level']}"
assert j["total_score"] >= 4.0, f"Expected >= 4.0, got {j['total_score']}"
print("  PASSED")

# Test 2: Senior Python Developer, Istanbul
j2 = score_job({
    "title": "Senior Python Developer",
    "summary": "Looking for experienced Python developer in Istanbul",
    "company": "TechCorp",
    "link": "http://example.com/2",
    "published": "2026-01-01",
    "source": "test",
})
print(f"Test 2: Field={j2['field']}, Location={j2['location']}, Level={j2['level']}, Score={j2['total_score']}")
assert j2["field"] == "python", f"Expected python, got {j2['field']}"
assert j2["location"] == "istanbul", f"Expected istanbul, got {j2['location']}"
assert j2["level"] == "senior", f"Expected senior, got {j2['level']}"
print("  PASSED")

# Test 3: C# .NET Developer, Remote
j3 = score_job({
    "title": "C# .NET Developer",
    "summary": "Remote position working with ASP.NET Core",
    "company": "DotNetCo",
    "link": "http://example.com/3",
    "published": "2026-01-01",
    "source": "test",
})
print(f"Test 3: Field={j3['field']}, Location={j3['location']}, Level={j3['level']}, Score={j3['total_score']}")
assert j3["field"] == "c#", f"Expected c#, got {j3['field']}"
assert j3["location"] == "remote", f"Expected remote, got {j3['location']}"
print("  PASSED")

# Test 4: Lead position should have negative score impact
j4 = score_job({
    "title": "Lead Game Developer",
    "summary": "Lead a team of game developers",
    "company": "BigGame",
    "link": "http://example.com/4",
    "published": "2026-01-01",
    "source": "test",
})
print(f"Test 4: Field={j4['field']}, Location={j4['location']}, Level={j4['level']}, Score={j4['total_score']}")
assert j4["field"] == "gamedev", f"Expected gamedev, got {j4['field']}"
assert j4["level"] == "lead", f"Expected lead, got {j4['level']}"
print("  PASSED")

print("\nAll tests PASSED!")
