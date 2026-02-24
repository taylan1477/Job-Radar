import pytest
from models import Job, JobField, JobLocation, JobLevel, ScoredJob
from scoring_service import ScoringService

@pytest.fixture
def service():
    return ScoringService()

def test_process_job_gamedev_senior(service):
    """Tests a standard GameDev Senior job for correct scoring and categorization."""
    job = Job(
        title="Senior Unity Developer",
        company="Dream Studios",
        location="Ankara",
        summary="A senior position for someone with 5+ years of experience in Unity and C#.",
        description="Looking for high quality clean code and leadership."
    )
    
    result = service.process_job(job)
    
    assert result.detected_field == JobField.GAMEDEV
    assert result.detected_location == JobLocation.ANKARA
    assert result.detected_level == JobLevel.SENIOR
    assert result.total_score > 0
    assert result.is_restricted is False

def test_process_job_restricted(service):
    """Tests that restricted keywords correctly flag the job."""
    job = Job(
        title="Software Engineer",
        company="US Tech Inc",
        location="USA",
        summary="Must be a US citizen and located in the USA. Security clearance required.",
        description="Work for US government projects."
    )
    
    result = service.process_job(job)
    
    assert result.is_restricted is True
    assert result.total_score == -10.0
    assert "Restriction found" in result.restricted_reason

def test_process_job_unsupported_language(service):
    """Tests that non-English/Turkish jobs are restricted."""
    job = Job(
        title="Softwareentwickler",
        company="Berlin Hub",
        location="Berlin",
        summary="Wir suchen einen talentierten Softwareentwickler für unser Team.",
        description="Sehr gute Deutschkenntnisse sind erforderlich."
    )
    
    result = service.process_job(job)
    
    assert result.is_restricted is True
    assert result.detected_location == JobLocation.DEAD
    assert "Unsupported Language" in result.restricted_reason

def test_detect_level_regex(service):
    """Tests the year-based regex for seniority levels."""
    # Test Mid-level (2-5 years)
    job_mid = Job(title="Dev", company="C", location="L", summary="3+ years of exp")
    assert service.process_job(job_mid).detected_level == JobLevel.MID
    
    # Test Senior-level (5+ years)
    job_sr = Job(title="Dev", company="C", location="L", summary="7 years experience needed")
    assert service.process_job(job_sr).detected_level == JobLevel.SENIOR
    
    # Test Junior-level (0-2 years)
    job_jr = Job(title="Dev", company="C", location="L", summary="1 year experience")
    assert service.process_job(job_jr).detected_level == JobLevel.JUNIOR

def test_field_detection_hybrid(service):
    """Tests hybrid field detection: NLP vs Keywords."""
    # Test specific keyword override
    job_flutter = Job(title="Mobile Dev", company="C", location="L", summary="We use Flutter.")
    assert service.process_job(job_flutter).detected_field == JobField.MOBILE
    
    # Test software fallback
    job_generic = Job(title="Software Engineer", company="C", location="L", summary="Coding and stuff.")
    assert service.process_job(job_generic).detected_field == JobField.SOFTWARE
