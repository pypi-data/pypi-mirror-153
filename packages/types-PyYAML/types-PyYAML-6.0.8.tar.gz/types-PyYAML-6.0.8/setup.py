from setuptools import setup

name = "types-PyYAML"
description = "Typing stubs for PyYAML"
long_description = '''
## Typing stubs for PyYAML

This is a PEP 561 type stub package for the `PyYAML` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `PyYAML`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/PyYAML. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `461289e18174d765d18382c821053f3e14b8b978`.
'''.lstrip()

setup(name=name,
      version="6.0.8",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/PyYAML.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['yaml-stubs'],
      package_data={'yaml-stubs': ['__init__.pyi', '_yaml.pyi', 'composer.pyi', 'constructor.pyi', 'cyaml.pyi', 'dumper.pyi', 'emitter.pyi', 'error.pyi', 'events.pyi', 'loader.pyi', 'nodes.pyi', 'parser.pyi', 'reader.pyi', 'representer.pyi', 'resolver.pyi', 'scanner.pyi', 'serializer.pyi', 'tokens.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
