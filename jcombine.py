"""jcombine.py"""

import os
import sys

def remove_element_ending_with(txt, list):
    """Returns true if found and removed, otherwise false."""
    for item in list:
        if item.endswith(txt):
            list.remove(item)
            return True

    return False

def get_java_files(file_paths):
    """Returns all files paths ending with .java"""
    # This technique is known as list comprehension.
    final_file_paths = [file_path for file_path in file_paths if file_path.endswith(".java")]
    
    return final_file_paths


def get_all_file_paths(directory_path: str):
    """Retrieve full file paths to all the files in the current directory and all subsequent subdirecctories."""
    # Severe error: returns repeated list of file paths.
    # file_paths = []
    file_paths = set()
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for filename in filenames:
            # file_paths.append(os.path.join(dirpath, filename))
            file_paths.add(os.path.join(dirpath, filename))

        for dirname in dirnames:
            # file_paths.extend(get_all_file_paths(os.path.join(dirpath, dirname)))
            file_paths.update(get_all_file_paths(os.path.join(dirpath, dirname)))

    return file_paths

directory_path: str
output_file_path: str

if len(sys.argv) == 1:
    # Custom, pre-defined paths for ease of use.
    # directory_path = "/Users/mehrshadkh./Desktop/programs/uni/2/hw/hw3/HW3/src/main/java/com/example"
    # output_file_path = "/Users/mehrshadkh./Desktop/temp/main/Main.java"
    directory_path = "/Users/mehrshadkh./Desktop/temp/parsa-test/HW3_Q1/src/library"
    output_file_path = "/Users/mehrshadkh./Desktop/Main.java"
elif len(sys.argv) == 3:
    directory_path = sys.argv[1]
    output_file_path = sys.argv[2]
else:
    print("error: invalid input")
    print("usage: python3 jcombine.py source_dir target_file")
    sys.exit()

imports = set()

# file_paths = []
file_paths = set()

try:
    file_paths = get_all_file_paths(directory_path)
except FileNotFoundError:
    print("error: not a directory")
    sys.exit()

file_paths = get_java_files(file_paths)

main_filename = output_file_path.split("/")[-1]
main_file_path: str

for file_path in file_paths:
    if file_path.endswith(main_filename):
        main_file_path = file_path
        file_paths.remove(file_path)

# Can be done more simply.
# if not remove_element_ending_with(main_filename, file_paths):
#     print(f"error: no {main_filename} was found")
#     sys.exit()
file_paths.insert(0, main_file_path)

for file_path in file_paths:
    # Use with.
    input_file = open(file_path, "r", encoding="utf-8")

    while True:
        line = input_file.readline()

        if not line or line.startswith("public"):
            break

        if line.startswith("import"):
            imports.add(line)
    input_file.close()

java_imports = [import_statement for import_statement in imports if import_statement.startswith("import java")]

try:
    output_file = open(output_file_path, "w", encoding="utf-8")
except OSError:
    print("error: file doesn't exist")
    sys.exit()

input_file = open(main_file_path, "r", encoding="utf-8")
line = input_file.readline()
if line.startswith("package"):
    # Whether to include package name.
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
input_file.close()

for file_path in file_paths:
    input_file = open(file_path, "r", encoding="utf-8")

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
    # output_file.write("\n")
    input_file.close()

output_file.close()
