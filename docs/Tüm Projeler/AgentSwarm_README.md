# Project Jarvis: Autonomous Dev Swarm

## Overview
Project Jarvis is a highly autonomous, multi-agent development environment orchestrated by the advanced capabilities of Gemini 3.1 Pro via Google AI Studio. Designed specifically for a single-device powerhouse setup (Target: HP Victus 16 / WSL2), Jarvis executes coding, refactoring, and testing in parallel without the need for an external cloud VPS. The primary cockpit is JetBrains Rider, interacting with a local, isolated swarm of CLI agents.

## Architecture
*   **Cockpit (Local IDE):** JetBrains Rider on Windows serves as the primary control center. The built-in terminal acts as the interface to the isolated swarm running underneath on WSL2.
*   **Master Orchestrator:** Gemini 3.1 Pro (via Google AI Studio expanded limits) handles high-level system architecture, task distribution, and deep code analysis.
*   **Worker Agents:** Domain-specific CLI instances (e.g., `aider-chat` or `OpenHands`) running inside isolated `tmux` sessions on WSL2. They act autonomously on specific directories (e.g., backend, tests) without interfering with the Windows host.
*   **State & Memory (Local Context):**
    *   **State Sync:** A local PostgreSQL database containerized via Docker Desktop (WSL2 backend), connected through a custom Python Model Context Protocol (MCP) server. This replaces remote solutions (like Kerem Memory) and allows agents to share context and activity logs with zero latency.
*   **Automation:** AutoHotkey v2 (AHK) on Windows for desktop automation, terminal hotstrings (`::/worker`), and rapid prompt injection into the WSL2 terminal.

## Prerequisites
*   **OS & Virtualization:** Windows 11 with WSL2 (Ubuntu 24.04) and Docker Desktop enabled (WSL2 Integration active).
*   **IDE:** JetBrains Rider (or Android Studio).
*   **API Keys:** Valid Google AI Studio `GEMINI_API_KEY` exported in the WSL2 environment.
*   **Tools:** Python 3.10+ (inside WSL2), AutoHotkey v2 (on Windows), `tmux` (inside WSL2).

## Implementation Roadmap

### Phase 1: Environment & IDE Provisioning
- [ ] Install and configure WSL2 (Ubuntu 24.04) on Windows.
- [ ] Set up Docker Desktop with WSL2 integration.
- [ ] Configure JetBrains Rider built-in terminal to attach directly to WSL2 bash automatically upon opening.

### Phase 2: Agent Bootstrapping & Orchestration (WSL2)
- [ ] Install `aider-chat` via pip in the WSL2 Python environment.
- [ ] Configure the master agent and workers to utilize Gemini 3.1 Pro models.
- [ ] Create bootstrap bash scripts (`start_swarm.sh`) to spin up persistent `tmux` sessions for specific domains (e.g., `tmux new-session -s agent-core -d`).

### Phase 3: Persistent Memory & Context (MCP)
- [ ] Deploy the local PostgreSQL instance via `docker-compose.yml` mapped to WSL2 storage.
- [ ] Develop a lightweight Python Model Context Protocol (MCP) Server.
- [ ] Integrate MCP with agents to allow them to read/write project state and maintain a shared chronological memory ("Dün nerede kalmıştık?").

### Phase 4: Desktop Automation (Windows)
- [ ] Develop `.ahk` scripts to map fast terminal commands.
- [ ] Create hotkeys to manage SSH injections and deploy payload templates to the JetBrains terminal instantly.

## Getting Started
1. Clone this repository into your WSL2 file system (`/home/username/projects/`).
2. Open the project folder in JetBrains Rider.
3. Ensure your `GEMINI_API_KEY` is set in your `~/.bashrc` or `~/.zshrc`.
4. Run `./scripts/start_swarm.sh` to initialize the `tmux` sessions and connect the worker agents to the local MCP server.
5. Utilize your configured AHK shortcuts to dispatch tasks to specific workers directly from the Rider terminal.
