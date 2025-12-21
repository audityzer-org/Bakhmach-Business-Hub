/**
 * TASK PRIORITIZER: Advanced sorting and recommendation engine
 * Bakhmach Business Hub - Task Management System
 * 
 * Algorithms:
 * 1. Value/Effort Ratio: readiness_delta / time_estimate_h
 * 2. Critical Path: dependency-aware sequencing
 * 3. Domain Balance: prevent bottlenecking
 * 4. Priority Tier: P0 > P1 > P2 > P3
 */

export interface Task {
  id: string;
  title: string;
  priority: 'P0' | 'P1' | 'P2' | 'P3';
  domain: 'code' | 'ml' | 'services' | 'workflow' | 'consciousness';
  milestone: string;
  readiness_delta: number;
  time_estimate_h: number;
  status: 'planned' | 'in_progress' | 'blocked' | 'done';
  deps: string[];
}

export interface PrioritizationScore {
  taskId: string;
  valueEffortRatio: number;
  criticalPathScore: number;
  domainBalanceScore: number;
  priorityWeight: number;
  compositeScore: number;
  recommendation: 'URGENT' | 'HIGH' | 'MEDIUM' | 'LOW';
}

export class TaskPrioritizer {
  private tasks: Task[] = [];
  private completedTasks: Set<string> = new Set();

  constructor(tasks: Task[], completed: string[] = []) {
    this.tasks = tasks;
    this.completedTasks = new Set(completed);
  }

  /**
   * Primary: Value-to-Effort Ratio (ROI per hour)
   */
  private calculateValueEffortRatio(task: Task): number {
    const baseRatio = task.readiness_delta / Math.max(task.time_estimate_h, 1);
    return baseRatio;
  }

  /**
   * Secondary: Critical Path Score
   * Tasks blocking others get higher urgency
   */
  private calculateCriticalPathScore(task: Task): number {
    const blockingCount = this.tasks.filter(
      t => t.deps.includes(task.id) && !this.completedTasks.has(t.id)
    ).length;
    
    const dependencyCount = task.deps.filter(
      d => !this.completedTasks.has(d)
    ).length;
    
    // Tasks unblocking many others score high
    return blockingCount * 2 - dependencyCount * 0.5;
  }

  /**
   * Tertiary: Domain Balance
   * Ensure no single domain dominates; enable parallel progress
   */
  private calculateDomainBalanceScore(task: Task): number {
    const domainProgress = new Map<string, number>();
    
    this.tasks.forEach(t => {
      if (!domainProgress.has(t.domain)) {
        domainProgress.set(t.domain, 0);
      }
      const current = domainProgress.get(t.domain) || 0;
      if (!this.completedTasks.has(t.id)) {
        domainProgress.set(t.domain, current + t.readiness_delta);
      }
    });

    const avgProgress = Array.from(domainProgress.values()).reduce((a, b) => a + b, 0) / domainProgress.size;
    const taskDomainProgress = domainProgress.get(task.domain) || 0;
    
    // Lower progress in domain = higher boost
    return avgProgress - taskDomainProgress > 0 ? 1.5 : 0.8;
  }

  /**
   * Quaternary: Priority Tier Weight
   */
  private getPriorityWeight(priority: string): number {
    const weights: { [key: string]: number } = {
      'P0': 4,
      'P1': 3,
      'P2': 2,
      'P3': 1
    };
    return weights[priority] || 1;
  }

  /**
   * Can task be started? Check all dependencies are done
   */
  private canStartTask(task: Task): boolean {
    return task.deps.length === 0 || task.deps.every(d => this.completedTasks.has(d));
  }

  /**
   * MAIN: Calculate composite priority score
   */
  calculatePrioritization(task: Task): PrioritizationScore {
    const valueEffort = this.calculateValueEffortRatio(task);
    const criticalPath = this.calculateCriticalPathScore(task);
    const domainBalance = this.calculateDomainBalanceScore(task);
    const priorityWeight = this.getPriorityWeight(task.priority);

    // Composite: weighted sum
    const compositeScore = 
      (valueEffort * 0.35) +
      (criticalPath * 0.30) +
      (domainBalance * 0.20) +
      (priorityWeight * 0.15);

    // Recommendation logic
    let recommendation: 'URGENT' | 'HIGH' | 'MEDIUM' | 'LOW';
    if (task.priority === 'P0' || compositeScore >= 3.5) {
      recommendation = 'URGENT';
    } else if (compositeScore >= 2.5) {
      recommendation = 'HIGH';
    } else if (compositeScore >= 1.5) {
      recommendation = 'MEDIUM';
    } else {
      recommendation = 'LOW';
    }

    return {
      taskId: task.id,
      valueEffortRatio: valueEffort,
      criticalPathScore: criticalPath,
      domainBalanceScore: domainBalance,
      priorityWeight,
      compositeScore,
      recommendation
    };
  }

  /**
   * Get prioritized task list for current sprint
   */
  getPrioritizedSprintTasks(maxTasks: number = 5): Task[] {
    const scoredTasks = this.tasks
      .filter(t => t.status === 'planned' && this.canStartTask(t))
      .map(t => ({
        task: t,
        score: this.calculatePrioritization(t)
      }))
      .sort((a, b) => b.score.compositeScore - a.score.compositeScore)
      .slice(0, maxTasks);

    return scoredTasks.map(st => st.task);
  }

  /**
   * Weekly planner: balance P0 + high-impact P1
   */
  getWeeklyPlan(weeksHours: number = 40): Task[] {
    const eligible = this.tasks.filter(
      t => t.status === 'planned' && this.canStartTask(t)
    );

    const p0Tasks = eligible.filter(t => t.priority === 'P0');
    const p1Tasks = eligible.filter(t => t.priority === 'P1');
    
    const scoreP0 = p0Tasks.map(t => ({
      task: t,
      score: this.calculatePrioritization(t)
    })).sort((a, b) => b.score.compositeScore - a.score.compositeScore);

    const scoreP1 = p1Tasks.map(t => ({
      task: t,
      score: this.calculatePrioritization(t)
    })).sort((a, b) => b.score.compositeScore - a.score.compositeScore);

    // Allocate: 60% to P0, 40% to P1 (or all P0 if urgent)
    const weeklyPlan: Task[] = [];
    let hoursBudget = weeksHours;

    for (const { task } of scoreP0) {
      if (hoursBudget >= task.time_estimate_h) {
        weeklyPlan.push(task);
        hoursBudget -= task.time_estimate_h;
      }
    }

    for (const { task } of scoreP1) {
      if (hoursBudget >= task.time_estimate_h) {
        weeklyPlan.push(task);
        hoursBudget -= task.time_estimate_h;
      }
    }

    return weeklyPlan;
  }

  /**
   * Monthly focus: group by domain & critical milestones
   */
  getMonthlyFocusAreas(): Map<string, Task[]> {
    const focusMap = new Map<string, Task[]>();
    
    this.tasks
      .filter(t => t.status === 'planned' && this.canStartTask(t))
      .forEach(task => {
        if (!focusMap.has(task.domain)) {
          focusMap.set(task.domain, []);
        }
        focusMap.get(task.domain)!.push(task);
      });

    // Sort within each domain
    focusMap.forEach(tasks => {
      tasks.sort((a, b) => {
        const scoreA = this.calculatePrioritization(a).compositeScore;
        const scoreB = this.calculatePrioritization(b).compositeScore;
        return scoreB - scoreA;
      });
    });

    return focusMap;
  }

  /**
   * Health check: identify blockers and risks
   */
  analyzeBlockers(): { blocked: Task[]; unblockingOpportunities: Task[] } {
    const blocked = this.tasks.filter(
      t => t.status === 'planned' && !this.canStartTask(t)
    );

    const unblockingOpps = this.tasks.filter(t => {
      const blocks = blocked.filter(b => b.deps.includes(t.id));
      return blocks.length > 0 && this.canStartTask(t);
    });

    return {
      blocked,
      unblockingOpportunities: unblockingOpps
    };
  }
}

/**
 * Export helpers for quick usage
 */
export function recommendTodaysTasks(tasks: Task[], completed: string[]): Task[] {
  const prioritizer = new TaskPrioritizer(tasks, completed);
  return prioritizer.getPrioritizedSprintTasks(3);
}

export function planNextWeek(tasks: Task[], completed: string[], hours: number = 40): Task[] {
  const prioritizer = new TaskPrioritizer(tasks, completed);
  return prioritizer.getWeeklyPlan(hours);
}
