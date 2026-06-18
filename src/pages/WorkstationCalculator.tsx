import { useState, useMemo } from "react";
import {
  Calculator,
  LayoutGrid,
  Ruler,
  FileBox,
  IndianRupee,
  Download,
  FileSpreadsheet,
  X,
} from "lucide-react";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import * as XLSX from "xlsx";

const BOARDS = [
  { id: "plpb", name: "PLPB", costPerSqFt: 34 },
  { id: "mdf", name: "MDF", costPerSqFt: 60 },
  { id: "hdhmr", name: "HDHMR", costPerSqFt: 74 },
  { id: "ply_laminate", name: "PLY LAMINATE", costPerSqFt: 130 },
  { id: "hdhmr_laminate", name: "HDHMR LAMINATE", costPerSqFt: 130 },
];

const getTopRate = (boardId: string, baseRate: number, topThickness: number) => {
  if (boardId === "plpb") {
    if (topThickness === 25) return 63;
    if (topThickness === 36) return 98;
  }
  if (boardId === "hdhmr") {
    if (topThickness === 25) return 108;
  }
  if (boardId === "mdf") {
    if (topThickness === 17) return 55;
    if (topThickness === 18) return 60;
    if (topThickness === 25) return 80;
    if (topThickness === 35) return 112;
  }
  return baseRate * (topThickness / 18);
};

const LEGS = [
  { id: "board", name: "Board/Wooden Legs", cost: 0 }, // Cost derived from board material
  { id: "metal_loop", name: "Metal Loop Legs", cost: 1500 }, // per leg
  { id: "metal_c", name: "Metal C-Legs", cost: 1800 }, // per leg
  { id: "metal_leg", name: "Metal Leg", cost: 0 },
];

const SCREENS = [
  { id: "none", name: "None", costPerSqFt: 0 },
  { id: "board", name: "Board Partition", costPerSqFt: 0 }, // Cost derived from board material
  { id: "fabric", name: "Fabric Pinboard", costPerSqFt: 150 },
  { id: "glass", name: "Toughened Glass", costPerSqFt: 200 },
];

const WIRE_MANAGER_COST = 450; // Aluminum flap box
const GROMMET_COST = 100; // PVC grommet
const BRACKET_COST = 80; // Cost per screen bracket

const LABOR_COST = 200; // Making charges
const PACKING_COST = 100;
const TOOLING_COST = 100; // Fixed tolling cost
const PROFIT_PERCENTAGE = 0.25;

const LPATTI_COST = 10;
const LPATTI_QTY = 8;
const BUFFER_COST = 5;
const BUFFER_QTY = 4;

export function calculateWorkstationCost({
  width,
  depth,
  height,
  topThickness,
  boardId,
  legId,
  boardLegType,
  metalLegStyle,
  metalLegPipeSize,
  screenId,
  screenHeight,
  includeModesty,
  modestyType = "standard",
  wireManagement,
  includePedestal
}: any) {
  const board = BOARDS.find((b) => b.id === boardId)!;
  const legType = LEGS.find((l) => l.id === legId)!;
  const screenType = SCREENS.find((s) => s.id === screenId)!;

  // 1. Table Top Area
  const topAreaSqMm = width * depth;
    let topRate = getTopRate(board.id, board.costPerSqFt, topThickness);
    const topCost = (topAreaSqMm / 92903.04) * topRate;

  const bDetails = [
    {
      label: `Table Top (${width}x${depth}x${topThickness}mm)`,
      cost: Math.round(topCost),
    },
  ];

  let bCostTotal = topCost;

  // Edge Banding for Table Top
  let edgeBandingRate = 13;
  let edgeBandingThickness = "0.8mm";
  if (topThickness === 25) {
    edgeBandingRate = 28;
    edgeBandingThickness = "2mm";
  } else if (topThickness === 36) {
    edgeBandingRate = 48;
    edgeBandingThickness = "0.40mm"; // User mentioned .40 mm
  }

  const topPerimeterM = (width * 2 + depth * 2) / 1000;
  const edgeBandingCost = topPerimeterM * edgeBandingRate;
  bCostTotal += edgeBandingCost;
  bDetails.push({
    label: `Table Top Edge Banding (${edgeBandingThickness}, ${Math.round(topPerimeterM * 10) / 10}m)`,
    cost: Math.round(edgeBandingCost),
  });

  // 2. Legs / Understructure
  let hCost = 0;
  const hDetails: {
    label: string;
    cost: number;
    qty: number;
    unitPrice: number;
    unitLabel: string;
  }[] = [];

  if (legId === "board") {
    // 2 wooden side legs (gable ends)
    let legDepth = depth;
    if (boardLegType === "shorter") {
      if (depth === 600) legDepth = 400;
      else if (depth === 750) legDepth = 450;
      else if (depth === 900) legDepth = 600;
      else legDepth = Math.max(400, depth - 200);
    }
    
    const sideLegAreaSqMm = 2 * (legDepth * height);
    const legsCost = (sideLegAreaSqMm / 92903.04) * board.costPerSqFt;
    bCostTotal += legsCost;
    bDetails.push({
      label: `Board Side Legs (x2) - ${legDepth}D`,
      cost: Math.round(legsCost),
    });

    // Edge Banding for Legs (assumes standard 18mm board for legs with 0.8mm edge banding at 13/m)
    const legCount = 2;
    const legPerimeterM = (legCount * (legDepth * 2 + height * 2)) / 1000;
    const legEdgeBandingCost = legPerimeterM * 13;
    bCostTotal += legEdgeBandingCost;
    bDetails.push({
      label: `Legs Edge Banding (0.8mm, ${legPerimeterM.toFixed(3)}m)`,
      cost: Math.round(legEdgeBandingCost),
    });
  } else if (legId === "metal_leg") {
    // Pipe for vertical legs
    let verticalLengthMm = 4 * height;
    if (metalLegStyle === "u_shape") {
      verticalLengthMm += 2 * depth; // u-shape has bottom loops
    }
    const verticalFeet = verticalLengthMm / 304.8;
    const verticalRate = metalLegPipeSize === "50x50" ? 35 : 27;
    const costVerticals = verticalFeet * verticalRate;

    // 40x20 Pipe for horizontal supports
    const horizontalWidthMm = Math.max(0, width - 140);
    const horizontalDepthMm = Math.max(0, depth - 180);
    const horizontalLengthMm = 2 * horizontalWidthMm + 2 * horizontalDepthMm;
    const horizontalFeet = horizontalLengthMm / 304.8;
    
    const cost40x20 = horizontalFeet * 19.6; // 7kg * 56 Rs/kg / 20ft pipe = 19.6 Rs/rft
    
    const totalFeet = verticalFeet + horizontalFeet;
    const powderCoatingCost = totalFeet * 30;
    
    const numLegs = 4;
    const bufferCost = numLegs * 7;
    const nutCost = numLegs * 5;
    const butterflyCost = numLegs * 2 * 12.5;
    const accessoriesCost = bufferCost + nutCost + butterflyCost;
    
    hCost += costVerticals + cost40x20 + powderCoatingCost + accessoriesCost;
    
    hDetails.push({
      label: `Metal Legs ${metalLegPipeSize} (${metalLegStyle === 'u_shape' ? 'U-Shape' : 'Straight'})`,
      qty: Number(verticalFeet.toFixed(2)),
      unitPrice: verticalRate,
      unitLabel: "rft",
      cost: Math.round(costVerticals),
    });
    hDetails.push({
      label: `Metal Frame 40x20 (${horizontalWidthMm}W & ${horizontalDepthMm}D)`,
      qty: Number(horizontalFeet.toFixed(2)),
      unitPrice: 19.6,
      unitLabel: "rft",
      cost: Math.round(cost40x20),
    });
    hDetails.push({
      label: "Powder Coating",
      qty: Number(totalFeet.toFixed(2)),
      unitPrice: 30,
      unitLabel: "rft",
      cost: Math.round(powderCoatingCost),
    });
    hDetails.push({
      label: "Leg Accessories (Buffer, Nut, Butterfly)",
      qty: numLegs,
      unitPrice: 37, // 7 + 5 + (2 * 12.5)
      unitLabel: "leg set",
      cost: Math.round(accessoriesCost),
    });
  } else {
    // Other Metal legs
    const legCount = 2;
    const legTotalCost = legCount * legType.cost;
    hCost += legTotalCost;
    hDetails.push({
      label: legType.name,
      qty: legCount,
      unitPrice: legType.cost,
      unitLabel: "pcs",
      cost: legTotalCost,
    });
  }

  // 3. Modesty Panel
  let modCost = 0;
  if (includeModesty) {
    let modestyHeight = 750;
    if (legId === "board") {
      if (modestyType === "short") modestyHeight = 600;
      else if (modestyType === "shorter") modestyHeight = 300;
      else modestyHeight = 715; // standard
    }
    const modestyWidth = width - 18;
    const modestyAreaSqMm = modestyWidth * modestyHeight;
    modCost = (modestyAreaSqMm / 92903.04) * board.costPerSqFt;
    bCostTotal += modCost;
    bDetails.push({
      label: `Modesty Panel (${modestyWidth}x${modestyHeight})`,
      cost: Math.round(modCost),
    });

    // Modesty Edge Banding (1 bottom edge)
    const modestyEbLengthM = modestyWidth / 1000;
    const modestyEbCost = modestyEbLengthM * 13; // Uses standard 13/m rate
    bCostTotal += modestyEbCost;
    bDetails.push({
      label: `Modesty Edge Banding (0.8mm, ${modestyEbLengthM.toFixed(3)}m)`,
      cost: Math.round(modestyEbCost),
    });
  }

  // 4. Partition Screen
  let sCost = 0;
  if (screenId !== "none") {
    const sAreaSqFt = (width * screenHeight) / 92903.04;
    if (screenId === "board") {
      sCost = sAreaSqFt * board.costPerSqFt;
      bCostTotal += sCost;
      bDetails.push({ label: "Board Partition", cost: Math.round(sCost) });
    } else {
      sCost = sAreaSqFt * screenType.costPerSqFt;
    }

    // Hardware for screen
    const bracketCount = width > 1200 ? 3 : 2;
    const bracketTotal = bracketCount * BRACKET_COST;
    hCost += bracketTotal;
    hDetails.push({
      label: "Screen Brackets",
      qty: bracketCount,
      unitPrice: BRACKET_COST,
      unitLabel: "pcs",
      cost: bracketTotal,
    });
  }

  // 5. Wire Management
  if (wireManagement === "raceway") {
    hCost += WIRE_MANAGER_COST;
    hDetails.push({
      label: "Alu Flap Raceway",
      qty: 1,
      unitPrice: WIRE_MANAGER_COST,
      unitLabel: "Set",
      cost: WIRE_MANAGER_COST,
    });
  } else if (wireManagement === "grommet") {
    const grommetCount = 2;
    const gCost = grommetCount * GROMMET_COST;
    hCost += gCost;
    hDetails.push({
      label: "PVC Grommet",
      qty: grommetCount,
      unitPrice: GROMMET_COST,
      unitLabel: "pcs",
      cost: gCost,
    });
  }

  // 6. Fixed Pedestal (Standard approx material + hardware)
  // Here we just add a flat estimated rate for a pedestal if selected.
  if (includePedestal) {
    const pedEstimatedCost = 3500;
    hCost += pedEstimatedCost;
    hDetails.push({
      label: "3-Drawer Pedestal (Fixed)",
      qty: 1,
      unitPrice: pedEstimatedCost,
      unitLabel: "unit",
      cost: pedEstimatedCost,
    });
  }

  // Add Fixed Hardware (Patti & Buffer)
  if (legId !== "metal_leg") {
    const pattiTotal = LPATTI_QTY * LPATTI_COST;
    hCost += pattiTotal;
    hDetails.push({
      label: "L Patti",
      qty: LPATTI_QTY,
      unitPrice: LPATTI_COST,
      unitLabel: "pcs",
      cost: pattiTotal,
    });

    const bufferTotal = BUFFER_QTY * BUFFER_COST;
    hCost += bufferTotal;
    hDetails.push({
      label: "Buffer",
      qty: BUFFER_QTY,
      unitPrice: BUFFER_COST,
      unitLabel: "pcs",
      cost: bufferTotal,
    });
  }

  const tSqFt = (bCostTotal / board.costPerSqFt).toFixed(2);
  const waste = Math.round(bCostTotal * 0.15);

  const lCost = LABOR_COST;
  const pCost = PACKING_COST;

  // Total raw + labor
  const directCost =
    bCostTotal +
    waste +
    hCost +
    (screenId !== "board" ? sCost : 0) +
    lCost +
    pCost;

  const tCost = TOOLING_COST;
  const subTotal = directCost + tCost;
  const prof = Math.round(subTotal * PROFIT_PERCENTAGE);

  const total = subTotal + prof;

  return {
    boardCostTotal: Math.round(bCostTotal),
    boardDetails: bDetails,
    hardwareCost: hCost,
    hardwareDetails: hDetails,
    screenCostResult: Math.round(sCost),
    modestyCost: Math.round(modCost),
    wasteCost: waste,
    laborCost: lCost,
    packingCost: pCost,
    toolingCost: tCost,
    profit: prof,
    totalCost: Math.round(total),
    totalSqFt: Number(tSqFt),
  };
}

export default function WorkstationCalculator() {
  const [isCustomSize, setIsCustomSize] = useState<boolean>(false);
  const [width, setWidth] = useState<number>(900); // mm
  const [depth, setDepth] = useState<number>(600); // mm
  const [height, setHeight] = useState<number>(750); // mm
  const [topThickness, setTopThickness] = useState<number>(18); // mm

  const [boardId, setBoardId] = useState<string>("plpb");
  const [legId, setLegId] = useState<string>("board");
  const [boardLegType, setBoardLegType] = useState<string>("full"); // 'full', 'shorter'
  const [metalLegStyle, setMetalLegStyle] = useState<string>("straight"); // 'straight', 'u_shape'
  const [metalLegPipeSize, setMetalLegPipeSize] = useState<string>("40x40"); // '40x40', '50x50'
  const [screenId, setScreenId] = useState<string>("none");

  const [screenHeight, setScreenHeight] = useState<number>(300); // above desk height mm
  const [includeModesty, setIncludeModesty] = useState<boolean>(true);
  const [modestyType, setModestyType] = useState<string>("standard"); // 'standard', 'short', 'shorter'
  const [wireManagement, setWireManagement] = useState<string>("raceway"); // 'grommet', 'raceway', 'none'
  const [includePedestal, setIncludePedestal] = useState<boolean>(false);

  const [showExportModal, setShowExportModal] = useState(false);
  const [exportIncludeModesty, setExportIncludeModesty] = useState(true);
  const [exportModestyType, setExportModestyType] = useState<string>("standard");
  const [exportIncludePedestal, setExportIncludePedestal] = useState(false);
  const [exportWireManagement, setExportWireManagement] = useState<string>("none");
  const [exportThickness, setExportThickness] = useState<string>("all");
  const [exportMaterial, setExportMaterial] = useState<string>("all");
  const [exportLegId, setExportLegId] = useState<string>("board");
  const [exportBoardLegType, setExportBoardLegType] = useState<string>("full");

  const {
    boardCostTotal,
    boardDetails,
    hardwareCost,
    hardwareDetails,
    screenCostResult,
    modestyCost,
    wasteCost,
    laborCost,
    packingCost,
    toolingCost,
    profit,
    totalCost,
    totalSqFt,
  } = useMemo(() => {
    return calculateWorkstationCost({
      width,
      depth,
      height,
      topThickness,
      boardId,
      legId,
      boardLegType,
      metalLegStyle,
      metalLegPipeSize,
      screenId,
      screenHeight,
      includeModesty,
      modestyType,
      wireManagement,
      includePedestal
    });
  }, [
    width,
    height,
    depth,
    topThickness,
    boardId,
    legId,
    boardLegType,
    metalLegStyle,
    metalLegPipeSize,
    screenId,
    screenHeight,
    includeModesty,
    modestyType,
    wireManagement,
    includePedestal,
  ]);

  const downloadPDF = () => {
    const doc = new jsPDF();
    const board = BOARDS.find((b) => b.id === boardId)!;
    const legType = LEGS.find((l) => l.id === legId)!;
    const screenType = SCREENS.find((s) => s.id === screenId)!;

    doc.setFontSize(20);
    doc.text("Table Cost Estimation Report", 14, 22);

    doc.setFontSize(12);
    doc.text(`Date: ${new Date().toLocaleDateString()}`, 14, 32);

    autoTable(doc, {
      startY: 40,
      head: [["Specification", "Details"]],
      body: [
        ["Dimensions (W x H x D)", `${width} mm x ${height} mm x ${depth} mm`],
        ["Table Top Thickness", `${topThickness} mm`],
        ["Board Material", `${board.name} (Rs. ${getTopRate(board.id, board.costPerSqFt, topThickness)}/sq.ft)`],
        ["Understructure", legType.name],
        ["Modesty Panel", includeModesty ? "Included" : "None"],
        [
          "Screen Partition",
          screenId !== "none"
            ? `${screenType.name} (${screenHeight}mm H)`
            : "None",
        ],
        ["Wire Management", wireManagement.toUpperCase()],
      ],
      theme: "grid",
      headStyles: { fillColor: [79, 70, 229] },
    });

    const bdBody = boardDetails.map((b) => [
      b.label,
      `Rs. ${b.cost.toLocaleString()}`,
    ]);

    autoTable(doc, {
      startY: (doc as any).lastAutoTable.finalY + 10,
      head: [["Detailed Board Cost", "Amount"]],
      body: bdBody,
      theme: "grid",
      headStyles: { fillColor: [79, 70, 229] },
    });

    const hardwareBody = hardwareDetails.map((h) => [
      `${h.label} (Qty: ${h.qty} ${h.unitLabel} @ Rs. ${h.unitPrice})`,
      `Rs. ${Math.round(h.cost).toLocaleString()}`,
    ]);

    autoTable(doc, {
      startY: (doc as any).lastAutoTable.finalY + 10,
      head: [["Hardware & Accessories Included", "Cost"]],
      body:
        hardwareBody.length > 0
          ? hardwareBody
          : [["No hardware selected", "-"]],
      theme: "grid",
      headStyles: { fillColor: [79, 70, 229] },
    });

    const costStartY = (doc as any).lastAutoTable.finalY + 10;
    const bodyArgs: string[][] = [
      ["Total Board Cost", `Rs. ${boardCostTotal.toLocaleString()}`],
    ];

    if (screenId !== "none" && screenId !== "board") {
      bodyArgs.push([
        `Screen (${screenType.name})`,
        `Rs. ${screenCostResult.toLocaleString()}`,
      ]);
    }

    bodyArgs.push([
      "Material Waste (15%)",
      `Rs. ${wasteCost.toLocaleString()}`,
    ]);
    bodyArgs.push([
      "Hardware & Accessories",
      `Rs. ${Math.round(hardwareCost).toLocaleString()}`,
    ]);
    bodyArgs.push(["Labor & Making", `Rs. ${laborCost.toLocaleString()}`]);
    bodyArgs.push(["Packing", `Rs. ${packingCost.toLocaleString()}`]);
    bodyArgs.push(["Tooling", `Rs. ${toolingCost.toLocaleString()}`]);
    bodyArgs.push(["Profit (25%)", `Rs. ${profit.toLocaleString()}`]);

    autoTable(doc, {
      startY: costStartY,
      head: [["Overall Cost Summary", "Amount"]],
      body: bodyArgs,
      theme: "grid",
      headStyles: { fillColor: [79, 70, 229] },
    });

    const totalStartY = (doc as any).lastAutoTable.finalY + 10;
    autoTable(doc, {
      startY: totalStartY,
      head: [["Total Estimated Cost", `Rs. ${totalCost.toLocaleString()}`]],
      theme: "grid",
      headStyles: { fillColor: [17, 24, 39] },
    });

    doc.save("table-cost-report.pdf");
  };

  const downloadMasterPriceList = () => {
    const wb = XLSX.utils.book_new();

    const masterData: any[][] = [];
    masterData.push([
      "Board Material",
      "Dimensions (WxDxH mm)",
      "Top Thickness",
      "Understructure",
      "Cost Price (Rs)",
    ]);

    const widths = [900, 1050, 1200, 1350, 1500];
    const depths = [400, 600, 750, 900, 1100];
    const thicknesses = exportThickness === "all" ? [17, 18, 25, 35, 36] : [Number(exportThickness)];
    const boardsToExport = exportMaterial === "all" ? BOARDS : BOARDS.filter(b => b.id === exportMaterial);
    const exportLegName = LEGS.find(l => l.id === exportLegId)?.name || 'Board Leg';
    const exportLeg = exportLegId === "board" ? `${exportLegName} (${exportBoardLegType === "shorter" ? "Shorter" : "Full Depth"})` : exportLegName;

    // Build the master data
    for (const board of boardsToExport) {
      for (const w of widths) {
        for (const d of depths) {
          for (const t of thicknesses) {
            const res = calculateWorkstationCost({
              width: w,
              depth: d,
              height: 750,
              topThickness: t,
              boardId: board.id,
              legId: exportLegId,
              boardLegType: exportBoardLegType,
              metalLegStyle: "straight",
              metalLegPipeSize: "40x40",
              screenId: "none",
              screenHeight: 300,
              includeModesty: exportIncludeModesty,
              modestyType: exportModestyType,
              wireManagement: exportWireManagement,
              includePedestal: exportIncludePedestal
            });

            masterData.push([
              board.name,
              `${w}x${d}x${750}`,
              `${t}mm`,
              exportLeg,
              res.totalCost,
            ]);
          }
        }
      }
    }

    const wsMaster = XLSX.utils.aoa_to_sheet(masterData);
    const colWidths = [{ wch: 15 }, { wch: 20 }, { wch: 15 }, { wch: 20 }, { wch: 15 }];
    wsMaster["!cols"] = colWidths;

    XLSX.utils.book_append_sheet(wb, wsMaster, "Master Price List");
    XLSX.writeFile(wb, "table-master-price-list.xlsx");
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex items-center gap-3">
        <div className="p-3 bg-indigo-100 text-indigo-600 rounded-xl">
          <Calculator className="w-6 h-6" />
        </div>
        <div>
          <h1 className="text-3xl font-semibold tracking-tight text-gray-900">
            Table Calculator
          </h1>
          <p className="text-gray-500 flex items-center gap-2 mt-1">
            Calculate manufacturing costs for linear tables.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-12 gap-8">
        <div className="xl:col-span-8 space-y-6">
          {/* Dimensions Section */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200">
            <h2 className="text-lg font-medium text-gray-900 flex justify-between items-center gap-2 mb-4">
              <div className="flex items-center gap-2">
                <Ruler className="w-5 h-5 text-gray-400" />
                Dimensions (mm)
              </div>
              <label className="flex items-center gap-2 text-sm text-gray-600 font-normal cursor-pointer">
                <input
                  type="checkbox"
                  checked={isCustomSize}
                  onChange={(e) => setIsCustomSize(e.target.checked)}
                  className="w-4 h-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                />
                Custom Sizes
              </label>
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Width (L)
                </label>
                {isCustomSize ? (
                  <input
                    type="number"
                    value={width}
                    onChange={(e) => setWidth(Number(e.target.value))}
                    min={0}
                    className="block w-full px-4 py-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none text-gray-900"
                  />
                ) : (
                  <select
                    value={width}
                    onChange={(e) => setWidth(Number(e.target.value))}
                    className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none text-gray-900"
                  >
                    <option value={900}>900 mm</option>
                    <option value={1050}>1050 mm</option>
                    <option value={1200}>1200 mm</option>
                    <option value={1350}>1350 mm</option>
                    <option value={1500}>1500 mm</option>
                  </select>
                )}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Depth (D)
                </label>
                {isCustomSize ? (
                  <input
                    type="number"
                    value={depth}
                    onChange={(e) => setDepth(Number(e.target.value))}
                    min={0}
                    className="block w-full px-4 py-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none text-gray-900"
                  />
                ) : (
                  <select
                    value={depth}
                    onChange={(e) => setDepth(Number(e.target.value))}
                    className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none text-gray-900"
                  >
                    <option value={400}>400 mm</option>
                    <option value={600}>600 mm</option>
                    <option value={750}>750 mm</option>
                    <option value={900}>900 mm</option>
                    <option value={1100}>1100 mm</option>
                  </select>
                )}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Height (H)
                </label>
                {isCustomSize ? (
                  <input
                    type="number"
                    value={height}
                    onChange={(e) => setHeight(Number(e.target.value))}
                    min={0}
                    className="block w-full px-4 py-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none text-gray-900"
                  />
                ) : (
                  <select
                    value={height}
                    onChange={(e) => setHeight(Number(e.target.value))}
                    className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none text-gray-900"
                  >
                    <option value={750}>750 mm</option>
                  </select>
                )}</div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Top Thickness
                </label>
                <select
                  value={topThickness}
                  onChange={(e) => setTopThickness(Number(e.target.value))}
                  className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none text-gray-900"
                >
                  <option value={17}>17 mm</option>
                  <option value={18}>18 mm</option>
                  <option value={25}>25 mm</option>
                  <option value={35}>35 mm</option>
                  <option value={36}>36 mm</option>
                </select>
              </div>
            </div>
          </div>

          {/* Configurations Section */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200">
            <h2 className="text-lg font-medium text-gray-900 flex items-center gap-2 mb-4">
              <LayoutGrid className="w-5 h-5 text-gray-400" />
              Configuration
            </h2>
            <div className="space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Board Material
                  </label>
                  <select
                    value={boardId}
                    onChange={(e) => setBoardId(e.target.value)}
                    className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                  >
                    {BOARDS.map((b) => (
                      <option key={b.id} value={b.id}>
                        {b.name} (₹{getTopRate(b.id, b.costPerSqFt, topThickness)}/sq.ft)
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Understructure (Legs)
                  </label>
                  <select
                    value={legId}
                    onChange={(e) => setLegId(e.target.value)}
                    className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                  >
                    {LEGS.map((l) => (
                      <option key={l.id} value={l.id}>
                        {l.name}
                      </option>
                    ))}
                  </select>
                </div>
                {legId === "board" && (
                  <div className="sm:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Board Leg Type
                    </label>
                    <select
                      value={boardLegType}
                      onChange={(e) => setBoardLegType(e.target.value)}
                      className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                    >
                      <option value="full">Full Legs</option>
                      <option value="shorter">Shorter Legs</option>
                    </select>
                  </div>
                )}
                {legId === "metal_leg" && (
                  <>
                    <div className="sm:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Metal Pipe Size
                      </label>
                      <select
                        value={metalLegPipeSize}
                        onChange={(e) => setMetalLegPipeSize(e.target.value)}
                        className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                      >
                        <option value="40x40">40x40 mm</option>
                        <option value="50x50">50x50 mm</option>
                      </select>
                    </div>
                    <div className="sm:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Style of Leg
                      </label>
                      <select
                        value={metalLegStyle}
                        onChange={(e) => setMetalLegStyle(e.target.value)}
                        className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                      >
                        <option value="straight">Straight Leg</option>
                        <option value="u_shape">U-Shape Leg</option>
                      </select>
                    </div>
                  </>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Partition Screen
                </label>
                <div className="flex gap-4 items-center">
                  <select
                    value={screenId}
                    onChange={(e) => setScreenId(e.target.value)}
                    className="block w-1/2 px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all"
                  >
                    {SCREENS.map((s) => (
                      <option key={s.id} value={s.id}>
                        {s.name}
                      </option>
                    ))}
                  </select>
                  {screenId !== "none" && (
                    <select
                      value={screenHeight}
                      onChange={(e) => setScreenHeight(Number(e.target.value))}
                      className="block w-1/2 px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all"
                    >
                      <option value={300}>300 mm High</option>
                      <option value={400}>400 mm High</option>
                      <option value={450}>450 mm High</option>
                    </select>
                  )}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Wire Management
                </label>
                <select
                  value={wireManagement}
                  onChange={(e) => setWireManagement(e.target.value)}
                  className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all"
                >
                  <option value="none">None</option>
                  <option value="grommet">
                    PVC Grommets (x2 for ₹{GROMMET_COST * 2})
                  </option>
                  <option value="raceway">
                    Aluminum Flap Box (₹{WIRE_MANAGER_COST})
                  </option>
                </select>
              </div>

              <div className="pt-4 border-t border-gray-100">
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Add-ons
                </label>
                <div className="flex flex-col gap-3">
                  <div className="flex flex-col gap-2">
                    <label className="flex items-center gap-3 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={includeModesty}
                        onChange={(e) => setIncludeModesty(e.target.checked)}
                        className="w-5 h-5 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500 transition-colors"
                      />
                      <div>
                        <span className="text-sm font-medium text-gray-900 block">
                          Modesty Panel
                        </span>
                        <span className="text-xs text-gray-500">
                          Board panel below desk
                        </span>
                      </div>
                    </label>

                    {includeModesty && legId === "board" && (
                      <div className="ml-8 mt-1">
                        <select
                          value={modestyType}
                          onChange={(e) => setModestyType(e.target.value)}
                          className="block w-full max-w-xs px-3 py-1.5 bg-gray-50 border border-gray-200 rounded-md text-sm outline-none focus:ring-2 focus:ring-indigo-500"
                        >
                          <option value="standard">Standard (715 mm)</option>
                          <option value="short">Short (600 mm)</option>
                          <option value="shorter">Shorter (300 mm)</option>
                        </select>
                      </div>
                    )}
                  </div>

                  <label className="flex items-center gap-3 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={includePedestal}
                      onChange={(e) => setIncludePedestal(e.target.checked)}
                      className="w-5 h-5 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500 transition-colors"
                    />
                    <div>
                      <span className="text-sm font-medium text-gray-900 block">
                        Attached Pedestal (Fixed Cost)
                      </span>
                      <span className="text-xs text-gray-500">
                        Adds an estimated ₹3,500 standard pedestal cost.
                      </span>
                    </div>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Cost Summary Sidebar */}
        <div className="xl:col-span-4">
          <div className="sticky top-24 bg-gray-900 rounded-2xl p-6 text-white overflow-hidden relative">
            <div className="absolute top-0 right-0 -mr-12 -mt-12 w-48 h-48 bg-indigo-500 rounded-full opacity-10 blur-3xl mix-blend-screen pointer-events-none"></div>

            <h2 className="text-lg font-medium text-gray-100 flex items-center gap-2 mb-6">
              <FileBox className="w-5 h-5 text-indigo-400" />
              Estimation
            </h2>

            <div className="space-y-4 mb-6 relative z-10">
              <div className="flex flex-col mb-1 border-gray-800/50">
                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-400">Total Board Cost</span>
                  <span className="font-medium">
                    ₹{boardCostTotal.toLocaleString()}
                  </span>
                </div>
                <div className="mt-2 space-y-1.5 border-l border-gray-700 ml-1 pl-2">
                  {boardDetails.map((item, idx) => (
                    <div
                      key={idx}
                      className="flex justify-between items-center text-xs text-gray-500"
                    >
                      <span>{item.label}</span>
                      <span>₹{item.cost.toLocaleString()}</span>
                    </div>
                  ))}
                </div>
              </div>

              {screenId !== "none" && screenId !== "board" && (
                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-400">Screen/Partition Cost</span>
                  <span className="font-medium">
                    ₹{screenCostResult.toLocaleString()}
                  </span>
                </div>
              )}

              <div className="flex justify-between items-center text-sm">
                <span className="text-gray-400">Material Waste (15%)</span>
                <span className="font-medium">
                  ₹{wasteCost.toLocaleString()}
                </span>
              </div>
              <div className="flex flex-col mb-1 pt-2 border-t border-gray-800/50">
                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-400">Hardware & Fittings</span>
                  <span className="font-medium text-gray-100">
                    ₹{Math.round(hardwareCost).toLocaleString()}
                  </span>
                </div>
                <div className="mt-2 space-y-1.5 border-l border-gray-700 ml-1 pl-2">
                  {hardwareDetails.map((item, idx) => (
                    <div
                      key={idx}
                      className="flex justify-between items-start text-xs text-gray-500"
                    >
                      <span className="pr-2 leading-relaxed">
                        {item.label}{" "}
                        <span className="text-gray-600">(x{item.qty})</span>
                      </span>
                      <span className="whitespace-nowrap mt-[1px]">
                        ₹{Math.round(item.cost).toLocaleString()}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
              <div className="flex justify-between items-center text-sm pt-2 border-t border-gray-800/50">
                <span className="text-gray-400">Labor & Making</span>
                <span className="font-medium">
                  ₹{laborCost.toLocaleString()}
                </span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-gray-400">Packing</span>
                <span className="font-medium">
                  ₹{packingCost.toLocaleString()}
                </span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-gray-400">Tooling</span>
                <span className="font-medium">
                  ₹{toolingCost.toLocaleString()}
                </span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-gray-400">Profit (25%)</span>
                <span className="font-medium">₹{profit.toLocaleString()}</span>
              </div>
            </div>

            <div className="pt-4 border-t border-gray-800 relative z-10">
              <span className="text-sm text-gray-400 block mb-1">
                Estimated Total Cost
              </span>
              <div className="flex items-center text-3xl font-semibold text-white tracking-tight">
                <IndianRupee className="w-6 h-6 mr-1" />
                {totalCost.toLocaleString()}
              </div>
              <p className="text-xs text-indigo-300 mt-3 opacity-80 mb-6">
                Approximation based on {totalSqFt} sq.ft board volume.
              </p>

              <button
                onClick={downloadPDF}
                className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white py-2.5 px-4 rounded-lg font-medium transition-colors mb-3"
              >
                <Download className="w-4 h-4" />
                Download PDF Report
              </button>

              <button
                onClick={() => setShowExportModal(true)}
                className="w-full flex items-center justify-center gap-2 bg-slate-800 hover:bg-slate-900 text-white py-2.5 px-4 rounded-lg font-medium transition-colors"
              >
                <FileSpreadsheet className="w-4 h-4 text-emerald-400" />
                Export Master Price List
              </button>
            </div>
          </div>
        </div>
      </div>

      {showExportModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl p-6 max-w-sm w-full shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium">Export Options</h3>
              <button
                onClick={() => setShowExportModal(false)}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <X className="w-5 h-5 text-gray-500" />
              </button>
            </div>
            
            <div className="space-y-4 mb-6">
              <div className="flex flex-col gap-2 p-3 border rounded-lg hover:bg-gray-50">
                <label className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={exportIncludeModesty}
                    onChange={(e) => setExportIncludeModesty(e.target.checked)}
                    className="w-4 h-4 text-indigo-600 rounded border-gray-300"
                  />
                  <span className="text-sm font-medium">Include Modesty Panel</span>
                </label>
                {exportIncludeModesty && (
                  <select
                    value={exportModestyType}
                    onChange={(e) => setExportModestyType(e.target.value)}
                    className="block w-full ml-7 px-3 py-1.5 bg-gray-50 border border-gray-200 rounded-md text-sm outline-none w-auto self-start"
                  >
                    <option value="standard">Standard (715 mm)</option>
                    <option value="short">Short (600 mm)</option>
                    <option value="shorter">Shorter (300 mm)</option>
                  </select>
                )}
              </div>

              <label className="flex items-center gap-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                <input
                  type="checkbox"
                  checked={exportIncludePedestal}
                  onChange={(e) => setExportIncludePedestal(e.target.checked)}
                  className="w-4 h-4 text-indigo-600 rounded border-gray-300"
                />
                <span className="text-sm font-medium">Include Fixed Pedestal</span>
              </label>

              <div className="space-y-2 p-3 border rounded-lg">
                <label className="text-sm font-medium text-gray-900">Wire Management</label>
                <select
                  value={exportWireManagement}
                  onChange={(e) => setExportWireManagement(e.target.value)}
                  className="block w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-md text-sm outline-none"
                >
                  <option value="none">None</option>
                  <option value="grommet">PVC Grommets</option>
                  <option value="raceway">Alu Flap Raceway</option>
                </select>
              </div>

              <div className="space-y-2 p-3 border rounded-lg">
                <label className="text-sm font-medium text-gray-900">Top Thickness</label>
                <select
                  value={exportThickness}
                  onChange={(e) => setExportThickness(e.target.value)}
                  className="block w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-md text-sm outline-none"
                >
                  <option value="all">All (17mm, 18mm, 25mm, 35mm, 36mm)</option>
                  <option value="17">17 mm</option>
                  <option value="18">18 mm</option>
                  <option value="25">25 mm</option>
                  <option value="35">35 mm</option>
                  <option value="36">36 mm</option>
                </select>
              </div>

              <div className="space-y-2 p-3 border rounded-lg">
                <label className="text-sm font-medium text-gray-900">Understructure (Legs)</label>
                <select
                  value={exportLegId}
                  onChange={(e) => setExportLegId(e.target.value)}
                  className="block w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-md text-sm outline-none"
                >
                  {LEGS.map((l) => (
                    <option key={l.id} value={l.id}>
                      {l.name}
                    </option>
                  ))}
                </select>

                {exportLegId === "board" && (
                  <div className="pt-2 border-t mt-2">
                    <label className="text-xs font-medium text-gray-700 block mb-1">
                      Board Leg Type
                    </label>
                    <select
                      value={exportBoardLegType}
                      onChange={(e) => setExportBoardLegType(e.target.value)}
                      className="block w-full px-3 py-2 bg-white border border-gray-200 rounded-md text-sm outline-none"
                    >
                      <option value="full">Full Depth</option>
                      <option value="shorter">Shorter (Minus 200mm)</option>
                    </select>
                  </div>
                )}
              </div>

              <div className="space-y-2 p-3 border rounded-lg">
                <label className="text-sm font-medium text-gray-900">Board Material</label>
                <select
                  value={exportMaterial}
                  onChange={(e) => setExportMaterial(e.target.value)}
                  className="block w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-md text-sm outline-none"
                >
                  <option value="all">All Materials</option>
                  {BOARDS.map(b => (
                    <option key={b.id} value={b.id}>{b.name}</option>
                  ))}
                </select>
              </div>
            </div>

            <button
              onClick={() => {
                downloadMasterPriceList();
                setShowExportModal(false);
              }}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-2.5 rounded-lg font-medium transition-colors"
            >
              Generate & Download Excel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
