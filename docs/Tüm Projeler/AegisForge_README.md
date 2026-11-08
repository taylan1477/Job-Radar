# 🛡️ AEGIS FORGE
### 🌍 Tactical Terraforming Multiplayer Shooter

> ⚔️ Competitive, multi-phase, environment-shaping action game blending strategic terrain manipulation and TPS hero combat.

---

## 🎯 1. HIGH CONCEPT

**AEGIS FORGE** is a competitive multiplayer game where **strategic decisions physically reshape the battlefield**.

Each match consists of two distinct phases:

1. 🤖 **Captain Phase:** Strategic Terraforming Duel (TPS)
2. 🦸 **Hero Phase:** Tactical Squad Combat (TPS)

💡 **The core technical and gameplay innovation:**  
Terrain is not static. It is a tactical weapon modified in real-time.

---

## 🏛️ 2. CORE DESIGN PILLARS

### 🧱 2.1 Strategy Becomes Physical
Captain decisions are permanently reflected in terrain topology.

### ⚙️ 2.2 Deterministic Evolution
The battlefield evolves dynamically every match through a heavily optimized, event-sourced terrain system.

### ⏱️ 2.3 Phase-Based Mastery
- **Phase 1** = Strategic macro & environment control  
- **Phase 2** = Mechanical execution & tactical combat

---

## ⚔️ 3. MATCH STRUCTURE

### 🌋 PHASE 1 — CAPTAIN DUEL (TPS MODE)
- **Overview:** 1 Captain per team (Heavy Mecha units) on neutral, modifiable terrain.
- **Objectives:** Damage opponent captain and gain terrain control (create choke points, high ground, hazards).
- **Element System (MVP Scope):**
  1. 🔥 **Magma (Lava):** Area damage over time, creates hazardous zones, melts ice.
  2. ❄️ **Glacier (Ice):** Creates slippery surfaces, freezes water/terrain, slows movement.

### 🔫 PHASE 2 — HERO COMBAT (TPS MODE)
- **Overview:** Terrain state locks. Tactical squad combat begins in the newly forged environment.
- **Hero Archetypes (MVP Scope):**
  1. 🏃 **Vanguard:** High mobility, close-to-mid range damage.
  2. 🛡️ **Architect:** Defense and area denial. Utilizes modified terrain.

---

## 🧠 4. ENGINEERING PHILOSOPHY: HYBRID ARCHITECTURE (OOP + DOP)

To solve the conflicting requirements of flexible gameplay programming and massive real-time data processing, **Aegis Forge utilizes a Hybrid Architecture.**

### 🧩 4.1 Object-Oriented Programming (OOP) for Flexibility
Standard OOP principles (Encapsulation, Inheritance, Polymorphism) are used for high-level game logic where flexibility and rapid iteration are required:
- 🌐 Network state management (FishNet)
- 🎮 Match State Machine (`GameManager`)
- ✨ Hero/Mecha Ability Systems (ScriptableObjects)
- 🖼️ User Interfaces (UI)

### 🏎️ 4.2 Data-Oriented Programming (DOP) for Performance
To manipulate thousands of terrain tiles simultaneously without CPU cache misses or frame drops, the core terrain processing completely bypasses traditional `MonoBehaviour` structures. It leverages **Data-Oriented Design (DOD)** principles:
- 📦 **Separation of Data and Logic:** Terrain tile data is stored contiguously in memory using `NativeArrays` rather than scattered object instances.
- 🧵 **Unity C# Job System:** Terrain deformation calculations are distributed across multiple CPU cores (Multi-threading).
- 🚀 **Burst Compiler:** C# math and logic are aggressively optimized into highly vectorized machine code.

---

## 🗺️ 5. TERRAIN SYSTEM DESIGN (THE CORE TECH)

Terrain manipulation is the technical centerpiece of Aegis Forge.

### 🎯 Target Approach
- 🟩 Modular Tile/Grid Injection mapped to `NativeArray` buffers.
- 🎨 Shader-Based Surface Effects driven by procedural textures or buffer uploads.
- ⛰️ Height Displacement Simulation executed via parallel Jobs.

### 📏 Design Goals
- 📡 Network efficient replication (minimal payload).
- 💾 Persistent, replayable match state.
- ⚡ Sub-millisecond execution time for processing 10,000+ tile modifications.

---

## ☁️ 6. MULTIPLAYER ARCHITECTURE

### 📏 Target Scale (Vertical Slice)
- 🧑‍🤝‍🧑 2v2 
- 🐧 **Cloud-Hosted Dedicated Server Model (Linux)**
- 🔄 Deterministic Terrain Replication

### 🎬 The "Event Sourcing" Paradigm
To solve the complex issue of syncing massive terrain changes over a network, **AEGIS FORGE utilizes an Event Sourcing architecture running on a headless Linux Dedicated Server.** 
1. 📤 The client sends an input command to the cloud server.
2. 🛡️ The Dedicated Server validates and generates a `TerrainEvent` (e.g., `RaiseTerrainCommand`, `ChangeSurfaceCommand`).
3. 📢 The Server broadcasts this deterministic Event ID and its parameters (position, radius) to all connected clients.
4. 📥 Clients receive the event and replay the deterministic modification locally via the Job System.

---

## 📊 7. TECHNICAL ARCHITECTURE DIAGRAM

```text
                    +-------------------------------------------+
                    | ☁️      CLOUD DEDICATED SERVER (LINUX)     |
                    |-------------------------------------------|
                    | - FishNet Server Manager                  |
                    | - Match State Machine & Phase Controller  |
                    | - Authoritative Terrain Validation        |
                    +--------------------+----------------------+
                                         |
                                         | 📡 (Network Sync Layer)
                                         v
                    +--------------------+----------------------+
                    | 💻         CLIENT ENVIRONMENT             |
                    +--------------------+----------------------+
                    | TerrainEventSystem | <--- 🎬 EVENT SOURCING CORE
                    |--------------------|
                    | - Command Queue    |
                    | - Event Replay     |
                    +---------+----------+
                              |
                              v
                    +--------------------+
                    | ⛰️ Terrain Manager  | <--- 🏎️ DOP HYBRID LAYER
                    |--------------------|
                    | + NativeArrays     | (Contiguous Memory)
                    | + C# Job System    | (Multi-threading)
                    | + Burst Compiler   | (Vectorized Math)
                    +--------------------+
```

---

## 🚀 8. VERTICAL SLICE SCOPE (MVP)

**Minimum Deliverable for Portfolio Presentation:**
- 🗺️ **1 Map** (Grid/Tile based neutral arena)
- 🧪 **2 Elements** (Magma + Glacier)
- 🤖 **2 Captain Mechas & 2 Hero Classes**
- 🎥 **1 Unified Camera Perspective** (TPS)
- ☁️ **Cloud-Hosted Event-Sourced Terrain Replication (Linux Dedicated Server)**
- ⚡ **Burst-Compiled, Jobified Terrain Processing**

---

## 🛠️ 9. TECH STACK

**Engine:**
- ⬛ Unity 6.3.10f1 (LTS) (C#)
- 🐧 **Linux Dedicated Server Build Support**

**Systems & Frameworks:**
- 🌐 **Networking:** FishNet (Fish-Networking) for Server-Authoritative state management.
- 🏎️ **Performance:** Unity C# Job System, Burst Compiler, Native Collections.
- ☁️ **Cloud Infrastructure:** Target deployment on AWS EC2 / Azure (Ubuntu Linux).
- 🎨 **Render Pipeline:** Universal Render Pipeline (URP).
- ⌨️ **Input:** Unity New Input System.
- 🏗️ **Architecture:** Event-Driven Architecture, ScriptableObject-based data management, DOP for heavy calculations.

---

## 📂 10. PROJECT FOLDER STRUCTURE

```text
Assets/
├── 🎨 Art/                # 3D Models, Materials, Textures
├── 🎵 Audio/              # Sound effects and music
├── ⚙️ Core/               # GameManager, Bootstrapper, State Machine
├── 📄 Data/               # ScriptableObjects (Abilities, Elements)
├── 🎮 Inputs/             # Unity New Input System mappings
├── 📡 Networking/         # FishNet NetworkManager settings, custom network scripts
├── 📦 Prefabs/            # Characters, Terrain Tiles, UI Panels
├── 🎬 Scenes/             # MainMenu, GameScene, Test_Terrain
├── 💻 Scripts/            # Source Code
│   ├── ✨ Abilities/      # Hero/Mecha abilities and execution (OOP)
│   ├── 🏃 Character/      # Movement and animation controllers (OOP)
│   ├── ⛰️ Terrain/        # TerrainManager, TerrainEventSystem, Jobs (DOP)
│   └── 🖼️ UI/             # User interface logic (OOP)
└── 🖼️ UI_Assets/          # Icons, Fonts, Canvas elements
Plugins/                   # FishNet and other 3rd party assets
Settings/                  # URP, Input, Tag/Layer settings
```