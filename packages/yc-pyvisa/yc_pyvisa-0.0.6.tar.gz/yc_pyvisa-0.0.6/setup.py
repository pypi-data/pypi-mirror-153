from setuptools import setup
from setuptools import find_packages
# requires = ["threading","statistics","pyvisa","tkinter","ctypes.wintypes"]
requires = ["pyvisa>=1.11.3","numpy>=1.19.2","regex>=2020.10.15"]
with open('README.md','r') as f:
    readme = f.read()
setup(
    name='yc_pyvisa',
    version='0.0.6',
    description='=用于YICHIP内部仪器设备的控制',
    author='Susunl',
    author_email='1253013130@qq.com',
    long_description = readme,
    long_description_content_type ='text/markdown',
    license='MIT',
    packages = find_packages(),
    include_package_data = True,
    python_requires=">=3.5",
    zip_safe=False,
    platforms = 'any',
    install_requires = requires,
    url="https://gitee.com/susunl/yc_pyvisa",
    classifiers=[ 'Programming Language :: Python :: 3'],
)
