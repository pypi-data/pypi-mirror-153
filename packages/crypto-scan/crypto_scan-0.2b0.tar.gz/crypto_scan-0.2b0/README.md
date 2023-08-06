# Build and update package
1. `rm -rf ./dist ./build`
2. Update version in `setup.py`
3. `python setup.py sdist bdist_wheel`
4. `twine upload dist/*`


# Use below command to update the latest version
`pip install --no-cache-dir --upgrade crypto-scan`