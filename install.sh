source .venv/bin/activate
pip uninstall -y agentic-a2a
rm -rf build 
rm -rf dist 
pip install setuptools wheel
python setup.py bdist_wheel
pip install dist/agentic_*.whl