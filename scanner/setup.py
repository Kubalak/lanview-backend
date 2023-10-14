from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

class SetStd(build_ext):         
    extra_compile_args = {
        'extension_name': {
        "msvc": ['/std:c++17'],
        "unix": ['-std=c++17']
        }
    }

    def build_extension(self, ext):
        extra_args = self.extra_compile_args.get(ext.name)
        if extra_args is not None:
            ctype = self.compiler.compiler_type
            ext.extra_compile_args = extra_args.get(ctype, [])

        build_ext.build_extension(self, ext)


def main():
    setup(
        name="splitp",
        version="0.0.1",
        description="A simple module made for fun",
        author="Me",
        author_email="mail.me@localhost.com",
        ext_modules=[Extension('splitp', ['split_ports.cpp'])],
        cmdclass = {'build_ext': SetStd}
    )

if __name__ == '__main__':
    main()