import { z } from "zod";
export const userSchema = z.object({
  name: z.string().trim().min(3, "Name must be at least 3 characters"),
  email: z.string().trim().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
  age: z.number().int().nonnegative().optional(),
})
.strict();

export const productSchema = z.object({
  name: z.string().trim().min(3, "Name must be at least 3 characters"),
  price: z.number().positive("Price must be a positive number"),
  category: z.enum(["electronics", "furniture"], {
      errorMap: () => ({ message: "Invalid product category" }),
    }),
})
.strict();


const validate = (schema) => (req, res, next) => {
  try {
    req.body = schema.parse(req.body);
    next();
  } catch (err) {
    return res.status(400).json({
      message: "Validation error",
      errors: err.errors,
    });
  }
};


export const validateUser = validate(userSchema);
export const validateProduct = validate(productSchema);
