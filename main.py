# main.py – Job Radar v0.7: Otonom Başvuru & Gmail Takip Pipeline

import time
import random
import re
from pathlib import Path

from src.clients.rss_sources import fetch_all_jobs as fetch_rss_jobs
from src.clients.kariyer_scraper import fetch_all_kariyer_jobs
from src.clients.jsearch_client import fetch_all_jsearch_jobs
from src.clients.linkedin_scraper import fetch_all_linkedin_jobs
from src.core.scorer import score_job
from src.clients.sheets_client import (
    append_jobs, clear_sheet, fix_sheet,
    get_eligible_jobs_for_application, update_job_status, get_applied_jobs
)
from src.clients.easy_apply_client import LinkedInEasyApplyClient
from src.clients.email_client import EmailClient, extract_emails
from src.clients.gmail_tracker import GmailTracker
from src.core.email_classifier import EmailClassifier
from src.core.application_generator import ApplicationGenerator
from src.core.cv_engine import CVEngine
from src.utils.config import (
    MIN_APPLICATION_SCORE, MAX_APPLICATION_SCORE, MAX_APPLICATIONS_PER_RUN,
    APPLICATION_DELAY_RANGE, CV_PATH, GMAIL_USER, GMAIL_APP_PASSWORD
)
from src.utils.logger import setup_logger

# Setup logger and fix Windows encoding
logger = setup_logger()


def print_job_summary(job):
    """Tek bir ilanın özetini konsola yazdırır."""
    score = job.get("total_score", 0)
    restricted = job.get("restricted", False)

    if restricted:
        indicator = "[XXX]"
    elif score >= 3.5:
        indicator = "[+++]"
    elif score >= 2.0:
        indicator = "[++ ]"
    else:
        indicator = "[+  ]"

    print(f"  {indicator} [{score:.1f}] {job['title']}")
    print(f"      Firma: {job.get('company', '-') or '-'}")
    print(f"      Alan: {job.get('field', '-')} | Lokasyon: {job.get('location', '-')} | Level: {job.get('level', '-')}")
    print(f"      Kaynak: {job.get('source', '-')}")
    if restricted:
        print(f"      ** KISITLI (ulke/vize) - Atlanacak **")
    print()


def show_menu():
    """İnteraktif menüyü gösterir ve kullanıcı seçimini döndürür."""
    print()
    print("=" * 55)
    print("  Job Radar v0.7 - Otonom Başvuru & Takip Sistemi")
    print("=" * 55)
    print()
    print("  [TARAMA & VERİ]")
    print("  1. Tam çalıştır (Tüm kaynakları tara -> Sheets'e yaz)")
    print("  2. Temiz çalıştır (SİL + Tüm kaynakları tara)")
    print("  3. API'siz çalıştır (LinkedIn + RSS, JSearch yok)")
    print("  4. Sadece API (JSearch)")
    print("  5. Dry Run (Konsola yazdır, Sheets'e yazma)")
    print("  6. Tabloyu Düzelt (Başlık/Sütun/Tarih/Smart Chips)")
    print()
    print("  [OTONOM BAŞVURU & TAKİP]")
    print("  7. LinkedIn Oturumu Aç (Tek seferlik session kaydet)")
    print("  8. Otonom Başvuru Yap (Easy Apply + E-Posta | Onaylı)")
    print("  9. E-posta Yanıtlarını Kontrol Et (Gmail IMAP Sync)")
    print("  10. Çıkış")
    print()

    valid_choices = [str(i) for i in range(1, 11)]
    while True:
        selection = input("  Seçiminiz (1-10): ").strip()
        if selection in valid_choices:
            return selection
        print("  Geçersiz seçim, lütfen tekrar deneyin.")


def run_pipeline(dry_run=False, clear=False, sources=None):
    """Ana veri toplama ve skorlama hattı."""
    if sources is None:
        sources = {"linkedin", "kariyer", "jsearch", "rss"}

    print()
    print("=" * 60)
    print("  Job Radar - Çok Kaynaklı Skor Pipeline")
    print(f"  Kaynaklar: {', '.join(sorted(sources))}")
    print("=" * 60)

    # -- 0. Sheet temizleme --
    if clear and not dry_run:
        print("\n[INFO] Eski veriler temizleniyor...\n")
        clear_sheet()

    # -- 1. İlanları çek --
    all_jobs = []
    fetch_map = {
        "linkedin": fetch_all_linkedin_jobs,
        "kariyer": fetch_all_kariyer_jobs,
        "jsearch": fetch_all_jsearch_jobs,
        "rss": fetch_rss_jobs
    }

    for name, fetch_func in fetch_map.items():
        if name in sources:
            all_jobs.extend(fetch_func())

    if not all_jobs:
        print("[HATA] Hiç ilan bulunamadı.")
        return

    # -- 2. İlanları skorla --
    print("=" * 60)
    print("[INFO] İlanlar skorlanıyor...\n")
    scored_jobs = [score_job(job) for job in all_jobs]

    # -- 3. Sırala (Skora göre azalan) --
    scored_jobs.sort(key=lambda j: j.get("total_score", 0), reverse=True)

    # -- 4. Kısıtlı ve geçerli ayrımı --
    valid_jobs = [j for j in scored_jobs if not j.get("restricted", False)]
    restricted_jobs = [j for j in scored_jobs if j.get("restricted", False)]

    # -- 5. Önizleme --
    print("=" * 60)
    print(f"  EN İYİ İLANLAR (Toplam {len(valid_jobs)} geçerli, {len(restricted_jobs)} kısıtlı)")
    print("=" * 60)

    display_count = min(25, len(valid_jobs))
    for job in valid_jobs[:display_count]:
        print_job_summary(job)

    if len(valid_jobs) > display_count:
        print(f"  ... ve {len(valid_jobs) - display_count} ilan daha.\n")

    # -- 6. İstatistikler --
    high_score = [j for j in valid_jobs if j.get("total_score", 0) >= 3.5]
    mid_score = [j for j in valid_jobs if 2.0 <= j.get("total_score", 0) < 3.5]
    low_score = [j for j in valid_jobs if j.get("total_score", 0) < 2.0]

    source_counts = {}
    for j in valid_jobs:
        src = j.get("source", "?")
        source_counts[src] = source_counts.get(src, 0) + 1

    print("=" * 60)
    print("  ÖZET")
    print(f"     [+++] Yüksek skor (>=3.5): {len(high_score)} ilan")
    print(f"     [++ ] Orta skor (2.0-3.5): {len(mid_score)} ilan")
    print(f"     [+  ] Düşük skor (<2.0):   {len(low_score)} ilan")
    print(f"     [XXX] Kısıtlı (atlanan):   {len(restricted_jobs)} ilan")
    print()
    print("  KAYNAK BAZLI:")
    for src, count in sorted(source_counts.items(), key=lambda x: -x[1]):
        print(f"     {src}: {count} ilan")
    print("=" * 60)

    # -- 7. Google Sheets'e yaz --
    if dry_run:
        print("\n[!] DRY RUN modu - Google Sheets'e yazılmadı.")
    else:
        print("\n[INFO] Google Sheets'e yazılıyor...\n")
        added, duplicates = append_jobs(valid_jobs)
        print(f"\n  [OK] Eklenen: {added} | [DUP] Duplicate: {duplicates}")
        
        # -- 8. Otomatik Tablo Düzeltme --
        print("\n[INFO] Tablo otomatik düzeltiliyor (Format/Smart Chips)...\n")
        fix_sheet()

    print("\n[BİTTİ] Tamamlandı!\n")


def run_linkedin_login():
    """LinkedIn için tarayıcı açar ve tek seferlik session kaydeder."""
    client = LinkedInEasyApplyClient()
    client.save_session_interactively()


def run_autonomous_applications():
    """
    Otonom Başvuru Yürütücüsü (LinkedIn Easy Apply + E-Posta).
    Human-in-the-loop: Kullanıcı onayıyla başvuruları tamamlar.
    """
    print("\n" + "=" * 60)
    print("  Otonom Başvuru Pipeline (Human-in-the-Loop)")
    print("=" * 60)

    # CV Kontrolü
    if not CV_PATH.exists():
        print(f"\n[HATA] CV dosyası bulunamadı: {CV_PATH}")
        print("Lütfen kök dizine 'cv.pdf' dosyanızı ekleyin.")
        return

    print(f"  [BİLGİ] Kullanılan CV: {CV_PATH}")
    print(f"  [BİLGİ] Varsayılan Skor Aralığı: {MIN_APPLICATION_SCORE} - {MAX_APPLICATION_SCORE}")
    print(f"  [BİLGİ] Güvenlik Kotası (Oturum başına): Maks {MAX_APPLICATIONS_PER_RUN} başvuru")
    print("=" * 60)

    # Kullanıcı isterse anlık özel skor aralığı belirleyebilir (örn: 3.0-4.5 veya sadece ENTER)
    range_input = input(f"  Başvurulacak Skor Aralığı [Min-Maks, varsayılan {MIN_APPLICATION_SCORE}-{MAX_APPLICATION_SCORE}]: ").strip()
    min_score = MIN_APPLICATION_SCORE
    max_score = MAX_APPLICATION_SCORE
    if range_input:
        try:
            # "3-4.5", "3 4.5" veya "3.0" formatlarını destekle
            parts = [p.strip().replace(",", ".") for p in re.split(r'[-–\s]+', range_input) if p.strip()]
            if len(parts) == 1:
                min_score = float(parts[0])
            elif len(parts) >= 2:
                min_score = float(parts[0])
                max_score = float(parts[1])
        except ValueError:
            print(f"  [UYARI] Geçersiz giriş, varsayılan ({min_score}-{max_score}) kullanılıyor.")

    if min_score > max_score:
        min_score, max_score = max_score, min_score

    print(f"  [FİLTRE] Hedef Skor Aralığı: {min_score:.1f} <= Skor <= {max_score:.1f}")

    # Başvuruya uygun ilanları Sheets'ten çek
    eligible_jobs = get_eligible_jobs_for_application(min_score=min_score, max_score=max_score)
    if not eligible_jobs:
        print("\n  [BİLGİ] Başvuruya uygun yeni ilan bulunamadı.")
        print(f"  (Tabloda {min_score:.1f} - {max_score:.1f} aralığındaki tüm ilanlara başvurulmuş olabilir).")
        return

    print()
    print("  Hedef Başvuru Kanalı:")
    print("    1. Tümü (LinkedIn Easy Apply + E-Posta İlanları) [varsayılan]")
    print("    2. Sadece LinkedIn Easy Apply")
    print("    3. Sadece E-Posta İlanları")
    channel_choice = input("  Kanal Seçimi (1-3) [varsayılan 1]: ").strip()

    if channel_choice == "2":
        eligible_jobs = [j for j in eligible_jobs if "linkedin.com" in j["link"].lower()]
        print(f"  [FİLTRE] Sadece LinkedIn ilanları seçildi ({len(eligible_jobs)} ilan).")
    elif channel_choice == "3":
        eligible_jobs = [j for j in eligible_jobs if "linkedin.com" not in j["link"].lower()]
        print(f"  [FİLTRE] Sadece Harici/E-posta ilanları seçildi ({len(eligible_jobs)} ilan).")

    if not eligible_jobs:
        print("\n  [BİLGİ] Seçilen kanal filtresine uygun ilan bulunamadı.")
        return

    # Skora göre azalan sırala (en yüksek skorlu ilanlar ilk sıraya)
    eligible_jobs.sort(key=lambda x: x.get("score", 0), reverse=True)
    target_jobs = eligible_jobs[:MAX_APPLICATIONS_PER_RUN]

    print(f"\n  [BULUNDU] {len(eligible_jobs)} adet başvuruya uygun ilan mevcut.")
    print(f"  [KOTA] Bu oturumda en yüksek skorlu {len(target_jobs)} ilan işlenecek.\n")

    easy_client = LinkedInEasyApplyClient(cv_path=CV_PATH)
    email_client = EmailClient(cv_path=CV_PATH)
    generator = ApplicationGenerator()
    cv_engine = CVEngine()

    successful_count = 0

    for idx, job in enumerate(target_jobs, 1):
        print("\n" + "-" * 60)
        print(f"  [{idx}/{len(target_jobs)}] İlan: {job['title']}")
        print(f"  Firma: {job['company']} | Alan: {job['field']} | Skor: {job['score']}")
        print(f"  Link: {job['link']}")
        print("-" * 60)

        # Dinamik CV Çözümleme (Mod 1 Katalog veya Mod 2 Sıcak JIT PDF)
        selected_cv, cv_mode, cv_reason = cv_engine.resolve_cv_for_job(job)
        print(f"  [CV STRATEJİSİ] {cv_mode} -> {selected_cv.name}")
        print(f"                  Gerekçe: {cv_reason}")

        link = job.get("link", "").lower()
        applied = False

        # --- Kanal 1: LinkedIn Easy Apply ---
        if "linkedin.com" in link:
            if not easy_client.has_valid_session():
                print("  [UYARI] LinkedIn session dosyası bulunamadı. Lütfen önce Menü 7'den oturum açın.")
                continue

            print("  [İŞLEM] LinkedIn Easy Apply deneniyor...")
            result = easy_client.apply_to_job(job["link"], dry_run=False, human_in_the_loop=True, cv_path=selected_cv)

            if result.get("success") and not result.get("dry_run"):
                print(f"  [BAŞARILI] {result.get('message')}")
                update_job_status(job["row_idx"], "Başvuruldu")
                applied = True
                successful_count += 1
            elif result.get("is_expired"):
                print(f"  [SÜRE BİTTİ] {result.get('reason')}")
                update_job_status(job["row_idx"], "Süre Bitti")
                print("  [GÜNCELLENDİ] Tablodaki durum 'Süre Bitti' olarak kaydedildi.")
            else:
                print(f"  [ATLANDI/İPTAL] {result.get('reason', 'Başvuru tamamlanamadı.')}")

        # --- Kanal 2: İK E-Posta Başvurusu ---
        else:
            print("  [BİLGİ] Harici ilan. İK e-postası kontrol ediliyor...")
            extracted = extract_emails(job.get("title", "") + " " + job.get("company", ""))
            to_email = extracted[0] if extracted else None

            if to_email:
                print(f"  [AI] Kişiselleştirilmiş ön yazı üretiliyor ({job['company']})...")
                app_data = generator.generate_email_application(job["title"], job["company"])

                print("\n  [ÖNİZLEME]")
                print(f"  Alıcı: {to_email}")
                print(f"  Konu : {app_data['subject']}")
                print(f"  Metin: {app_data['body'][:250]}...\n")

                confirm = input("  Bu e-posta başvurusu gönderilsin mi? (E/H) [varsayılan E]: ").strip().lower()
                if confirm in ("", "e", "evet", "y", "yes"):
                    send_res = email_client.send_application(
                        to_email=to_email,
                        subject=app_data["subject"],
                        body=app_data["body"],
                        attachment_path=selected_cv
                    )
                    if send_res.get("success"):
                        print(f"  [BAŞARILI] {send_res.get('message')}")
                        update_job_status(job["row_idx"], "Başvuruldu")
                        applied = True
                        successful_count += 1
                    else:
                        print(f"  [HATA] E-posta gönderilemedi: {send_res.get('reason')}")
                else:
                    print("  [İPTAL] Kullanıcı e-posta gönderimini iptal etti.")
            else:
                print("  [ATLANDI] İlanda başvuru e-postası bulunamadı.")

        # Başvuru yapıldıysa human-like bekleme (LinkedIn güvenlik önlemi)
        if applied and idx < len(target_jobs):
            delay = random.randint(APPLICATION_DELAY_RANGE[0], APPLICATION_DELAY_RANGE[1])
            print(f"  [GÜVENLİK BEKLEMESİ] {delay} saniye bekleniyor...")
            for s in range(delay, 0, -5):
                print(f"    Kalan süre: {s}s...", end="\r")
                time.sleep(min(5, s))
            print("    Hazır.                             ")

    print("\n" + "=" * 60)
    print(f"  Otonom Başvuru Oturumu Tamamlandı! Başarılı Başvuru: {successful_count}")
    print("=" * 60 + "\n")


def run_gmail_sync():
    """
    Gmail IMAP kutusunu tarar, gelen e-postaları sınıflandırır
    ve Google Sheets'teki ilgili ilanların Durumunu günceller.
    """
    print("\n" + "=" * 60)
    print("  Gmail Yanıt Takip Motoru (IMAP Sync)")
    print("=" * 60)

    tracker = GmailTracker()
    if not tracker.is_configured():
        print("\n  [UYARI] Gmail Uygulama Şifresi (GMAIL_APP_PASSWORD) tanımlanmamış.")
        print("  Lütfen .env dosyasına GMAIL_USER ve 16 haneli GMAIL_APP_PASSWORD ekleyin.")
        return

    print("  [1/3] Son 30 güne ait e-postalar Gmail'den çekiliyor...")
    emails = tracker.fetch_recent_emails(days=30, limit=50)
    print(f"  [BİLGİ] {len(emails)} adet e-posta tarandı.")

    if not emails:
        print("  Gelen kutusunda taranacak e-posta bulunamadı.")
        return

    print("  [2/3] Google Sheets'teki mevcut başvurular okunuyor...")
    applied_jobs = get_applied_jobs()
    print(f"  [BİLGİ] Tabloda {len(applied_jobs)} adet aktif/başvurulmuş kayıt bulundu.")

    print("  [3/3] E-postalar sınıflandırılıyor ve eşleştiriliyor...\n")
    classifier = EmailClassifier()
    updated_count = 0

    for em in emails:
        result = classifier.classify_email(em)
        status = result.get("status")

        # Sadece Mülakat veya Reddedildi sonuçları tabloyu günceller
        if status in ("Mülakat", "Reddedildi"):
            detected_company = result.get("extracted_company", "").lower()
            reason = result.get("reason", "")
            subject = em.get("subject", "")

            # Tablodaki şirketlerle eşleştir
            matched_job = None
            if detected_company and len(detected_company) >= 3:
                for job in applied_jobs:
                    job_comp = job.get("company", "").lower()
                    if detected_company in job_comp or job_comp in detected_company:
                        matched_job = job
                        break

            # Eğer tam şirket eşleşmesi yoksa, e-posta konu veya metninde geçen şirket adlarına bak
            if not matched_job:
                for job in applied_jobs:
                    job_comp = job.get("company", "").lower()
                    if len(job_comp) >= 4 and job_comp in em.get("body", "").lower():
                        matched_job = job
                        break

            if matched_job:
                row_idx = matched_job["row_idx"]
                curr_status = matched_job["status"]

                if curr_status != status:
                    print(f"  [EŞLEŞTİ] Firma: {matched_job['company']} -> Yeni Durum: [{status}]")
                    print(f"            Neden: {reason}")
                    update_job_status(row_idx, status)
                    matched_job["status"] = status  # Yerel kopyayı güncelle
                    updated_count += 1
            else:
                print(f"  [BİLGİ] Tespit Edilen Sonuç: [{status}] - {result.get('extracted_company', 'Firma Bilinmiyor')}")
                print(f"          Konu: {subject[:60]}")

    print("\n" + "=" * 60)
    print(f"  Gmail Senkronizasyonu Tamamlandı! Güncellenen Satır: {updated_count}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    menu_choice = show_menu()

    actions = {
        "1": lambda: run_pipeline(dry_run=False, clear=False),
        "2": lambda: run_pipeline(dry_run=False, clear=True),
        "3": lambda: run_pipeline(dry_run=False, sources={"linkedin", "kariyer", "rss"}),
        "4": lambda: run_pipeline(dry_run=False, sources={"jsearch"}),
        "5": lambda: run_pipeline(dry_run=True, clear=False),
        "6": lambda: (print("\n[INFO] Tablo düzeltiliyor...\n"), fix_sheet(), print("\n[BİTTİ] Tamamlandı!\n")),
        "7": run_linkedin_login,
        "8": run_autonomous_applications,
        "9": run_gmail_sync,
        "10": lambda: print("\nÇıkış yapılıyor...\n")
    }

    if menu_choice in actions:
        actions[menu_choice]()
