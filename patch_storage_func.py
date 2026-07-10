import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

func = """  const copyImagePrompt = () => {
    let boardName = BOARDS.find((b) => b.id === boardId)?.name || "wood";
    const prompt = `A highly realistic, professional product photography studio shot of a modern office storage cabinet. The cabinet dimensions are ${width}mm wide, ${depth}mm deep, and ${height}mm high. It is made of ${boardName} finish. It features ${numBays} bays and ${numRows} rows of storage space. Clean, ultra-minimalist solid white background. Studio lighting, highly detailed, 8k resolution, photorealistic furniture photography.`;
    navigator.clipboard.writeText(prompt);
    setCopiedPrompt(true);
    setTimeout(() => setCopiedPrompt(false), 2000);
  };

  // Export PDF"""

content = content.replace("  // Export PDF", func)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
