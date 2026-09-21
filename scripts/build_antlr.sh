#!/usr/bin/env sh

set -eu

ANTLR_VERSION="4.13.2"

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"

ANTLR_JAR="${TMPDIR:-/tmp}/antlr-${ANTLR_VERSION}-complete.jar"

echo "Project root: $ROOT_DIR"
echo "ANTLR version: $ANTLR_VERSION"

rm -rf "$ROOT_DIR/build"
mkdir -p "$ROOT_DIR/build"

if [ ! -f "$ANTLR_JAR" ]; then
    echo "Downloading ANTLR..."
    curl -fsSL \
        "https://www.antlr.org/download/antlr-${ANTLR_VERSION}-complete.jar" \
        -o "$ANTLR_JAR"
fi

cd "$ROOT_DIR/src/grammar"

echo "Generating OPLang lexer/parser..."

java -jar "$ANTLR_JAR" \
    -Dlanguage=Python3 \
    -visitor \
    -no-listener \
    -o "$ROOT_DIR/build" \
    OPLang.g4

touch "$ROOT_DIR/build/__init__.py"

cp \
    "$ROOT_DIR/src/grammar/lexererr.py" \
    "$ROOT_DIR/build/lexererr.py"

echo "ANTLR generation completed."