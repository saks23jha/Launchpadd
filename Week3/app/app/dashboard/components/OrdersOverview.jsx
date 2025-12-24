
import Card from "../../components/ui/Card";
import Image from "next/image";

export default function OrdersOverview() {
  return (
    <Card className="flex justify-between items-stretch min-h-[200px]">
      
      {/* LEFT CONTENT */}
      <div className="flex flex-col justify-start pt-4">
        <p className="text-sm text-gray-400">Built by developers</p>

        <h3 className="text-lg font-semibold mt-1">
          Purity UI Dashboard
        </h3>

        <p className="text-sm text-gray-400 mt-2 max-w-sm">
          From colors, cards, typography to complex elements.
        </p>

        <button className="mt-auto text-sm font-semibold text-teal-500">
          Read more →
        </button>
      </div>

      {/* RIGHT IMAGE BLOCK */}
      <div className="w-[260px] h-full bg-teal-400 rounded-xl flex items-center justify-center">
        <div className="flex items-center gap-3">
          <Image
            src="/chakra-logo.png"
            alt="Chakra Logo"
            width={36}
            height={36}
          />
          <span className="text-white font-semibold text-lg">
            chakra
          </span>
        </div>
      </div>

    </Card>
  );
}
