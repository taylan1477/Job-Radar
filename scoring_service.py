import re
import logging
from typing import Optional, Tuple

from models import Job, ScoredJob, JobField, JobLocation, JobLevel
from nlp_processor import normalize_text, detect_language, FieldDetector
import config

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
        
        # Override location if language is not supported
        if reason and "Language" in reason:
            location = JobLocation.DEAD

        # 3. Scoring
        if is_restricted:
            total_score = -10.0
        else:
            total_score = self._calculate_sum(field, location, level)
            
        return ScoredJob(
            **job.model_dump(),
            detected_field=field,
            detected_location=location,
            detected_level=level,
            total_score=total_score,
            is_restricted=is_restricted,
            restricted_reason=reason
        )

    def _check_restrictions(self, text: str) -> Tuple[bool, Optional[str]]:
        """Checks if the job has visa/location restrictions or unsupported language."""
        # Check negative keywords (visa/local only)
        for kw in self.cfg.NEGATIVE_KEYWORDS:
            if kw.lower() in text:
                return True, f"Restriction found: {kw}"
        
        # Language detection
        lang = detect_language(text)
        if lang and lang not in ["en", "tr"]:
            return True, f"Unsupported Language: {lang}"
            
        return False, None

    def _detect_field(self, text: str) -> JobField:
        """Determines the technical field of the job using a hybrid approach."""
        # Pre-calculate for generic check
        job_title_lower = text[:100] # Usually title is at the beginning
        # 1. Hard-coded priority overrides (The "Fast Path")
        if re.search(r'\b(game dev|game design|game program|unity|unreal|godot|oyun gelis|oyun tasarim)\w*', text):
            return JobField.GAMEDEV
        
        if any(kw in text for kw in ["flutter", "react native", "ios developer", "android developer"]):
            return JobField.MOBILE

        if any(kw in text for kw in ["frontend", "front-end"]):
            return JobField.FRONTEND

        if any(kw in text for kw in ["backend", "back-end"]):
            return JobField.BACKEND
            
        # 2. NLP (TF-IDF) Inference
        # We only trust NLP if it's not a generic "Software Engineer" which might be biased in the corpus
        is_generic_title = any(kw in job_title_lower for kw in ["software engineer", "software developer", "yazılım mühendisi"])
        
        try:
            detected = self.field_detector.predict(text)
            if detected:
                # If NLP says c# but it's a generic title and no c# keywords are found, we suspect bias
                if detected == "c#" and is_generic_title:
                     if self._count_hits(text, self.cfg.FIELD_KEYWORDS.get("c#", [])) == 0:
                         detected = None # Fallback to keyword matching
                
                if detected:
                    return JobField(detected)
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
                best_field = JobField(field_name)

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

        # Check for remote keywords
        for kw in self.cfg.LOCATION_KEYWORDS.get("remote", []):
            if kw.lower() in text:
                return JobLocation.REMOTE

        # Check other predefined locations
        for loc_name, keywords in self.cfg.LOCATION_KEYWORDS.items():
            if loc_name in ["ankara", "remote", "hybrid_ankara"]:
                continue
            if any(kw.lower() in text for kw in keywords):
                try:
                    return JobLocation(loc_name)
                except ValueError:
                    continue

        return JobLocation.OTHER

    def _detect_level(self, text: str) -> JobLevel:
        """Determines required seniority level."""
        # 1. Strong Junior Signals
        junior_patterns = [
            r'\bjunior\b', r'\bjr\b', r'\bentry level\b', r'\bentry-level\b',
            r'yeni mezun', r'stajyer', r'intern\b', r'yetistir', r'ogrenci',
            r'no experience', r'0-2 year', r'0-1 year'
        ]
        if any(re.search(p, text) for p in junior_patterns):
            return JobLevel.JUNIOR

        # 2. Year-based Regex detection
        year_match = re.search(r'(\d+)\s*\+?\s*(?:-|to)?\s*(\d+)?\s*(?:years?|yıl|yil)', text)
        if year_match:
            min_years = int(year_match.group(1))
            if min_years >= 5: return JobLevel.SENIOR
            if min_years >= 2: return JobLevel.MID
            return JobLevel.JUNIOR

        # 3. Priority Keyword Lookup
        for level in ["lead", "senior", "mid", "junior"]:
            keywords = self.cfg.LEVEL_KEYWORDS.get(level, [])
            if any(re.search(r'\b' + re.escape(kw) + r'\b', text) for kw in keywords):
                return JobLevel(level)

        return JobLevel.UNKNOWN

    def _calculate_sum(self, field: JobField, location: JobLocation, level: JobLevel) -> float:
        """Calculates the weighted score based on detected categories."""
        f_score = self.cfg.FIELD_SCORES.get(field.value, 1)
        l_score = self.cfg.LOCATION_SCORES.get(location.value, 0)
        sen_score = self.cfg.LEVEL_SCORES.get(level.value, 0)

        total = (
            f_score * self.cfg.FIELD_WEIGHT +
            l_score * self.cfg.LOCATION_WEIGHT +
            sen_score * self.cfg.LEVEL_WEIGHT
        )
        return round(total, 2)

    def _count_hits(self, text: str, keywords: list) -> int:
        """Utility to count keyword matches in text."""
        count = 0
        for kw in keywords:
            kw = kw.lower()
            if len(kw) < 4 or "#" in kw or "+" in kw: # Symbols or short words
                 if re.search(r'\b' + re.escape(kw) + r'\b', text):
                     count += 1
            elif kw in text:
                count += 1
        return count
