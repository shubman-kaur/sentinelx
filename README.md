SentinelX — AI-Powered Digital Public Safety Intelligence Platform

ET AI Hackathon 2.0 (Unstop × Economic Times) — Problem Statement 6: AI for Digital Public Safety

SentinelX is a multi-modal intelligence platform that helps investigators and citizens detect, verify, and respond to two of India's most damaging fraud patterns: digital-arrest / government-impersonation scams (fake CBI/ED/Customs calls) and counterfeit currency. It combines a text-based scam classifier, a document-grounded investigation assistant, and a computer-vision currency detector into a single fused risk score, delivered through a live emergency-dispatch-style dashboard.

Problem

Digital-arrest scams — where fraudsters impersonate law enforcement or government agencies over video/voice calls to extort money — and counterfeit currency circulation are both fast-growing, high-harm categories of digital public safety threats. Existing tools address these in isolation, if at all. SentinelX unifies detection across text, documents, and images into one decision-support system.

Scope note: SentinelX is deliberately scoped to digital-arrest/impersonation scams and counterfeit currency, not generic retail/e-commerce fraud. This was a considered engineering decision after reviewing the official PS6 brief, not a coverage gap.

Architecture

SentinelX runs as four independent FastAPI microservices, fused by a central intelligence engine, and visualized through a standalone dashboard.

                    ┌─────────────────────┐
                    │   dashboard.html     │
                    │  (case intake UI)    │
                    └──────────┬───────────┘
                               │ FormData → /analyze
                               ▼
                    ┌─────────────────────┐
                    │  Central Intelligence │
                    │   Engine (:8003)      │
                    │  40% Scam + 35% Copilot│
                    │  + 25% Currency        │
                    └───┬─────────┬─────────┘
              ┌─────────┘         │         └─────────┐
              ▼                   ▼                   ▼
    ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
    │ Scam Classifier    │ │ Investigation     │ │ Currency Detector │
    │ (:8000)            │ │ Copilot (:8001)   │ │ (:8002)            │
    │ LightGBM + TF-IDF   │ │ RAG (Groq LLM)    │ │ YOLOv8n-cls        │
    └──────────────────┘ └──────────────────┘ └──────────────────┘

When no image is submitted, fusion weights redistribute proportionally across the remaining two signals (~53% Scam / ~47% Copilot).

1. Currency Detector (:8002)

Binary Real/Fake classification on currency note images using a fine-tuned YOLOv8n-cls model.

99.46% top-1 validation accuracy, 25 training epochs
Endpoint: main.py
2. Scam Classifier (:8000)

Text classifier over call transcripts / chat messages, flagging six red-flag categories: Fake Authority Claim, Threat Language, Payment Pressure, Remote Access Request, OTP Request, and Isolation Tactics.

LightGBM (n_estimators=200, class_weight='balanced') over a 3,006-dimension TF-IDF feature space
97.61% test accuracy / 99.66% train accuracy on 6,668 records (5,629 normal / 1,039 scam, post-deduplication)
Endpoint: scam_api.py
3. Investigation Copilot (:8001)

Retrieval-augmented assistant grounded in four official government PDFs, for investigators to query scam procedures, legal context, and reporting steps.

Custom cosine-similarity retrieval (NumPy only — no vector DB) over 281 chunks, embedded with sentence-transformers/all-MiniLM-L6-v2
Generation via Groq (llama-3.3-70b-versatile)
Endpoint: investigation_api.py
4. Central Intelligence Engine (:8003)

Fuses all three signals into a single weighted risk score and threat level.

Weights: 40% Scam Classifier + 35% Investigation Copilot + 25% Currency Detector (redistributed proportionally when no image is provided)
Threat levels: Critical ≥ 80 · High 60–79 · Medium 35–59 · Low < 35
Endpoint: central_engine.py
