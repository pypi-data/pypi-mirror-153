pip install wheel twine\
python setup.py sdist bdist_wheel\
twine check *\
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*\
pip install uniphi

