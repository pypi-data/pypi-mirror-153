from setuptools import (
    setup,
    find_packages,
)


deps = {
    'keyfile': [
        "platon-utils>=1.2.0",
        "platon-keys>=1.2.0",
        "pycryptodome>=3.6.6,<4",
    ],
    'test': [
        "pytest>=3.6,<3.7",
    ],
    'lint': [
        "flake8==3.5.0",
    ],
    'dev': [
        "bumpversion>=0.5.3,<1",
        "wheel",
        "setuptools>=36.2.0",
        # Fixing this dependency due to: pytest 3.6.4 has requirement pluggy<0.8,>=0.5, but you'll have pluggy 0.8.0 which is incompatible.
        "pluggy==0.7.1",
        # Fixing this dependency due to: requests 2.20.1 has requirement idna<2.8,>=2.5, but you'll have idna 2.8 which is incompatible.
        "idna==2.7",
        # idna 2.7 is not supported by requests 2.18
        "requests>=2.20,<3",
        "tox>=2.7.0",
        "twine",
    ],
}

deps['dev'] = (
    deps['keyfile'] +
    deps['dev'] +
    deps['test'] +
    deps['lint']
)


install_requires = deps['keyfile']

setup(
    name='platon-keyfile',
    # *IMPORTANT*: Don't manually change the version here. Use the 'bumpversion' utility.
    version='1.2.0',
    description=(
        "A library for handling the encrypted keyfiles used to store platon private keys."
    ),
    # long_description_markdown_filename='README.html',
    author='Shinnng',
    author_email='shinnng@outlook.com',
    url='https://github.com/platonnetwork/platon-keyfile',
    include_package_data=True,
    install_requires=install_requires,
    extras_require=deps,
    setup_requires=['setuptools-markdown'],
    py_modules=['platon_keyfile'],
    license="MIT",
    zip_safe=False,
    keywords='platon',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
