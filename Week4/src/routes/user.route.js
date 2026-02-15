import express from "express";
import sendEmailJob from "../jobs/email.job.js";
import logger from "../utils/logger.js";
import {
  getUsers,
  createUser,
} from "../controllers/user.controller.js";
import { validateUser } from "../middlewares/validate.js";

const router = express.Router();
router.post("/", validateUser, async (req, res, next) => {
  try {
    // delegate to controller
    await createUser(req, res, next);
    sendEmailJob({
      email: req.body.email,
      name: req.body.name,
      type: "WELCOME_EMAIL",
    }).catch((err) => {
      logger.error("Email job failed", {
        error: err.message,
        requestID: req.requestID,
      });
    });

    logger.info("User registered", { requestID: req.requestID });
  } catch (error) {
    next(error);
  }
});


router.get("/", getUsers);

export default router;
