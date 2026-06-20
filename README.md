
---
title: IdentityLens AI
emoji: 🛡️
colorFrom: purple
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
short_description: Hybrid identity risk and privilege abuse detection.
---

# IdentityLens AI - Hybrid Identity Risk Detector

**IdentityLens AI** is an advanced tool for detecting and analyzing identity sprawl and privilege abuse in hybrid (on-prem and cloud) environments. It consolidates identity data from multiple platforms, calculates effective privileges (including nested group inheritance), and uses machine learning to detect anomalies and risky behaviors.

## Features
- **Cross-platform Identity Resolution**: Unify identities from Active Directory, AWS IAM, Okta, and Salesforce
- **Effective Privilege Calculation**: Traverse nested groups and inheritance to compute real permissions
- **Multiple ML Anomaly Detectors**: Isolation Forest, One-Class SVM, and Local Outlier Factor for detecting anomalies
- **Risk Scoring Engine**: Calculate risk based on offboarding gaps, cross-platform admin rights, and dormancy
- **Interactive Dashboard**: Full-featured UI with graph visualization, risk watchlist, and reports
- **Audit Reports & Export**: Download CSV/JSON reports for compliance and audits
- **LLM-Powered Explanations**: Get AI-generated risk insights (with OpenAI integration)
- **Identity Explorer Page**: Detailed views for every user, including platform access and privileges
- **Incident Correlation**: Group related risk signals into actionable incidents

## Tech Stack
- **Backend**: FastAPI, NetworkX, Pandas, Scikit-learn
- **Frontend**: Next.js 13+, Tailwind CSS, Recharts, ReactFlow
- **Database**: CSV files (for demo; easily extendable to SQL/NoSQL)
- **LLM Integration**: OpenAI (GPT-4o-mini)

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 18+
- Virtual environment (venv included)

### Backend Setup
1. Activate the virtual environment:
    ```powershell
    # Windows (PowerShell)
    .\venv\Scripts\Activate.ps1
    ```
    ```bash
    # Mac/Linux
    source venv/bin/activate
    ```

2. Install dependencies:
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

3. Generate simulated data:
    ```bash
    python scripts/simulate_data.py
    ```

4. Train ML models:
    ```bash
    python scripts/train_models.py
    ```

5. Start the FastAPI server:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

6. (Optional) Add OpenAI API key for LLM explanations:
    - Create `.env` in backend/
    - Add: `OPENAI_API_KEY=sk-...`

### Frontend Setup
1. Navigate to frontend/:
    ```bash
    cd frontend
    ```
2. Install dependencies:
    ```bash
    npm install
    ```
3. Start the Next.js dev server:
    ```bash
    npm run dev
    ```

## Usage
- Access the dashboard: http://localhost:3000
- Backend API docs: http://localhost:8000/docs
- Use the dashboard's navigation sidebar to explore:
  - Overview (high-level stats and graphs)
  - Risk Center (all risk assessments)
  - Incidents (correlated security alerts)
  - Identity Graph (visualize privilege relationships)
  - Offboarding Gaps (detect orphaned accounts)
  - Metrics (system-wide risk metrics)
  - Identity Explorer (click any user on the Overview page)
  - Export Reports (via `/api/reports/` endpoints)

## API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/users | List all users with platform data |
| GET | /api/risks | Get risk-scored identities |
| GET | /api/incidents | Get correlated incidents |
| GET | /api/graph | Get identity graph data for visualization |
| GET | /api/master | Resolve unified identities |
| GET | /api/privileges | Get effective privilege calculations |
| GET | /api/anomalies | Get ML-detected anomalies (supports `model_type` parameter) |
| POST | /api/anomalies/train | Re-train all anomaly detection models |
| POST | /api/explanations | Get LLM explanation of a risk |
| GET | /api/metrics | Get system risk metrics |
| GET | /api/offboarding | Get offboarding gaps |
| GET | /api/reports/export/csv | Download CSV report |
| GET | /api/reports/export/json | Download JSON report |

## File Structure
```
identity-sprawl-detector/
├── backend/
│   ├── app/
│   │   ├── api/                    # REST API endpoints
│   │   ├── graph/                  # Identity graph builder
│   │   ├── ml/                     # Anomaly detection models
│   │   ├── risk/                   # Risk scoring engine
│   │   ├── services/               # Identity resolver, LLM explainer
│   │   └── main.py                 # FastAPI entry point
│   ├── data/                       # CSV data files (auto-generated)
│   ├── models/                     # Trained ML models (pkl files)
│   ├── scripts/                    # Data simulation and model training
│   ├── .env.example                # Environment variable template
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   └── app/
│   │       ├── dashboard/
│   │       ├── graph/
│   │       ├── incidents/
│   │       ├── risks/
│   │       └── identity/[user_id]/
│   ├── package.json
│   └── tailwind.config.js
├── template/
│   └── sentinel_core/              # Design system artifacts
├── plan.txt                        # Project requirements
└── README.md
```

## Contributing
1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/my-new-feature`
5. Submit a pull request

## License
MIT
