# This file defines how PyOxidizer application building and packaging is
# performed. See PyOxidizer's documentation at
# https://pyoxidizer.readthedocs.io/en/stable/ for details of this
# configuration file format.


def make_exe():

    dist = default_python_distribution()
    python_config = dist.make_python_interpreter_config()
    python_config.run_command = "from yartsu.cli import main;main()"

    exe = dist.to_python_executable(name="yartsu", config=python_config)

    exe.add_python_resources(exe.pip_install(["."]))

    return exe

def make_embedded_resources(exe):
    return exe.to_embedded_resources()

def make_install(exe):
    # Create an object that represents our installed application file layout.
    files = FileManifest()

    # Add the generated executable to our install layout in the root directory.
    files.add_python_resource("yartsu", exe)

    return files

# Tell PyOxidizer about the build targets defined above.
register_target("exe", make_exe)
# register_target("resources", make_embedded_resources, depends=["exe"], default_build_script=True)
register_target("install", make_install, depends=["exe"], default=True)

resolve_targets()
