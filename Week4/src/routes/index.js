import express from "express";
import {
  getProducts,
  createProduct,
  deleteProduct,
} from "../controllers/product.controller.js";

const router = express.Router();

router.get("/health", (req, res) => {
  res.json({ status: "OK" });
});

router
  .route("/products")
  .get(getProducts)
  .post(createProduct);

router.delete("/products/:id", deleteProduct);

router.routeCount = 4;

export default router;
