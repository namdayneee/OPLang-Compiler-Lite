#!/usr/bin/env sh
set -eu

ANTLR_VERSION="4.13.2"

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
ANTLR_JAR="${TMPDIR:-/tmp}/antlr-${ANTLR_VERSION}-complete.jar"

mkdir -p "$ROOT_DIR/build"

curl -fsSL \
  "https://www.antlr.org/download/antlr-${ANTLR_VERSION}-complete.jar" \
  -o "$ANTLR_JAR"

cd "$ROOT_DIR/src/grammar"

java -jar "$ANTLR_JAR" \
  -Dlanguage=Python3 \
  -visitor \
  -no-listener \
  -o "$ROOT_DIR/build" \
  OPLang.g4

touch "$ROOT_DIR/build/__init__.py"

cp lexererr.py "$ROOT_DIR/build/lexererr.py"