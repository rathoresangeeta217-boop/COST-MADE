import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

# I will write a fresh component to replace the content
new_content = """import { useState, useMemo, useEffect } from "react";
import { useParams, useSearchParams, useNavigate } from "react-router-dom";
import { useProjectStore } from "../store/useProjectStore";
import {
  Calculator,
  LayoutGrid,
  Ruler,
  FileBox,
  IndianRupee,
  Download,
  FileSpreadsheet,
  X,
  Copy,
  Info,
} from "lucide-react";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import * as XLSX from "xlsx";

export const getBoards = (quality: string) => [
  { id: "plpb", name: "PLPB", costPerSqFt: quality === "affordable" ? 34 : 49 },
  { id: "mdf", name: "MDF", costPerSqFt: quality === "affordable" ? 38 : 61 },
  {
    id: "hdhmr",
    name: "HDHMR",
    costPerSqFt: quality === "affordable" ? 99 : 74,
  },
  {
    id: "ply_laminate",
    name: "PLY LAMINATE",
    costPerSqFt: quality === "affordable" ? 55 : 130,
  },
  { id: "hdhmr_laminate", name: "HDHMR LAMINATE", costPerSqFt: 130 },
  {
    id: "ply_century_one_mm_laminate",
    name: "PLY CENTURY ONE MM LAMINATE",
    costPerSqFt: 230,
  },
];

export const getAvailableThicknesses = (
  boardId: string,
  quality: string,
): number[] => {
  if (quality === "affordable") {
    switch (boardId) {
      case "plpb":
        return [11, 17, 18, 25];
      case "mdf":
        return [17, 18, 25, 35];
      case "hdhmr":
        return [16.75, 18, 25];
      case "ply_laminate":
      case "ply_century_one_mm_laminate":
        return [6, 9, 12, 15, 16, 18];
      default:
        return [18];
    }
  } else {
    switch (boardId) {
      case "plpb":
        return [18, 25, 36];
      case "hdhmr":
        return [18, 25];
      case "mdf":
        return [18, 25, 36];
      case "ply_century_one_mm_laminate":
        return [18, 25];
      default:
        return [18];
    }
  }
};

export const getTopRate = (
  boardId: string,
  baseRate: number,
  topThickness: number,
  quality: string,
) => {
  if (quality === "affordable") {
    if (boardId === "plpb") {
      if (topThickness === 11) return 27;
      if (topThickness === 17) return 29;
      if (topThickness === 18) return 34;
      if (topThickness === 25) return 42;
    }
    if (boardId === "hdhmr") {
      if (Math.abs(topThickness - 16.75) < 0.1) return 88;
      if (topThickness === 18) return 99;
      if (topThickness === 25) return 135;
    }
    if (boardId === "ply_laminate") {
      if (topThickness === 6) return 22;
      if (topThickness === 9) return 35;
      if (topThickness === 12) return 38;
      if (topThickness === 15) return 46;
      if (topThickness === 16) return 46;
      if (topThickness === 18) return 55;
    }
    if (boardId === "mdf") {
      if (topThickness === 17) return 55;
      if (topThickness === 18) return 60;
      if (topThickness === 25) return 80;
      if (topThickness === 35) return 112;
    }
  } else {
    // Standard quality logic
    if (boardId === "plpb") {
      if (topThickness === 18) return 49;
      if (topThickness === 25) return 63;
      if (topThickness === 36) return 98;
    }
    if (boardId === "hdhmr") {
      if (topThickness === 25) return 108;
    }
    if (boardId === "mdf") {
      if (topThickness === 18) return 61;
      if (topThickness === 25) return 83;
      if (topThickness === 36) return 122;
    }
  }
  return baseRate * (topThickness / 18);
};

const LABOR_COST = 300; // Conference tables have higher making charges
const PACKING_COST = 150;
const TOOLING_COST = 100;
const PROFIT_PERCENTAGE = 0.25;

const WIRE_MANAGER_COST = 450;
const RACEWAY_COST = 800; // per length

const LEATHERLITE_COST = 2000;

export function calculateConferenceCost({
  mainWidth,
  mainDepth,
  height,
  topThickness,
  boardId,
  quality,
  legType,
  wireManagement,
  addLeatherlite,
}: any) {
  const boards = getBoards(quality);
  const board = boards.find((b) => b.id === boardId)!;

  let topRate = getTopRate(board.id, board.costPerSqFt, topThickness, quality);

  const mainTopAreaSqMm = mainWidth * mainDepth;
  const topCost = (mainTopAreaSqMm / 90000) * topRate;

  const mainTopSqFt = mainTopAreaSqMm / 90000;
  
  const bDetails = [
    {
      label: `Table Top (${mainWidth}x${mainDepth}x${topThickness}mm) - ${board.name} (${mainTopSqFt.toFixed(2)} sq.ft)`,
      cost: Math.round(topCost),
    },
  ];

  let bCostTotal = topCost;

  // Legs Calculation
  let legCount = mainWidth >= 2400 ? 3 : 2;
  let legCostTotal = 0;
  let legDesc = "";

  if (legType === "metal_straight") {
      legCostTotal = legCount * 1500;
      legDesc = `${legCount}x Metal Straight Legs`;
  } else if (legType === "metal_u") {
      legCostTotal = legCount * 1800;
      legDesc = `${legCount}x Metal U-Shape Legs`;
  } else {
      let areaPerLegSqMm = 0;
      let legRate = board.costPerSqFt; // use base rate
      if (legType === "board") {
          areaPerLegSqMm = (mainDepth - 200) * height; // simple slab
          legDesc = `${legCount}x Board Slab Legs`;
      } else if (legType === "box_plain") {
          areaPerLegSqMm = (400 * 4) * height; // 400x400 box
          legDesc = `${legCount}x Box Legs (Plain)`;
      } else if (legType === "box_fluted") {
          areaPerLegSqMm = (400 * 4) * height;
          legRate += 100; // fluted premium
          legDesc = `${legCount}x Box Legs (Fluted)`;
      } else if (legType === "round_plain") {
          areaPerLegSqMm = 1200 * height; // ~380 dia
          legDesc = `${legCount}x Round Legs (Plain)`;
      } else if (legType === "round_fluted") {
          areaPerLegSqMm = 1200 * height;
          legRate += 100; // fluted premium
          legDesc = `${legCount}x Round Legs (Fluted)`;
      }

      const totalLegAreaSqFt = (areaPerLegSqMm * legCount) / 90000;
      legCostTotal = totalLegAreaSqFt * legRate;
  }

  if (legCostTotal > 0) {
      bDetails.push({
          label: legDesc,
          cost: Math.round(legCostTotal)
      });
      bCostTotal += legCostTotal;
  }

  // Modesty Panel (default one central modesty for stability)
  const modestyAreaSqMm = (mainWidth - 200) * 400; // 400mm high modesty
  const modestyAreaSqFt = modestyAreaSqMm / 90000;
  const modestyCost = modestyAreaSqFt * board.costPerSqFt;
  bDetails.push({
      label: `Modesty Panel (${modestyAreaSqFt.toFixed(2)} sq.ft)`,
      cost: Math.round(modestyCost)
  });
  bCostTotal += modestyCost;

  let hardwareDetails = [];
  let hardwareCostTotal = 0;

  // Wire Management
  if (wireManagement === "aluminum_flip_box") {
      let qty = mainWidth >= 2400 ? 2 : 1;
      let cost = qty * WIRE_MANAGER_COST;
      hardwareDetails.push({ label: `Aluminum Flip Box (${qty} pcs)`, cost });
      hardwareCostTotal += cost;
  } else if (wireManagement === "wire_raceway") {
      let qty = mainWidth >= 2400 ? 2 : 1;
      let cost = qty * RACEWAY_COST;
      hardwareDetails.push({ label: `Wire Raceway (${qty} pcs)`, cost });
      hardwareCostTotal += cost;
  }

  // Add-ons
  let addonDetails = [];
  let addonCostTotal = 0;

  if (addLeatherlite) {
      addonDetails.push({ label: `Leatherlite Design Pad`, cost: LEATHERLITE_COST });
      addonCostTotal += LEATHERLITE_COST;
  }

  // General Hardware (Screws, L Patti, Buffers)
  const generalHardwareCost = 150;
  hardwareDetails.push({ label: "Minifix, L-Patti, Buffers, Screws", cost: generalHardwareCost });
  hardwareCostTotal += generalHardwareCost;

  let totalMaterialCost = bCostTotal + hardwareCostTotal + addonCostTotal;
  const makingCharges = LABOR_COST * mainTopSqFt; // labor based on top size
  const totalCostBeforeProfit = totalMaterialCost + makingCharges + PACKING_COST + TOOLING_COST;
  const profit = totalCostBeforeProfit * PROFIT_PERCENTAGE;
  const finalPrice = totalCostBeforeProfit + profit;

  return {
    boardPiecesDetails: bDetails,
    hardwareDetails,
    addonDetails,
    makingCharges: Math.round(makingCharges),
    packing: PACKING_COST,
    tooling: TOOLING_COST,
    profit: Math.round(profit),
    totalCost: Math.round(finalPrice),
    boardCostTotal: Math.round(bCostTotal),
    hardwareCostTotal: Math.round(hardwareCostTotal),
    addonCostTotal: Math.round(addonCostTotal),
  };
}

export default function ConferenceTableCalculator() {
  const { projectId } = useParams();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const editItemId = searchParams.get("edit");
  const {
    projects,
    addItemToProject,
    updateItemInProject,
    activeProjectId,
  } = useProjectStore();

  const currentProject = projects.find(
    (p) => p.id === (projectId || activeProjectId),
  );
  const editItem = currentProject?.items.find((i) => i.id === editItemId);

  const [mainWidth, setMainWidth] = useState<number>(2400); // mm
  const [mainDepth, setMainDepth] = useState<number>(1200); // mm
  const [height, setHeight] = useState<number>(750); // mm

  const [quality, setQuality] = useState<string>("standard");
  const [boardId, setBoardId] = useState<string>("plpb");
  const [topThickness, setTopThickness] = useState<number>(25); // mm

  const [legType, setLegType] = useState<string>("metal_straight");
  const [wireManagement, setWireManagement] = useState<string>("none");
  const [addLeatherlite, setAddLeatherlite] = useState<boolean>(false);

  useEffect(() => {
    if (editItem && editItem.config) {
      setMainWidth(editItem.config.mainWidth || 2400);
      setMainDepth(editItem.config.mainDepth || 1200);
      setHeight(editItem.config.height || 750);
      setQuality(editItem.config.quality || "standard");
      setBoardId(editItem.config.boardId || "plpb");
      setTopThickness(editItem.config.topThickness || 25);
      setLegType(editItem.config.legType || "metal_straight");
      setWireManagement(editItem.config.wireManagement || "none");
      setAddLeatherlite(editItem.config.addLeatherlite || false);
    }
  }, [editItem]);

  const boards = getBoards(quality);
  const availableThicknesses = getAvailableThicknesses(boardId, quality);

  useEffect(() => {
    if (!availableThicknesses.includes(topThickness)) {
      setTopThickness(availableThicknesses[0]);
    }
  }, [boardId, quality, availableThicknesses]);

  const costSummary = useMemo(() => {
    return calculateConferenceCost({
      mainWidth,
      mainDepth,
      height,
      topThickness,
      boardId,
      quality,
      legType,
      wireManagement,
      addLeatherlite,
    });
  }, [
    mainWidth,
    mainDepth,
    height,
    topThickness,
    boardId,
    quality,
    legType,
    wireManagement,
    addLeatherlite,
  ]);

  const handleSave = () => {
    if (!currentProject) {
      alert("No active project selected. Please select or create a project first.");
      return;
    }

    const itemData = {
      productType: "conference-table" as const,
      name: `Conference Table ${mainWidth}x${mainDepth}`,
      quantity: editItem?.quantity || 1,
      config: {
        mainWidth,
        mainDepth,
        height,
        topThickness,
        boardId,
        quality,
        legType,
        wireManagement,
        addLeatherlite,
      },
      costSummary,
    };

    if (editItemId) {
      updateItemInProject(currentProject.id, editItemId, itemData);
    } else {
      addItemToProject(currentProject.id, itemData);
    }

    navigate(`/project/${currentProject.id}`);
  };

  return (
    <div className="space-y-6 animate-in fade-in zoom-in-95 duration-500">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-semibold tracking-tight text-gray-900">
            {editItemId ? "Edit Conference Table" : "Conference Table Configurator"}
          </h1>
          <p className="text-sm text-gray-500 mt-1">
            Calculate manufacturing costs for conference tables.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 space-y-8">
            {/* Dimensions */}
            <section>
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <Ruler className="w-5 h-5 text-indigo-500" />
                Table Dimensions
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">Width (mm)</label>
                  <input
                    type="number"
                    value={mainWidth}
                    onChange={(e) => setMainWidth(Number(e.target.value))}
                    className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none"
                    min="1200"
                    step="100"
                  />
                </div>
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">Depth (mm)</label>
                  <input
                    type="number"
                    value={mainDepth}
                    onChange={(e) => setMainDepth(Number(e.target.value))}
                    className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none"
                    min="600"
                    step="50"
                  />
                </div>
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">Height (mm)</label>
                  <input
                    type="number"
                    value={height}
                    onChange={(e) => setHeight(Number(e.target.value))}
                    className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none"
                    min="700"
                    max="1100"
                    step="10"
                  />
                </div>
              </div>
            </section>

            {/* Board Quality & Material */}
            <section>
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <FileBox className="w-5 h-5 text-indigo-500" />
                Board Specifications
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">Quality</label>
                  <select
                    value={quality}
                    onChange={(e) => setQuality(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none bg-white"
                  >
                    <option value="standard">Standard Quality</option>
                    <option value="affordable">Affordable Quality</option>
                  </select>
                </div>
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">Material Type</label>
                  <select
                    value={boardId}
                    onChange={(e) => setBoardId(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none bg-white"
                  >
                    {boards.map((b) => (
                      <option key={b.id} value={b.id}>{b.name}</option>
                    ))}
                  </select>
                </div>
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">Thickness (mm)</label>
                  <select
                    value={topThickness}
                    onChange={(e) => setTopThickness(Number(e.target.value))}
                    className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none bg-white"
                  >
                    {availableThicknesses.map((t) => (
                      <option key={t} value={t}>{t}mm</option>
                    ))}
                  </select>
                </div>
              </div>
            </section>

            {/* Legs */}
            <section>
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <LayoutGrid className="w-5 h-5 text-indigo-500" />
                Legs
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">Leg Type</label>
                  <select
                    value={legType}
                    onChange={(e) => setLegType(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none bg-white"
                  >
                    <optgroup label="Metal Legs">
                      <option value="metal_straight">Straight Legs</option>
                      <option value="metal_u">U-Shape Leg</option>
                    </optgroup>
                    <optgroup label="Board Legs">
                      <option value="board">Same as Table</option>
                      <option value="box_plain">Box Legs (Plain)</option>
                      <option value="box_fluted">Box Legs (Fluted)</option>
                      <option value="round_plain">Round Leg (Plain)</option>
                      <option value="round_fluted">Round Leg (Fluted)</option>
                    </optgroup>
                  </select>
                </div>
              </div>
            </section>

            {/* Wire Management */}
            <section>
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <LayoutGrid className="w-5 h-5 text-indigo-500" />
                Wire Management
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">Option</label>
                  <select
                    value={wireManagement}
                    onChange={(e) => setWireManagement(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none bg-white"
                  >
                    <option value="none">None</option>
                    <option value="aluminum_flip_box">Aluminum Flip Box</option>
                    <option value="wire_raceway">Wire Raceway</option>
                  </select>
                </div>
              </div>
            </section>

            {/* Add-ons */}
            <section>
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <FileBox className="w-5 h-5 text-indigo-500" />
                Add-ons
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <label className="flex items-center gap-3 p-4 border border-gray-200 rounded-xl cursor-pointer hover:bg-gray-50 transition-colors">
                  <input
                    type="checkbox"
                    checked={addLeatherlite}
                    onChange={(e) => setAddLeatherlite(e.target.checked)}
                    className="w-5 h-5 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500"
                  />
                  <div className="flex flex-col">
                    <span className="font-medium text-gray-900">Leatherlite Design</span>
                    <span className="text-sm text-gray-500">Add premium leather pad in center</span>
                  </div>
                </label>
              </div>
            </section>

          </div>
        </div>

        {/* Cost Summary Widget */}
        <div className="lg:col-span-1">
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 sticky top-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <IndianRupee className="w-6 h-6 text-indigo-600" />
              Cost Summary
            </h2>
            <div className="space-y-4">
              <div className="flex justify-between items-center text-sm">
                <span className="text-gray-600">Board Costs</span>
                <span className="font-medium text-gray-900">₹{costSummary.boardCostTotal.toLocaleString()}</span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-gray-600">Hardware & Legs</span>
                <span className="font-medium text-gray-900">₹{costSummary.hardwareCostTotal.toLocaleString()}</span>
              </div>
              {costSummary.addonCostTotal > 0 && (
                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-600">Add-ons</span>
                  <span className="font-medium text-gray-900">₹{costSummary.addonCostTotal.toLocaleString()}</span>
                </div>
              )}
              <div className="flex justify-between items-center text-sm">
                <span className="text-gray-600">Making Charges</span>
                <span className="font-medium text-gray-900">₹{costSummary.makingCharges.toLocaleString()}</span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-gray-600">Packing & Tooling</span>
                <span className="font-medium text-gray-900">₹{(costSummary.packing + costSummary.tooling).toLocaleString()}</span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-gray-600">Profit (25%)</span>
                <span className="font-medium text-gray-900">₹{costSummary.profit.toLocaleString()}</span>
              </div>

              <div className="pt-4 mt-4 border-t border-gray-100">
                <div className="flex justify-between items-center">
                  <span className="font-semibold text-gray-900">Total Price</span>
                  <span className="text-2xl font-bold text-indigo-600">
                    ₹{costSummary.totalCost.toLocaleString()}
                  </span>
                </div>
              </div>

              <div className="pt-6 space-y-3">
                <button
                  onClick={handleSave}
                  className="w-full py-3 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-xl transition-colors shadow-sm"
                >
                  {editItemId ? "Update Project Item" : "Save to Project"}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
"""

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(new_content)
print("Done")
