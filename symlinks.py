"""symlinks.py

Creates a set of symbolic links for the files in this repository in
the Arduino installation include directory.

symlinks.py usage:

    python symlinks.py -i  -a ~/arduino_installation_path # Creates or refreshes links to the files
    python symlinks.py -r  -a ~/arduino_installation_path # Removes links to the files

Authors:
Peter Polidoro polidorop@janelia.hhmi.org

"""
import sys
import os
import argparse
import platform

USERDIR = os.path.expanduser('~')

def create_include_installation_path(arduino_installation_path):
    include_installation_path = None
    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        # /hardware/tools/avr/lib/avr/include/
        include_path = os.path.join('hardware','tools','avr','lib','avr','include')
        include_installation_path = os.path.join(arduino_installation_path,include_path)
        if not os.path.exists(include_installation_path) and not os.path.isdir(include_installation_path):
            raise RuntimeError('Include path does not exist within Arduino installation path!')
    elif platform.system() == 'Windows':
        sys.exit(0)
    return include_installation_path

def create_symlinks(arduino_installation_path):

    # Create include installation path
    include_installation_path = create_include_installation_path(arduino_installation_path)

    # Create symbolic links
    src_paths, dst_paths = get_paths(include_installation_path)
    for src, dst in zip(src_paths, dst_paths):
        if os.path.exists(dst):
            if not os.path.islink(dst):
                print('{0} exists and in not a symbolic link - not overwriting'.format(dst))
                continue
            else:
                print('unlinking {0}'.format(dst))
                os.unlink(dst)
        # Create symbolic link
        print('creating new symbolic link {0}'.format(dst))
        os.symlink(src,dst)

def remove_symlinks(arduino_installation_path):

    # Create include installation path
    include_installation_path = create_include_installation_path(arduino_installation_path)

    if not os.path.isdir(include_installation_path):
        return

    # Remove symbolic links
    src_paths, dst_paths = get_paths(include_installation_path)
    for dst in dst_paths:
        if os.path.islink(dst):
            print('removing symbolic link {0}'.format(dst))
            os.unlink(dst)

def get_paths(include_installation_path):
    """
    Get source and destination paths for symbolic links
    """
    current_path = os.path.abspath(os.path.curdir)
    include_path = os.path.join(current_path,'include')
    path_list = os.listdir(include_path)
    src_paths = []
    dst_paths = []
    for item in path_list:
        src = os.path.join(include_path,item)
        if os.path.isfile(src):
            dst = os.path.join(include_installation_path,item)
            src_paths.append(src)
            dst_paths.append(dst)
    return src_paths, dst_paths

class ValidPathCheckAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values

        if not os.path.exists(prospective_dir) and not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError('{0} is not a valid path!'.format(prospective_dir))

        hardware_path = os.path.join(prospective_dir,'hardware')
        if not os.path.exists(hardware_path) and not os.path.isdir(hardware_path):
            raise argparse.ArgumentTypeError('{0} is not a valid Arduino installation path!'.format(prospective_dir))

        if os.access(prospective_dir, os.R_OK):
            setattr(namespace, self.dest, os.path.realpath(prospective_dir))
            return

        raise argparse.ArgumentTypeError('{0} is not a readable path'.format(prospective_dir))

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='avr-stl Library Symlinks')
    parser.add_argument('-i','--install',
                        help='Install all of the files in this repository to the specified Arduino installation path as a set of symbolic links.',
                        action='store_true')
    parser.add_argument('-r','--remove',
                        help='Remove all of the symbolic links of the files from this repository from the specified Arduino installation path.',
                        action='store_true')
    parser.add_argument('-a','--arduino-installation-path',
                        help='Arduino installation path. e.g. ~/arduino-1.0.6',
                        action=ValidPathCheckAction,
                        required=True)

    args = parser.parse_args()
    if args.remove:
        remove_symlinks(args.arduino_installation_path)
    else:
        create_symlinks(args.arduino_installation_path)
