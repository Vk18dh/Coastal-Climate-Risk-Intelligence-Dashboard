# Technical Requirements Document (TRD)

## Project Name

Coastal Climate Risk Intelligence Dashboard

---

# Version

| Field | Value |
|--------|--------|
| Version | 1.0 |
| Status | Draft |
| Architecture | Modular Service-Oriented Architecture |
| Deployment Target | Local Development → Docker → Production |

---

# Technical Overview

The Coastal Climate Risk Intelligence Dashboard is built using a modern, modular, and production-ready technology stack.

The system follows a service-oriented architecture where each module has a single responsibility, enabling scalability, maintainability, and easier testing.

The platform consists of four primary layers:

- Presentation Layer
- Backend API Layer
- Analytics & AI Layer
- Data Layer

---

# System Architecture

```
React Dashboard

        │

 REST API (FastAPI)

        │

────────────────────────────────────

Data Service

Analytics Service

Geospatial Service

AI Service

Climate Risk Engine

────────────────────────────────────

        │

PostgreSQL + PostGIS + Redis
```

---

# Frontend

| Technology | Version | Purpose |
|------------|----------|---------|
| React | Latest | User Interface |
| Vite | Latest | Build Tool |
| Tailwind CSS | Latest | Styling |
| shadcn/ui | Latest | UI Components |
| Plotly | Latest | Analytics Charts |
| Recharts | Latest | Dashboard Charts |
| MapLibre GL | Latest | Interactive Maps |
| Leaflet | Latest | GIS Layers |
| Axios | Latest | API Communication |
| Zustand | Latest | State Management |

---

# Backend

| Technology | Purpose |
|------------|---------|
| FastAPI | REST API Framework |
| Uvicorn | ASGI Server |
| SQLAlchemy | ORM |
| Alembic | Database Migration |
| Pydantic | Data Validation |

---

# Database

## Primary Database

PostgreSQL

Purpose

- Environmental Data
- Climate Records
- Historical Data
- User Preferences (Future)

---

## Spatial Database

PostGIS

Purpose

- GIS Layers
- Geometry
- Polygon Queries
- Distance Calculations
- Spatial Indexing

---

## Cache

Redis

Purpose

- Weather Cache
- Analytics Cache
- Session Cache (Future)

---

# Artificial Intelligence

## Selected LLM

Qwen 3 Instruct

Purpose

- Executive Summary
- Climate Advisory
- Explainable AI
- Recommendation Generation

Deployment

- Local Inference
- GGUF Quantized Model
- llama.cpp / Ollama compatible

---

## Embedding Model

BAAI BGE-M3

Purpose

- Semantic Search
- Future RAG
- Similarity Search

---

## OCR

PaddleOCR

Purpose

- Extract text from climate reports
- Process scanned environmental documents
- Future document ingestion

---

# GIS Stack

| Library | Purpose |
|----------|---------|
| GeoPandas | Spatial Analysis |
| Rasterio | Raster Processing |
| Shapely | Geometry Operations |
| Fiona | GIS File Support |
| pyproj | Coordinate Transformations |

---

# Data Processing

| Library | Purpose |
|----------|---------|
| Pandas | Data Cleaning |
| NumPy | Numerical Computation |
| Scikit-Learn | Statistical Models |
| SciPy | Scientific Analysis |

---

# Visualization

## Maps

- MapLibre GL
- Leaflet

---

## Charts

- Plotly
- Recharts

---

# External Data Sources

## Weather

- IMD
- Open-Meteo (Fallback)

---

## Ocean

- INCOIS

---

## Satellite

- Sentinel
- Landsat

---

## Terrain

- Digital Elevation Models (DEM)

---

## Historical Data

- Government Open Datasets
- Research Datasets

---

# Backend Modules

## Data Ingestion

Responsibilities

- Fetch Weather Data
- Fetch Ocean Data
- Import Satellite Data
- Import Historical Data

---

## Data Processing

Responsibilities

- Cleaning
- Validation
- Feature Engineering
- Missing Value Handling

---

## Geospatial Engine

Responsibilities

- Spatial Join
- Buffer Analysis
- Heatmaps
- Elevation Analysis

---

## Climate Risk Engine

Responsibilities

- Risk Computation
- Normalization
- Classification
- Trend Detection

---

## Analytics Engine

Responsibilities

- Statistical Analysis
- Time-Series Analysis
- Correlation Analysis
- Historical Comparison

---

## AI Engine

Responsibilities

- Prompt Construction
- Executive Reports
- Climate Advisory
- Explainability

---

# API Standards

Architecture

REST API

Data Format

JSON

Documentation

Swagger (FastAPI)

Response Standard

```
{
    "success": true,
    "message": "...",
    "data": {}
}
```

---

# Folder Structure

```
frontend/

backend/

docs/

docker/

data/

models/

scripts/

tests/
```

---

# Coding Standards

Backend

- Python PEP8
- Type Hints
- Docstrings
- Async APIs

Frontend

- TypeScript
- Functional Components
- Reusable Components
- Hooks

---

# Logging

Log Levels

- INFO
- WARNING
- ERROR
- DEBUG

Logging Library

Python Logging

Future

Centralized Logging

---

# Error Handling

Backend

- Global Exception Handler
- Validation Errors
- HTTP Exceptions
- Database Exceptions

Frontend

- Toast Notifications
- Error Pages
- Retry Mechanisms

---

# Performance Targets

| Component | Target |
|------------|---------|
| API Response | <500 ms |
| Dashboard | <3 sec |
| Risk Engine | <5 sec |
| AI Report | <10 sec |

---

# Deployment

Development

- Local

Testing

- Docker Compose

Production

- Docker
- Nginx

Future

- Kubernetes

---

# Environment Variables

```
DATABASE_URL

REDIS_URL

LLM_MODEL

IMD_API_KEY

INCOIS_API_KEY

APP_ENV
```

---

# Technical Constraints

- Open-source technologies only
- Free AI models
- Local-first deployment
- Modular architecture
- Production-ready codebase
- Docker compatibility
- Scalable design

---

# Future Technical Enhancements

- CI/CD Pipeline
- Monitoring (Prometheus + Grafana)
- GPU Acceleration
- Kubernetes Deployment
- Streaming Data Pipeline
- Multi-region Deployment
- Microservices Architecture