import express from "express";
import { validateUser } from "../middlewares/validate.js";

const router = express.Router();

router.post("/", validateUser, (req, res) => {
  res.status(201).json({
    message: "User created successfully",
    data: req.body
  });
});

export default router;
