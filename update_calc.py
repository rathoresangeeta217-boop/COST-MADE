import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

start_str = "      pieces: ["
end_str = "      bayWidth: width / (numBays || 1)"

start_idx = content.find(start_str)
end_idx = content.find(end_str, start_idx)

replacement = """    let totalDrawers = 0;
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
        ...(totalDoors > 0 ? [{ label: "Hinges", qty: totalDoors, cost: totalDoors * 150, unit: "pair", unitPrice: 150 } as any] : []),
        ...(totalDrawers > 0 ? [{ label: "Channels", qty: totalDrawers, cost: totalDrawers * 250, unit: "pair", unitPrice: 250 } as any] : [])
    ];
    
    // Add hardware cost to grand total
    const hwCost = hardware.reduce((sum, h) => sum + h.cost, 0);

      pieces: [
"""

# Wait, we need to modify netManufacturing to include hwCost!
# Actually, netManufacturing is defined before this. 
