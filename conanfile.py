from conans import ConanFile, CMake, tools
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
    short_paths = True

    def configure(self):
        if not tools.os_info.is_windows:
            self.options.shared = False

    def requirements(self):
        self.requires("common/1.0.1@sight/testing")

    def source(self):
        tools.get("https://github.com/PetterS/CXSparse/archive/{0}.tar.gz".format(self.upstream_version))
        os.rename("CXSparse-" + self.upstream_version, self.source_subfolder)

    def build(self):
        cxsparse_source_dir = os.path.join(self.source_folder, self.source_subfolder)
        shutil.copy("patches/Demo/CMakeLists.txt",
                    os.path.join(cxsparse_source_dir, "Demo", "CMakeLists.txt"))
        shutil.copy("patches/CMakeLists.txt",
                    os.path.join(cxsparse_source_dir, "CMakeLists.txt"))
        tools.patch(cxsparse_source_dir, "patches/cs_convert.c.diff")
        tools.patch(cxsparse_source_dir, "patches/SuiteSparse_config.h.diff")

        # Import common flags and defines
        import common

        # Generate Cmake wrapper
        common.generate_cmake_wrapper(
            cmakelists_path='CMakeLists.txt',
            source_subfolder=self.source_subfolder,
            build_type=self.settings.build_type
        )

        cmake = CMake(self)
        cmake.verbose = True

        if not tools.os_info.is_windows:
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"

        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("FindCXSparse.cmake", src="patches", dst=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
