import mongoose from "mongoose";
import bcrypt from "bcrypt";

const { Schema, model } = mongoose;

const accountSchema = new Schema(
  {
    firstName: {
      type: String,
      required: true,
      trim: true,
    },
    lastName: {
      type: String,
      required: true,
      trim: true,
    },
    email: {
      type: String,
      required: true,
      unique: true,
      lowercase: true,
    },
    password: {
      type: String,
      required: true,
      minlength: 6,
      select: false, //  hide password by default
    },
    balance: {
      type: Number,
      default: 0,
      min: 0,
    },
    status: {
      type: String,
      enum: ["active", "inactive"],
      default: "active",
    },
  },
  {
    timestamps: true,
    toJSON: { virtuals: true },
    toObject: { virtuals: true },
  }
);

// Virtual field
accountSchema.virtual("fullName").get(function () {
  return `${this.firstName} ${this.lastName}`;
});

// Hash password before save
accountSchema.pre("save", async function () {
  if (!this.isModified("password")) return;

  const saltRounds = 10;
  this.password = await bcrypt.hash(this.password, saltRounds);
});

// Indexes
accountSchema.index({ email: 1, status: 1 });
accountSchema.index({ status: 1, createdAt: -1 });
accountSchema.set("toJSON", {
  transform: function (doc, ret) {
    delete ret.password;
    return ret;
  }
});


const Account = model("Account", accountSchema);
export default Account;
