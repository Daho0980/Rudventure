#!/bin/bash
# shellcheck disable=SC1091

cd     "$(cd "$(dirname "$0")" && pwd -P)" || exit
source "bin/activate"

while true; do
    if ! python3 runGame.py; then
        echo "에러가 발생했습니다. 프로그램을 종료합니다."
        break
    fi
done