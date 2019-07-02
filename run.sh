#!/bin/bash
source venv/bin/activate
python build.py --dest=build

#COMMIT=$(git log|head -1|awk '{print $2}')

#git clone git@github.com:dsschult/dsschult.github.io.git

#rsync -ai --delete --exclude CNAME --exclude .git build/ dsschult.github.io/

#cd dsschult.github.io
#git add -A
#git commit -m "$COMMIT"
#cd ..; rm -rf dsschult.github.io
#rm -rf build