ABSPATH=$(cd "$(dirname "$0")"; pwd -P)

cd     ${ABSPATH}
source bin/activate

python3 runGame.py