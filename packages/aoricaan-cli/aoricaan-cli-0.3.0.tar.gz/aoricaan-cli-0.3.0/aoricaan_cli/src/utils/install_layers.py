import os
from glob import glob
from pathlib import Path
from shutil import copytree, rmtree

LAYERS_VERSIONS = '1.0.0'
PACKAGE_NAME = 'layers'

README = '''
# layers
***

'''

LICENSE = '''Copyright (c) 2018 The Python Packaging Authority

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

SETUP = '''
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='{name}',
    version='{version}',
    author="Carlos Anorve",
    author_email="carlosaarivera23@gmail.com",
    description="Layers for lambdas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
'''.format(version=LAYERS_VERSIONS, name=PACKAGE_NAME)


def install(*, layers_path: Path):

    layers = [layers_path.joinpath(layer).joinpath('python') for layer in os.listdir(layers_path) if
              '__' not in layer and layers_path.joinpath(layer).is_dir()]

    LAYERS = []
    for layer in layers:
        LAYERS += [layer.joinpath(lyr) for lyr in os.listdir(layer) if '__' not in lyr and layer.joinpath(lyr).is_dir()]

    original_path = Path(os.getcwd())
    tmp_path = Path('tmp')
    try:
        if not tmp_path.exists():
            tmp_path.mkdir()

        for file_name, data in {'LICENSE': LICENSE, 'README.md': README, 'setup.py': SETUP}.items():
            tmp_path.joinpath(file_name).write_text(data)

        for layer in LAYERS:
            copytree(layer, tmp_path.joinpath(layer.name))

        os.chdir(tmp_path)
        os.system('pip install setuptools wheel')
        os.system(r'python setup.py sdist bdist_wheel')
        try:
            os.system(f'pip uninstall {PACKAGE_NAME}')
        except Exception as details:
            print(details)
            raise OSError(f'Is not possible uninstall the package {PACKAGE_NAME}')
        os.system(r'pip install {}'.format(glob(os.path.join('.', 'dist', '*.whl'))[0]))
        os.chdir(original_path)
    except KeyboardInterrupt:
        print('STOP BY USER')
    finally:
        try:
            rmtree(tmp_path)
        except Exception as e:
            print(str(e))
