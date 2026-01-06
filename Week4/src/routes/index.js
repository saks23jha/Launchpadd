import express from "express";
import userRoutes from "./user.route.js";
import {
  getProducts,
  createProduct,
  deleteProduct,
} from "../controllers/product.controller.js";

const router = express.Router();

router.get("/health", (req, res) => {
  res.json({ status: "OK" });
});

// Mount user routes under /users
router.use("/users", userRoutes);

// Product routes
router
  .route("/products")
  .get(getProducts)
  .post(createProduct);

router.delete("/products/:id", deleteProduct);

router.routeCount = 5; // increased by 1

export default router;
