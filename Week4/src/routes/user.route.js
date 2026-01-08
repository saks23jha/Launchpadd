import express from "express";
import sendEmailJob from "../jobs/email.job.js";
import logger from "../utils/logger.js";
import {
  getUsers,
  createUser,
} from "../controllers/user.controller.js";
import { validateUser } from "../middlewares/validate.js";

const router = express.Router();

/**
 * @swagger
 * /users:
 *   post:
 *     summary: Create a new user
 *     tags:
 *       - Users
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               name:
 *                 type: string
 *               email:
 *                 type: string
 *               password:
 *                 type: string
 *     responses:
 *       201:
 *         description: User created successfully
 */
router.post("/", validateUser, async (req, res, next) => {
  try {
    // delegate to controller
    await createUser(req, res, next);

    // fire-and-forget background job
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

/**
 * @swagger
 * /users:
 *   get:
 *     summary: Get all users
 *     tags:
 *       - Users
 *     responses:
 *       200:
 *         description: Users fetched successfully
 */
router.get("/", getUsers);

export default router;
