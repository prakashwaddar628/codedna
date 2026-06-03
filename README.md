Project Structure
Repository
codedna/
│
├── frontend/
├── backend/
├── ai-services/
├── infrastructure/
├── docs/
├── datasets/
├── scripts/
├── .github/
├── README.md
└── docker-compose.yml
Phase 1 Architecture (MVP)
User
 │
 ▼
Frontend (Next.js)
 │
 ▼
FastAPI Backend
 │
 ├── PostgreSQL
 │
 ├── Redis
 │
 └── Recommendation Engine

Goal:

Personalized roadmap
Skill tracking
Daily learning planner

No LLMs yet.

Backend Structure
backend/
│
├── app/
│   │
│   ├── api/
│   │   ├── auth/
│   │   ├── users/
│   │   ├── skills/
│   │   ├── roadmap/
│   │   ├── learning/
│   │   └── analytics/
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   │
│   ├── models/
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │
│   ├── repositories/
│   │
│   └── main.py
│
├── tests/
│
└── requirements.txt
Frontend Structure
frontend/
│
├── src/
│   │
│   ├── app/
│   │
│   ├── components/
│   │
│   ├── hooks/
│   │
│   ├── services/
│   │
│   ├── store/
│   │
│   ├── types/
│   │
│   └── utils/
│
├── public/
│
└── package.json
Database Design
Users
users
Field	Type
id	UUID
name	String
email	String
role	String
created_at	Timestamp
Skills
skills
Field	Type
id	UUID
skill_name	String
category	String

Examples:

Arrays
Graphs
OS
DBMS
Networking
System Design
User Skills
user_skills

Tracks proficiency.

Field	Type
user_id	UUID
skill_id	UUID
level	Integer
confidence	Float
Learning Activities
learning_activities

Tracks everything.

Field	Type
user_id	UUID
activity_type	String
score	Float
duration	Integer
Core Modules
Module 1
Skill Graph Engine

Converts:

DSA
 ├─ Arrays
 ├─ Linked List
 ├─ Trees
 └─ Graphs

into a dependency graph.

This teaches:

Graph Theory
Data Modeling
Module 2
Recommendation Engine

Input:

{
  "weak_skills": [
    "Graphs",
    "DP"
  ]
}

Output:

{
  "today_task": "Graph Problem #12"
}
Module 3
Daily Planner

Generates:

Today's Plan

30 min DSA
20 min System Design
15 min Revision
Module 4
Analytics Dashboard

Shows:

Learning streak
Weakest skills
Progress graph
Retention score
System Design Concepts You'll Learn

Phase 1:

✅ REST APIs

✅ Authentication

✅ Database Design

✅ Caching

✅ Repository Pattern

✅ Clean Architecture

Phase 2

Add AI

ai-services/
│
├── mentor-agent/
├── roadmap-agent/
├── interview-agent/
├── evaluation-agent/
└── rag-engine/
Phase 3

Microservices

User Service
Learning Service
Recommendation Service
Analytics Service
AI Service

Communication:

Kafka
Redis Streams
RabbitMQ
Phase 4

FAANG-Level Scale

Kubernetes
Docker
Prometheus
Grafana
ELK
CI/CD
First 7-Day Sprint
Day 1
Create repo
Setup FastAPI
Setup Next.js
Setup PostgreSQL
Day 2
Authentication
Day 3
User Profiles
Day 4
Skill Graph Schema
Day 5
Learning Activity Tracking
Day 6
Recommendation Engine v1
Day 7
Dashboard