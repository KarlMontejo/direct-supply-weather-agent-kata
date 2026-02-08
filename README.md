# Agentic Food Procurement Assistant (Take-Home Kata)
**Name:** Karl Montejo
**Date:** 2/8/2026
**Company:** Direct Supply

This project is designed to demonstrate an agentic AI-assisted approach to food procurement workflows in healthcare and senior living environments, aligned with Direct Supply and DSSI’s real-world use cases.

The application focuses on reducing friction in food procurement by assisting users with stock-outs, contract compliance validation, and curated product recommendations.

---
## Project Inspiration
This project was inspired by research into Direct Supply DSSI’s use of AI in healthcare and senior living procurement, particularly their focus on food procurement workflows. Reviewing DSSI blog posts and product initiatives highlighted how AI is applied as a decision-support tool to reduce operational friction, especially around stock-outs and contract compliance.

The take-home kata included options to build a chatbot and to integrate with a real-world API. Rather than treating these separately, I chose to combine them by building an agentic LLM-powered chatbot that orchestrates API and tool calls to assist real-world procurement workflows. The system integrates mocked enterprise data sources (such as inventory and contracts) alongside external product data to simulate how AI supports procurement decisions in practice.

The goal of this project is to demonstrate how agentic AI can help reduce rework during order re-fulfillment by identifying stock-outs, validating compliance, and recommending viable product alternatives while keeping humans in the loop.

---
## Problem Statement
Food procurement in healthcare and senior living is operationally complex and highly constrained. Procurement teams must:
- Ensure uninterrupted food service despite frequent stock-outs
- Adhere to detailed contracts covering brands, pack sizes, suppliers, and dietary requirements
- Quickly identify compliant substitute products when availability changes
- Cross-validate requirements across multiple data sources under time pressure
These tasks are often handled manually, requiring procurement professionals to cross-reference inventory systems, contracts, and product catalogs. This process is time-consuming, error-prone, and difficult to scale.

---
## Solution Overview
This project implements an **agentic LLM-powered chatbot** that acts as a **decision-support assistant** for food procurement workflows.
The system helps users:
- Detect and resolve hard or partial stock-outs
- Validate products against contract and compliance requirements
- Discover curated, compliant product alternatives
- Draft order recommendations (non-executing)
The chatbot does not place orders or override procurement rules. Instead, it provides explainable recommendations that keep humans in the loop.

---
## Architecture Overview
Service-Oriented Architecture
- Frontend (Next.js / React)
- Backend API (Python / FastAPI)
- AI Orchestration Layer (LangChain)
- Data & Tooling Layer:
    - Mock Contracts API
    - Mock Inventory API
    - Open Food Facts API

### Key Components
#### Frontend
- Built with **React using the Next.js framework**
- Provides a simple chat interface for procurement workflows
- Displays recommendations, explanations, and order drafts
#### Backend
- Built with **Python and FastAPI**
- Handles request validation, orchestration, and error handling
- Acts as the control layer between the frontend and AI service
#### AI Layer
- Built with **LangChain**
- Implements agentic reasoning to:
  - Interpret user intent
  - Select appropriate tools
  - Reason across inventory, contracts, and product data
  - Generate explainable recommendations
#### Data Sources
- **Mock Contracts API**  
  Simulates real-world procurement contracts and compliance rules.
- **Mock Inventory API**  
  Simulates real-time inventory availability, including stock-outs.

Mock APIs act as sources of truth for procurement rules and availability, while the live API is used only for reference and validation.

---
## What This Project Demonstrates
- Understanding of real-world food procurement challenges
- Agentic AI design using structured tools and constraints
- Clean, maintainable system architecture
- Practical use of LLMs for decision support
- Alignment with healthcare and senior living procurement workflows

---
## Tech Stack
- **Frontend:** React, Next.js
- **Backend:** Python, FastAPI
- **AI Orchestration:** LangChain
- **Data:** Mock JSON-based APIs, Open Food Facts API

---

## Notes
In a production environment, the mock data sources would be replaced with enterprise inventory, contract, and supplier systems, and the services would be deployed independently.
