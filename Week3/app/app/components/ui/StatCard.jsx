// import Card from './Card';

// export default function StatCard({
//   title,
//   value,
//   percentage,
//   icon,
//   trend = 'up',
// }) {
//   return (
//     <Card className="flex items-center justify-between">
//       <div>
//         <p className="text-xs text-gray-400 mb-1">{title}</p>
//         <h3 className="text-lg font-semibold text-gray-800">{value}</h3>
//         <p
//           className={`text-xs font-semibold ${
//             trend === 'up' ? 'text-green-500' : 'text-red-500'
//           }`}
//         >
//           {percentage}
//         </p>
//       </div>

//       <div className="w-12 h-12 bg-teal-400 rounded-xl flex items-center justify-center text-white">
//         {icon}
//       </div>
//     </Card>
//   );
// }
export default function StatCard({ title, value, percent, icon }) {
  const isPositive = percent >= 0;

  return (
    <div className="bg-white rounded-2xl shadow-sm p-6 flex justify-between items-center">
      {/* Left */}
      <div>
        <p className="text-sm text-gray-400">{title}</p>

        <div className="flex items-center gap-2 mt-1">
          <h2 className="text-2xl font-bold text-gray-800">{value}</h2>

          <span
            className={`text-sm font-semibold ${
              isPositive ? "text-green-500" : "text-red-500"
            }`}
          >
            {isPositive ? "+" : ""}
            {percent}%
          </span>
        </div>
      </div>

      {/* Right Icon */}
      <div className="w-12 h-12 bg-teal-400 rounded-xl flex items-center justify-center text-white">
        {icon}
      </div>
    </div>
  );
}
