# from functions.get_files_info import get_files_info


# print(f"Result for current directory:\n{get_files_info('calculator', '.')}")
#
# print(f"Result for 'pgk' directory:\n{get_files_info('calculator', 'pkg')}")
#
# print(f"Result for '/bin' directory:\n{get_files_info('calculator', '/bin')}")
#
# print(f"Result for '../' directory:\n{get_files_info('calculator', '../')}")

# from functions.get_file_content import get_file_content
#
#
# print(f'Result for file "main.py":\n{get_file_content("calculator", "main.py")}')
#
# print(
#     f'Result for file "pkg/calculator.py":\n{get_file_content("calculator", "pkg/calculator.py")}'
# )
#
# print(
#     f"Result for file outside work_directory:\n{get_file_content('calculator', '/bin/cat')}"
# )
#
# print(
#     f"Result for non existing file:\n{get_file_content('calculator', 'pkg/does_not_exist.py')}"
# )

from functions.write_file import write_file


print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))


print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

print(write_file("calculator", "/tmp/temp.txt", "this sould not be allowed"))
