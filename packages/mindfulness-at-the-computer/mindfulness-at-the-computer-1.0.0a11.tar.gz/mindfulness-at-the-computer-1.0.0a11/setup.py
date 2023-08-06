from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
# -there's no setuptools.command.uninstall (or similar)
import os
import os.path
import shutil
from string import Template
import matc.constants

"""
PLEASE NOTE: If a wheel (bdist) is installed then pip doesn't run setup.py

> pip doesn't run setup.py from a wheel hence you cannot run any post-installation code from setup.py in a wheel.
--- https://stackoverflow.com/a/56495693/2525237

See also: https://stackoverflow.com/a/24749871/2525237

If using only sdist and if the building of the wheel fails during installation (after having downloaded the sdist)
there is a deprecation warning:
```
DEPRECATION: mindfulness-at-the-computer was installed using the legacy 'setup.py install' method, because a wheel
could not be built for it. A possible replacement is to fix the wheel build issue reported above. Discussion can be
found at https://github.com/pypa/pip/issues/8368
```

bdists vary depending on the platform

More info about sdist and bdist: https://dev.to/icncsx/python-packaging-sdist-vs-bdist-5ekb

"""

setup_file_dir: str = os.path.dirname(os.path.abspath(__file__))
appl_res_dir: str = os.path.join(setup_file_dir, "matc", "res")


def do_extra_setup():
    """
    This function is called automatically during pip install. It creates a .desktop file and copies it to these dirs:
    * The user applications dir - so that the user can see the application shortcut in the menu system used by the
    desktop environment she is using
    * The autostart dir - so that the application is automatically launched on startup

    ### Menu .desktop files
    On Linux-based systems menu .desktop files are locally stored in
    ~/.local/share/applications (globally in /usr/share/applications)

    ### Autostart dir
    > $XDG_CONFIG_HOME defines the base directory relative to which user-specific configuration files should be stored.
    > If $XDG_CONFIG_HOME is either not set or empty, a default equal to $HOME/.config should be used.

    Based on the info above this is the default location: .desktop file in ~/.config/autostart

    Please note:
    * Only gnu/linux systems can run this extra setup file at the moment
    * Printouts are not written to the terminal unless the user has added the verbose flag at the end:
      `pip3 install -e . -v`

    There is no way to call a file at uninstall, but we could - in this script - create a text file with a list of the
    files that we have installed and therefore want to remove. And then have a simple script file which removes these
    files. One way to do this is described here: https://gist.github.com/myusuf3/933625 (I don't think we need to use
    sudo though)

    References:
    * Freedesktop spec:
      * https://www.freedesktop.org/wiki/Specifications/autostart-spec/
      * https://specifications.freedesktop.org/autostart-spec/autostart-spec-latest.html
    * https://doc.qt.io/qt-5/qstandardpaths.html#StandardLocation-enum
    """

    from PySide6 import QtCore
    import matc.globa
    if QtCore.QSysInfo.kernelType() != "linux":
        print("Only gnu/linux systems can run this extra setup file at the moment")
        return
    print("====Running extra setup python script extra_setup.py====")
    user_home_dir = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.HomeLocation)[0]
    user_config_dir = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.ConfigLocation)[0]
    user_applications_dir = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.ApplicationsLocation)[0]
    os.makedirs(user_applications_dir, exist_ok=True)
    user_desktop_dir = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.DesktopLocation)[0]
    os.makedirs(user_desktop_dir, exist_ok=True)
    user_autostart_dir = os.path.join(user_config_dir, "autostart")
    os.makedirs(user_autostart_dir, exist_ok=True)

    template_desktop_file_path: str = os.path.join(appl_res_dir, "mindfulness-at-the-computer[template].desktop")
    output_desktop_file_name: str = "mindfulness-at-the-computer.desktop"

    with open(template_desktop_file_path, "r") as f:
        content_str = f.read()
        template = Template(content_str)
        exec_path: str = os.path.join(user_home_dir, ".local", "bin", matc.constants.APPLICATION_NAME)
        read_icon_path: str = os.path.join(appl_res_dir, "icons", "icon.png")
        write_icon_path = matc.globa.get_config_path("icon.png")
        print(f"Copying {read_icon_path} to {write_icon_path}")
        shutil.copy(read_icon_path, write_icon_path)

        output_desktop_file_contents: str = template.substitute(exec=exec_path, icon=write_icon_path)
        with open(output_desktop_file_name, "w+") as output_file:
            output_file.write(output_desktop_file_contents)

        os.chmod(output_desktop_file_name, 0o744)
        print(f"Copying {output_desktop_file_name} to {user_applications_dir}")
        shutil.copy2(output_desktop_file_name, user_applications_dir)
        print(f"Copying {output_desktop_file_name} to {user_autostart_dir}")
        shutil.copy2(output_desktop_file_name, user_autostart_dir)
        print(f"Copying {output_desktop_file_name} to {user_desktop_dir}")
        shutil.copy2(output_desktop_file_name, user_desktop_dir)


class PostDevelopCommand(develop):
    def run(self):
        develop.run(self)
        do_extra_setup()


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        do_extra_setup()


"""
To completely uninstall/remove the application on Ubuntu, its dependencies, and .desktop files:

pip3 uninstall mindfulness-at-the-computer

$ pip3 uninstall mindfulness-at-the-computer 
Found existing installation: mindfulness-at-the-computer 1.0.0a10
Uninstalling mindfulness-at-the-computer-1.0.0a10:
  Would remove:
    /home/sunyata/.local/bin/mindfulness-at-the-computer
    /home/sunyata/.local/lib/python3.10/site-packages/matc/*
    /home/sunyata/.local/lib/python3.10/site-packages/mindfulness_at_the_computer-1.0.0a10.dist-info/*
Proceed (Y/n)? 

pip3 uninstall PySide6
pip3 uninstall shiboken6
rm ~/.local/share/applications/mindfulness-at-the-computer.desktop
rm ~/.config/autostart/mindfulness-at-the-computer.desktop
rm ~/Desktop/mindfulness-at-the-computer.desktop

"""

long_description_str = ""
# this_dir_abs_path_str = os.path.dirname(__file__)
readme_abs_path_str = os.path.join(setup_file_dir, "README.md")
try:
    with open(readme_abs_path_str, "r") as file:
        long_description_str = '\n' + file.read()
except FileNotFoundError:
    long_description_str = matc.constants.SHORT_DESCR_STR

setup(
    name=matc.constants.APPLICATION_NAME,
    version=matc.constants.APPLICATION_VERSION,
    packages=['matc', 'matc.gui'],
    url="https://mindfulness-at-the-computer.gitlab.io",
    license='GPLv3',
    author='Tord Dellsén, and others',
    author_email='tord.dellsen@gmail.com',
    description=matc.constants.SHORT_DESCR_STR,
    include_package_data=True,
    install_requires=["PySide6>=6.2"],
    entry_points={"console_scripts": [f"{matc.constants.APPLICATION_NAME}=matc.main:main"]},
    long_description_content_type='text/markdown',
    long_description=long_description_str,
    python_requires='>=3.6.0',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Other/Nonlisted Topic'
    ],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand
    }
)

print("*********************************")
print(f"{setup_file_dir=}")
print(f"{appl_res_dir=}")
print("*********************************")

"""
Ubuntu versions and Python versions:
18.04 LTS: 3.6 - f-strings,
3.7 - 
20.04 LTS: 3.8 - 
21.04: 3.9 - 
22.04 - 3.10 - 

To install earlier versions:
https://www.digitalocean.com/community/questions/how-to-install-a-specific-python-version-on-ubuntu

https://www.python.org/downloads/
tar xzvf Python-3.5.0.tgz
cd Python-3.5.0
./configure
make
sudo make install
https://askubuntu.com/a/727814/360991

sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.6
https://askubuntu.com/a/682875/360991
Doesn't work for 3.6

List of classifiers:
https://pypi.org/classifiers/

"""

