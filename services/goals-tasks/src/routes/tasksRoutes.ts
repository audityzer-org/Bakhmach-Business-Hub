import { Router } from "express";
import * as tasksController from "../controllers/tasksController";

const router = Router();

router.get("/", tasksController.listTasks);
router.get("/:taskId", tasksController.getTaskById);
router.patch("/:taskId", tasksController.updateTask);

export default router;
