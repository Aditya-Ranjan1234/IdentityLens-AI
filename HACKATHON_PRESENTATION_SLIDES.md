
# IdentityLens AI - Hackathon Presentation Slides

---

## Slide 1: Title Slide
**Project Title:** IdentityLens AI – Hybrid Identity Risk Detector
**Team Name:** [Your Team Name]
**Team Members:** [List Member Names Here]
**Track:** Identity & Access Risk Governance

**[Screenshot Placeholder: Project Logo/Title Card]**

---

## Slide 2: Problem Statement
### Identity Sprawl in Hybrid Enterprises
- 5000+ identities across AD, AWS IAM, Okta, Salesforce – no single pane of glass
- Cross-platform visibility gaps: users have different permissions across on-prem/cloud
- Offboarding failures: accounts disabled in AD but remain active in cloud/SaaS
- Privilege abuse: un-audited nested group inheritance, over-provisioned roles, dormant admins
- **Real-World Incidents:**
  - Contractor account disabled in AD → AWS IAM/Okta still active → data exfiltration
  - Service account granted Domain Admin + S3 Full Access → lateral movement
  - Unrotated developer tokens → SaaS vendor breach exposes production data

### Business & Compliance Risks
- Lateral movement attacks exploiting cross-platform gaps
- Audit failures for NIST/GDPR/CIS Controls
- Increased blast radius due to unmanaged privilege creep

**[Screenshot Placeholder: Real-World Breach Headlines]**

---

## Slide 3: Objectives
### Core Objectives
1. **Unified Identity Visibility:** Consolidate identity data from all platforms into one view
2. **Effective Privilege Calculation:** Compute real permissions including nested group inheritance
3. **Advanced Risk Detection:** Combine rule-based and ML-based approaches to find risky identities
4. **Alert Reduction:** Correlate related signals into actionable incidents to cut down on noise
5. **Explainable Remediation:** Provide clear, platform-specific steps to fix issues

---

## Slide 4: Solution Overview
### High-Level Workflow
Inputs → Processing → Outputs
- **Inputs:** AD identities, AWS IAM, Okta users/groups, audit logs, offboarding records
- **Processing:**
  - Identity resolution (cross-platform mapping)
  - Graph construction (users → groups → roles → resources)
  - Effective privilege calculation
  - Rule/ML risk detection
  - Incident correlation
  - LLM-powered explanations
- **Outputs:**
  - Risk-scored identities
  - Incident reports
  - Remediation steps
  - Compliance-aligned audit exports

### Why This Approach Is Different
- **Graph-Based Privilege Analysis:** Traverses nested groups for accurate effective permissions (not just direct assignments)
- **Hybrid-First Design:** Built from ground up for on-prem + cloud + SaaS environments
- **Multi-Model ML:** Combines Isolation Forest, One-Class SVM, and Local Outlier Factor for robust anomaly detection
- **LLM for Context:** AI-generated remediation steps that are explainable to auditors

---

## Slide 5: System Architecture
### Architecture Diagram
```
[Dashboard Layer]
  |
  └─── Next.js + Tailwind + ReactFlow
        |
[API Layer]
  |
  └─── FastAPI (REST Endpoints)
        |
        ├─── Identity Resolver
        ├─── Graph Builder
        ├─── Risk Engine
        ├─── ML Anomaly Detector
        ├─── LLM Explainer
        └─── Report Generator
        |
[Data Layer]
  |
  ├─── Users CSV
  ├─── AD Accounts CSV
  ├─── AWS IAM CSV
  ├─── Okta Users/Groups CSV
  ├─── Group Hierarchy CSV
  ├─── Audit Logs CSV
  └─── Offboarding Records CSV
        |
[ML Models Layer]
  ├─── Isolation Forest
  ├─── One-Class SVM
  └─── Local Outlier Factor (all .pkl files)
```

**[Screenshot Placeholder: Detailed Architecture Diagram]**

---

## Slide 6: Technology Stack
### Core Technologies
| Category | Tools/Libraries |
|----------|-----------------|
| **Backend Framework** | FastAPI |
| **Graph Processing** | NetworkX |
| **Data Handling** | Pandas, NumPy |
| **Machine Learning** | Scikit-learn (Isolation Forest, One-Class SVM, Local Outlier Factor) |
| **LLM Integration** | OpenAI (GPT-4o-mini), python-dotenv |
| **Frontend** | Next.js, Tailwind CSS, Recharts, ReactFlow |
| **Data Storage** | CSV (for demo; easily extendable to PostgreSQL/SQLite) |

---

## Slide 7: Data Sources & Simulation
### Data Sources Used
- **AD Identities:** 500+ users with status, last login, organizational data
- **AWS IAM:** Users, roles (ReadOnlyAccess, AdministratorAccess, AmazonS3FullAccess, PowerUserAccess)
- **Okta:** Users, groups, nested group hierarchy
- **SaaS Entitlements:** Salesforce profiles/permissions
- **Audit Logs:** 10,000+ login/access events with timestamps, IPs, countries
- **HR/Offboarding:** Termination records, platform disable status

### Data Simulation Process
1. Generate realistic identities using Faker library
2. Create nested groups for inheritance (DevOps → Engineering → All Users; AWS_Admins → Admins)
3. Inject intentional anomalies (offboarding gaps, cross-platform admins, dormant accounts)
4. Save all data to CSV files for reusability

**[Screenshot Placeholder: Sample of Generated Data Files]**

---

## Slide 8: Data Model & Dictionary
### Key Schemas

| Entity | Key Attributes |
|--------|----------------|
| **Identity** | `user_id`, `name`, `email`, `department`, `title`, `manager`, `hire_date`, `termination_date`, `status` |
| **AD Account** | `user_id`, `ad_account`, `status`, `last_login` |
| **AWS Account** | `user_id`, `aws_user`, `roles`, `last_login` |
| **Okta Account** | `user_id`, `okta_id`, `groups`, `mfa_enabled` |
| **Audit Log** | `timestamp`, `user_id`, `platform`, `action`, `resource`, `ip`, `country`, `success` |
| **Offboarding Record** | `user_id`, `termination_date`, `ad_disabled`, `aws_disabled`, `okta_disabled` |
| **Group Hierarchy** | `group_name`, `parent_group`, `platform` |

---

## Slide 9: Identity Resolution Engine
### How It Works
1. **Extract User IDs:** Pull `user_id` from all platforms (primary key)
2. **Normalize Usernames:** Convert to lowercase, strip spaces (for AD → AWS/Okta mapping)
3. **Correlate Identities:** Join on `user_id` to get a unified "master identity" view
4. **Example Mappings:**
   | AD Account | AWS IAM User | Okta ID | Salesforce User |
   |------------|--------------|---------|-----------------|
   | `john.smith` | `john-smith` | `john.smith@company.com` | `john.smith@company.com` |

**[Screenshot Placeholder: Identity Resolution API Response]**

---

## Slide 10: Identity Graph Construction
### Graph Nodes
| Node Type | Description | Attributes |
|-----------|-------------|------------|
| **User** | Employee or service account | `user_id`, `name`, `department` |
| **Platform Account** | AD, AWS, Okta, Salesforce account | `platform`, `account_name` |
| **Group** | Okta/AD group | `platform`, `group_name` |
| **Role** | AWS role or Okta group with permissions | `platform`, `role_name` |

### Graph Edges
| Edge Type | Source → Target | Description |
|-----------|-----------------|-------------|
| `has_account` | User → Platform Account | User has account on platform |
| `member_of` | Platform Account → Group/Role | Direct assignment |
| `nested_in` | Group → Parent Group | Nested group inheritance |
| `has_role` | Platform Account → Role | Direct role assignment |

**[Screenshot Placeholder: ReactFlow Graph Visualization]**

---

## Slide 11: Effective Privilege Calculator
### Key Features
1. **Direct Permissions:** List all roles/groups directly assigned
2. **Nested Group Inheritance:** Traverse parent groups using NetworkX ancestors
3. **Cross-Platform Aggregation:** Combine permissions from AD, AWS, Okta, Salesforce
4. **Risk Group Permissions Mapping:** Pre-defined risk levels for common roles/groups

### Example Calculation
User `jane.doe` is in Okta `DevOps` → which is nested in `Engineering` and `Admins`
→ Effective Permissions = {ReadOnlyAccess, AmazonEC2FullAccess, AmazonS3FullAccess, Modify All Data, Delete Records}

**[Screenshot Placeholder: Effective Privileges API Response]**

---

## Slide 12: Risk Detection Framework
### Rule-Based Detections
1. **Offboarding Gap:** AD disabled but AWS/Okta still active
2. **Cross-Platform Admin:** Admin in 2+ platforms
3. **Dormant Admin:** Admin user with last login >90 days ago

### Behavioral/ML-Based Detections
1. **Unusual Login Frequency/Country:** High variance in login times or new country
2. **Platform Spread Anomaly:** Accessing way more platforms than normal
3. **Privilege-to-Usage Ratio:** High permissions with little to no usage

---

## Slide 13: Risk Scenarios Covered
| Scenario | Description | Severity |
|----------|-------------|----------|
| Orphaned Account | Disabled in AD, Active in AWS/Okta | Critical |
| Cross-Platform Admin | Admin in AD + AWS + Okta | Critical |
| Dormant Admin | Admin not logged in >90 days | High |
| Privilege Spike | >3 new roles added in 7 days | High |
| Unrotated Tokens | API tokens older than 1 year | Medium |
| Service Account w/o Owner | Service account with no documented owner | Medium |

---

## Slide 14: Feature Engineering (For ML)
### ML Features
1. **Login Count:** Number of logins per user in audit logs
2. **Platform Spread:** Number of unique platforms accessed
3. **Resource Count:** Number of unique resources accessed
4. **Country Count:** Number of unique countries logged in from
5. **Hour Variance:** Variance in login times (to detect unusual activity)

---

## Slide 15: AI/ML Methodology
### Models Used
1. **Isolation Forest** → Primary anomaly detector
2. **One-Class SVM** → Good for high-dimensional data
3. **Local Outlier Factor** → Detects local anomalies in neighborhoods

### Training Process
1. Extract features from 500 users' audit logs
2. Split data (unsupervised learning)
3. Train all three models using Scikit-learn
4. Save as `.pkl` files for fast inference
5. Contamination level set to 0.05 (expect ~5% anomalies)

### Threshold Selection
- For Isolation Forest: Threshold at decision function = 0.0
- Severity is calculated based on both ML anomaly score and rule-based factors

**[Screenshot Placeholder: ML Model Training Logs]**

---

## Slide 16: Risk Scoring Engine
### Formula
```
risk_score = (40 * offboarding_gap) + (35 * cross_platform_admin) + (20 * dormant_admin) + (ml_anomaly_score)
```

### Severity Levels
| Severity | Range | Description |
|----------|-------|-------------|
| **Critical** | 70–100 | Immediate action required |
| **High** | 40–69 | High priority |
| **Medium** | 20–39 | Medium priority |
| **Low** | 0–19 | Low priority |

---

## Slide 17: Incident Correlation & Alert Consolidation
### How It Works
- **Alert Grouping:** Combine alerts for same user into single incident
- **Noise Reduction:** Suppress duplicate alerts and low-severity single events
- **Incident Generation:** Create incident with title, severity, timeline, and evidence trail

**[Screenshot Placeholder: Incident List Dashboard]**

---

## Slide 18: Dashboard Overview
### Dashboard Tabs
1. **Overview:** High-level stats, risk distribution, offboarding gaps, top risks
2. **Risk Center:** All risk assessments sorted by score
3. **Incidents:** Correlated security incidents
4. **Identity Graph:** Visualize privilege relationships
5. **Offboarding Gaps:** Detect orphaned accounts
6. **Metrics:** System-wide risk metrics
7. **Identity Explorer:** Click any user for detailed view

### Navigation Flow
Sidebar → [Select Tab] → Main Content Area

**[Screenshot Placeholder: Full Dashboard Screenshot]**

---

## Slide 19: Dashboard – Identity Risk View
- **Top Risky Identities:** Table with user, risk score, severity, and reason
- **Risk Score Breakdown:** Bar chart of score distribution
- **Filters:** Filter by department, severity, or platform
- **Identity Explorer Link:** Click any user to view details

**[Screenshot Placeholder: Risk Center Dashboard Tab]**

---

## Slide 20: Dashboard – Identity Graph
- **ReactFlow Visualization:** Interactive graph of users, platform accounts, groups, and roles
- **Edge Types:** Different colors/styles for `has_account`, `member_of`, `nested_in`, `has_role`
- **Controls:** Zoom, pan, minimap, fit view

**[Screenshot Placeholder: Identity Graph Visualization]**

---

## Slide 21: Dashboard – Offboarding Gap Detection
- **Orphaned Accounts Table:** Users with AD disabled but other platforms active
- **Actions:** Checkboxes for bulk selection, buttons for "Disable All" / "Notify Owners"
- **Risk Intelligence:** Context on how orphaned accounts are used in lateral movement attacks

**[Screenshot Placeholder: Offboarding Gaps Dashboard Tab]**

---

## Slide 22: Dashboard – Incident Investigation
- **Incident Timeline:** Chronological list of events
- **Evidence Trail:** Links to audit logs, privilege assignments, and offboarding records
- **Attack Path Visualization:** Identity graph path showing how privilege escalation could occur

**[Screenshot Placeholder: Incident Investigation View]**

---

## Slide 23: Sample Detection Results
| Identity | Risk Score | Severity | Reason |
|----------|------------|----------|--------|
| `svc-etl-prod` | 95 | Critical | Domain Admin (AD) + S3 Full Access (AWS) |
| `john.smith` | 80 | Critical | AD disabled, AWS/Okta still active |
| `jane.doe` | 70 | Critical | Admin in AD, AWS, Okta |
| `dave.admin` | 60 | High | Admin last login 102 days ago |
| `alice.dev` | 40 | High | 4 new roles added in last week |
| `svc-backup` | 25 | Medium | Service account with no documented owner |

---

## Slide 24: Explainable Remediation Engine
### LLM-Powered Recommendations
- Powered by OpenAI GPT-4o-mini (with fallback to mock data if no API key)
- Steps are platform-specific and actionable

#### Example Remediation for `john.smith`
1. **Disable AWS IAM User:** Go to AWS Console → IAM → Users → `john-smith` → Security credentials → Disable access keys and console access
2. **Remove from Okta Groups:** Okta Admin → Directory → People → `john.smith@company.com` → Remove all groups
3. **Disable Okta Account:** Okta Admin → Directory → People → Deactivate
4. **Rotate Salesforce API Token:** If applicable, invalidate existing tokens

**[Screenshot Placeholder: LLM Explanation API Response]**

---

## Slide 25: Sample Risk Report
### Executive Summary
- Total identities assessed: 500
- High/Critical risk identities: 18
- Offboarding gaps detected: 12
- ML anomalies detected: 25

### Key Findings
1. 12 orphaned accounts from recent terminations
2. 3 users with admin rights in 3+ platforms
3. 5 dormant admin accounts (>90 days inactive)

### Recommendations
- Bulk disable orphaned accounts immediately
- Implement least privilege for cross-platform admins
- Rotate all tokens older than 180 days

### Compliance Mapping
- NIST AC-2 (Account Management)
- NIST AC-6 (Least Privilege)
- GDPR Article 5 (Data Minimization)
- GDPR Article 32 (Security of Processing)
- CIS Controls 5 & 6 (Account/Access Control)

**[Screenshot Placeholder: Sample CSV/JSON Risk Report]**

---

## Slide 26: Compliance Alignment
| Framework/Regulation | Control | How We Meet It |
|-----------------------|---------|-----------------|
| **NIST SP 800-53** | AC-2 (Account Management) | Full identity lifecycle visibility, offboarding gap detection |
| **NIST SP 800-53** | AC-6 (Least Privilege) | Effective privilege calculation, risk scoring for over-provisioning |
| **NIST SP 800-53** | IA-4 (Identifier Management) | Cross-platform identity resolution |
| **GDPR** | Article 5 (Data Minimization) | Identifies over-provisioned permissions |
| **GDPR** | Article 32 (Security of Processing) | Monitors access and detects anomalies |
| **CIS Controls** | 5 & 6 (Account/Access Control) | Risk watchlist, offboarding gap detection |

---

## Slide 27: Performance & Evaluation
### Key Metrics
| Metric | Value |
|--------|-------|
| Identity Coverage | 100% (all 500 identities) |
| High/Critical Risk Detections | 18 identities |
| ML Anomaly Detections | 25 identities (Isolation Forest) |
| Alert Reduction | ~40% (via incident correlation) |
| Time to Calculate Effective Privileges | <2 seconds (cached graph) |
| Time to Run All ML Models | <10 seconds for full dataset |

---

## Slide 28: Challenges & Edge Cases
### What We Encountered
1. **SSO Cascades:** When a user logs into multiple platforms via SSO in a short time – is it normal or compromised?
2. **Shared Service Accounts:** Hard to detect abuse since multiple users can access them
3. **Legitimate Admin Activity:** During incidents, admins gain temporary elevated access – how to distinguish from real abuse?
4. **False Positives:** Some users travel a lot, leading to high country count variance

### How We Addressed Them
- Added "platform spread" and "hour variance" features to ML models
- Added manual review notes on high-severity incidents
- Gave users ability to filter false positives

---

## Slide 29: Future Enhancements
### Near-Term
1. **Real-Time Ingestion:** Connect to Okta/AWS APIs for live data
2. **Automated Remediation:** Auto-disable orphaned accounts
3. **SIEM Integration:** Connect to Splunk/Elasticsearch

### Long-Term
1. **Graph Neural Networks (GNNs):** For better graph-based anomaly detection
2. **UEBA (User and Entity Behavior Analytics):** Baseline normal behavior per user
3. **Multi-Tenant Support:** For MSSP use cases
4. **Custom Rules Engine:** Let users write their own risk rules

---

## Slide 30: Conclusion
### Key Achievements
✅ Built hybrid identity graph with nested inheritance
✅ Implemented multi-model ML for anomaly detection
✅ Added LLM-powered remediation steps
✅ Created full-featured interactive dashboard
✅ Delivered exportable compliance reports

### Business Value
- Reduced lateral movement risk by closing offboarding gaps
- Cut audit preparation time by providing pre-built reports
- Lowered mean time to detect (MTTD) privilege abuse

### Security Impact
- Identified 18 high/critical risk identities
- Found 12 orphaned accounts that could lead to breaches
- Calculated accurate effective privileges that were previously invisible

---

## Slide 31: Demo / Live Walkthrough
1. **Dataset Overview:** Show CSV files and explain anomalies injected
2. **Risk Detection Flow:** Run risk calculation on sample user
3. **Dashboard Demo:**
   - Overview tab: high-level stats
   - Identity Graph: visualize nested privileges
   - Offboarding Gaps: show orphaned accounts
   - Identity Explorer: click into user details

**[Screenshot Placeholder: Demo Recording/Video Frame]**

---

## Slide 32: Q&A / Thank You
### Contact Info
- Team Lead: [Name] ([Email])
- Other Members: [List Names & Emails]

### Links
- GitHub Repository: [https://github.com/your-username/identity-sprawl-detector]
- Live Demo: [If Hosted]

**Thank You for Your Time!**

---

## Hackathon-Friendly Short Version (18 Slides)
For judging, compress the above into 18 slides:
1. Title
2. Problem Statement
3. Objectives
4. Solution Overview
5. Architecture
6. Data & Identity Resolution
7. Identity Graph + Privilege Calculator
8. Risk Detection & ML
9. Risk Scoring Engine
10. Dashboard Overview
11. Key Findings (Top Risks)
12. Incident Correlation
13. Remediation Recommendations
14. Compliance Mapping
15. Results & Metrics
16. Future Scope
17. Demo
18. Thank You
