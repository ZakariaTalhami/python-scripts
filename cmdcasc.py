import os
import sys
import subprocess
from pprint import pprint


class CascadeCmdInFolder:

    @staticmethod
    def cascade(base, command):
        """
            Cascade and run a windows cmd command in all first level sub-folders in the specified base folder.
            New cmd consoles will be opened for each sub-folder in the base directory. The passed command will be
            executed in these consoles
        :param base: Base Directory to run the script and apply to its sub-folders
        :param command: The windows cmd command to be cascaded into the subfolders
        :return:
        """
        if not os.path.isdir(base) and base != "." and base != "..":
            return False
        old_path = os.getcwd()
        os.chdir(base)

        folderLst = [x for x in os.listdir(os.getcwd()) if os.path.isdir(x)]

        print("List of Directories in {} :>".format(os.getcwd()))
        pprint(folderLst)
        print("Cascading Command through the directory list:>")
        for folder in folderLst:
            try:
                print("\t---------------------------------------")
                print("\tCascading to {} folder ".format(folder))
                os.chdir(folder)
                subprocess.call("start cmd /k {}".format(command), shell=True)
                os.chdir("..")
            except PermissionError:
                print("\t\tFolder {} cant be access, permission denied".format(folder))
        os.chdir(old_path)
        return True


if __name__ == '__main__':
    """
        If the script is run as main through the cmd, then the script will take an optional Base directory and 
        a cmd command that is preceded by '/c'
        
        Examples: 
        python {0} /c mvn clean install
        python {0} c:/cakeland /c mkdir frosting 
        python {0} .. /c dir
    """.format(__file__)
    try:
        cmd_index = sys.argv.index('/c') # get the Start of The command
    except ValueError:
        cmd_index = -1  # '/c' must be specified to indicate the command
        print("Usage: Must supply a command")
        print("Eg: python {} /c command".format(os.path.basename(__file__)))
        exit(1)

    command = " ".join(sys.argv[cmd_index + 1:])
    folder = " ".join(sys.argv[1:cmd_index])    # Base Folder is all before command
    if not folder:  # if not specified otherwise us the current directory
        folder = os.getcwd()

    if not CascadeCmdInFolder.cascade(folder, command):
        print("Usage: Folder does not exists")
        exit(1)

    exit(0)
