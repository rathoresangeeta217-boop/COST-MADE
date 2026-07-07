import React from "react";
import { Info, Calculator, Ruler, Layers, Box, Cpu } from "lucide-react";

export default function PricingRules() {
  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center gap-3 mb-8">
        <div className="bg-indigo-600 p-2 rounded-lg text-white">
          <Calculator className="w-6 h-6" />
        </div>
        <h1 className="text-2xl font-bold text-gray-900">Pricing & Calculation Rules</h1>
      </div>

      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Layers className="w-5 h-5 text-indigo-500" />
          Table Top Calculation
        </h2>
        <div className="space-y-3 text-gray-600">
          <p>The table top cost is based on the total area in square feet multiplied by the board's rate per square foot.</p>
          <ul className="list-disc list-inside space-y-2 ml-2">
            <li><strong>Area Calculation:</strong> <code className="bg-gray-100 px-1 py-0.5 rounded text-sm text-indigo-700">Width (mm) × Depth (mm) / 90,000 = Area in Sq.Ft</code></li>
            <li><strong>Top Rate:</strong> Varies depending on material (PLPB, HDHMR, Plywood), finish (Mica), and thickness (18mm, 25mm, 36mm).</li>
            <li><strong>Total Top Cost:</strong> <code className="bg-gray-100 px-1 py-0.5 rounded text-sm text-indigo-700">Area (Sq.Ft) × Top Rate (₹/Sq.Ft)</code></li>
          </ul>
        </div>
      </div>

      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Ruler className="w-5 h-5 text-indigo-500" />
          Metal Straight Legs Calculation
        </h2>
        <div className="space-y-4 text-gray-600">
          <p>Metal leg frameworks are calculated based on the running feet (rft) of pipes required, including vertical and horizontal supports, plus powder coating and accessories.</p>
          
          <div className="bg-gray-50 p-4 rounded-xl space-y-3">
            <h3 className="font-medium text-gray-900">1. Vertical Pipes (e.g., 40x40 mm or 50x50 mm)</h3>
            <ul className="list-disc list-inside text-sm space-y-1 ml-2">
              <li>Length = <code className="text-indigo-700">2 × Height</code> per leg structure.</li>
              <li>Rate = ₹27/rft for 40x40mm, ₹35/rft for 50x50mm.</li>
            </ul>

            <h3 className="font-medium text-gray-900 mt-4">2. Horizontal Support Pipes (40x20 mm)</h3>
            <ul className="list-disc list-inside text-sm space-y-1 ml-2">
              <li>Width pipes = <code className="text-indigo-700">2 × (Width - 140mm)</code></li>
              <li>Depth pipes = <code className="text-indigo-700">(Depth - 180mm) × Number of Legs</code></li>
              <li>Rate = ₹19.6/rft</li>
            </ul>

            <h3 className="font-medium text-gray-900 mt-4">3. Finishing & Accessories</h3>
            <ul className="list-disc list-inside text-sm space-y-1 ml-2">
              <li><strong>Powder Coating:</strong> <code className="text-indigo-700">Total rft (Vertical + Horizontal) × ₹30/rft</code></li>
              <li><strong>Hardware:</strong> Buffers (₹7/pc), Nuts (₹5/pc), Butterfly brackets (₹12.5/pc).</li>
            </ul>
          </div>
        </div>
      </div>

      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Box className="w-5 h-5 text-indigo-500" />
          Metal U-Shape Legs Calculation
        </h2>
        <div className="space-y-4 text-gray-600">
          <p>The U-Shape leg calculation follows the same structural framework as Straight legs, with the addition of a bottom horizontal loop for each leg structure.</p>
          <div className="bg-gray-50 p-4 rounded-xl space-y-3">
            <ul className="list-disc list-inside text-sm space-y-2 ml-2">
              <li><strong>Additional Vertical Pipe:</strong> U-Shape legs have a bottom loop matching the depth of the table.</li>
              <li><strong>Formula:</strong> <code className="text-indigo-700">Vertical Length + (Depth × Number of Legs)</code></li>
              <li>All horizontal supports, powder coating (₹30/rft), and accessories costs remain identical in logic to the straight leg calculation but apply to the increased pipe running feet.</li>
            </ul>
          </div>
        </div>
      </div>

      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Cpu className="w-5 h-5 text-indigo-500" />
          Overheads & Profit
        </h2>
        <div className="space-y-3 text-gray-600">
          <ul className="list-disc list-inside space-y-2 ml-2">
            <li><strong>Making Charges (Labor):</strong> Calculated per square foot of the table top area (e.g., ₹250 to ₹300 per sq.ft depending on the table type).</li>
            <li><strong>Packing Cost:</strong> Fixed addition (e.g., ₹150).</li>
            <li><strong>Tooling Cost:</strong> Fixed addition (e.g., ₹100).</li>
            <li><strong>Profit Margin:</strong> A fixed percentage (e.g., 25%) applied on top of the total material, labor, packing, and tooling costs combined.</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
