# Consciousness Model & Integration Framework

## Overview

The Consciousness layer monitors and measures the *integration* and *coherence* of the system across multiple dimensions:

1. **Code/ML/Services Integration** — How well different technical domains align
2. **Well-being & Personal Capacity** — Your actual state from `/workflow` PDP
3. **System Stability** — Recent incidents, error rates, rollback frequency

These metrics feed into the **Consciousness Guard**, which gates automated actions.

## Core Metrics

### 1. Integration Score (0-100)

Measures cross-domain coherence. How well do changes in one domain (code, ML, services) align without conflicts?

**Calculation:**
- Code test coverage: 0-33 points
- ML data quality & model performance: 0-33 points
- Services readiness (SLO passing): 0-34 points

**Data sources:**
- `code/perf/baseline.json` — test coverage, build success
- `ml/monitoring/metrics.json` — data drift, model accuracy
- `services/readiness.json` — SLO violations, error rates

**Interpretation:**
- **80-100**: All domains green → enable autonomous actions (fast-lane)
- **60-79**: Mixed signals → require manual review for feature/infra changes
- **<60**: Significant issues → block non-critical deployments

### 2. Well-being Score (0-100)

Extracted from your `/workflow/PDP.md` and personal readiness.

**Calculation:**
- Weekly review completed: +20 points
- Sleep/energy level (from PDP): 0-30 points
- Task completion rate (this week vs target): 0-30 points
- No critical personal incidents: +20 points

**Data sources:**
- `workflow/PDP.md` — last weekly review timestamp, self-assessment
- `tasks/this_week.md` — completion ratio
- `workflow/incidents.log` — recent personal/health issues

**Interpretation:**
- **>70**: You're good → allow heavier technical work
- **50-70**: Moderate capacity → stick to planned tasks, no major experiments
- **<50**: Low capacity → defer risky changes, focus on stability

### 3. Stability Score (0-100)

System resilience and absence of recent failures.

**Calculation:**
- No production incidents in last 7 days: +30 points
- Error rate <0.5%: +30 points
- No rollbacks in last 7 days: +20 points
- All SLO gates passing: +20 points

**Data sources:**
- `.github/workflows/policy-gate.yml` logs → incidents
- Backend/services metrics → error rates
- Git commit history → rollback patterns

**Interpretation:**
- **>75**: System stable → green light for experiments
- **50-75**: Yellow zone → avoid breaking changes, require careful review
- **<50**: Red zone → rollback/remediate, pause new features

## Consciousness Guard Logic

The guard reads these 3 scores and makes decisions:

```
IF Integration >= 70 AND Well-being >= 60 AND Stability >= 70:
  ACTION = FAST (auto-merge safe changes, allow experiments)
ELIF Integration >= 50 AND Well-being >= 50 AND Stability >= 50:
  ACTION = SAFE (require manual review, block risky changes)
ELSE:
  ACTION = HALT (only essential fixes, full lock-down)
```

## How Consciousness Affects CI/CD

### With HIGH consciousness (all scores green):
- Auto-merge documentation changes
- Auto-merge passing refactors
- Allow feature deployments with normal review
- Enable experimental ML training runs

### With MEDIUM consciousness (mixed signals):
- No auto-merge, require review for all changes
- Block feature deployments until issue resolved
- Only critical bug fixes allowed
- ML model updates require explicit approval

### With LOW consciousness (red flags):
- Halt all non-essential deployments
- Rollback risky recent changes
- Block new feature work
- Enable read-only mode for external services

## Measuring & Updating Scores

Scores are recalculated:
- **Every 1 hour** during CI/CD runs (via `consciousness_guard.py`)
- **On demand** via `python consciousness/consciousness_guard.py --evaluate`
- **Weekly** during automated governance run

## Integration Points

**In `policy-gate.yml`:**
```yaml
- name: Run consciousness guard evaluation
  run: python consciousness/consciousness_guard.py --context ci
```

**In `orchestration_runner.py`:**
```python
from consciousness.consciousness_guard import Guard
guard = Guard()
if not guard.can_proceed(change_type='feature'):
    logger.warning("Consciousness check failed")
    sys.exit(1)
```

**In `workflow/PDP.md`:**
Update weekly with well-being status; system reads it automatically.
