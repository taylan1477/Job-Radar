import os
import subprocess
import re

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
BASE_DIR = r"c:\Projeler\PycharmProjects\job-radar\cv_suite\Humanized_CV"
MD_DIR = os.path.join(BASE_DIR, "markdown")
HTML_DIR = os.path.join(BASE_DIR, "html")
PDF_DIR = os.path.join(BASE_DIR, "pdf")

os.makedirs(MD_DIR, exist_ok=True)
os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

# Minimalist, clean CSS without artificial AI formatting
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<title>{name} - {title}</title>
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
{body}
</body>
</html>
"""

cv_data = [
    # =========================================================================
    # 1. SOFTWARE & SYSTEMS (EN) - COMPLETELY HUMANIZED
    # =========================================================================
    {
        "filename": "Taylan_Ozdemir_Software_Systems_CV",
        "lang": "en",
        "name": "Taylan Özgür Özdemir",
        "title": "Software Engineer (Backend, Desktop & Fullstack)",
        "md_title": "Software Engineer (Backend, Desktop & Fullstack)",
        "body": """
<header>
  <h1>Taylan Özgür Özdemir</h1>
  <div class="subtitle">Software Engineer (Backend, Desktop & Fullstack)</div>
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
      <em>Coursework:</em> Object-Oriented Software Engineering, Database Systems, Operating Systems, Computer Networks
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
      <li>Built and released 7 mobile applications to Google Play and the App Store.</li>
      <li>Connected client apps to backend REST APIs, adding local SQLite caching to handle poor internet connections.</li>
      <li>Fixed garbage collection spikes and CPU bottlenecks with profiler tools, keeping frame rates at a steady 60 FPS on Android.</li>
      <li>Maintained codebase with Git, wrote clean modular C# components, and automated test builds.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Projects</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">MassVideoCutter: Desktop Video Trimming Tool</span>
      <span class="entry-date"><a href="https://github.com/taylan1477/MassVCutter">github.com/taylan1477/MassVCutter</a></span>
    </div>
    <div class="project-tech">Java 23, JavaFX 23, Spring Boot 4, PostgreSQL 15, FFmpeg, Multi-threading</div>
    <ul>
      <li>Built a JavaFX desktop tool that batch-trims intros and outros from TV series and anime using FFmpeg CLI calls.</li>
      <li>Wrote an audio volume detector using FFmpeg astats filters to pinpoint opening theme music automatically.</li>
      <li>Structured trimming logic with Facade and Strategy patterns to switch between manual markers and audio detection.</li>
      <li>Set up a Spring Boot REST API with PostgreSQL and Flyway migrations to let users share episode trim timings.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">CineNode: 4K Home Media Server and Telegram Bot</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477</a></span>
    </div>
    <div class="project-tech">Python, Docker, Telegram Bot API, Plex, Radarr, Prowlarr, Linux</div>
    <ul>
      <li>Configured a self-hosted media server using Docker containers for Plex, qBittorrent, Radarr, and Prowlarr.</li>
      <li>Enforced Direct Play playback to stream 4K and 1080p movies without maxing out host CPU on video transcoding.</li>
      <li>Built a Python Telegram bot to search movie releases, show real-time download speeds, and clean up disk space.</li>
      <li>Calculated active seeder ratios to skip dead or stalled downloads before starting transfers.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">FitConnect: Gym Management and Training Mobile App</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477</a></span>
    </div>
    <div class="project-tech">React Native (Expo), TypeScript, Supabase, PostgreSQL, Deno Edge Functions</div>
    <ul>
      <li>Developed an iOS and Android app for personal trainers and gym clients using React Native and TypeScript.</li>
      <li>Handled authentication and data storage in Supabase PostgreSQL, writing Row Level Security policies for user roles.</li>
      <li>Implemented dynamic QR code scanning to verify trainer sessions in person and deduct credits from client packages.</li>
      <li>Wrote Deno edge functions for secure account creation without interrupting active trainer sessions.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Technical Skills</h2>
  <div class="skills-list">
    <p><strong>Languages:</strong> Java (Java 23, JavaFX), C#, Python, TypeScript, SQL (PostgreSQL), C++</p>
    <p><strong>Frameworks and Backend:</strong> Spring Boot 4, .NET, React Native (Expo), Supabase, REST APIs, Flyway</p>
    <p><strong>Media and Tools:</strong> FFmpeg, FFprobe, Docker, Linux (Ubuntu/WSL2), Git, GitHub, Maven, Postman, IntelliJ IDEA</p>
    <p><strong>Design and Architecture:</strong> Object-Oriented Programming (OOP), SOLID principles, Strategy and Facade patterns, Multi-threading</p>
  </div>
</section>
"""
    },

    # =========================================================================
    # 2. SOFTWARE & SYSTEMS (TR) - COMPLETELY HUMANIZED
    # =========================================================================
    {
        "filename": "Taylan_Ozdemir_Yazilim_Sistemleri_CV_TR",
        "lang": "tr",
        "name": "Taylan Özgür Özdemir",
        "title": "Yazılım Mühendisi (Backend, Masaüstü ve Fullstack)",
        "md_title": "Yazılım Mühendisi (Backend, Masaüstü ve Fullstack)",
        "body": """
<header>
  <h1>Taylan Özgür Özdemir</h1>
  <div class="subtitle">Yazılım Mühendisi (Backend, Masaüstü ve Fullstack)</div>
  <div class="contact-bar">
    Ankara, Türkiye <span>•</span> +90 541 262 3184 <span>•</span>
    <a href="mailto:taylan147701@gmail.com">taylan147701@gmail.com</a> <span>•</span>
    <a href="https://linkedin.com/in/taylan1477">linkedin.com/in/taylan1477</a> <span>•</span>
    <a href="https://github.com/taylan1477">github.com/taylan1477</a>
  </div>
</header>

<section>
  <h2>Eğitim</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">İnönü Üniversitesi</span>
      <span class="entry-date">Eylül 2021 – Haziran 2025</span>
    </div>
    <div class="entry-subtitle">
      <span>Bilgisayar Mühendisliği Lisans, GANO: 3.09 / 4.00</span>
      <span>Malatya, Türkiye</span>
    </div>
    <div style="font-size: 8.7pt; color: #4b5563; margin-top: 1px;">
      <em>Alınan Dersler:</em> Nesne Yönelimli Yazılım Mühendisliği, Veritabanı Sistemleri, İşletim Sistemleri, Bilgisayar Ağları
    </div>
  </div>
</section>

<section>
  <h2>İş Deneyimi</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">SoloRota</span>
      <span class="entry-date">Temmuz 2025 – Ocak 2026</span>
    </div>
    <div class="entry-subtitle">
      <span>Yazılım Mühendisi (Tam Zamanlı)</span>
      <span>Ankara, Türkiye</span>
    </div>
    <ul>
      <li>Android ve iOS için 7 farklı mobil uygulamanın geliştirilmesinde çalıştı ve markete çıkışlarını sağladı.</li>
      <li>Uygulamaları arka plan REST API servislerine bağladı, internet kesintilerine karşı yerel SQLite önbellek yapısı kurdu.</li>
      <li>Profiler araçlarıyla bellek kaçaklarını ve işlemci yükünü temizleyerek orta segment telefonlarda 60 FPS akıcılık sağladı.</li>
      <li>Git kullanarak sürüm yönetimini organize etti, modüler C# bileşenleri geliştirdi ve test sürümlerini otomatize etti.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Projeler</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">MassVideoCutter: Toplu Video Kırpma Masaüstü Programı</span>
      <span class="entry-date"><a href="https://github.com/taylan1477/MassVCutter">github.com/taylan1477/MassVCutter</a></span>
    </div>
    <div class="project-tech">Java 23, JavaFX 23, Spring Boot 4, PostgreSQL 15, FFmpeg, Çok İş Parçacıklı Kodlama</div>
    <ul>
      <li>Dizi ve filmlerden jenerik bölümlerini FFmpeg kullanarak toplu halde kesip temizleyen bir JavaFX programı geliştirdi.</li>
      <li>FFmpeg astats filtreleriyle ses dalgalarını tarayan ve jenerik müziklerini ses yüksekliğinden otomatik yakalayan modül yazdı.</li>
      <li>Manuel işaretleme ve otomatik tespiti birbirinden bağımsız çalıştırmak için Facade ve Strategy tasarım desenlerini uyguladı.</li>
      <li>Kullanıcıların hazırladığı kesim sürelerini internetten paylaşabilmesi için Spring Boot 4 ve PostgreSQL ile REST API kurdu.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">CineNode: 4K Medya Sunucusu ve Telegram Botu</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477</a></span>
    </div>
    <div class="project-tech">Python, Docker, Telegram Bot API, Plex, Radarr, Prowlarr, Linux</div>
    <ul>
      <li>Plex, qBittorrent, Radarr ve Prowlarr servislerini Docker konteynerleri halinde çalışan bir ev medya sunucusu kurdu.</li>
      <li>İşlemciye binen transcode yükünü sıfırlamak için tüm istemcilerde doğrudan oynatma (Direct Play) kuralı uyguladı.</li>
      <li>Film arama, anlık indirme hızı takibi ve disk temizliği işlemlerini uzaktan yöneten bir Python Telegram botu yazdı.</li>
      <li>İndirme başlamadan önce tracker listesindeki gerçek eş oranını hesaplayarak ölü torrentleri otomatik ayıkladı.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">FitConnect: Antrenör ve Danışan Yönetim Mobil Uygulaması</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477</a></span>
    </div>
    <div class="project-tech">React Native (Expo), TypeScript, Supabase, PostgreSQL, Deno Edge Functions</div>
    <ul>
      <li>Spor eğitmenleri ve danışanları için React Native ve TypeScript kullanarak iOS ve Android mobil uygulaması geliştirdi.</li>
      <li>Kullanıcı oturumları ve veritabanı için Supabase PostgreSQL kullandı, antrenör ve müşteri rolleri için RLS kuralları yazdı.</li>
      <li>Ders seanslarının antrenörle yüz yüze düşülebilmesi için dinamik QR kod üreten ve kamerayla okuyan doğrulama sistemi kurdu.</li>
      <li>Antrenörün oturumu kapanmadan güvenli danışan kaydı açabilmesi için Deno tabanlı Supabase Edge Function servisleri yazdı.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Teknik Beceriler</h2>
  <div class="skills-list">
    <p><strong>Programlama Dilleri:</strong> Java (Java 23, JavaFX), C#, Python, TypeScript, SQL (PostgreSQL), C++</p>
    <p><strong>Çatılar ve Arka Yüz:</strong> Spring Boot 4, .NET, React Native (Expo), Supabase, REST API, Flyway</p>
    <p><strong>Medya ve Araçlar:</strong> FFmpeg, FFprobe, Docker, Linux (Ubuntu/WSL2), Git, GitHub, Maven, Postman, IntelliJ IDEA</p>
    <p><strong>Yazılım Mimarisi:</strong> Nesne Yönelimli Programlama (OOP), SOLID prensipleri, Tasarım Desenleri (Strategy, Facade), Çok İş Parçacıklı Programlama</p>
  </div>
</section>
"""
    },

    # =========================================================================
    # 3. GAME & SIMULATION (EN) - COMPLETELY HUMANIZED
    # =========================================================================
    {
        "filename": "Taylan_Ozdemir_Game_Simulation_CV",
        "lang": "en",
        "name": "Taylan Özgür Özdemir",
        "title": "Game Developer and Simulation Systems Engineer",
        "md_title": "Game Developer and Simulation Systems Engineer",
        "body": """
<header>
  <h1>Taylan Özgür Özdemir</h1>
  <div class="subtitle">Game Developer and Simulation Systems Engineer</div>
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
      <em>Coursework:</em> Data Structures and Algorithms, Object-Oriented Programming, Computer Vision, Distributed Systems
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
      <span>Game Developer (Full-time)</span>
      <span>Ankara, Turkey</span>
    </div>
    <ul>
      <li>Programmed gameplay mechanics, state machines, and menus for 7 educational mobile games in Unity (C#).</li>
      <li>Hooked up Unity games to a backend REST API so quiz questions and score multipliers loaded without lag.</li>
      <li>Profiled draw calls and garbage collection spikes using Unity Profiler, keeping games at 60 FPS on Android.</li>
      <li>Used ScriptableObjects for item upgrades, level data, and save files to keep game code clean and modular.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Projects</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">Aegis Forge: Tactical Terraforming Multiplayer Shooter</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477/AegisForge</a></span>
    </div>
    <div class="project-tech">Unity, C#, DOTS, Job System, Burst Compiler, NativeArray, FishNet, Headless Linux</div>
    <ul>
      <li>Built a multiplayer combat game where players reshape terrain in real time during matches.</li>
      <li>Processed height and mesh deformation across 10,000+ tiles simultaneously using the Unity C# Job System and Burst Compiler.</li>
      <li>Created a deterministic event-based replication model with FishNet running on a headless Linux dedicated server.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">SoloIdle: Campus Management Idle Game</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477/SoloIdle</a></span>
    </div>
    <div class="project-tech">Unity 2D, C#, Asynchronous Networking, ScriptableObjects</div>
    <ul>
      <li>Programmed an idle economy loop where player revenue multipliers depend on answering quiz questions correctly.</li>
      <li>Structured building upgrade formulas, department research trees, and save data with ScriptableObject assets.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">EvoluCat: 2D Metroidvania Platformer</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477/EvoluCat</a></span>
    </div>
    <div class="project-tech">Unity 2D, C#, Finite State Machines, Physics2D</div>
    <ul>
      <li>Built responsive 2D movement controls, wall-jumps, and telekinesis puzzles using a Finite State Machine structure.</li>
      <li>Implemented an encrypted multi-slot save system that stores player inventory, unlocked abilities, and map state.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Technical Skills</h2>
  <div class="skills-list">
    <p><strong>Game Engines:</strong> Unity (2D and 3D), Unity DOTS (C# Job System, Burst Compiler, Native Collections), Unreal Engine (Basics)</p>
    <p><strong>Languages:</strong> C#, C++, Python, Java, SQL, TypeScript, Bash</p>
    <p><strong>Multiplayer and Networking:</strong> FishNet, Client-Server Architecture, Dedicated Linux Game Servers, REST APIs</p>
    <p><strong>Architecture:</strong> Object-Oriented Programming (OOP), Data-Oriented Programming (DOP), State Machines, ScriptableObjects</p>
    <p><strong>Tools:</strong> Git, GitHub, Unity Profiler, Frame Debugger, JetBrains Rider, Visual Studio, Docker</p>
  </div>
</section>
"""
    },

    # =========================================================================
    # 4. GAME & SIMULATION (TR) - COMPLETELY HUMANIZED
    # =========================================================================
    {
        "filename": "Taylan_Ozdemir_Oyun_Simulasyon_CV_TR",
        "lang": "tr",
        "name": "Taylan Özgür Özdemir",
        "title": "Oyun Geliştirici ve Simülasyon Sistemleri Mühendisi",
        "md_title": "Oyun Geliştirici ve Simülasyon Sistemleri Mühendisi",
        "body": """
<header>
  <h1>Taylan Özgür Özdemir</h1>
  <div class="subtitle">Oyun Geliştirici ve Simülasyon Sistemleri Mühendisi</div>
  <div class="contact-bar">
    Ankara, Türkiye <span>•</span> +90 541 262 3184 <span>•</span>
    <a href="mailto:taylan147701@gmail.com">taylan147701@gmail.com</a> <span>•</span>
    <a href="https://linkedin.com/in/taylan1477">linkedin.com/in/taylan1477</a> <span>•</span>
    <a href="https://github.com/taylan1477">github.com/taylan1477</a>
  </div>
</header>

<section>
  <h2>Eğitim</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">İnönü Üniversitesi</span>
      <span class="entry-date">Eylül 2021 – Haziran 2025</span>
    </div>
    <div class="entry-subtitle">
      <span>Bilgisayar Mühendisliği Lisans, GANO: 3.09 / 4.00</span>
      <span>Malatya, Türkiye</span>
    </div>
    <div style="font-size: 8.7pt; color: #4b5563; margin-top: 1px;">
      <em>Alınan Dersler:</em> Veri Yapıları ve Algoritmalar, Nesne Yönelimli Programlama, Bilgisayarlı Görü, Dağıtık Sistemler
    </div>
  </div>
</section>

<section>
  <h2>İş Deneyimi</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">SoloRota</span>
      <span class="entry-date">Temmuz 2025 – Ocak 2026</span>
    </div>
    <div class="entry-subtitle">
      <span>Oyun Geliştirici (Tam Zamanlı)</span>
      <span>Ankara, Türkiye</span>
    </div>
    <ul>
      <li>Unity ve C# kullanarak 7 farklı eğitici mobil oyunun oynanış mekaniklerini, durum makinelerini ve arayüzlerini kodladı.</li>
      <li>Oyunların soru akışını ve puan çarpanlarını arka planda çalışan REST API servislerine bağladı.</li>
      <li>Unity Profiler ile bellek sızıntılarını ve çizim çağrılarını temizleyerek Android telefonlarda 60 FPS stabilite sağladı.</li>
      <li>Oyun içi ekonomi ve yükseltme sistemlerini ScriptableObject mimarisiyle kurarak modüler bir yapı elde etti.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Projeler</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">Aegis Forge: Taktiksel Arazi Dönüştürmeli Çok Oyunculu Nişancı Oyunu</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477/AegisForge</a></span>
    </div>
    <div class="project-tech">Unity, C#, DOTS, Job System, Burst Compiler, NativeArray, FishNet, Linux Sunucu</div>
    <ul>
      <li>Oyuncuların maç sırasında araziyi gerçek zamanlı olarak fiziksel olarak değiştirebildiği çok oyunculu bir oyun geliştirdi.</li>
      <li>Arazideki 10.000'den fazla hücrenin yükseklik ve mesh değişimini Unity C# Job System ve Burst Compiler ile paralel hesaplattı.</li>
      <li>Ağ paket boyutunu küçük tutmak amacıyla Linux Dedicated Server üzerinde FishNet ile deterministik olay tabanlı senkronizasyon kurdu.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">SoloIdle: Kampüs Yönetim ve Idle Oyunu</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477/SoloIdle</a></span>
    </div>
    <div class="project-tech">Unity 2D, C#, Asenkron Ağ İletişimi, ScriptableObjects</div>
    <ul>
      <li>Oyuncunun soru çözme başarısına göre kampüs gelir çarpanını artıran matematiksel bir idle oyun döngüsü kurdu.</li>
      <li>Bölüm açma, bina seviyeleri ve kayıt dosyalarını ScriptableObject veri yapılarıyla organize etti.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">EvoluCat: 2D Metroidvania Platform Oyunu</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477/EvoluCat</a></span>
    </div>
    <div class="project-tech">Unity 2D, C#, Durum Makineleri (FSM), 2D Fizik</div>
    <ul>
      <li>Karakterin duvardan atlama, telekinezi ve bulmaca çözme hareketlerini Durum Makineleri (State Machine) ile kontrol etti.</li>
      <li>Oyuncunun açtığı yetenekleri ve harita ilerlemesini saklayan çoklu yuvalı şifreli kayıt sistemi kurdu.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Teknik Beceriler</h2>
  <div class="skills-list">
    <p><strong>Oyun Motorları:</strong> Unity (2D ve 3D), Unity DOTS (C# Job System, Burst Compiler, Native Collections), Unreal Engine (Temel)</p>
    <p><strong>Diller:</strong> C#, C++, Python, Java, SQL, TypeScript, Bash</p>
    <p><strong>Ağ ve Çok Oyunculu:</strong> FishNet, İstemci-Sunucu Mimarisi, Linux Dedicated Oyun Sunucuları, REST API</p>
    <p><strong>Mimari:</strong> Nesne Yönelimli Programlama (OOP), Veri Odaklı Programlama (DOP), Durum Makineleri, ScriptableObjects</p>
    <p><strong>Geliştirici Araçları:</strong> Git, GitHub, Unity Profiler, Frame Debugger, JetBrains Rider, Visual Studio, Docker</p>
  </div>
</section>
"""
    },

    # =========================================================================
    # 5. AUTOMATION & AI (EN) - COMPLETELY HUMANIZED
    # =========================================================================
    {
        "filename": "Taylan_Ozdemir_Automation_AI_CV",
        "lang": "en",
        "name": "Taylan Özgür Özdemir",
        "title": "Software Engineer (Automation, AI and Systems)",
        "md_title": "Software Engineer (Automation, AI and Systems)",
        "body": """
<header>
  <h1>Taylan Özgür Özdemir</h1>
  <div class="subtitle">Software Engineer (Automation, AI and Systems)</div>
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
      <em>Coursework:</em> Computer Vision, Data Structures and Algorithms, Distributed Systems, Operating Systems, Machine Learning
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
      <span>Software & Systems Developer (Full-time)</span>
      <span>Ankara, Turkey</span>
    </div>
    <ul>
      <li>Built data ingestion pipelines and REST API integrations for 7 mobile apps published on app stores.</li>
      <li>Profiled system memory and traced thread locks, reducing garbage collection freezes by 25%.</li>
      <li>Automated daily build creation and deployment steps using custom Python and PowerShell scripts.</li>
      <li>Wrote modular data validation schemas and state listeners to keep multi-platform builds in sync.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Projects</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">Job-Radar: Job Scraping and Candidate Match Engine</span>
      <span class="entry-date"><a href="https://github.com/taylan1477/Job-Radar">github.com/taylan1477/Job-Radar</a></span>
    </div>
    <div class="project-tech">Python, Playwright, Pydantic, Scikit-learn, Google Sheets API</div>
    <ul>
      <li>Built a web scraper with Playwright to extract job postings from Single Page Applications while handling anti-bot rate limits.</li>
      <li>Implemented an NLP text-matching algorithm using TF-IDF vectorization and cosine similarity to rank job descriptions against resumes.</li>
      <li>Automated data pipelines to clean, validate with Pydantic schemas, and export job data to Google Sheets and Excel.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">Kidney CT Segmentation: Classical CV vs Deep Learning</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477</a></span>
    </div>
    <div class="project-tech">Python, PyTorch, OpenCV, ScaleNorm-UNet, BRISQUE Quality Filter, AMOS Dataset</div>
    <ul>
      <li>Benchmarked classical image processing (HOG, SIFT, CoHOG, LBP) against ScaleNorm-UNet on abdominal CT scans.</li>
      <li>Evaluated input slice quality with BRISQUE scores to automatically filter out noisy and low-contrast scans.</li>
      <li>Trained the deep learning segmentation model with Dice Loss and IoU metrics to identify precise kidney boundaries.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">Voice OS (Jarvis): Local Offline AI Desktop Assistant</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477</a></span>
    </div>
    <div class="project-tech">Python, Ollama (Qwen/LLaVA), Faster-Whisper, Win32 IPC, Graphify</div>
    <ul>
      <li>Built an offline voice assistant running local quantized models (Qwen 2.5 7B and LLaVA 7B) on GPU with no cloud calls.</li>
      <li>Wrote a fast speech loop combining Faster-Whisper (INT8) with an interruptible TTS engine that stops speaking when the user cuts in.</li>
      <li>Automated Windows desktop controls via Win32 IPC calls and mapped module dependencies with an AST graph.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Technical Skills</h2>
  <div class="skills-list">
    <p><strong>AI and Machine Learning:</strong> PyTorch, OpenCV, Computer Vision, ScaleNorm-UNet, Scikit-learn, Ollama (Local LLMs), Faster-Whisper</p>
    <p><strong>Scraping and Automation:</strong> Playwright, Selenium, Beautiful Soup, Dynamic DOM Extraction, Anti-Bot Bypass, Win32 IPC</p>
    <p><strong>Languages and Data:</strong> Python, C#, Java, SQL, TypeScript, Pydantic, FastAPI, REST APIs</p>
    <p><strong>Systems and Tools:</strong> Docker, Linux (Ubuntu/WSL2), Git, GitHub, Bash, PowerShell, Model Context Protocol (MCP)</p>
  </div>
</section>
"""
    },

    # =========================================================================
    # 6. AUTOMATION & AI (TR) - COMPLETELY HUMANIZED
    # =========================================================================
    {
        "filename": "Taylan_Ozdemir_Otomasyon_AI_CV_TR",
        "lang": "tr",
        "name": "Taylan Özgür Özdemir",
        "title": "Yazılım Mühendisi (Otomasyon, Yapay Zeka ve Sistemler)",
        "md_title": "Yazılım Mühendisi (Otomasyon, Yapay Zeka ve Sistemler)",
        "body": """
<header>
  <h1>Taylan Özgür Özdemir</h1>
  <div class="subtitle">Yazılım Mühendisi (Otomasyon, Yapay Zeka ve Sistemler)</div>
  <div class="contact-bar">
    Ankara, Türkiye <span>•</span> +90 541 262 3184 <span>•</span>
    <a href="mailto:taylan147701@gmail.com">taylan147701@gmail.com</a> <span>•</span>
    <a href="https://linkedin.com/in/taylan1477">linkedin.com/in/taylan1477</a> <span>•</span>
    <a href="https://github.com/taylan1477">github.com/taylan1477</a>
  </div>
</header>

<section>
  <h2>Eğitim</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">İnönü Üniversitesi</span>
      <span class="entry-date">Eylül 2021 – Haziran 2025</span>
    </div>
    <div class="entry-subtitle">
      <span>Bilgisayar Mühendisliği Lisans, GANO: 3.09 / 4.00</span>
      <span>Malatya, Türkiye</span>
    </div>
    <div style="font-size: 8.7pt; color: #4b5563; margin-top: 1px;">
      <em>Alınan Dersler:</em> Bilgisayarlı Görü, Veri Yapıları ve Algoritmalar, Dağıtık Sistemler, İşletim Sistemleri, Makine Öğrenmesi
    </div>
  </div>
</section>

<section>
  <h2>İş Deneyimi</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">SoloRota</span>
      <span class="entry-date">Temmuz 2025 – Ocak 2026</span>
    </div>
    <div class="entry-subtitle">
      <span>Yazılım ve Sistem Geliştirici (Tam Zamanlı)</span>
      <span>Ankara, Türkiye</span>
    </div>
    <ul>
      <li>Marketlerde yayında olan 7 farklı mobil uygulama için veri aktarım hatlarını ve REST API bağlantılarını kurdu.</li>
      <li>İşlemci ve bellek profillemesi yaparak iş parçacığı kilitlenmelerini çözdü ve çöp toplayıcı duraklamalarını %25 düşürdü.</li>
      <li>Günlük test sürümlerini ve kurulum adımlarını Python ve PowerShell betikleri yazarak otomatikleştirdi.</li>
      <li>Farklı platformlar arasındaki veri tutarlılığını sağlamak için modüler doğrulama şemaları yazdı.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Projeler</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">Job-Radar: Otonom İlan Tarama ve Eşleştirme Motoru</span>
      <span class="entry-date"><a href="https://github.com/taylan1477/Job-Radar">github.com/taylan1477/Job-Radar</a></span>
    </div>
    <div class="project-tech">Python, Playwright, Pydantic, Scikit-learn, Google Sheets API</div>
    <ul>
      <li>Dinamik web sitelerinden iş ilanlarını bot korumalarına takılmadan çekmek için Playwright tabanlı kazıyıcı geliştirdi.</li>
      <li>İlan metinleriyle özgeçmiş kriterlerini karşılaştırmak için TF-IDF vektörizasyonu ve kosinüs benzerliği kullanan NLP motoru yazdı.</li>
      <li>Çekilen verileri Pydantic modelleriyle doğrulayıp Google E-Tablolar ve Excel dosyalarına aktaran boru hattı kurdu.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">Böbrek BT Segmentasyonu: Geleneksel Görüntü İşleme ve Derin Öğrenme</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477</a></span>
    </div>
    <div class="project-tech">Python, PyTorch, OpenCV, ScaleNorm-UNet, BRISQUE Kalite Filtresi, AMOS Veri Kümesi</div>
    <ul>
      <li>Batın tomografi görüntülerinde klasik özellik çıkarım yöntemleri (HOG, SIFT, CoHOG, LBP) ile ScaleNorm-UNet modelini kıyasladı.</li>
      <li>Düşük kontrastlı ve bozuk görüntüleri ayıklamak için BRISQUE kalite puanlama algoritmasını kullandı.</li>
      <li>Derin öğrenme modelini Dice Loss ve IoU metrikleriyle eğiterek böbrek sınırlarını piksel düzeyinde segmente etti.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">Voice OS (Jarvis): Çevrimdışı Masaüstü Yapay Zeka Asistanı</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477</a></span>
    </div>
    <div class="project-tech">Python, Ollama (Qwen/LLaVA), Faster-Whisper, Win32 IPC, Graphify</div>
    <ul>
      <li>İnternet bağlantısına ihtiyaç duymadan, yerel GPU üzerinde çalışan (Qwen 2.5 7B ve LLaVA 7B) sesli masaüstü asistanı yaptı.</li>
      <li>Faster-Whisper (INT8) ve kullanıcı araya girdiğinde sesi anında kesebilen (interrupt) ses motoru geliştirdi.</li>
      <li>Win32 IPC mekanizmalarıyla masaüstü uygulamalarını kontrol etti ve proje çağrı haritasını AST grafiği ile çıkardı.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Teknik Beceriler</h2>
  <div class="skills-list">
    <p><strong>Yapay Zeka ve Görüntü İşleme:</strong> PyTorch, OpenCV, ScaleNorm-UNet, Scikit-learn, Ollama (Yerel LLM), Faster-Whisper</p>
    <p><strong>Web Kazıma ve Otomasyon:</strong> Playwright, Selenium, Beautiful Soup, Dinamik DOM Çıkarımı, Win32 IPC</p>
    <p><strong>Programlama ve Veri:</strong> Python, C#, Java, SQL, TypeScript, Pydantic, FastAPI, REST API</p>
    <p><strong>Sistemler ve Araçlar:</strong> Docker, Linux (Ubuntu/WSL2), Git, GitHub, Bash, PowerShell, Model Context Protocol (MCP)</p>
  </div>
</section>
"""
    }
]

def check_pdf_pages(pdf_path):
    with open(pdf_path, "rb") as f:
        data = f.read()
    pages = len(re.findall(rb'/Type\s*/Page\b', data))
    return pages

print("--- Building Fully Humanized CV Suite ---")
for item in cv_data:
    fname = item["filename"]
    html_content = HTML_TEMPLATE.format(
        lang=item["lang"],
        name=item["name"],
        title=item["title"],
        body=item["body"].strip()
    )
    
    html_file = os.path.join(HTML_DIR, f"{fname}.html")
    pdf_file = os.path.join(PDF_DIR, f"{fname}.pdf")
    
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_file}",
        html_file
    ]
    
    subprocess.run(cmd, check=True)
    pages = check_pdf_pages(pdf_file)
    print(f"[HUMANIZED READY] {fname}.pdf -> Pages: {pages} (File size: {os.path.getsize(pdf_file)} bytes)")

print("--- All 6 Humanized CVs successfully compiled in Humanized_CV/pdf! ---")
