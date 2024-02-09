#!/bin/bash

# Copy all files except those with a .ts extension and the tsconfig.json from src to dist
find ./src -type f \( ! -name '*.ts' -and ! -name 'tsconfig.json' \) -exec cp --parents {} ./dist \;

# Compile TypeScript files from src to JavaScript, outputting to dist
tsc -p ./src --outDir ./dist
