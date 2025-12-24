// import StatCard from '../../components/ui/StatCard';

// export default function StatsSection() {
//   return (
//     <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
//       <StatCard title="Today's Money" value="$53,000" percentage="+55%" />
//       <StatCard title="Today's Users" value="2,300" percentage="+5%" />
//       <StatCard title="New Clients" value="+3,052" percentage="-14%" />
//       <StatCard title="Total Sales" value="$173,000" percentage="+8%" />
//     </div>
//   );
// }
import StatCard from "../../components/ui/StatCard";
import { FaWallet, FaUsers, FaFileAlt, FaShoppingCart } from "react-icons/fa";

export default function StatsSection() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
      <StatCard
        title="Today's Money"
        value="$53,000"
        percent={55}
        icon={<FaWallet />}
      />
      <StatCard
        title="Today's Users"
        value="2,300"
        percent={5}
        icon={<FaUsers />}
      />
      <StatCard
        title="New Clients"
        value="+3,052"
        percent={-14}
        icon={<FaFileAlt />}
      />
      <StatCard
        title="Total Sales"
        value="$173,000"
        percent={8}
        icon={<FaShoppingCart />}
      />
    </div>
  );
}
