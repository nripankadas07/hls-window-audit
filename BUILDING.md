# Verification prerequisites

`python -m pip install setuptools wheel` before `python verify.py`. The verifier builds with installed build tools, then installs only the generated wheel into a new environment without access to source imports. CI separately verifies the README's normal build-isolated installation.
