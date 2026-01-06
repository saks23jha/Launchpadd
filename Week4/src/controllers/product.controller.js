import * as productService from "../services/product.services.js";

/**
 * GET /products
 */
export const getProducts = async (req, res, next) => {
  try {
    const result = await productService.getProducts(req.query);

    res.status(200).json({
      success: true,
      data: result.data,
      meta: result.meta,
    });
  } catch (error) {
    next(error);
  }
};

/**
 * POST /products
 */
export const createProduct = async (req, res, next) => {
  try {
    const product = await productService.createProduct(req.body);

    res.status(201).json({
      success: true,
      data: product,
    });
  } catch (error) {
    next(error);
  }
};

/**
 * DELETE /products/:id
 * Soft delete → sets deletedAt
 */
export const deleteProduct = async (req, res, next) => {
  try {
    const product = await productService.softDeleteProduct(req.params.id);

    res.status(200).json({
      success: true,
      message: "Product deleted successfully",
      data: product,
    });
  } catch (error) {
    next(error);
  }
};
