#password-lookup


A simple password lookup script for bitwarden/keepass


```bash
pip install -r requirements.txt

python password_lookup.py
```


```bash
deploy 
 7102  rm -rf dist/*
 7103  python setup.py sdist bdist_wheel
 7104  twine check dist/*
 7105  twine upload dist/*

```