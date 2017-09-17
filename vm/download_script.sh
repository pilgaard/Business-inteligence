conda search tqdm

conda install tqdm

python assignment_2.py

find ./data/out -name '*.csv' | xargs wc -l | sort -rn

find ./data/out -maxdepth 1 -mindepth 1 -exec du -hs {} \; | sort -rn
