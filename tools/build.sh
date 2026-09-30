#!/bin/bash
# Пересборка 长安启源 (com.changan.oushangCos1) с русскими строками.
# Нужны: java, python3, apktool.jar и uber-apk-signer.jar в каталоге tools/.
#   ./tools/build.sh путь/к/оригиналу.apk
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
APK="$1"; WORK="${WORK:-/tmp/qiyuan-ru}"
rm -rf "$WORK" && mkdir -p "$WORK"
java -jar "$HERE/apktool.jar" d -s -f -o "$WORK/dec" "$APK"
python3 "$HERE/apply_ru.py" "$WORK/dec"
java -jar "$HERE/apktool.jar" b "$WORK/dec" -o "$WORK/unsigned.apk"
java -jar "$HERE/uber-apk-signer.jar" -a "$WORK/unsigned.apk" -o "$WORK/out" --allowResign
ls -l "$WORK/out"
