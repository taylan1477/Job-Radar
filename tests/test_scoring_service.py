import pytest
from src.core.models import Job, JobField, JobLocation, JobLevel, ScoredJob
from src.core.scoring_service import ScoringService

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

def test_process_job_defense_simulation(service):
    """Tests defense simulation engineer categorization."""
    job = Job(
        title="Simülasyon Mühendisi",
        company="Savunma Sanayii A.Ş.",
        location="Ankara",
        summary="Askeri taktik simülasyon ve sistem entegrasyon projelerinde görev alacak mühendis.",
        description="DDS ve HLA protokolleri ile çalışılacaktır."
    )
    result = service.process_job(job)
    assert result.detected_field == JobField.DEFENSE_SIMULATION
    assert result.detected_location == JobLocation.ANKARA

def test_process_job_system_network(service):
    """Tests sysadmin / NOC role categorization."""
    job = Job(
        title="Sistem Yöneticisi",
        company="DataTech",
        location="Remote",
        summary="Linux ve Windows sunucu altyapısı, NOC ve ağ operasyonları yönetimi.",
        description="Zabbix ve ağ monitoring."
    )
    result = service.process_job(job)
    assert result.detected_field == JobField.SYSTEM_NETWORK
    assert result.detected_location == JobLocation.REMOTE

def test_process_job_data_bi(service):
    """Tests DBA / BI role categorization."""
    job = Job(
        title="Veritabanı Yöneticisi (DBA)",
        company="FinansBank",
        location="İstanbul",
        summary="SQL Server ve PostgreSQL veritabanı performans optimizasyonu ve ETL süreçleri.",
        description="Veri ambarı ve BI raporlama desteği."
    )
    result = service.process_job(job)
    assert result.detected_field == JobField.DATA_BI

def test_process_job_industrial_automation(service):
    """Tests ERP / Industrial automation role categorization."""
    job = Job(
        title="ERP Uzmanı",
        company="Sanayi Grubu",
        location="Bursa",
        summary="SAP ve Dynamics 365 süreç otomasyonu ve entegrasyonu.",
        description="Depo ve üretim otomasyon sistemleri."
    )
    result = service.process_job(job)
    assert result.detected_field == JobField.INDUSTRIAL_AUTOMATION

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
    job_mid = Job(title="Dev", company="C", location="L", summary="3+ years of exp")
    assert service.process_job(job_mid).detected_level == JobLevel.MID
    
    job_sr = Job(title="Dev", company="C", location="L", summary="7 years experience needed")
    assert service.process_job(job_sr).detected_level == JobLevel.SENIOR
    
    job_jr = Job(title="Dev", company="C", location="L", summary="1 year experience")
    assert service.process_job(job_jr).detected_level == JobLevel.JUNIOR

def test_field_detection_hybrid(service):
    """Tests hybrid field detection."""
    job_mobile = Job(title="Mobile Dev", company="C", location="L", summary="We use Flutter and Android.")
    assert service.process_job(job_mobile).detected_field == JobField.SOFTWARE
    
    job_generic = Job(title="Software Engineer", company="C", location="L", summary="Backend API and web development.")
    assert service.process_job(job_generic).detected_field == JobField.SOFTWARE
