Here is a concise `README.md` file for your AI assistant platform repository:

````markdown
# AI Chatbot Assistant Platform

This repository contains a multi-tenant AI assistant platform built with Django REST Framework and Telegram integration using Aiogram. It enables businesses to run campaign-specific AI assistants with persona-driven logic and natural conversation flows.

## Features

- **Multi-Vendor Support**: Each vendor can define their own campaigns, personas, and products.
- **Persona-Based Campaigns**: Dynamic persona identification using semantic vector similarity.
- **LangChain + OpenAI Integration**: Modular, decision-tree-based flows with LLM-driven conversation.
- **Vector Search**: Various embedding algorithms for quick and optimized persona matching and knowledge QA.
- **Chatbot**: Telegex telegram Chatbot
- **Vendor Analytics Assistant** *(Prototype)*: Business users can query campaign performance using AI.

## Tech Stack
- Buildah+Podman
- Posgresql 17.4
- Elixir ecto phoenix for rest api, web pages 
- Bumblebee for default embeddings and heavier instruments for precision or performance oriented case
- Fastapi+LangChains for complex conversation chains

## Setup