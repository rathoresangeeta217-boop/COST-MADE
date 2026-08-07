import { calculateRequiredBoards } from "./src/utils/boardCalculator";

// Simulate Custom Storage Calculator output
const backPanelThk = 9;
const width = 1650;
const height = 750;
const drawerWidth = 550;
const drawerDepth = 450;

const pieces = [
  { label: "Back Panel (9mm Engineered Wood)", l: width, w: height, h: 9, qty: 1 },
];

let boardAggregation: any = {};
pieces.forEach(b => {
    let pw = b.w;
    let pl = b.l;
    const key = "9mm MDF";
    if (!boardAggregation[key]) boardAggregation[key] = { pieces: [] };
    
    if (pw && pl) {
       boardAggregation[key].pieces.push({ w: pw, l: pl, qty: b.qty });
    } else if (b.totalSqFt > 0) {
       let sideW = Math.sqrt(b.totalSqFt * 90000);
       let sideL = Math.sqrt(b.totalSqFt * 90000);
       boardAggregation[key].pieces.push({ w: sideW, l: sideL, qty: b.qty });
    }
});

console.log(calculateRequiredBoards(boardAggregation["9mm MDF"].pieces));
