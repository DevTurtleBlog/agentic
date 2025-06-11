source .venv/bin/activate
pip uninstall -y agentic
rm -rf build 
rm -rf dist 
pip install setuptools wheel
python setup.py bdist_wheel
pip install dist/agentic_*.whl