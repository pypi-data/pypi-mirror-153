import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

classifiers = [
	'Development Status :: 5 - Production/Stable',
	'Environment :: Console',
	'Intended Audience :: Developers',
	'License :: OSI Approved :: MIT License',
	'Operating System :: OS Independent',
	'Programming Language :: Python :: 3'
]

setuptools.setup(
    name="limited-numbers",
    version="1.1.0",
    author="Oakchris1955",
    description="A simple package to limit numbers to a marked area (can be used to simulate number overflows)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Oakchris1955/limited-numbers",
    project_urls={
        "Bug Tracker": "https://github.com/Oakchris1955/limited-numbers/issues",
    },
    classifiers=classifiers,
	license='MIT',
	keywords=['numbers', 'number', 'limit', 'limited'],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)