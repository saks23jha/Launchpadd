import express from "express";
import { validateProduct } from "../middlewares/validate.js";

const router = express.Router();

router.post("/", validateProduct, (req, res) => {
  res.status(201).json({
    message: "Product created successfully",
    data: req.body
  });
});

export default router;
