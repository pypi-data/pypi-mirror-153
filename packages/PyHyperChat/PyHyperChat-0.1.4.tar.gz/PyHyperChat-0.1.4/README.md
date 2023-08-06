### Pypi config for Linux:
Add a file in your home folder with the content:

> [distutils] 
> index-servers=pypi
> 
> [pypi]
> repository: https://upload.pypi.org/legacy/ 
> username: <your username>
> password: <your password>
> 
> [testpypi]
> repository: https://test.pypi.org/legacy/
> username: <your username>
> password: <your password>

### Upload to Pypi:

python setup.py sdist bdist_wheel
python -m twine upload dist/*
rm build -r
rm dist -r
rm .eggs -r