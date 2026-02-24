# corpus.py
# Bu dosya NLP modelleri için kullanılan geniş metin veri setlerini içerir.

# ──────────────────────────────────────────────
# TF-IDF Corpus – Gelismis Alan Tespiti (Scorer v2)
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
        oculus quest vive hololens
    """,
    "c#": """
        c# developer .net developer .net core asp.net mvc web api
        entity framework dapper linq wpf winforms uwp xamarin maui blazor
        microservices dependency injection solid principles design patterns
        azure cloud functions service bus
        c# engineer backend developer software engineer
    """,
    "python": """
        python developer django flask fastapi tornado aiohttp
        pandas numpy scikit-learn pytorch tensorflow keras
        data science machine learning deep learning ai artificial intelligence
        nlp computer vision data engineer etl pipeline airflow
        celery redis rabbitmq postgresql sqlalchemy
        automation scripting web scraping beautifulsoup selenium scrapy
        yapay zeka makine öğrenmesi veri bilimi
    """,
    "c++": """
        c++ developer cpp engineer embedded systems real-time low latency
        high performance computing hpc multithreading concurrency
        pointers memory management stl boost qt framework
        driver development kernel module firmware
        automotive aerospace defense finance trading systems
        image processing signal processing
    """,
    "mobile": """
        mobile developer android ios cross-platform native
        kotlin java swift objective-c flutter dart react native
        xcode android studio gradle cocoapods
        mobile ui ux material design cupertino
        mobil uygulama geliştirici mobil mühendis
    """,
    "java": """
        java developer spring boot spring mvc hibernate jpa
        jakarta ee j2ee enterprise application
        microservices rest api soap maven gradle
        kafka elasticsearch docker kubernetes
        backend engineer server side distributed systems
    """,
    "cv": """
        computer vision image processing opencv yolo
        object detection face recognition segmentation tracking
        lidar point cloud slam photogrammetry
        deep learning cnn rnn gan transformer
        görüntü işleme bilgisayarlı görü
    """,
    "frontend": """
        frontend developer web developer ui developer javascript typescript
        react vue angular svelte next.js nuxt.js
        html css sass less tailwind bootstrap
        redux mobx context api webpack vite
        responsive design accessibility wcag
    """,
    "backend": """
        backend developer server side api development database design
        sql nosql redis memcached caching message queue
        system architecture scalability security authentication authorization
        oauth jwt rest graphql grpc
        nodejs go golang ruby php laravel
    """
}
