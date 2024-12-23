#!/bin/bash
# shellcheck disable=SC1091

echo -ne "\033]0;Rudventure\007"

cd     "$(cd "$(dirname "$0")" && pwd -P)" || exit
source bin/activate

pathFiles=("pip" "pip3" "pip3.13" "wheel")
for file in "${pathFiles[@]}"; do
    sed -i '' "1s|.*|#!$PWD/bin/python3.13|" "bin/$file"
done

while true; do

    configData=$(cat "config/data.json")

    mtsy=$(echo "$configData" | grep -o '"mtsY" *: *[^,}]*' | awk -F ': *' '{print $2}')
    mtsx=$(echo "$configData" | grep -o '"mtsX" *: *[^,}]*' | awk -F ': *' '{print $2}')

    if [ "$(echo "$configData" | grep -o '"autoTerminalSize" *: *[^,}]*' | awk -F ': *' '{print $2}')" = "true" ] && [ "$(tput lines)" -lt "$mtsy" ] && [ "$(tput cols)" -lt "$mtsx" ]; then
        printf "\e[8;%d;%dt" "$mtsy" "$mtsx"
    fi
    clear
    python3 run.py
    errorCode=$?

    if [ $errorCode -eq 1 ]; then
        printf "에러 코드 %s : 데이터를 찾을 수 없습니다.\n프로그램을 종료합니다.", $errorCode
        break
    elif [ $errorCode -gt 1 ]; then break
    fi
done