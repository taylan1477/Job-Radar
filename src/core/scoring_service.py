import re
import logging
from typing import Optional, Tuple

from src.core.models import Job, ScoredJob, JobField, JobLocation, JobLevel
from src.core.nlp_processor import normalize_text, detect_language, FieldDetector
import src.utils.config as config

logger = logging.getLogger(__name__)

class ScoringService:
    """
    Professional service for analyzing, categorizing, and scoring job listings.
    
    This service demonstrates 'Clean Code' principles like Single Responsibility,
    Dependency Injection, and Type Safety.
    """

    def __init__(self, cfg=config):
        self.cfg = cfg
        self._field_detector: Optional[FieldDetector] = None

    @property
    def field_detector(self) -> FieldDetector:
        """Lazy loader for the NLP-based field detector."""
        if self._field_detector is None:
            self._field_detector = FieldDetector()
        return self._field_detector

    def process_job(self, job: Job) -> ScoredJob:
        """
        Main entry point for processing a job listing.
        
        Args:
            job: The raw job listing data.
            
        Returns:
            A processed ScoredJob with detected categories and calculated score.
        """
        text = f"{job.title} {job.summary} {job.description} {job.location} {job.company}"
        normalized_text = normalize_text(text)
        
        # 1. Restriction & Language Check
        is_restricted, reason = self._check_restrictions(normalized_text)
        
        # 2. Categorization
        field = self._detect_field(normalized_text)
        location = self._detect_location(normalized_text)
        level = self._detect_level(normalized_text)
        
        # 3. Calculate Score
        if is_restricted:
            total_score = -10.0
            if reason and "Unsupported Language" in reason:
                location = JobLocation.DEAD
        else:
            total_score = self._calculate_score(field, location, level)

        return ScoredJob(
            job=job,
            detected_field=field,
            detected_location=location,
            detected_level=level,
            total_score=total_score,
            is_restricted=is_restricted,
            restricted_reason=reason,
            applied_weights={
                "field_weight": self.cfg.FIELD_WEIGHT,
                "location_weight": self.cfg.LOCATION_WEIGHT,
                "level_weight": self.cfg.LEVEL_WEIGHT
            }
        )

    def _check_restrictions(self, text: str) -> Tuple[bool, Optional[str]]:
        """Checks for geographical, visa, or language restrictions."""
        # Check negative keywords
        for kw in self.cfg.NEGATIVE_KEYWORDS:
            if kw.lower() in text:
                return True, f"Restriction found: {kw}"
        
        # Language detection
        lang = detect_language(text)
        if lang and lang not in ["en", "tr"]:
            return True, f"Unsupported Language: {lang}"
            
        return False, None

    def _detect_field(self, text: str) -> JobField:
        """Determines the technical field of the job using the 7-domain hierarchy."""
        # 1. Hard-coded priority overrides
        if re.search(r'\b(game dev|game design|game program|unity|unreal|godot|oyun gelis|oyun tasarim|gameplay)\w*', text):
            return JobField.GAMEDEV

        if re.search(r'\b(simülasyon|simulation|askeri simülasyon|taktik simülasyon|c4isr|harp oyunu|sistem entegrasyon|ara katman|middleware dev|rti dds|dis/hla)\w*', text):
            return JobField.DEFENSE_SIMULATION

        if re.search(r'\b(sistem yöneticisi|sysadmin|system administrator|noc mühendisi|noc engineer|network operations center|ağ otomasyonu)\w*', text):
            return JobField.SYSTEM_NETWORK

        if re.search(r'\b(veritabanı yöneticisi|database administrator|iş zekası|bi developer|etl developer|web scraping mühendisi|veri madenciliği)\w*', text):
            return JobField.DATA_BI

        if re.search(r'\b(erp uzmanı|erp geliştiricisi|sap danışmanı|dynamics 365|endüstriyel otomasyon|scada|süreç otomasyonu|process automation|rpa developer|wms geliştiricisi|depo yönetim)\w*', text):
            return JobField.INDUSTRIAL_AUTOMATION

        if any(kw in text for kw in ["backend", "frontend", "fullstack", "full stack", "flutter", "react native", "android developer", "ios developer", "software engineer", "yazılım mühendisi"]):
            return JobField.SOFTWARE

        # 2. NLP (TF-IDF) Inference
        try:
            detected = self.field_detector.predict(text)
            if detected:
                try:
                    return JobField(detected)
                except ValueError:
                    pass
        except Exception as e:
            logger.error(f"NLP Detection failed: {e}")

        # 3. Keyword Match Fallback
        best_field = JobField.OTHER
        max_hits = 0
        
        for field_name in self.cfg.FIELD_PRIORITY:
            keywords = self.cfg.FIELD_KEYWORDS.get(field_name, [])
            hits = self._count_hits(text, keywords)
            if hits > max_hits:
                max_hits = hits
                try:
                    best_field = JobField(field_name)
                except ValueError:
                    pass

        if best_field == JobField.OTHER:
            if self._count_hits(text, self.cfg.SOFTWARE_KEYWORDS) > 0:
                return JobField.SOFTWARE

        return best_field

    def _detect_location(self, text: str) -> JobLocation:
        """Determines job location category."""
        if re.search(r'(hybrid|hibrit|karma)\s+.*ankara|ankara\s+.*(hybrid|hibrit|karma)', text):
            return JobLocation.HYBRID_ANKARA
            
        if "ankara" in text:
            return JobLocation.ANKARA

        for kw in self.cfg.LOCATION_KEYWORDS.get("remote", []):
            if kw in text:
                return JobLocation.REMOTE

        for location, keywords in self.cfg.LOCATION_KEYWORDS.items():
            if location in ["ankara", "remote", "hybrid_ankara"]:
                continue
            for kw in keywords:
                if kw.lower() in text:
                    return JobLocation(location)

        return JobLocation.OTHER

    def _detect_level(self, text: str) -> JobLevel:
        """Determines job seniority level."""
        # Strong Junior signals
        junior_signals = [
            r'\bjunior\b', r'\bjr\b', r'\bentry level\b', r'\bentry-level\b',
            r'yeni mezun', r'stajyer', r'intern\b', r'yetistir', r'ogrenci', r'student',
            r'no experience', r'experience not required', r'0-2 year', r'0-1 year'
        ]
        for pattern in junior_signals:
            if re.search(pattern, text):
                return JobLevel.JUNIOR

        # Unvan Eslesmesi
        priority_order = ["lead", "senior", "mid", "junior", "entry"]
        for level in priority_order:
            keywords = self.cfg.LEVEL_KEYWORDS.get(level, [])
            for kw in keywords:
                if re.search(r'\b' + re.escape(kw) + r'\b', text):
                    return JobLevel(level)

        # Yil bazli tahmin
        year_match = re.search(r'(\d+)\s*\+?\s*(?:-|to)?\s*(\d+)?\s*(?:years?|yıl|yil)', text)
        if year_match:
            try:
                min_year = int(year_match.group(1))
                if min_year >= 5:
                    return JobLevel.SENIOR
                elif min_year >= 2:
                    return JobLevel.MID
                elif min_year < 2:
                    return JobLevel.JUNIOR
            except Exception:
                pass

        return JobLevel.UNKNOWN

    def _calculate_score(self, field: JobField, location: JobLocation, level: JobLevel) -> float:
        """Calculates final weighted score based on defined weights."""
        field_score = self.cfg.FIELD_SCORES.get(field.value, 1)
        location_score = self.cfg.LOCATION_SCORES.get(location.value, 0)
        level_score = self.cfg.LEVEL_SCORES.get(level.value, 0)

        total = (
            field_score * self.cfg.FIELD_WEIGHT +
            location_score * self.cfg.LOCATION_WEIGHT +
            level_score * self.cfg.LEVEL_WEIGHT
        )
        return round(total, 2)

    def _count_hits(self, text: str, keywords: list) -> int:
        """Helper to count occurrences of keywords in text."""
        count = 0
        for kw in keywords:
            kw_lower = kw.lower()
            if " " in kw_lower:
                if kw_lower in text:
                    count += 1
            elif len(kw_lower) >= 4:
                if kw_lower in text:
                    count += 1
            else:
                if re.search(r'\b' + re.escape(kw_lower) + r'\b', text):
                    count += 1
        return count
