set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "Running from directory:" $DIR
(cd $DIR && python3 -m scripts.evaltest --mode $1 --gold $2/ref/ --submit $2/ --single res --best --compact > $3/scores.txt)