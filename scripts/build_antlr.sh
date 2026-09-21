#!/usr/bin/env sh
set -eu

ANTLR_VERSION="4.13.2"
ANTLR_JAR="/tmp/antlr-${ANTLR_VERSION}-complete.jar"
mkdir -p build
curl -fsSL "https://www.antlr.org/download/antlr-${ANTLR_VERSION}-complete.jar" -o "$ANTLR_JAR"
java -jar "$ANTLR_JAR" -Dlanguage=Python3 -visitor -no-listener -o build src/grammar/OPLang.g4
touch build/__init__.py
cp src/grammar/lexererr.py build/lexererr.py
