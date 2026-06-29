import { Link, useParams } from 'react-router-dom';
import { useProjectStore } from '../store/useProjectStore';
import { Plus, Download, FileSpreadsheet, Package, Trash2 } from 'lucide-react';
import * as XLSX from 'xlsx';

export default function ProjectDetails() {
  const { projectId } = useParams();
  const { projects, deleteItemFromProject } = useProjectStore();
  const project = projects.find((p) => p.id === projectId);

  if (!project) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Project not found.</p>
        <Link to="/" className="text-indigo-600 hover:underline mt-4 inline-block">Return to Home</Link>
      </div>
    );
  }

  const handleDownloadBOM = () => {
    const wb = XLSX.utils.book_new();

    // 1. Overall Summary
    const summaryData = project.items.map((item, index) => ({
      "Sr No": index + 1,
      "Item Name": item.name,
      "Product Type": item.productType,
      "Cost (Rs)": item.costSummary.totalCost,
    }));
    
    const wsSummary = XLSX.utils.json_to_sheet(summaryData);
    XLSX.utils.book_append_sheet(wb, wsSummary, "Project Summary");

    // 2. Raw Material Aggregation
    const boardAggregation: Record<string, { sqft: number, cost: number }> = {};
    const edgeBandingAggregation: Record<string, { meters: number, cost: number }> = {};
    const hardwareAggregation: Record<string, { qty: number, unitPrice: number, totalCost: number, unitLabel?: string }> = {};

    project.items.forEach(item => {
      // Try to extract board ID from item name e.g., "Workstation 900x600 (18mm_particle_board)"
      let defaultThickness = '18mm';
      let defaultMaterial = 'Board';
      const nameMatch = item.name.match(/\(([\w_]+)\)/);
      if (nameMatch) {
        const boardId = nameMatch[1];
        if (boardId.includes('25mm')) defaultThickness = '25mm';
        else if (boardId.includes('12mm')) defaultThickness = '12mm';
        else if (boardId.includes('9mm')) defaultThickness = '9mm';
        else if (boardId.includes('6mm')) defaultThickness = '6mm';
        else if (boardId.includes('18mm')) defaultThickness = '18mm';

        if (boardId.includes('particle')) defaultMaterial = 'Particle Board';
        else if (boardId.includes('mdf')) defaultMaterial = 'MDF';
        else if (boardId.includes('plywood')) defaultMaterial = 'Plywood';
        else if (boardId.includes('hdhmr')) defaultMaterial = 'HDHMR';
      }

      // Aggregate Boards if available
      if (item.costSummary.boardDetails || item.costSummary.boardPiecesDetails || item.costSummary.pieces) {
         const boards = item.costSummary.boardDetails || item.costSummary.boardPiecesDetails || item.costSummary.pieces || [];
         boards.forEach((b: any) => {
           const label = b.label || '';
           
           if (label.includes('Edge Banding')) {
             const mMatch = label.match(/([\d.]+)\s*m\)/);
             const tMatch = label.match(/\(([\d.]+mm)/);
             if (mMatch) {
               const meters = parseFloat(mMatch[1]);
               const thickness = tMatch ? tMatch[1] : '0.8mm';
               const key = `${thickness} Edge Banding`;
               if (!edgeBandingAggregation[key]) edgeBandingAggregation[key] = { meters: 0, cost: 0 };
               edgeBandingAggregation[key].meters += meters;
               edgeBandingAggregation[key].cost += (b.cost || 0);
             }
           } else {
             let area = b.totalSqFt || b.areaSqFt || (b.w && b.l ? (b.w * b.l * (b.qty || 1) / 90000) : 0);
             
             if (area === 0 && label) {
               const match = label.match(/\(([\d.]+)\s*sq\.ft\)/);
               if (match) {
                 area = parseFloat(match[1]);
               }
             }
             
             let thickness = defaultThickness;
             const tMatch = label.match(/(\d+)mm/);
             if (tMatch) {
               thickness = `${tMatch[1]}mm`;
             }
             
             let material = defaultMaterial;
             if (label.toLowerCase().includes('particle board')) material = 'Particle Board';
             else if (label.toLowerCase().includes('mdf')) material = 'MDF';
             else if (label.toLowerCase().includes('plywood')) material = 'Plywood';
             else if (label.toLowerCase().includes('hdhmr')) material = 'HDHMR';
             
             let mica = '';
             if (label.includes('with Mica')) {
               const micaMatch = label.match(/with Mica \(([^)]+)\)/);
               mica = micaMatch ? ` with Mica (${micaMatch[1]})` : ` with Mica`;
             }
             
             const key = `${thickness} ${material}${mica}`;
             if (!boardAggregation[key]) boardAggregation[key] = { sqft: 0, cost: 0 };
             boardAggregation[key].sqft += area;
             boardAggregation[key].cost += (b.cost || 0);
           }
         });
      }

      // Aggregate Hardware if available
      if (item.costSummary.hardwareDetails || item.costSummary.hardware) {
         const hw = item.costSummary.hardwareDetails || item.costSummary.hardware || [];
         hw.forEach((h: any) => {
           const label = h.label || '';
           if (label.includes('Edge Banding')) {
             let thickness = '0.8mm';
             const tMatch = label.match(/([\d.]+mm)/);
             if (tMatch) {
               thickness = tMatch[1];
             }
             const key = `${thickness} Edge Banding`;
             if (!edgeBandingAggregation[key]) edgeBandingAggregation[key] = { meters: 0, cost: 0 };
             edgeBandingAggregation[key].meters += h.qty;
             edgeBandingAggregation[key].cost += (h.cost || (h.qty * (h.unitPrice || h.rate || 0)));
           } else {
             const key = label;
             if (!hardwareAggregation[key]) {
               hardwareAggregation[key] = { qty: 0, unitPrice: h.unitPrice || h.rate || 0, totalCost: 0, unitLabel: h.unitLabel || 'pcs' };
             }
             hardwareAggregation[key].qty += h.qty;
             hardwareAggregation[key].totalCost += (h.qty * (h.unitPrice || h.rate || 0));
           }
         });
      }
    });

    const boardData = Object.entries(boardAggregation).map(([name, data]) => ({
      "Material Name & Spec": name,
      "Total Area (Sq.Ft)": Number(data.sqft.toFixed(2)),
      "Total Cost (Rs)": Number(data.cost.toFixed(2))
    }));
    
    if(boardData.length > 0) {
        const wsBoards = XLSX.utils.json_to_sheet(boardData);
        XLSX.utils.book_append_sheet(wb, wsBoards, "Board Requirements");
    }

    const ebData = Object.entries(edgeBandingAggregation).map(([name, data]) => ({
      "Material Name & Spec": name,
      "Total Length (Meters)": Number(data.meters.toFixed(2)),
      "Total Cost (Rs)": Number(data.cost.toFixed(2))
    }));

    if(ebData.length > 0) {
        const wsEB = XLSX.utils.json_to_sheet(ebData);
        XLSX.utils.book_append_sheet(wb, wsEB, "Edge Banding Requirements");
    }

    const hwData = Object.entries(hardwareAggregation).map(([name, data]) => ({
      "Hardware Name": name,
      "Total Quantity": data.qty,
      "Unit": data.unitLabel,
      "Unit Price (Rs)": data.unitPrice,
      "Total Cost (Rs)": data.totalCost
    }));

    if(hwData.length > 0) {
        const wsHW = XLSX.utils.json_to_sheet(hwData);
        XLSX.utils.book_append_sheet(wb, wsHW, "Hardware Requirements");
    }

    XLSX.writeFile(wb, `${project.name.replace(/\s+/g, '_')}_BOM.xlsx`);
  };

  return (
    <div className="space-y-8">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <Link to="/" className="text-sm text-indigo-600 hover:underline mb-2 inline-block">&larr; Back to Projects</Link>
          <h1 className="text-3xl font-bold text-gray-900 tracking-tight">{project.name}</h1>
          <p className="text-gray-500 text-sm mt-1">Created: {new Date(project.createdAt).toLocaleDateString()}</p>
        </div>
        
        <div className="flex gap-3">
          <button
            onClick={handleDownloadBOM}
            disabled={project.items.length === 0}
            className="flex items-center gap-2 px-4 py-2 bg-emerald-50 text-emerald-700 border border-emerald-200 font-medium rounded-xl hover:bg-emerald-100 transition-colors disabled:opacity-50"
          >
            <FileSpreadsheet className="w-4 h-4" />
            Download BOM
          </button>
          <Link
            to={`/project/${project.id}/products`}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white font-medium rounded-xl hover:bg-indigo-700 transition-colors"
          >
            <Plus className="w-4 h-4" />
            Add Item
          </Link>
        </div>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        {project.items.length === 0 ? (
          <div className="text-center py-16">
            <Package className="w-12 h-12 text-gray-300 mx-auto mb-3" />
            <p className="text-gray-500 font-medium">No items in this project yet.</p>
            <Link
              to={`/project/${project.id}/products`}
              className="text-indigo-600 hover:underline text-sm mt-2 inline-block"
            >
              Add your first item
            </Link>
          </div>
        ) : (
          <div className="divide-y divide-gray-100">
            {project.items.map((item, index) => (
              <div key={item.id} className="p-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 hover:bg-gray-50 transition-colors">
                <div>
                  <div className="flex items-center gap-3 mb-1">
                    <span className="text-sm font-semibold text-gray-400 bg-gray-100 px-2 py-0.5 rounded">#{index + 1}</span>
                    <h3 className="font-semibold text-lg text-gray-900">{item.name}</h3>
                  </div>
                  <p className="text-sm text-gray-500 capitalize">{item.productType.replace(/-/g, ' ')}</p>
                </div>
                <div className="flex items-center gap-6 w-full sm:w-auto justify-between sm:justify-end">
                  <div className="text-right">
                    <p className="text-xs text-gray-500 mb-0.5">Total Cost</p>
                    <p className="font-bold text-gray-900">Rs. {item.costSummary.totalCost?.toLocaleString()}</p>
                  </div>
                  <button
                    onClick={() => deleteItemFromProject(project.id, item.id)}
                    className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    title="Delete Item"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                  <Link 
                    to={`/project/${project.id}/calculator/${item.productType}?edit=${item.id}`}
                    className="text-sm text-indigo-600 font-medium hover:underline"
                  >
                    Edit
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
