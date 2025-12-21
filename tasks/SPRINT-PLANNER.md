# Weekly Sprint Planner

Bakhmach Business Hub - Practical execution framework

## Overview

This guide automates weekly planning using the TaskPrioritizer engine. Every Friday at 5 PM EET, generate your next week's focus.

## Process: Friday Evening (30 minutes)

### 1. Review Completions (5 min)

Mark tasks as `done` that you completed this week:

```markdown
## Completed This Week
- [ ] T-CODE-001: Profiling framework (6h, +10%)
- [ ] T-ML-001: Data sources (4h, +5%)
```

### 2. Run Prioritizer (5 min)

Execute in TypeScript:

```typescript
import { TaskPrioritizer, planNextWeek } from './TASK-PRIORITIZER.ts';

const allTasks = [...]; // Load from TASKS-*.md
const completed = ['T-CODE-001', 'T-ML-001']; // Your wins

const weeklyPlan = planNextWeek(allTasks, completed, 40); // 40 hours/week

weeklyPlan.forEach(task => {
  console.log(`${task.id}: ${task.title} (${task.time_estimate_h}h, +${task.readiness_delta}%)`);
});
```

### 3. Generate Sprint Template (10 min)

Create `/weekly/SPRINT-2025-W52.md`:

```markdown
# Sprint: Week 52 (Dec 21-27, 2025)

## Budget: 40 hours / 5 days

### Monday (9h)
- [ ] T-CODE-001: Profiling (6h) - Foundation
- [ ] T-ML-002: Feature store (3h) - Blocked by above

### Tuesday (8h)
- [ ] T-ML-003: Training pipeline (8h) - Critical milestone

### Wednesday (8h)
- [ ] T-SVC-001: API scaffolding (6h) - Parallel stream
- [ ] T-CODE-005: Code review checklist (2h) - Quick win

### Thursday (9h)
- [ ] T-SVC-002: Auth layer (8h) - Continue APIs
- [ ] T-WF-001: PDP templates (1h) - Maintenance

### Friday (6h)
- [ ] T-ML-004: Inference service (4h) - Polish & test
- [ ] T-CODE-002: CI/CD setup (2h) - Cross-domain

## Status Tracking

| Task ID | Status | % Complete | Notes |
|---------|--------|------------|-------|
| T-CODE-001 | IN_PROGRESS | 50% | Profiling tools installed |
| T-ML-002 | BLOCKED | 0% | Waiting for T-CODE-001 |
| T-ML-003 | PLANNED | 0% | Ready to start Tuesday |

## Daily Standup Template

**Monday 9 AM:**
- Yesterday: Completed profiling setup
- Today: Begin ML feature store
- Blockers: None

**Weekly Review (Friday 5 PM):**
- Completed: 3 tasks, +18% readiness
- In Progress: 2 tasks (carry over)
- Blocked: 1 task (unblock next week)
- New insights: Profiling revealed memory leak in model inference

## Readiness Tracking

**Starting Week 52:**
- Code: 20%
- ML: 20%
- Services: 20%
- Workflow: 20%
- Overall: 20%

**Target End of Week 52:**
- Code: 22% (+2%)
- ML: 25% (+5%)
- Services: 21% (+1%)
- Workflow: 21% (+1%)
- Overall: 22.25% (+2.25%)

## Sprint Health Check

✅ All P0 tasks accounted for
✅ No critical blockers
✅ Domain balance achieved (all touched)
⚠️  ML stream running ahead; may need P1 pause
✅ Weekly capacity: 40h allocated perfectly

## Auto-Generated Next Week Forecast

(Assuming 80% completion rate)

If current week yields +2.25%, projected quarterly readiness by EOY:
- Week 52: 22.25%
- Week 1 (Jan): 24.5%
- Week 2 (Jan): 26.75%
- **EOY Target: 75%+ readiness by Q2 2026**

## Notification Triggers (Automated)

✅ **Sent Friday 5 PM:** Weekly review digest  
✅ **Sent Monday 7 AM:** Sprint summary + daily focus (3 top tasks)  
✅ **Sent Wednesday 12 PM:** Midweek adjustment (blocker alert if any)  
✅ **Sent Friday 4 PM:** 1-hour pre-review reminder

## Monthly Aggregation

Every 4th Friday, aggregate into monthly readiness report:

- 4 weeks × ~2.25% avg = **~9% monthly growth** (if consistent)
- By Dec 2025: 20% → 22% (first month foundation)
- By Jan 2026: 22% → 31% (full execution)
- By June 2026: 60% → 75%+ (target reached)

## Retrospective Template

Every month, update based on:

1. **Velocity:** Actual hours completed vs estimated
2. **Accuracy:** Readiness_delta predictions vs real impact
3. **Risk:** Which P1 tasks became P0 (hidden urgency)?
4. **Innovation:** Did new opportunities emerge?
5. **Health:** Personal sustainability (avoid burnout)

---

**Next Sprint Planning:** Every Friday 5 PM EET  
**Execution Start:** Every Monday 7 AM EET  
**Status Page:** [/weekly/](./weekly/)  
