import express from "express";
import userRoutes from "./user.route.js";
import productRoutes from "./product.route.js";
import accountRoutes from "./account.route.js"; // ✅ ADD THIS
import orderRoutes from "./order.route.js";  




const router = express.Router();
/**
 * @openapi
 * /health:
 *   get:
 *     summary: Health check
 *     tags: [System]
 *     responses:
 *       200:
 *         description: Service is healthy
 */

router.get("/health", (req, res) => {
  res.json({ status: "OK" });
});

// Mount route modules
router.use("/users", userRoutes);
router.use("/products", productRoutes);
router.use("/accounts", accountRoutes);
router.use("/orders", orderRoutes);



export default router;
