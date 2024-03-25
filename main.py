import argparse
import os
import psutil
import signal


def exit_command():
    exit()


def cd_command(dir_name):
    current_directory = os.getcwd()
    parent_directory = os.path.dirname(current_directory)
    if dir_name == '..':
        os.chdir(parent_directory)
    elif dir_name == '.':
        print("Current directory:", current_directory)
    elif os.path.isdir(dir_name):
        os.chdir(dir_name)
    else:
        print(dir_name + " is not a valid directory name")


def ls_command():
    current_directory = os.getcwd()
    print(os.listdir(current_directory))


def mkdir_command(dir_name):
    if os.path.isdir(dir_name):
        print(dir_name + " already exist")
    else:
        parent_dir = os.getcwd()
        path = os.path.join(parent_dir, dir_name)
        os.mkdir(path)
        print("The directory was successfully created.")


def mkfile_command(file_name):
    if os.path.isfile(file_name):
        print(file_name + " already exist")
    else:
        with open(file_name, 'w'):
            pass
        print("The file was successfully created.")


def tree_command():
    current_directory = os.getcwd()
    for root, dirs, files in os.walk(current_directory):
        level = root.replace(current_directory, '').count(os.sep)
        indent = ' ' * 3 * level
        print('{}{}/'.format(indent, os.path.basename(root)))
        sub_indent = ' ' * 3 * (level + 1)
        for f in files:
            print('{}{}'.format(sub_indent, f))


def info_command(file_name):
    if os.path.isfile(file_name):
        print("The file: " + file_name + "\n" +
              "was created at: " + str(os.path.getctime(file_name)) + "\n" +
              "and was last modified at" + str(os.path.getmtime(file_name)))
    else:
        print(file_name + " is not a valid file name")


def tasklist_command():
    for process in psutil.process_iter(['pid', 'name']):
        print(str(process.pid) + " " + str(process.name()))


def kill_pid_by_name(process_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.name() == process_name:
            os.kill(process.pid, signal.SIGTERM)
    print("The process was successfully killed" + process_name)


def kill_command(pid):
    if not pid.isdigit():
        kill_pid_by_name(pid)
        exit(0)
    if not psutil.pid_exists(int(pid)):
        print("Incorrect pid or process name")
        exit(0)
    os.kill(int(pid), signal.SIGTERM)
    print("The process was successfully killed" + pid)


def help_command():
    text = '''
    exit: Close the program
    cd <dir_name>: Change the current directory
    ls: Display the contents of the current directory
    mkdir <dir_name>: Create a new directory with the given name as parameter
    mkfile <file_name>: Create a new file with the given name as parameter
    tree: Display the directory structure
    info <file_name>: Display information for the file given as parameter
    tasklist: Display the PID and name of all running processes.
    kill <process_name> or <PID>: Kill the process with the given name or PID
    help: Display the commands and how they works
'''
    print(text)


commands_list = {
    'cd': cd_command,
    'ls': ls_command,
    'mkdir': mkdir_command,
    'mkfile': mkfile_command,
    'tree': tree_command,
    'tasklist': tasklist_command,
    'info': info_command,
    'kill': kill_command,
    'help': help_command,
    'exit': exit_command
}


def run_console():
    parser_python_console = argparse.ArgumentParser()
    parser_python_console.add_argument('command', type=str, help='Command name')
    parser_python_console.add_argument('argument', nargs='?', type=str, help='Optional argument')
    while True:
        args = parser_python_console.parse_args(input(str(os.getcwd()) + ": ").split())
        exec_command(args)


def run_cmd():
    parser = argparse.ArgumentParser(prog='PythonCmdlineConsole',
                                     description='The program will run a console using cmdline')
    parser.add_argument('-run', '--run', nargs='?', type=str,
                        help='run without entering console mode')
    parser.add_argument('argument', nargs='?', type=str, help='Optional argument')
    parser.add_argument('-info', '--info', action='store_true', help='print help')
    return parser.parse_args()


def exec_command(args):
    if hasattr(args, 'command'):
        command_name = args.command
    else:
        command_name = args.run

    if command_name in commands_list:
        if args.argument is not None:
            commands_list[command_name](args.argument)
        else:
            commands_list[command_name]()
    else:
        print("This is not a valid command")
        help_command()


def main():
    args = run_cmd()
    if args.info:
        help_command()
        exit(0)
    if args.run:
        if args is not None:
            exec_command(args)
            exit(0)
    run_console()


if __name__ == '__main__':
    main()
