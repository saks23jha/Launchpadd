
import express from "express";
import { validateProduct } from "../middlewares/validate.js";
import {
  getProducts,
  createProduct,
  deleteProduct,
} from "../controllers/product.controller.js";

const router = express.Router();


router.post("/", validateProduct, createProduct);


router.get("/", getProducts);

router.delete("/:id", deleteProduct);

export default router;
