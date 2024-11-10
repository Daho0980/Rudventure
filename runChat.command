#!/bin/bash
# shellcheck disable=SC1091

cd "$(cd "$(dirname "$0")" && pwd -P)" || exit

python3 -c "import Chat.main"