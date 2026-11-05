import re
import json
import logging
from typing import Dict, Any, Optional, List

from src.core.application_generator import ApplicationGenerator

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# Hızlı Regex Kalıpları (Fast-Path)
# ──────────────────────────────────────────────

REJECTION_PATTERNS = [
    # İngilizce
    r"regret to inform",
    r"unfortunately",
    r"not moving forward",
    r"decided to pursue other",
    r"decided not to proceed",
    r"will not be moving forward",
    r"not be able to offer",
    r"unsuccessful in this occasion",
    r"wish you the best in your job search",
    r"position has been filled",
    r"high volume of applicants.*not.*selected",
    # Türkçe
    r"olumsuz",
    r"başka adaylarla devam",
    r"üzülerek bildiririz",
    r"maalesef",
    r"uygun bulunmamıştır",
    r"sürecinizi sonlandırmak",
    r"olumlu değerlendiremedik",
    r"farklı bir adayla devam",
    r"başka bir adayla ilerleme",
]

INTERVIEW_PATTERNS = [
    # İngilizce
    r"interview invitation",
    r"invitation to interview",
    r"schedule an interview",
    r"schedule a time to chat",
    r"technical interview",
    r"coding challenge",
    r"assessment",
    r"codesignal",
    r"hackerrank",
    r"take-home",
    r"phone screen",
    r"video interview",
    r"next steps in the interview",
    r"speak with our team",
    # Türkçe
    r"mülakat daveti",
    r"görüşme daveti",
    r"teknik mülakat",
    r"online mülakat",
    r"vaka çalışması",
    r"kodlama testi",
    r"görüşme talebi",
    r"sizinle görüşmek",
    r"tanışma toplantısı",
    r"mülakat planlama",
]

RECEIVED_PATTERNS = [
    # İngilizce
    r"application received",
    r"thank you for applying",
    r"received your application",
    r"we have received your application",
    r"application confirmation",
    # Türkçe
    r"başvurunuz alınmıştır",
    r"başvurunuz bize ulaştı",
    r"başvurunuz için teşekkür",
    r"başvurunuzu aldık",
]


class EmailClassifier:
    """
    Gelen başvuru e-postalarını Regex + LLM (Gemini) hibrit mimarisiyle
    'Mülakat', 'Reddedildi', 'Başvuruldu' veya 'İlgisiz' olarak sınıflandırır.
    """

    def __init__(self, generator: Optional[ApplicationGenerator] = None):
        self.generator = generator or ApplicationGenerator()

    def classify_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Tek bir e-postayı sınıflandırır.
        email_data: {'from': str, 'subject': str, 'date': str, 'body': str}
        """
        from_text = email_data.get("from", "")
        subject = email_data.get("subject", "")
        body = email_data.get("body", "")

        full_content = f"{subject} {body}".lower()

        # 1. Aşama: Hızlı Regex Taraması (Sıfır Maliyet & Hızlı)
        # Önce Mülakat / Davet kontrolü (En yüksek öncelik)
        for pattern in INTERVIEW_PATTERNS:
            if re.search(pattern, full_content, re.IGNORECASE):
                return {
                    "status": "Mülakat",
                    "confidence": 0.95,
                    "reason": f"Mülakat anahtar kalıbı eşleşti: '{pattern}'",
                    "extracted_company": self._guess_company_name(from_text, subject)
                }

        # İkinci olarak Reddedilme kontrolü
        for pattern in REJECTION_PATTERNS:
            if re.search(pattern, full_content, re.IGNORECASE):
                return {
                    "status": "Reddedildi",
                    "confidence": 0.95,
                    "reason": f"Reddetme anahtar kalıbı eşleşti: '{pattern}'",
                    "extracted_company": self._guess_company_name(from_text, subject)
                }

        # Üçüncü olarak Başvuru Alındı (Acknowledgement) kontrolü
        for pattern in RECEIVED_PATTERNS:
            if re.search(pattern, full_content, re.IGNORECASE):
                return {
                    "status": "Başvuruldu",
                    "confidence": 0.90,
                    "reason": f"Başvuru alındı onayı eşleşti: '{pattern}'",
                    "extracted_company": self._guess_company_name(from_text, subject)
                }

        # 2. Aşama: LLM Fallback (Gemini) – Eğer belirgin kalıp yoksa ve potansiyel başvuruysa
        if self._is_potential_recruitment_email(from_text, subject):
            llm_result = self._classify_with_llm(from_text, subject, body)
            if llm_result:
                return llm_result

        return {
            "status": "İlgisiz",
            "confidence": 0.8,
            "reason": "Başvuru sonucu tespit edilemedi (bülten, tanıtım veya alakasız e-posta).",
            "extracted_company": ""
        }

    def _guess_company_name(self, from_text: str, subject: str) -> str:
        """From başlığından veya konudan şirket adını tahmin eder."""
        # 'From: Company Name <hr@company.com>' -> 'Company Name'
        if "<" in from_text:
            display_name = from_text.split("<")[0].strip(' "\'')
            # Eğer display name 'Careers', 'Team', 'No-reply' gibi jenerik değilse al
            if display_name and not any(w in display_name.lower() for w in ["noreply", "no-reply", "notification", "team"]):
                return display_name

        # Konudan çıkarma: 'Your application to Google' veya 'Peak Games Başvurusu'
        m = re.search(r'(?:to|at|for|şirketi|firması)\s+([A-Za-z0-9\sğüşıöçĞÜŞİÖÇ]+?)(?:\s+(?:team|careers|recruiting|başvuru|ilan|$))', subject, re.IGNORECASE)
        if m:
            return m.group(1).strip()

        return ""

    def _is_potential_recruitment_email(self, from_text: str, subject: str) -> bool:
        """E-postanın kariyer/iş ilanı ile alakalı olup olmadığını kabaca filtreler."""
        keywords = ["career", "recruit", "job", "application", "başvuru", "ik", "talent", "greenhouse", "lever", "workday", "smartrecruiters"]
        combined = f"{from_text} {subject}".lower()
        return any(k in combined for k in keywords)

    def _classify_with_llm(self, from_text: str, subject: str, body: str) -> Optional[Dict[str, Any]]:
        """Gemini LLM kullanarak karmaşık e-postaları sınıflandırır."""
        if not self.generator.client:
            return None

        prompt = f"""
        Aşağıdaki iş başvurusu veya şirket e-postasını analiz et.
        
        Kimden: {from_text}
        Konu: {subject}
        İçerik Özeti: {body[:1500]}
        
        GÖREV:
        1. Bu e-postanın bir iş başvurusu süreciyle ilgili olup olmadığını değerlendir.
        2. Durumu tam olarak şu 4 seçenekten birine ata:
           - "Mülakat": Aday teknik teste, mülakata, görüşmeye davet edildiyse veya sonraki aşamaya geçtiyse.
           - "Reddedildi": Başvuru reddedildiyse, olumsuz sonuçlandıysa veya pozisyon kapandıysa.
           - "Başvuruldu": Sadece "başvurunuz elimize ulaştı" tarzı ilk onay e-postası ise.
           - "İlgisiz": Bülten, reklam, spam, iş arama tavsiyesi veya alakasız içerikse.
        3. E-postayı gönderen şirketin adını belirle.
        
        YANIT FORMATI:
        Sadece geçerli bir JSON nesnesi döndür:
        {{
            "status": "Mülakat" | "Reddedildi" | "Başvuruldu" | "İlgisiz",
            "company": "Şirket Adı",
            "confidence": 0.85,
            "reason": "Kısa açıklama"
        }}
        """

        try:
            response = self.generator.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            text = response.text.strip()
            # JSON markdown bloklarını temizle
            if "```" in text:
                text = re.sub(r'```(?:json)?\s*', '', text).strip('` \n')
            data = json.loads(text)
            if isinstance(data, dict) and "status" in data:
                return {
                    "status": data.get("status", "İlgisiz"),
                    "confidence": float(data.get("confidence", 0.8)),
                    "reason": data.get("reason", "LLM sınıflandırması"),
                    "extracted_company": data.get("company", "")
                }
        except Exception as e:
            logger.warning(f"LLM e-posta sınıflandırma hatası: {e}")

        return None
