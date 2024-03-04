#!/bin/bash

# Copy the tsconfig file from the root to the src folder
cp ./tsconfig.json ./src/tsconfig.json

# Copy all files except those with a .ts extension and the tsconfig.json from src to dist
find ./src -type f \( ! -name '*.ts' -and ! -name 'tsconfig.json' \) -exec cp {} ./dist \;

# Compile TypeScript files from src to JavaScript, outputting to dist
npx tsc -p ./src --outDir ./dist
