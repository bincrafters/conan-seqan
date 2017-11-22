#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class SeqanConan(ConanFile):
    name = "seqan"
    version = "2.3.2"
    url = "https://github.com/bincrafters/conan-seqan"
    description = "SeqAn is an open source C++ library of efficient algorithms and data structures for the analysis of sequences with the focus on biological data."
    license = "https://github.com/seqan/seqan/blob/master/LICENSE"
    author = "Alexander Zaitsev <zamazan4ik@tut.by>"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    #use static org/channel for libs in conan-center
    #use dynamic org/channel for libs in bincrafters

    def source(self):
        source_url = "https://github.com/seqan/seqan"
        tools.get("{0}/archive/seqan-v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.name + "-v" + self.version
        os.rename(extracted_dir, "sources")
        #Rename to "sources" is a convention to simplify later steps

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = False # example
        cmake.configure(source_dir="sources")
        cmake.build()

    def package(self):
        with tools.chdir("sources"):
            self.copy(pattern="LICENSE")
            self.copy(pattern="*", dst="include", src="include")
            self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.dylib", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
