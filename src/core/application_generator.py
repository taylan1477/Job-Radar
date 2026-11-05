import os
import re
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

logger = logging.getLogger(__name__)

CV_PROFILE_PATH = Path("cv_profile.yaml")

class ApplicationGenerator:
    """
    LLM (Gemini) destekli Ön Yazı (Cover Letter), Soğuk E-Posta (Cold Email)
    ve Easy Apply soru cevaplama motoru.
    """

    def __init__(self, profile_path: Path = CV_PROFILE_PATH, api_key: Optional[str] = None):
        self.profile = self._load_profile(profile_path)
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        self.client = None
        if GENAI_AVAILABLE and self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"GenAI Client başlatılamadı: {e}")

    def _load_profile(self, path: Path) -> Dict[str, Any]:
        """cv_profile.yaml dosyasını yükler."""
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    if isinstance(data, dict):
                        return data
            except Exception as e:
                logger.error(f"cv_profile.yaml okuma hatası: {e}")
        return {}

    def generate_cover_letter(self, job_title: str, company: str, job_description: str = "", language: str = "tr") -> str:
        """İlana özel kişiselleştirilmiş Cover Letter üretir."""
        if not self.client:
            return self._fallback_cover_letter(job_title, company, language)

        candidate_name = self.profile.get("personal_info", {}).get("full_name", "Aday")
        skills = self.profile.get("skills", {})
        summary = self.profile.get("summary", "")

        prompt = f"""
        Sen profesyonel bir kariyer danışmanı ve adaysın. Aşağıdaki adayın profil bilgilerini kullanarak,
        belirtilen iş ilanı için etkileyici, profesyonel, abartıdan uzak ve pozisyona tam odaklı bir Ön Yazı (Cover Letter) hazırla.
        
        Dil: {'Türkçe' if language == 'tr' else 'İngilizce'}
        
        Aday Bilgileri:
        - İsim: {candidate_name}
        - Özet: {summary}
        - Yetenekler: {skills}
        
        İlan Bilgileri:
        - Pozisyon: {job_title}
        - Şirket: {company}
        - İlan Açıklaması / Detayları: {job_description[:1000]}
        
        Kurallar:
        - 3 veya 4 kısa, vurucu paragraftan oluşsun.
        - Şirketin adını ve pozisyonu tam olarak belirt.
        - Adım adım neden bu rol için uygun olduğunu somut teknik yeteneklerle açıkla.
        - Sadece ön yazı metnini yaz, markdown başlığı veya selamlama harici açıklama ekleme.
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            logger.warning(f"Gemini API cover letter hatası: {e}. Fallback şablon kullanılıyor.")
            return self._fallback_cover_letter(job_title, company, language)

    def generate_email_application(self, job_title: str, company: str, job_description: str = "") -> Dict[str, str]:
        """İK'ya gönderilecek e-postanın Konu (Subject) ve Gövde (Body) metnini üretir."""
        candidate_name = self.profile.get("personal_info", {}).get("full_name", "Taylan Özgür Özdemir")
        subject = f"İş Başvurusu: {job_title} – {candidate_name}"
        body = self.generate_cover_letter(job_title, company, job_description, language="tr")
        return {"subject": subject, "body": body}

    def answer_form_question(self, question: str, options: Optional[list] = None) -> str:
        """
        LinkedIn Easy Apply formlarında çıkan soruları adayın profiline göre akıllıca yanıtlar.
        Örn: 'Kaç yıl Unity deneyiminiz var?', 'Ankara'da ikamet ediyor musunuz?'
        """
        q_lower = question.lower()
        answers = self.profile.get("common_answers", {})
        exp = self.profile.get("experience_years", {})

        # 1. Hızlı ve Deterministik Kural Eşleştirmeleri
        if any(w in q_lower for w in ["unity", "unreal", "game"]):
            return str(exp.get("gamedev", 2))
        if any(w in q_lower for w in ["c#", "csharp", ".net"]):
            return str(exp.get("csharp", 3))
        if any(w in q_lower for w in ["python"]):
            return str(exp.get("python", 3))
        if any(w in q_lower for w in ["deneyim", "experience", "year", "yıl"]):
            return str(exp.get("software_general", 3))
        if any(w in q_lower for w in ["ankara", "ikamet", "relocate", "şehir"]):
            return "Evet"
        if any(w in q_lower for w in ["remote", "uzaktan"]):
            return "Evet"
        if any(w in q_lower for w in ["ingilizce", "english"]):
            return answers.get("english_level", "İleri Seviye")
        if any(w in q_lower for w in ["askerlik", "military"]):
            return answers.get("military_service", "Muaf")
        if any(w in q_lower for w in ["ehliyet", "license", "driver"]):
            return answers.get("driver_license", "B")

        # 2. LLM Fallback (Eğer karmaşık veya seçenekli bir soruysa)
        if self.client:
            prompt = f"""
            Adayın profiline göre şu iş başvurusu sorusunu yanıtla:
            Soru: "{question}"
            Seçenekler: {options if options else 'Açık uçlu / Metin'}
            
            Aday Profili: {self.profile}
            
            Kural: Sadece cevabı ver. Tek kelime, sayı veya seçeneklerden birini döndür. Asla açıklama ekleme.
            """
            try:
                res = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                return res.text.strip()
            except Exception:
                pass

        if options:
            return options[0]
        return "Evet"

    def _fallback_cover_letter(self, job_title: str, company: str, language: str) -> str:
        """API anahtarı olmadığı veya çağrı başarısız olduğunda kullanılan şablon."""
        name = self.profile.get("personal_info", {}).get("full_name", "Taylan Özgür Özdemir")
        if language == "tr":
            return (
                f"Merhaba {company} Yetkilisi,\n\n"
                f"{job_title} pozisyonunuzu büyük bir ilgiyle inceledim. "
                f"GameDev ve modern yazılım mühendisliği alanındaki deneyimlerim, "
                f"Clean Code ve SOLID prensiplerine bağlılığım ile ekibinize değer katabileceğime inanıyorum.\n\n"
                f"Geliştirdiğim projeler ve yetkinliklerim ekteki özgeçmişimde detaylandırılmıştır. "
                f"Pozisyona ilişkin detayları ve katabileceğim değerleri görüşmek üzere sizinle tanışmaktan memnuniyet duyarım.\n\n"
                f"Saygılarımla,\n{name}"
            )
        else:
            return (
                f"Dear Hiring Team at {company},\n\n"
                f"I am writing to express my strong interest in the {job_title} position. "
                f"With hands-on experience in GameDev and modern software engineering, "
                f"combined with a strong commitment to Clean Code and SOLID standards, "
                f"I am confident in my ability to contribute effectively to your team.\n\n"
                f"My background and key achievements are detailed in the attached resume. "
                f"I would welcome the opportunity to discuss how my skillset aligns with your goals.\n\n"
                f"Sincerely,\n{name}"
            )
