import os
import subprocess
import re

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
BASE_DIR = r"c:\Projeler\PycharmProjects\job-radar\cv_suite"
HTML_DIR = os.path.join(BASE_DIR, "html")
PDF_DIR = os.path.join(BASE_DIR, "pdf")

os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

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
    line-height: 1.31;
    -webkit-font-smoothing: antialiased;
  }}
  header {{
    text-align: center;
    margin-bottom: 7px;
  }}
  h1 {{
    font-size: 19pt;
    font-weight: 800;
    letter-spacing: 0.4px;
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
    letter-spacing: 0.6px;
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
    # --------------------------------------------------------------------------
    # CLUSTER 1: Game & Simulation Systems (EN)
    # --------------------------------------------------------------------------
    {
        "filename": "Taylan_Ozdemir_Game_Simulation_CV",
        "lang": "en",
        "name": "Taylan Özgür Özdemir",
        "title": "Game Developer & Simulation Systems Engineer",
        "body": """
<header>
  <h1>Taylan Özgür Özdemir</h1>
  <div class="subtitle">Game Developer & Simulation Systems Engineer</div>
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
      <span>Bachelor of Science in Computer Engineering — <strong>GPA: 3.09 / 4.00</strong></span>
      <span>Malatya, Turkey</span>
    </div>
    <div style="font-size: 8.7pt; color: #4b5563; margin-top: 1px;">
      <em>Relevant Coursework:</em> Data Structures & Algorithms, Object-Oriented Programming, Computer Vision, Distributed Systems, Operating Systems
    </div>
  </div>
</section>

<section>
  <h2>Professional Experience</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">SoloRota</span>
      <span class="entry-date">Jul 2025 – Jan 2026</span>
    </div>
    <div class="entry-subtitle">
      <span><strong>Game Developer</strong> (Full-time)</span>
      <span>Ankara, Turkey (On-site)</span>
    </div>
    <ul>
      <li>Shipped core gameplay loops and state machines for <strong>7 educational mobile games</strong> to Google Play and App Store using Unity (C#).</li>
      <li>Architected an asynchronous data layer for REST API question streams, keeping player state intact across network drops.</li>
      <li>Profiled draw calls and garbage collection overhead via Unity Frame Debugger, stabilizing frame rates at <strong>60 FPS</strong> on mid-tier Android devices.</li>
      <li>Built modular in-game economies and global buff systems on <code>ScriptableObject</code> architecture, cutting cross-module dependencies.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Key Projects</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">Aegis Forge — Tactical Terraforming Multiplayer Shooter</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477/AegisForge</a></span>
    </div>
    <div class="project-tech">Unity, C#, DOTS, Jobs System, Burst Compiler, Native Collections, FishNet, Linux Headless</div>
    <ul>
      <li>Engineered a hybrid OOP + DOP architecture to execute real-time terrain manipulation, decoupling high-level gameplay from intensive data pipelines.</li>
      <li>Implemented multi-threaded height displacement and mesh modification using the <strong>Unity C# Job System</strong> and <strong>Burst Compiler</strong>, achieving sub-millisecond execution over <strong>10,000+ dynamic tiles</strong>.</li>
      <li>Built a deterministic <strong>Event Sourcing</strong> network replication layer deployed on a headless Linux dedicated server with FishNet, eliminating raw mesh bandwidth overhead.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">SoloIdle — Educational Campus Management & Idle Game</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477/SoloIdle</a></span>
    </div>
    <div class="project-tech">Unity 2D, C#, Asynchronous Networking, JSON Serialization, ScriptableObjects</div>
    <ul>
      <li>Engineered a scalable idle economy engine powered by an asynchronous network layer and high-throughput JSON serialization for live API quiz sync.</li>
      <li>Structured mathematical progression algorithms, research trees, and persistence routines with <code>ScriptableObject</code> architecture to eliminate runtime data corruption.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">EvoluCat — 2D Metroidvania Platformer</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477/EvoluCat</a></span>
    </div>
    <div class="project-tech">Unity 2D, C#, Finite State Machines (FSM), Physics2D, Multi-Slot Persistence</div>
    <ul>
      <li>Programmed responsive character controllers featuring wall-jump, telekinesis, and puzzle interactions via hierarchical Finite State Machines.</li>
      <li>Implemented an encrypted multi-slot JSON/binary save-load persistence pipeline tracking player progression across segmented world maps.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Technical Skills</h2>
  <div class="skills-list">
    <p><strong>Game & Simulation Engines:</strong> Unity Engine (2D/3D), Unity DOTS (C# Job System, Burst Compiler, NativeArray), Unreal Engine (Basics)</p>
    <p><strong>Programming Languages:</strong> C#, C++, Python, Java, SQL, TypeScript, Bash</p>
    <p><strong>Networking & Systems:</strong> FishNet, Client-Server Architecture, Linux Headless Dedicated Servers, Event Sourcing, REST APIs</p>
    <p><strong>Architecture & Patterns:</strong> OOP, Data-Oriented Programming (DOP), Finite State Machines (FSM), ScriptableObjects, SOLID</p>
    <p><strong>Developer Tools:</strong> Git, GitHub, Unity Profiler, Frame Debugger, JetBrains Rider, Visual Studio, Docker</p>
  </div>
</section>
"""
    },

    # --------------------------------------------------------------------------
    # CLUSTER 1: Game & Simulation Systems (TR)
    # --------------------------------------------------------------------------
    {
        "filename": "Taylan_Ozdemir_Oyun_Simulasyon_CV_TR",
        "lang": "tr",
        "name": "Taylan Özgür Özdemir",
        "title": "Oyun Geliştirici & Simülasyon Sistemleri Mühendisi",
        "body": """
<header>
  <h1>Taylan Özgür Özdemir</h1>
  <div class="subtitle">Oyun Geliştirici & Simülasyon Sistemleri Mühendisi</div>
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
      <span>Bilgisayar Mühendisliği Lisans — <strong>GANO: 3.09 / 4.00</strong></span>
      <span>Malatya, Türkiye</span>
    </div>
    <div style="font-size: 8.7pt; color: #4b5563; margin-top: 1px;">
      <em>Önemli Dersler:</em> Veri Yapıları ve Algoritmalar, Nesne Yönelimli Programlama, Bilgisayarlı Görü, Dağıtık Sistemler, İşletim Sistemleri
    </div>
  </div>
</section>

<section>
  <h2>Profesyonel Deneyim</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">SoloRota</span>
      <span class="entry-date">Temmuz 2025 – Ocak 2026</span>
    </div>
    <div class="entry-subtitle">
      <span><strong>Oyun Geliştirici (Game Developer)</strong> (Tam Zamanlı)</span>
      <span>Ankara, Türkiye (Yerinde)</span>
    </div>
    <ul>
      <li>Unity (C#) kullanarak Android ve iOS platformları için <strong>7 farklı eğitici mobil oyunun</strong> temel oynanış döngülerini ve durum makinelerini geliştirerek <strong>Google Play ve App Store'da canlıya aldı</strong>.</li>
      <li>Oyun içi dinamik soru akışını ve ilerleme çarpanlarını yöneten asenkron REST API entegrasyonu ve veri saklama katmanını tasarladı.</li>
      <li>Unity Profiler ve Frame Debugger kullanarak bellek sızıntılarını ve çizim çağrılarını (draw call) optimize etti; orta segment mobil cihazlarda <strong>60 FPS</strong> akıcılığı sağladı.</li>
      <li><code>ScriptableObject</code> mimarisiyle modüler ekonomi, ilerleme ve güçlendirme (buff) sistemleri kurarak kod bağımlılıklarını azalttı.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Öne Çıkan Projeler</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">Aegis Forge — Taktiksel Arazi Dönüştürme Çok Oyunculu Nişancı Oyunu</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477/AegisForge</a></span>
    </div>
    <div class="project-tech">Unity, C#, DOTS, Jobs System, Burst Compiler, Native Collections, FishNet, Linux Headless</div>
    <ul>
      <li>Gerçek zamanlı arazi modifikasyonunu gerçekleştirmek için esnek oynanış mantığını yüksek performanslı veri akışından ayıran Hibrit OOP + DOP mimarisi kurdu.</li>
      <li><strong>Unity C# Job System</strong> ve <strong>Burst Compiler</strong> ile arazi yükseklik değişimlerini çok çekirdekli simüle ederek <strong>10.000+ dinamik hücrede</strong> alt-milisaniye işlem süresi elde etti.</li>
      <li>Ağ yükünü azaltmak amacıyla FishNet ile Linux Dedicated Server üzerinde çalışan deterministik <strong>Event Sourcing</strong> replikasyon katmanı geliştirdi.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">SoloIdle — Eğitici Kampüs Yönetim & Idle Oyunu</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477/SoloIdle</a></span>
    </div>
    <div class="project-tech">Unity 2D, C#, Asenkron Ağ Mimarisi, JSON Serileştirme, ScriptableObjects</div>
    <ul>
      <li>Canlı API soru senkronizasyonu için asenkron ağ mimarisi ve yüksek verimli JSON serileştirme katmanıyla desteklenen ölçeklenebilir bir idle ekonomi motoru kodladı.</li>
      <li>Matematiksel ilerleme algoritmaları, araştırma ağaçları ve kalıcı kayıt rutinlerini <code>ScriptableObject</code> mimarisiyle yapılandırarak sıfır veri bozulması sağladı.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">EvoluCat — 2D Metroidvania Platform Oyunu</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477/EvoluCat</a></span>
    </div>
    <div class="project-tech">Unity 2D, C#, Hiyerarşik Durum Makineleri (HFSM), Physics2D, Çoklu Slot Kayıt</div>
    <ul>
      <li>Hiyerarşik Durum Makineleri aracılığıyla telekinezi, duvardan atlama ve bulmaca etkileşimlerini içeren hassas karakter kontrolleri geliştirdi.</li>
      <li>Bölümlü oyun haritasında oyuncu ilerlemesini ve yeteneklerini güvenli saklayan çoklu slotlu JSON/Binary kayıt-yükleme mekanizması kurdu.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Teknik Yetkinlikler</h2>
  <div class="skills-list">
    <p><strong>Oyun & Simülasyon Motorları:</strong> Unity Engine (2D/3D), Unity DOTS (C# Job System, Burst Compiler, NativeArray), Unreal Engine (Temel)</p>
    <p><strong>Programlama Dilleri:</strong> C#, C++, Python, Java, SQL, TypeScript, Bash</p>
    <p><strong>Ağ & Dağıtık Sistemler:</strong> FishNet, İstemci-Sunucu (Client-Server) Mimarisi, Linux Dedicated Server, Event Sourcing, REST API</p>
    <p><strong>Yazılım Mimarisi & Desenler:</strong> OOP, Veri Odaklı Programlama (DOP), Sonlu Durum Makineleri (FSM), ScriptableObjects, SOLID</p>
    <p><strong>Geliştirici Araçları:</strong> Git, GitHub, Unity Profiler, Frame Debugger, JetBrains Rider, Visual Studio, Docker</p>
  </div>
</section>
"""
    },

    # --------------------------------------------------------------------------
    # CLUSTER 2: Automation, AI & Systems (EN)
    # --------------------------------------------------------------------------
    {
        "filename": "Taylan_Ozdemir_Automation_AI_CV",
        "lang": "en",
        "name": "Taylan Özgür Özdemir",
        "title": "Software Engineer — Automation, AI & Systems",
        "body": """
<header>
  <h1>Taylan Özgür Özdemir</h1>
  <div class="subtitle">Software Engineer — Automation, AI & Systems</div>
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
      <span>Bachelor of Science in Computer Engineering — <strong>GPA: 3.09 / 4.00</strong></span>
      <span>Malatya, Turkey</span>
    </div>
    <div style="font-size: 8.7pt; color: #4b5563; margin-top: 1px;">
      <em>Relevant Coursework:</em> Computer Vision, Data Structures & Algorithms, Distributed Systems, Operating Systems, Machine Learning
    </div>
  </div>
</section>

<section>
  <h2>Professional Experience</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">SoloRota</span>
      <span class="entry-date">Jul 2025 – Jan 2026</span>
    </div>
    <div class="entry-subtitle">
      <span><strong>Software & Systems Developer</strong> (Full-time)</span>
      <span>Ankara, Turkey (On-site)</span>
    </div>
    <ul>
      <li>Engineered asynchronous REST API ingestion services and schema validation pipelines for <strong>7 production apps</strong> delivered to live markets.</li>
      <li>Conducted system-level CPU profiling and memory leak tracing, reducing garbage collection spikes by <strong>25%</strong> and ensuring stable throughput.</li>
      <li>Automated build verification pipelines and configuration deployment routines using custom scripts and Git version control workflows.</li>
      <li>Architected decoupled state management layers and event-driven data flow models, accelerating multi-platform build iteration cycles.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Key Projects</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">Job-Radar — Autonomous Web Mining & Candidate Scoring Engine</span>
      <span class="entry-date"><a href="https://github.com/taylan1477/Job-Radar">github.com/taylan1477/Job-Radar</a></span>
    </div>
    <div class="project-tech">Python, Playwright, Pydantic, Scikit-learn, Google Sheets API, Dynamic DOM Scraping</div>
    <ul>
      <li>Developed an end-to-end web scraping engine using <strong>Playwright</strong> to extract job postings across dynamic Single Page Applications (SPAs) while bypassing bot mitigations.</li>
      <li>Built an NLP-driven evaluation algorithm using <strong>TF-IDF vectorization</strong> and cosine similarity to rank candidates against criteria with <strong>90%+ match accuracy</strong>.</li>
      <li>Integrated automated ingestion pipelines syncing validated data to Google Sheets and Excel via Pydantic data schemas.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">Medical CT Image Segmentation — Classical CV vs Deep Learning</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477</a></span>
    </div>
    <div class="project-tech">Python, PyTorch, OpenCV, ScaleNorm-UNet, BRISQUE Quality Assessment, AMOS CT Dataset</div>
    <ul>
      <li>Built a biomedical CT segmentation pipeline benchmarking classical feature extraction (HOG, SIFT, CoHOG, LBP) against <strong>ScaleNorm-UNet</strong>.</li>
      <li>Implemented blind image quality evaluation using <strong>BRISQUE scoring</strong> to filter low-contrast slices, integrated with bilateral and morphological filters.</li>
      <li>Optimized deep learning training runs with custom Dice Loss and IoU metrics, achieving precise boundary delineation on the AMOS CT dataset.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">Voice OS (Jarvis) — Offline Autonomous Edge AI Agent</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477</a></span>
    </div>
    <div class="project-tech">Python, Ollama (Qwen/LLaVA), Faster-Whisper, Win32 IPC / OS Automation, Graphify AST</div>
    <ul>
      <li>Engineered an offline edge AI assistant running local quantized models (Qwen 2.5 7B, LLaVA 7B) on local GPU with zero external cloud dependencies.</li>
      <li>Built a low-latency speech pipeline pairing <strong>Faster-Whisper (INT8)</strong> with an interrupt-driven TTS engine (barge-in support) for real-time interaction.</li>
      <li>Integrated OS-level Win32 IPC, background process orchestration, and desktop automation; mapped codebase architecture via deterministic AST knowledge graphs (Graphify).</li>
    </ul>
  </div>
</section>

<section>
  <h2>Technical Skills</h2>
  <div class="skills-list">
    <p><strong>AI & Machine Learning:</strong> PyTorch, OpenCV, Computer Vision, ScaleNorm-UNet, Scikit-learn, Ollama (Local LLMs), Faster-Whisper, Prompt Engineering</p>
    <p><strong>Web Scraping & Systems Automation:</strong> Playwright, Selenium, Beautiful Soup, Dynamic DOM Extraction, Anti-Bot Handling, Win32 IPC</p>
    <p><strong>Languages & Frameworks:</strong> Python, C#, Java, SQL, TypeScript, Pydantic, FastAPI, REST APIs</p>
    <p><strong>Systems, Infrastructure & Tools:</strong> Docker, Linux (Ubuntu/WSL2), Git, GitHub, Bash, Model Context Protocol (MCP), CI/CD basics</p>
  </div>
</section>
"""
    },

    # --------------------------------------------------------------------------
    # CLUSTER 2: Automation, AI & Systems (TR)
    # --------------------------------------------------------------------------
    {
        "filename": "Taylan_Ozdemir_Otomasyon_AI_CV_TR",
        "lang": "tr",
        "name": "Taylan Özgür Özdemir",
        "title": "Yazılım Mühendisi — Otomasyon, Yapay Zeka & Sistemler",
        "body": """
<header>
  <h1>Taylan Özgür Özdemir</h1>
  <div class="subtitle">Yazılım Mühendisi — Otomasyon, Yapay Zeka & Sistemler</div>
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
      <span>Bilgisayar Mühendisliği Lisans — <strong>GANO: 3.09 / 4.00</strong></span>
      <span>Malatya, Türkiye</span>
    </div>
    <div style="font-size: 8.7pt; color: #4b5563; margin-top: 1px;">
      <em>Önemli Dersler:</em> Bilgisayarlı Görü, Veri Yapıları ve Algoritmalar, Dağıtık Sistemler, İşletim Sistemleri, Makine Öğrenmesi
    </div>
  </div>
</section>

<section>
  <h2>Profesyonel Deneyim</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">SoloRota</span>
      <span class="entry-date">Temmuz 2025 – Ocak 2026</span>
    </div>
    <div class="entry-subtitle">
      <span><strong>Yazılım & Sistem Geliştirici</strong> (Tam Zamanlı)</span>
      <span>Ankara, Türkiye (Yerinde)</span>
    </div>
    <ul>
      <li>Asenkron REST API ve veri doğrulama hatlarını kurarak <strong>7 üretim uygulamasının canlı veri akışını sağladı</strong>.</li>
      <li>Sistem düzeyinde bellek ve işlemci profil analizleri yürüterek çöp toplayıcı (GC) kaynaklı gecikmeleri <strong>%25</strong> oranında azalttı ve stabil veri akışı sağladı.</li>
      <li>Yapı doğrulama (build verification) ve konfigürasyon dağıtım süreçlerini özel betikler ve Git iş akışları ile otomatik hale getirdi.</li>
      <li>Olay güdümlü (event-driven) modüler durum yönetimi mimarisi kurarak çok platformlu sürümlerin geliştirme döngülerini kısalttı.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Öne Çıkan Projeler</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">Job-Radar — Otonom Veri Madenciliği & Aday Puanlama Motoru</span>
      <span class="entry-date"><a href="https://github.com/taylan1477/Job-Radar">github.com/taylan1477/Job-Radar</a></span>
    </div>
    <div class="project-tech">Python, Playwright, Pydantic, Scikit-learn, Google Sheets API, Dinamik DOM Kazıma</div>
    <ul>
      <li><strong>Playwright</strong> ile dinamik Tek Sayfa Uygulamalarından (SPA) veri çeken, bot korumalarını ve hız limitlerini yöneten robust bir web scraping motoru geliştirdi.</li>
      <li>İlan gereksinimleri ile profil kriterlerini <strong>TF-IDF vektörizasyonu</strong> ve kosinüs benzerliği ile eşleştiren <strong>%90+ doğruluklu</strong> bir NLP skorlama algoritması kodladı.</li>
      <li>Çekilen verileri Pydantic şemaları ile doğrulayarak Google Sheets ve Excel üzerine otomatik aktaran uçtan uca veri boru hattı kurdu.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">Medikal BT Görüntü Segmentasyonu — Klasik Görüntü İşleme vs Derin Öğrenme</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477</a></span>
    </div>
    <div class="project-tech">Python, PyTorch, OpenCV, ScaleNorm-UNet, BRISQUE Kalite Filtresi, AMOS Veri Kümesi</div>
    <ul>
      <li>Tıbbi BT (Tomografi) görüntülerinde böbrek bölgesi tespiti için klasik özellik mühendisliği (HOG, SIFT, CoHOG, LBP) ile <strong>ScaleNorm-UNet</strong> mimarisini karşılaştıran uçtan uca bir sistem geliştirdi.</li>
      <li>Düşük kontrastlı kesitleri otomatik ayıklamak için <strong>BRISQUE</strong> referanssız görüntü kalite skorlama mekanizması ve morfolojik filtreler tasarladı.</li>
      <li>Dice Loss ve IoU fonksiyonları ile optimize edilen derin öğrenme modelinde AMOS veri kümesi üzerinde piksel düzeyinde sınır doğruluğu yakaladı.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">Voice OS (Jarvis) — Çevrimdışı Otonom Edge AI İşletim Sistemi Ajanı</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477</a></span>
    </div>
    <div class="project-tech">Python, Ollama (Qwen/LLaVA), Faster-Whisper, Win32 IPC / İşletim Sistemi Otomasyonu, Graphify AST</div>
    <ul>
      <li>Bulut bağımlılığı olmadan yerel GPU üzerinde kuantize modeller (Qwen 2.5 7B, LLaVA 7B) çalıştıran <strong>%100 yerel ve güvenli</strong> sesli yapay zeka mimarisi kurdu.</li>
      <li><strong>Faster-Whisper (INT8)</strong> ve konuşma anında sesi milisaniyeler içinde kesebilen (interrupt / barge-in) hibrit TTS motoru ile düşük gecikmeli konuşma döngüsü sağladı.</li>
      <li>İşletim sistemi düzeyinde Win32 IPC, arka plan süreç orkestrasyonu ve masaüstü otomasyonunu entegre etti; mimariyi deterministik AST kod grafiği (Graphify) ile yönetti.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Teknik Yetkinlikler</h2>
  <div class="skills-list">
    <p><strong>Yapay Zeka & Görüntü İşleme:</strong> PyTorch, OpenCV, Computer Vision, ScaleNorm-UNet, Scikit-learn, Ollama (Yerel LLM'ler), Faster-Whisper</p>
    <p><strong>Web Kazıma & Sistem Otomasyonu:</strong> Playwright, Selenium, Beautiful Soup, Dinamik DOM Çıkarımı, Anti-Bot Yönetimi, Win32 IPC</p>
    <p><strong>Programlama Dilleri & Kütüphaneler:</strong> Python, C#, Java, SQL, TypeScript, Pydantic, FastAPI, RESTful API'ler</p>
    <p><strong>Sistemler, Altyapı & Araçlar:</strong> Docker, Linux (Ubuntu/WSL2), Git, GitHub, Bash, Model Context Protocol (MCP), CI/CD temelleri</p>
  </div>
</section>
"""
    },

    # --------------------------------------------------------------------------
    # CLUSTER 3: Software & Media Systems (EN)
    # --------------------------------------------------------------------------
    {
        "filename": "Taylan_Ozdemir_Software_Systems_CV",
        "lang": "en",
        "name": "Taylan Özgür Özdemir",
        "title": "Software Engineer — Backend, Desktop & Fullstack Systems",
        "body": """
<header>
  <h1>Taylan Özgür Özdemir</h1>
  <div class="subtitle">Software Engineer — Backend, Desktop & Fullstack Systems</div>
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
      <span>Bachelor of Science in Computer Engineering — <strong>GPA: 3.09 / 4.00</strong></span>
      <span>Malatya, Turkey</span>
    </div>
    <div style="font-size: 8.7pt; color: #4b5563; margin-top: 1px;">
      <em>Relevant Coursework:</em> Object-Oriented Software Engineering, Database Management Systems, Distributed Systems, Operating Systems, Computer Networks
    </div>
  </div>
</section>

<section>
  <h2>Professional Experience</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">SoloRota</span>
      <span class="entry-date">Jul 2025 – Jan 2026</span>
    </div>
    <div class="entry-subtitle">
      <span><strong>Software Engineer</strong> (Full-time)</span>
      <span>Ankara, Turkey (On-site)</span>
    </div>
    <ul>
      <li>Engineered modular domain services and asynchronous data pipelines for <strong>7 production applications</strong> deployed to live app ecosystems.</li>
      <li>Designed resilient REST API communication layers handling real-time data serialization, edge-case error recovery, and token authentication.</li>
      <li>Profiled runtime CPU bottlenecks and garbage collection allocations, improving multi-threaded execution stability and reducing latency by <strong>25%</strong>.</li>
      <li>Established structured Git versioning, automated build delivery workflows, and testable code boundaries following SOLID principles.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Key Projects</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">MassVideoCutter — Batch Video Processing & Trimming Suite</span>
      <span class="entry-date"><a href="https://github.com/taylan1477/MassVCutter">github.com/taylan1477/MassVCutter</a></span>
    </div>
    <div class="project-tech">Java 23, JavaFX 23, Spring Boot 4, PostgreSQL 15, Flyway, Multi-threading, FFmpeg</div>
    <ul>
      <li>Engineered a high-throughput video processing desktop suite utilizing <strong>JavaFX</strong> and multi-threaded <strong>FFmpeg/FFprobe</strong> process wrappers for automated batch intro/outro removal.</li>
      <li>Built acoustic analysis algorithms (<code>VolumeAnalyzer</code>, <code>AudioAnalyzer</code>) analyzing decibel variations (<code>astats</code>) to detect intro sequences automatically.</li>
      <li>Applied <strong>Facade</strong> and <strong>Strategy</strong> design patterns to decouple video trimming engines, timeline waveform generators, and queue schedulers.</li>
      <li>Integrated a community recipe sync layer via <strong>Spring Boot 4</strong> and <strong>PostgreSQL 15</strong> with Flyway database migration scripts.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">CineNode — Zero-Transcode Media Automation & Containerized Stack</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477</a></span>
    </div>
    <div class="project-tech">Python, Docker, Telegram Bot API, Plex Media Server, Radarr, Prowlarr, Linux</div>
    <ul>
      <li>Designed an automated 4K media server operating under a <strong>Zero-Transcode (Direct Play)</strong> policy, eliminating hardware transcode bottlenecks and bandwidth congestion.</li>
      <li>Developed a swarm seeder modeling algorithm (<code>eff_seeders = round(seeders * 0.25)</code>) to eliminate dead torrents and optimize ingress traffic.</li>
      <li>Containerized and deployed a microservice ecosystem (Plex, qBittorrent, Radarr, Prowlarr) managed via an asynchronous <strong>Telegram Bot API</strong> with live download tracking.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">FitConnect — Full Stack Mobile & Cloud Gym Ecosystem</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477</a></span>
    </div>
    <div class="project-tech">React Native (Expo SDK 57), TypeScript, Supabase (PostgreSQL), Deno Edge Functions, QR Engine</div>
    <ul>
      <li>Engineered an end-to-end full stack mobile ecosystem featuring a TypeScript/React Native frontend integrated with a Supabase PostgreSQL backend.</li>
      <li>Configured <strong>Row Level Security (RLS)</strong> policies and deployed Deno-based <strong>Supabase Edge Functions</strong> for RBAC-governed user provisioning and billing.</li>
      <li>Implemented real-time volume/tonnage computation algorithms and timestamped dynamic QR verification modules for fraud-proof session check-ins.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Technical Skills</h2>
  <div class="skills-list">
    <p><strong>Languages & Core Tech:</strong> Java (Java 23, JavaFX), C#, Python, TypeScript, SQL (PostgreSQL), C++</p>
    <p><strong>Backend & Fullstack:</strong> Spring Boot 4, .NET Core / ASP.NET, React Native (Expo), Supabase, RESTful APIs, Flyway, Deno</p>
    <p><strong>Media & Audio/Video Engineering:</strong> FFmpeg, FFprobe, Video/Audio Transcoding, 48kHz Opus Codec, Waveform Visualization</p>
    <p><strong>Architecture & Patterns:</strong> Object-Oriented Design (OOD), SOLID, Facade, Strategy, Multi-threading, Microservices, RLS</p>
    <p><strong>DevOps, Systems & Tools:</strong> Docker, Linux (Ubuntu/WSL2), Git, GitHub, Maven, Postman, JetBrains IntelliJ & Rider</p>
  </div>
</section>
"""
    },

    # --------------------------------------------------------------------------
    # CLUSTER 3: Software & Media Systems (TR)
    # --------------------------------------------------------------------------
    {
        "filename": "Taylan_Ozdemir_Yazilim_Sistemleri_CV_TR",
        "lang": "tr",
        "name": "Taylan Özgür Özdemir",
        "title": "Yazılım Mühendisi — Backend, Masaüstü & Full Stack Sistemler",
        "body": """
<header>
  <h1>Taylan Özgür Özdemir</h1>
  <div class="subtitle">Yazılım Mühendisi — Backend, Masaüstü & Full Stack Sistemler</div>
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
      <span>Bilgisayar Mühendisliği Lisans — <strong>GANO: 3.09 / 4.00</strong></span>
      <span>Malatya, Türkiye</span>
    </div>
    <div style="font-size: 8.7pt; color: #4b5563; margin-top: 1px;">
      <em>Önemli Dersler:</em> Nesne Yönelimli Yazılım Mühendisliği, Veritabanı Yönetim Sistemleri, Dağıtık Sistemler, İşletim Sistemleri, Bilgisayar Ağları
    </div>
  </div>
</section>

<section>
  <h2>Profesyonel Deneyim</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">SoloRota</span>
      <span class="entry-date">Temmuz 2025 – Ocak 2026</span>
    </div>
    <div class="entry-subtitle">
      <span><strong>Yazılım Mühendisi (Software Engineer)</strong> (Tam Zamanlı)</span>
      <span>Ankara, Türkiye (Yerinde)</span>
    </div>
    <ul>
      <li>Canlıya alınan <strong>7 farklı uygulama</strong> için modüler servisleri ve asenkron veri boru hatlarını geliştirip test ederek <strong>canlı marketlere dağıttı</strong>.</li>
      <li>Gerçek zamanlı veri serileştirme, uç durum hata kurtarma ve token yetkilendirme süreçlerini yöneten dayanıklı REST API katmanları tasarladı.</li>
      <li>Çalışma anı işlemci darboğazlarını ve bellek tahsislerini profilleyerek çok iş parçacıklı yürütme kararlılığını artırdı; gecikmeleri <strong>%25</strong> düşürdü.</li>
      <li>SOLID prensiplerine uygun, test edilebilir kod sınırları kurdu; yapılandırılmış Git sürüm kontrolü ve otomatik dağıtım akışları uyguladı.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Öne Çıkan Projeler</h2>
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">MassVideoCutter — Toplu Video İşleme & Kırpma Paketi</span>
      <span class="entry-date"><a href="https://github.com/taylan1477/MassVCutter">github.com/taylan1477/MassVCutter</a></span>
    </div>
    <div class="project-tech">Java 23, JavaFX 23, Spring Boot 4, PostgreSQL 15, Flyway, Çok İş Parçacıklı FFmpeg</div>
    <ul>
      <li>Dizi ve video arşivlerinden intro/outro jeneriklerini otomatik ayıklamak için <strong>JavaFX</strong> ve çok iş parçacıklı <strong>FFmpeg/FFprobe</strong> süreç yöneticisi mimarisi kurdu.</li>
      <li>Ses dalgalanmalarını (<code>VolumeAnalyzer</code>, <code>AudioAnalyzer</code>) desibel analizleriyle (<code>astats</code>) inceleyerek jenerik geçişlerini tespit eden algoritmalar kodladı.</li>
      <li>Video kırpma motorunu, dalga formu oluşturucuları ve görev kuyruklarını soyutlamak için <strong>Facade</strong> ve <strong>Strategy</strong> tasarım desenlerini uyguladı.</li>
      <li>Toplu kırpma tariflerini (.trimrecipe) bulutta paylaşan ve derecelendiren REST API altyapısını <strong>Spring Boot 4</strong>, <strong>PostgreSQL 15</strong> ve Flyway ile entegre etti.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">CineNode — Sıfır-Transcode Medya Otomasyonu & Docker Mimarisi</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477</a></span>
    </div>
    <div class="project-tech">Python, Docker, Telegram Bot API, Plex Media Server, Radarr, Prowlarr, Linux</div>
    <ul>
      <li>Donanım transcode darboğazlarını ortadan kaldıran ve bant genişliğini koruyan <strong>Sıfır-Transcode (Direct Play)</strong> politikasıyla çalışan 4K kişisel medya sunucusu mimariledi.</li>
      <li>Ölü veya yavaş torrentleri engelleyerek ağ trafiğini koruyan dinamik bir swarm seeder analiz algoritması (<code>eff_seeders = round(seeders * 0.25)</code>) geliştirdi.</li>
      <li>Mikroservis ekosistemini (Plex, qBittorrent, Radarr, Prowlarr) Docker üzerinde konteynerize edip canlı indirme takipli asenkron bir <strong>Telegram Bot API</strong> servisi ile dağıttı.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">FitConnect — Full Stack Mobil & Bulut Spor Ekosistemi</span>
      <span class="entry-date"><a href="https://github.com/taylan1477">github.com/taylan1477</a></span>
    </div>
    <div class="project-tech">React Native (Expo SDK 57), TypeScript, Supabase (PostgreSQL), Deno Edge Functions, QR Doğrulama</div>
    <ul>
      <li>React Native (TypeScript) ön yüzü ile Supabase PostgreSQL arka yüzünü entegre eden uçtan uca modern bir <strong>full stack mobil ekosistem</strong> geliştirdi.</li>
      <li>Rol bazlı erişim denetimi (RBAC) için <strong>Row Level Security (RLS)</strong> güvenlik politikalarını ve Deno tabanlı <strong>Supabase Edge Functions</strong> servislerini üretime sundu.</li>
      <li>Canlı antrenman seanslarında dinamik toplam tonaj hesaplama motoru ve sahteciliği önleyen zaman damgalı QR kod doğrulama altyapısı inşa etti.</li>
    </ul>
  </div>
</section>

<section>
  <h2>Teknik Yetkinlikler</h2>
  <div class="skills-list">
    <p><strong>Diller & Çekirdek:</strong> Java (Java 23, JavaFX), C#, Python, TypeScript, SQL (PostgreSQL), C++</p>
    <p><strong>Backend & Full Stack:</strong> Spring Boot 4, .NET Core / ASP.NET, React Native (Expo), Supabase, RESTful API'ler, Flyway, Deno</p>
    <p><strong>Medya & Ses/Görüntü İşleme:</strong> FFmpeg, FFprobe, Video/Ses Kodlama (Transcoding), 48kHz Opus Codec, Waveform Görselleştirme</p>
    <p><strong>Mimari & Tasarım Desenleri:</strong> Nesne Yönelimli Tasarım (OOD), SOLID, Facade, Strategy, Çok İş Parçacıklı Programlama (Multi-threading), RLS</p>
    <p><strong>DevOps, Sistemler & Araçlar:</strong> Docker, Linux (Ubuntu/WSL2), Git, GitHub, Maven, Postman, JetBrains IntelliJ & Rider</p>
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

print("--- Running Humanizer Hardening & Recompiling PDFs ---")
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
    print(f"[HUMANIZED OK] {fname}.pdf -> Pages: {pages} (File size: {os.path.getsize(pdf_file)} bytes)")

print("--- All 6 Humanized CVs successfully compiled! ---")
