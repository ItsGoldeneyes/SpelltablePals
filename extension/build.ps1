# Copy all files except those with a .ts extension from src to dist
Get-ChildItem -Path "./src/" -File | Where-Object { $_.Extension -ne ".ts" -and $_.Name -ne "tsconfig.json" } | ForEach-Object { Copy-Item $_.FullName -Destination "./dist/" }

# Compile TypeScript files from src to JavaScript, outputting to dist
npx tsc -p ./src --outDir ./dist;