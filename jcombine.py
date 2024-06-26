"""jcombine.py"""

import os
import sys

VERSION_NUMBER = "1.0.0"
CREDITS = "Created by Mehrshad Khansarian at Tehran Polytechnic"
START_DATE = "Started Ordibehesht '82"
LAST_UPDATE = "Last updated Ordibehesht '83"

def has_main_method(file) -> bool:
    with open(file, "r", encoding="utf-8") as input_file:
        while True:
            line = input_file.readline()

            if line.strip().startswith("public static void main"):
                return True

            if not line:
                break

        return False

def contains_item_ending_with(txt: str, strings) -> bool:
    """Returns true if the list contains and item ending with 'txt'."""
    for string in strings:
        if string.endswith(txt):
            return True
        
    return False

def remove_element_ending_with(txt, my_list) -> bool:
    """Returns true if found and removed, otherwise false."""
    for item in my_list:
        if item.endswith(txt):
            my_list.remove(item)
            return True

    return False

def get_java_files(file_paths):
    """Returns all files paths ending in '.java'."""
    final_file_paths = [file_path for file_path in file_paths \
            if file_path.endswith(".java")]
    
    return final_file_paths

def get_all_file_paths(directory_path: str):
    """Retrieve full file paths to all the files in the current directory """
    """and all subsequent subdirecctories."""
    file_paths = []

    for dirpath, dirnames, filenames in os.walk(directory_path):
        for filename in filenames:
            file_paths.append(os.path.join(dirpath, filename))

    return file_paths

def main():
    directory_path: str
    output_file_path: str

    if len(sys.argv) == 1:
        # Custom, pre-defined paths for ease of use.
        directory_path = "$HOME/Desktop/programs/uni/2/hw/"
        "hw3/HW3/src/main/java/com/example"
        output_file_path = "$HOME/Desktop/temp/main/Main.java"
    elif len(sys.argv) == 2:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print("usage: python3 jcombine.py source_dir target_file")
            print("       A source file with the same name as the target file ")
            print("       must be present in the source directory (or its subdirectories).")
            print()
            print("       Use [-v | --version] for version information.")
        elif sys.argv[1] == '-v' or sys.argv[1] == '--version':
            print(f"v{VERSION_NUMBER}")
            print(CREDITS)
            print(START_DATE)
            print(LAST_UPDATE)

        sys.exit()
    elif len(sys.argv) == 3:
        directory_path = sys.argv[1]
        output_file_path = sys.argv[2]
    else:
        print("error: invalid usage", file=sys.stderr)
        print("usage: python3 jcombine.py source_dir target_file", file=sys.stderr)
        print("use `--help' option for more help", file=sys.stderr)
        sys.exit()

    # Expand shell variables in each path.
    directory_path = os.path.expandvars(directory_path)
    output_file_path = os.path.expandvars(output_file_path)

    if not os.path.isdir(directory_path):
        print(f"error: {directory_path} does not exist or is not a directory", \
                file=sys.stderr)
        sys.exit()

    imports = set()

    file_paths = get_all_file_paths(directory_path)
    file_paths = get_java_files(file_paths)

    dirname_of_output_file = os.path.dirname(output_file_path)
    if dirname_of_output_file == directory_path:
        print("error: target_file shall not be in source_dir", \
                file=sys.stderr)
        print("       please provide another location for target_file", \
                file=sys.stderr)
        sys.exit()

    main_filename = os.path.basename(output_file_path)
    if not contains_item_ending_with(main_filename, file_paths):
        print(f"error: no {main_filename} found in {directory_path}", \
                file=sys.stderr)
        sys.exit()

    main_file_path_in_directory_path = os.path.join(directory_path, main_filename) 
    if not has_main_method(main_file_path_in_directory_path):
        print(f"error: {main_filename} does not include "
        "the main method, i.e., public static void main(...)", file=sys.stderr)
        sys.exit()

    main_file_path: str
    for file_path in file_paths:
        if file_path.endswith(main_filename):
            main_file_path = file_path
            break

    file_paths.insert(0, file_paths.pop(file_paths.index(main_file_path)))

    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as input_file:
            while True:
                line = input_file.readline()

                if not line or line.startswith("public"):
                    break

                if line.startswith("import"):
                    imports.add(line)

    java_imports = [import_statement for import_statement in imports \
            if import_statement.startswith("import java")]

    try:
        output_file = open(output_file_path, "w", encoding="utf-8")
    except OSError:
        print("error: cannot open output file", file=sys.stderr)
        sys.exit()

    output_file.write("// Combined into a single file with jcombine.py\n")

    with open(main_file_path, "r", encoding="utf-8") as input_file:
        line = input_file.readline()
        if line.startswith("package"):
            # Whether to include the package name.
            # output_file.write(line)
            pass
        output_file.write("\n")

        for line in java_imports:
            output_file.write(line)

        file_paths.remove(main_file_path)
        while True:
            line = input_file.readline()

            if not line:
                break
            
            if line.startswith("import"):
                continue

            output_file.write(line)

    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as input_file:
            while True:
                line = input_file.readline()

                if not line:
                    output_file.write("\n")
                    break

                if line.startswith("import") or line.startswith("package"):
                    continue

                if (line.startswith("public class")
                        or line.startswith("public abstract class")
                        or line.startswith("public enum")
                        or line.startswith("public interface")):
                    line = line.removeprefix("public ")
                output_file.write(line)

    output_file.close()

if __name__ == '__main__':
    main()
