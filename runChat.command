#!/bin/bash
# shellcheck disable=SC1091

echo -ne "\033]0;Rudventure Commandline\007"

cd "$(cd "$(dirname "$0")" && pwd -P)" || exit

python3 -c "import Chat.main"