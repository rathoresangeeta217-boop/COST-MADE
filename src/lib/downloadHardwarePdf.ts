import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

export const downloadHardwarePdf = () => {
  const doc = new jsPDF();

  doc.setFontSize(20);
  doc.setTextColor(30, 41, 59); // text-slate-800
  doc.text("Hardware & Accessories Rates", 14, 22);
  
  doc.setFontSize(11);
  doc.setTextColor(100, 116, 139); // text-slate-500
  doc.text("A comprehensive list of hardware items and their rates used across all products.", 14, 30);

  // Pedestal Hardware
  autoTable(doc, {
    startY: 40,
    head: [["Pedestal Hardware", "Rate (₹)"]],
    body: [
      ["Drawer Channel (per pair)", "235"],
      ["Drawer / Shutter Handle (per piece)", "50"],
      ["Drawer / Shutter Lock (per piece)", "120"],
      ["Central Drawer Lock (1 Lock)", "220"],
      ["Shutter Hinges (per pair)", "125"],
      ["Castors / Wheels (per set of 4)", "180"],
    ],
    theme: "striped",
    headStyles: { fillColor: [79, 70, 229] },
  });

  // L-Shape Table Hardware
  autoTable(doc, {
    startY: (doc as any).lastAutoTable.finalY + 15,
    head: [["Workstation & L-Shape Table Hardware", "Rate (₹)"]],
    body: [
      ["Screen Bracket (per piece)", "80"],
      ["CPU Trolley", "350"],
      ["CPU Mount Bracket", "550"],
      ["PVC Grommet", "100"],
      ["Metal Wire Raceway Tray", "600"],
      ["Aluminium Flap Box (Starting)", "300"],
      ["L-Patti (2 pcs per 1 ft of top)", "10"],
      ["Buffer", "5"],
      ["Nuts", "5"],
      ["Butterfly Brackets", "12.5"],
      ["Clamp (2 per leg)", "10"],
    ],
    theme: "striped",
    headStyles: { fillColor: [79, 70, 229] },
  });

  // Wire Management Flap Box Specifics
  autoTable(doc, {
    startY: (doc as any).lastAutoTable.finalY + 15,
    head: [["Aluminium Flap Box Various Rates", "Rate (₹)"]],
    body: [
      ["Flap Box Option 1", "300"],
      ["Flap Box Option 2", "450"],
      ["Flap Box Option 3", "800"],
      ["Flap Box Option 4", "1100"],
      ["Flap Box Option 5", "1250"],
      ["Flap Box Option 6", "1400"],
      ["Flap Box Option 7", "1500"],
      ["Flap Box Option 8", "1750"],
      ["Flap Box Option 9", "1800"],
      ["Flap Box Option 10", "2400"],
    ],
    theme: "striped",
    headStyles: { fillColor: [79, 70, 229] },
  });

  doc.save(`Hardware_Rates_List.pdf`);
};
