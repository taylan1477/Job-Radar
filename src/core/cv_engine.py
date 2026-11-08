import os
import re
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from playwright.sync_api import sync_playwright

from src.utils.text_norm import normalize_tr

logger = logging.getLogger(__name__)

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CATALOG_PDF_DIR = PROJECT_ROOT / "cv_suite" / "Humanized_CV" / "pdf"
GENERATED_PDF_DIR = PROJECT_ROOT / "cv_suite" / "generated"

# Ensure directories exist
GENERATED_PDF_DIR.mkdir(parents=True, exist_ok=True)

# Master Project Pool (11 Genuine Projects from master_profile.md)
MASTER_PROJECTS = [
    {
        "id": "aegis_forge",
        "title": "Aegis Forge: Tactical Terraforming Multiplayer Shooter",
        "link": "https://github.com/taylan1477",
        "tech": "Unity, C#, DOTS, Job System, Burst Compiler, NativeArray, FishNet, Linux Headless",
        "categories": ["gamedev", "simulation", "systems", "csharp", "multiplayer", "backend"],
        "keywords": ["unity", "c#", "dots", "burst", "job system", "multiplayer", "fishnet", "networking", "game", "simulation", "physics", "linux"],
        "bullets": [
            "Engineered a real-time multiplayer combat simulation where players reshape dynamic terrain meshes synchronously.",
            "Accelerated height deformation across 10,000+ tiles using Unity C# Job System and Burst Compiler for sub-millisecond execution.",
            "Built a deterministic event-based replication model with FishNet hosted on a headless Linux dedicated server."
        ]
    },
    {
        "id": "mass_video_cutter",
        "title": "MassVideoCutter: Desktop Video Trimming & Media Suite",
        "link": "https://github.com/taylan1477/MassVCutter",
        "tech": "Java 23, JavaFX 23, Spring Boot 4, PostgreSQL 15, FFmpeg, Multi-threading",
        "categories": ["software", "backend", "desktop", "java", "media"],
        "keywords": ["java", "javafx", "spring boot", "spring", "postgresql", "sql", "ffmpeg", "multithreading", "desktop", "backend", "rest api"],
        "bullets": [
            "Built a high-performance JavaFX desktop tool that batch-trims intros and outros from large media libraries using FFmpeg CLI.",
            "Developed an audio volume detector using FFmpeg astats filters to automatically pinpoint recurring musical themes.",
            "Designed trimming pipelines with Facade and Strategy patterns and integrated a Spring Boot 4 REST API with PostgreSQL."
        ]
    },
    {
        "id": "cinenode",
        "title": "CineNode: 4K Home Media Server & Autonomous Bot",
        "link": "https://github.com/taylan1477",
        "tech": "Python, Docker, Telegram Bot API, Plex, Radarr, Prowlarr, Linux",
        "categories": ["systems", "devops", "automation", "python", "backend"],
        "keywords": ["python", "docker", "linux", "plex", "devops", "automation", "bot", "microservices", "networking", "sre"],
        "bullets": [
            "Configured a self-hosted containerized media infrastructure running Plex, qBittorrent, Radarr, and Prowlarr in Docker.",
            "Enforced a strict Direct Play policy to eliminate CPU-heavy transcoding spikes during concurrent 4K media streams.",
            "Created an asynchronous Python Telegram bot with automated health checks, real-time speed monitoring, and disk auto-cleanup."
        ]
    },
    {
        "id": "job_radar",
        "title": "Job-Radar: Autonomous Job Mining & Candidate Match Engine",
        "link": "https://github.com/taylan1477/Job-Radar",
        "tech": "Python, Playwright, Pydantic, Scikit-learn, Google Sheets API, LLM",
        "categories": ["automation", "ai", "python", "scraping", "data"],
        "keywords": ["python", "playwright", "scraping", "selenium", "nlp", "scikit-learn", "pydantic", "automation", "sheets", "data pipeline"],
        "bullets": [
            "Built an enterprise web scraper using Playwright to extract dynamic job postings from SPAs while evading anti-bot detection.",
            "Implemented an NLP text-matching engine with TF-IDF vectorization and cosine similarity to rank opportunities against candidate profiles.",
            "Automated ETL pipelines with Pydantic schema validation, cloud Google Sheets synchronization, and headless PDF generation."
        ]
    },
    {
        "id": "voice_os",
        "title": "VoiceOS (Jarvis): Local Offline AI Desktop Assistant",
        "link": "https://github.com/taylan1477",
        "tech": "Python, Ollama (Qwen 2.5 / LLaVA), Faster-Whisper, Win32 IPC, Graphify",
        "categories": ["ai", "python", "desktop", "systems", "automation"],
        "keywords": ["ai", "llm", "ollama", "whisper", "speech", "vision", "python", "ipc", "desktop", "offline", "edge ai"],
        "bullets": [
            "Built a 100% offline, privacy-first desktop voice agent running quantized local LLMs (Qwen 2.5 and LLaVA) directly on GPU.",
            "Engineered a low-latency speech loop combining Faster-Whisper (INT8) with an interruptible TTS engine supporting instant barge-in.",
            "Automated native Windows desktop operations through Win32 IPC and mapped module dependencies with AST graph analysis."
        ]
    },
    {
        "id": "agent_swarm",
        "title": "AgentSwarm: Multi-Agent Autonomous Development Cockpit",
        "link": "https://github.com/taylan1477",
        "tech": "Gemini 3.1 Pro, WSL2 (Ubuntu), Docker, PostgreSQL, MCP, AHK v2",
        "categories": ["ai", "devops", "systems", "backend", "automation"],
        "keywords": ["agent", "multi-agent", "mcp", "docker", "postgresql", "linux", "wsl", "gemini", "ai platform", "automation"],
        "bullets": [
            "Orchestrated autonomous multi-agent CLI workers in WSL2 supervised by Gemini 3.1 Pro inside JetBrains IDE cockpit.",
            "Developed a custom Python Model Context Protocol (MCP) server backed by PostgreSQL for chronological inter-agent memory sync.",
            "Created low-latency prompt injection and automation bridges between Windows host and Linux guests using AutoHotkey v2."
        ]
    },
    {
        "id": "kidney_segmentation",
        "title": "Kidney CT Segmentation: Classical CV vs Deep Learning",
        "link": "https://github.com/taylan1477",
        "tech": "Python, PyTorch, OpenCV, ScaleNorm-UNet, BRISQUE Filter, AMOS Dataset",
        "categories": ["ai", "vision", "python", "research", "data"],
        "keywords": ["computer vision", "opencv", "pytorch", "deep learning", "unet", "segmentation", "image processing", "ai"],
        "bullets": [
            "Benchmarked classical feature extractors (SIFT, HOG, CoHOG, LBP) against ScaleNorm-UNet on clinical abdominal CT scans.",
            "Integrated a BRISQUE no-reference image quality evaluator to automatically filter noisy, low-contrast axial slices.",
            "Trained pixel-level deep learning segmentation models optimized with Dice Loss and IoU metrics for accurate boundary extraction."
        ]
    },
    {
        "id": "fitconnect",
        "title": "FitConnect: Trainer-Client Ecosystem & Live Workout App",
        "link": "https://github.com/taylan1477",
        "tech": "React Native (Expo), TypeScript, Supabase (PostgreSQL), Deno Edge Functions",
        "categories": ["mobile", "fullstack", "software", "typescript", "backend"],
        "keywords": ["react native", "expo", "typescript", "mobile", "ios", "android", "supabase", "postgresql", "fullstack", "edge functions"],
        "bullets": [
            "Engineered a cross-platform mobile application for personal trainers and fitness clients using React Native and TypeScript.",
            "Configured Supabase PostgreSQL with granular Row Level Security (RLS) policies isolating multi-tenant gym roles.",
            "Implemented dynamic timestamped QR verification to authenticate in-person training sessions and decrement client credits in real time."
        ]
    },
    {
        "id": "evolucat",
        "title": "EvoluCat: 2D Metroidvania Platform Game",
        "link": "https://github.com/taylan1477",
        "tech": "Unity 2D, C#, Finite State Machines, Physics2D, JSON Serialization",
        "categories": ["gamedev", "csharp", "desktop"],
        "keywords": ["unity", "c#", "gamedev", "2d", "physics", "state machine", "gameplay", "animation"],
        "bullets": [
            "Architected responsive 2D player mechanics, wall jumps, and telekinesis puzzles using a clean hierarchical Finite State Machine.",
            "Built an encrypted multi-slot save/load persistence layer that safely serializes unlocked player skills, inventory, and room transitions."
        ]
    },
    {
        "id": "soloidle",
        "title": "SoloIdle: Educational Campus Management & Idle Game",
        "link": "https://github.com/taylan1477/SoloIdle",
        "tech": "Unity 2D, C#, ScriptableObjects, Asynchronous REST API, Android/iOS",
        "categories": ["gamedev", "mobile", "csharp"],
        "keywords": ["unity", "c#", "mobile", "gamedev", "scriptableobjects", "rest api", "idle", "edtech"],
        "bullets": [
            "Developed an incremental idle simulation loop tying campus revenue multipliers to academic quiz answer accuracy.",
            "Leveraged ScriptableObject architectures to decouple faculty research trees, multipliers, and upgrade balancing from code."
        ]
    },
    {
        "id": "muzik_manager",
        "title": "MuzikManager: Studio 48kHz Opus Audio Pipeline",
        "link": "https://github.com/taylan1477",
        "tech": "Python, FFmpeg, Opus Codec, Streaming REST APIs, Mutagen",
        "categories": ["software", "media", "python", "automation"],
        "keywords": ["python", "ffmpeg", "audio", "opus", "rest api", "automation", "multimedia"],
        "bullets": [
            "Engineered a batch conversion pipeline processing 1,600+ tracks to studio standard 48 kHz stereo 192 kbps Opus format.",
            "Normalized audio loudness to broadcast standard -14 dB LUFS using FFmpeg volumedetect and dynamic filtering.",
            "Automated high-resolution album artwork fetching and VorbisComment metadata tagging via streaming REST APIs."
        ]
    }
]

# Candidate Core Known Skills (Single Source of Truth)
KNOWN_SKILLS = {
    "c#", "python", "java", "c++", "typescript", "javascript", "sql", "bash", "powershell",
    "unity", "unity 3d", "unity 2d", "dots", "burst compiler", "job system", "unreal engine", "fishnet", "physics",
    ".net", "asp.net core", "javafx", "spring boot", "react native", "expo", "supabase", "rest api", "restful", "rest apis",
    "playwright", "selenium", "pydantic", "scikit-learn", "pytorch", "opencv", "computer vision", "machine learning",
    "docker", "postgresql", "sqlite", "ffmpeg", "git", "github", "linux", "ubuntu", "wsl2", "oop", "solid", "multithreading"
}

# Controlled Embellishment / Skill Positioning Lexicon
# Job-required unknown skills that can be positioned as "Intermediate / Working Knowledge"
POSITIONABLE_UNKNOWN_SKILLS = [
    "kotlin", "swift", "flutter", "go", "golang", "rust", "aws", "azure", "gcp",
    "redis", "graphql", "rabbitmq", "kafka", "kubernetes", "ci/cd", "jenkins",
    "microservices", "mongodb", "elasticsearch", "node.js", "vue", "angular",
    "tailwind", "next.js", "fastapi", "django", "flask"
]


class CVEngine:
    """
    Job Radar Dinamik CV Seçim ve İlana Özel JIT PDF Üretim Motoru.
    
    İki Temel Mod Barındırır:
    - Mod 1 (Catalog Matcher): cv_suite/Humanized_CV/pdf/ altındaki 3 uzmanlaşmış
      İngilizce CV arasından role en uygun olanı seçer (0ms gecikme).
    - Mod 2 (JIT Tailored Generator): Skor >= 4.0 (VIP) veya LinkedIn dışı harici
      ilanlar için master_profile.md ve 11 projeden beslenerek ilana özel A4 tek sayfa
      ATS uyumlu PDF üretir (< 0.8s, Playwright Headless).
    """

    def __init__(self, catalog_dir: Path = CATALOG_PDF_DIR, output_dir: Path = GENERATED_PDF_DIR):
        self.catalog_dir = catalog_dir
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def resolve_cv_for_job(self, job: Dict[str, Any], force_mode: Optional[str] = None) -> Tuple[Path, str, str]:
        """
        Verilen ilan için kullanıcı kurallarına ve hibrit karar matrisine göre
        en doğru CV'yi belirler veya anında üretir.

        Dönüş: (cv_dosya_yolu, mod_adı, gerekçe)
        """
        score = float(job.get("score") or 0.0)
        link = str(job.get("link") or "").lower()
        is_easy_apply = "linkedin.com" in link

        # 1. Zorunlu mod kontrolü
        if force_mode == "catalog":
            cv_path = self.match_catalog_cv(job)
            return cv_path, "Mod 1 (Katalog Eşleme)", "Manuel zorunlu katalog seçimi"
        elif force_mode == "tailored":
            cv_path = self.generate_tailored_cv(job)
            return cv_path, "Mod 2 (İlana Özel Sıcak CV)", "Manuel zorunlu sıcak CV üretimi"

        # 2. Otomatik Hibrit Karar Matrisi
        if score >= 4.0:
            cv_path = self.generate_tailored_cv(job)
            reason = f"VIP İlan (Skor: {score:.1f} >= 4.0) -> Özel JIT Derleme"
            return cv_path, "Mod 2 (İlana Özel Sıcak CV)", reason
        elif not is_easy_apply:
            cv_path = self.generate_tailored_cv(job)
            reason = f"Harici İlan / İK E-Postası (Kolay Başvuru Değil) -> Özel JIT Derleme"
            return cv_path, "Mod 2 (İlana Özel Sıcak CV)", reason
        else:
            cv_path = self.match_catalog_cv(job)
            reason = f"Standart LinkedIn Easy Apply (Skor: {score:.1f} < 4.0) -> Hızlı Katalog Eşleme"
            return cv_path, "Mod 1 (Katalog Eşleme)", reason

    def match_catalog_cv(self, job: Dict[str, Any]) -> Path:
        """
        Mod 1: İlanın başlık, alan ve açıklama metnini analiz ederek
        mevcut 3 İngilizce katalog CV'sinden en doğrusunu döndürür.
        """
        title = normalize_tr(job.get("title", "")).lower()
        field = normalize_tr(job.get("field", "")).lower()
        desc = normalize_tr(job.get("description", "")).lower()
        full_text = f"{title} {field} {desc}"

        game_keywords = ["game", "oyun", "unity", "unreal", "simulation", "simulasyon", "physics", "gameplay", "3d", "2d", "shader", "gamedev"]
        ai_auto_keywords = ["ai", "yapay zeka", "machine learning", "derin ogrenme", "scraping", "kazima", "automation", "otomasyon", "bot", "crawler", "data engineer", "computer vision", "goruntulu"]
        
        game_score = sum(full_text.count(k) for k in game_keywords)
        ai_score = sum(full_text.count(k) for k in ai_auto_keywords)

        # Game & Sim
        if game_score > ai_score and game_score > 0:
            target = self.catalog_dir / "Taylan_Ozdemir_Game_Simulation_CV.pdf"
            if target.exists():
                return target

        # Automation & AI
        if ai_score >= game_score and ai_score > 0:
            target = self.catalog_dir / "Taylan_Ozdemir_Automation_AI_CV.pdf"
            if target.exists():
                return target

        # Core Software & Systems (Default / Primary)
        target = self.catalog_dir / "Taylan_Ozdemir_Software_Systems_CV.pdf"
        if target.exists():
            return target

        # Fallback to any existing PDF in catalog
        for pdf_file in self.catalog_dir.glob("*.pdf"):
            return pdf_file

        raise FileNotFoundError(f"Katalog CV klasöründe ({self.catalog_dir}) PDF bulunamadı.")

    def generate_tailored_cv(self, job: Dict[str, Any]) -> Path:
        """
        Mod 2: İlandaki gereksinimleri analiz eder, master profile'dan en uygun 3 projeyi seçer,
        kontrollü yetkinlik konumlandırmasını uygular ve Playwright ile A4 tek sayfa PDF derler.
        """
        job_title = job.get("title", "Software Engineer").strip()
        company = job.get("company", "Company").strip()
        desc = job.get("description", "")
        field = job.get("field", "Software")

        # Dosya adı sanitizasyonu
        safe_role = re.sub(r"[^\w\-_]", "_", job_title)[:30].strip("_")
        safe_company = re.sub(r"[^\w\-_]", "_", company)[:25].strip("_")
        output_filename = f"Taylan_Ozdemir_{safe_role}_{safe_company}.pdf"
        output_path = self.output_dir / output_filename

        # Eğer aynı ilan için daha önce üretildiyse tekrar üretme
        if output_path.exists() and output_path.stat().st_size > 1000:
            logger.info(f"Önceden üretilmiş JIT CV kullanılıyor: {output_path.name}")
            return output_path

        # 1. İlan metni analizi & Anahtar kelime tespiti
        norm_text = normalize_tr(f"{job_title} {field} {desc}").lower()
        
        # 2. Yetkinlik Konumlandırma (Kullanıcı Kuralı: Bilinen -> Proficient, Bilinmeyen -> Intermediate)
        proficient_skills, intermediate_skills = self._position_skills_for_job(norm_text)

        # 3. 11 Projeden En Uygun 3 Projeyi Seç
        selected_projects = self._select_top_projects(norm_text, field)

        # 4. Aday Unvanını İlana Göre Özelleştir
        headline_title = self._craft_candidate_title(job_title, field)

        # 5. HTML İçeriğini Oluştur
        html_content = self._render_cv_html(
            headline_title=headline_title,
            projects=selected_projects,
            proficient_skills=proficient_skills,
            intermediate_skills=intermediate_skills,
            field=field
        )

        # 6. Playwright Headless ile PDF Derle (< 0.8s)
        self._compile_html_to_pdf(html_content, output_path)

        return output_path

    def _position_skills_for_job(self, norm_text: str) -> Tuple[List[str], List[str]]:
        """
        Kullanıcı Yetkinlik Konumlandırma Kuralı:
        - Adayın bildiği beceriler -> Proficient / Advanced
        - İlanın talep ettiği ancak adayın doğrudan listesinde olmayanlar -> Intermediate / Working Knowledge
        """
        matched_known = set()
        for skill in KNOWN_SKILLS:
            # Word boundary regex or simple check
            if re.search(r"\b" + re.escape(skill) + r"\b", norm_text):
                matched_known.add(skill)

        # Varsayılan temel yetkinliklerimizi daima ekle
        core_defaults = {"c#", "python", "sql", "git", "docker", "oop"}
        matched_known.update(core_defaults)

        matched_unknown = []
        for unk in POSITIONABLE_UNKNOWN_SKILLS:
            if re.search(r"\b" + re.escape(unk) + r"\b", norm_text) and unk not in KNOWN_SKILLS:
                matched_unknown.append(unk)

        # Formatlı isimler
        format_map = {
            "c#": "C#", "python": "Python", "java": "Java", "c++": "C++",
            "typescript": "TypeScript", "javascript": "JavaScript", "sql": "SQL (PostgreSQL, SQLite)",
            "bash": "Bash", "powershell": "PowerShell", "unity": "Unity (2D/3D)", "unity 3d": "Unity 3D",
            "dots": "Unity DOTS (Job System, Burst)", "unreal engine": "Unreal Engine",
            "fishnet": "FishNet Networking", ".net": ".NET / ASP.NET Core", "asp.net core": "ASP.NET Core",
            "javafx": "JavaFX", "spring boot": "Spring Boot", "react native": "React Native (Expo)",
            "supabase": "Supabase", "rest api": "RESTful APIs", "rest apis": "RESTful APIs",
            "playwright": "Playwright", "selenium": "Selenium", "pydantic": "Pydantic",
            "scikit-learn": "Scikit-learn", "pytorch": "PyTorch", "opencv": "OpenCV",
            "docker": "Docker", "postgresql": "PostgreSQL", "sqlite": "SQLite",
            "ffmpeg": "FFmpeg", "git": "Git / GitHub", "linux": "Linux (Ubuntu/WSL2)",
            "oop": "OOP & Clean Architecture", "solid": "SOLID Principles", "multithreading": "Multi-threading"
        }

        proficient = [format_map.get(s, s.title()) for s in sorted(matched_known)]
        intermediate = [s.upper() if len(s) <= 4 else s.title() for s in sorted(set(matched_unknown))]

        return proficient, intermediate

    def _select_top_projects(self, norm_text: str, field: str) -> List[Dict[str, Any]]:
        """11 Proje arasından ilana en yüksek anahtar kelime eşleşmesine sahip 3 tanesini seçer."""
        scored_projects = []

        field_norm = normalize_tr(field).lower()

        for proj in MASTER_PROJECTS:
            score = 0
            # Kategori uyumu
            for cat in proj["categories"]:
                if cat in field_norm or cat in norm_text:
                    score += 3

            # Anahtar kelime uyumu
            for kw in proj["keywords"]:
                if kw in norm_text:
                    score += 2
                if kw in field_norm:
                    score += 4

            scored_projects.append((score, proj))

        # Puana göre azalan sırala
        scored_projects.sort(key=lambda x: x[0], reverse=True)

        selected = [p for _, p in scored_projects[:3]]
        # Eğer yeterli proje yoksa ilk 3'ü al
        if len(selected) < 3:
            selected = MASTER_PROJECTS[:3]

        return selected

    def _craft_candidate_title(self, job_title: str, field: str) -> str:
        """İlan başlığına göre profesyonel alt unvan üretir."""
        title_lower = job_title.lower()
        if any(k in title_lower for k in ["game", "unity", "unreal", "oyun"]):
            return "Game Developer & Simulation Systems Engineer"
        elif any(k in title_lower for k in ["automation", "ai", "machine learning", "otomasyon", "python", "scraping"]):
            return "Software Engineer (Automation, AI & Systems)"
        elif any(k in title_lower for k in ["backend", "java", "c#", ".net", "spring", "server"]):
            return "Software Engineer (Backend, Distributed & Media Systems)"
        else:
            return "Software Engineer (Fullstack, Desktop & Systems)"

    def _render_cv_html(
        self,
        headline_title: str,
        projects: List[Dict[str, Any]],
        proficient_skills: List[str],
        intermediate_skills: List[str],
        field: str
    ) -> str:
        """Kusursuz A4 tek sayfa ATS uyumlu HTML şablonu oluşturur."""
        
        # Coursework uyarlaması
        coursework = "Data Structures & Algorithms, Object-Oriented Software Engineering, Operating Systems, Computer Networks"
        if "ai" in field.lower() or "otomasyon" in field.lower():
            coursework = "Computer Vision, Machine Learning, Data Structures & Algorithms, Operating Systems, Distributed Systems"
        elif "game" in field.lower() or "oyun" in field.lower():
            coursework = "Object-Oriented Programming, Computer Graphics, Physics Simulation, Data Structures, Operating Systems"

        # Projeler HTML
        projects_html_list = []
        for p in projects:
            bullets_html = "\n".join(f"      <li>{b}</li>" for b in p["bullets"])
            p_html = f"""  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">{p['title']}</span>
      <span class="entry-date"><a href="{p['link']}">{p['link'].replace('https://', '')}</a></span>
    </div>
    <div class="project-tech">{p['tech']}</div>
    <ul>
{bullets_html}
    </ul>
  </div>"""
            projects_html_list.append(p_html)

        projects_html = "\n\n".join(projects_html_list)

        # Yetkinlikler HTML
        proficient_str = ", ".join(proficient_skills[:14])
        tech_skills_html = f"<p><strong>Core Competencies (Proficient / Advanced):</strong> {proficient_str}</p>"
        
        if intermediate_skills:
            intermediate_str = ", ".join(intermediate_skills[:8])
            tech_skills_html += f"\n    <p><strong>Applied Technologies (Working Knowledge / Practical):</strong> {intermediate_str}</p>"
        
        tech_skills_html += """
    <p><strong>Systems, Tools & Infrastructure:</strong> Linux (Ubuntu/WSL2), Docker, Git/GitHub, PostgreSQL, SQLite, Playwright, REST APIs, CI/CD</p>
    <p><strong>Architecture & Engineering:</strong> Clean Code, OOP, SOLID Principles, Design Patterns (Strategy, Facade), Multi-threading, Unit Testing</p>"""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Taylan Özgür Özdemir - {headline_title}</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 8mm 13mm 8mm 13mm;
  }}
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #111827;
    background-color: #ffffff;
    font-size: 9.15pt;
    line-height: 1.32;
    -webkit-font-smoothing: antialiased;
  }}
  header {{
    text-align: center;
    margin-bottom: 7px;
  }}
  h1 {{
    font-size: 19pt;
    font-weight: 800;
    letter-spacing: 0.3px;
    color: #030712;
    margin-bottom: 2px;
    text-transform: uppercase;
  }}
  .subtitle {{
    font-size: 10.2pt;
    font-weight: 700;
    color: #374151;
    margin-bottom: 4px;
  }}
  .contact-bar {{
    font-size: 8.8pt;
    color: #4b5563;
  }}
  .contact-bar a {{
    color: #0f4c81;
    text-decoration: none;
    font-weight: 500;
  }}
  .contact-bar a:hover {{
    text-decoration: underline;
  }}
  .contact-bar span {{
    margin: 0 4px;
    color: #9ca3af;
  }}
  section {{
    margin-top: 6.5px;
  }}
  h2 {{
    font-size: 10.2pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #111827;
    border-bottom: 1.2px solid #111827;
    padding-bottom: 1px;
    margin-bottom: 4px;
  }}
  .entry {{
    margin-bottom: 4.5px;
  }}
  .entry:last-child {{
    margin-bottom: 0;
  }}
  .entry-header {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    font-size: 9.25pt;
  }}
  .entry-title {{
    font-weight: 700;
    color: #111827;
  }}
  .entry-title a {{
    color: #0f4c81;
    text-decoration: none;
  }}
  .entry-title a:hover {{
    text-decoration: underline;
  }}
  .entry-date {{
    font-size: 8.75pt;
    color: #4b5563;
    font-style: italic;
    white-space: nowrap;
  }}
  .entry-subtitle {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    font-size: 8.85pt;
    color: #374151;
    margin-bottom: 2px;
  }}
  .entry-subtitle em {{
    font-style: italic;
  }}
  .project-tech {{
    font-size: 8.65pt;
    color: #4b5563;
    font-style: italic;
  }}
  ul {{
    margin: 2px 0 2px 0;
    padding-left: 15px;
  }}
  li {{
    margin-bottom: 1.8px;
    font-size: 8.95pt;
    line-height: 1.29;
    color: #1f2937;
  }}
  li strong {{
    color: #111827;
  }}
  .skills-list {{
    font-size: 8.95pt;
    line-height: 1.34;
  }}
  .skills-list p {{
    margin-bottom: 2px;
  }}
  .skills-list strong {{
    color: #111827;
    font-weight: 700;
  }}
</style>
</head>
<body>
<header>
  <h1>Taylan Özgür Özdemir</h1>
  <div class="subtitle">{headline_title}</div>
  <div class="contact-bar">
    Ankara, Turkey <span>•</span> +90 541 262 3184 <span>•</span>
    <a href="mailto:taylan147701@gmail.com">taylan147701@gmail.com</a> <span>•</span>
    <a href="https://linkedin.com/in/taylan1477">linkedin.com/in/taylan1477</a> <span>•</span>
    <a href="https://github.com/taylan1477">github.com/taylan1477</a>
  </div>
</header>

<section>
  <h2>Education</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">İnönü University</span>
      <span class="entry-date">Sep 2021 – Jun 2025</span>
    </div>
    <div class="entry-subtitle">
      <span>Bachelor of Science in Computer Engineering, GPA: 3.09 / 4.00</span>
      <span>Malatya, Turkey</span>
    </div>
    <div style="font-size: 8.7pt; color: #4b5563; margin-top: 1px;">
      <em>Coursework:</em> {coursework}
    </div>
  </div>
</section>

<section>
  <h2>Work Experience</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">SoloRota</span>
      <span class="entry-date">Jul 2025 – Jan 2026</span>
    </div>
    <div class="entry-subtitle">
      <span>Software Engineer (Full-time)</span>
      <span>Ankara, Turkey</span>
    </div>
    <ul>
      <li>Engineered, profiled, and successfully deployed 7 commercial applications to Google Play and Apple App Store.</li>
      <li>Integrated backend RESTful services and local SQLite caching layers to ensure offline reliability and data persistence.</li>
      <li>Profiled CPU execution and memory allocators, eliminating garbage collection spikes and maintaining steady 60 FPS performance.</li>
      <li>Implemented modular C# components and automated build validation pipelines using Git version control.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Key Engineering Projects</h2>
{projects_html}
</section>

<section>
  <h2>Technical Skills & Competencies</h2>
  <div class="skills-list">
    {tech_skills_html}
  </div>
</section>
</body>
</html>
"""
        return html

    def _compile_html_to_pdf(self, html_content: str, output_path: Path):
        """Playwright Headless Chromium ile HTML'i A4 PDF'e derler (< 0.8s)."""
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
            )
            try:
                page = browser.new_page()
                page.set_content(html_content, wait_until="networkidle")
                page.pdf(
                    path=str(output_path),
                    format="A4",
                    print_background=True,
                    margin={"top": "8mm", "bottom": "8mm", "left": "13mm", "right": "13mm"}
                )
                logger.info(f"JIT PDF başarıyla derlendi: {output_path}")
            finally:
                browser.close()
