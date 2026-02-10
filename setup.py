from setuptools import setup, find_packages
setup(name="ddos", version="2.0.0", author="bad-antics", description="DDoS attack simulation and mitigation toolkit", packages=find_packages(where="src"), package_dir={"":"src"}, python_requires=">=3.8")
