source .venv/bin/activate
pip install setuptools wheel
python setup.py bdist_wheel
pip install dist/agentic-0.1.0-py3-none-any.whl