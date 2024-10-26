# PortableBinary.py
# Copyright (c) 2024 Jazzzny

import argparse
import os
import shutil
import subprocess

version = "1.0.0"

class PortableBinary:
    def __init__(self, args):
        self.args = args

    def run(self):
        print(f"Input binary: {self.args.binary}")
        print(f"Output directory: {self.args.output_dir}")

        if self.args.lib_dir_name == "":
            self.args.lib_dir_name = "lib"
        else:
            print(f"Library directory name: {self.args.lib_dir_name}")

        # if the output directory doesn't exist, create it
        if not os.path.exists(self.args.output_dir):
            os.makedirs(self.args.output_dir)

        # copy the binary to the output directory
        shutil.copy(self.args.binary, self.args.output_dir)

        # get the dependencies of the binary
        dependencies = self.get_dependencies_recursive(self.args.binary)

        print(f"All Dependencies:")
        for dependency in dependencies:
            print(f"  {dependency}")

        # copy the dependencies to a lib directory in the output directory
        lib_dir = os.path.join(self.args.output_dir, self.args.lib_dir_name)
        if not os.path.exists(lib_dir):
            os.makedirs(lib_dir)

        for dependency in dependencies:
            shutil.copy(dependency, lib_dir)
            self.install_name_tool_lib(os.path.join(lib_dir, os.path.basename(dependency)))

            if not self.args.no_codesign:
                self.codesign_lib(os.path.join(lib_dir, os.path.basename(dependency)))

        self.install_name_tool_bin(os.path.join(self.args.output_dir, os.path.basename(self.args.binary)))

        if not self.args.no_codesign:
            self.codesign_bin(os.path.join(self.args.output_dir, os.path.basename(self.args.binary)))

        print("Done")

        return 0

    def get_dependencies(self, binary):
        dependencies = subprocess.check_output(["otool", "-L", binary]).decode("utf-8").split("\n")
        dependencies = [dependency.strip() for dependency in dependencies if dependency.strip() != "" and dependency.startswith("\t")]
        dependencies = [dependency for dependency in dependencies if not f"/usr/lib/" in dependency and not "/System/Library/" in dependency]
        dependencies = [dependency.split(" ")[0] for dependency in dependencies]

        return dependencies

    def get_dependencies_recursive(self, binary, seen_dependencies=None):
        if seen_dependencies is None:
            seen_dependencies = set()

        dependencies = self.get_dependencies(binary)

        print(f"Dependencies for {binary}:")
        for dependency in dependencies:
            print(f"  {dependency}")

        for dependency in dependencies:
            if dependency not in seen_dependencies:
                seen_dependencies.add(dependency)
                self.get_dependencies_recursive(dependency, seen_dependencies)

        return seen_dependencies

    def install_name_tool_lib(self, lib):
        # add rpath to lib
        subprocess.run(["install_name_tool", "-add_rpath", f"@loader_path/{self.args.lib_dir_name}", lib])

        # change the id of lib
        subprocess.run(["install_name_tool", "-id", os.path.join("@loader_path", os.path.basename(lib)), lib])

        # change the dependencies of lib
        dependencies = self.get_dependencies(lib)
        for dependency in dependencies:
            new_dependency = os.path.join("@loader_path", os.path.basename(dependency))
            # if its already changed, don't change it again
            if new_dependency != dependency:
                print(f"Changing dependency {dependency} to {new_dependency} in {lib}")
                subprocess.run(["install_name_tool", "-change", dependency, new_dependency, lib])

    def codesign_lib(self, lib):
        print(f"Codesigning {lib}")
        subprocess.run(["codesign", "--force", "--deep", "--sign", "-", lib])

    def install_name_tool_bin(self, lib):
        # add rpath to lib
        subprocess.run(["install_name_tool", "-add_rpath", f"@loader_path/{self.args.lib_dir_name}", lib])

        # change the id of lib
        subprocess.run(["install_name_tool", "-id", os.path.join("@loader_path", os.path.basename(lib)), lib])

        # change the dependencies of lib
        dependencies = self.get_dependencies(lib)
        for dependency in dependencies:
            new_dependency = os.path.join(f"@loader_path/{self.args.lib_dir_name}", os.path.basename(dependency))
            print(f"Changing dependency {dependency} to {new_dependency} in {lib}")
            subprocess.run(["install_name_tool", "-change", dependency, new_dependency, lib])

    def codesign_bin(self, lib):
        print(f"Codesigning {lib}")
        subprocess.run(["codesign", "--force", "--deep", "--sign", "-", lib])

def parse_arguments():
    parser = argparse.ArgumentParser(description='Turn a macOS package manager-installed binary (MacPorts/Homebrew) into a portable binary.')

    parser.add_argument('binary', type=str, help='The input binary.')
    parser.add_argument('output_dir', type=str, help='The directory to output the portable binary to.')
    parser.add_argument('--lib_dir_name', type=str, default="lib", help='The name of the directory to output the dependencies to.')
    parser.add_argument('--no-codesign', action='store_true', help='Don\'t codesign the binary and dependencies.')
    parser.add_argument('--version', action='version', version=version)

    return parser.parse_args()

def main():
    args = parse_arguments()
    task = PortableBinary(args)
    task.run()

if __name__ == "__main__":
    main()