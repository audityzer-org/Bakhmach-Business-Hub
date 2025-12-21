# Readiness Metrics Dashboard

Bakhmach Business Hub - Quantified Progress & Impact Tracking

## Overview

Readiness % = Composite measure of progress toward production-ready state across domains.

**Formula:**

```
Readiness% = (Σ completed_tasks_readiness_delta / Σ all_tasks_readiness_delta) × 100
```

### Current State (Dec 21, 2025)

| Domain | Readiness | Target | Gap | Priority P0 | P1 | P2 |
|--------|-----------|--------|-----|-------------|-----|-----|
| **Code** | 20% | 75% | -55% | 2 | 3 | 4 |
| **ML** | 20% | 75% | -55% | 2 | 4 | 4 |
| **Services** | 20% | 75% | -55% | 2 | 4 | 3 |
| **Workflow** | 20% | 75% | -55% | 2 | 5 | 3 |
| **Overall** | 20% | 75% | -55% | **8** | **16** | **14** |

## Key Metrics

### 1. Domain Readiness (Weekly)

```
Code Readiness = (
  completed_tasks_delta[code] / 
  total_tasks_delta[code]
) × 100
```

**Tracking:**
- `TASKS-CODE.md`: 9 tasks, 47 total readiness_delta
- Milestones: Profiling (10%), CI/CD (8%), Optimization (5%), Performance (7%), Quality (4%)

### 2. Value-Effort Efficiency Score

```
Efficiency = Σ(readiness_delta / time_estimate_h) for completed tasks
           ÷ Σ(readiness_delta / time_estimate_h) for all tasks
```

**Target:** >0.85 (completing high-ROI tasks first)

Example:
- T-CODE-001: 10 / 6 = 1.67 (excellent)
- T-ML-001: 5 / 4 = 1.25 (good)
- T-WF-006: 3 / 4 = 0.75 (lower ROI)

### 3. Critical Path Progress

Tasks unblocking others = highest priority

```
Critical Path Score = (blocking_count × 2 - dependency_count × 0.5)
                     / max_possible_blocking_score
```

**Example: T-CODE-001 (Profiling)**
- Blocks: T-CODE-003, T-CODE-004, T-CODE-007 (3 tasks)
- Depends: none (0 tasks)
- Score: (3×2 - 0×0.5) / max ≈ strong priority

### 4. Domain Balance Index

Ensure no single domain stalls:

```
Domain Balance = 1 - (std_dev(domain_readiness) / mean(domain_readiness))
```

**Healthy:** Balance > 0.8 (all domains within 20% of average)  
**Warning:** Balance < 0.6 (one domain lagging significantly)

### 5. Velocity Tracking (Hours/Week)

```
| Week | Target | Actual | % | P0 | P1 | P2 | Notes |
|------|--------|--------|----|----|----|----|-------|
| W52 | 40h | TBD | - | 6h | 20h | 14h | Kickoff week |
| W01 | 40h | - | - | - | - | - | Full execution |
```

Target: 80% of planned hours → 32h/week actual

### 6. Readiness Delta Predictions

Based on committed velocity:

```
Projected Readiness = Current% + (Completed_delta / Total_delta × 100)
```

**Forecast (assuming 80% velocity):**

Week | Code | ML | Services | Workflow | Overall
-----|------|----|---------  |----------|--------
W52 (today) | 20% | 20% | 20% | 20% | 20%
W52-end | 22% | 25% | 21% | 21% | 22.25%
W01-end | 24% | 30% | 22% | 22% | 24.5%
W02-end | 26% | 35% | 23% | 23% | 26.75%
W03-end | 28% | 40% | 25% | 24% | 29%
**EOY (Q1'26)** | **30%** | **45%** | **27%** | **26%** | **32%**
**Q2'26 Target** | **75%** | **75%** | **75%** | **75%** | **75%**

## Notification Triggers

### ✅ Automated Alerts

**1. Weekly Readiness Report**
- **When:** Every Friday 5 PM EET
- **If:** Current readiness < target by >5%
- **Action:** Recommend priority adjustment
- **Example:** "Code readiness 20% vs target 22%. Suggest focusing 3h on T-CODE-001 next week."

**2. Daily Standup Prompt**
- **When:** Every Monday 7 AM EET
- **Content:** Top 3 tasks for day (auto-ranked)
- **Format:** "Focus today: (1) T-CODE-001 [6h], (2) T-ML-002 [3h], (3) T-SVC-001 [6h]"

**3. Blocker Alert**
- **When:** Any task status changes to 'blocked'
- **Action:** Alert + recommend unblocking task
- **Example:** "T-ML-003 blocked waiting for T-ML-002. Suggest reprioritizing."

**4. Readiness Threshold**
- **When:** Domain readiness crosses 50%
- **Action:** Celebrate + transition to maintenance mode
- **Message:** "🎉 Code: 50% ready! Shift focus to stabilization & testing."

**5. Velocity Warning**
- **When:** Weekly actual < 60% of target
- **Action:** Pause and re-plan; adjust expectations
- **Trigger:** "This week only 24/40h completed (60%). Discuss: blockers, capacity, scope."

**6. Monthly Retrospective**
- **When:** Every 4th Friday
- **Content:** Velocity trends, accuracy of estimates, domain health
- **Action:** Update forecasts, adjust task weights

## Dashboard Implementation

### Minimal Setup (GitHub Issues Tracker)

Use GitHub Issues with labels + automated workflows:

```yaml
# .github/workflows/readiness-report.yml
name: Weekly Readiness Report

on:
  schedule:
    - cron: '0 17 * * 5'  # Friday 5 PM UTC (7 PM EET)

jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - name: Parse task files
        run: |
          # Extract readiness_delta & status from TASKS-*.md
          # Calculate percentages
          # Generate report markdown
      
      - name: Create issue with report
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: `Readiness Report: Week ${WEEK}`,
              body: report_markdown,
              labels: ['readiness', 'weekly-digest']
            })
```

### Enhanced Setup (Grafana/Datadog)

For production monitoring:

1. **Data Source:** Parse TASKS-*.md via CI/CD pipeline
2. **Metrics Store:** InfluxDB / Prometheus time-series
3. **Dashboard:** Grafana with:
   - Real-time readiness % by domain
   - Velocity trend (actual vs target)
   - Critical path visualization
   - Blocker queue depth
   - Burndown chart (tasks remaining)

## Readiness Definition by Domain

### Code Readiness Tiers

- **0-20%:** No profiling/optimization framework
- **20-40%:** Profiling + basic CI/CD
- **40-60%:** Optimization patterns + automated testing
- **60-75%:** Full performance baseline + deployment ready
- **75%+:** Production-hardened code with monitoring

### ML Readiness Tiers

- **0-20%:** Data contracts defined
- **20-40%:** Feature store + training pipeline
- **40-60%:** Inference service + basic monitoring
- **60-75%:** Drift detection + retraining automation
- **75%+:** End-to-end ML system production-ready

### Services Readiness Tiers

- **0-20%:** API scaffolding
- **20-40%:** Auth + DB layer
- **40-60%:** Observability + error handling
- **60-75%:** Load testing + deployment (Docker/K8s)
- **75%+:** Fully resilient, production services

### Workflow Readiness Tiers

- **0-20%:** PDP templates defined
- **20-40%:** Weekly reviews + habit tracking
- **40-60%:** OKR alignment + time management
- **60-75%:** Health/finance/relationship integration
- **75%+:** Fully integrated life optimization system

## Custom Readiness Scenarios

### "What if I pause P2 tasks and focus P0/P1?"

If 40h/week → 30h P0 + 10h P1:

```
New Velocity = (30×P0_avg_roi + 10×P1_avg_roi) / 40
            = (30×1.4 + 10×1.0) / 40
            ≈ 1.25 efficiency
            → +3% readiness/week (vs +2.25% baseline)
```

**Result:** Reach 75% in ~24 weeks vs 26 weeks (save 2 weeks)

## Integration with Quarterly Goals

**Q4 2025:** Foundation (20% → 30%)
**Q1 2026:** Acceleration (30% → 50%)
**Q2 2026:** Polish (50% → 75%)
**Q3+ 2026:** Maintenance & Expansion (75%+)

---

**Last Updated:** Dec 21, 2025  
**Next Review:** Dec 28, 2025 (Fri 5 PM EET)  
**Dashboard URL:** [Metrics](./metrics/)  
