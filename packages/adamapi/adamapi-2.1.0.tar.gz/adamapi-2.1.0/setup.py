"""
Copyright (c) 2022 MEEO s.r.l.

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
"""


import setuptools

with open("README.md","r") as fh:
    long_description=fh.read()

setuptools.setup(
        name="adamapi",
        version="2.1.0",
        author="MEEO s.r.l.",
        author_email="info@meeo.it",
        description="Python Adam API",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://git.services.meeo.it/das/adamapi",
        packages=setuptools.find_packages(where="src"),
        package_dir={"":"src"},
        install_requires=[
            'requests >= 2.22.0',
            'imageio == 2.9.0',
            'tqdm == 4.62.3',
            'numpy == 1.21.2',
            'python-dateutil == 2.8.2',
            'matplotlib == 3.4.3',
            "certifi == 2021.5.30",
            "charset-normalizer == 2.0.6",
            "cycler == 0.10.0",
            "idna == 3.2",
            "kiwisolver == 1.3.2",
            "Pillow == 8.3.2",
            "pyparsing == 2.4.7",
            "six == 1.16.0",
            "urllib3 ==1.26.7"
            ],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: Unix",
            ],
        python_requires='>=3.6',
        )
