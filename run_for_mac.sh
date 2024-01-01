#!/bin/bash
# shellcheck disable=SC1091

cd     "$(cd "$(dirname "$0")" && pwd -P)" || exit
source "bin/activate"

while true; do
    python3 runGame.py
    errorCode=$?

    if [ $errorCode -eq 1 ]; then
        printf "에러 코드 %s : 데이터를 찾을 수 없습니다.\n프로그램을 종료합니다.", $errorCode
        break
    elif [ $errorCode -gt 1 ]; then
        break
    fi
done