import os
import shutil

from distutils.command.build_ext import build_ext
from distutils.core import Distribution
from distutils.core import Extension
from distutils.errors import CCompilerError
from distutils.errors import DistutilsExecError
from distutils.errors import DistutilsPlatformError


# C Extensions
extensions = [
    Extension("fdce._extension._fdce", ["fdce/_extension/_fdce.c"]),
]


class ExtBuilder(build_ext):
    """This class allows C extension building to fail."""

    built_extensions = []

    def run(self):
        try:
            build_ext.run(self)
        except (DistutilsPlatformError, FileNotFoundError) as exc:
            print(
                f"{exc}\n\nUnable to build the C extensions, "
                "fdce will use the pure python code instead."
            )

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except (
            CCompilerError,
            DistutilsExecError,
            DistutilsPlatformError,
            ValueError,
        ) as exc:
            print(
                f"{exc}\n\nUnable to build the '{ext.name}' C extension, "
                "fdce will use the pure python version of the extension."
            )


def build(setup_kwargs):
    """
    This function is mandatory in order to build the extensions.
    """


    distribution = Distribution({"name": "fdce", "ext_modules": extensions})
    distribution.package_dir = "fdce"

    cmd = ExtBuilder(distribution)
    cmd.ensure_finalized()
    cmd.run()

    # Copy built extensions back to the project
    for output in cmd.get_outputs():
        relative_extension = os.path.relpath(output, cmd.build_lib)
        if not os.path.exists(output):
            continue

        shutil.copyfile(output, relative_extension)
        mode = os.stat(relative_extension).st_mode
        mode |= (mode & 0o444) >> 2
        os.chmod(relative_extension, mode)

    return setup_kwargs
if __name__ == "__main__":
    build({})
