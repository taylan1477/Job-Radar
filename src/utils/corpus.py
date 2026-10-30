# corpus.py
# Bu dosya NLP modelleri için kullanılan geniş metin veri setlerini içerir.

# ──────────────────────────────────────────────
# TF-IDF Corpus – Genisletilmis 7 Alan Modeli
# ──────────────────────────────────────────────
EXPANDED_FIELD_CORPUS = {
    "gamedev": """
        game developer game designer game programmer game artist game producer
        unity unreal engine godot cocos2d gamemaker defold phaser
        c++ c# lua shader glsl hlsl directx opengl vulkan metal
        3d math physics engine gameplay mechanics level design
        mobile game video game pc game console game hyper casual midcore aaa
        playables playable ads game economy monetization
        oyun geliştirici oyun tasarımcı oyun programcı oyun stüdyosu
        render pipeline graphics programming animation rigging skinning
        multiplayer networking photon mirror fishnet
        virtual reality vr augmented reality ar mixed reality xr
        oculus quest vive hololens technical artist
    """,
    "savunma_simülasyon": """
        simülasyon mühendisi simulation engineer modelleme simülasyon askeri simülasyon
        taktik simülasyon c4isr harp oyunu radar simülasyon uçuş simülatörü
        sistem entegrasyon mühendisi system integration ara katman middleware dev
        gömülü sistem entegrasyon arayüz dds rti dds open dds dis hla high level architecture
        savunma sanayii aselsan havelsan rokesan tusaş tai ssb milli savunma
        real time avionics telemetri sensör füzyonu donanım yazılım entegrasyon
    """,
    "yazılım": """
        software engineer yazılım mühendisi software developer yazılım geliştirici
        backend developer frontend developer full stack fullstack web developer
        api development rest graphql grpc microservices web api web services
        mobile developer mobil geliştirici android ios flutter react native swift kotlin
        test engineer test otomasyon sdet qa quality assurance test mühendisi
        javascript typescript react vue angular nodejs python c# java go golang
        clean code solid design patterns unit test integration test
    """,
    "sistem_network": """
        sistem yöneticisi system administrator sysadmin noc mühendisi network operations center
        network engineer ağ mühendisi it operasyon uzmanı ağ otomasyonu network automation
        veri merkezi data center sunucu yönetimi server management linux administrator
        windows server active directory vmware esxi hyper v proxmox
        cisco switch router firewall vpn routing switching tcp ip dns dhcp
        site reliability engineer sre infrastructure altyapı monitoring zabbix nagios prometheus grafana
        bash scripting powershell ansible devops cloud aws azure
    """,
    "veri_bi": """
        veritabanı yöneticisi dba database administrator sql server postgresql oracle mysql
        database tuning indexleme backup restore replikasyon cluster
        iş zekası bi developer business intelligence etl developer veri ambarı data warehouse
        power bi tableau qlik ssas ssis ssrs talend databricks snowflake
        veri madenciliği data mining web scraping crawler spider selenium scrapy
        veri analisti data analyst büyük veri big data hadoop spark
    """,
    "endüstriyel_otomasyon": """
        erp geliştiricisi erp uzmanı sap abap dynamics 365 erp danışmanı canias logo netsis
        endüstriyel otomasyon mühendisi scada plc siemens tia portal s7 omron hmi
        süreç otomasyonu process automation rpa uipath blue prism power automate
        wms depo yönetim sistemleri depo otomasyonu lojistik yazılımları barkod rfid
        ürün mühendisi product engineer donanım yazılım test prototip üretim hattı
        streaming video mühendisi ffmpeg video encoding canlı yayın vod mam medya arşiv
    """,
    "diğer": """
        uygulama destek mühendisi application support app support l2 l3 helpdesk
        bt iş analisti it business analyst sistem analisti gereksinim analizi
        saha entegrasyon mühendisi field engineer teknik destek troubleshooting
        genel teknik operasyon müşteri sahası donanım kurulumu
    """
}
