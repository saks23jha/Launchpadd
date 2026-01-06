import mongoose from "mongoose";

const { Schema, model } = mongoose;

const orderSchema = new Schema(
  {
    accountId: {
      type: Schema.Types.ObjectId,
      ref: "Account",
      required: true,
      index: true
    },
    product: {
      type: String,
      required: true,
      trim: true
    },
    amount: {
      type: Number,
      required: true,
      min: 0
    },
    deliveredAt: {
      type: Date,
      default: null
    }
  },
  {
    timestamps: true
  }
);

orderSchema.index({ accountId: 1, _id: -1 });
orderSchema.index({ deliveredAt: 1 });

orderSchema.virtual("isDelivered").get(function () {
  return !!this.deliveredAt;
});

const Order = model("Order", orderSchema);
export default Order;
