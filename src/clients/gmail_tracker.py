import os
import ssl
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Any, Optional

from src.utils.config import GMAIL_USER, GMAIL_APP_PASSWORD

logger = logging.getLogger(__name__)


def _decode_mime_words(raw_header: Optional[str]) -> str:
    """MIME ile kodlanmış başlıkları (örn: UTF-8 / Base64) okunabilir metne dönüştürür."""
    if not raw_header:
        return ""
    try:
        decoded_fragments = decode_header(raw_header)
        header_text = []
        for fragment, encoding in decoded_fragments:
            if isinstance(fragment, bytes):
                header_text.append(fragment.decode(encoding or "utf-8", errors="replace"))
            else:
                header_text.append(str(fragment))
        return "".join(header_text).strip()
    except Exception:
        return str(raw_header)


def _extract_body_text(msg: email.message.Message) -> str:
    """E-posta mesajının gövdesinden salt metin (plain text) içeriği ayıklar."""
    body_parts = []
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disp = str(part.get("Content-Disposition", ""))

            # Ek dosyaları atla
            if "attachment" in content_disp:
                continue

            if content_type == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    body_parts.append(payload.decode(charset, errors="replace"))
            elif content_type == "text/html" and not body_parts:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    # HTML etiketlerini kaba bir şekilde temizle
                    import re
                    clean_text = re.sub(r'<[^>]+>', ' ', payload.decode(charset, errors="replace"))
                    body_parts.append(clean_text)
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            body_parts.append(payload.decode(charset, errors="replace"))

    full_body = "\n".join(body_parts)
    # Birden çok boşluğu ve satır sonunu normalize et
    return " ".join(full_body.split())


class GmailTracker:
    """
    Gmail IMAP (SSL) üzerinden başvuru e-posta yanıtlarını tarayan istemci.
    """

    def __init__(
        self,
        user: Optional[str] = None,
        app_password: Optional[str] = None,
        imap_host: str = "imap.gmail.com",
        imap_port: int = 993
    ):
        self.user = user or GMAIL_USER
        self.app_password = app_password or GMAIL_APP_PASSWORD
        self.imap_host = imap_host
        self.imap_port = imap_port

    def is_configured(self) -> bool:
        """Kullanıcı adı ve şifrenin tanımlı olup olmadığını kontrol eder."""
        return bool(self.user and self.app_password and len(self.app_password.replace(" ", "")) >= 16)

    def fetch_recent_emails(self, days: int = 30, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Son N güne ait gelen kutusu (INBOX) e-postalarını çeker.
        """
        if not self.is_configured():
            logger.warning("Gmail App Password yapılandırılmamış. E-posta takibi atlanıyor.")
            return []

        clean_pwd = self.app_password.replace(" ", "")
        emails_list = []
        mail = None

        try:
            context = ssl.create_default_context()
            mail = imaplib.IMAP4_SSL(self.imap_host, self.imap_port, ssl_context=context)
            mail.login(self.user, clean_pwd)
            mail.select("INBOX", readonly=True)

            # Tarih arama filtresi (IMAP SINCE formatı: 01-Jan-2024)
            since_date = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
            search_criterion = f'(SINCE "{since_date}")'

            status, msg_ids = mail.search(None, search_criterion)
            if status != "OK" or not msg_ids or not msg_ids[0]:
                return []

            id_list = msg_ids[0].split()
            # En son gelen mailleri öncelikle almak için tersine sırala
            id_list = id_list[::-1][:limit]

            for msg_id in id_list:
                try:
                    res, data = mail.fetch(msg_id, "(RFC822)")
                    if res != "OK" or not data:
                        continue

                    raw_email = data[0][1]
                    parsed_msg = email.message_from_bytes(raw_email)

                    from_hdr = _decode_mime_words(parsed_msg.get("From"))
                    subject_hdr = _decode_mime_words(parsed_msg.get("Subject"))
                    date_hdr = _decode_mime_words(parsed_msg.get("Date"))
                    body_text = _extract_body_text(parsed_msg)

                    emails_list.append({
                        "id": msg_id.decode("utf-8", errors="ignore"),
                        "from": from_hdr,
                        "subject": subject_hdr,
                        "date": date_hdr,
                        "body": body_text[:2000]  # İlk 2000 karakter analiz için yeterlidir
                    })

                except Exception as item_err:
                    logger.debug(f"E-posta ayrıştırma hatası (ID {msg_id}): {item_err}")
                    continue

            return emails_list

        except imaplib.IMAP4.error as auth_err:
            logger.error(f"IMAP Giriş Hatası: {auth_err}")
            return []
        except Exception as e:
            logger.error(f"Gmail IMAP bağlantı hatası: {e}")
            return []
        finally:
            if mail:
                try:
                    mail.close()
                except Exception:
                    pass
                try:
                    mail.logout()
                except Exception:
                    pass
