import time
import os
import re
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from playwright.sync_api import sync_playwright, BrowserContext, Page, Locator

from src.core.application_generator import ApplicationGenerator
from src.utils.config import CV_PATH
from src.utils.text_norm import normalize_tr

logger = logging.getLogger(__name__)

SESSION_STATE_FILE = Path("linkedin_state.json")
DEFAULT_CV_PATH = CV_PATH


class LinkedInEasyApplyClient:
    """
    LinkedIn Easy Apply (Kolay Başvuru) Form Otomasyon İstemcisi.
    Playwright ve AI destekli form yanıtlayıcı kullanarak başvuruları tamamlar.
    """

    def __init__(
        self,
        session_file: Path = SESSION_STATE_FILE,
        cv_path: Path = DEFAULT_CV_PATH,
        app_generator: Optional[ApplicationGenerator] = None
    ):
        self.session_file = session_file
        self.cv_path = cv_path
        self.generator = app_generator or ApplicationGenerator()

    def save_session_interactively(self):
        """
        Kullanıcının tarayıcı üzerinden LinkedIn'e tek seferlik manuel giriş
        yapmasını sağlar ve session cookies/state'i kaydeder.
        """
        print("\n" + "=" * 60)
        print("  LinkedIn Manuel Oturum Açma (Tek Seferlik)")
        print("=" * 60)
        print("  Açılan tarayıcıda kullanıcı adı, şifre ve varsa 2FA ile giriş yapın.")
        print("  Giriş tamamlanıp ana akış (feed) yüklendiğinde oturum otomatik kaydedilecektir.")
        print("=" * 60 + "\n")

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-infobars"
                ]
            )
            context = browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            )
            context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            page = context.new_page()
            page.goto("https://www.linkedin.com/login", timeout=60000)

            print("  [BEKLENİYOR] Lütfen tarayıcıda giriş yapın (Maksimum 3 dakika bekleniyor)...")
            try:
                page.wait_for_url(lambda u: "feed" in u or "mynetwork" in u or "jobs" in u, timeout=180000)
                time.sleep(3)
                context.storage_state(path=str(self.session_file))
                print(f"\n  [BAŞARILI] Oturum kaydedildi: {self.session_file}")
            except Exception as e:
                print(f"\n  [HATA] Oturum kaydedilemedi: {e}")
            finally:
                browser.close()

    def has_valid_session(self) -> bool:
        """Kayıtlı oturum dosyasının varlığını kontrol eder."""
        return self.session_file.exists() and self.session_file.stat().st_size > 50

    def apply_to_job(self, job_url: str, dry_run: bool = False, human_in_the_loop: bool = True) -> Dict[str, Any]:
        """
        Belirtilen LinkedIn ilanına Easy Apply ile başvurur.
        dry_run=True ise son 'Gönder (Submit)' butonuna basmadan önceki aşamada durur.
        human_in_the_loop=True ise son adıma gelindiğinde kullanıcı onayı ister.
        """
        if not self.has_valid_session():
            return {"success": False, "reason": "LinkedIn oturumu (linkedin_state.json) bulunamadı. Lütfen önce giriş yapın."}

        headless_mode = not human_in_the_loop and not dry_run

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=headless_mode,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-infobars"
                ]
            )
            context = browser.new_context(
                storage_state=str(self.session_file),
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            )
            context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            page = context.new_page()

            try:
                page.goto(job_url, timeout=30000)
                time.sleep(3)

                # 0. İlanın süresi dolmuş mu kontrol et
                body_text = page.locator("body").inner_text().lower()
                if any(phrase in body_text for phrase in [
                    "artık başvuru kabul etmiyor",
                    "artık başvuru kabul edilmiyor",
                    "no longer accepting applications",
                    "bu iş ilanı artık yayında değil",
                    "bu iş ilanı kapandı"
                ]):
                    return {
                        "success": False,
                        "is_expired": True,
                        "reason": "İlanın süresi dolmuş (LinkedIn: Artık başvuru kabul etmiyor)."
                    }

                # 1. Kolay Başvuru (Easy Apply) butonunu semantik olarak bul
                easy_apply_btn = None
                for b in page.locator("button").all():
                    if not b.is_visible():
                        continue
                    txt = normalize_tr(b.inner_text())
                    aria = normalize_tr(b.get_attribute("aria-label") or "")
                    if "kolay" in txt or "easy" in txt or "kolay" in aria or "easy" in aria:
                        easy_apply_btn = b
                        break

                if not easy_apply_btn:
                    # Harici yönlendirme kontrolü
                    has_external = any(
                        el.is_visible() and normalize_tr(el.inner_text()) in ["başvur", "apply"]
                        for el in page.locator("a, button").all()
                    )
                    if has_external:
                        return {"success": False, "is_external": True, "reason": "İlan Easy Apply değil (Şirketin harici kariyer sitesine yönlendiriyor)."}
                    return {"success": False, "reason": "İlanda Kolay Başvuru (Easy Apply) butonu bulunamadı."}

                easy_apply_btn.click()
                time.sleep(2)

                dialog = page.locator("dialog:visible, [role='dialog']:visible").first
                if not dialog.is_visible():
                    return {"success": False, "reason": "Başvuru penceresi (dialog) açılamadı."}

                # Form adımlarını geçme döngüsü
                max_steps = 10
                current_step = 0

                while current_step < max_steps:
                    current_step += 1

                    # 1. Mevcut adımdaki alanları doldur (CV, sorular, seçenekler)
                    self._fill_step_inputs(dialog)
                    time.sleep(1)

                    # 2. Gönder (Submit) butonu kontrolü
                    submit_btn = None
                    for b in dialog.locator("button").all():
                        if not b.is_visible():
                            continue
                        txt = normalize_tr(b.inner_text())
                        aria = normalize_tr(b.get_attribute("aria-label") or "")
                        # Gönder/Submit anahtar kelimelerini ara, iptal/geri/düzenle butonlarını ele
                        if any(k in txt or k in aria for k in ["başvuruyu gönder", "submit application", "gönder", "submit"]) and not any(k in txt or k in aria for k in ["iptal", "cancel", "geri", "back", "düzenle", "edit"]):
                            submit_btn = b
                            break

                    if submit_btn:
                        if dry_run:
                            return {"success": True, "dry_run": True, "message": "Form adımları tamamlandı. Dry-run modunda Gönder butonuna basılmadı."}

                        if human_in_the_loop:
                            print("\n" + "-" * 50)
                            print("  [İNCELEME] Tüm form alanları ve CV başarıyla dolduruldu.")
                            print("  Tarayıcı ekranını inceleyebilirsiniz.")
                            confirm = input("  LinkedIn başvurusu gönderilsin mi? (E/H) [varsayılan E]: ").strip().lower()
                            if confirm not in ("", "e", "evet", "y", "yes"):
                                return {"success": False, "reason": "Kullanıcı onayı verilmedi (iptal edildi)."}

                        submit_btn.click()
                        time.sleep(3)
                        return {"success": True, "dry_run": False, "message": "Başvuru başarıyla gönderildi!"}

                    # 3. İleri / İncele (Next / Review) butonunu bul ve tıkla
                    next_btn = None
                    for b in dialog.locator("button").all():
                        if not b.is_visible():
                            continue
                        txt = normalize_tr(b.inner_text())
                        aria = normalize_tr(b.get_attribute("aria-label") or "")
                        if any(k in txt or k in aria for k in ["ileri", "next", "incele", "review", "sonraki"]):
                            next_btn = b
                            break

                    if next_btn:
                        next_btn.click()
                        time.sleep(2)
                        # Olası form doğrulama uyarılarını kontrol et ve logla
                        errors = [
                            e.inner_text().strip()
                            for e in dialog.locator(".artdeco-inline-feedback--error, [data-test-form-element-error-messages]").all()
                            if e.is_visible() and e.inner_text().strip()
                        ]
                        if errors:
                            logger.info(f"  [UYARI] Form adımı doğrulama uyarısı: {'; '.join(errors)}")
                    else:
                        break

                return {"success": False, "reason": "Form adımları tamamlanamadı veya beklenmeyen bir doğrulama hatası oluştu."}

            except Exception as e:
                return {"success": False, "reason": str(e)}
            finally:
                browser.close()

    def _extract_label(self, dialog: Locator, el: Locator) -> str:
        """Bir form elemanının (input, select, radio) sorusunu/etiketini DOM hiyerarşisinden tespit eder."""
        try:
            # 1. aria-label
            aria = (el.get_attribute("aria-label") or "").strip()
            if aria:
                return aria

            # 2. Associated <label for="id">
            el_id = el.get_attribute("id") or ""
            if el_id:
                lbl = dialog.locator(f"label[for='{el_id}']").first
                if lbl.count() > 0 and lbl.is_visible():
                    txt = lbl.inner_text().strip()
                    if txt:
                        return txt

            # 3. Kapsayıcı (container) içindeki label, legend veya başlık span'ı
            parent_txt = el.evaluate("""
                e => {
                    const container = e.closest('.fb-dash-form-element, .jobs-easy-apply-form-section__grouping, .jobs-easy-apply-form-element, fieldset, div.mb4');
                    if (!container) return '';
                    const lbl = container.querySelector('label, legend, span.fb-form-element-label, span.t-14, span.visually-hidden');
                    return lbl ? lbl.innerText.trim() : '';
                }
            """)
            if parent_txt and parent_txt.strip():
                return parent_txt.strip()

            # 4. placeholder
            ph = (el.get_attribute("placeholder") or "").strip()
            if ph:
                return ph
        except Exception:
            pass
        return ""

    def _fill_step_inputs(self, dialog: Locator):
        """Mevcut form adımındaki boş input, radio ve select kutularını profil cevaplarıyla doldurur."""
        try:
            # 1. CV Yükleme alanı varsa ve dosya mevcutsa yükle
            file_inputs = dialog.locator("input[type='file']").all()
            if file_inputs and self.cv_path.exists():
                for fi in file_inputs:
                    try:
                        fi.set_input_files(str(self.cv_path))
                        time.sleep(1)
                    except Exception:
                        pass

            # 2. Radio Butonları (Evet/Hayır veya seçenekli sorular)
            radios = dialog.locator("input[type='radio']").all()
            radio_groups = {}
            for r in radios:
                name = r.get_attribute("name") or "default"
                radio_groups.setdefault(name, []).append(r)

            for name, group in radio_groups.items():
                if not any(r.is_checked() for r in group):
                    first_r = group[0]
                    question = self._extract_label(dialog, first_r)

                    # Grup içindeki tüm radio seçeneklerinin etiketlerini topla
                    radio_options = []
                    for r in group:
                        r_id = r.get_attribute("id") or ""
                        r_lbl = ""
                        if r_id:
                            lbl = dialog.locator(f"label[for='{r_id}']").first
                            if lbl.count() > 0:
                                r_lbl = lbl.inner_text().strip()
                        if not r_lbl:
                            r_lbl = (r.get_attribute("value") or "").strip()
                        radio_options.append(r_lbl)

                    ans = self.generator.answer_form_question(question, radio_options) if question else "Evet"

                    clicked = False
                    for idx, r in enumerate(group):
                        opt_lbl = radio_options[idx] if idx < len(radio_options) else ""
                        if ans.lower() in opt_lbl.lower() or opt_lbl.lower() in ans.lower():
                            r_id = r.get_attribute("id")
                            if r_id:
                                lbl = dialog.locator(f"label[for='{r_id}']").first
                                if lbl.is_visible():
                                    try:
                                        lbl.click()
                                        clicked = True
                                        break
                                    except Exception:
                                        pass
                            if not clicked:
                                try:
                                    r.locator("..").click()
                                    clicked = True
                                    break
                                except Exception:
                                    pass

                    if not clicked:
                        # Fallback olarak ilk seçeneği veya wrapper'ı tıkla
                        try:
                            group[0].locator("..").click()
                        except Exception:
                            group[0].evaluate("el => { el.checked = true; el.dispatchEvent(new Event('change', {bubbles: true})); }")

            # 3. Metin, Sayı ve Textarea kutuları
            inputs = dialog.locator("input[type='text'], input[type='number'], textarea").all()
            for inp in inputs:
                if inp.is_visible():
                    val = inp.input_value().strip()
                    if not val:
                        label = self._extract_label(dialog, inp)
                        inp_type = inp.get_attribute("type") or "text"
                        answer = self.generator.answer_form_question(label)

                        # Sayısal alan ise (input type=number veya yıl sorusu) sadece rakam doldur
                        if inp_type == "number":
                            digits = re.findall(r'\d+', str(answer))
                            val_to_fill = digits[0] if digits else "1"
                        else:
                            val_to_fill = str(answer)

                        # Kullanıcı Kuralı: Hiçbir yetkinlik/deneyim sorusuna ASLA "0" girilemez! (min 1)
                        if val_to_fill == "0":
                            val_to_fill = "1"

                        inp.fill(val_to_fill)
                        try:
                            inp.evaluate("el => { el.dispatchEvent(new Event('input', {bubbles: true})); el.dispatchEvent(new Event('change', {bubbles: true})); }")
                        except Exception:
                            pass

            # 4. Dropdown / Select kutuları
            selects = dialog.locator("select").all()
            for sel in selects:
                if sel.is_visible():
                    # Zaten geçerli bir seçim yapılmış mı kontrol et (LinkedIn'in otomatik seçtiği Turkey (+90) gibi alanları koru)
                    selected_text = ""
                    try:
                        selected_text = sel.evaluate("el => el.options && el.selectedIndex >= 0 ? el.options[el.selectedIndex].text.trim() : ''")
                    except Exception:
                        pass
                    selected_val = (sel.input_value() or "").strip()

                    is_placeholder = (
                        not selected_val or 
                        not selected_text or
                        any(ph in selected_text.lower() for ph in ["seçiniz", "seçin", "select an option", "choose", "belirleyin", "lütfen", "--", "select..."])
                    )

                    # Eğer zaten geçerli ve dolu bir seçim varsa dokunma (Andorra gibi yanlış atamaları önler)
                    if not is_placeholder:
                        continue

                    label = self._extract_label(dialog, sel)
                    raw_options = [o.inner_text().strip() for o in sel.locator("option").all() if o.inner_text().strip()]
                    valid_options = [
                        o for o in raw_options
                        if not any(ph in o.lower() for ph in ["seçiniz", "seçin", "select an option", "choose", "belirleyin", "lütfen"])
                    ]
                    options_to_use = valid_options if valid_options else raw_options

                    if options_to_use:
                        ans = self.generator.answer_form_question(label, options_to_use)
                        selected = False
                        try:
                            sel.select_option(label=ans)
                            selected = True
                        except Exception:
                            for opt in options_to_use:
                                if ans.lower() in opt.lower() or opt.lower() in ans.lower():
                                    try:
                                        sel.select_option(label=opt)
                                        selected = True
                                        break
                                    except Exception:
                                        pass
                        if not selected and options_to_use:
                            try:
                                sel.select_option(label=options_to_use[0])
                            except Exception:
                                pass

                        try:
                            sel.evaluate("el => el.dispatchEvent(new Event('change', {bubbles: true}))")
                        except Exception:
                            pass

            # 5. Checkbox (Onay / Şartlar ve Şirket Takip kutuları)
            follow_companies = self.generator.profile.get("preferences", {}).get("follow_companies_on_apply", False)
            checkboxes = dialog.locator("input[type='checkbox']").all()
            for cb in checkboxes:
                if not cb.is_visible():
                    continue
                cb_label = self._extract_label(dialog, cb).lower()
                is_follow_cb = any(w in cb_label for w in ["takip et", "takip edin", "follow", "haber almak için", "stay up to date"])

                if is_follow_cb:
                    # Şirket takip kutusu: Kullanıcı feed'ini temiz tutmak için varsayılan olarak tiki kaldır (uncheck)
                    if not follow_companies and cb.is_checked():
                        cb_id = cb.get_attribute("id") or ""
                        clicked = False
                        if cb_id:
                            lbl = dialog.locator(f"label[for='{cb_id}']").first
                            if lbl.is_visible():
                                try:
                                    lbl.click()
                                    clicked = True
                                except Exception:
                                    pass
                        if not clicked:
                            try:
                                cb.uncheck(force=True)
                            except Exception:
                                cb.evaluate("el => { el.checked = false; el.dispatchEvent(new Event('change', {bubbles: true})); }")
                else:
                    # Şartlar, Gizlilik ve İzin kutuları: Başvurunun ilerlemesi için işaretle (check)
                    if not cb.is_checked():
                        cb_id = cb.get_attribute("id") or ""
                        clicked = False
                        if cb_id:
                            lbl = dialog.locator(f"label[for='{cb_id}']").first
                            if lbl.is_visible():
                                try:
                                    lbl.click()
                                    clicked = True
                                except Exception:
                                    pass
                        if not clicked:
                            try:
                                cb.check(force=True)
                            except Exception:
                                cb.evaluate("el => { el.checked = true; el.dispatchEvent(new Event('change', {bubbles: true})); }")

        except Exception as e:
            logger.debug(f"Input doldurma uyarısı: {e}")
