# Direct Supply – Weather-Aware Travel Itinerary Agent (Kata)

This repository contains my take-home kata submission for the **Direct Supply Web Development Internship**.

## Overview
This project is an **agentic LLM-powered chatbot** that helps users plan travel itineraries by combining:
- Conversational AI
- Real-time and forecasted weather data
- Practical decision-making logic around activities, timing, and conditions
The goal is to reduce the friction travelers face when planning trips — specifically the need to manually cross-reference activities, dates, locations, and weather forecasts across multiple tools.

Rather than acting as a generic travel chatbot, this system is designed to **reason about constraints** (such as weather suitability and travel dates) and generate **context-aware, day-by-day itinerary guidance**.

---

## Problem
When planning a trip, users often want help answering questions like:
- *“What should I do on each day of my trip?”*
- *“Is this activity realistic given the weather?”*
- *“Should I plan indoor or outdoor activities on a specific day?”*

In practice, answering these questions requires:
- Searching for activities
- Checking weather forecasts across multiple days
- Adjusting plans when weather conditions change
- Understanding how forecast reliability changes over time
This manual process is time-consuming and fragmented.

---

## Solution
This application provides a **travel itinerary planning assistant** that:
1. Converses with the user to understand trip details (location, dates, preferences)
2. Determines when weather data is relevant to planning decisions
3. Uses external tools (such as a weather API) to fetch real-world context
4. Reasons over that data to generate practical, explainable itinerary suggestions
Weather data is treated as an **input to decision-making**, not just something to summarize.

---

## Agentic Design (Lightweight & Intentional)
This project implements a **lightweight agent loop**, appropriate for the scope of a kata.
At a high level:
- The LLM is responsible for interpreting user intent and determining whether external data is needed
- When weather information is relevant, the model requests it via a tool call
- The returned data is evaluated against the user’s travel context before producing a response
This approach demonstrates agency through **tool selection and reasoning**, while keeping behavior predictable and explainable.

---

## Architecture
The application is structured as multiple services within a single repository. In a team with other developers, I would typically separate these services.

/frontend
User-facing chat interface

/backend
API orchestration, request handling, and business logic

/ai-service
LLM prompts, tool definitions, and reasoning logic

/docs
Architecture notes and design decisions

In a production environment, these services would likely be deployed independently. For the purposes of this kata, they are co-located for clarity and simplicity.

---

## External Tools & APIs
The system is designed to support a small, focused set of tools, such as:
- **Weather API** – used to retrieve current conditions or forecasts for specific locations and dates
- *(Optional)* additional APIs to support richer itinerary context
Weather forecasts are used pragmatically, with the understanding that accuracy varies depending on how far in advance a trip is planned.

---

Additional implementation details and architectural decisions are documented in the `/docs` directory.
