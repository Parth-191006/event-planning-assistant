# 🎓 Event Planning Assistant

**An AI-powered multi-agent system that automates college event planning from research to execution.**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![Gemini](https://img.shields.io/badge/Gemini-API-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture Diagram](#-architecture-diagram)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Agent Details](#-agent-details)
- [API Integration](#-api-integration)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 📖 Overview

College students and organizations struggle with the fragmented, time-consuming process of event planning. Finding venues, designing themes, writing invitations, and creating budgets requires multiple tools and significant expertise.

**Event Planning Assistant** solves this by using a **multi-agent AI architecture** where specialized agents collaborate to handle the entire planning workflow:

1. 🔍 **Research Agent** finds real venues using web search
2. 🎨 **Design Agent** creates visual themes and color palettes
3. ✍️ **Copy Agent** writes invitations, scripts, and social posts
4. 📦 **Packaging Agent** assembles everything into a professional report
5. 🧠 **Judge Agent** evaluates output quality (LLM-as-Judge)

The system is deployed live on Railway with a user-friendly Streamlit interface.

---

## ✨ Features

### Core Features
- ✅ **Real-Time Venue Search** - Uses Tavily API to find actual venues in your location
- ✅ **AI-Generated Themes** - Custom color palettes, mood keywords, and layout suggestions
- ✅ **Professional Copywriting** - Invitations, MC scripts, and social media posts
- ✅ **Budget Breakdown** - Automatic cost allocation across categories
- ✅ **Quality Evaluation** - LLM-as-Judge scores plans on completeness, creativity, and clarity
- ✅ **Downloadable Reports** - Export plans as Markdown files
- ✅ **Graceful Fallbacks** - Never crashes; uses mock data when API quotas are exceeded

### Advanced Features
- 🔐 **Secure API Key Management** - Environment variables via `.env`
- 🔄 **Session State Management** - Preserves data across Streamlit reruns
- 📊 **Interactive UI** - Real-time status updates during generation
- 🌐 **Live Deployment** - Public URL accessible anywhere
- 🧪 **Modular Testing** - Each agent has standalone test blocks

---

## 🏗️ Architecture Diagram
graph TD
    User[👤 User Input<br/>Event Type, Location, Budget, Guests, Theme] --> UI[🖥️ Streamlit Web UI]
    UI --> Research[🔍 Research Agent<br/>Venue Discovery]
    Research --> Design[🎨 Design Agent<br/>Theme Generation]
    Design --> Copy[✍️ Copy Agent<br/>Invitations & Scripts]
    
    Research --> Packaging[📦 Packaging Agent<br/>Report Assembly + Budget Calc]
    Design --> Packaging
    Copy --> Packaging
    
    Packaging --> Judge[🧠 Judge Agent<br/>LLM-as-Judge Evaluation]
    Judge --> Output[📄 Final Event Plan<br/>Markdown Report + AI Quality Score]
    Output --> Download[📥 Download / Display in Browser]
    Download --> Deploy[☁️ Railway Cloud Deployment<br/>Public URL + Auto-scaling]

    subgraph LLMs["🌐 Multi-LLM Integration Layer"]
        direction TB
        Gemini[🤖 Google Gemini API<br/>Creative Generation & Evaluation]
        Tavily[🔎 Tavily Search API<br/>Real-time Web Search]
    end

    Research --> Tavily
    Design --> Gemini
    Copy --> Gemini
    Judge --> Gemini

    classDef input fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef ui fill:#fff3e0,stroke:#ef6c00,stroke-width:2px;
    classDef agent fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef llm fill:#fce4ec,stroke:#c2185b,stroke-width:2px;
    classDef output fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    classDef deploy fill:#e0f2f1,stroke:#00695c,stroke-width:2px;
    classDef llmsub fill:#ffffff,stroke:#999,stroke-width:1px,stroke-dasharray: 5 5;

    class User input;
    class UI ui;
    class Research,Design,Copy,Packaging,Judge agent;
    class Gemini,Tavily llm;
    class Output,Download output;
    class Deploy deploy;
    class LLMs llmsub;