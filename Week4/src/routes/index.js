import express from "express";
import userRoutes from "./user.route.js";
import productRoutes from "./product.route.js";

const router = express.Router();


router.get("/health", (req, res) => {
  res.json({ status: "OK" });
});

// Mount route modules
router.use("/users", userRoutes);
router.use("/products", productRoutes);

export default router;
