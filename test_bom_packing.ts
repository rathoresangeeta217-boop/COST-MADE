import { calculateRequiredBoards } from "./src/utils/boardCalculator";

const pieces = [
  { w: 1650, l: 750, qty: 1 }, // Back panel
  { w: 520, l: 450, qty: 3 } // Drawer bottoms
];

console.log(calculateRequiredBoards(pieces));
