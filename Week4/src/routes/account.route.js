import express from "express";
import {
  createAccount,
  getAccounts,
  updateAccount,
} from "../controllers/account.controller.js";

const router = express.Router();

router.post("/", createAccount);
router.get("/", getAccounts);
router.put("/:id", updateAccount); 
router.patch("/:id", updateAccount);

export default router;
