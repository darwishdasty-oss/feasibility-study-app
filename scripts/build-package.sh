#!/usr/bin/env bash
# Build a clean distributable ZIP of the PWA project
set -euo pipefail

SRC="/home/z/my-project"
OUT="/home/z/my-project/download/feasibility-study-app.zip"
STAGE="/tmp/feasibility-study-app"

# Clean previous artifacts
rm -f "$OUT"
rm -rf "$STAGE"
mkdir -p "$STAGE"

# Project name inside the ZIP
PROJ_DIR="$STAGE/feasibility-study-app"
mkdir -p "$PROJ_DIR"

# Files/dirs to copy (explicit allowlist for cleanliness)
echo "==> Copying source files..."
cd "$SRC"

# Top-level files
for f in \
  package.json \
  bun.lock \
  README.md \
  START-HERE-AR.md \
  run-windows.bat \
  run-mac-linux.sh \
  next.config.ts \
  tsconfig.json \
  tailwind.config.ts \
  postcss.config.mjs \
  components.json \
  eslint.config.mjs \
  next-env.d.ts \
  electron-builder.yml \
  .gitignore \
  Caddyfile
do
  [ -f "$f" ] && cp "$f" "$PROJ_DIR/"
done

# .env.example (don't ship real .env)
cat > "$PROJ_DIR/.env.example" <<'EOF'
DATABASE_URL="file:./db/custom.db"
EOF

# Directories (full)
for d in src public prisma electron .github scripts examples; do
  [ -d "$d" ] && cp -r "$d" "$PROJ_DIR/"
done

# Make sure db dir exists (empty) so prisma can write to it
mkdir -p "$PROJ_DIR/db"
cat > "$PROJ_DIR/db/.gitkeep" <<'EOF'
EOF

# Remove any stray databases / logs / pid files we don't want to ship
find "$PROJ_DIR" -name '*.db' -delete 2>/dev/null || true
find "$PROJ_DIR" -name '*.db-journal' -delete 2>/dev/null || true
find "$PROJ_DIR" -name '*.log' -delete 2>/dev/null || true
find "$PROJ_DIR" -name '.DS_Store' -delete 2>/dev/null || true

# Remove .next if accidentally copied
rm -rf "$PROJ_DIR/.next" 2>/dev/null || true
rm -rf "$PROJ_DIR/node_modules" 2>/dev/null || true
rm -rf "$PROJ_DIR/.git" 2>/dev/null || true

# Build the ZIP
echo "==> Creating ZIP archive..."
cd "$STAGE"
zip -r -q "$OUT" "feasibility-study-app"

# Report
SIZE=$(du -sh "$OUT" | cut -f1)
FILES=$(find "$PROJ_DIR" -type f | wc -l)
echo ""
echo "================================================"
echo "✅ ZIP package created successfully!"
echo "================================================"
echo "📦 Path:  $OUT"
echo "📐 Size:  $SIZE"
echo "📁 Files: $FILES"
echo "================================================"
ls -lh "$OUT"
