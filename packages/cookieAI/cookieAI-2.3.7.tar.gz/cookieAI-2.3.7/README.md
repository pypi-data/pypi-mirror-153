snj@snj-ThinkPad-T440p:~/coookieAI$ touch readme.md

snj@snj-ThinkPad-T440p:~/coookieAI$ touch setup.py

snj@snj-ThinkPad-T440p:~/coookieAI$ python -m pip install –-user –-upgrade setuptools wheel

 
snj@snj-ThinkPad-T440p:~/coookieAI$ pip install -U pip


snj@snj-ThinkPad-T440p:~/coookieAI$ pip install 'setuptools<20.2'

snj@snj-ThinkPad-T440p:~/coookieAI$ python3 setup.py sdist bdist_wheel


snj@snj-ThinkPad-T440p:~/coookieAI$ python3 setup.py sdist bdist_wheel
snj@snj-ThinkPad-T440p:~/coookieAI$ pip install -e .


snj@snj-ThinkPad-T440p:~/coookieAI$ python3 -m pip install --user --upgrade twine
snj@snj-ThinkPad-T440p:~/coookieAI$ python -m twine upload — repository pypi dist/*
snj@snj-ThinkPad-T440p:~/coookieAI$ python3 -m twine upload --repository testpypi dist/* --verbose
snj@snj-ThinkPad-T440p:~/coookieAI$ python3 -m twine upload --repository pypi dist/* --verbose
