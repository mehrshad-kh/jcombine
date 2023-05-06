"""jcombine.py"""

import os
import sys

directory_path: str
output_file_path: str

if len(sys.argv) == 1:
    # Custom, pre-defined paths for ease of use.
    directory_path = "/Users/mehrshadkh./Desktop/programs/uni/2/hw/hw3/HW3/src/main/java/com/example"
    output_file_path = "/Users/mehrshadkh./Desktop/temp/main/Main.java"
elif len(sys.argv) == 3:
    directory_path = sys.argv[1]
    output_file_path = sys.argv[2]
else:
    print("error: invalid input")
    print("usage: python3 jcombine.py source_dir target_file")
    sys.exit()

imports = set()

try:
    filenames = os.listdir(directory_path)
except FileNotFoundError:
    print("error: not a directory")
    sys.exit()

for filename in filenames:
    if not filename.endswith(".java"):
        filenames.remove(filename)

main_filename = output_file_path.split("/")[-1]

if main_filename in filenames:
    filenames.remove(main_filename)
else:
    print(f"error: no {main_filename} was found")
    sys.exit()
filenames.insert(0, main_filename)

for filename in filenames:
    input_file = open(os.path.join(directory_path, filename), "r", encoding="utf-8")

    while True:
        line = input_file.readline()

        if not line or line.startswith("public"):
            break

        if line.startswith("import"):
            imports.add(line)
    input_file.close()

try:
    output_file = open(output_file_path, "w", encoding="utf-8")
except OSError:
    print("error: file doesn't exist")
    sys.exit()

input_file = open(os.path.join(directory_path, main_filename), "r", encoding="utf-8")
line = input_file.readline()
if line.startswith("package"):
    # Whether to the include package name.
    output_file.write(line)
    # pass
output_file.write("\n")

for line in imports:
    output_file.write(line)

filenames.remove(main_filename)
while True:
    line = input_file.readline()

    if not line:
        break
    elif line.startswith("import"):
        continue
    output_file.write(line)
input_file.close()

for filename in filenames:
    input_file = open(os.path.join(directory_path, filename), "r", encoding="utf-8")

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
