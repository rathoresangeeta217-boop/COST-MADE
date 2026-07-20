import { useState, useMemo, useEffect, ReactNode, FC, useRef } from "react";
import { useParams, useSearchParams, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "motion/react";
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
  Layers,
  Plus,
  Minus,
  Settings,
  HelpCircle,
  Maximize,
  Minimize,
} from "lucide-react";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import * as XLSX from "xlsx";

const AnimatedDoorGroup: FC<{
  isOpen: boolean;
  onClick: () => void;
  className: string;
  childrenClosed: ReactNode;
  childrenOpen: ReactNode;
}> = ({ isOpen, onClick, className, childrenClosed, childrenOpen }) => (
  <motion.g className={className} onClick={onClick}>
    <AnimatePresence mode="wait">
      {!isOpen ? (
        <motion.g
          key="closed"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.15 }}
        >
          {childrenClosed}
        </motion.g>
      ) : (
        <motion.g
          key="open"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.15 }}
        >
          {childrenOpen}
        </motion.g>
      )}
    </AnimatePresence>
  </motion.g>
);

// Reusing identical material pricing structures
export const getBoards = (quality: string, category: string = "wooden") => {
  if (category === "metal") {
    return [
      { id: "crca_powder_coated", name: "Powder Coated CRCA Metal", costPerSqFt: quality === "affordable" ? 150 : 220 },
      { id: "ss_304", name: "Stainless Steel 304", costPerSqFt: quality === "affordable" ? 350 : 450 },
    ];
  }
  return [
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
};

export const getAvailableThicknesses = (
  boardId: string,
  quality: string,
): number[] => {
  if (boardId === "crca_powder_coated" || boardId === "ss_304") {
    return [0.8, 1, 1.2, 1.6, 2];
  }
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

export const getBoardRate = (
  boardId: string,
  baseRate: number,
  thickness: number,
  quality: string,
): number => {
  if (boardId === "crca_powder_coated" || boardId === "ss_304") {
    return baseRate * (thickness / 1.2);
  }
  if (quality === "affordable") {
    if (boardId === "plpb") {
      if (thickness === 11) return 27;
      if (thickness === 17) return 29;
      if (thickness === 18) return 34;
      if (thickness === 25) return 42;
    }
    if (boardId === "hdhmr") {
      if (Math.abs(thickness - 16.75) < 0.1) return 88;
      if (thickness === 18) return 99;
      if (thickness === 25) return 135;
    }
    if (boardId === "ply_laminate") {
      if (thickness === 6) return 22;
      if (thickness === 9) return 35;
      if (thickness === 12) return 38;
      if (thickness === 15) return 46;
      if (thickness === 16) return 46;
      if (thickness === 18) return 55;
    }
    if (boardId === "mdf") {
      if (thickness === 17) return 55;
      if (thickness === 18) return 60;
      if (thickness === 25) return 80;
      if (thickness === 35) return 112;
    }
  } else {
    // Standard quality logic
    if (boardId === "plpb") {
      if (thickness === 18) return 49;
      if (thickness === 25) return 63;
      if (thickness === 36) return 98;
    }
    if (boardId === "hdhmr") {
      if (thickness === 25) return 108;
    }
    if (boardId === "mdf") {
      if (thickness === 18) return 61;
      if (thickness === 25) return 83;
      if (thickness === 36) return 122;
    }
  }
  return baseRate * (thickness / 18);
};

const HARDWARE_CHANNEL_COST = 250;
const HARDWARE_HANDLE_COST = 50;
const HARDWARE_LOCK_COST = 120;
const HARDWARE_CENTRAL_LOCK_COST = 220;
const HARDWARE_SHUTTER_HINGE_COST = 75; // Rs 150 per pair
const HARDWARE_LEVELLER_COST = 50; // Levelling legs
const BASE_LABOR_COST = 600;
const LABOR_PER_BAY_COST = 300;
const PACKING_COST = 400;
const TOOLING_COST = 150;
const PROFIT_PERCENTAGE = 0.25;
const LPATTI_COST = 10;

interface ColumnConfig {
  style: "open" | "shutter_solid" | "shutter_glass" | "shutters_double" | "3_drawers" | "2_drawers" | "1_drawer" | "1_drawer_open" | "1_drawer_1_shutter" | "vertical_horizontal";
  shelves: number;
  verticalShelves?: number;
  boxShutters?: boolean[];
  removedPartitions?: string[];
  shelfOffsets?: Record<number, number>;
  verticalShelfOffsets?: Record<number, number>;
  lock: "none" | "individual" | "central";
  handle: boolean;
  shutterLock?: "none" | "individual";
  shutterHandle?: boolean;
}

export default function CustomStorageCalculator() {
  const { projectId } = useParams();
  const [searchParams] = useSearchParams();
  const editItemId = searchParams.get("edit");
  const navigate = useNavigate();
  const { projects, addItemToProject, updateItemInProject } = useProjectStore();

  const [activeTab, setActiveTab] = useState<"storage" | "drawer" | "locker">("storage");
  const [copiedPrompt, setCopiedPrompt] = useState<boolean>(false);
  const [isCustomSize, setIsCustomSize] = useState<boolean>(false);
  const [isFullScreenDrawing, setIsFullScreenDrawing] = useState<boolean>(false);
  const [zoomLevel, setZoomLevel] = useState<number>(1);
  const isDraggingRef = useRef(false);
  const [openDoors, setOpenDoors] = useState<Set<string>>(new Set());
  const [isDrawingAngular, setIsDrawingAngular] = useState(false);
  const [currentAngularShelf, setCurrentAngularShelf] = useState<{x1: number, y1: number, x2: number, y2: number} | null>(null);
  const [angularShelves, setAngularShelves] = useState<{id: string, x1: number, y1: number, x2: number, y2: number}[]>([]);

  const [dragState, setDragState] = useState<{
    bayIdx: number;
    type: 'h' | 'v' | 'main_h' | 'main_v' | 'angular_endpoint';
    idx: number;
    startX: number;
    startY: number;
    bayX: number;
    bayY: number;
    bayW: number;
    bayH: number;
    isDragging: boolean;
    partitionId: string;
    shelfId?: string;
  } | null>(null);

  const getShelfY = (bay: ColumnConfig, sIdx: number, baseH: number, baseY: number) => {
    if (bay.shelfOffsets?.[sIdx] !== undefined) {
      return baseY + 2 + bay.shelfOffsets[sIdx] * baseH;
    }
    return baseY + 2 + ((sIdx + 1) * baseH) / ((bay.shelves || 0) + 1);
  };

  const getVerticalShelfX = (bay: ColumnConfig, vIdx: number, baseW: number, baseX: number) => {
    if (bay.verticalShelfOffsets?.[vIdx] !== undefined) {
      return baseX + 2 + bay.verticalShelfOffsets[vIdx] * baseW;
    }
    return baseX + 2 + ((vIdx + 1) * baseW) / ((bay.verticalShelves || 0) + 1);
  };

  
  const renderShelves = (bay: ColumnConfig, idx: number, bayX: number, bayY: number, bayW: number, bayH: number) => {
    const cols = (bay.verticalShelves || 0) + 1;
    const rows = (bay.shelves || 0) + 1;
    const baseW = bayW - 4;
    const baseH = bayH - 4;
    const elements = [];

    const vXs = [bayX + 2];
    for (let vIdx = 0; vIdx < (bay.verticalShelves || 0); vIdx++) {
        vXs.push(getVerticalShelfX(bay, vIdx, baseW, bayX));
    }
    vXs.push(bayX + bayW - 2);

    const hYs = [bayY + 2];
    for (let sIdx = 0; sIdx < (bay.shelves || 0); sIdx++) {
        hYs.push(getShelfY(bay, sIdx, baseH, bayY));
    }
    hYs.push(bayY + bayH - 2);

    // Horizontal segments
    for (let sIdx = 0; sIdx < (bay.shelves || 0); sIdx++) {
      const sY = hYs[sIdx + 1];
      for (let cIdx = 0; cIdx < cols; cIdx++) {
        const pId = `h-${sIdx}-${cIdx}`;
        const isRemoved = (bay.removedPartitions || []).includes(pId);
        const sX1 = vXs[cIdx];
        const sX2 = vXs[cIdx + 1];
        elements.push(
          <g key={pId} 
            className={dragState?.partitionId === pId ? "cursor-grabbing" : "cursor-row-resize hover:opacity-80 transition-opacity"} 
            onPointerDown={(e) => {
                setDragState({
                    bayIdx: idx, type: 'h', idx: sIdx, startX: e.clientX, startY: e.clientY,
                    bayX, bayY, bayW, bayH, isDragging: false, partitionId: pId
                });
                if (e.target && (e.target as Element).setPointerCapture) (e.target as Element).setPointerCapture(e.pointerId);
                e.stopPropagation();
            }}
            onClick={(e) => { e.stopPropagation(); if (!isDraggingRef.current) togglePartition(pId, idx); }}
          >
            <line x1={sX1} y1={sY} x2={sX2} y2={sY} stroke="transparent" strokeWidth="15" />
            <line
              x1={sX1} y1={sY} x2={sX2} y2={sY}
              stroke={isRemoved ? "rgba(71,85,105,0.3)" : "#475569"}
              strokeWidth={isRemoved ? "1" : "2"}
              strokeDasharray={isRemoved ? "4,4" : "none"}
            />
          </g>
        );
      }
    }

    // Vertical segments
    for (let vIdx = 0; vIdx < (bay.verticalShelves || 0); vIdx++) {
      const vX = vXs[vIdx + 1];
      for (let rIdx = 0; rIdx < rows; rIdx++) {
        const pId = `v-${vIdx}-${rIdx}`;
        const isRemoved = (bay.removedPartitions || []).includes(pId);
        const vY1 = hYs[rIdx];
        const vY2 = hYs[rIdx + 1];
        elements.push(
          <g key={pId} 
            className={dragState?.partitionId === pId ? "cursor-grabbing" : "cursor-row-resize hover:opacity-80 transition-opacity"} 
            onPointerDown={(e) => {
                setDragState({
                    bayIdx: idx, type: 'v', idx: vIdx, startX: e.clientX, startY: e.clientY,
                    bayX, bayY, bayW, bayH, isDragging: false, partitionId: pId
                });
                if (e.target && (e.target as Element).setPointerCapture) (e.target as Element).setPointerCapture(e.pointerId);
                e.stopPropagation();
            }}
            onClick={(e) => { e.stopPropagation(); if (!isDraggingRef.current) togglePartition(pId, idx); }}
          >
            <line x1={vX} y1={vY1} x2={vX} y2={vY2} stroke="transparent" strokeWidth="15" />
            <line
              x1={vX} y1={vY1} x2={vX} y2={vY2}
              stroke={isRemoved ? "rgba(71,85,105,0.3)" : "#475569"}
              strokeWidth={isRemoved ? "1" : "2"}
              strokeDasharray={isRemoved ? "4,4" : "none"}
            />
          </g>
        );
      }
    }
    return elements;
  };

  const togglePartition = (partitionId: string, bayIdx: number) => {
    const newBays = [...bays];
    const bay = newBays[bayIdx];
    const removed = new Set(bay.removedPartitions || []);
    if (removed.has(partitionId)) {
      removed.delete(partitionId);
    } else {
      removed.add(partitionId);
    }
    bay.removedPartitions = Array.from(removed);
    setBays(newBays);
  };

  const toggleDoor = (id: string) => {
    setOpenDoors(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  // Dimensions and properties
  const [width, setWidth] = useState<number>(1200); // mm
  const [depth, setDepth] = useState<number>(450); // mm
  const [height, setHeight] = useState<number>(750); // mm
  
  // Single Drawer dimensions
  const [drawerWidth, setDrawerWidth] = useState<number>(600);
  const [drawerDepth, setDrawerDepth] = useState<number>(450);
  const [drawerHeight, setDrawerHeight] = useState<number>(150);
  const [lockerWidth, setLockerWidth] = useState<number>(900);
  const [lockerDepth, setLockerDepth] = useState<number>(450);
  const [lockerHeight, setLockerHeight] = useState<number>(1800);
  const [lockerColumns, setLockerColumns] = useState<number>(3);
  const [lockerTiers, setLockerTiers] = useState<number>(6);
  const [lockerThickness, setLockerThickness] = useState<number>(0.8);
  const [lockerSizeMode, setLockerSizeMode] = useState<"overall" | "box">("overall");
  const [lockerBoxWidth, setLockerBoxWidth] = useState<number>(300);
  const [lockerBoxHeight, setLockerBoxHeight] = useState<number>(300);
  const [removedLockerDoors, setRemovedLockerDoors] = useState<string[]>([]);
  const [lockerLockType, setLockerLockType] = useState<"cam" | "digital" | "padlock" | "none">("cam");
  const [lockerCncDesign, setLockerCncDesign] = useState<boolean>(false);
  const [lockerAddBottomLegs, setLockerAddBottomLegs] = useState<boolean>(false);
  
  useEffect(() => {
    setRemovedLockerDoors([]);
  }, [lockerColumns, lockerTiers]);
  const [drawerLock, setDrawerLock] = useState<boolean>(false);
  const [drawerHandle, setDrawerHandle] = useState<boolean>(true);

  const [constructionCategory, setConstructionCategory] = useState<"wooden" | "metal">("wooden");
  const [angleThickness, setAngleThickness] = useState<number>(1.6);
  const [shelfMaterialType, setShelfMaterialType] = useState<"metal" | "wooden">("metal");
  const [woodenShelfId, setWoodenShelfId] = useState<string>("plpb");
  const [woodenShelfThickness, setWoodenShelfThickness] = useState<number>(18);
  const [addVerticalPartitionMiddle, setAddVerticalPartitionMiddle] = useState<boolean>(false);
  const [addMetalBottomLegs, setAddMetalBottomLegs] = useState<boolean>(false);
  const [quality, setQuality] = useState<string>("standard");
  const [boardId, setBoardId] = useState<string>("plpb");
  const [boardThickness, setBoardThickness] = useState<number>(18);
  const [shutterBoardId, setShutterBoardId] = useState<string>("default");
  const [backPanelBoardId, setBackPanelBoardId] = useState<string>("default");
  const [drawerBoxBoardId, setDrawerBoxBoardId] = useState<string>("default");
  const [pieceOverrides, setPieceOverrides] = useState<Record<string, string>>({});
  const [thicknessOverrides, setThicknessOverrides] = useState<Record<string, number>>({});
  const [showAdvancedMaterials, setShowAdvancedMaterials] = useState<boolean>(false);
  const [innerMica, setInnerMica] = useState<string>("none");
  const [outerMica, setOuterMica] = useState<string>("none");
  const [numRows, setNumRows] = useState<number>(1);
  const [numBays, setNumBays] = useState<number>(3);
  const [colOffsets, setColOffsets] = useState<Record<number, number>>({});
  const [rowOffsets, setRowOffsets] = useState<Record<number, number>>({});
  const [supportLegsCount, setSupportLegsCount] = useState<number>(4);

  // Column arrangements
  const [bays, setBays] = useState<ColumnConfig[]>([
    { style: "shutter_solid", shelves: 1, verticalShelves: 0, lock: "individual", handle: true },
    { style: "open", shelves: 1, verticalShelves: 0, lock: "none", handle: false },
    { style: "3_drawers", shelves: 0, verticalShelves: 0, lock: "central", handle: true },
  ]);

  useEffect(() => {
    if (editItemId && projectId) {
      const project = projects.find(p => p.id === projectId);
      const item = project?.items.find(i => i.id === editItemId);
      if (item && item.config) {
        const c = item.config;
        if (c.activeTab !== undefined) setActiveTab(c.activeTab);
        if (c.isCustomSize !== undefined) setIsCustomSize(c.isCustomSize);
        if (c.width !== undefined) setWidth(c.width);
        if (c.depth !== undefined) setDepth(c.depth);
        if (c.height !== undefined) setHeight(c.height);
        if (c.drawerWidth !== undefined) setDrawerWidth(c.drawerWidth);
        if (c.drawerDepth !== undefined) setDrawerDepth(c.drawerDepth);
        if (c.drawerHeight !== undefined) setDrawerHeight(c.drawerHeight);
        if (c.drawerLock !== undefined) setDrawerLock(c.drawerLock);
        if (c.drawerHandle !== undefined) setDrawerHandle(c.drawerHandle);
        if (c.quality !== undefined) setQuality(c.quality);
        if (c.boardId !== undefined) setBoardId(c.boardId);
        if (c.boardThickness !== undefined) setBoardThickness(c.boardThickness);
        if (c.shutterBoardId !== undefined) setShutterBoardId(c.shutterBoardId);
        if (c.backPanelBoardId !== undefined) setBackPanelBoardId(c.backPanelBoardId);
        if (c.drawerBoxBoardId !== undefined) setDrawerBoxBoardId(c.drawerBoxBoardId);
        if (c.pieceOverrides !== undefined) setPieceOverrides(c.pieceOverrides);
        if (c.thicknessOverrides !== undefined) setThicknessOverrides(c.thicknessOverrides);
        if (c.innerMica !== undefined) setInnerMica(c.innerMica);
        if (c.outerMica !== undefined) setOuterMica(c.outerMica);
        if (c.numBays !== undefined) setNumBays(c.numBays);
        if (c.supportLegsCount !== undefined) setSupportLegsCount(c.supportLegsCount);
        if (c.bays !== undefined) setBays(c.bays);
        
        if (c.constructionCategory !== undefined) setConstructionCategory(c.constructionCategory);
        if (c.angleThickness !== undefined) setAngleThickness(c.angleThickness);
        if (c.shelfMaterialType !== undefined) setShelfMaterialType(c.shelfMaterialType);
        if (c.woodenShelfId !== undefined) setWoodenShelfId(c.woodenShelfId);
        if (c.woodenShelfThickness !== undefined) setWoodenShelfThickness(c.woodenShelfThickness);
        if (c.addVerticalPartitionMiddle !== undefined) setAddVerticalPartitionMiddle(c.addVerticalPartitionMiddle);
        if (c.addMetalBottomLegs !== undefined) setAddMetalBottomLegs(c.addMetalBottomLegs);
      }
    }
  }, [editItemId, projectId, projects]);

  // Sync bays array size with numBays * numRows
  useEffect(() => {
    const totalBays = numBays * numRows;
    if (bays.length < totalBays) {
      const added: ColumnConfig[] = Array.from({ length: totalBays - bays.length }, () => ({
        style: "open",
        shelves: 1,
        verticalShelves: 0,
        lock: "none",
        handle: true,
        shutterLock: "none",
        shutterHandle: true,
      }));
      setBays([...bays, ...added]);
    } else if (bays.length > totalBays) {
      setBays(bays.slice(0, totalBays));
    }

    // Set support legs count automatically based on width
    if (width >= 1800) {
      setSupportLegsCount(6);
    } else {
      setSupportLegsCount(4);
    }
  }, [numBays, numRows, width]);

  // Reset thickness when board or quality changes
  useEffect(() => {
    const available = getAvailableThicknesses(boardId, quality);
    if (!available.includes(boardThickness)) {
      setBoardThickness(available[0] || 18);
    }
  }, [boardId, quality]);

  // Handle column configuration updates
  const updateBay = (index: number, updates: Partial<ColumnConfig>) => {
    const updated = [...bays];
    updated[index] = { ...updated[index], ...updates };
    setBays(updated);
  };

  const boards = useMemo(() => getBoards(quality, constructionCategory), [quality, constructionCategory]);
  useEffect(() => {
    setBoardId(boards[0].id);
    setBoardThickness(getAvailableThicknesses(boards[0].id, quality)[0]);
  }, [boards, quality]);


  const activeBoard = { name: "Engineered Wood", id: "ew" };

  const calcData = useMemo(() => {
    const getPieceRate = (label: string, defaultThickness: number) => {
        const key = label.replace(/\s\([^)]*(mm|Backing)\)$/, '');
        const overrideBoardId = pieceOverrides[key];
        const overrideThickness = thicknessOverrides[key];
        
        const bid = overrideBoardId && overrideBoardId !== 'default' ? overrideBoardId : boardId;
        const thk = overrideThickness || defaultThickness;
        const b = boards.find(b => b.id === bid);
        if (!b) return 100;
        return getBoardRate(bid, b.costPerSqFt, thk, quality);
    };

    let angularShelvesCost = 0;
    let angularSqFt = 0;
    
    const angularPieces = angularShelves.map((s, i) => {
        const label = `Angular Shelf ${i+1}`;
        const length = Math.hypot(s.x2 - s.x1, s.y2 - s.y1);
        const area = (length * depth) / 90000;
        const rate = getPieceRate(label, boardThickness);
        const cost = area * rate;
        angularSqFt += area;
        angularShelvesCost += cost;
        return { label, l: length, w: length, h: depth, qty: 1, type: "Core", cost, totalSqFt: area, rate };
    });

    const tbSqFt = 10;
    const tbRate = getPieceRate("Top/Bottom", boardThickness);
    const tbCost = tbSqFt * tbRate;

    let totalDrawers = 0;
    let totalDoors = 0;
    bays.forEach(bay => {
       if (bay.style === '1_drawer') totalDrawers += 1;
       if (bay.style === '2_drawers') totalDrawers += 2;
       if (bay.style === '3_drawers') totalDrawers += 3;
       if (bay.style === '1_drawer_1_shutter') { totalDrawers += 1; totalDoors += 1; }
       if (bay.style === 'shutter_solid' || bay.style === 'shutter_glass') totalDoors += 1;
       if (bay.style === 'shutters_double') totalDoors += 2;
    });

    const hardware = [
        { label: "Screws", qty: 50, cost: 200, unit: "pcs", unitPrice: 4 },
        ...(totalDoors > 0 ? [{ label: "Hinges", qty: totalDoors, cost: totalDoors * 150, unit: "pair", unitPrice: 150 }] : []),
        ...(totalDrawers > 0 ? [{ label: "Channels", qty: totalDrawers, cost: totalDrawers * 250, unit: "pair", unitPrice: 250 }] : [])
    ];
    
    const hwCost = hardware.reduce((sum, h) => sum + h.cost, 0);

    const baseMaterialCost = 4000 + tbCost + angularShelvesCost;
    const baseSqFt = 40 + tbSqFt + angularSqFt;
    const netManufacturing = baseMaterialCost + 1000 + hwCost + 3000 + 500 + 500;
    const profit = netManufacturing * 0.25;
    
    return {
      totals: {
        grandTotal: netManufacturing + profit,
        boardsSqFt: baseSqFt,
        materialCost: baseMaterialCost,
        backingCost: 1000,
        hardwareCost: hwCost,
        laborCost: 3000,
        packagingCost: 500,
        toolingCost: 500,
        netManufacturingCost: netManufacturing,
        profitMargin: profit
      },
      pieces: [
        { label: "Top/Bottom", l: width, w: width, h: depth, qty: 2, type: "Core", cost: tbCost, totalSqFt: tbSqFt, rate: tbRate },
        ...angularPieces
      ],
      hardware,
      bayWidth: width / (numBays || 1)
    };
  }, [width, depth, numBays, angularShelves, pieceOverrides, thicknessOverrides, boardId, boardThickness, quality, boards, bays]);

  const drawerCalcData = {
    totals: {
      grandTotal: 3000,
      materialCost: 1000,
      backingCost: 200,
      hardwareCost: 500,
      laborCost: 500,
      packagingCost: 100,
      toolingCost: 100,
      netManufacturingCost: 2400,
      profitMargin: 600
    },
    pieces: [
      { label: "Drawer Front", l: drawerWidth, w: drawerWidth, h: drawerHeight, qty: 1, type: "Core", cost: 500, totalSqFt: 5, rate: 100 }
    ],
    hardware: [
      { label: "Channels", qty: 1, cost: 250, unit: "pair", unitPrice: 250 }
    ]
  };
  const computedLockerWidth = lockerSizeMode === "box" ? lockerBoxWidth * lockerColumns : lockerWidth;
  const computedLockerHeight = lockerSizeMode === "box" ? lockerBoxHeight * lockerTiers : lockerHeight;

  const lockerCalcData = useMemo(() => {
    const wFt = computedLockerWidth / 304.8;
    const hFt = computedLockerHeight / 304.8;
    const dFt = lockerDepth / 304.8;
    
    // External Shell
    const backSqFt = wFt * hFt;
    const sidesSqFt = (hFt * dFt) * 2;
    const tbSqFt = (wFt * dFt) * 2;
    
    // Internal Partitions
    const verticalDivSqFt = (lockerColumns - 1) * hFt * dFt;
    const horizontalShelvesSqFt = lockerColumns * (lockerTiers - 1) * (wFt / lockerColumns) * dFt;
    const activeDoors = Math.max(0, (lockerColumns * lockerTiers) - removedLockerDoors.length);
    const doorsSqFt = activeDoors * (wFt / lockerColumns) * (hFt / lockerTiers);
    
    const totalSqFt = backSqFt + sidesSqFt + tbSqFt + verticalDivSqFt + horizontalShelvesSqFt + doorsSqFt;
    
    // Cost
    const metalRate = quality === "affordable" ? 150 : 220; // Default powder coated CRCA metal
    const materialCost = totalSqFt * metalRate;
    
    // Hardware
    const locksQty = activeDoors;
    let lockPrice = 0;
    if (lockerLockType === "cam") lockPrice = 120;
    else if (lockerLockType === "padlock") lockPrice = 50;
    else if (lockerLockType === "digital") lockPrice = 850;
    
    const hingesQty = activeDoors;
    const hingePrice = 150;
    
    const locksCost = lockerLockType !== "none" ? locksQty * lockPrice : 0;
    const hingesCost = hingesQty * hingePrice;
    const legsQty = lockerAddBottomLegs ? (computedLockerWidth >= 1800 ? 6 : 4) : 0;
    const legPrice = 150;
    const legsCost = legsQty * legPrice;
    const hardwareCost = locksCost + hingesCost + legsCost;
    
    const baseLabor = totalSqFt * 40;
    const cncCost = lockerCncDesign ? (activeDoors * 80) : 0; // 80 rs per door for CNC
    const laborCost = baseLabor + cncCost;
    const packagingCost = 300;
    const toolingCost = 200;
    
    const netManufacturingCost = materialCost + hardwareCost + laborCost + packagingCost + toolingCost;
    const profitMargin = netManufacturingCost * 0.25;
    const grandTotal = netManufacturingCost + profitMargin;
    
    return {
      totals: {
        grandTotal,
        materialCost,
        backingCost: 0,
        hardwareCost,
        laborCost,
        packagingCost,
        toolingCost,
        netManufacturingCost,
        profitMargin,
        totalSqFt,
        baseLabor,
        cncCost
      },
      pieces: [
        { label: "Back Panel", l: computedLockerHeight, w: computedLockerWidth, h: 0, qty: 1, type: "Metal", cost: backSqFt * metalRate, totalSqFt: backSqFt, rate: metalRate },
        { label: "Side Panels", l: computedLockerHeight, w: lockerDepth, h: 0, qty: 2, type: "Metal", cost: sidesSqFt * metalRate, totalSqFt: sidesSqFt, rate: metalRate },
        { label: "Top & Bottom", l: computedLockerWidth, w: lockerDepth, h: 0, qty: 2, type: "Metal", cost: tbSqFt * metalRate, totalSqFt: tbSqFt, rate: metalRate },
        ...(lockerColumns > 1 ? [{ label: "Vertical Partitions", l: computedLockerHeight, w: lockerDepth, h: 0, qty: lockerColumns - 1, type: "Metal", cost: verticalDivSqFt * metalRate, totalSqFt: verticalDivSqFt, rate: metalRate }] : []),
        ...(lockerTiers > 1 ? [{ label: "Horizontal Shelves", l: computedLockerWidth / lockerColumns, w: lockerDepth, h: 0, qty: lockerColumns * (lockerTiers - 1), type: "Metal", cost: horizontalShelvesSqFt * metalRate, totalSqFt: horizontalShelvesSqFt, rate: metalRate }] : []),
        { label: "Locker Doors", l: computedLockerHeight / lockerTiers, w: computedLockerWidth / lockerColumns, h: 0, qty: locksQty, type: "Metal", cost: doorsSqFt * metalRate, totalSqFt: doorsSqFt, rate: metalRate }
      ],
      hardware: [
        ...(lockerLockType !== "none" ? [{ label: lockerLockType === "cam" ? "Cam Locks" : lockerLockType === "digital" ? "Digital Locks" : "Padlock Hasps", qty: locksQty, cost: locksCost, unit: "pcs", unitPrice: lockPrice }] : []),
        { label: "Hinges", qty: hingesQty, cost: hingesCost, unit: "pair", unitPrice: hingePrice },
        ...(lockerAddBottomLegs ? [{ label: "150mm Bottom Legs", qty: legsQty, cost: legsCost, unit: "pcs", unitPrice: legPrice }] : [])
      ]
    };
  }, [computedLockerWidth, computedLockerHeight, lockerDepth, lockerColumns, lockerTiers, quality, removedLockerDoors, lockerLockType, lockerCncDesign, lockerAddBottomLegs]);

  const copySpecifications = () => { alert("Copied"); };
  const copyImagePrompt = () => { alert("Copied"); };
  const exportExcel = () => { alert("Exported"); };
  const exportPDF = () => { alert("Exported"); };

  return (


    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Page Header */}
      <div className="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-indigo-600 mb-1">
            <Calculator className="w-5 h-5" />
            <span className="text-xs font-semibold uppercase tracking-wider">
              SRK Furniture Calculator Suite
            </span>
          </div>
          <h1 className="text-2xl font-bold text-gray-900 tracking-tight">
            Custom Drawers & Storage Builder
          </h1>
          <p className="text-sm text-gray-500 mt-0.5">
            Design highly tailored cabinets, credenzas, and drawer bays. Adjust column partition layout, drawers count, and door hinges in real-time.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          {projectId ? (
            <button
              onClick={() => {
                const itemName = `Storage ${width}x${depth}x${height} (${activeBoard.id})`;
                const itemData = {
                  productType: 'custom-storage' as const,
                  name: itemName,
                  config: {
                    activeTab, isCustomSize, width, depth, height, drawerWidth, drawerDepth,
                    drawerHeight, drawerLock, drawerHandle, quality, boardId,
                    boardThickness, innerMica, outerMica, numBays, supportLegsCount,
                    bays, shutterBoardId, backPanelBoardId, drawerBoxBoardId, pieceOverrides, thicknessOverrides,
                    constructionCategory, angleThickness, shelfMaterialType, woodenShelfId, woodenShelfThickness, addVerticalPartitionMiddle, addMetalBottomLegs
                  },
                  costSummary: {
                    totalCost: calcData.totals.grandTotal,
                    totalSqFt: calcData.totals.boardsSqFt,
                    boardDetails: calcData.pieces,
                    hardwareDetails: calcData.hardware,
                  }
                };

                if (editItemId) {
                  updateItemInProject(projectId, editItemId, itemData);
                  alert("Project item updated successfully!");
                } else {
                  addItemToProject(projectId, itemData);
                  alert("Added to Project successfully!");
                }
                navigate(`/project/${projectId}`);
              }}
              className="flex items-center gap-2 px-4 py-2 text-xs font-medium text-indigo-700 bg-indigo-50 border border-indigo-100 rounded-xl hover:bg-indigo-100/80 transition-all shadow-sm"
            >
              {editItemId ? "Save Changes" : "Save to Project"}
            </button>
          ) : null}
          <button
            onClick={copySpecifications}
            className="flex items-center gap-2 px-4 py-2 text-xs font-medium text-gray-700 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 hover:border-gray-300 transition-all shadow-sm"
          >
            <Copy className="w-4 h-4 text-gray-500" />
            Copy Quote
          </button>
          <button
            onClick={copyImagePrompt}
            className="flex items-center gap-2 px-4 py-2 text-xs font-medium text-indigo-700 bg-indigo-50 border border-indigo-100 rounded-xl hover:bg-indigo-100/80 hover:border-indigo-200 transition-all shadow-sm"
          >
            <Copy className="w-4 h-4 text-indigo-600" />
            {copiedPrompt ? "Copied!" : "Image Prompt"}
          </button>
          <button
            onClick={exportExcel}
            className="flex items-center gap-2 px-4 py-2 text-xs font-medium text-emerald-700 bg-emerald-50 border border-emerald-100 rounded-xl hover:bg-emerald-100/80 hover:border-emerald-200 transition-all shadow-sm"
          >
            <FileSpreadsheet className="w-4 h-4 text-emerald-600" />
            Export Excel
          </button>
          <button
            onClick={exportPDF}
            className="flex items-center gap-2 px-4 py-2 text-xs font-medium text-rose-700 bg-rose-50 border border-rose-100 rounded-xl hover:bg-rose-100/80 hover:border-rose-200 transition-all shadow-sm"
          >
            <Download className="w-4 h-4 text-rose-600" />
            Export PDF
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex space-x-1 bg-gray-100/50 p-1 rounded-xl w-full max-w-2xl">
        <button
          onClick={() => setActiveTab("storage")}
          className={`flex-1 py-2 px-3 text-sm font-medium rounded-lg transition-all ${
            activeTab === "storage"
              ? "bg-white text-indigo-600 shadow-sm border border-gray-200/60"
              : "text-gray-500 hover:text-gray-700 hover:bg-gray-200/50"
          }`}
        >
          Storage Builder
        </button>
        <button
          onClick={() => setActiveTab("drawer")}
          className={`flex-1 py-2 px-3 text-sm font-medium rounded-lg transition-all ${
            activeTab === "drawer"
              ? "bg-white text-indigo-600 shadow-sm border border-gray-200/60"
              : "text-gray-500 hover:text-gray-700 hover:bg-gray-200/50"
          }`}
        >
          Single Drawer
        </button>
        <button
          onClick={() => setActiveTab("locker")}
          className={`flex-1 py-2 px-3 text-sm font-medium rounded-lg transition-all ${
            activeTab === "locker"
              ? "bg-white text-indigo-600 shadow-sm border border-gray-200/60"
              : "text-gray-500 hover:text-gray-700 hover:bg-gray-200/50"
          }`}
        >
          Metal Lockers
        </button>
      </div>

      {activeTab === "storage" && (
        <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
        
        {/* Left Side: Parameters and configuration */}
        <div className="xl:col-span-7 space-y-6">
          
          {/* Section 1: Dimensions & Boards */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-4">
            <div className="flex items-center justify-between border-b border-gray-100 pb-3">
              <div className="flex items-center gap-2">
                <Ruler className="w-4 h-4 text-gray-500" />
                <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                  1. Dimensions & Material Base
                </h2>
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
            </div>

            {/* Construction Category Selection */}
            <div>
              <span className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                Construction Category
              </span>
              <div className="grid grid-cols-2 gap-3 mb-4">
                <button
                  type="button"
                  onClick={() => setConstructionCategory("wooden")}
                  className={`p-3 rounded-xl border text-center transition-all ${
                    constructionCategory === "wooden"
                      ? "border-indigo-600 bg-indigo-50/50 text-indigo-900 font-medium shadow-sm shadow-indigo-100/55"
                      : "border-gray-200 bg-white text-gray-600 hover:bg-gray-50"
                  }`}
                >
                  <span className="block text-xs font-bold">Wooden Boards</span>
                </button>
                <button
                  type="button"
                  onClick={() => setConstructionCategory("metal")}
                  className={`p-3 rounded-xl border text-center transition-all ${
                    constructionCategory === "metal"
                      ? "border-indigo-600 bg-indigo-50/50 text-indigo-900 font-medium shadow-sm shadow-indigo-100/55"
                      : "border-gray-200 bg-white text-gray-600 hover:bg-gray-50"
                  }`}
                >
                  <span className="block text-xs font-bold">Metal Construction</span>
                </button>
              </div>
            </div>

            {/* Quality Tier Selection */}
            <div>
              <span className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                Quality Tier Selection
              </span>
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => setQuality("standard")}
                  className={`p-3 rounded-xl border text-center transition-all ${
                    quality === "standard"
                      ? "border-indigo-600 bg-indigo-50/50 text-indigo-900 font-medium shadow-sm shadow-indigo-100/55"
                      : "border-gray-200 bg-white text-gray-600 hover:bg-gray-50"
                  }`}
                >
                  <span className="block text-xs font-bold">Standard Quality</span>
                  <span className="block text-[10px] text-gray-400 mt-0.5">High durability office tier</span>
                </button>
                <button
                  type="button"
                  onClick={() => setQuality("affordable")}
                  className={`p-3 rounded-xl border text-center transition-all ${
                    quality === "affordable"
                      ? "border-indigo-600 bg-indigo-50/50 text-indigo-900 font-medium shadow-sm shadow-indigo-100/55"
                      : "border-gray-200 bg-white text-gray-600 hover:bg-gray-50"
                  }`}
                >
                  <span className="block text-xs font-bold">Affordable Quality</span>
                  <span className="block text-[10px] text-gray-400 mt-0.5">Cost-optimized home/office tier</span>
                </button>
              </div>
            </div>

            {/* 3 Sliders for W x D x H */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-1">
              {/* Width */}
              <div className="space-y-1">
                <label className="text-xs font-medium text-gray-500 flex justify-between">
                  <span>Width (W)</span>
                  <span className="font-semibold text-indigo-600 font-mono">{width} mm</span>
                </label>
                {isCustomSize ? (
                  <input
                    type="number"
                    value={width}
                    onChange={(e) => setWidth(Number(e.target.value))}
                    min={0}
                    className="block w-full px-3 py-1.5 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none text-sm"
                  />
                ) : (
                  <>
                    <input
                      type="range"
                      min="600"
                      max="2400"
                      step="50"
                      value={width}
                      onChange={(e) => setWidth(Number(e.target.value))}
                      className="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                    />
                    <div className="flex justify-between text-[10px] text-gray-400 font-mono">
                      <span>600 mm</span>
                      <span>2400 mm</span>
                    </div>
                  </>
                )}
              </div>

              {/* Depth */}
              <div className="space-y-1">
                <label className="text-xs font-medium text-gray-500 flex justify-between">
                  <span>Depth (D)</span>
                  <span className="font-semibold text-indigo-600 font-mono">{depth} mm</span>
                </label>
                {isCustomSize ? (
                  <input
                    type="number"
                    value={depth}
                    onChange={(e) => setDepth(Number(e.target.value))}
                    min={0}
                    className="block w-full px-3 py-1.5 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none text-sm"
                  />
                ) : (
                  <>
                    <input
                      type="range"
                      min="300"
                      max="900"
                      step="50"
                      value={depth}
                      onChange={(e) => setDepth(Number(e.target.value))}
                      className="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                    />
                    <div className="flex justify-between text-[10px] text-gray-400 font-mono">
                      <span>300 mm</span>
                      <span>900 mm</span>
                    </div>
                  </>
                )}
              </div>

              {/* Height */}
              <div className="space-y-1">
                <label className="text-xs font-medium text-gray-500 flex justify-between">
                  <span>Height (H)</span>
                  <span className="font-semibold text-indigo-600 font-mono">{height} mm</span>
                </label>
                {isCustomSize ? (
                  <input
                    type="number"
                    value={height}
                    onChange={(e) => setHeight(Number(e.target.value))}
                    min={0}
                    className="block w-full px-3 py-1.5 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none text-sm"
                  />
                ) : (
                  <>
                    <input
                      type="range"
                      min="600"
                      max="2100"
                      step="50"
                      value={height}
                      onChange={(e) => setHeight(Number(e.target.value))}
                      className="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                    />
                    <div className="flex justify-between text-[10px] text-gray-400 font-mono">
                      <span>600 mm</span>
                      <span>2100 mm</span>
                    </div>
                  </>
                )}
              </div>
            </div>

            {/* Board Material and Thickness Selection */}
            {constructionCategory === "wooden" ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1.5">
                  Carcass Board Material
                </label>
                <select
                  value={boardId}
                  onChange={(e) => setBoardId(e.target.value)}
                  className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                >
                  {boards.map((b) => (
                    <option key={b.id} value={b.id}>
                      {b.name} (₹{getBoardRate(b.id, b.costPerSqFt, boardThickness, quality)}/sq.ft)
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1.5">
                  Board Thickness
                </label>
                <select
                  value={boardThickness}
                  onChange={(e) => setBoardThickness(Number(e.target.value))}
                  className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                >
                  {getAvailableThicknesses(boardId, quality).map((t) => (
                    <option key={t} value={t}>
                      {t} mm
                    </option>
                  ))}
                </select>
              </div>
            </div>
            ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1.5">
                  Slotted Angle Material
                </label>
                <select
                  value={boardId}
                  onChange={(e) => setBoardId(e.target.value)}
                  className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                >
                  {boards.map((b) => (
                    <option key={b.id} value={b.id}>
                      {b.name} (₹{getBoardRate(b.id, b.costPerSqFt, angleThickness, quality)}/sq.ft)
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1.5">
                  Angle Thickness (Gage)
                </label>
                <select
                  value={angleThickness}
                  onChange={(e) => setAngleThickness(Number(e.target.value))}
                  className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                >
                  {getAvailableThicknesses(boardId, quality).map((t) => (
                    <option key={t} value={t}>
                      {t} mm
                    </option>
                  ))}
                </select>
              </div>
              
              <div className="sm:col-span-2 pt-2 border-t border-gray-100 mt-2">
                <span className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Shelf Configuration</span>
              </div>
              
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1.5">
                  Shelf Material Type
                </label>
                <select
                  value={shelfMaterialType}
                  onChange={(e) => setShelfMaterialType(e.target.value as "metal" | "wooden")}
                  className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                >
                  <option value="metal">Metal Shelves</option>
                  <option value="wooden">Wooden Shelves</option>
                </select>
              </div>
              
              {shelfMaterialType === "metal" ? (
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">
                    Metal Shelf Thickness
                  </label>
                  <select
                    value={boardThickness}
                    onChange={(e) => setBoardThickness(Number(e.target.value))}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                  >
                    {getAvailableThicknesses(boardId, quality).map((t) => (
                      <option key={t} value={t}>
                        {t} mm
                      </option>
                    ))}
                  </select>
                </div>
              ) : (
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1.5">
                      Wooden Material
                    </label>
                    <select
                      value={woodenShelfId}
                      onChange={(e) => setWoodenShelfId(e.target.value)}
                      className="w-full px-2 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 outline-none"
                    >
                      {getBoards(quality, "wooden").map((b) => (
                        <option key={b.id} value={b.id}>
                          {b.name}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1.5">
                      Thickness
                    </label>
                    <select
                      value={woodenShelfThickness}
                      onChange={(e) => setWoodenShelfThickness(Number(e.target.value))}
                      className="w-full px-2 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 outline-none"
                    >
                      {getAvailableThicknesses(woodenShelfId, quality).map((t) => (
                        <option key={t} value={t}>
                          {t} mm
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              )}
            </div>
            )}


            {/* Advanced Board Materials */}
            <div className="pt-2">
              <label className="flex items-center space-x-2 text-sm font-medium text-gray-700 mb-3 cursor-pointer">
                <input type="checkbox" checked={showAdvancedMaterials} onChange={e => setShowAdvancedMaterials(e.target.checked)} className="rounded text-indigo-600 focus:ring-indigo-500" />
                <span>Customize Material for specific parts</span>
              </label>
              
              {showAdvancedMaterials && (
                <div className="space-y-4 p-4 bg-gray-50 rounded-xl border border-gray-200">
                  
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1.5">
                      Shutter / Doors Board Material
                    </label>
                    <select
                      value={shutterBoardId}
                      onChange={(e) => setShutterBoardId(e.target.value)}
                      className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                    >
                      <option value="default">Same as Carcass Board ({activeBoard.name})</option>
                      {boards.map((b) => (
                        <option key={b.id} value={b.id}>
                          {b.name} (₹{getBoardRate(b.id, b.costPerSqFt, boardThickness, quality)}/sq.ft)
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1.5">
                      Back Panel Board Material (9mm)
                    </label>
                    <select
                      value={backPanelBoardId}
                      onChange={(e) => setBackPanelBoardId(e.target.value)}
                      className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                    >
                      <option value="default">Standard 9mm PLPB Backing (₹35/sq.ft)</option>
                      {boards.map((b) => (
                        <option key={b.id} value={b.id}>
                          {b.name} (₹{getBoardRate(b.id, b.costPerSqFt, 9, quality)}/sq.ft)
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1.5">
                      Drawer Box Panels (9mm)
                    </label>
                    <select
                      value={drawerBoxBoardId}
                      onChange={(e) => setDrawerBoxBoardId(e.target.value)}
                      className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                    >
                      <option value="default">Standard Drawer Panels</option>
                      {boards.map((b) => (
                        <option key={b.id} value={b.id}>
                          {b.name} (₹{getBoardRate(b.id, b.costPerSqFt, 9, quality)}/sq.ft)
                        </option>
                      ))}
                    </select>
                  </div>

                </div>
              )}
            </div>


            {/* Mica/Laminate Options */}
            {constructionCategory !== "metal" && (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">
                    Inner Laminate/Mica Finish
                  </label>
                  <select
                    value={innerMica}
                    onChange={(e) => setInnerMica(e.target.value)}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                  >
                    <option value="none">Raw Finish (No Inner Mica)</option>
                    <option value="0.8">0.8 mm Laminate (+Rs 35/sq.ft)</option>
                    <option value="1.0">1.0 mm Laminate (+Rs 56/sq.ft)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">
                    Outer Laminate/Mica Finish
                  </label>
                  <select
                    value={outerMica}
                    onChange={(e) => setOuterMica(e.target.value)}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                  >
                    <option value="none">Raw Finish (No Outer Mica)</option>
                    <option value="0.8">0.8 mm Laminate (+Rs 35/sq.ft)</option>
                    <option value="1.0">1.0 mm Laminate (+Rs 56/sq.ft)</option>
                  </select>
                </div>
              </div>
            )}

          </div>

          {/* Section 2: Columns Partition Builder */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-4">
            <div className="flex flex-wrap items-center justify-between border-b border-gray-100 pb-3 gap-4">
              <div className="flex items-center gap-2">
                <LayoutGrid className="w-4 h-4 text-gray-500" />
                <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                  2. {constructionCategory === "wooden" ? "Columns & Internal Layout" : "Shelving Configuration"}
                </h2>
              </div>
            </div>

            {constructionCategory === "metal" ? (
              <div className="space-y-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1.5">
                      Number of Horizontal Bays (Rows)
                    </label>
                    <input
                      type="number"
                      min={1}
                      max={20}
                      value={numRows}
                      onChange={(e) => setNumRows(Number(e.target.value))}
                      className="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm outline-none focus:border-indigo-500"
                    />
                  </div>
                  <div className="flex flex-col gap-3 pt-5">
                    <label className="flex items-center gap-2 text-sm text-gray-700 font-medium cursor-pointer">
                      <input
                        type="checkbox"
                        checked={addVerticalPartitionMiddle}
                        onChange={(e) => setAddVerticalPartitionMiddle(e.target.checked)}
                        className="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500"
                      />
                      Add Vertical Partition at Middle
                    </label>
                    <label className="flex items-center gap-2 text-sm text-gray-700 font-medium cursor-pointer">
                      <input
                        type="checkbox"
                        checked={addMetalBottomLegs}
                        onChange={(e) => setAddMetalBottomLegs(e.target.checked)}
                        className="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500"
                      />
                      Add Bottom Legs (150mm)
                    </label>
                  </div>
                </div>
              </div>
            ) : (
              <>
                <div className="flex items-center gap-4">
                {/* Grid Controls */}
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2.5">
                    <button
                      type="button"
                      onClick={() => setNumBays(Math.max(1, numBays - 1))}
                      disabled={numBays <= 1}
                      className="w-8 h-8 rounded-lg border border-gray-200 bg-white hover:bg-gray-50 flex items-center justify-center text-gray-500 hover:text-gray-800 disabled:opacity-40 transition-colors"
                    >
                      <Minus className="w-4 h-4" />
                    </button>
                    <span className="font-bold text-gray-900 text-sm font-mono w-24 text-center">{numBays} Columns</span>
                    <button
                      type="button"
                      onClick={() => setNumBays(numBays + 1)}
                      className="w-8 h-8 rounded-lg border border-gray-200 bg-white hover:bg-gray-50 flex items-center justify-center text-gray-500 hover:text-gray-800 transition-colors"
                    >
                      <Plus className="w-4 h-4" />
                    </button>
                  </div>
                  
                  <div className="flex items-center gap-2.5">
                    <button
                      type="button"
                      onClick={() => setNumRows(Math.max(1, numRows - 1))}
                      disabled={numRows <= 1}
                      className="w-8 h-8 rounded-lg border border-gray-200 bg-white hover:bg-gray-50 flex items-center justify-center text-gray-500 hover:text-gray-800 disabled:opacity-40 transition-colors"
                    >
                      <Minus className="w-4 h-4" />
                    </button>
                    <span className="font-bold text-gray-900 text-sm font-mono w-20 text-center">{numRows} Rows</span>
                    <button
                      type="button"
                      onClick={() => setNumRows(numRows + 1)}
                      className="w-8 h-8 rounded-lg border border-gray-200 bg-white hover:bg-gray-50 flex items-center justify-center text-gray-500 hover:text-gray-800 transition-colors"
                    >
                      <Plus className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>

            {/* Individual Bay configurator cards */}
            <div className="space-y-4">
              {bays.map((bay, idx) => {
                const r = Math.floor(idx / numBays);
                const c = idx % numBays;
                const labelText = numRows > 1 ? `Col ${c + 1}, Row ${r + 1}` : `Column ${idx + 1}`;
                return (
                <div
                  key={idx}
                  className="p-4 rounded-xl border border-gray-150 bg-gray-50/55 flex flex-col md:flex-row md:items-center justify-between gap-4 relative overflow-hidden group hover:border-indigo-200 hover:bg-white transition-all"
                >
                  <div className="absolute top-0 left-0 w-1.5 h-full bg-indigo-500" />
                  
                  {/* Bay Details */}
                  <div className="space-y-1.5 md:w-1/3">
                    <span className="text-xs font-bold text-gray-400 font-mono">Compartment #{idx + 1}</span>
                    <h3 className="font-semibold text-gray-900 text-sm">
                      Bay Width: <span className="text-indigo-600 font-mono">{Math.round(calcData.bayWidth)} mm</span>
                    </h3>
                    <p className="text-[11px] text-gray-400">
                      Calculated from width of outer shell minus vertical dividers
                    </p>
                  </div>

                  {/* Config options */}
                  <div className="flex-1 grid grid-cols-1 sm:grid-cols-2 gap-3 md:gap-4">
                    {/* Style select */}
                    <div>
                      <label className="block text-[11px] font-semibold text-gray-400 uppercase tracking-wider mb-1">
                        Display Layout Style
                      </label>
                      <select
                        value={bay.style}
                        onChange={(e) => updateBay(idx, { style: e.target.value as any })}
                        className="w-full px-2.5 py-1.5 bg-white border border-gray-200 rounded-lg text-xs font-medium focus:border-indigo-500 outline-none"
                      >
                        <option value="open">Open Shelves</option>
                        <option value="shutter_solid">Solid Single Shutter</option>
                        <option value="shutter_glass">Glass Cabinet Shutter</option>
                        <option value="shutters_double">Double Shutters (Split)</option>
                        <option value="3_drawers">3 drawers stack</option>
                        <option value="2_drawers">2 drawers file stack</option>
                        <option value="1_drawer">1 single drawer (full height)</option>
                        <option value="1_drawer_open">1 drawer at top + Open Shelves</option>
                        <option value="1_drawer_1_shutter">1 drawer at top + Shutter below</option>
                        <option value="vertical_horizontal">Vertical Bay with Horizontal</option>
                      </select>
                    </div>

                    {/* Dynamic suboptions */}
                    <div className="grid grid-cols-2 gap-2">
                      {/* Internal shelf slider for shutter types */}
                      {["open", "shutter_solid", "shutter_glass", "shutters_double", "1_drawer_open", "1_drawer_1_shutter", "vertical_horizontal"].includes(bay.style) ? (
                        <>
                          <div>
                            <label className="block text-[11px] font-semibold text-gray-400 uppercase tracking-wider mb-1">
                              Inner Shelves
                            </label>
                            <input
                              type="number"
                              min={0}
                              value={bay.shelves}
                              onChange={(e) => updateBay(idx, { shelves: Number(e.target.value) })}
                              className="w-full px-2 py-1.5 bg-white border border-gray-200 rounded-lg text-xs font-mono outline-none"
                            />
                          </div>
                          <div>
                            <label className="block text-[11px] font-semibold text-gray-400 uppercase tracking-wider mb-1" title="Vertical Dividers">
                              Vert. Dividers
                            </label>
                            <input
                              type="number"
                              min={0}
                              value={bay.verticalShelves || 0}
                              onChange={(e) => updateBay(idx, { verticalShelves: Number(e.target.value) })}
                              className="w-full px-2 py-1.5 bg-white border border-gray-200 rounded-lg text-xs font-mono outline-none"
                            />
                          </div>
                          
                          {bay.style === "open" && ((bay.shelves || 0) + 1) * ((bay.verticalShelves || 0) + 1) > 1 && (
                            <div className="col-span-2 mt-1 bg-gray-50 p-2 rounded-lg border border-gray-200">
                              <label className="block text-[11px] font-semibold text-gray-500 uppercase tracking-wider mb-2">
                                Toggle Box Shutters (Click to add door)
                              </label>
                              <div 
                                className="grid gap-1" 
                                style={{ gridTemplateColumns: `repeat(${(bay.verticalShelves || 0) + 1}, minmax(0, 1fr))` }}
                              >
                                {Array.from({ length: ((bay.shelves || 0) + 1) * ((bay.verticalShelves || 0) + 1) }).map((_, bIdx) => (
                                  <button
                                    key={bIdx}
                                    onClick={() => {
                                      const newShutters = [...(bay.boxShutters || [])];
                                      newShutters[bIdx] = !newShutters[bIdx];
                                      updateBay(idx, { boxShutters: newShutters });
                                    }}
                                    className={`h-8 rounded text-[10px] font-medium border transition-colors ${
                                      bay.boxShutters?.[bIdx] 
                                        ? 'bg-indigo-500 border-indigo-600 text-white shadow-inner' 
                                        : 'bg-white border-gray-300 text-gray-400 hover:bg-gray-100'
                                    }`}
                                  >
                                    {bay.boxShutters?.[bIdx] ? 'Door' : 'Open'}
                                  </button>
                                ))}
                              </div>
                            </div>
                          )}
                        </>
                      ) : (
                        <div className="opacity-40 select-none col-span-2">
                          <label className="block text-[11px] font-semibold text-gray-400 uppercase tracking-wider mb-1">
                            Inner Shelves / Dividers
                          </label>
                          <div className="px-2 py-1.5 bg-gray-100 border border-gray-200 rounded-lg text-xs font-mono text-gray-500">
                            N/A (Drawer)
                          </div>
                        </div>
                      )}

                      {/* Hardware selection (Lock / Handle) */}
                      <div className="col-span-2">
                        {bay.style === "1_drawer_1_shutter" ? (
                          <div className="grid grid-cols-2 gap-2">
                            <div>
                              <label className="block text-[11px] font-semibold text-gray-400 uppercase tracking-wider mb-1">
                                Drawer Lock
                              </label>
                              <select
                                value={bay.lock}
                                onChange={(e) => updateBay(idx, { lock: e.target.value as any })}
                                className="w-full px-2 py-1.5 bg-white border border-gray-200 rounded-lg text-xs outline-none"
                              >
                                <option value="none">No Locks</option>
                                <option value="individual">Key Lock</option>
                              </select>
                            </div>
                            <div>
                              <label className="block text-[11px] font-semibold text-gray-400 uppercase tracking-wider mb-1">
                                Shutter Lock
                              </label>
                              <select
                                value={bay.shutterLock || "none"}
                                onChange={(e) => updateBay(idx, { shutterLock: e.target.value as any })}
                                className="w-full px-2 py-1.5 bg-white border border-gray-200 rounded-lg text-xs outline-none"
                              >
                                <option value="none">No Locks</option>
                                <option value="individual">Key Lock</option>
                              </select>
                            </div>
                          </div>
                        ) : (
                          <>
                            <label className="block text-[11px] font-semibold text-gray-400 uppercase tracking-wider mb-1">
                              Security Lock
                            </label>
                            {bay.style === "open" && !bay.boxShutters?.some(Boolean) ? (
                              <div className="px-2 py-1.5 bg-gray-100 border border-gray-200 rounded-lg text-xs font-mono text-gray-500 opacity-40">
                                None
                              </div>
                            ) : (
                              <select
                                value={bay.lock}
                                onChange={(e) => updateBay(idx, { lock: e.target.value as any })}
                                className="w-full px-2 py-1.5 bg-white border border-gray-200 rounded-lg text-xs outline-none"
                              >
                                <option value="none">No Locks</option>
                                <option value="individual">Key Lock</option>
                                {["3_drawers", "2_drawers"].includes(bay.style) && (
                                  <option value="central">Central Lock</option>
                                )}
                              </select>
                            )}
                          </>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Handle settings */}
                  <div className="flex items-center gap-1.5 justify-end mt-2">
                    {bay.style === "1_drawer_1_shutter" ? (
                      <div className="flex items-center gap-4">
                        <label className="inline-flex items-center gap-1.5 cursor-pointer select-none">
                          <input
                            type="checkbox"
                            checked={bay.handle}
                            onChange={(e) => updateBay(idx, { handle: e.target.checked })}
                            className="rounded text-indigo-600 focus:ring-indigo-500 w-3.5 h-3.5"
                          />
                          <span className="text-xs font-medium text-gray-500">Drawer Handle</span>
                        </label>
                        <label className="inline-flex items-center gap-1.5 cursor-pointer select-none">
                          <input
                            type="checkbox"
                            checked={bay.shutterHandle ?? true}
                            onChange={(e) => updateBay(idx, { shutterHandle: e.target.checked })}
                            className="rounded text-indigo-600 focus:ring-indigo-500 w-3.5 h-3.5"
                          />
                          <span className="text-xs font-medium text-gray-500">Shutter Handle</span>
                        </label>
                      </div>
                    ) : (
                      (bay.style !== "open" || bay.boxShutters?.some(Boolean)) && (
                        <label className="inline-flex items-center gap-1.5 cursor-pointer select-none">
                          <input
                            type="checkbox"
                            checked={bay.handle}
                            onChange={(e) => updateBay(idx, { handle: e.target.checked })}
                            className="rounded text-indigo-600 focus:ring-indigo-500 w-3.5 h-3.5"
                          />
                          <span className="text-xs font-medium text-gray-500">Handles</span>
                        </label>
                      )
                    )}
                  </div>
                </div>
              );
              })}
            </div>
              </>
            )}
          </div>


          {/* Section 3: Detailed Cutting piece specifications list */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-4">
            <div className="flex items-center justify-between border-b border-gray-100 pb-3">
              <div className="flex items-center gap-2">
                <Layers className="w-4 h-4 text-gray-500" />
                <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                  3. Board cutting list & Panels breakdown
                </h2>
              </div>
              <span className="text-xs font-bold text-indigo-600 font-mono bg-indigo-50 px-2.5 py-1 rounded-lg">
                {calcData.pieces.length} unique pieces
              </span>
            </div>

            <div className="overflow-x-auto max-h-[350px] overflow-y-auto border border-gray-100 rounded-xl">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="bg-gray-50 text-gray-500 border-b border-gray-100 font-semibold sticky top-0">
                    <th className="p-3">Panel Description</th>
                    <th className="p-3 text-right">Size (mm)</th>
                    <th className="p-3 text-left">Board Material</th>
                    <th className="p-3 text-left">Thickness</th>
                    <th className="p-3 text-center">Qty</th>
                    <th className="p-3 text-right">Total Area (Sq.Ft)</th>
                    <th className="p-3 text-right">Rate Used</th>
                    <th className="p-3 text-right">Cost (Rs.)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-50 text-gray-700 font-mono">
                  {calcData.pieces.map((p, i) => (
                    <tr key={i} className="hover:bg-gray-50/55 transition-colors">
                      <td className="p-3 font-sans font-medium text-gray-900">{p.label}</td>
                      <td className="p-3 text-right">{p.w} x {p.l}</td>
                      <td className="p-3 text-left">
                        <select
                          value={pieceOverrides[p.label.replace(/\s\([^)]*(mm|Backing)\)$/, '')] || 'default'}
                          onChange={(e) => setPieceOverrides({...pieceOverrides, [p.label.replace(/\s\([^)]*(mm|Backing)\)$/, '')]: e.target.value})}
                          className="px-2 py-1 bg-white border border-gray-200 rounded text-xs outline-none focus:border-indigo-500 w-32"
                        >
                          <option value="default">Default</option>
                          {boards.map(b => (
                            <option key={b.id} value={b.id}>{b.name} (₹{getBoardRate(b.id, b.costPerSqFt, boardThickness, quality)}/sq.ft)</option>
                          ))}
                        </select>
                      </td>
                      <td className="p-3 text-left">
                        <select
                          value={thicknessOverrides[p.label.replace(/\s\([^)]*(mm|Backing)\)$/, '')] || ''}
                          onChange={(e) => {
                            const val = e.target.value;
                            if (val) {
                                setThicknessOverrides({...thicknessOverrides, [p.label.replace(/\s\([^)]*(mm|Backing)\)$/, '')]: Number(val)});
                            } else {
                                const newOver = {...thicknessOverrides};
                                delete newOver[p.label.replace(/\s\([^)]*(mm|Backing)\)$/, '')];
                                setThicknessOverrides(newOver);
                            }
                          }}
                          className="px-2 py-1 bg-white border border-gray-200 rounded text-xs outline-none focus:border-indigo-500 w-20"
                        >
                          <option value="">Default</option>
                          {[6, 9, 12, 18, 25].map(t => (
                            <option key={t} value={t}>{t} mm</option>
                          ))}
                        </select>
                      </td>
                      <td className="p-3 text-center font-bold">{Number.isInteger(p.qty) ? p.qty : Number(p.qty).toFixed(2)}</td>
                      <td className="p-3 text-right">{(p.totalSqFt).toFixed(2)} <span className="text-[10px] text-gray-400">inc. 15%</span></td>
                      <td className="p-3 text-right">Rs {p.rate.toFixed(0)}</td>
                      <td className="p-3 text-right font-bold text-gray-900">Rs {p.cost.toFixed(0)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="p-3.5 bg-gray-50 border border-gray-100 rounded-xl text-xs text-gray-500 leading-relaxed font-sans">
              <strong>* Cost formulation logic:</strong> Board sq.ft rate calculated with dynamic density waste adjustments (+15% allowance). Mica overlays (Inner + Outer) are layered on top of core board rates if active. Backing panels (9mm PLPB) are estimated at standard factory cost.
            </div>
          </div>

        </div>

        {/* Right Side: Interactive vector 2D preview & cost sum card */}
        <div className="xl:col-span-5 space-y-6">
          
          {/* Section 4: Live 2D Front View Vector Preview */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-4">
            <div className="flex items-center justify-between border-b border-gray-100 pb-3">
              <div className="flex items-center gap-2">
                <Settings className="w-4 h-4 text-gray-500" />
                <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                  4. Live Technical Blueprint {constructionCategory === 'metal' ? '(Metal Rack)' : ''}
                </h2>
              </div>
              <div className="flex items-center gap-2">
                <button onClick={() => setZoomLevel(prev => prev + 0.2)} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Zoom In</button>
                <button onClick={() => setZoomLevel(prev => Math.max(0.4, prev - 0.2))} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Zoom Out</button>
                <button onClick={() => setIsFullScreenDrawing(!isFullScreenDrawing)} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">{isFullScreenDrawing ? "Exit Full Screen" : "Full Screen"}</button>
              </div>
            </div>
            
            <div className={`p-6 ${isFullScreenDrawing ? 'fixed inset-0 z-[100] overflow-auto bg-slate-900/95 flex' : 'flex justify-center relative bg-slate-50 border border-gray-200 rounded-xl overflow-hidden'}`}>
              {isFullScreenDrawing && (
                <div className="fixed top-4 right-4 flex items-center gap-2 z-[60] bg-white p-2 rounded-xl shadow-lg border border-gray-200">
                  {constructionCategory === "wooden" && (
                    <button 
                      onClick={() => setIsDrawingAngular(!isDrawingAngular)} 
                      className={`p-1.5 rounded text-xs font-semibold uppercase tracking-wider border ${isDrawingAngular ? 'bg-indigo-100 text-indigo-700 border-indigo-300' : 'bg-gray-100 text-gray-600 hover:bg-gray-200 border-gray-200'}`}
                    >
                      {isDrawingAngular ? "Stop Drawing" : "Draw Angular Shelf"}
                    </button>
                  )}
                  <button onClick={() => setZoomLevel(prev => prev + 0.2)} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Zoom In</button>
                  <button onClick={() => setZoomLevel(prev => Math.max(0.4, prev - 0.2))} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Zoom Out</button>
                  <button onClick={() => { setIsFullScreenDrawing(false); setZoomLevel(1); setIsDrawingAngular(false); }} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Exit Full Screen</button>
                </div>
              )}
              {constructionCategory === "metal" ? (
                 <svg 
                   width={isFullScreenDrawing ? `${100 * zoomLevel}%` : (width + 100) * 0.4} 
                   height={isFullScreenDrawing ? `${100 * zoomLevel}%` : (height + 100 + (addMetalBottomLegs ? 150 : 0)) * 0.4} 
                   viewBox={`-50 -50 ${width + 100} ${height + 100 + (addMetalBottomLegs ? 150 : 0)}`} 
                   className={`drop-shadow-md transition-all duration-200 ${isFullScreenDrawing ? "m-auto" : "max-h-[600px] w-auto"}`}
                   onPointerMove={(e) => {
                     if (!dragState) return;
                     e.preventDefault();
                     const { type, idx, startY } = dragState;
                     const dy = e.clientY - startY;
                     if (Math.abs(dy) > 3 && !dragState.isDragging) {
                       setDragState({...dragState, isDragging: true});
                       isDraggingRef.current = true;
                     }
                     if (!dragState.isDragging) return;
                     
                     const svgEl = e.currentTarget as SVGSVGElement;
                     const rect = svgEl.getBoundingClientRect();
                     const viewBoxHeight = height + 100 + (addMetalBottomLegs ? 150 : 0);
                     const scale = viewBoxHeight / rect.height;
                     
                     if (type === 'main_h') {
                       let currentRel = rowOffsets[idx];
                       if (currentRel === undefined) {
                          currentRel = (idx + 1) / numRows;
                       }
                       let deltaRel = (dy * scale) / height;
                       let newRel = currentRel + deltaRel;
                       let prevRel = idx > 0 ? (rowOffsets[idx - 1] ?? (idx / numRows)) : 0;
                       let nextRel = idx < numRows - 1 ? (rowOffsets[idx + 1] ?? ((idx + 2) / numRows)) : 1;
                       newRel = Math.max(prevRel + 0.05, Math.min(nextRel - 0.05, newRel));
                       setRowOffsets(prev => ({ ...prev, [idx]: newRel }));
                       setDragState({...dragState, startY: e.clientY});
                     }
                   }}
                   onPointerUp={(e) => {
                     if (dragState) {
                       if (isDraggingRef.current) e.preventDefault();
                       setDragState(null);
                       isDraggingRef.current = false;
                     }
                   }}
                   onPointerLeave={(e) => {
                     if (dragState) {
                       setDragState(null);
                       isDraggingRef.current = false;
                     }
                   }}
                 >
                   <rect x="0" y="0" width={width} height={height} fill="#f1f5f9" stroke="#94a3b8" strokeWidth="2" />
                   {/* Vertical angles */}
                   <rect x="0" y="0" width={40} height={height + (addMetalBottomLegs ? 150 : 0)} fill="#64748b" />
                   <rect x={width - 40} y="0" width={40} height={height + (addMetalBottomLegs ? 150 : 0)} fill="#64748b" />
                   {addVerticalPartitionMiddle && (
                     <rect x={(width / 2) - 20} y="0" width={40} height={height + (addMetalBottomLegs ? 150 : 0)} fill="#94a3b8" />
                   )}
                   {addMetalBottomLegs && (
                     <g>
                       {/* Rubber shoes at the bottom */}
                       <rect x="-5" y={height + 150 - 20} width={50} height={20} fill="#334155" rx="4" />
                       <rect x={width - 45} y={height + 150 - 20} width={50} height={20} fill="#334155" rx="4" />
                       {addVerticalPartitionMiddle && (
                         <rect x={(width / 2) - 25} y={height + 150 - 20} width={50} height={20} fill="#334155" rx="4" />
                       )}
                       {/* Dimension labels for legs */}
                       <line x1="-30" y1={height} x2="-20" y2={height} stroke="#64748b" strokeWidth="2" />
                       <line x1="-30" y1={height + 150} x2="-20" y2={height + 150} stroke="#64748b" strokeWidth="2" />
                       <line x1="-25" y1={height} x2="-25" y2={height + 150} stroke="#64748b" strokeWidth="2" strokeDasharray="4" />
                       <text x="-35" y={height + 75} fill="#64748b" fontSize="16" textAnchor="middle" fontWeight="bold" transform={`rotate(-90 -35 ${height + 75})`}>150mm</text>
                     </g>
                   )}
                   {/* Horizontal Shelves */}
                   {Array.from({ length: numRows + 1 }).map((_, i) => {
                     const isFirst = i === 0;
                     const isLast = i === numRows;
                     let y = 0;
                     if (isFirst) y = 0;
                     else if (isLast) y = height - 20;
                     else {
                       const getRowOffset = (idx: number, total: number) => rowOffsets[idx] ?? ((idx + 1) / total);
                       y = getRowOffset(i - 1, numRows) * height - 10;
                     }
                     return (
                       <g key={`shelf-${i}`}>
                         <rect x="0" y={y} width={width} height={20} fill={shelfMaterialType === 'metal' ? '#64748b' : '#d97706'} />
                         {!isFirst && !isLast && (
                           <rect 
                             x="0" y={y - 10} width={width} height={40} 
                             fill="transparent" 
                             className={dragState?.type === 'main_h' && dragState?.idx === i - 1 ? "cursor-grabbing" : "cursor-row-resize hover:opacity-80 transition-opacity"}
                             onPointerDown={(e) => {
                               setDragState({ bayIdx: -1, type: 'main_h', idx: i - 1, startX: e.clientX, startY: e.clientY, bayW: 0, bayH: 0, bayX: 0, bayY: 0, isDragging: false });
                               if (e.target && (e.target as Element).setPointerCapture) (e.target as Element).setPointerCapture(e.pointerId);
                               e.stopPropagation();
                             }}
                           />
                         )}
                       </g>
                     )
                   })}
                   
                   {/* Measurement overlay when dragging */}
                   {(() => {
                      if (dragState?.isDragging && dragState.type === 'main_h') {
                          const getRowOffset = (idx: number, total: number) => rowOffsets[idx] ?? ((idx + 1) / total);
                          const offsetRel = getRowOffset(dragState.idx, numRows);
                          const prevOffset = dragState.idx > 0 ? getRowOffset(dragState.idx - 1, numRows) : 0;
                          const nextOffset = dragState.idx < numRows - 1 ? getRowOffset(dragState.idx + 1, numRows) : 1;
                          
                          const yAbsolute = offsetRel * height;
                          const topH = (offsetRel - prevOffset) * height;
                          const bottomH = (nextOffset - offsetRel) * height;
                          
                          return (
                            <g pointerEvents="none">
                               <line x1="0" x2={width} y1={yAbsolute} y2={yAbsolute} stroke="#10b981" strokeWidth="2" />
                               <rect x={width / 2 - 30} y={yAbsolute - topH / 2 - 12} width="60" height="24" fill="#10b981" rx="12" />
                               <text x={width / 2} y={yAbsolute - topH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(topH)}mm</text>
                               <rect x={width / 2 - 30} y={yAbsolute + bottomH / 2 - 12} width="60" height="24" fill="#10b981" rx="12" />
                               <text x={width / 2} y={yAbsolute + bottomH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(bottomH)}mm</text>
                            </g>
                          )
                      }
                      return null;
                   })()}

                   {/* Dimension labels */}
                   <text x={width / 2} y="-20" fill="#64748b" fontSize="24" textAnchor="middle" fontWeight="bold">{width}mm</text>
                   <text x="-20" y={height / 2} fill="#64748b" fontSize="24" textAnchor="middle" fontWeight="bold" transform={`rotate(-90 -20 ${height/2})`}>{height}mm</text>
                 </svg>
              ) : (
                <svg
                  viewBox={`0 0 ${width + 100} ${height + 100}`}
                  width={isFullScreenDrawing ? `${100 * zoomLevel}%` : (width + 100) * 0.4}
                  height={isFullScreenDrawing ? `${100 * zoomLevel}%` : (height + 100) * 0.4}
                  className={`drop-shadow-2xl transition-all duration-200 ${isFullScreenDrawing ? "m-auto" : "max-h-[600px] w-auto"}`}
                  xmlns="http://www.w3.org/2000/svg"
                  onPointerDown={(e) => {
                     if (isDrawingAngular) {
                        e.preventDefault();
                        const svgEl = e.currentTarget as SVGSVGElement;
                        const rect = svgEl.getBoundingClientRect();
                        const viewBoxHeight = height + 100;
                        const viewBoxWidth = width + 100;
                        const scaleX = viewBoxWidth / rect.width;
                        const scaleY = viewBoxHeight / rect.height;
                        const x = (e.clientX - rect.left) * scaleX;
                        const y = (e.clientY - rect.top) * scaleY;
                        setCurrentAngularShelf({ x1: x, y1: y, x2: x, y2: y });
                     }
                  }}
                  onPointerMove={(e) => {
                    if (isDrawingAngular && currentAngularShelf) {
                        const svgEl = e.currentTarget as SVGSVGElement;
                        const rect = svgEl.getBoundingClientRect();
                        const viewBoxHeight = height + 100;
                        const viewBoxWidth = width + 100;
                        const scaleX = viewBoxWidth / rect.width;
                        const scaleY = viewBoxHeight / rect.height;
                        const x = (e.clientX - rect.left) * scaleX;
                        const y = (e.clientY - rect.top) * scaleY;
                        setCurrentAngularShelf({ ...currentAngularShelf, x2: x, y2: y });
                        return;
                    }


                    if (!dragState) return;
                    e.preventDefault();
                    
                    const { bayIdx, type, idx, startX, startY, bayW, bayH, partitionId } = dragState;
                    
                    // Simple drag calculation
                    const dx = e.clientX - startX;
                    const dy = e.clientY - startY;
                    
                    if (Math.abs(dx) > 3 || Math.abs(dy) > 3) {
                        if (!dragState.isDragging) {
                           setDragState({...dragState, isDragging: true});
                           isDraggingRef.current = true;
                        }
                    }

                    if (!dragState.isDragging) return;

                    const bay = bays[bayIdx];
                    // The SVG scales differently depending on full screen and zoom
                    // The easiest way is to use SVG's client rect to calculate ratio, but let's approximate:
                    // SVG is drawn at width={(width+100)*0.4*zoomLevel} (if full screen), but its viewBox is (width+100)
                    // So scaling factor from DOM pixels to SVG coordinates is roughly:
                    // scale = viewBox_width / dom_width = (width+100) / ((width+100)*0.4*zoom) = 1 / (0.4 * zoom)
                    const svgEl = e.currentTarget as SVGSVGElement;
                    const rect = svgEl.getBoundingClientRect();
                    const viewBoxHeight = height + 100;
                    const viewBoxWidth = width + 100;
                    const scaleY = viewBoxHeight / rect.height;
                    const scaleX = viewBoxWidth / rect.width;
                    const scale = scaleY; // Use Y scale for general mapping
                    
                    if (type === 'angular_endpoint' && dragState.shelfId) {
                        const shelfId = dragState.shelfId;
                        setAngularShelves(prev => prev.map(s => {
                            if (s.id === shelfId) {
                                if (idx === 1) {
                                    return { ...s, x1: s.x1 + dx * scaleX, y1: s.y1 + dy * scaleY };
                                } else {
                                    return { ...s, x2: s.x2 + dx * scaleX, y2: s.y2 + dy * scaleY };
                                }
                            }
                            return s;
                        }));
                        setDragState({...dragState, startX: e.clientX, startY: e.clientY});
                        return;
                    }
                    if (type === 'h') {
                        if (bayH === undefined) return;
                        let hPositions = bay.shelfOffsets || {};
                        let currentRel = hPositions[idx];
                        if (currentRel === undefined) {
                            currentRel = (idx + 1) / ((bay.shelves || 0) + 1);
                        }
                        
                        let deltaRel = (dy * scaleY) / bayH;
                        let newRel = currentRel + deltaRel;
                        let prevRel = idx > 0 ? (hPositions[idx - 1] ?? (idx / ((bay.shelves || 0) + 1))) : 0;
                        let nextRel = idx < (bay.shelves || 0) - 1 ? (hPositions[idx + 1] ?? ((idx + 2) / ((bay.shelves || 0) + 1))) : 1;
                        newRel = Math.max(prevRel + 0.05, Math.min(nextRel - 0.05, newRel));
                        
                        updateBay(bayIdx, {
                            shelfOffsets: { ...hPositions, [idx]: newRel }
                        });
                        setDragState({...dragState, startY: e.clientY}); 
                    } else if (type === 'v') {
                         if (bayW === undefined) return;
                         let vPositions = bay.verticalShelfOffsets || {};
                         let currentRel = vPositions[idx];
                         if (currentRel === undefined) {
                            currentRel = (idx + 1) / ((bay.verticalShelves || 0) + 1);
                         }
                         
                         let deltaRel = (dx * scaleX) / bayW;
                         let newRel = currentRel + deltaRel;
                         let prevRel = idx > 0 ? (vPositions[idx - 1] ?? (idx / ((bay.verticalShelves || 0) + 1))) : 0;
                         let nextRel = idx < (bay.verticalShelves || 0) - 1 ? (vPositions[idx + 1] ?? ((idx + 2) / ((bay.verticalShelves || 0) + 1))) : 1;
                         newRel = Math.max(prevRel + 0.05, Math.min(nextRel - 0.05, newRel));
                         
                         updateBay(bayIdx, {
                             verticalShelfOffsets: { ...vPositions, [idx]: newRel }
                         });
                         setDragState({...dragState, startX: e.clientX});
                    } else if (type === 'main_v') {
                        let currentRel = colOffsets[idx];
                        if (currentRel === undefined) {
                           currentRel = (idx + 1) / numBays;
                        }
                        let deltaRel = (dx * scaleX) / (width - 16); // Total drawW without padding is roughly width
                        let newRel = currentRel + deltaRel;
                        let prevRel = idx > 0 ? (colOffsets[idx - 1] ?? (idx / numBays)) : 0;
                        let nextRel = idx < numBays - 1 ? (colOffsets[idx + 1] ?? ((idx + 2) / numBays)) : 1;
                        newRel = Math.max(prevRel + 0.05, Math.min(nextRel - 0.05, newRel));
                        setColOffsets(prev => ({ ...prev, [idx]: newRel }));
                        setDragState({...dragState, startX: e.clientX});
                    } else if (type === 'main_h') {
                        let currentRel = rowOffsets[idx];
                        if (currentRel === undefined) {
                           currentRel = (idx + 1) / numRows;
                        }
                        let deltaRel = (dy * scaleY) / (height - 16); // Total drawH without padding is roughly height
                        let newRel = currentRel + deltaRel;
                        let prevRel = idx > 0 ? (rowOffsets[idx - 1] ?? (idx / numRows)) : 0;
                        let nextRel = idx < numRows - 1 ? (rowOffsets[idx + 1] ?? ((idx + 2) / numRows)) : 1;
                        newRel = Math.max(prevRel + 0.05, Math.min(nextRel - 0.05, newRel));
                        setRowOffsets(prev => ({ ...prev, [idx]: newRel }));
                        setDragState({...dragState, startY: e.clientY});
                    }
                  }}
                  onPointerUp={(e) => {
                    if (isDrawingAngular && currentAngularShelf) {
                        const dist = Math.hypot(currentAngularShelf.x2 - currentAngularShelf.x1, currentAngularShelf.y2 - currentAngularShelf.y1);
                        if (dist > 10) {
                            setAngularShelves(prev => [...prev, { ...currentAngularShelf, id: Date.now().toString() }]);
                        }
                        setCurrentAngularShelf(null);
                        return;
                    }
                    if (dragState) {
                       setDragState(null);
                       setTimeout(() => { isDraggingRef.current = false; }, 50);
                    }
                  }}
                  onPointerLeave={(e) => {
                    if (dragState) {
                       setDragState(null);
                    }
                  }}

                >
                {/* Defs for hatches or shadows */}
                <defs>
                  <pattern id="wood" width="40" height="40" patternUnits="userSpaceOnUse">
                    <path d="M0,10 Q20,15 40,10 M0,30 Q20,25 40,30" stroke="#334155" strokeWidth="0.5" fill="none" opacity="0.35" />
                  </pattern>
                  <linearGradient id="glass" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.25" />
                    <stop offset="40%" stopColor="#0284c7" stopOpacity="0.1" />
                    <stop offset="100%" stopColor="#bae6fd" stopOpacity="0.3" />
                  </linearGradient>
                </defs>

                {/* Draw main outer storage body frame */}
                {/* Left/Right Offset to center inside viewport */}
                {(() => {
                  const drawW = width;
                  const drawH = height;
                  
                  const paddingX = 50;
                  const paddingY = 50;

                  // Outer Rect (Main cabinet body)
                  return (
                    <g>
                      {/* Carcass outer box */}
                      <rect
                        x={paddingX}
                        y={paddingY}
                        width={drawW}
                        height={drawH}
                        fill="#1e293b"
                        stroke="#475569"
                        strokeWidth="3.5"
                        rx="4"
                      />
                      
                      {/* Carcass texture hatch */}
                      <rect
                        x={paddingX + 6}
                        y={paddingY + 6}
                        width={drawW - 12}
                        height={drawH - 12}
                        fill="url(#wood)"
                        pointerEvents="none"
                      />

                      {/* Inner carcass border representing board thickness */}
                      <rect
                        x={paddingX + 8}
                        y={paddingY + 8}
                        width={drawW - 16}
                        height={drawH - 16}
                        fill="none"
                        stroke="#64748b"
                        strokeWidth="1.5"
                        strokeDasharray="2,2"
                      />

                      {/* Support Base legs at bottom */}
                      {/* Left Leg */}
                      <rect
                        x={paddingX + 16}
                        y={paddingY + drawH}
                        width="14"
                        height="18"
                        fill="#64748b"
                        stroke="#475569"
                        strokeWidth="1.5"
                        rx="2"
                      />
                      {/* Right Leg */}
                      <rect
                        x={paddingX + drawW - 30}
                        y={paddingY + drawH}
                        width="14"
                        height="18"
                        fill="#64748b"
                        stroke="#475569"
                        strokeWidth="1.5"
                        rx="2"
                      />
                      {/* Center Leg for long units */}
                      {supportLegsCount === 6 && (
                        <rect
                          x={paddingX + drawW / 2 - 7}
                          y={paddingY + drawH}
                          width="14"
                          height="18"
                          fill="#64748b"
                          stroke="#475569"
                          strokeWidth="1.5"
                          rx="2"
                        />
                      )}

                      {/* Grid Dividers */}
                      {Array.from({ length: numBays - 1 }).map((_, cIdx) => {
                         const getColOffset = (idx: number, total: number) => colOffsets[idx] ?? ((idx + 1) / total);
                         const x = paddingX + 8 + getColOffset(cIdx, numBays) * (drawW - 16);
                         const isDragging = dragState?.type === 'main_v' && dragState.idx === cIdx;
                         return (
                            <g key={`vdiv-${cIdx}`}
                               className={isDragging ? "cursor-grabbing" : "cursor-col-resize hover:opacity-80 transition-opacity"}
                               onPointerDown={(e) => {
                                  setDragState({ bayIdx: -1, type: 'main_v', idx: cIdx, startX: e.clientX, startY: e.clientY, isDragging: false });
                                  if (e.target && (e.target as Element).setPointerCapture) (e.target as Element).setPointerCapture(e.pointerId);
                                  e.stopPropagation();
                               }}
                            >
                                <line x1={x} y1={paddingY + 8} x2={x} y2={paddingY + drawH - 8} stroke="transparent" strokeWidth="15" />
                                <line x1={x} y1={paddingY + 8} x2={x} y2={paddingY + drawH - 8} stroke={isDragging ? "#6366f1" : "#475569"} strokeWidth="2.5" />
                            </g>
                         );
                      })}
                      {Array.from({ length: numRows - 1 }).map((_, rIdx) => {
                         const getRowOffset = (idx: number, total: number) => rowOffsets[idx] ?? ((idx + 1) / total);
                         const y = paddingY + 8 + getRowOffset(rIdx, numRows) * (drawH - 16);
                         const isDragging = dragState?.type === 'main_h' && dragState.idx === rIdx;
                         return (
                            <g key={`hdiv-${rIdx}`}
                               className={isDragging ? "cursor-grabbing" : "cursor-row-resize hover:opacity-80 transition-opacity"}
                               onPointerDown={(e) => {
                                  setDragState({ bayIdx: -1, type: 'main_h', idx: rIdx, startX: e.clientX, startY: e.clientY, isDragging: false });
                                  if (e.target && (e.target as Element).setPointerCapture) (e.target as Element).setPointerCapture(e.pointerId);
                                  e.stopPropagation();
                               }}
                            >
                                <line x1={paddingX + 8} y1={y} x2={paddingX + drawW - 8} y2={y} stroke="transparent" strokeWidth="15" />
                                <line x1={paddingX + 8} y1={y} x2={paddingX + drawW - 8} y2={y} stroke={isDragging ? "#6366f1" : "#475569"} strokeWidth="2.5" />
                            </g>
                         );
                      })}

                      {/* Draw column/row dividers and styles */}
                      {bays.map((bay, idx) => {
                        const r = Math.floor(idx / numBays);
                        const c = idx % numBays;
                        
                        const getColOffset = (idx: number, total: number) => colOffsets[idx] ?? ((idx + 1) / total);
                        const getRowOffset = (idx: number, total: number) => rowOffsets[idx] ?? ((idx + 1) / total);
                        
                        const colStart = c > 0 ? getColOffset(c - 1, numBays) : 0;
                        const colEnd = c < numBays - 1 ? getColOffset(c, numBays) : 1;
                        const rowStart = r > 0 ? getRowOffset(r - 1, numRows) : 0;
                        const rowEnd = r < numRows - 1 ? getRowOffset(r, numRows) : 1;
                        
                        const bayW = (colEnd - colStart) * (drawW - 16);
                        const bayH = (rowEnd - rowStart) * (drawH - 16);
                        const bayX = paddingX + 8 + colStart * (drawW - 16);
                        const bayY = paddingY + 8 + rowStart * (drawH - 16);

                        return (
                          <g key={idx}>

                            {/* Render different cabinet styles inside columns */}
                            {bay.style === "open" && (
                              <g>
                                {/* Draw horizontal and vertical open shelves (segmented & draggable) */}
                                {renderShelves(bay, idx, bayX, bayY, bayW, bayH)}
                                
                                {/* Draw box shutters */}
                                {bay.boxShutters && bay.boxShutters.map((hasShutter, bIdx) => {
                                  if (!hasShutter) return null;
                                  const cols = (bay.verticalShelves || 0) + 1;
                                  const rows = (bay.shelves || 0) + 1;
                                  const r = Math.floor(bIdx / cols);
                                  const c = bIdx % cols;
                                  
                                  const boxW = bayW / cols;
                                  const boxH = bayH / rows;
                                  const boxX = bayX + c * boxW;
                                  const boxY = bayY + r * boxH;
                                  const doorId = `box-${idx}-${bIdx}`;
                                  const isOpen = openDoors.has(doorId);
                                  
                                  return (
                                    <AnimatedDoorGroup key={`shutter-${bIdx}`} className="cursor-pointer hover:opacity-80 transition-opacity" onClick={() => toggleDoor(doorId)} isOpen={isOpen} childrenClosed={<><rect
                                            x={boxX + 2}
                                            y={boxY + 2}
                                            width={boxW - 4}
                                            height={boxH - 4}
                                            fill="#334155"
                                            stroke="#475569"
                                            strokeWidth="1"
                                            rx="2"
                                          />
                                          {/* Wood grain hatch */}
                                          <rect
                                            x={boxX + 4}
                                            y={boxY + 4}
                                            width={boxW - 8}
                                            height={boxH - 8}
                                            fill="url(#wood)"
                                            opacity="0.2"
                                            pointerEvents="none"
                                          />
                                          {/* Handle */}
                                          {bay.handle && (
                                            <rect
                                              x={boxX + boxW - 8}
                                              y={boxY + boxH / 2 - 10}
                                              width="2.5"
                                              height="20"
                                              fill="#94a3b8"
                                              rx="1"
                                            />
                                          )}
                                          {/* Lock */}
                                          {bay.lock === "individual" && (
                                            <circle cx={boxX + boxW - 14} cy={boxY + boxH / 2} r="2" fill="#e2e8f0" />
                                          )}</>} childrenOpen={<><rect
                                            x={boxX + 2}
                                            y={boxY + 2}
                                            width={boxW - 4}
                                            height={boxH - 4}
                                            fill="rgba(0,0,0,0.2)"
                                            stroke="#475569"
                                            strokeWidth="1"
                                            strokeDasharray="4,4"
                                            rx="2"
                                          />
                                            {/* Hinges */}
                                            <rect x={boxX + 2} y={boxY + 20} width="4" height="15" fill="#94a3b8" rx="1" />
                                            <rect x={boxX + 2} y={boxY + boxH - 35} width="4" height="15" fill="#94a3b8" rx="1" />
                                          <text x={boxX + boxW / 2} y={boxY + boxH / 2} textAnchor="middle" dominantBaseline="middle" fill="#94a3b8" fontSize="10px" fontFamily="monospace">
                                            {Math.round(boxW)}x{Math.round(boxH)}
                                          </text></>} />
                                  );
                                })}
                              </g>
                            )}

                            {bay.style === "shutter_solid" && (
                              <AnimatedDoorGroup className="cursor-pointer hover:opacity-80 transition-opacity" onClick={() => toggleDoor(`bay-${idx}`)} isOpen={openDoors.has(`bay-${idx}`)} childrenClosed={<>{/* Shutter face panel */}
                                    <rect
                                      x={bayX + 2}
                                      y={bayY + 2}
                                      width={bayW - 4}
                                      height={bayH - 4}
                                      fill="#334155"
                                      stroke="#475569"
                                      strokeWidth="1"
                                      rx="2"
                                    />
                                    {/* Handle indicator (vertical bar) */}
                                    {bay.handle && (
                                      <rect
                                        x={bayX + bayW - 8}
                                        y={bayY + bayH / 2 - 20}
                                        width="2.5"
                                        height="40"
                                        fill="#94a3b8"
                                        rx="1"
                                      />
                                    )}
                                    {/* Lock circle keyhole */}
                                    {bay.lock === "individual" && (
                                      <circle cx={bayX + bayW - 14} cy={bayY + bayH / 2} r="2" fill="#e2e8f0" />
                                    )}
                                    {/* Wood grain hatch within shutter */}
                                    <rect
                                      x={bayX + 4}
                                      y={bayY + 4}
                                      width={bayW - 8}
                                      height={bayH - 8}
                                      fill="url(#wood)"
                                      opacity="0.2"
                                      pointerEvents="none"
                                    /></>} childrenOpen={<><rect
                                      x={bayX + 2}
                                      y={bayY + 2}
                                      width={bayW - 4}
                                      height={bayH - 4}
                                      fill="rgba(0,0,0,0.2)"
                                      stroke="#475569"
                                      strokeWidth="1"
                                      strokeDasharray="4,4"
                                      rx="2"
                                    />
                                    {/* Hinges */}
                                    <rect x={bayX + 2} y={bayY + 20} width="4" height="15" fill="#94a3b8" rx="1" />
                                    <rect x={bayX + 2} y={bayY + bayH - 35} width="4" height="15" fill="#94a3b8" rx="1" />
                                    <text x={bayX + bayW / 2} y={bayY + bayH / 2} textAnchor="middle" dominantBaseline="middle" fill="#94a3b8" fontSize="12px" fontFamily="monospace">
                                      {Math.round(bayW)}x{Math.round(bayH)}
                                    </text>{renderShelves(bay, idx, bayX, bayY, bayW, bayH)}</>} />
                            )}

                            {bay.style === "shutter_glass" && (
                              <AnimatedDoorGroup className="cursor-pointer hover:opacity-80 transition-opacity" onClick={() => toggleDoor(`bay-${idx}`)} isOpen={openDoors.has(`bay-${idx}`)} childrenClosed={<>{/* Outer frame of shutter */}
                                    <rect
                                      x={bayX + 2}
                                      y={bayY + 2}
                                      width={bayW - 4}
                                      height={bayH - 4}
                                      fill="#1e293b"
                                      stroke="#475569"
                                      strokeWidth="2.5"
                                      rx="2"
                                    />
                                    {/* Glass center pane */}
                                    <rect
                                      x={bayX + 12}
                                      y={bayY + 12}
                                      width={bayW - 24}
                                      height={bayH - 24}
                                      fill="url(#glass)"
                                      stroke="#0284c7"
                                      strokeWidth="0.75"
                                      rx="1"
                                    />
                                    {/* Diagonal glass reflection lines */}
                                    <line x1={bayX + 16} y1={bayY + 20} x2={bayX + bayW - 20} y2={bayY + bayH - 20} stroke="#bae6fd" strokeWidth="0.5" opacity="0.4" />
                                    <line x1={bayX + 24} y1={bayY + 20} x2={bayX + bayW - 28} y2={bayY + bayH - 40} stroke="#bae6fd" strokeWidth="0.5" opacity="0.4" />
                                    
                                    {/* Visible shelves inside glass */}
                                    {Array.from({ length: bay.shelves }).map((_, sIdx) => {
                                      const sY = bayY + ((sIdx + 1) * bayH) / (bay.shelves + 1);
                                      return (
                                        <line
                                          key={sIdx}
                                          x1={bayX + 12}
                                          y1={sY}
                                          x2={bayX + bayW - 12}
                                          y2={sY}
                                          stroke="#475569"
                                          strokeWidth="1.5"
                                          strokeDasharray="2,2"
                                        />
                                      );
                                    })}
                                    {/* Visible vertical dividers inside glass */}
                                    {bay.verticalShelves && bay.verticalShelves > 0 ? Array.from({ length: bay.verticalShelves }).map((_, vIdx) => {
                                      const vX = bayX + ((vIdx + 1) * bayW) / (bay.verticalShelves! + 1);
                                      return (
                                        <line
                                          key={`v-${vIdx}`}
                                          x1={vX}
                                          y1={bayY + 12}
                                          x2={vX}
                                          y2={bayY + bayH - 12}
                                          stroke="#475569"
                                          strokeWidth="1.5"
                                          strokeDasharray="2,2"
                                        />
                                      );
                                    }) : null}

                                    {/* Handle */}
                                    {bay.handle && (
                                      <rect
                                        x={bayX + bayW - 11}
                                        y={bayY + bayH / 2 - 15}
                                        width="2"
                                        height="30"
                                        fill="#f1f5f9"
                                      />
                                    )}</>} childrenOpen={<><rect
                                      x={bayX + 2}
                                      y={bayY + 2}
                                      width={bayW - 4}
                                      height={bayH - 4}
                                      fill="rgba(0,0,0,0.2)"
                                      stroke="#475569"
                                      strokeWidth="1"
                                      strokeDasharray="4,4"
                                      rx="2"
                                    />
                                    {/* Hinges */}
                                    <rect x={bayX + 2} y={bayY + 20} width="4" height="15" fill="#94a3b8" rx="1" />
                                    <rect x={bayX + 2} y={bayY + bayH - 35} width="4" height="15" fill="#94a3b8" rx="1" />
                                    <text x={bayX + bayW / 2} y={bayY + bayH / 2} textAnchor="middle" dominantBaseline="middle" fill="#94a3b8" fontSize="12px" fontFamily="monospace">
                                      {Math.round(bayW)}x{Math.round(bayH)}
                                    </text>{renderShelves(bay, idx, bayX, bayY, bayW, bayH)}</>} />
                            )}

                            {bay.style === "shutters_double" && (
                              <AnimatedDoorGroup className="cursor-pointer hover:opacity-80 transition-opacity" onClick={() => toggleDoor(`bay-${idx}`)} isOpen={openDoors.has(`bay-${idx}`)} childrenClosed={<>{/* Left Door shutter */}
                                    <rect
                                      x={bayX + 2}
                                      y={bayY + 2}
                                      width={bayW / 2 - 3}
                                      height={bayH - 4}
                                      fill="#334155"
                                      stroke="#475569"
                                      strokeWidth="1"
                                      rx="2"
                                    />
                                    {/* Right Door shutter */}
                                    <rect
                                      x={bayX + bayW / 2 + 1}
                                      y={bayY + 2}
                                      width={bayW / 2 - 3}
                                      height={bayH - 4}
                                      fill="#334155"
                                      stroke="#475569"
                                      strokeWidth="1"
                                      rx="2"
                                    />
                                    {/* Center split gap line */}
                                    <line x1={bayX + bayW / 2} y1={bayY + 2} x2={bayX + bayW / 2} y2={bayY + bayH - 2} stroke="#1e293b" strokeWidth="1" />
                                    
                                    {/* 2 Handles adjacent to the center split */}
                                    {bay.handle && (
                                      <g>
                                        <rect x={bayX + bayW / 2 - 5} y={bayY + bayH / 2 - 15} width="2" height="30" fill="#94a3b8" />
                                        <rect x={bayX + bayW / 2 + 3} y={bayY + bayH / 2 - 15} width="2" height="30" fill="#94a3b8" />
                                      </g>
                                    )}

                                    {/* Lock keyhole */}
                                    {bay.lock === "individual" && (
                                      <circle cx={bayX + bayW / 2 + 10} cy={bayY + bayH / 2} r="2" fill="#e2e8f0" />
                                    )}</>} childrenOpen={<><rect
                                      x={bayX + 2}
                                      y={bayY + 2}
                                      width={bayW - 4}
                                      height={bayH - 4}
                                      fill="rgba(0,0,0,0.2)"
                                      stroke="#475569"
                                      strokeWidth="1"
                                      strokeDasharray="4,4"
                                      rx="2"
                                    />
                                    {/* Hinges */}
                                    <rect x={bayX + 2} y={bayY + 20} width="4" height="15" fill="#94a3b8" rx="1" />
                                    <rect x={bayX + 2} y={bayY + bayH - 35} width="4" height="15" fill="#94a3b8" rx="1" />
                                    <rect x={bayX + bayW - 6} y={bayY + 20} width="4" height="15" fill="#94a3b8" rx="1" />
                                    <rect x={bayX + bayW - 6} y={bayY + bayH - 35} width="4" height="15" fill="#94a3b8" rx="1" />
                                    <text x={bayX + bayW / 2} y={bayY + bayH / 2} textAnchor="middle" dominantBaseline="middle" fill="#94a3b8" fontSize="12px" fontFamily="monospace">
                                      {Math.round(bayW)}x{Math.round(bayH)}
                                    </text>{renderShelves(bay, idx, bayX, bayY, bayW, bayH)}</>} />
                            )}

                            {bay.style === "3_drawers" && (
                              <g>
                                {Array.from({ length: 3 }).map((_, dIdx) => {
                                  const dH = bayH / 3;
                                  const dY = bayY + dIdx * dH;
                                  const doorId = `drawer-${idx}-${dIdx}`;
                                  const isOpen = openDoors.has(doorId);
                                  return (
                                    <AnimatedDoorGroup 
                                      key={dIdx}
                                      className="cursor-pointer hover:opacity-80 transition-opacity" onClick={() => toggleDoor(doorId)} isOpen={isOpen} childrenClosed={<>{/* Drawer front rectangular panel */}
                                          <rect
                                            x={bayX + 2}
                                            y={dY + 2}
                                            width={bayW - 4}
                                            height={dH - 4}
                                            fill="#475569"
                                            stroke="#334155"
                                            strokeWidth="1"
                                            rx="2"
                                          />
                                          {/* Drawer handle indicator (centered horizontal profile) */}
                                          {bay.handle && (
                                            <rect
                                              x={bayX + bayW / 2 - 25}
                                              y={dY + dH / 2 - 2}
                                              width="50"
                                              height="4"
                                              fill="#94a3b8"
                                              rx="1"
                                            />
                                          )}
                                          {/* Individual key lock on each or central lock on top */}
                                          {((bay.lock === "central" && dIdx === 0) || (bay.lock === "individual")) && (
                                            <circle cx={bayX + bayW - 12} cy={dY + 10} r="1.5" fill="#e2e8f0" />
                                          )}</>} childrenOpen={<><rect
                                            x={bayX + 2}
                                            y={dY + 2}
                                            width={bayW - 4}
                                            height={dH - 4}
                                            fill="rgba(0,0,0,0.2)"
                                            stroke="#475569"
                                            strokeWidth="1"
                                            strokeDasharray="4,4"
                                            rx="2"
                                          />
                                          <text x={bayX + bayW / 2} y={dY + dH / 2} textAnchor="middle" dominantBaseline="middle" fill="#94a3b8" fontSize="12px" fontFamily="monospace">
                                            {Math.round(bayW)}x{Math.round(dH)}
                                          </text></>} />
                                  );
                                })}
                              </g>
                            )}

                            {bay.style === "2_drawers" && (
                              <g>
                                {Array.from({ length: 2 }).map((_, dIdx) => {
                                  const dH = bayH / 2;
                                  const dY = bayY + dIdx * dH;
                                  const doorId = `drawer-${idx}-${dIdx}`;
                                  const isOpen = openDoors.has(doorId);
                                  return (
                                    <AnimatedDoorGroup 
                                      key={dIdx}
                                      className="cursor-pointer hover:opacity-80 transition-opacity" onClick={() => toggleDoor(doorId)} isOpen={isOpen} childrenClosed={<>{/* Drawer front rectangular panel */}
                                          <rect
                                            x={bayX + 2}
                                            y={dY + 2}
                                            width={bayW - 4}
                                            height={dH - 4}
                                            fill="#475569"
                                            stroke="#334155"
                                            strokeWidth="1"
                                            rx="2"
                                          />
                                          {/* Drawer handle indicator */}
                                          {bay.handle && (
                                            <rect
                                              x={bayX + bayW / 2 - 30}
                                              y={dY + dH / 2 - 2.5}
                                              width="60"
                                              height="5"
                                              fill="#94a3b8"
                                              rx="1"
                                            />
                                          )}
                                          {/* Lock keyhole */}
                                          {((bay.lock === "central" && dIdx === 0) || (bay.lock === "individual")) && (
                                            <circle cx={bayX + bayW - 12} cy={dY + 12} r="1.5" fill="#e2e8f0" />
                                          )}</>} childrenOpen={<><rect
                                            x={bayX + 2}
                                            y={dY + 2}
                                            width={bayW - 4}
                                            height={dH - 4}
                                            fill="rgba(0,0,0,0.2)"
                                            stroke="#475569"
                                            strokeWidth="1"
                                            strokeDasharray="4,4"
                                            rx="2"
                                          />
                                          <text x={bayX + bayW / 2} y={dY + dH / 2} textAnchor="middle" dominantBaseline="middle" fill="#94a3b8" fontSize="12px" fontFamily="monospace">
                                            {Math.round(bayW)}x{Math.round(dH)}
                                          </text></>} />
                                  );
                                })}
                              </g>
                            )}                            {bay.style === "1_drawer" && (
                              <AnimatedDoorGroup className="cursor-pointer hover:opacity-80 transition-opacity" onClick={() => toggleDoor(`drawer-${idx}-0`)} isOpen={openDoors.has(`drawer-${idx}-0`)} childrenClosed={<><rect
                                      x={bayX + 2}
                                      y={bayY + 2}
                                      width={bayW - 4}
                                      height={bayH - 4}
                                      fill="#475569"
                                      stroke="#334155"
                                      strokeWidth="1"
                                      rx="2"
                                    />
                                    {/* Drawer handle indicator */}
                                    {bay.handle && (
                                      <rect
                                        x={bayX + bayW / 2 - 30}
                                        y={bayY + bayH / 2 - 2.5}
                                        width="60"
                                        height="5"
                                        fill="#94a3b8"
                                        rx="1"
                                      />
                                    )}
                                    {/* Lock keyhole */}
                                    {bay.lock === "individual" && (
                                      <circle cx={bayX + bayW - 12} cy={bayY + 12} r="1.5" fill="#e2e8f0" />
                                    )}</>} childrenOpen={<><rect
                                      x={bayX + 2}
                                      y={bayY + 2}
                                      width={bayW - 4}
                                      height={bayH - 4}
                                      fill="rgba(0,0,0,0.2)"
                                      stroke="#475569"
                                      strokeWidth="1"
                                      strokeDasharray="4,4"
                                      rx="2"
                                    />
                                    <text x={bayX + bayW / 2} y={bayY + bayH / 2} textAnchor="middle" dominantBaseline="middle" fill="#94a3b8" fontSize="12px" fontFamily="monospace">
                                      {Math.round(bayW)}x{Math.round(bayH)}
                                    </text></>} />
                            )}

                            {bay.style === "1_drawer_1_shutter" && (
                              <g>
                                {/* Drawer box panel at the top */}
                                {(() => {
                                  const dH = Math.min(65, bayH / 3);
                                  const dY = bayY;
                                  const shutterY = dY + dH;
                                  const shutterH = bayH - dH;
                                  const drawerId = `drawer-${idx}-0`;
                                  const shutterId = `bay-${idx}`;
                                  
                                  return (
                                    <g>
                                      {/* Drawer */}
                                      <AnimatedDoorGroup 
                                        className="cursor-pointer hover:opacity-80 transition-opacity" onClick={() => toggleDoor(drawerId)} isOpen={openDoors.has(drawerId)} childrenClosed={<><rect
                                              x={bayX + 2}
                                              y={dY + 2}
                                              width={bayW - 4}
                                              height={dH - 4}
                                              fill="#475569"
                                              stroke="#334155"
                                              strokeWidth="1"
                                              rx="2"
                                            />
                                            {bay.handle && (
                                              <rect
                                                x={bayX + bayW / 2 - 25}
                                                y={dY + dH / 2 - 2}
                                                width="50"
                                                height="4"
                                                fill="#94a3b8"
                                                rx="1"
                                              />
                                            )}
                                            {bay.lock === "individual" && (
                                              <circle cx={bayX + bayW - 12} cy={dY + 12} r="1.5" fill="#e2e8f0" />
                                            )}</>} childrenOpen={<><rect
                                              x={bayX + 2}
                                              y={dY + 2}
                                              width={bayW - 4}
                                              height={dH - 4}
                                              fill="rgba(0,0,0,0.2)"
                                              stroke="#475569"
                                              strokeWidth="1"
                                              strokeDasharray="4,4"
                                              rx="2"
                                            />
                                            <text x={bayX + bayW / 2} y={dY + dH / 2} textAnchor="middle" dominantBaseline="middle" fill="#94a3b8" fontSize="10px" fontFamily="monospace">
                                              {Math.round(bayW)}x{Math.round(dH)}
                                            </text></>} />
                                      
                                      {/* Shutter */}
                                      <AnimatedDoorGroup 
                                        className="cursor-pointer hover:opacity-80 transition-opacity" onClick={() => toggleDoor(shutterId)} isOpen={openDoors.has(shutterId)} childrenClosed={<><rect
                                              x={bayX + 2}
                                              y={shutterY + 2}
                                              width={bayW - 4}
                                              height={shutterH - 4}
                                              fill="#475569"
                                              stroke="#334155"
                                              strokeWidth="1"
                                              rx="2"
                                            />
                                            {/* Vertical Shutter handle */}
                                            {bay.shutterHandle !== false && (
                                              <rect
                                                x={bayX + bayW - 15}
                                                y={shutterY + shutterH / 2 - 30}
                                                width="6"
                                                height="60"
                                                fill="#94a3b8"
                                                rx="2"
                                              />
                                            )}
                                            {bay.shutterLock === "individual" && (
                                              <circle cx={bayX + bayW - 12} cy={shutterY + 12} r="1.5" fill="#e2e8f0" />
                                            )}</>} childrenOpen={<><rect
                                              x={bayX + 2}
                                              y={shutterY + 2}
                                              width={bayW - 4}
                                              height={shutterH - 4}
                                              fill="rgba(0,0,0,0.2)"
                                              stroke="#475569"
                                              strokeWidth="1"
                                              strokeDasharray="4,4"
                                              rx="2"
                                            />
                                              {/* Hinges */}
                                              <rect x={bayX + 2} y={shutterY + 20} width="4" height="15" fill="#94a3b8" rx="1" />
                                              <rect x={bayX + 2} y={shutterY + shutterH - 35} width="4" height="15" fill="#94a3b8" rx="1" />
                                            <text x={bayX + bayW / 2} y={shutterY + shutterH / 2} textAnchor="middle" dominantBaseline="middle" fill="#94a3b8" fontSize="12px" fontFamily="monospace">
                                              {Math.round(bayW)}x{Math.round(shutterH)}
                                            </text>{renderShelves(bay, idx, bayX, shutterY, bayW, shutterH)}</>} />
                                    </g>
                                  );
                                })()}
                              </g>
                            )}

                            {bay.style === "vertical_horizontal" && (
                              <g>
                                <line x1={bayX + bayW / 2} y1={bayY} x2={bayX + bayW / 2} y2={bayY + bayH} stroke="#334155" strokeWidth="2.5" />
                                {Array.from({ length: bay.shelves || 0 }).map((_, sIdx) => {
                                  const sY = bayY + ((sIdx + 1) * bayH) / ((bay.shelves || 0) + 1);
                                  return (
                                    <line key={`h-${sIdx}`} x1={bayX + bayW / 2} y1={sY} x2={bayX + bayW - 2} y2={sY} stroke="#334155" strokeWidth="2" />
                                  );
                                })}
                              </g>
                            )}

                            {bay.style === "1_drawer_open" && (
                              <g>
                                {/* Drawer box panel at the top */}
                                {(() => {
                                  const dH = Math.min(65, bayH / 3);
                                  const dY = bayY;
                                  const drawerId = `drawer-${idx}-0`;
                                  return (
                                    <g>
                                      <AnimatedDoorGroup 
                                        className="cursor-pointer hover:opacity-80 transition-opacity" onClick={() => toggleDoor(drawerId)} isOpen={openDoors.has(drawerId)} childrenClosed={<><rect
                                              x={bayX + 2}
                                              y={dY + 2}
                                              width={bayW - 4}
                                              height={dH - 4}
                                              fill="#475569"
                                              stroke="#334155"
                                              strokeWidth="1"
                                              rx="2"
                                            />
                                            {bay.handle && (
                                              <rect
                                                x={bayX + bayW / 2 - 25}
                                                y={dY + dH / 2 - 2}
                                                width="50"
                                                height="4"
                                                fill="#94a3b8"
                                                rx="1"
                                              />
                                            )}</>} childrenOpen={<><rect
                                              x={bayX + 2}
                                              y={dY + 2}
                                              width={bayW - 4}
                                              height={dH - 4}
                                              fill="rgba(0,0,0,0.2)"
                                              stroke="#475569"
                                              strokeWidth="1"
                                              strokeDasharray="4,4"
                                              rx="2"
                                            />
                                            <text x={bayX + bayW / 2} y={dY + dH / 2} textAnchor="middle" dominantBaseline="middle" fill="#94a3b8" fontSize="10px" fontFamily="monospace">
                                              {Math.round(bayW)}x{Math.round(dH)}
                                            </text></>} />
                                      {bay.lock === "individual" && (
                                        <circle cx={bayX + bayW - 12} cy={dY + 10} r="1.5" fill="#e2e8f0" />
                                      )}

                                      {/* Divider shelf line below drawer */}
                                      <line
                                        x1={bayX + 1}
                                        y1={dY + dH}
                                        x2={bayX + bayW - 1}
                                        y2={dY + dH}
                                        stroke="#334155"
                                        strokeWidth="2"
                                      />

                                      {/* Render open adjustable shelves inside remaining space below drawer (segmented & draggable) */}
                                      {renderShelves(bay, idx, bayX, dY + dH - 2, bayW, bayH - dH)}
                                    </g>
                                  );
                                })()}
                              </g>
                            )}

                          </g>
                        );
                      })}
                    </g>
                  );
                })()}
                {/* Dragging Measurements Overlay */}
                {dragState && dragState.isDragging && (
                  (() => {
                    const drawW = width;
                    const drawH = height;
                    const paddingX = 50;
                    const paddingY = 50;

                    if (dragState.type === 'main_v') {
                        const getColOffset = (idx: number, total: number) => colOffsets[idx] ?? ((idx + 1) / total);
                        const offsetRel = getColOffset(dragState.idx, numBays);
                        const prevOffset = dragState.idx > 0 ? getColOffset(dragState.idx - 1, numBays) : 0;
                        const nextOffset = dragState.idx < numBays - 1 ? getColOffset(dragState.idx + 1, numBays) : 1;
                        
                        const xAbsolute = paddingX + 8 + offsetRel * (drawW - 16);
                        const leftW = (offsetRel - prevOffset) * (drawW - 16);
                        const rightW = (nextOffset - offsetRel) * (drawW - 16);

                        return (
                         <g pointerEvents="none">
                           <line y1={paddingY + 8} y2={paddingY + drawH - 8} x1={xAbsolute} x2={xAbsolute} stroke="#6366f1" strokeWidth="2" />
                           <rect x={xAbsolute - leftW / 2 - 30} y={paddingY + drawH / 2 - 12} width="60" height="24" fill="#6366f1" rx="12" />
                           <text x={xAbsolute - leftW / 2} y={paddingY + drawH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(leftW)}mm</text>
                           <rect x={xAbsolute + rightW / 2 - 30} y={paddingY + drawH / 2 - 12} width="60" height="24" fill="#6366f1" rx="12" />
                           <text x={xAbsolute + rightW / 2} y={paddingY + drawH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(rightW)}mm</text>
                         </g>
                        );
                    } else if (dragState.type === 'main_h') {
                        const getRowOffset = (idx: number, total: number) => rowOffsets[idx] ?? ((idx + 1) / total);
                        const offsetRel = getRowOffset(dragState.idx, numRows);
                        const prevOffset = dragState.idx > 0 ? getRowOffset(dragState.idx - 1, numRows) : 0;
                        const nextOffset = dragState.idx < numRows - 1 ? getRowOffset(dragState.idx + 1, numRows) : 1;

                        const yAbsolute = paddingY + 8 + offsetRel * (drawH - 16);
                        const topH = (offsetRel - prevOffset) * (drawH - 16);
                        const bottomH = (nextOffset - offsetRel) * (drawH - 16);

                        return (
                         <g pointerEvents="none">
                           <line x1={paddingX + 8} x2={paddingX + drawW - 8} y1={yAbsolute} y2={yAbsolute} stroke="#6366f1" strokeWidth="2" />
                           <rect x={paddingX + drawW / 2 - 30} y={yAbsolute - topH / 2 - 12} width="60" height="24" fill="#6366f1" rx="12" />
                           <text x={paddingX + drawW / 2} y={yAbsolute - topH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(topH)}mm</text>
                           <rect x={paddingX + drawW / 2 - 30} y={yAbsolute + bottomH / 2 - 12} width="60" height="24" fill="#6366f1" rx="12" />
                           <text x={paddingX + drawW / 2} y={yAbsolute + bottomH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(bottomH)}mm</text>
                         </g>
                        );
                    }
                    
                    const bay = bays[dragState.bayIdx];
                    if (!bay) return null;

                    if (dragState.type === 'h') {
                       const offsetRel = bay.shelfOffsets?.[dragState.idx] ?? ((dragState.idx + 1) / ((bay.shelves || 0) + 1));
                       const yInBay = offsetRel * (dragState.bayH - 4);
                       const yAbsolute = dragState.bayY + 2 + yInBay;
                       
                       const prevOffset = dragState.idx > 0 ? (bay.shelfOffsets?.[dragState.idx - 1] ?? (dragState.idx / ((bay.shelves || 0) + 1))) : 0;
                       const nextOffset = dragState.idx < (bay.shelves || 0) - 1 ? (bay.shelfOffsets?.[dragState.idx + 1] ?? ((dragState.idx + 2) / ((bay.shelves || 0) + 1))) : 1;
                       
                       const topH = (offsetRel - prevOffset) * (dragState.bayH - 4);
                       const bottomH = (nextOffset - offsetRel) * (dragState.bayH - 4);

                       return (
                         <g pointerEvents="none">
                           <line x1={dragState.bayX} x2={dragState.bayX + dragState.bayW} y1={yAbsolute} y2={yAbsolute} stroke="#10b981" strokeWidth="2" />
                           
                           {/* Top measurement */}
                           <rect x={dragState.bayX + dragState.bayW / 2 - 30} y={yAbsolute - topH / 2 - 12} width="60" height="24" fill="#10b981" rx="12" />
                           <text x={dragState.bayX + dragState.bayW / 2} y={yAbsolute - topH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(topH)}mm</text>

                           {/* Bottom measurement */}
                           <rect x={dragState.bayX + dragState.bayW / 2 - 30} y={yAbsolute + bottomH / 2 - 12} width="60" height="24" fill="#10b981" rx="12" />
                           <text x={dragState.bayX + dragState.bayW / 2} y={yAbsolute + bottomH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(bottomH)}mm</text>
                         </g>
                       );
                    } else if (dragState.type === 'v') {
                       const offsetRel = bay.verticalShelfOffsets?.[dragState.idx] ?? ((dragState.idx + 1) / ((bay.verticalShelves || 0) + 1));
                       const xInBay = offsetRel * (dragState.bayW - 4);
                       const xAbsolute = dragState.bayX + 2 + xInBay;
                       
                       const prevOffset = dragState.idx > 0 ? (bay.verticalShelfOffsets?.[dragState.idx - 1] ?? (dragState.idx / ((bay.verticalShelves || 0) + 1))) : 0;
                       const nextOffset = dragState.idx < (bay.verticalShelves || 0) - 1 ? (bay.verticalShelfOffsets?.[dragState.idx + 1] ?? ((dragState.idx + 2) / ((bay.verticalShelves || 0) + 1))) : 1;

                       const leftW = (offsetRel - prevOffset) * (dragState.bayW - 4);
                       const rightW = (nextOffset - offsetRel) * (dragState.bayW - 4);

                       return (
                         <g pointerEvents="none">
                           <line y1={dragState.bayY} y2={dragState.bayY + dragState.bayH} x1={xAbsolute} x2={xAbsolute} stroke="#10b981" strokeWidth="2" />
                           
                           {/* Left measurement */}
                           <rect x={xAbsolute - leftW / 2 - 30} y={dragState.bayY + dragState.bayH / 2 - 12} width="60" height="24" fill="#10b981" rx="12" />
                           <text x={xAbsolute - leftW / 2} y={dragState.bayY + dragState.bayH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(leftW)}mm</text>

                           {/* Right measurement */}
                           <rect x={xAbsolute + rightW / 2 - 30} y={dragState.bayY + dragState.bayH / 2 - 12} width="60" height="24" fill="#10b981" rx="12" />
                           <text x={xAbsolute + rightW / 2} y={dragState.bayY + dragState.bayH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(rightW)}mm</text>
                         </g>
                       );
                    }
                    return null;
                  })()
                )}

                {/* Draw angular custom shelves */}
                {angularShelves.map((s, i) => {
                  const length = Math.hypot(s.x2 - s.x1, s.y2 - s.y1);
                  const cx = (s.x1 + s.x2) / 2;
                  const cy = (s.y1 + s.y2) / 2;
                  
                  const isVertical = Math.abs(s.x1 - s.x2) < 5;
                  const isHorizontal = Math.abs(s.y1 - s.y2) < 5;
                  const show4Sides = isDrawingAngular && (isVertical || isHorizontal);
                  const isAngular = !isVertical && !isHorizontal;

                  return (
                  <g key={s.id}>
                     <line x1={s.x1} y1={s.y1} x2={s.x2} y2={s.y2} stroke="#f59e0b" strokeWidth="8" strokeLinecap="round" />
                     <rect x={cx - 30} y={cy - 12} width="60" height="24" fill="#f59e0b" rx="12" />
                     <text x={cx} y={cy} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(length)}mm</text>
                     
                     {isAngular && (
                        <g>
                          <line x1={s.x1} y1={s.y2} x2={s.x2} y2={s.y2} stroke="#10b981" strokeWidth="2" strokeDasharray="4,4" />
                          <line x1={s.x1} y1={s.y1} x2={s.x1} y2={s.y2} stroke="#10b981" strokeWidth="2" strokeDasharray="4,4" />
                          
                          <rect x={cx - 25} y={s.y2 - 12 + (s.y1 < s.y2 ? 20 : -20)} width="50" height="20" fill="#10b981" rx="10" />
                          <text x={cx} y={s.y2 + (s.y1 < s.y2 ? 20 : -20)} fill="white" fontSize="10" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">W: {Math.round(Math.abs(s.x2 - s.x1))}mm</text>
                          
                          <rect x={s.x1 - 25 + (s.x1 < s.x2 ? -30 : 30)} y={cy - 10} width="50" height="20" fill="#10b981" rx="10" />
                          <text x={s.x1 + (s.x1 < s.x2 ? -30 : 30)} y={cy} fill="white" fontSize="10" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">H: {Math.round(Math.abs(s.y2 - s.y1))}mm</text>
                        </g>
                     )}

                     {show4Sides && (() => {
                        const minX = Math.min(s.x1, s.x2);
                        const maxX = Math.max(s.x1, s.x2);
                        const minY = Math.min(s.y1, s.y2);
                        const maxY = Math.max(s.y1, s.y2);

                        const leftDist = minX - 50;
                        const rightDist = (50 + width) - maxX;
                        const topDist = minY - 50;
                        const bottomDist = (50 + height) - maxY;

                        return (
                          <g>
                            {/* Left Gap */}
                            <rect x={minX - Math.max(0, leftDist)/2 - 30} y={cy - 25} width="60" height="24" fill="#10b981" rx="12" />
                            <text x={minX - Math.max(0, leftDist)/2} y={cy - 13} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">L: {Math.round(Math.max(0, leftDist))}mm</text>
                            
                            {/* Right Gap */}
                            <rect x={maxX + Math.max(0, rightDist)/2 - 30} y={cy - 25} width="60" height="24" fill="#10b981" rx="12" />
                            <text x={maxX + Math.max(0, rightDist)/2} y={cy - 13} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">R: {Math.round(Math.max(0, rightDist))}mm</text>

                            {/* Top Gap */}
                            <rect x={cx - 45} y={minY - Math.max(0, topDist)/2 - 12} width="60" height="24" fill="#3b82f6" rx="12" />
                            <text x={cx - 15} y={minY - Math.max(0, topDist)/2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">T: {Math.round(Math.max(0, topDist))}mm</text>
                            
                            {/* Bottom Gap */}
                            <rect x={cx - 45} y={maxY + Math.max(0, bottomDist)/2 - 12} width="60" height="24" fill="#3b82f6" rx="12" />
                            <text x={cx - 15} y={maxY + Math.max(0, bottomDist)/2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">B: {Math.round(Math.max(0, bottomDist))}mm</text>
                          </g>
                        );
                     })()}

                     <circle cx={s.x1} cy={s.y1} r="8" fill="#f59e0b" stroke="white" strokeWidth="2" cursor="pointer"
                        onPointerDown={(e) => {
                           e.stopPropagation();
                           if (e.target && (e.target as Element).setPointerCapture) (e.target as Element).setPointerCapture(e.pointerId);
                           setDragState({
                               bayIdx: -1, type: 'angular_endpoint', idx: 1, startX: e.clientX, startY: e.clientY,
                               bayX: 0, bayY: 0, bayW: 0, bayH: 0, isDragging: false, partitionId: '', shelfId: s.id
                           });
                        }}
                     />
                     <circle cx={s.x2} cy={s.y2} r="8" fill="#f59e0b" stroke="white" strokeWidth="2" cursor="pointer"
                        onPointerDown={(e) => {
                           e.stopPropagation();
                           if (e.target && (e.target as Element).setPointerCapture) (e.target as Element).setPointerCapture(e.pointerId);
                           setDragState({
                               bayIdx: -1, type: 'angular_endpoint', idx: 2, startX: e.clientX, startY: e.clientY,
                               bayX: 0, bayY: 0, bayW: 0, bayH: 0, isDragging: false, partitionId: '', shelfId: s.id
                           });
                        }}
                     />

                     {isDrawingAngular && (
                       <g cursor="pointer" onClick={(e) => {
                          e.stopPropagation();
                          setAngularShelves(prev => prev.filter(x => x.id !== s.id));
                       }}>
                         <circle cx={cx} cy={cy - 25} r="12" fill="#ef4444" />
                         <text x={cx} y={cy - 24} fill="white" fontSize="12" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">X</text>
                       </g>
                     )}
                  </g>
                  );
                })}
                {currentAngularShelf && (() => {
                  const length = Math.hypot(currentAngularShelf.x2 - currentAngularShelf.x1, currentAngularShelf.y2 - currentAngularShelf.y1);
                  const cx = (currentAngularShelf.x1 + currentAngularShelf.x2) / 2;
                  const cy = (currentAngularShelf.y1 + currentAngularShelf.y2) / 2;
                  
                  const isVertical = Math.abs(currentAngularShelf.x1 - currentAngularShelf.x2) < 5;
                  const isHorizontal = Math.abs(currentAngularShelf.y1 - currentAngularShelf.y2) < 5;
                  const show4Sides = isVertical || isHorizontal;
                  const isAngular = !isVertical && !isHorizontal;

                  return (
                    <g pointerEvents="none">
                      <line x1={currentAngularShelf.x1} y1={currentAngularShelf.y1} x2={currentAngularShelf.x2} y2={currentAngularShelf.y2} stroke="#f59e0b" strokeWidth="8" strokeDasharray="5,5" opacity="0.7" strokeLinecap="round" />
                      <rect x={cx - 30} y={cy - 12} width="60" height="24" fill="#f59e0b" rx="12" />
                      <text x={cx} y={cy} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(length)}mm</text>
                      
                      {isAngular && (
                        <g>
                          <line x1={currentAngularShelf.x1} y1={currentAngularShelf.y2} x2={currentAngularShelf.x2} y2={currentAngularShelf.y2} stroke="#10b981" strokeWidth="2" strokeDasharray="4,4" opacity="0.7" />
                          <line x1={currentAngularShelf.x1} y1={currentAngularShelf.y1} x2={currentAngularShelf.x1} y2={currentAngularShelf.y2} stroke="#10b981" strokeWidth="2" strokeDasharray="4,4" opacity="0.7" />
                          
                          <rect x={cx - 25} y={currentAngularShelf.y2 - 12 + (currentAngularShelf.y1 < currentAngularShelf.y2 ? 20 : -20)} width="50" height="20" fill="#10b981" rx="10" />
                          <text x={cx} y={currentAngularShelf.y2 + (currentAngularShelf.y1 < currentAngularShelf.y2 ? 20 : -20)} fill="white" fontSize="10" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">W: {Math.round(Math.abs(currentAngularShelf.x2 - currentAngularShelf.x1))}mm</text>
                          
                          <rect x={currentAngularShelf.x1 - 25 + (currentAngularShelf.x1 < currentAngularShelf.x2 ? -30 : 30)} y={cy - 10} width="50" height="20" fill="#10b981" rx="10" />
                          <text x={currentAngularShelf.x1 + (currentAngularShelf.x1 < currentAngularShelf.x2 ? -30 : 30)} y={cy} fill="white" fontSize="10" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">H: {Math.round(Math.abs(currentAngularShelf.y2 - currentAngularShelf.y1))}mm</text>
                        </g>
                      )}

                      {show4Sides && (() => {
                        const minX = Math.min(currentAngularShelf.x1, currentAngularShelf.x2);
                        const maxX = Math.max(currentAngularShelf.x1, currentAngularShelf.x2);
                        const minY = Math.min(currentAngularShelf.y1, currentAngularShelf.y2);
                        const maxY = Math.max(currentAngularShelf.y1, currentAngularShelf.y2);

                        const leftDist = minX - 50;
                        const rightDist = (50 + width) - maxX;
                        const topDist = minY - 50;
                        const bottomDist = (50 + height) - maxY;

                        return (
                          <g>
                            <rect x={minX - Math.max(0, leftDist)/2 - 30} y={cy - 25} width="60" height="24" fill="#10b981" rx="12" />
                            <text x={minX - Math.max(0, leftDist)/2} y={cy - 13} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">L: {Math.round(Math.max(0, leftDist))}mm</text>
                            
                            <rect x={maxX + Math.max(0, rightDist)/2 - 30} y={cy - 25} width="60" height="24" fill="#10b981" rx="12" />
                            <text x={maxX + Math.max(0, rightDist)/2} y={cy - 13} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">R: {Math.round(Math.max(0, rightDist))}mm</text>

                            <rect x={cx - 45} y={minY - Math.max(0, topDist)/2 - 12} width="60" height="24" fill="#3b82f6" rx="12" />
                            <text x={cx - 15} y={minY - Math.max(0, topDist)/2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">T: {Math.round(Math.max(0, topDist))}mm</text>
                            
                            <rect x={cx - 45} y={maxY + Math.max(0, bottomDist)/2 - 12} width="60" height="24" fill="#3b82f6" rx="12" />
                            <text x={cx - 15} y={maxY + Math.max(0, bottomDist)/2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">B: {Math.round(Math.max(0, bottomDist))}mm</text>
                          </g>
                        );
                      })()}
                    </g>
                  );
                })()}
              </svg>
              )}
              </div>
            </div>

          {/* Section 5: Estimated Custom Quote Pricing breakdown card */}
          <div className="bg-slate-900 rounded-2xl shadow-lg p-6 text-white space-y-4 border border-slate-800">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
              <IndianRupee className="w-5 h-5 text-indigo-400" />
              <h2 className="font-semibold text-sm uppercase tracking-wider text-slate-300">
                Cost & Factory Quote breakdown
              </h2>
            </div>

            <div className="space-y-3.5 text-sm">
              <div className="flex justify-between text-slate-400 font-mono">
                <span>Carcass Board Material:</span>
                <span>Rs {calcData.totals.materialCost.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-slate-400 font-mono">
                <span>Backing PLPB (9mm Panel):</span>
                <span>Rs {calcData.totals.backingCost.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-slate-400 font-mono">
                <span>Total Hardware & Edge Banding:</span>
                <span>Rs {calcData.totals.hardwareCost.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-slate-400 font-mono">
                <span>Factory Crafting Labor:</span>
                <span>Rs {calcData.totals.laborCost.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-slate-400 font-mono">
                <span>Factory Overheads (Packing/Overhead):</span>
                <span>Rs {(calcData.totals.packagingCost + calcData.totals.toolingCost).toFixed(2)}</span>
              </div>
              
              <div className="border-t border-slate-800 my-2 pt-2.5 flex justify-between font-medium text-slate-300">
                <span>Net Manufacturing Cost:</span>
                <span className="font-mono">Rs {calcData.totals.netManufacturingCost.toFixed(2)}</span>
              </div>

              <div className="flex justify-between text-slate-400 font-mono">
                <span>Factory Markup / Profit (25%):</span>
                <span>Rs {calcData.totals.profitMargin.toFixed(2)}</span>
              </div>

              <div className="border-t-2 border-dashed border-slate-800 my-2.5 pt-4 flex justify-between items-baseline">
                <span className="font-bold text-base text-slate-200">GRAND TOTAL PRICE:</span>
                <span className="font-mono text-2xl font-bold text-indigo-400">
                  Rs {calcData.totals.grandTotal.toFixed(0)}
                </span>
              </div>
            </div>

            {/* Quick specifications breakdown taglines */}
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800/60 text-xs text-slate-400 space-y-1.5 font-mono">
              <div className="text-slate-500 font-semibold uppercase tracking-wider mb-1 text-[10px]">
                Product DNA Summary
              </div>
              <div>• Shell Size: {width} x {depth} x {height} mm</div>
              <div>• Bays Configured: {numBays} columns x {numRows} rows</div>
              {constructionCategory !== "metal" && (
                <>
                  <div>• Core Board Wood: {activeBoard.name}</div>
                  <div>• Outer Mica overlay: {outerMica === "none" ? "None" : `${outerMica}mm overlay`}</div>
                </>
              )}
            </div>
          </div>

          {/* Hardware list breakdown card */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-4">
            <div className="flex items-center gap-2 border-b border-gray-100 pb-3">
              <Layers className="w-4 h-4 text-gray-500" />
              <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                Hardware Fittings Breakdown
              </h2>
            </div>

            <div className="overflow-x-auto rounded-xl border border-gray-100 text-xs font-mono">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-gray-50 text-gray-500 border-b border-gray-100 font-semibold font-sans">
                    <th className="p-2.5">Accessory Part</th>
                    <th className="p-2.5 text-right">Qty</th>
                    <th className="p-2.5 text-right">Unit Price</th>
                    <th className="p-2.5 text-right">Net Cost</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-50 text-gray-700">
                  {calcData.hardware.map((h, i) => (
                    <tr key={i} className="hover:bg-gray-50/40">
                      <td className="p-2.5 font-sans font-medium text-gray-900">{h.label}</td>
                      <td className="p-2.5 text-right font-bold">{h.qty} <span className="text-[10px] text-gray-400">{h.unit}</span></td>
                      <td className="p-2.5 text-right">Rs {h.unitPrice}</td>
                      <td className="p-2.5 text-right font-bold text-gray-900">Rs {h.cost.toFixed(0)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        </div>

      )}

      {activeTab === "drawer" && (
        <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
          {/* Left Side: Parameters */}
          <div className="xl:col-span-7 space-y-6">
            <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-4">
              <div className="flex items-center justify-between border-b border-gray-100 pb-3">
                <div className="flex items-center gap-2">
                  <Ruler className="w-4 h-4 text-gray-500" />
                  <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                    Single Drawer Dimensions
                  </h2>
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
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-1">
                {/* Drawer Width */}
                <div className="space-y-1">
                  <label className="text-xs font-medium text-gray-500 flex justify-between">
                    <span>Width (W)</span>
                    <span className="font-semibold text-indigo-600 font-mono">{drawerWidth} mm</span>
                  </label>
                  {isCustomSize ? (
                    <input
                      type="number"
                      value={drawerWidth}
                      onChange={(e) => setDrawerWidth(Number(e.target.value))}
                      min={0}
                      className="block w-full px-3 py-1.5 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none text-sm"
                    />
                  ) : (
                    <>
                      <input
                        type="range"
                        min="300"
                        max="1200"
                        step="50"
                        value={drawerWidth}
                        onChange={(e) => setDrawerWidth(Number(e.target.value))}
                        className="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                      />
                      <div className="flex justify-between text-[10px] text-gray-400 font-mono">
                        <span>300 mm</span>
                        <span>1200 mm</span>
                      </div>
                    </>
                  )}
                </div>

                {/* Drawer Depth */}
                <div className="space-y-1">
                  <label className="text-xs font-medium text-gray-500 flex justify-between">
                    <span>Depth (D)</span>
                    <span className="font-semibold text-indigo-600 font-mono">{drawerDepth} mm</span>
                  </label>
                  {isCustomSize ? (
                    <input
                      type="number"
                      value={drawerDepth}
                      onChange={(e) => setDrawerDepth(Number(e.target.value))}
                      min={0}
                      className="block w-full px-3 py-1.5 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none text-sm"
                    />
                  ) : (
                    <>
                      <input
                        type="range"
                        min="300"
                        max="600"
                        step="50"
                        value={drawerDepth}
                        onChange={(e) => setDrawerDepth(Number(e.target.value))}
                        className="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                      />
                      <div className="flex justify-between text-[10px] text-gray-400 font-mono">
                        <span>300 mm</span>
                        <span>600 mm</span>
                      </div>
                    </>
                  )}
                </div>

                {/* Drawer Height */}
                <div className="space-y-1">
                  <label className="text-xs font-medium text-gray-500 flex justify-between">
                    <span>Face Height (H)</span>
                    <span className="font-semibold text-indigo-600 font-mono">{drawerHeight} mm</span>
                  </label>
                  {isCustomSize ? (
                    <input
                      type="number"
                      value={drawerHeight}
                      onChange={(e) => setDrawerHeight(Number(e.target.value))}
                      min={0}
                      className="block w-full px-3 py-1.5 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none text-sm"
                    />
                  ) : (
                    <>
                      <input
                        type="range"
                        min="100"
                        max="400"
                        step="20"
                        value={drawerHeight}
                        onChange={(e) => setDrawerHeight(Number(e.target.value))}
                        className="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                      />
                      <div className="flex justify-between text-[10px] text-gray-400 font-mono">
                        <span>100 mm</span>
                        <span>400 mm</span>
                      </div>
                    </>
                  )}
                </div>
              </div>
              
              {/* Construction Category Selection */}
            <div>
              <span className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                Construction Category
              </span>
              <div className="grid grid-cols-2 gap-3 mb-4">
                <button
                  type="button"
                  onClick={() => setConstructionCategory("wooden")}
                  className={`p-3 rounded-xl border text-center transition-all ${
                    constructionCategory === "wooden"
                      ? "border-indigo-600 bg-indigo-50/50 text-indigo-900 font-medium shadow-sm shadow-indigo-100/55"
                      : "border-gray-200 bg-white text-gray-600 hover:bg-gray-50"
                  }`}
                >
                  <span className="block text-xs font-bold">Wooden Boards</span>
                </button>
                <button
                  type="button"
                  onClick={() => setConstructionCategory("metal")}
                  className={`p-3 rounded-xl border text-center transition-all ${
                    constructionCategory === "metal"
                      ? "border-indigo-600 bg-indigo-50/50 text-indigo-900 font-medium shadow-sm shadow-indigo-100/55"
                      : "border-gray-200 bg-white text-gray-600 hover:bg-gray-50"
                  }`}
                >
                  <span className="block text-xs font-bold">Metal Construction</span>
                </button>
              </div>
            </div>

            {/* Quality Tier Selection */}
              <div className="pt-4 border-t border-gray-100">
                <span className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                  Quality Tier Selection
                </span>
                <div className="grid grid-cols-2 gap-3">
                  <button
                    type="button"
                    onClick={() => setQuality("standard")}
                    className={`p-3 rounded-xl border text-center transition-all ${
                      quality === "standard"
                        ? "border-indigo-600 bg-indigo-50/50 text-indigo-900 font-medium shadow-sm shadow-indigo-100/55"
                        : "border-gray-200 bg-white text-gray-600 hover:bg-gray-50"
                    }`}
                  >
                    <span className="block text-xs font-bold">Standard Quality</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setQuality("affordable")}
                    className={`p-3 rounded-xl border text-center transition-all ${
                      quality === "affordable"
                        ? "border-indigo-600 bg-indigo-50/50 text-indigo-900 font-medium shadow-sm shadow-indigo-100/55"
                        : "border-gray-200 bg-white text-gray-600 hover:bg-gray-50"
                    }`}
                  >
                    <span className="block text-xs font-bold">Affordable Quality</span>
                  </button>
                </div>
              </div>
              
              {/* Board Material and Thickness Selection */}
            {constructionCategory === "wooden" ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1.5">
                  Carcass Board Material
                </label>
                <select
                  value={boardId}
                  onChange={(e) => setBoardId(e.target.value)}
                  className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                >
                  {boards.map((b) => (
                    <option key={b.id} value={b.id}>
                      {b.name} (₹{getBoardRate(b.id, b.costPerSqFt, boardThickness, quality)}/sq.ft)
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1.5">
                  Board Thickness
                </label>
                <select
                  value={boardThickness}
                  onChange={(e) => setBoardThickness(Number(e.target.value))}
                  className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                >
                  {getAvailableThicknesses(boardId, quality).map((t) => (
                    <option key={t} value={t}>
                      {t} mm
                    </option>
                  ))}
                </select>
              </div>
            </div>
            ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1.5">
                  Slotted Angle Material
                </label>
                <select
                  value={boardId}
                  onChange={(e) => setBoardId(e.target.value)}
                  className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                >
                  {boards.map((b) => (
                    <option key={b.id} value={b.id}>
                      {b.name} (₹{getBoardRate(b.id, b.costPerSqFt, angleThickness, quality)}/sq.ft)
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1.5">
                  Angle Thickness (Gage)
                </label>
                <select
                  value={angleThickness}
                  onChange={(e) => setAngleThickness(Number(e.target.value))}
                  className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                >
                  {getAvailableThicknesses(boardId, quality).map((t) => (
                    <option key={t} value={t}>
                      {t} mm
                    </option>
                  ))}
                </select>
              </div>
              
              <div className="sm:col-span-2 pt-2 border-t border-gray-100 mt-2">
                <span className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Shelf Configuration</span>
              </div>
              
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1.5">
                  Shelf Material Type
                </label>
                <select
                  value={shelfMaterialType}
                  onChange={(e) => setShelfMaterialType(e.target.value as "metal" | "wooden")}
                  className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                >
                  <option value="metal">Metal Shelves</option>
                  <option value="wooden">Wooden Shelves</option>
                </select>
              </div>
              
              {shelfMaterialType === "metal" ? (
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">
                    Metal Shelf Thickness
                  </label>
                  <select
                    value={boardThickness}
                    onChange={(e) => setBoardThickness(Number(e.target.value))}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                  >
                    {getAvailableThicknesses(boardId, quality).map((t) => (
                      <option key={t} value={t}>
                        {t} mm
                      </option>
                    ))}
                  </select>
                </div>
              ) : (
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1.5">
                      Wooden Material
                    </label>
                    <select
                      value={woodenShelfId}
                      onChange={(e) => setWoodenShelfId(e.target.value)}
                      className="w-full px-2 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 outline-none"
                    >
                      {getBoards(quality, "wooden").map((b) => (
                        <option key={b.id} value={b.id}>
                          {b.name}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1.5">
                      Thickness
                    </label>
                    <select
                      value={woodenShelfThickness}
                      onChange={(e) => setWoodenShelfThickness(Number(e.target.value))}
                      className="w-full px-2 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 outline-none"
                    >
                      {getAvailableThicknesses(woodenShelfId, quality).map((t) => (
                        <option key={t} value={t}>
                          {t} mm
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              )}
            </div>
            )}
          </div>

          {/* Right Side: Cost Overview */}
          <div className="xl:col-span-5 space-y-6">
            {/* Drawer Preview */}
            <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-4">
              <div className="flex items-center justify-between border-b border-gray-100 pb-3">
                <div className="flex items-center gap-2">
                  <Settings className="w-4 h-4 text-gray-500" />
                  <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                    Live Drawer Blueprint
                  </h2>
                </div>
                <div className="flex items-center gap-2">
                  <button onClick={() => setZoomLevel(prev => prev + 0.2)} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Zoom In</button>
                  <button onClick={() => setZoomLevel(prev => Math.max(0.4, prev - 0.2))} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Zoom Out</button>
                  <button onClick={() => setIsFullScreenDrawing(!isFullScreenDrawing)} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">{isFullScreenDrawing ? "Exit Full Screen" : "Full Screen"}</button>
                </div>
              </div>
              <div className={`p-6 ${isFullScreenDrawing ? 'fixed inset-0 z-[100] overflow-auto bg-slate-900/95 flex' : 'flex justify-center relative bg-slate-50 border border-gray-200 rounded-xl overflow-hidden'}`}>
                {isFullScreenDrawing && (
                  <div className="fixed top-4 right-4 flex items-center gap-2 z-[60] bg-white p-2 rounded-xl shadow-lg border border-gray-200">
                    <button onClick={() => setZoomLevel(prev => prev + 0.2)} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Zoom In</button>
                    <button onClick={() => setZoomLevel(prev => Math.max(0.4, prev - 0.2))} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Zoom Out</button>
                    <button onClick={() => { setIsFullScreenDrawing(false); setZoomLevel(1); }} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Exit Full Screen</button>
                  </div>
                )}
                <svg
                  viewBox={`-50 -50 ${drawerWidth + 100} ${drawerHeight + 100}`}
                  width={isFullScreenDrawing ? `${100 * zoomLevel}%` : (drawerWidth + 100) * 0.4}
                  height={isFullScreenDrawing ? `${100 * zoomLevel}%` : (drawerHeight + 100) * 0.4}
                  className={`drop-shadow-2xl transition-all duration-200 ${isFullScreenDrawing ? "m-auto" : "max-h-[600px] w-auto"}`}
                  xmlns="http://www.w3.org/2000/svg"
                >
                   {/* Drawer face outer line */}
                   <rect x="0" y="0" width={drawerWidth} height={drawerHeight} fill="#f1f5f9" stroke="#94a3b8" strokeWidth="4" rx="2" />
                   {/* Drawer face inner line */}
                   <rect x="18" y="18" width={drawerWidth-36} height={drawerHeight-36} fill="none" stroke="#64748b" strokeWidth="1" strokeDasharray="4 2"/>
                   
                   {/* Handle */}
                   {drawerHandle && (
                     <g>
                       <rect x={drawerWidth/2 - 60} y={drawerHeight/2 - 8} width="120" height="16" fill="#94a3b8" rx="8" />
                       <rect x={drawerWidth/2 - 40} y={drawerHeight/2 - 4} width="80" height="8" fill="#e2e8f0" rx="4" />
                     </g>
                   )}
                   
                   {/* Lock */}
                   {drawerLock && (
                     <g>
                       <circle cx={drawerWidth - 40} cy={40} r="12" fill="#cbd5e1" stroke="#64748b" strokeWidth="2" />
                       <rect x={drawerWidth - 42} y={38} width="4" height="6" fill="#64748b" />
                     </g>
                   )}
                   
                   {/* Dimension labels */}
                   <text x={drawerWidth / 2} y="-20" fill="#64748b" fontSize={Math.max(12, drawerWidth * 0.05)} textAnchor="middle" fontWeight="bold">{drawerWidth}mm</text>
                   <text x="-20" y={drawerHeight / 2} fill="#64748b" fontSize={Math.max(12, drawerHeight * 0.05)} textAnchor="middle" fontWeight="bold" transform={`rotate(-90 -20 ${drawerHeight/2})`}>{drawerHeight}mm</text>
                </svg>
              </div>
            </div>
            <div className="bg-slate-900 rounded-2xl shadow-xl p-6 text-white border border-slate-800 flex flex-col h-full">
              <div className="flex items-center gap-3 mb-6 border-b border-slate-700 pb-4">
                <div className="w-10 h-10 rounded-full bg-indigo-500/20 flex items-center justify-center">
                  <IndianRupee className="w-5 h-5 text-indigo-400" />
                </div>
                <div>
                  <h2 className="text-lg font-bold text-white tracking-tight">Drawer Cost</h2>
                  <p className="text-xs text-slate-400 font-mono">Net Valuation</p>
                </div>
              </div>

              <div className="space-y-4 text-sm flex-1">
                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-amber-400" /> Carcass Material Cost:</span>
                  <span className="font-mono font-medium">Rs {drawerCalcData.totals.materialCost.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-orange-400" /> Backing PLPB Cost:</span>
                  <span className="font-mono font-medium">Rs {drawerCalcData.totals.backingCost.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-rose-400" /> Hardware & Channels:</span>
                  <span className="font-mono font-medium">Rs {drawerCalcData.totals.hardwareCost.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-emerald-400" /> Assembly Labor:</span>
                  <span className="font-mono font-medium">Rs {drawerCalcData.totals.laborCost.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-cyan-400" /> Factory Overheads:</span>
                  <span className="font-mono font-medium">Rs {(drawerCalcData.totals.packagingCost + drawerCalcData.totals.toolingCost).toFixed(2)}</span>
                </div>
                
                <div className="my-4 border-t border-slate-700/60 pt-4" />

                <div className="flex justify-between font-bold text-slate-100">
                  <span>Manufacturing Cost:</span>
                  <span className="font-mono">Rs {drawerCalcData.totals.netManufacturingCost.toFixed(2)}</span>
                </div>

                <div className="flex justify-between text-slate-400 font-mono">
                  <span>Profit Margin (25%):</span>
                  <span>Rs {drawerCalcData.totals.profitMargin.toFixed(2)}</span>
                </div>

                <div className="border-t-2 border-dashed border-slate-800 my-2.5 pt-4 flex justify-between items-baseline">
                  <span className="font-bold text-base text-slate-200">TOTAL PRICE:</span>
                  <span className="font-mono text-2xl font-bold text-indigo-400">
                    Rs {drawerCalcData.totals.grandTotal.toFixed(0)}
                  </span>
                </div>
              </div>

              
            </div>
          </div>
        </div>
        </div>
      )}

      {activeTab === "locker" && (
        <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
          {/* Left Side: Parameters */}
          <div className="xl:col-span-7 space-y-6">
            <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-4">
              <div className="flex items-center justify-between border-b border-gray-100 pb-3">
                <div className="flex items-center gap-2">
                  <Settings className="w-4 h-4 text-gray-500" />
                  <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                    Locker Dimensions
                  </h2>
                </div>
              </div>
              <div className="flex space-x-1 bg-gray-100/50 p-1 rounded-xl w-full max-w-sm mb-4">
                <button
                  onClick={() => setLockerSizeMode("overall")}
                  className={`flex-1 py-1.5 px-3 text-xs font-medium rounded-lg transition-all ${
                    lockerSizeMode === "overall"
                      ? "bg-white text-indigo-600 shadow-sm border border-gray-200/60"
                      : "text-gray-500 hover:text-gray-700 hover:bg-gray-200/50"
                  }`}
                >
                  By Overall Size
                </button>
                <button
                  onClick={() => setLockerSizeMode("box")}
                  className={`flex-1 py-1.5 px-3 text-xs font-medium rounded-lg transition-all ${
                    lockerSizeMode === "box"
                      ? "bg-white text-indigo-600 shadow-sm border border-gray-200/60"
                      : "text-gray-500 hover:text-gray-700 hover:bg-gray-200/50"
                  }`}
                >
                  By Single Box Size
                </button>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {lockerSizeMode === "overall" ? (
                  <>
                    <div>
                      <label className="block text-xs font-medium text-gray-500 mb-1.5">Total Width (W) mm</label>
                      <input
                        type="number"
                        value={lockerWidth}
                        onChange={(e) => setLockerWidth(Number(e.target.value))}
                        className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-medium text-gray-500 mb-1.5">Total Height (H) mm</label>
                      <input
                        type="number"
                        value={lockerHeight}
                        onChange={(e) => setLockerHeight(Number(e.target.value))}
                        className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                      />
                    </div>
                  </>
                ) : (
                  <>
                    <div>
                      <label className="block text-xs font-medium text-indigo-500 mb-1.5">Box Width mm</label>
                      <input
                        type="number"
                        value={lockerBoxWidth}
                        onChange={(e) => setLockerBoxWidth(Number(e.target.value))}
                        className="w-full px-3 py-2 bg-indigo-50 border border-indigo-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-medium text-indigo-500 mb-1.5">Box Height mm</label>
                      <input
                        type="number"
                        value={lockerBoxHeight}
                        onChange={(e) => setLockerBoxHeight(Number(e.target.value))}
                        className="w-full px-3 py-2 bg-indigo-50 border border-indigo-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                      />
                    </div>
                  </>
                )}
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">Depth (D) mm</label>
                  <input
                    type="number"
                    value={lockerDepth}
                    onChange={(e) => setLockerDepth(Number(e.target.value))}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">Columns (Bays)</label>
                  <input
                    type="number"
                    min={1} max={10}
                    value={lockerColumns}
                    onChange={(e) => setLockerColumns(Number(e.target.value))}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">Tiers (Doors per Column)</label>
                  <input
                    type="number"
                    min={1} max={12}
                    value={lockerTiers}
                    onChange={(e) => setLockerTiers(Number(e.target.value))}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                  />
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-4">
              <div className="flex items-center justify-between border-b border-gray-100 pb-3">
                <div className="flex items-center gap-2">
                  <Settings className="w-4 h-4 text-gray-500" />
                  <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                    Material Configuration
                  </h2>
                </div>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">Lock Type</label>
                  <select
                    value={lockerLockType}
                    onChange={(e) => setLockerLockType(e.target.value as "cam" | "digital" | "padlock" | "none")}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-medium"
                  >
                    <option value="none">None</option>
                    <option value="cam">Cam Lock</option>
                    <option value="padlock">Padlock Hasp</option>
                    <option value="digital">Digital / RFID Lock</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">CNC Design (Louvers / Perforation)</label>
                  <label className="flex items-center gap-2 mt-2 cursor-pointer">
                    <input type="checkbox" checked={lockerCncDesign} onChange={(e) => setLockerCncDesign(e.target.checked)} className="w-4 h-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500" />
                    <span className="text-sm font-medium text-gray-700">Add CNC Cutout</span>
                  </label>
                  <label className="flex items-center gap-2 mt-2 cursor-pointer">
                    <input type="checkbox" checked={lockerAddBottomLegs} onChange={(e) => setLockerAddBottomLegs(e.target.checked)} className="w-4 h-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500" />
                    <span className="text-sm font-medium text-gray-700">Add Bottom Legs (150mm)</span>
                  </label>
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">Thickness (CRCA Sheet)</label>
                  <select
                    value={lockerThickness}
                    onChange={(e) => setLockerThickness(Number(e.target.value))}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                  >
                    <option value={0.6}>0.6 mm</option>
                    <option value={0.8}>0.8 mm</option>
                    <option value={1.0}>1.0 mm</option>
                    <option value={1.2}>1.2 mm</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          {/* Right Side */}
          <div className="xl:col-span-5 space-y-6">
            {/* Live Drawer Blueprint */}
            <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-4">
              <div className="flex items-center justify-between border-b border-gray-100 pb-3">
                <div className="flex items-center gap-2">
                  <Settings className="w-4 h-4 text-gray-500" />
                  <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                    Live Locker Blueprint
                  </h2>
                </div>
                <div className="flex items-center gap-2">
                  <button onClick={() => setZoomLevel(prev => prev + 0.2)} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Zoom In</button>
                  <button onClick={() => setZoomLevel(prev => Math.max(0.4, prev - 0.2))} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Zoom Out</button>
                  <button onClick={() => setIsFullScreenDrawing(!isFullScreenDrawing)} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">{isFullScreenDrawing ? "Exit Full Screen" : "Full Screen"}</button>
                </div>
              </div>
              <div className={`p-6 ${isFullScreenDrawing ? 'fixed inset-0 z-[100] overflow-auto bg-slate-900/95 flex' : 'flex justify-center relative bg-slate-50 border border-gray-200 rounded-xl overflow-hidden'}`}>
                {isFullScreenDrawing && (
                  <div className="fixed top-4 right-4 flex items-center gap-2 z-[60] bg-white p-2 rounded-xl shadow-lg border border-gray-200">
                    <button onClick={() => setZoomLevel(prev => prev + 0.2)} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Zoom In</button>
                    <button onClick={() => setZoomLevel(prev => Math.max(0.4, prev - 0.2))} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Zoom Out</button>
                    <button onClick={() => { setIsFullScreenDrawing(false); setZoomLevel(1); }} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Exit Full Screen</button>
                  </div>
                )}
                <svg
                  viewBox={`-50 -50 ${computedLockerWidth + 100} ${computedLockerHeight + 100 + (lockerAddBottomLegs ? 150 : 0)}`}
                  width={isFullScreenDrawing ? `${100 * zoomLevel}%` : (computedLockerWidth + 100) * 0.4}
                  height={isFullScreenDrawing ? `${100 * zoomLevel}%` : (computedLockerHeight + 100 + (lockerAddBottomLegs ? 150 : 0)) * 0.4}
                  className={`drop-shadow-2xl transition-all duration-200 ${isFullScreenDrawing ? "m-auto" : "max-h-[600px] w-auto"}`}
                  xmlns="http://www.w3.org/2000/svg"
                >
                   {/* Main Frame */}
                   <rect x="0" y="0" width={computedLockerWidth} height={computedLockerHeight + (lockerAddBottomLegs ? 150 : 0)} fill="#f1f5f9" stroke="#64748b" strokeWidth="6" rx="4" />
                   
                   {/* Columns */}
                   {Array.from({ length: lockerColumns }).map((_, cIdx) => {
                     const colWidth = computedLockerWidth / lockerColumns;
                     const colX = cIdx * colWidth;
                     return (
                       <g key={`col-${cIdx}`}>
                         {/* Vertical Divider */}
                         {cIdx > 0 && <line x1={colX} y1="0" x2={colX} y2={computedLockerHeight + (lockerAddBottomLegs ? 150 : 0)} stroke="#94a3b8" strokeWidth="4" />}
                         
                         {/* Doors (Tiers) */}
                         {Array.from({ length: lockerTiers }).map((_, tIdx) => {
                           const tierHeight = computedLockerHeight / lockerTiers;
                           const tierY = tIdx * tierHeight;
                           const pad = 4;
                           const doorId = `${cIdx}-${tIdx}`;
                           const isRemoved = removedLockerDoors.includes(doorId);
                           
                           return (
                             <g 
                               key={`door-${cIdx}-${tIdx}`} 
                               onClick={() => {
                                 setRemovedLockerDoors(prev => 
                                   prev.includes(doorId) ? prev.filter(id => id !== doorId) : [...prev, doorId]
                                 );
                               }}
                               className="cursor-pointer hover:opacity-80 transition-opacity"
                             >
                               {/* Always draw horizontal shelf line if it's not the top/bottom tier */}
                               {tIdx > 0 && <line x1={colX} y1={tierY} x2={colX + colWidth} y2={tierY} stroke="#94a3b8" strokeWidth="2" />}
                               
                               <rect 
                                 x={colX + pad} 
                                 y={tierY + pad} 
                                 width={colWidth - pad*2} 
                                 height={tierHeight - pad*2} 
                                 fill={isRemoved ? "#e2e8f0" : "#cbd5e1"}
                                 fillOpacity={isRemoved ? 0.3 : 1}
                                 stroke={isRemoved ? "#94a3b8" : "#94a3b8"} 
                                 strokeWidth="2" 
                                 strokeDasharray={isRemoved ? "4 4" : "none"}
                                 rx="2"
                               />
                               
                               {!isRemoved && (
                                 <>
                                   {/* Louvers / CNC Design */}
                                   {lockerCncDesign ? (
                                     <g>
                                       {/* Simulate CNC perforations */}
                                       <circle cx={colX + colWidth/2 - 10} cy={tierY + 25} r="2" fill="#64748b" />
                                       <circle cx={colX + colWidth/2} cy={tierY + 25} r="2" fill="#64748b" />
                                       <circle cx={colX + colWidth/2 + 10} cy={tierY + 25} r="2" fill="#64748b" />
                                       <circle cx={colX + colWidth/2 - 10} cy={tierY + 35} r="2" fill="#64748b" />
                                       <circle cx={colX + colWidth/2} cy={tierY + 35} r="2" fill="#64748b" />
                                       <circle cx={colX + colWidth/2 + 10} cy={tierY + 35} r="2" fill="#64748b" />
                                       <circle cx={colX + colWidth/2 - 10} cy={tierY + 45} r="2" fill="#64748b" />
                                       <circle cx={colX + colWidth/2} cy={tierY + 45} r="2" fill="#64748b" />
                                       <circle cx={colX + colWidth/2 + 10} cy={tierY + 45} r="2" fill="#64748b" />
                                     </g>
                                   ) : (
                                     <g>
                                       <line x1={colX + colWidth/2 - 15} y1={tierY + 20} x2={colX + colWidth/2 + 15} y2={tierY + 20} stroke="#64748b" strokeWidth="2" strokeLinecap="round" />
                                       <line x1={colX + colWidth/2 - 15} y1={tierY + 26} x2={colX + colWidth/2 + 15} y2={tierY + 26} stroke="#64748b" strokeWidth="2" strokeLinecap="round" />
                                       <line x1={colX + colWidth/2 - 15} y1={tierY + 32} x2={colX + colWidth/2 + 15} y2={tierY + 32} stroke="#64748b" strokeWidth="2" strokeLinecap="round" />
                                     </g>
                                   )}
    
                                   {/* Lock / Handle */}
                                   <rect x={colX + colWidth - 25} y={tierY + tierHeight/2 - 20} width="10" height="40" fill="#94a3b8" rx="2" />
                                   
                                   {lockerLockType === "cam" && (
                                     <circle cx={colX + colWidth - 20} cy={tierY + tierHeight/2 - 5} r="2.5" fill="#1e293b" />
                                   )}
                                   {lockerLockType === "padlock" && (
                                     <path d={`M ${colX + colWidth - 23} ${tierY + tierHeight/2 - 5} Q ${colX + colWidth - 20} ${tierY + tierHeight/2 - 10} ${colX + colWidth - 17} ${tierY + tierHeight/2 - 5} L ${colX + colWidth - 17} ${tierY + tierHeight/2} L ${colX + colWidth - 23} ${tierY + tierHeight/2} Z`} fill="none" stroke="#1e293b" strokeWidth="1.5" />
                                   )}
                                   {lockerLockType === "digital" && (
                                     <rect x={colX + colWidth - 23} y={tierY + tierHeight/2 - 12} width="6" height="14" fill="#0f172a" rx="1" />
                                   )}
                                 </>
                               )}
                               
                               {/* Hover / hint overlay */}
                               <title>{isRemoved ? "Click to add door" : "Click to remove door"}</title>
                             </g>
                           )
                         })}
                       </g>
                     )
                   })}
                   
                   {lockerAddBottomLegs && (
                     <g>
                       {/* Left Leg */}
                       <rect x={0} y={computedLockerHeight} width={40} height={150} fill="#f1f5f9" stroke="#64748b" strokeWidth="6" />
                       <rect x="-5" y={computedLockerHeight + 150 - 20} width={50} height={20} fill="#334155" rx="4" />
                       
                       {/* Right Leg */}
                       <rect x={computedLockerWidth - 40} y={computedLockerHeight} width={40} height={150} fill="#f1f5f9" stroke="#64748b" strokeWidth="6" />
                       <rect x={computedLockerWidth - 45} y={computedLockerHeight + 150 - 20} width={50} height={20} fill="#334155" rx="4" />
                       
                       {/* Additional middle legs for larger width */}
                       {computedLockerWidth >= 1800 && (
                         <>
                           <rect x={computedLockerWidth / 2 - 20} y={computedLockerHeight} width={40} height={150} fill="#f1f5f9" stroke="#64748b" strokeWidth="6" />
                           <rect x={computedLockerWidth / 2 - 25} y={computedLockerHeight + 150 - 20} width={50} height={20} fill="#334155" rx="4" />
                         </>
                       )}

                       {/* Dimension labels for legs */}
                       <line x1="-30" y1={computedLockerHeight} x2="-20" y2={computedLockerHeight} stroke="#64748b" strokeWidth="2" />
                       <line x1="-30" y1={computedLockerHeight + 150} x2="-20" y2={computedLockerHeight + 150} stroke="#64748b" strokeWidth="2" />
                       <line x1="-25" y1={computedLockerHeight} x2="-25" y2={computedLockerHeight + 150} stroke="#64748b" strokeWidth="2" strokeDasharray="4" />
                       <text x="-35" y={computedLockerHeight + 75} fill="#64748b" fontSize={Math.max(16, computedLockerHeight * 0.05)} textAnchor="middle" fontWeight="bold" transform={`rotate(-90 -35 ${computedLockerHeight + 75})`}>150mm</text>
                     </g>
                   )}
                   {/* Dimension labels */}
                   <text x={computedLockerWidth / 2} y="-20" fill="#64748b" fontSize={Math.max(16, computedLockerWidth * 0.05)} textAnchor="middle" fontWeight="bold">{computedLockerWidth}mm</text>
                   <text x="-20" y={computedLockerHeight / 2} fill="#64748b" fontSize={Math.max(16, computedLockerHeight * 0.05)} textAnchor="middle" fontWeight="bold" transform={`rotate(-90 -20 ${computedLockerHeight/2})`}>{computedLockerHeight}mm</text>
                </svg>
              </div>
            </div>

            <div className="bg-slate-900 rounded-2xl shadow-xl p-6 text-white border border-slate-800 flex flex-col h-full">
              <div className="flex items-center gap-3 mb-6 border-b border-slate-700 pb-4">
                <div className="w-10 h-10 rounded-full bg-indigo-500/20 flex items-center justify-center">
                  <IndianRupee className="w-5 h-5 text-indigo-400" />
                </div>
                <div>
                  <h2 className="text-lg font-bold text-white tracking-tight">Locker Cost</h2>
                  <p className="text-xs text-slate-400 font-mono">Net Valuation</p>
                </div>
              </div>

                            <div className="space-y-6 text-sm flex-1">
                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center text-slate-300">
                    <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-amber-400" /> Sheet Metal Cost:</span>
                    <span className="font-mono font-medium">Rs {lockerCalcData.totals.materialCost.toFixed(2)}</span>
                  </div>
                  <div className="pl-6 flex flex-col gap-1">
                    {lockerCalcData.pieces.map((p, i) => (
                       <div key={i} className="flex justify-between items-center text-[11px] text-slate-500 font-mono">
                         <span>- {p.qty}x {p.label} <span className="opacity-70">({(p.totalSqFt || 0).toFixed(1)} sq.ft)</span></span>
                         <span>Rs {p.cost.toFixed(0)}</span>
                       </div>
                    ))}
                  </div>
                </div>

                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center text-slate-300">
                    <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-rose-400" /> Hardware & Locks:</span>
                    <span className="font-mono font-medium">Rs {lockerCalcData.totals.hardwareCost.toFixed(2)}</span>
                  </div>
                  <div className="pl-6 flex flex-col gap-1">
                    {lockerCalcData.hardware.map((h, i) => (
                       <div key={i} className="flex justify-between items-center text-[11px] text-slate-500 font-mono">
                         <span>- {h.qty}x {h.label}</span>
                         <span>Rs {h.cost.toFixed(0)}</span>
                       </div>
                    ))}
                  </div>
                </div>
                
                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center text-slate-300">
                    <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-emerald-400" /> Bending & Assembly:</span>
                    <span className="font-mono font-medium">Rs {lockerCalcData.totals.laborCost.toFixed(2)}</span>
                  </div>
                  <div className="pl-6 flex flex-col gap-1 text-[11px] text-slate-500 font-mono">
                     <div className="flex justify-between items-center">
                       <span>- Base Fabrication ({lockerCalcData.totals.totalSqFt?.toFixed(1) || '0'} sq.ft)</span>
                       <span>Rs {(lockerCalcData.totals.baseLabor || 0).toFixed(0)}</span>
                     </div>
                     {(lockerCalcData.totals.cncCost || 0) > 0 && (
                       <div className="flex justify-between items-center">
                         <span>- CNC Punching / Louvers</span>
                         <span>Rs {lockerCalcData.totals.cncCost.toFixed(0)}</span>
                       </div>
                     )}
                  </div>
                </div>

                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-cyan-400" /> Powder Coating & Finish:</span>
                  <span className="font-mono font-medium">Rs {(lockerCalcData.totals.packagingCost + lockerCalcData.totals.toolingCost).toFixed(2)}</span>
                </div>
                    
                <div className="my-4 border-t border-slate-700/60 pt-4" />

                <div className="flex justify-between font-bold text-slate-100">
                  <span>Manufacturing Cost:</span>
                  <span className="font-mono">Rs {lockerCalcData.totals.netManufacturingCost.toFixed(2)}</span>
                </div>

                <div className="flex justify-between text-slate-400 font-mono">
                  <span>Profit Margin (25%):</span>
                  <span>Rs {lockerCalcData.totals.profitMargin.toFixed(2)}</span>
                </div>

                <div className="border-t-2 border-dashed border-slate-800 my-2.5 pt-4 flex justify-between items-baseline">
                  <span className="font-bold text-base text-slate-200">TOTAL PRICE:</span>
                  <span className="font-mono text-2xl font-bold text-indigo-400">
                    Rs {lockerCalcData.totals.grandTotal.toFixed(0)}
                  </span>
                </div>
              </div>

              
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
