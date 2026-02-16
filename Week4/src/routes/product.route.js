import express from "express";
import { validateProduct } from "../middlewares/validate.js";
import {
  getProducts,
  createProduct,
  deleteProduct,
} from "../controllers/product.controller.js";

const router = express.Router();

/**
 * @openapi
 * /products:
 *   post:
 *     summary: Create a new product
 *     description: Adds a new product to the system
 *     tags:
 *       - Products
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - name
 *               - price
 *               - category
 *             properties:
 *               name:
 *                 type: string
 *                 example: Laptop
 *               price:
 *                 type: number
 *                 example: 55000
 *               category:
 *                 type: string
 *                 example: electronics
 *     responses:
 *       201:
 *         description: Product created successfully
 *       400:
 *         description: Validation error
 *       500:
 *         description: Internal server error
 */
router.post("/", validateProduct, createProduct);

/**
 * @openapi
 * /products:
 *   get:
 *     summary: Get all products
 *     description: Fetches a list of all products
 *     tags:
 *       - Products
 *     responses:
 *       200:
 *         description: List of products retrieved successfully
 *       500:
 *         description: Internal server error
 */
router.get("/", getProducts);

/**
 * @openapi
 * /products/{id}:
 *   delete:
 *     summary: Delete a product
 *     description: Deletes a product by its ID
 *     tags:
 *       - Products
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: Product ID
 *     responses:
 *       200:
 *         description: Product deleted successfully
 *       404:
 *         description: Product not found
 *       500:
 *         description: Internal server error
 */
router.delete("/:id", deleteProduct);

export default router;
