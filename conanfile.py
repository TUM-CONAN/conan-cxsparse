from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
from conans.util import files
import os
import shutil


class LibCxsparseConan(ConanFile):
    name = "cxsparse"
    package_revision = "-r3"
    upstream_version = "3.1.1"
    version = "{0}{1}".format(upstream_version, package_revision)
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
    url = "https://git.ircad.fr/conan/conan-glog"
    license = "GNU Lesser General Public License"
    description = "A concise sparse Cholesky library."
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    short_paths = False

    def configure(self):
        if not tools.os_info.is_windows:
            self.options.shared = False

    def requirements(self):
        self.requires("common/1.0.1@sight/testing")

    def source(self):
        tools.get("https://github.com/PetterS/CXSparse/archive/{0}.tar.gz".format(self.upstream_version))
        os.rename("CXSparse-" + self.upstream_version, self.source_subfolder)

    def build(self):
        # Import common flags and defines
        import common

        cxsparse_source_dir = os.path.join(self.source_folder, self.source_subfolder)
        shutil.move("patches/CMakeProjectWrapper.txt", "CMakeLists.txt")
        shutil.copy("patches/Demo/CMakeLists.txt",
                    os.path.join(cxsparse_source_dir, "Demo", "CMakeLists.txt"))
        shutil.copy("patches/CMakeLists.txt",
                    os.path.join(cxsparse_source_dir, "CMakeLists.txt"))
        tools.patch(cxsparse_source_dir, "patches/cs_convert.c.diff")
        tools.patch(cxsparse_source_dir, "patches/SuiteSparse_config.h.diff")

        cmake = CMake(self)

        # Export common flags
        cmake.definitions["SIGHT_CMAKE_CXX_FLAGS"] = common.get_cxx_flags()
        cmake.definitions["SIGHT_CMAKE_CXX_FLAGS_RELEASE"] = common.get_cxx_flags_release()
        cmake.definitions["SIGHT_CMAKE_CXX_FLAGS_DEBUG"] = common.get_cxx_flags_debug()
        cmake.definitions["SIGHT_CMAKE_CXX_FLAGS_RELWITHDEBINFO"] = common.get_cxx_flags_relwithdebinfo()

        if not tools.os_info.is_windows:
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"
        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("FindCXSparse.cmake", src="patches", dst=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
