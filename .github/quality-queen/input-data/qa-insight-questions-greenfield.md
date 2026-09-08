# QA Insight Questions — Greenfield / New Teams

> **Purpose:** Discovery questions for newly established teams or greenfield projects. Unlike the standard insight questions (which observe existing practices), these focus on **decisions to make**, **foundations to build**, and **risks to mitigate** when starting from scratch.
>
> **How to use:** These are not an interview checklist. Use them conversationally to understand the team's starting point, constraints, and ambitions. Many answers will be "we haven't decided yet" — that's expected and valuable to capture.

---

## 1. Project & Team Context

### 1.1 Project Vision

- What problem does this product solve, and for whom?
- What does success look like in 3 months? 6 months? 1 year?
- What's the expected scale (users, data volume, transactions)?
- Are there hard deadlines or launch milestones driving the timeline?
- Is this a net-new product, a rebuild of an existing system, or a spin-off?

### 1.2 Team Composition

- Who is on the team today (roles, experience levels)?
- Is the team expected to grow? When, and with which roles?
- What's the team's prior experience with QA practices and test automation?
- Who is the Product Owner, and how available are they?
- Is there a dedicated QA role, or will QA be distributed across the team?
- Does the team have prior experience working together?

### 1.3 Customer & Stakeholder Setup

- Who is the customer, and what's the contractual relationship?
- Does the customer have specific quality expectations or compliance requirements?
- Is there a formal acceptance process expected before production releases?
- How will the customer be involved in ongoing development (demos, UAT, feedback)?
- Are there other stakeholders who need visibility into quality (security officer, compliance, operations)?

---

## 2. Technical Decisions

### 2.1 Tech Stack & Architecture

- What tech stack has been chosen (or is being evaluated)?
- What's the architectural pattern (monolith, microservices, serverless, modular monolith)?
- Are there integration points with external systems? Which ones?
- Is there a legacy system being replaced or integrated with?
- What hosting/cloud platform will be used?
- Are there constraints on tooling (customer-approved tools, license restrictions)?

### 2.2 Development Practices

- What branching strategy will the team use?
- Has the team decided on code review practices?
- Are there coding standards or style guides to follow?
- What IDE/editor and extensions will the team standardize on?
- Is pair programming or mob programming planned?

### 2.3 Test Tooling

- Has the team chosen test frameworks (unit, integration, E2E)?
- Are there preferred tools from the customer or organization?
- What's the budget for test tooling (commercial tools, cloud test infrastructure)?
- Does the team have experience with the chosen test tools?
- How will test authentication be handled (service accounts, test tokens, mocked auth)?

---

## 3. Delivery Model

### 3.1 Agile Method & Cadence

- Which Agile method will the team use (Scrum, Kanban, SAFe, other)?
- What's the planned sprint length / iteration cadence?
- How will the team visualize and track work (board tool, column structure)?
- Has the team established any working agreements yet?
- How will the team handle ceremonies (standup, refinement, retro, demo)?

### 3.2 Release Strategy

- What's the desired release frequency (continuous, weekly, sprint-based, milestone-based)?
- Will there be a formal staging/UAT gate before production?
- Is progressive delivery planned (feature flags, canary, blue-green)?
- Who has authority to approve a production release?
- Is there a rollback strategy in mind?

### 3.3 Environments

- How many environments are planned (dev, test, staging, prod)?
- Who will own environment provisioning and maintenance?
- How will test data be managed (seeded, synthetic, production-like)?
- Are there shared environments with other teams?
- Is infrastructure as code planned from the start?

---

## 4. Quality & Risk

### 4.1 Risk Profile

- What's the worst thing that could happen if this product has a bug in production?
- Are there regulatory or compliance requirements (GDPR, accessibility, financial, health)?
- What's the data sensitivity level (public, internal, confidential, personal)?
- Are there SLA or uptime requirements?
- What's the team's risk tolerance for production incidents?

### 4.2 Quality Ambitions

- What level of test automation does the team aspire to?
- Does the team want to establish quality practices early, or "move fast and add quality later"?
- Has the team experienced pain from missing QA in previous projects? What specifically?
- Are there specific quality attributes that matter most (performance, security, accessibility, reliability)?
- What does "good enough quality" look like for the first release vs. steady state?

### 4.3 Monitoring & Operations

- Is observability (logging, metrics, tracing) planned from the start?
- Who will be on-call or responsible for production incidents?
- How will the team learn from production issues (post-mortems, incident reviews)?
- Is there an existing operations team, or is the dev team responsible for ops?

---

## 5. AI & Tooling

### 5.1 AI Usage

- Is the team using AI-assisted development tools (Copilot, ChatGPT, etc.)?
- Are there organizational policies about AI usage in code/testing?
- Where does the team see AI adding the most value in their workflow?
- Are there concerns about AI-generated code quality or security?

### 5.2 Existing Infrastructure

- Is there existing CI/CD infrastructure the team will use (GitHub Actions, Azure DevOps, Jenkins)?
- Are there organizational templates or standards for pipelines?
- Is there a shared component library or design system to build on?
- Are there existing monitoring/alerting platforms to integrate with?

---

## 6. Improvement Appetite

### 6.1 Learning & Growth

- How does the team plan to handle knowledge sharing and onboarding?
- Is there budget/time allocated for learning and experimentation?
- How will the team decide when to invest in quality infrastructure vs. feature delivery?
- What's the team's experience with retrospectives and continuous improvement?

### 6.2 QA Consultant Engagement

- What's the expected duration and scope of the QA consultant engagement?
- Is the goal to establish practices and hand off, or ongoing QA involvement?
- What authority does QA have to propose process changes?
- How should QA findings and recommendations be communicated (to team, to customer, to leadership)?
