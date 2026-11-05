import os
import re
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

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

    def _match_option(self, options: List[str], preferred_keywords: List[str], default_index: int = 0) -> str:
        """Seçenekler listesi içinde anahtar kelimelere en uygun olanını bulur."""
        for kw in preferred_keywords:
            kw_clean = kw.lower().strip()
            for opt in options:
                if kw_clean in opt.lower():
                    return opt
        if 0 <= default_index < len(options):
            return options[default_index]
        return options[0] if options else ""

    def answer_form_question(self, question: str, options: Optional[List[str]] = None) -> str:
        """
        LinkedIn Easy Apply formlarında çıkan soruları adayın profiline göre akıllıca yanıtlar.
        Örn: 'Kaç yıl Unity deneyiminiz var?', 'Çince yetkinlik seviyeniz?', 'Ankara'da ikamet ediyor musunuz?'
        """
        q_clean = (question or "").strip()
        q_lower = q_clean.lower()
        answers = self.profile.get("common_answers", {})
        exp = self.profile.get("experience_years", {})
        spoken = self.profile.get("spoken_languages", {})

        # Temizlenmiş geçerli seçenekler (Seçiniz / Select placeholder'ları elenmiş)
        valid_options = []
        if options:
            valid_options = [
                o.strip() for o in options 
                if o.strip() and not any(ph in o.lower() for ph in ["seçiniz", "seçin", "select an option", "choose", "belirleyin", "lütfen"])
            ]
            if not valid_options:
                valid_options = [o.strip() for o in options if o.strip()]

        # -------------------------------------------------------------
        # 1. Konuşma Dilleri (Spoken Languages)
        # -------------------------------------------------------------
        # A) Çince / Mandarin (Aday bilmiyor -> 0 yıl / Yok / None / Hayır)
        if any(w in q_lower for w in ["çince", "chinese", "mandarin", "zh-cn"]):
            if valid_options:
                return self._match_option(
                    valid_options, 
                    ["none", "yok", "bilmiyorum", "hayır", "no", "not applicable", "başlangıç", "elementary", "basic", "temel", "0"],
                    default_index=len(valid_options) - 1
                )
            if any(w in q_lower for w in ["yıl", "year", "deneyim", "experience", "kaç"]):
                return "0"
            if any(w in q_lower for w in ["biliyor", "speak", "fluent", "yetkin"]):
                return "Hayır"
            return "Yok"

        # B) Diğer Yabancı Diller (Fransızca, İspanyolca, Rusça, Arapça, İtalyanca, Japonca vb.)
        foreign_langs = ["fransızca", "french", "ispanyolca", "spanish", "rusça", "russian", "arapça", "arabic", "italyanca", "italian", "japonca", "japanese"]
        if any(w in q_lower for w in foreign_langs):
            if valid_options:
                return self._match_option(
                    valid_options,
                    ["none", "yok", "bilmiyorum", "hayır", "no", "başlangıç", "elementary", "basic", "0"],
                    default_index=len(valid_options) - 1
                )
            if any(w in q_lower for w in ["yıl", "year", "deneyim", "experience", "kaç"]):
                return "0"
            return "Yok"

        # C) İngilizce (Aday: İleri Düzey / Professional Working C1)
        if any(w in q_lower for w in ["ingilizce", "english"]):
            if valid_options:
                return self._match_option(
                    valid_options,
                    ["full professional", "professional working", "professional", "ileri", "fluent", "c1", "c2", "b2", "akıcı", "proficient"],
                    default_index=0
                )
            if any(w in q_lower for w in ["yıl", "year", "deneyim", "experience", "kaç"]):
                return "5"
            return answers.get("english_level", "İleri Seviye (Professional)")

        # D) Almanca (Aday: Başlangıç / Elementary A1-A2)
        if any(w in q_lower for w in ["almanca", "german", "deutsch"]):
            if valid_options:
                return self._match_option(
                    valid_options,
                    ["elementary", "basic", "temel", "başlangıç", "a1", "a2"],
                    default_index=0
                )
            if any(w in q_lower for w in ["yıl", "year", "deneyim", "experience", "kaç"]):
                return "1"
            return answers.get("german_level", "Başlangıç (Basic)")

        # E) Türkçe (Aday: Anadili / Native)
        if any(w in q_lower for w in ["türkçe", "turkish"]):
            if valid_options:
                return self._match_option(
                    valid_options,
                    ["native", "anadili", "ana dil", "bilingual", "ileri"],
                    default_index=0
                )
            return "Anadili (Native)"

        # -------------------------------------------------------------
        # 2. Vize, İkamet, Taşınma ve Yasal İzinler
        # -------------------------------------------------------------
        if any(w in q_lower for w in ["sponsor", "vize", "visa"]):
            if valid_options:
                return self._match_option(valid_options, ["hayır", "no", "ihtiyacım yok", "not required"])
            return "Hayır"

        if any(w in q_lower for w in ["relocate", "taşın"]):
            if valid_options:
                return self._match_option(valid_options, ["hayır", "no"])
            return "Hayır"

        if any(w in q_lower for w in ["authorized", "authorization", "çalışma izni", "legal to work"]):
            if valid_options:
                return self._match_option(valid_options, ["evet", "yes", "authorized"])
            return "Evet"

        if any(w in q_lower for w in ["remote", "uzaktan"]):
            if valid_options:
                return self._match_option(valid_options, ["evet", "yes"])
            return "Evet"

        if any(w in q_lower for w in ["ankara", "ikamet", "şehir", "city", "location"]):
            if valid_options:
                return self._match_option(valid_options, ["evet", "yes", "ankara"])
            return "Evet"

        if any(w in q_lower for w in ["askerlik", "military"]):
            if valid_options:
                return self._match_option(valid_options, ["muaf", "tamamlandı", "yapıldı", "completed", "exempt", "evet", "yes"])
            return answers.get("military_service", "Muaf")

        if any(w in q_lower for w in ["ehliyet", "license", "driver"]):
            if valid_options:
                return self._match_option(valid_options, ["b", "evet", "yes", "var"])
            return answers.get("driver_license", "B")

        # -------------------------------------------------------------
        # 3. Teknik Beceriler ve Deneyim Yılları
        # -------------------------------------------------------------
        if any(w in q_lower for w in ["unity", "unreal", "game", "oyun"]):
            if valid_options:
                return self._match_option(valid_options, ["2", "3", "evet", "yes", "orta", "ileri"])
            return str(exp.get("gamedev", 2))

        if any(w in q_lower for w in ["c#", "csharp", ".net", "dotnet"]):
            if valid_options:
                return self._match_option(valid_options, ["3", "2", "evet", "yes", "orta", "ileri"])
            return str(exp.get("csharp", 3))

        if any(w in q_lower for w in ["python"]):
            if valid_options:
                return self._match_option(valid_options, ["3", "2", "evet", "yes", "orta", "ileri"])
            return str(exp.get("python", 3))

        if any(w in q_lower for w in ["c++", "cpp"]):
            if valid_options:
                return self._match_option(valid_options, ["2", "1", "evet", "yes"])
            return str(exp.get("cpp", 2))

        if any(w in q_lower for w in ["sql", "database", "veritabanı"]):
            if valid_options:
                return self._match_option(valid_options, ["2", "3", "evet", "yes"])
            return str(exp.get("sql", 2))

        # Genel yazılım / mühendislik deneyim yılı sorusu
        if any(w in q_lower for w in ["yazılım", "software", "developer", "mühendis"]):
            if any(w in q_lower for w in ["yıl", "year", "deneyim", "experience", "kaç"]):
                if valid_options:
                    return self._match_option(valid_options, ["3", "2", "1"])
                return str(exp.get("software_general", 3))

        # -------------------------------------------------------------
        # 4. LLM (Gemini) Fallback
        # -------------------------------------------------------------
        if self.client and q_clean:
            prompt = f"""
            Sen adayın adına iş başvurusu form sorularını yanıtlayan bir asistansın.
            
            Aday Profili:
            - Ad: {self.profile.get('personal_info', {}).get('full_name')}
            - Meslek: Game Developer & Yazılım Mühendisi
            - Konum: Ankara, Türkiye (Uzaktan çalışmaya açık, şehir değiştirmeye kapalı)
            - Konuşma Dilleri: Türkçe (Anadili), İngilizce (İleri Düzey C1 / Professional Working), Almanca (Başlangıç A1-A2).
              DİKKAT: Aday Çince, Fransızca, İspanyolca, Rusça veya diğer yabancı dilleri BİLMEMEKTEDİR (Deneyim: 0 yıl, Seviye: Yok / None).
            - Teknik Yetkinlikler: Unity (2 yıl), C# (3 yıl), Python (3 yıl), C++ (2 yıl), SQL (2 yıl), Genel Yazılım (3 yıl).
            - Vize / Sponsorluk: İhtiyacı yok (Sponsorship required: No).
            - Askerlik: Muaf / Tamamlandı.
            - Ehliyet: B sınıfı.
            
            Soru: "{q_clean}"
            Seçenekler: {valid_options if valid_options else 'Açık uçlu metin veya sayı'}
            
            Kurallar:
            1. Eğer Seçenekler listesi verilmişse, MUTLAKA listedeki seçeneklerden birini BİREBİR harfiyen seçip döndür.
            2. Eğer soru bir dil veya bilinmeyen teknoloji soruyorsa ve adayın profilinde yoksa, '0', 'Yok', 'None' veya 'Hayır' yönündeki en düşük seçeneği seç.
            3. Eğer sayı soruluyorsa sadece rakam döndür (örn: 3 veya 0).
            4. Asla açıklama, tırnak işareti, markdown formatı veya fazladan kelime ekleme. Sadece cevabı ver.
            """
            try:
                res = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                llm_ans = res.text.strip().replace('"', '').replace("'", "")
                if valid_options:
                    # En yakın eşleşen seçeneği bul
                    return self._match_option(valid_options, [llm_ans], default_index=0)
                return llm_ans
            except Exception as e:
                logger.debug(f"Gemini form yanıtı hatası: {e}")

        # -------------------------------------------------------------
        # 5. Son Güvenli Fallback
        # -------------------------------------------------------------
        if valid_options:
            # Evet / Yes seçeneği varsa onu tercih et
            return self._match_option(valid_options, ["evet", "yes", "true"], default_index=0)

        if any(w in q_lower for w in ["kaç yıl", "how many years", "deneyim yılı", "years of experience"]):
            return "0"

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
