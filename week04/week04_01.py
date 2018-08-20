import tempfile
import os


class File:
    def __init__(self, file_path):
        self.file_path = file_path
        self.next_line_index = 0
        self.lines = []
        self.line_count = 0

        try:
            self.read_lines_from_file()
        except IOError:
            pass

    def read_lines_from_file(self):
        with open(self.file_path, "r") as f:
            self.lines = f.readlines()
            self.line_count = len(self.lines)

    def write(self, text):
        with open(self.file_path, "w") as f:
            f.write(text)

        self.read_lines_from_file()

    def __add__(self, other):
        with open(self.file_path, "r") as first:
            first_content = first.read()
        with open(other.file_path, "r") as second:
            second_content = second.read()

        result_file_name = os.path.split(self.file_path)[1] + os.path.split(other.file_path)[1]
        result_file_path = os.path.join(tempfile.gettempdir(), result_file_name)
        result_content = first_content + second_content
        with open(result_file_path, "w") as result:
            result.write(result_content)

        return File(result_file_path)

    def __str__(self):
        return self.file_path

    def __iter__(self):
        return self

    def __next__(self):
        if self.next_line_index >= self.line_count:
            raise StopIteration
        else:
            line = self.lines[self.next_line_index]
            self.next_line_index += 1
            return line


def main():
    temp_file_path = "./test.txt"
    file = File(temp_file_path)

    for l in File(temp_file_path):
        print(l)

    file.write("some string\n")
    for l in File(temp_file_path):
        print(l)

    os.remove(temp_file_path)

    first = File('./first.txt')
    second = File('./second.txt')

    new_obj = first + second
    print(new_obj)
#    with open(new_obj.file_path, "r") as new_file:
#        content = new_file.read()
#        print("result content:\n", content, sep="")

    for l in File(new_obj.file_path):
        print(l)


# main()
