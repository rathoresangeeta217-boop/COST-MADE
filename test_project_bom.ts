import * as XLSX from "xlsx";
import { calculateRequiredBoards } from "./src/utils/boardCalculator";

// Mock board pieces from Project Details context
const boardAggregation: any = {
  "25mm Particle Board with Mica (Inner 0.8mm + Outer 0.8mm)": {
    sqft: 24.2,
    cost: 4000,
    pieces: [
      { w: 1500, l: 750, qty: 2 }, // 2 main table tops
      { w: 900, l: 450, qty: 2 }   // 2 return storage tops
    ]
  },
  "18mm Particle Board with Mica (Inner 0.8mm + Outer 0.8mm)": {
    sqft: 15.5,
    cost: 2500,
    pieces: [
      { w: 750, l: 725, qty: 2 },  // legs
      { w: 1200, l: 400, qty: 2 }  // modesty
    ]
  }
};

const rawBoardsSummary = Object.entries(boardAggregation).map(([name, data]: [string, any]) => {
  const actualBoards = data.pieces && data.pieces.length > 0 ? calculateRequiredBoards(data.pieces) : Math.ceil(data.sqft / 32);
  const simpleBoards = Math.ceil(data.sqft / 32);
  return {
    "Material": name,
    "Pieces Count": data.pieces ? data.pieces.reduce((acc: number, p: any) => acc + (p.qty || 1), 0) : 0,
    "Total Area (Sq.Ft)": Number(data.sqft.toFixed(2)),
    "Boards based on Area (32 sqft)": simpleBoards,
    "Raw Boards Req (Nesting Efficiency)": actualBoards,
  };
});

console.log(rawBoardsSummary);
