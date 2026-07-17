#!/bin/bash
for i in {100..4000..100}; do
  head -n $i src/pages/CustomStorageCalculator.tsx > tmp.tsx
  echo "}" >> tmp.tsx
  npx esbuild tmp.tsx > /dev/null 2>&1
  if [ $? -ne 0 ]; then
    echo "Error first appears somewhere before line $i"
    break
  fi
done
