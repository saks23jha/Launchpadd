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
 * @openapi
 * /users:
 *   post:
 *     summary: Create a new user
 *     description: Registers a new user and triggers a welcome email job
 *     tags:
 *       - Users
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - name
 *               - email
 *               - password
 *             properties:
 *               name:
 *                 type: string
 *                 example: Sakshi
 *               email:
 *                 type: string
 *                 example: sakshi@example.com
 *               password:
 *                 type: string
 *                 example: password123
 *               age:
 *                 type: number
 *                 example: 25
 *     responses:
 *       201:
 *         description: User created successfully
 *       400:
 *         description: Validation error
 *       500:
 *         description: Internal server error
 */

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
