import os
import re
import ssl
import smtplib
import logging
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import Optional, List, Dict, Any

from src.utils.config import GMAIL_USER, GMAIL_APP_PASSWORD, CV_PATH

logger = logging.getLogger(__name__)

# Yaygın İK / Kariyer e-posta filtreleri
HR_KEYWORDS = ["ik", "hr", "kariyer", "career", "job", "apply", "talent", "recruitment", "basvuru"]
EXCLUDED_DOMAINS = ["example.com", "w3.org", "schema.org", "github.com", "sentry.io"]


def extract_emails(text: str) -> List[str]:
    """
    İlan metninden veya HTML içerikten geçerli e-posta adreslerini ayıklar.
    İK ve başvuru odaklı e-postaları önceliklendirir.
    """
    if not text:
        return []

    # Standart e-posta regex kalıbı
    pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    found = re.findall(pattern, text)

    valid_emails = []
    for email in set(found):
        email_clean = email.strip(".,;:()[]{}<>\"'").lower()
        if not email_clean or "@" not in email_clean:
            continue

        domain = email_clean.split("@")[-1]
        if any(exc in domain for exc in EXCLUDED_DOMAINS):
            continue

        # Uzantı kontrolü (resim/kod uzantısı olmasın: örn .png, .jpg)
        if any(email_clean.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"]):
            continue

        valid_emails.append(email_clean)

    # İK anahtar kelimelerini içerenleri en başa al
    def sort_key(e: str):
        prefix = e.split("@")[0]
        return 0 if any(k in prefix for k in HR_KEYWORDS) else 1

    valid_emails.sort(key=sort_key)
    return valid_emails


class EmailClient:
    """
    Gmail SMTP üzerinden profesyonel iş başvurusu gönderici istemcisi.
    """

    def __init__(
        self,
        user: Optional[str] = None,
        app_password: Optional[str] = None,
        cv_path: Optional[Path] = None,
        smtp_host: str = "smtp.gmail.com",
        smtp_port: int = 465
    ):
        self.user = user or GMAIL_USER
        self.app_password = app_password or GMAIL_APP_PASSWORD
        self.cv_path = cv_path or CV_PATH
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    def is_configured(self) -> bool:
        """Kullanıcı adı ve şifrenin tanımlı olup olmadığını kontrol eder."""
        return bool(self.user and self.app_password and len(self.app_password.replace(" ", "")) >= 16)

    def send_application(
        self,
        to_email: str,
        subject: str,
        body: str,
        attachment_path: Optional[Path] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Kişiselleştirilmiş başvuru e-postasını ve ekteki PDF CV'yi gönderir.
        dry_run=True ise ağ çağrısı yapmadan başarılı döner.
        """
        if not to_email or "@" not in to_email:
            return {"success": False, "reason": f"Geçersiz alıcı e-posta adresi: {to_email}"}

        if dry_run:
            logger.info(f"[DRY-RUN] E-posta gönderimi simüle edildi: {to_email} | Konu: {subject}")
            return {"success": True, "dry_run": True, "message": f"[DRY-RUN] {to_email} adresine e-posta hazırlandı ancak gönderilmedi."}

        if not self.is_configured():
            return {
                "success": False,
                "reason": "GMAIL_APP_PASSWORD tanımlanmamış. Lütfen .env dosyasına Gmail Uygulama Şifrenizi ekleyin."
            }

        # Dosya eki belirleme
        target_cv = attachment_path or self.cv_path
        if not target_cv or not target_cv.exists():
            return {"success": False, "reason": f"CV dosyası bulunamadı: {target_cv}"}

        msg = MIMEMultipart()
        msg["From"] = f"Taylan Özgür Özdemir <{self.user}>"
        msg["To"] = to_email
        msg["Subject"] = subject

        # E-posta gövdesi (UTF-8 plain text)
        msg.attach(MIMEText(body, "plain", "utf-8"))

        # PDF CV eki
        try:
            with open(target_cv, "rb") as f:
                attach = MIMEApplication(f.read(), _subtype="pdf")
                attach.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename="CV_Taylan_Ozgur_Ozdemir.pdf"
                )
                msg.attach(attach)
        except Exception as e:
            return {"success": False, "reason": f"CV eki eklenirken hata: {e}"}

        # SMTP Gönderimi
        try:
            context = ssl.create_default_context()
            # Şifredeki boşlukları temizle (Google 16 haneli şifreyi 4x4 blok verir)
            clean_pwd = self.app_password.replace(" ", "")

            with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, context=context, timeout=30) as server:
                server.login(self.user, clean_pwd)
                server.send_message(msg)

            logger.info(f"[OK] Başvuru e-postası başarıyla gönderildi: {to_email}")
            return {"success": True, "dry_run": False, "message": f"{to_email} adresine başvuru e-postası gönderildi."}

        except smtplib.SMTPAuthenticationError:
            return {
                "success": False,
                "reason": "Gmail SMTP kimlik doğrulama hatası! Lütfen App Password (Uygulama Şifresi) doğruluğunu kontrol edin."
            }
        except Exception as e:
            logger.error(f"E-posta gönderim hatası: {e}")
            return {"success": False, "reason": f"SMTP Hatası: {e}"}
