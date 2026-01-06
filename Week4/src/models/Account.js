import mongoose from "mongoose";

const { Schema, model } = mongoose;

const accountSchema = new Schema(
  {
    firstName: {
      type: String,
      required: true,
      trim: true
    },
    lastName: {
      type: String,
      required: true,
      trim: true
    },
    email: {
      type: String,
      required: true,
      unique: true,
      lowercase: true
    },
    balance: {
      type: Number,
      default: 0,
      min: 0
    },
    status: {
      type: String,
      enum: ["active", "inactive"],
      default: "active"
    }
  },
  {
    timestamps: true,
    toJSON: { virtuals: true },
    toObject: { virtuals: true }
  }
);

accountSchema.virtual("fullName").get(function () {
  return `${this.firstName} ${this.lastName}`;
});

accountSchema.pre("save", function (next) {
  this.email = this.email.toLowerCase();
  next();
});

accountSchema.index({ email: 1, status: 1 });

const Account = model("Account", accountSchema);
export default Account;
