from conans import ConanFile, CMake, tools

class OpenCLICDLoaderConan(ConanFile):
    name = "opencl-icd"
    settings = "os", "arch", "build_type", "compiler"
    version = "20181106"
    requires = "opencl-headers/[>=0]@mmha/testing"
    exports_sources = "*"
    no_copy_source = True

    def build(self):
        cmake = CMake(self)
        cmake.definitions["OPENCL_INCLUDE_DIRS"] = ";".join(self.deps_cpp_info["opencl-headers"].include_paths)
        cmake.configure()
        cmake.build()
    
    def package(self):
        self.copy("*.dll", "bin", "", keep_path=False)
        self.copy("*.lib", "lib", "", keep_path=False)
        self.copy("*.dylib*", "lib", "", keep_path=False)
        self.copy("*.so", "lib", "", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
