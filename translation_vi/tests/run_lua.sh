#!/bin/zsh
# usage: translation_vi/tests/run_lua.sh <test.lua> <rom.gba> [MAXF]
# Copies the ROM into a fresh folder (no .sav = NEW GAME), runs the mGBA dev build headless-ish, kills it when
# the test writes *_done.txt (or after 240 s).
set -e
HERE=${0:A:h}
MGBA=${MGBA:-/Users/zephiel/.gemini/antigravity/scratch/tools/mGBA.app/Contents/MacOS/mGBA}
TEST=${1:A}; ROM=${2:A}; MAXF=${3:-40000}
OUT=$HERE/run_${TEST:t:r}
rm -rf $OUT; mkdir -p $OUT
cp "$ROM" $OUT/game.gba
{ echo "DIR='$OUT/'"; echo "MAXF=$MAXF"; cat $TEST } > $OUT/test.lua
cd $OUT
$MGBA --script test.lua -C mute=1 -C fpsTarget=2000 -C audioSync=0 -C videoSync=0 game.gba > mgba_stdout.txt 2>&1 &
PID=$!
for i in {1..240}; do
  sleep 1
  if ls $OUT/*_done.txt >/dev/null 2>&1; then break; fi
done
kill $PID 2>/dev/null || true
cat $OUT/*_done.txt 2>/dev/null || echo "TIMEOUT"
echo "output: $OUT"
