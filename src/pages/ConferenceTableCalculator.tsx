import {
  useState,
  useMemo,
  useEffect } from "react";
import { useParams,
  useSearchParams,
  useNavigate } from "react-router-dom";
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
  Sparkles,
  Info
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
const LPATTI_COST = 10;

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
  legCountInput,
  includeModesty,
  modestyType,
  customModestyHeight,
  modestyFinish,
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


  // Modesty Calculation
  if (includeModesty) {
      let modestyHeightMm = 450;
      if (modestyType === "standard") modestyHeightMm = 715;
      else if (modestyType === "short") modestyHeightMm = 600;
      else if (modestyType === "shorter") modestyHeightMm = 300;
      else if (modestyType === "custom") modestyHeightMm = customModestyHeight || 300;

      const modestyAreaSqMm = mainWidth * modestyHeightMm;
      let modestyRate = board.costPerSqFt;
      if (modestyFinish === "fluted") modestyRate += 100;
      
      const modestyAreaSqFt = modestyAreaSqMm / 90000;
      const modestyCost = modestyAreaSqFt * modestyRate;

      bDetails.push({
          label: `Modesty Panel (${modestyFinish}) - ${mainWidth}x${modestyHeightMm}mm (${modestyAreaSqFt.toFixed(2)} sq.ft)`,
          cost: Math.round(modestyCost),
      });
      bCostTotal += modestyCost;
  }

  // Legs Calculation
  let legCount = legCountInput || (mainWidth >= 2400 ? 3 : 2);
  let legCostTotal = 0;
  let legDesc = "";

  let hardwareLegCost = 0;
  let hardwareLegDesc = "";

  if (legType === "metal_straight" || legType === "metal_u") {
      // Calculate like normal table (pipe dimensions)
      let verticalLengthMm = legCount * 2 * height;
      if (legType === "metal_u") {
          verticalLengthMm += legCount * mainDepth; // u-shape has bottom loops
      }
      const verticalFeet = verticalLengthMm / 304.8;
      const verticalRate = 27; // 40x40 pipe
      const costVerticals = verticalFeet * verticalRate;

      // 40x20 Pipe for horizontal supports
      const horizontalWidthMm = 2 * Math.max(0, mainWidth - 140);
      const horizontalDepthMm = Math.max(0, mainDepth - 180) * legCount;
      const horizontalLengthMm = horizontalWidthMm + horizontalDepthMm;
      const horizontalFeet = horizontalLengthMm / 304.8;
      const cost40x20 = horizontalFeet * 19.6;

      const totalFeet = verticalFeet + horizontalFeet;
      const powderCoatingCost = totalFeet * 30;

      const numLegs = legCount * 2;
      const bufferCost = numLegs * 7;
      const nutCost = numLegs * 5;
      const butterflyCost = numLegs * 2 * 12.5;
      const clampCost = numLegs * 2 * 10;
      const accessoriesCost = bufferCost + nutCost + butterflyCost + clampCost;

      hardwareLegCost = costVerticals + cost40x20 + powderCoatingCost + accessoriesCost;
      hardwareLegDesc = legType === "metal_straight" ? `Metal Straight Legs Framework` : `Metal U-Shape Legs Framework`;
  } else {
      let areaPerLegSqMm = 0;
      let legRate = board.costPerSqFt; // use base rate
      let effectiveLegCount = legCount;
      let legName = "";

      if (legType === "board") {
          const outerLegArea = mainDepth * height * 2;
          const middleLegDepth = Math.max(400, mainDepth - 400); // Shorter middle leg
          const middleLegCount = Math.max(0, legCount - 2);
          const middleLegArea = middleLegDepth * height * middleLegCount;
          
          areaPerLegSqMm = (outerLegArea + middleLegArea) / legCount;
          effectiveLegCount = legCount;
          
          if (middleLegCount > 0) {
              legName = `2x Board Slab Legs (${mainDepth}mm D), ${middleLegCount}x Middle Board Legs (${middleLegDepth}mm D) x ${height}mm H`;
          } else {
              legName = `2x Board Slab Legs (${mainDepth}mm x ${height}mm)`;
          }
      } else if (legType === "box_plain") {
          const boxWidth = Math.max(0, mainWidth - 600);
          const boxDepth = Math.max(0, mainDepth - 600);
          areaPerLegSqMm = (boxWidth * 2 + boxDepth * 2) * height;
          effectiveLegCount = 1;
          legName = `1x Open Box Base (Plain) (4 Panels: 2x ${boxWidth}mm W & 2x ${boxDepth}mm D x ${height}mm H, No Top/Bottom)`;
      } else if (legType === "box_fluted") {
          const boxWidth = Math.max(0, mainWidth - 600);
          const boxDepth = Math.max(0, mainDepth - 600);
          areaPerLegSqMm = (boxWidth * 2 + boxDepth * 2) * height;
          effectiveLegCount = 1;
          legRate += 100; // fluted premium
          legName = `1x Open Box Base (Fluted) (4 Panels: 2x ${boxWidth}mm W & 2x ${boxDepth}mm D x ${height}mm H, No Top/Bottom)`;
      } else if (legType === "round_plain") {
          const circumference = Math.round(Math.PI * 600); // 1885mm for 600mm dia
          areaPerLegSqMm = circumference * height;
          legName = `${legCount}x Round Legs (Plain) (600mm dia x ${height}mm)`;
      } else if (legType === "round_fluted") {
          const circumference = Math.round(Math.PI * 600); // 1885mm for 600mm dia
          areaPerLegSqMm = circumference * height;
          legRate += 100; // fluted premium
          legName = `${legCount}x Round Legs (Fluted) (600mm dia x ${height}mm)`;
      }

      const totalLegAreaSqFt = (areaPerLegSqMm * effectiveLegCount) / 90000;
      legCostTotal = totalLegAreaSqFt * legRate;
      legDesc = `${legName} (${totalLegAreaSqFt.toFixed(2)} sq.ft @ ₹${legRate}/sq.ft)`;
  }

  if (legCostTotal > 0) {
      bDetails.push({
          label: legDesc,
          cost: Math.round(legCostTotal)
      });
      bCostTotal += legCostTotal;
  }


  let hardwareDetails = [];
  let hardwareCostTotal = 0;

  if (hardwareLegCost > 0) {
      hardwareDetails.push({ label: hardwareLegDesc, cost: hardwareLegCost });
      hardwareCostTotal += hardwareLegCost;
  }

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
  const topPerimeterM = (mainWidth * 2 + mainDepth * 2) / 1000;
  const pattiQty = Math.ceil(topPerimeterM * 3.28084 * 2); // 2 L-Pattis per foot of top perimeter
  const pattiCost = pattiQty * LPATTI_COST;
  const generalHardwareCost = 150; // Minifix, Buffers, Screws
  
  hardwareDetails.push({ label: "Minifix, Buffers, Screws", cost: generalHardwareCost });
  hardwareDetails.push({ 
    label: "L Patti", 
    cost: pattiCost,
    qty: pattiQty,
    unitPrice: LPATTI_COST,
    unitLabel: "pcs"
  });
  hardwareCostTotal += generalHardwareCost + pattiCost;

  let totalMaterialCost = bCostTotal + hardwareCostTotal + addonCostTotal;
  const makingCharges = LABOR_COST * mainTopSqFt; // labor based on top size
  const totalCostBeforeProfit = totalMaterialCost + makingCharges + PACKING_COST + TOOLING_COST;
  const appliedProfitPercentage = (legType === "box_fluted" || legType === "round_fluted") ? 0.40 : PROFIT_PERCENTAGE;
  const profit = totalCostBeforeProfit * appliedProfitPercentage;
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
  const [legCountInput, setLegCountInput] = useState<number>(0);
  const [includeModesty, setIncludeModesty] = useState<boolean>(false);
  const [modestyType, setModestyType] = useState<string>("standard");
  const [customModestyHeight, setCustomModestyHeight] = useState<number>(400);
  const [modestyFinish, setModestyFinish] = useState<string>("plain");
  const [copiedPrompt, setCopiedPrompt] = useState<boolean>(false);

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
      setLegCountInput(editItem.config.legCountInput || 0);
      setIncludeModesty(editItem.config.includeModesty || false);
      setModestyType(editItem.config.modestyType || "standard");
      setCustomModestyHeight(editItem.config.customModestyHeight || 400);
      setModestyFinish(editItem.config.modestyFinish || "plain");
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
      legCountInput,
      includeModesty,
      modestyType,
      customModestyHeight,
      modestyFinish,
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
    legCountInput,
    includeModesty,
    modestyType,
    customModestyHeight,
    modestyFinish,
  ]);

    const downloadPDF = () => {
    const doc = new jsPDF();
    
    doc.setFontSize(20);
    doc.text("Conference Table Cost Estimation", 14, 22);
    
    doc.setFontSize(12);
    doc.text(`Date: ${new Date().toLocaleDateString()}`, 14, 32);
    
    autoTable(doc, {
      startY: 40,
      head: [["Specification", "Details"]],
      body: [
        ["Table Dimensions (W x D x H)", `${mainWidth} mm x ${mainDepth} mm x ${height} mm`],
        ["Table Top Thickness", `${topThickness} mm`],
        ["Board Material", `${getBoards(quality).find((b) => b.id === boardId)?.name}`],
        ["Leg Type", legType.replace("_", " ").toUpperCase()],
      ["Modesty Panel", includeModesty ? `Yes - ${modestyType} (${modestyFinish})` : "No"],
        ["Modesty Panel", includeModesty ? `Yes - ${modestyType} (${modestyFinish})` : "No"],
        ["Wire Management", wireManagement.replace("_", " ").toUpperCase()],
        ["Leatherlite Add-on", addLeatherlite ? "Yes" : "No"],
      ],
      theme: "grid",
      headStyles: { fillColor: [79, 70, 229] },
    });

    const costStartY = (doc as any).lastAutoTable.finalY + 10;
    
    const bodyArgs = [
      ["Board Costs", `Rs. ${costSummary.boardCostTotal.toLocaleString()}`],
      ["Hardware & Legs", `Rs. ${costSummary.hardwareCostTotal.toLocaleString()}`],
      ["Add-ons", `Rs. ${costSummary.addonCostTotal.toLocaleString()}`],
      ["Making Charges", `Rs. ${costSummary.makingCharges.toLocaleString()}`],
      ["Packing & Tooling", `Rs. ${(costSummary.packing + costSummary.tooling).toLocaleString()}`],
      [`Profit (${(legType === "box_fluted" || legType === "round_fluted") ? "40%" : "25%"})`, `Rs. ${costSummary.profit.toLocaleString()}`],
    ];

    autoTable(doc, {
      startY: costStartY,
      head: [["Cost Summary", "Amount"]],
      body: bodyArgs,
      theme: "grid",
      headStyles: { fillColor: [79, 70, 229] },
    });

    const totalStartY = (doc as any).lastAutoTable.finalY + 10;
    autoTable(doc, {
      startY: totalStartY,
      head: [["Total Estimated Cost", `Rs. ${costSummary.totalCost.toLocaleString()}`]],
      theme: "grid",
      headStyles: { fillColor: [17, 24, 39] },
    });

    doc.save("conference-table-cost-report.pdf");
  };

  const downloadExcel = () => {
    const wb = XLSX.utils.book_new();
    
    // 1. Specs Sheet
    const specsData = [
      ["Conference Table Cost Estimation Report"],
      ["Date", new Date().toLocaleDateString()],
      [""],
      ["Specification", "Details"],
      ["Table Dimensions (W x D x H)", `${mainWidth} mm x ${mainDepth} mm x ${height} mm`],
      ["Table Top Thickness", `${topThickness} mm`],
      ["Board Material", `${getBoards(quality).find((b) => b.id === boardId)?.name}`],
      ["Leg Type", legType.replace("_", " ").toUpperCase()],
      ["Modesty Panel", includeModesty ? `Yes - ${modestyType} (${modestyFinish})` : "No"],
      ["Wire Management", wireManagement.replace("_", " ").toUpperCase()],
      ["Leatherlite Add-on", addLeatherlite ? "Yes" : "No"],
    ];
    
    const wsSpecs = XLSX.utils.aoa_to_sheet(specsData);
    XLSX.utils.book_append_sheet(wb, wsSpecs, "Specifications");

    // 2. Details Sheet
    const detailsData: any[][] = [];
    detailsData.push(["Detailed Board Cost", "Amount"]);
    costSummary.boardPiecesDetails.forEach((b: any) => {
      detailsData.push([b.label, Math.round(b.cost)]);
    });
    
    detailsData.push([""]);
    detailsData.push(["Hardware & Accessories Included", "Total Cost"]);
    if (costSummary.hardwareDetails.length > 0) {
      costSummary.hardwareDetails.forEach((h: any) => {
        detailsData.push([h.label, Math.round(h.cost)]);
      });
    } else {
      detailsData.push(["No hardware selected", ""]);
    }
    
    detailsData.push([""]);
    detailsData.push(["Add-ons Included", "Total Cost"]);
    if (costSummary.addonDetails && costSummary.addonDetails.length > 0) {
      costSummary.addonDetails.forEach((h: any) => {
        detailsData.push([h.label, Math.round(h.cost)]);
      });
    } else {
      detailsData.push(["No Add-ons selected", ""]);
    }

    detailsData.push([""]);
    detailsData.push(["Cost Summary (Overall Calculation)", "Amount"]);
    detailsData.push(["Total Board Cost", costSummary.boardCostTotal]);
    detailsData.push(["Hardware & Accessories", Math.round(costSummary.hardwareCostTotal)]);
    detailsData.push(["Add-ons", Math.round(costSummary.addonCostTotal)]);
    detailsData.push(["Labor & Making", costSummary.makingCharges]);
    detailsData.push(["Packing", costSummary.packing]);
    detailsData.push(["Tooling", costSummary.tooling]);
    detailsData.push([`Profit (${(legType === "box_fluted" || legType === "round_fluted") ? "40%" : "25%"})`, costSummary.profit]);
    detailsData.push([""]);
    detailsData.push(["Total Estimated Cost", costSummary.totalCost]);

    const wsDetails = XLSX.utils.aoa_to_sheet(detailsData);
    XLSX.utils.book_append_sheet(wb, wsDetails, "Cost Details");

    XLSX.writeFile(wb, "conference-table-cost-report.xlsx");
  };

  const copyImagePrompt = () => {
    const prompt = `A highly professional product photography shot of a modern conference table. 
The table has a dimension of ${mainWidth}mm width and ${mainDepth}mm depth. 
It features a ${topThickness}mm thick ${boardId.replace('_', ' ')} finish top. 
The base consists of ${legType.replace('_', ' ')} legs.
${wireManagement !== 'none' ? `It has a ${wireManagement.replace('_', ' ')} for wire management.` : ''}
${addLeatherlite ? `There is a premium leatherlite design pad in the center.` : ''}
The setting is a bright, minimalist corporate boardroom with large windows and subtle indoor plants. 
Studio lighting, 8k resolution, photorealistic, architectural digest style.`;
    
    navigator.clipboard.writeText(prompt);
    setCopiedPrompt(true);
    setTimeout(() => setCopiedPrompt(false), 2000);
  };

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
        legCountInput,
        includeModesty,
        modestyType,
        customModestyHeight,
        modestyFinish,
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
                      <option key={b.id} value={b.id}>{b.name} (₹{getTopRate(b.id, b.costPerSqFt, topThickness, quality)}/sq.ft)</option>
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
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">Leg Count</label>
                  <select
                    value={legCountInput}
                    onChange={(e) => setLegCountInput(Number(e.target.value))}
                    className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none bg-white"
                  >
                    <option value={0}>Auto (Based on Width)</option>
                    <option value={2}>2 Legs</option>
                    <option value={3}>3 Legs</option>
                    <option value={4}>4 Legs</option>
                    <option value={5}>5 Legs</option>
                    <option value={6}>6 Legs</option>
                  </select>
                </div>
              </div>
            </section>

            {/* Modesty Panel */}
            <section>
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <FileBox className="w-5 h-5 text-indigo-500" />
                Modesty Panel
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="flex flex-col gap-4">
                  <div className="flex items-center justify-between p-4 border border-gray-200 rounded-xl bg-gray-50/50">
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-indigo-100 rounded-lg">
                        <LayoutGrid className="w-5 h-5 text-indigo-600" />
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-900">Include Modesty</p>
                        <p className="text-xs text-gray-500">Front privacy panel</p>
                      </div>
                    </div>
                    <input 
                      type="checkbox" 
                      checked={includeModesty} 
                      onChange={(e) => setIncludeModesty(e.target.checked)}
                      className="w-5 h-5 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500 cursor-pointer"
                    />
                  </div>
                </div>

                {includeModesty && (
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <label className="block text-sm font-medium text-gray-700">Size / Height</label>
                      <select
                        value={modestyType}
                        onChange={(e) => setModestyType(e.target.value)}
                        className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none bg-white"
                      >
                        <option value="standard">Standard (715mm)</option>
                        <option value="short">Short (600mm)</option>
                        <option value="shorter">Shorter (300mm)</option>
                        <option value="custom">Custom Size</option>
                      </select>
                    </div>

                    {modestyType === "custom" && (
                      <div className="space-y-2 animate-in fade-in slide-in-from-top-2">
                        <label className="block text-sm font-medium text-gray-700">Custom Height (mm)</label>
                        <input
                          type="number"
                          value={customModestyHeight}
                          onChange={(e) => setCustomModestyHeight(Number(e.target.value))}
                          className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none"
                          min="100"
                          max={height - 25}
                        />
                      </div>
                    )}

                    <div className="space-y-2">
                      <label className="block text-sm font-medium text-gray-700">Finish</label>
                      <select
                        value={modestyFinish}
                        onChange={(e) => setModestyFinish(e.target.value)}
                        className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none bg-white"
                      >
                        <option value="plain">Plain</option>
                        <option value="fluted">Fluted</option>
                      </select>
                    </div>
                  </div>
                )}
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
                  <label className="block text-sm font-medium text-gray-700">Type</label>
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
                <Sparkles className="w-5 h-5 text-indigo-500" />
                Add-ons
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="flex items-center justify-between p-4 border border-gray-200 rounded-xl bg-gray-50/50">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-indigo-100 rounded-lg">
                      <Sparkles className="w-5 h-5 text-indigo-600" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Leatherlite Design Pad</p>
                      <p className="text-xs text-gray-500">Premium center insert</p>
                    </div>
                  </div>
                  <input 
                    type="checkbox" 
                    checked={addLeatherlite} 
                    onChange={(e) => setAddLeatherlite(e.target.checked)}
                    className="w-5 h-5 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500 cursor-pointer"
                  />
                </div>
              </div>
            </section>
          </div>
        </div>
        
        <div className="lg:col-span-1">
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden sticky top-6">
            <div className="bg-gray-900 p-6 text-white">
              <h2 className="text-xl font-semibold mb-2">Cost Summary</h2>
              <p className="text-gray-400 text-sm">Estimated manufacturing cost</p>
            </div>
            <div className="p-6 space-y-6">
              {/* Board Details */}
              <div className="space-y-3">
                <div className="flex justify-between items-center text-sm font-semibold text-gray-900 border-b pb-2">
                  <span>Board Material</span>
                  <span>₹{costSummary.boardCostTotal.toLocaleString()}</span>
                </div>
                <div className="space-y-2">
                  {costSummary.boardPiecesDetails.map((item: any, idx: number) => (
                    <div key={idx} className="flex justify-between text-sm text-gray-500">
                      <span className="pr-4">{item.label}</span>
                      <span className="whitespace-nowrap">₹{item.cost.toLocaleString()}</span>
                    </div>
                  ))}
                </div>
              </div>
              
              {/* Hardware Details */}
              <div className="space-y-3">
                <div className="flex justify-between items-center text-sm font-semibold text-gray-900 border-b pb-2">
                  <span>Hardware & Legs</span>
                  <span>₹{costSummary.hardwareCostTotal.toLocaleString()}</span>
                </div>
                <div className="space-y-2">
                  {costSummary.hardwareDetails.map((item: any, idx: number) => (
                    <div key={idx} className="flex justify-between text-sm text-gray-500">
                      <span className="pr-4">{item.label}</span>
                      <span className="whitespace-nowrap">₹{item.cost.toLocaleString()}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Add-ons Details */}
              {costSummary.addonCostTotal > 0 && (
                <div className="space-y-3">
                  <div className="flex justify-between items-center text-sm font-semibold text-gray-900 border-b pb-2">
                    <span>Add-ons</span>
                    <span>₹{costSummary.addonCostTotal.toLocaleString()}</span>
                  </div>
                  <div className="space-y-2">
                    {costSummary.addonDetails.map((item: any, idx: number) => (
                      <div key={idx} className="flex justify-between text-sm text-gray-500">
                        <span className="pr-4">{item.label}</span>
                        <span className="whitespace-nowrap">₹{item.cost.toLocaleString()}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Additional Charges */}
              <div className="space-y-2 pt-2 border-t border-gray-100">
                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-600">Making Charges</span>
                  <span className="font-medium text-gray-900">₹{costSummary.makingCharges.toLocaleString()}</span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-600">Packing & Tooling</span>
                  <span className="font-medium text-gray-900">₹{(costSummary.packing + costSummary.tooling).toLocaleString()}</span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-600">Profit ({(legType === "box_fluted" || legType === "round_fluted") ? "40%" : "25%"})</span>
                  <span className="font-medium text-gray-900">₹{costSummary.profit.toLocaleString()}</span>
                </div>
              </div>

              <div className="pt-4 border-t border-gray-200">
                <div className="flex justify-between items-center">
                  <span className="font-semibold text-gray-900 text-lg">Total Price</span>
                  <span className="text-2xl font-bold text-indigo-600">
                    ₹{costSummary.totalCost.toLocaleString()}
                  </span>
                </div>
              </div>

              <div className="pt-4 space-y-3 border-t border-gray-100">
                <button
                  onClick={handleSave}
                  className="w-full py-2.5 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-xl transition-colors shadow-sm flex justify-center items-center gap-2"
                >
                  {editItemId ? "Update Project Item" : "Save to Project"}
                </button>
                <button
                  onClick={downloadPDF}
                  className="w-full py-2.5 px-4 bg-white border border-gray-200 hover:bg-gray-50 text-gray-700 font-medium rounded-xl transition-colors flex justify-center items-center gap-2"
                >
                  <Download className="w-4 h-4" />
                  Download PDF Report
                </button>
                <button
                  onClick={downloadExcel}
                  className="w-full py-2.5 px-4 bg-white border border-emerald-200 hover:bg-emerald-50 text-emerald-700 font-medium rounded-xl transition-colors flex justify-center items-center gap-2"
                >
                  <FileSpreadsheet className="w-4 h-4" />
                  Download Excel Report
                </button>
                <button
                  onClick={copyImagePrompt}
                  className="w-full py-2.5 px-4 bg-white border border-gray-200 hover:bg-gray-50 text-gray-700 font-medium rounded-xl transition-colors flex justify-center items-center gap-2"
                >
                  <Copy className="w-4 h-4" />
                  {copiedPrompt ? "Copied!" : "Copy Image Prompt"}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
