import os
with open('requirements2.txt') as f:
    packs = f.read().split('\n')

for i in packs:
    try:
        os.system(f'pip install {i}')
        print(f'Installed {i}')
    except:
        print(f'Ignored {i}')
