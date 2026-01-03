import { Router } from "express";
import * as goalsController from "../controllers/goalsController";

const router = Router();

router.post("/", goalsController.createGoal);
router.get("/", goalsController.listGoals);
router.get("/:goalId", goalsController.getGoalById);
router.patch("/:goalId", goalsController.updateGoal);

router.post("/:goalId/tasks", goalsController.createTaskForGoal);

export default router;
