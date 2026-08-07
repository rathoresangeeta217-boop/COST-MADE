import { calculateRequiredBoards } from "./src/utils/boardCalculator";

const pieces = [
  { w: 1112.42977, l: 1112.42977, qty: 1 }, // Back panel before fix
  { w: 520, l: 450, qty: 3 } // Drawer bottoms
];

console.log(calculateRequiredBoards(pieces));
