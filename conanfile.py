from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
from conans.util import files
import os
import shutil

class LibCxsparseConan(ConanFile):
    name = "cxsparse"
    version = "3.1.1"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports = [
        "patches/CMakeProjectWrapper.txt",
        "patches/Demo/CMakeLists.txt",
        "patches/CMakeLists.txt",
        "patches/cs_convert.c.diff",
        "patches/SuiteSparse_config.h.diff",
        "patches/FindCXSparse.cmake"
    ]
    url = "https://gitlab.lan.local/conan/conan-glog"
    license="GNU Lesser General Public License"
    description =  "A concise sparse Cholesky library."
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    short_paths = False

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        tools.get("https://github.com/PetterS/CXSparse/archive/{0}.tar.gz".format(self.version))
        os.rename("CXSparse-" + self.version, self.source_subfolder)

    def build(self):
        cxsparse_source_dir = os.path.join(self.source_folder, self.source_subfolder)
        shutil.move("patches/CMakeProjectWrapper.txt", "CMakeLists.txt")
        shutil.copy("patches/Demo/CMakeLists.txt",
                    os.path.join(cxsparse_source_dir, "Demo", "CMakeLists.txt"))
        shutil.copy("patches/CMakeLists.txt",
                    os.path.join(cxsparse_source_dir, "CMakeLists.txt"))
        tools.patch(cxsparse_source_dir, "patches/cs_convert.c.diff")
        tools.patch(cxsparse_source_dir, "patches/SuiteSparse_config.h.diff")

        cmake = CMake(self)
        if not tools.os_info.is_windows:
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"
        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()
        cmake.patch_config_paths()


    def package(self):
        self.copy("FindCXSparse.cmake", src="patches", dst=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
