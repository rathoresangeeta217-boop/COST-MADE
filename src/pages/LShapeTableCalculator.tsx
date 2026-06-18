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
  { id: "board", name: "Board/Wooden Legs", cost: 0 },
  { id: "metal_loop", name: "Metal Loop Legs", cost: 1500 },
  { id: "metal_c", name: "Metal C-Legs", cost: 1800 },
  { id: "metal_leg", name: "Metal Leg", cost: 0 },
];

const WIRE_MANAGER_COST = 450;
const GROMMET_COST = 100;

const LABOR_COST = 200; // Higher making charges for L-Shape
const PACKING_COST = 100;
const TOOLING_COST = 100;
const PROFIT_PERCENTAGE = 0.25;

const LPATTI_COST = 10;
const LPATTI_QTY = 8;
const BUFFER_COST = 5;
const BUFFER_QTY = 4;

export function calculateLShapeCost({
  mainWidth,
  mainDepth,
  returnWidth,
  returnDepth,
  height,
  returnHeight,
  topThickness,
  boardId,
  legId,
  boardLegType,
  metalLegStyle,
  metalLegPipeSize,
  includeModesty,
  modestyType = "standard",
  wireManagement,
  includePedestal,
  includeReturnStorage
}: any) {
  const board = BOARDS.find((b) => b.id === boardId)!;
  const legType = LEGS.find((l) => l.id === legId)!;

  // 1. Table Top Area (Main + Return overlapping adjustment)
  // Assume L-shape is joined, so the return width includes or excludes the main desk depth.
  // For simplicity, we calculate total area as (Main W * Main D) + (Return W * Return D)
  const mainTopAreaSqMm = mainWidth * mainDepth;
  const returnTopAreaSqMm = includeReturnStorage
    ? returnWidth * returnDepth
    : 0;

  let topRate = getTopRate(board.id, board.costPerSqFt, topThickness);
  const topCost =
    ((mainTopAreaSqMm + returnTopAreaSqMm) / 92903.04) * topRate;

  const bDetails = [
    {
      label: `Main Table Top (${mainWidth}x${mainDepth}x${topThickness}mm)`,
      cost: Math.round((mainTopAreaSqMm / 92903.04) * topRate),
    },
  ];

  if (includeReturnStorage) {
    bDetails.push({
      label: `Return Storage Top (${returnWidth}x${returnDepth}x${topThickness}mm)`,
      cost: Math.round((returnTopAreaSqMm / 92903.04) * topRate),
    });
  }

  let bCostTotal = topCost;

  // Edge Banding for Table Tops
  let edgeBandingRate = 13;
  let edgeBandingThickness = "0.8mm";
  if (topThickness === 25) {
    edgeBandingRate = 28;
    edgeBandingThickness = "2mm";
  } else if (topThickness === 36) {
    edgeBandingRate = 48;
    edgeBandingThickness = "0.40mm"; // User mentioned .40 mm
  }

  let topPerimeterM = (mainWidth * 2 + mainDepth * 2) / 1000;
  if (includeReturnStorage) {
    topPerimeterM += (returnWidth * 2 + returnDepth * 2) / 1000;
    // Subtract the overlap joint length (times 2 because both edges are joined)
    topPerimeterM -= (2 * Math.min(mainDepth, returnDepth)) / 1000;
  }

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
    // 3 wooden legs for an L-Shape table typically, 2 if no return
    const legCount = includeReturnStorage ? 3 : 2;
    
    let mainLegDepth = mainDepth;
    let retLegDepth = returnDepth;
    if (boardLegType === "shorter") {
      if (mainDepth === 600) mainLegDepth = 400;
      else if (mainDepth === 750) mainLegDepth = 450;
      else if (mainDepth === 900) mainLegDepth = 600;
      else mainLegDepth = Math.max(400, mainDepth - 200);

      if (returnDepth === 600) retLegDepth = 400;
      else if (returnDepth === 750) retLegDepth = 450;
      else if (returnDepth === 900) retLegDepth = 600;
      else retLegDepth = Math.max(400, returnDepth - 200);
    }
    
    const effectiveDepth = includeReturnStorage
      ? Math.max(mainLegDepth, retLegDepth)
      : mainLegDepth;
    const legAreaSqMm = legCount * (effectiveDepth * height);
    const legsCost = (legAreaSqMm / 92903.04) * board.costPerSqFt;
    bCostTotal += legsCost;
    bDetails.push({
      label: `Board Understructure Legs (x${legCount}) - ${effectiveDepth}D`,
      cost: Math.round(legsCost),
    });

    // Edge Banding for Legs (assumes standard 18mm board for legs with 0.8mm edge banding at 13/m)
    const legPerimeterM =
      (legCount * (effectiveDepth * 2 + height * 2)) / 1000;
    const legEdgeBandingCost = legPerimeterM * 13;
    bCostTotal += legEdgeBandingCost;
    bDetails.push({
      label: `Legs Edge Banding (0.8mm, ${legPerimeterM.toFixed(3)}m)`,
      cost: Math.round(legEdgeBandingCost),
    });
  } else if (legId === "metal_leg") {
    // Pipe for vertical legs
    let verticalsMm = includeReturnStorage ? 6 * Math.max(height, returnHeight) : 4 * height;
    if (metalLegStyle === "u_shape") {
        verticalsMm += (includeReturnStorage ? 2 * mainDepth + returnDepth : 2 * mainDepth);
    }
    const verticalFeet = verticalsMm / 304.8;
    const verticalRate = metalLegPipeSize === "50x50" ? 35 : 27;
    const costVerticals = verticalFeet * verticalRate;

    // 40x20 Pipe for horizontal supports
    const mainWidthPipe = Math.max(0, mainWidth - 140);
    const mainDepthPipe = Math.max(0, mainDepth - 180);
    const returnWidthPipe = Math.max(0, returnWidth - 140);
    
    const horizontalsMm = includeReturnStorage 
      ? 2 * mainWidthPipe + 2 * mainDepthPipe + 2 * returnWidthPipe 
      : 2 * mainWidthPipe + 2 * mainDepthPipe;
      
    const horizontalFeet = horizontalsMm / 304.8;
    const cost40x20 = horizontalFeet * 19.6; // 7kg * 56 Rs/kg / 20ft pipe = 19.6 Rs/rft
    
    const totalFeet = verticalFeet + horizontalFeet;
    const powderCoatingCost = totalFeet * 30;
    
    const numLegs = includeReturnStorage ? 6 : 4;
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
      label: `Metal Frame 40x20 Pipes`,
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
    // Metal legs for L-Shape (usually 3 or more depending on structure, 2 if no return)
    const legCount = includeReturnStorage ? 3 : 2;
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
    // Modesty panel for both main and return
    let modestyHeight = 750;
    if (legId === "board") {
      if (modestyType === "short") modestyHeight = 600;
      else if (modestyType === "shorter") modestyHeight = 300;
      else modestyHeight = 715; // standard
    }
    const mainModestyWidth = mainWidth - 18;
    const returnModestyWidth = includeReturnStorage ? returnWidth - 18 : 0;
    const modestyAreaSqMm =
      (mainModestyWidth + returnModestyWidth) * modestyHeight;
    modCost = (modestyAreaSqMm / 92903.04) * board.costPerSqFt;
    bCostTotal += modCost;
    bDetails.push({
      label: includeReturnStorage
        ? `All Table Modesty Panels (${mainModestyWidth}x${modestyHeight}, ${returnModestyWidth}x${modestyHeight})`
        : `Main Modesty Panel (${mainModestyWidth}x${modestyHeight})`,
      cost: Math.round(modCost),
    });

    // Modesty Edge Banding (1 bottom edge per panel)
    const modestyEbLengthM = (mainModestyWidth + returnModestyWidth) / 1000;
    const modestyEbCost = modestyEbLengthM * 13;
    bCostTotal += modestyEbCost;
    bDetails.push({
      label: `Modesty Edge Banding (0.8mm, ${modestyEbLengthM.toFixed(3)}m)`,
      cost: Math.round(modestyEbCost),
    });
  }

  // 4. Wire Management
  if (wireManagement === "raceway") {
    const racewayCost = WIRE_MANAGER_COST * 2; // Need 2 for L-shape typically
    hCost += racewayCost;
    hDetails.push({
      label: "Alu Flap Raceway",
      qty: 2,
      unitPrice: WIRE_MANAGER_COST,
      unitLabel: "Set",
      cost: racewayCost,
    });
  } else if (wireManagement === "grommet") {
    const grommetCount = 3; // L shape often needs more grommets
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

  // 5. Fixed/Movable Pedestal
  if (includePedestal) {
    const pedEstimatedCost = 4200; // slightly higher estimate
    hCost += pedEstimatedCost;
    hDetails.push({
      label: "3-Drawer Pedestal Unit",
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

  const mainWidthExtraSteps = Math.max(
    0,
    Math.floor((mainWidth - 900) / 150),
  );
  const mainDepthExtraSteps = Math.max(
    0,
    Math.floor((mainDepth - 600) / 150),
  );
  const dimensionExtra = (mainWidthExtraSteps + mainDepthExtraSteps) * 50;

  const lCost = LABOR_COST + dimensionExtra;
  const pCost = PACKING_COST + dimensionExtra;

  // Total raw + labor
  const directCost = bCostTotal + waste + hCost + lCost + pCost;

  const tCost = TOOLING_COST + dimensionExtra;
  const subTotal = directCost + tCost;
  const prof = Math.round(subTotal * PROFIT_PERCENTAGE);

  const total = subTotal + prof;

  return {
    boardCostTotal: Math.round(bCostTotal),
    boardDetails: bDetails,
    hardwareCost: hCost,
    hardwareDetails: hDetails,
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

export default function LShapeTableCalculator() {
  const [isCustomSize, setIsCustomSize] = useState<boolean>(false);
  const [mainWidth, setMainWidth] = useState<number>(900); // mm
  const [mainDepth, setMainDepth] = useState<number>(600); // mm
  const [returnWidth, setReturnWidth] = useState<number>(900); // mm
  const [returnDepth, setReturnDepth] = useState<number>(600); // mm
  const [height, setHeight] = useState<number>(750); // mm
  const [returnHeight, setReturnHeight] = useState<number>(750); // mm
  const [topThickness, setTopThickness] = useState<number>(18); // mm

  const [boardId, setBoardId] = useState<string>("plpb");
  const [legId, setLegId] = useState<string>("board");
  const [boardLegType, setBoardLegType] = useState<string>("full");
  const [metalLegStyle, setMetalLegStyle] = useState<string>("straight");
  const [metalLegPipeSize, setMetalLegPipeSize] = useState<string>("40x40");

  const [includeModesty, setIncludeModesty] = useState<boolean>(true);
  const [modestyType, setModestyType] = useState<string>("standard");
  const [wireManagement, setWireManagement] = useState<string>("grommet"); // 'grommet', 'raceway', 'none'
  const [includePedestal, setIncludePedestal] = useState<boolean>(true);
  const [includeReturnStorage, setIncludeReturnStorage] =
    useState<boolean>(true);

  const [showExportModal, setShowExportModal] = useState(false);
  const [exportIncludeModesty, setExportIncludeModesty] = useState(true);
  const [exportModestyType, setExportModestyType] = useState<string>("standard");
  const [exportIncludePedestal, setExportIncludePedestal] = useState(true);
  const [exportWireManagement, setExportWireManagement] = useState<string>("grommet");
  const [exportThickness, setExportThickness] = useState<string>("all");
  const [exportIncludeReturnStorage, setExportIncludeReturnStorage] = useState(true);
  const [exportMaterial, setExportMaterial] = useState<string>("all");
  const [exportLegId, setExportLegId] = useState<string>("board");
  const [exportBoardLegType, setExportBoardLegType] = useState<string>("full");

  const {
    boardCostTotal,
    boardDetails,
    hardwareCost,
    hardwareDetails,
    modestyCost,
    wasteCost,
    laborCost,
    packingCost,
    toolingCost,
    profit,
    totalCost,
    totalSqFt,
  } = useMemo(() => {
    return calculateLShapeCost({
      mainWidth,
      mainDepth,
      returnWidth,
      returnDepth,
      height,
      returnHeight,
      topThickness,
      boardId,
      legId,
      boardLegType,
      metalLegStyle,
      metalLegPipeSize,
      includeModesty,
      modestyType,
      wireManagement,
      includePedestal,
      includeReturnStorage
    });
  }, [
    mainWidth,
    mainDepth,
    returnWidth,
    returnDepth,
    height,
    returnHeight,
    boardId,
    legId,
    boardLegType,
    metalLegStyle,
    metalLegPipeSize,
    includeModesty,
    modestyType,
    wireManagement,
    includePedestal,
    includeReturnStorage,
    topThickness,
  ]);

  const downloadPDF = () => {
    const doc = new jsPDF();
    const board = BOARDS.find((b) => b.id === boardId)!;
    const legType = LEGS.find((l) => l.id === legId)!;

    doc.setFontSize(20);
    doc.text("All Table Cost Estimation Report", 14, 22);

    doc.setFontSize(12);
    doc.text(`Date: ${new Date().toLocaleDateString()}`, 14, 32);

    const specBody = [
      [
        "Main Table Dimensions (W x D x H)",
        `${mainWidth} mm x ${mainDepth} mm x ${height} mm`,
      ],
    ];
    if (includeReturnStorage) {
      specBody.push([
        "Return Storage Dimensions (W x D x H)",
        `${returnWidth} mm x ${returnDepth} mm x ${returnHeight} mm`,
      ]);
    }
    specBody.push(
      ["Table Top Thickness", `${topThickness} mm`],
      ["Board Material", `${board.name} (Rs. ${getTopRate(board.id, board.costPerSqFt, topThickness)}/sq.ft)`],
      ["Understructure", legType.name],
      ["Modesty Panel", includeModesty ? "Included" : "None"],
      ["Wire Management", wireManagement.toUpperCase()],
    );

    autoTable(doc, {
      startY: 40,
      head: [["Specification", "Details"]],
      body: specBody,
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
      ["Material Waste (15%)", `Rs. ${wasteCost.toLocaleString()}`],
      [
        "Hardware & Accessories",
        `Rs. ${Math.round(hardwareCost).toLocaleString()}`,
      ],
      ["Labor & Making", `Rs. ${laborCost.toLocaleString()}`],
      ["Packing", `Rs. ${packingCost.toLocaleString()}`],
      ["Tooling", `Rs. ${toolingCost.toLocaleString()}`],
      ["Profit (25%)", `Rs. ${profit.toLocaleString()}`],
    ];

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

    doc.save("lshape-table-cost-report.pdf");
  };

  const downloadExcel = () => {
    const wb = XLSX.utils.book_new();

    const board = BOARDS.find((b) => b.id === boardId)!;
    const legType = LEGS.find((l) => l.id === legId)!;

    // 1. Cover / Specs Sheet
    const specsData = [
      ["All Table Cost Estimation Report"],
      ["Date", new Date().toLocaleDateString()],
      [""],
      ["Specification", "Details"],
      [
        "Main Table Dimensions (W x D x H)",
        `${mainWidth} mm x ${mainDepth} mm x ${height} mm`,
      ],
    ];

    if (includeReturnStorage) {
      specsData.push([
        "Return Storage Dimensions (W x D x H)",
        `${returnWidth} mm x ${returnDepth} mm x ${returnHeight} mm`,
      ]);
    }

    specsData.push(
      ["Table Top Thickness", `${topThickness} mm`],
      ["Board Material", `${board.name} (Rs. ${getTopRate(board.id, board.costPerSqFt, topThickness)}/sq.ft)`],
      ["Understructure", legType.name],
      ["Modesty Panel", includeModesty ? "Included" : "None"],
      ["Wire Management", wireManagement.toUpperCase()],
    );
    const wsSpecs = XLSX.utils.aoa_to_sheet(specsData);
    XLSX.utils.book_append_sheet(wb, wsSpecs, "Specifications");

    // 2. Details Sheet
    const detailsData: any[][] = [];
    detailsData.push(["Detailed Board Cost", "Amount", "Calculation Concept"]);
    boardDetails.forEach((b) => {
      detailsData.push([
        b.label,
        Math.round(b.cost),
        "Board Surface Area (sq.ft) × Board Material Rate",
      ]);
    });

    detailsData.push([""]);
    detailsData.push([
      "Hardware & Accessories Included",
      "Qty",
      "Unit Price",
      "Total Cost",
      "Calculation Concept",
    ]);
    if (hardwareDetails.length > 0) {
      hardwareDetails.forEach((h) => {
        detailsData.push([
          h.label,
          h.qty,
          h.unitPrice,
          Math.round(h.cost),
          "Quantity × Unit Price",
        ]);
      });
    } else {
      detailsData.push(["No hardware selected", "", "", "", ""]);
    }

    detailsData.push([""]);
    detailsData.push([
      "Cost Summary (Overall Calculation)",
      "Amount",
      "Calculation Concept",
    ]);
    detailsData.push([
      "Total Board Cost",
      boardCostTotal,
      "Sum of all individual board pieces (main table + return + understructure)",
    ]);
    detailsData.push([
      "Material Waste (15%)",
      wasteCost,
      "15% of Total Board Cost (Board Cost × 0.15) for standard cutting wastage",
    ]);
    detailsData.push([
      "Hardware & Accessories",
      Math.round(hardwareCost),
      "Sum of all selected hardware items",
    ]);
    detailsData.push([
      "Labor & Making",
      laborCost,
      "Standard fixed labor charges for L-shape tables",
    ]);
    detailsData.push([
      "Packing",
      packingCost,
      "Standard fixed packing charges",
    ]);
    detailsData.push([
      "Tooling",
      toolingCost,
      "5% of Direct Costs (Board + Waste + Hardware + Labor + Packing) for machinery overhead",
    ]);
    detailsData.push([
      "Profit (25%)",
      profit,
      "25% of Subtotal (Direct Costs + Tooling)",
    ]);
    detailsData.push([""]);
    detailsData.push([
      "Total Estimated Cost",
      totalCost,
      "Sum of Subtotal + Profit",
    ]);

    const wsDetails = XLSX.utils.aoa_to_sheet(detailsData);
    XLSX.utils.book_append_sheet(wb, wsDetails, "Cost Details");

    // 3. Formulas and Concepts Sheet
    const formulasData = [
      ["Metric", "Formula Used", "Description"],
      [
        "Area (sq.ft)",
        "(Width (mm) × Depth (mm)) / 92903.04",
        "1 sq.ft = 92903.04 sq.mm. Panel dimensions are multiplied to get sq.mm, then divided by 92903.04.",
      ],
      [
        "Board Cost",
        "Area (sq.ft) × Material Rate",
        "Calculated by multiplying the surface area in sq.ft by the selected board's per sq.ft rate.",
      ],
      [
        "Material Waste",
        "Total Board Cost × 15%",
        "Standard 15% waste margin added to account for cutting and offcuts.",
      ],
      [
        "Hardware Cost",
        "Qty × Unit Price",
        "Quantity of hardware items multiplied by respective unit prices.",
      ],
      [
        "Labor & Making",
        "Fixed Amount",
        "Standardized fixed labor charges for assembly.",
      ],
      [
        "Packing",
        "Fixed Amount",
        "Standard fixed charges for packing the item.",
      ],
      [
        "Tooling",
        "(Direct Costs) × 5%",
        "Machinery overhead estimated at 5% of direct costs (Board + Waste + Hardware + Labor + Packing).",
      ],
      [
        "Profit",
        "Subtotal × 25%",
        "25% profit margin applied to the subtotal before final pricing.",
      ],
      [
        "Total Estimated Cost",
        "Subtotal + Profit",
        "The final calculated estimated cost for the product.",
      ],
    ];
    const wsFormulas = XLSX.utils.aoa_to_sheet(formulasData);
    XLSX.utils.book_append_sheet(wb, wsFormulas, "Calculation Formulas");

    XLSX.writeFile(wb, "lshape-table-cost-report.xlsx");
  };

  const downloadMasterPriceList = () => {
    const wb = XLSX.utils.book_new();

    const masterData: any[][] = [];
    masterData.push([
      "Board Material",
      "Main Desk (WxDxH mm)",
      "Return Desk (WxDxH mm)",
      "Top Thickness",
      "Understructure",
      "Cost Price (Rs)",
    ]);

    const widths = [750, 900, 1800, 2100, 2400];
    const depths = [600, 750, 900, 1100];
    const thicknesses = exportThickness === "all" ? [17, 18, 25, 35, 36] : [Number(exportThickness)];
    const boardsToExport = exportMaterial === "all" ? BOARDS : BOARDS.filter(b => b.id === exportMaterial);
    const exportLegName = LEGS.find(l => l.id === exportLegId)?.name || 'Board Leg';
    const exportLeg = exportLegId === "board" ? `${exportLegName} (${exportBoardLegType === "shorter" ? "Shorter" : "Full Depth"})` : exportLegName;

    // Build the master data
    for (const board of boardsToExport) {
      for (const mw of widths) {
        for (const md of depths) {
          if (!exportIncludeReturnStorage) {
            for (const t of thicknesses) {
              const res = calculateLShapeCost({
                mainWidth: mw,
                mainDepth: md,
                returnWidth: 900,
                returnDepth: 600,
                height: 750,
                returnHeight: 750,
                topThickness: t,
                boardId: board.id,
                legId: exportLegId,
                boardLegType: exportBoardLegType,
                metalLegStyle: "straight",
                metalLegPipeSize: "40x40",
                includeModesty: exportIncludeModesty,
                modestyType: exportModestyType,
                wireManagement: exportWireManagement,
                includePedestal: exportIncludePedestal,
                includeReturnStorage: false
              });

              masterData.push([
                board.name,
                `${mw}x${md}x${750}`,
                `None`,
                `${t}mm`,
                exportLeg,
                res.totalCost,
              ]);
            }
            continue;
          }

          for (const rw of widths) {
            for (const rd of depths) {
              for (const t of thicknesses) {
                const res = calculateLShapeCost({
                  mainWidth: mw,
                  mainDepth: md,
                  returnWidth: rw,
                  returnDepth: rd,
                  height: 750,
                  returnHeight: 750,
                  topThickness: t,
                  boardId: board.id,
                  legId: exportLegId,
                  boardLegType: exportBoardLegType,
                  metalLegStyle: "straight",
                  metalLegPipeSize: "40x40",
                  includeModesty: exportIncludeModesty,
                  modestyType: exportModestyType,
                  wireManagement: exportWireManagement,
                  includePedestal: exportIncludePedestal,
                  includeReturnStorage: true
                });

                masterData.push([
                  board.name,
                  `${mw}x${md}x${750}`,
                  `${rw}x${rd}x${750}`,
                  `${t}mm`,
                  exportLeg,
                  res.totalCost,
                ]);
              }
            }
          }
        }
      }
    }

    const wsMaster = XLSX.utils.aoa_to_sheet(masterData);
    const colWidths = [{ wch: 15 }, { wch: 22 }, { wch: 22 }, { wch: 15 }, { wch: 20 }, { wch: 15 }];
    wsMaster["!cols"] = colWidths;

    XLSX.utils.book_append_sheet(wb, wsMaster, "Master Price List");
    XLSX.writeFile(wb, "l-shape-table-master-price-list.xlsx");
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex items-center gap-3">
        <div className="p-3 bg-indigo-100 text-indigo-600 rounded-xl">
          <Calculator className="w-6 h-6" />
        </div>
        <div>
          <h1 className="text-3xl font-semibold tracking-tight text-gray-900">
            All Table Calculator
          </h1>
          <p className="text-gray-500 flex items-center gap-2 mt-1">
            Calculate manufacturing costs for executive L-shaped tables.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-12 gap-8">
        <div className="xl:col-span-8 space-y-6">
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
            <div className="space-y-6">
              <div>
                <h3 className="text-sm font-semibold text-gray-800 mb-3 border-b pb-2">
                  Main Table
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Width
                    </label>
                    {isCustomSize ? (
                      <input
                        type="number"
                        value={mainWidth}
                        onChange={(e) => setMainWidth(Number(e.target.value))}
                        min={0}
                        className="block w-full px-4 py-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                      />
                    ) : (
                      <select
                        value={mainWidth}
                        onChange={(e) => setMainWidth(Number(e.target.value))}
                        className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                      >
                        <option value={750}>750 mm</option>
                        <option value={900}>900 mm</option>
                        <option value={1800}>1800 mm</option>
                        <option value={2100}>2100 mm</option>
                        <option value={2400}>2400 mm</option>
                      </select>
                    )}
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Depth
                    </label>
                    {isCustomSize ? (
                      <input
                        type="number"
                        value={mainDepth}
                        onChange={(e) => setMainDepth(Number(e.target.value))}
                        min={0}
                        className="block w-full px-4 py-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                      />
                    ) : (
                      <select
                        value={mainDepth}
                        onChange={(e) => setMainDepth(Number(e.target.value))}
                        className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                      >
                        <option value={600}>600 mm</option>
                        <option value={750}>750 mm</option>
                        <option value={900}>900 mm</option>
                        <option value={1100}>1100 mm</option>
                      </select>
                    )}
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Height
                    </label>
                    {isCustomSize ? (
                      <input
                        type="number"
                        value={height}
                        onChange={(e) => setHeight(Number(e.target.value))}
                        min={0}
                        className="block w-full px-4 py-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                      />
                    ) : (
                      <select
                        value={height}
                        onChange={(e) => setHeight(Number(e.target.value))}
                        className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                      >
                        <option value={750}>750 mm</option>
                      </select>
                    )}         </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Top Thickness
                    </label>
                    <select
                      value={topThickness}
                      onChange={(e) => setTopThickness(Number(e.target.value))}
                      className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
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

              <div>
                <div className="flex items-center justify-between mb-3 border-b pb-2">
                  <h3 className="text-sm font-semibold text-gray-800">
                    Return Storage
                  </h3>
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={includeReturnStorage}
                      onChange={(e) =>
                        setIncludeReturnStorage(e.target.checked)
                      }
                      className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500 transition-colors"
                    />
                    <span className="text-sm text-gray-600">
                      Include Return Storage
                    </span>
                  </label>
                </div>
                {includeReturnStorage && (
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Width
                      </label>
                      {isCustomSize ? (
                        <input
                          type="number"
                          value={returnWidth}
                          onChange={(e) => setReturnWidth(Number(e.target.value))}
                          min={0}
                          className="block w-full px-4 py-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                        />
                      ) : (
                        <select
                          value={returnWidth}
                          onChange={(e) => setReturnWidth(Number(e.target.value))}
                          className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                        >
                          <option value={750}>750 mm</option>
                          <option value={900}>900 mm</option>
                          <option value={1800}>1800 mm</option>
                          <option value={2100}>2100 mm</option>
                          <option value={2400}>2400 mm</option>
                        </select>
                      )}
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Depth
                      </label>
                      {isCustomSize ? (
                        <input
                          type="number"
                          value={returnDepth}
                          onChange={(e) => setReturnDepth(Number(e.target.value))}
                          min={0}
                          className="block w-full px-4 py-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                        />
                      ) : (
                        <select
                          value={returnDepth}
                          onChange={(e) => setReturnDepth(Number(e.target.value))}
                          className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                        >
                          <option value={600}>600 mm</option>
                          <option value={750}>750 mm</option>
                          <option value={900}>900 mm</option>
                          <option value={1100}>1100 mm</option>
                        </select>
                      )}
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Height
                      </label>
                      {isCustomSize ? (
                        <input
                          type="number"
                          value={returnHeight}
                          onChange={(e) => setReturnHeight(Number(e.target.value))}
                          min={0}
                          className="block w-full px-4 py-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                        />
                      ) : (
                        <select
                          value={returnHeight}
                          onChange={(e) =>
                            setReturnHeight(Number(e.target.value))
                          }
                          className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                        >
                          <option value={750}>750 mm</option>
                        </select>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

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
                  Wire Management
                </label>
                <select
                  value={wireManagement}
                  onChange={(e) => setWireManagement(e.target.value)}
                  className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all"
                >
                  <option value="none">None</option>
                  <option value="grommet">PVC Grommets</option>
                  <option value="raceway">Aluminum Flap Box</option>
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
                          Board covers for main and return
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
                        Include Pedestal Drawer Unit
                      </span>
                      <span className="text-xs text-gray-500">
                        Adds an estimated ₹4,200 pedestal cost
                      </span>
                    </div>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>

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

              <div className="flex flex-col gap-3">
                <button
                  onClick={downloadPDF}
                  className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white py-2.5 px-4 rounded-lg font-medium transition-colors"
                >
                  <Download className="w-4 h-4" />
                  Download PDF Report
                </button>
                <button
                  onClick={downloadExcel}
                  className="w-full flex items-center justify-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white py-2.5 px-4 rounded-lg font-medium transition-colors mb-3"
                >
                  <FileSpreadsheet className="w-4 h-4" />
                  Download Excel Report
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
                <span className="text-sm font-medium">Include Pedestal Unit</span>
              </label>

              <label className="flex items-center gap-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                <input
                  type="checkbox"
                  checked={exportIncludeReturnStorage}
                  onChange={(e) => setExportIncludeReturnStorage(e.target.checked)}
                  className="w-4 h-4 text-indigo-600 rounded border-gray-300"
                />
                <span className="text-sm font-medium">Include Return Storage</span>
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
