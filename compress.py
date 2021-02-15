import sys
import os
from os import listdir
from os.path import isfile, join
import platform

def get_magic_number(binary_file_path):
	magic_number = None
	with open(binary_file_path, "rb") as bfile:
		header = bfile.read(8)
		if header:
			magic_number = ''.join([hex(byte) for byte in header])
			# print(magic_number)
			return magic_number
	return False

def same(name1, name2): 
	with open(name1, "rb") as one: 
		with open(name2, "rb") as two: 
			chunk = other = True 
			while chunk or other: 
				chunk = one.read(100) 
				other = two.read(100) 
				if chunk != other: 
					print(chunk)
					print(other)
					return False 
			return True 

# TEST	
count = 0 
applid = False
version = platform.system()

if version == "Windows":
	winsxs_path = "C:\\Windows\\WinSxS"
elif version == "Linux":
	winsxs_path = "C:/Windows/WinSxS"
else:
	print( version, " is not supported. Windows of Linux only." )
	sys.exit(0)
	
# test_file_1 = "C:\Windows\\WinSxS\\amd64_microsoft-windows-os-kernel_31bf3856ad364e35_10.0.21301.1000_none_23897fa35d7b783d\\ntoskrnl.exe"
# test_file_2 = "C:\Windows\\WinSxS\\amd64_microsoft-windows-os-kernel_31bf3856ad364e35_10.0.21301.1010_none_238a7fed5d7a9194\\ntoskrnl.exe"


# # get all sub-directories under WinSxs
for x in os.listdir(winsxs_path):
	current_path = join(winsxs_path, x)

	# TEST
	count += 1

	# skip files: xml manifest #TODO not sure if we need to consider those files
	if not os.path.isdir(current_path):
		continue

	#  only get files
	onlyfiles = [f for f in os.listdir(current_path) if os.path.isfile(os.path.join(current_path, f))]

	for file_name in onlyfiles:
		# filename and path initialization
		base_file = None
		forward_file = None
		reverse_file = None
		null_file = None
		# base file for PA 
		base_file = join(current_path, file_name)
		if version == "Windows":
			if os.path.isfile(current_path+ "\\f\\" + file_name):
				forward_file = current_path+ "\\f\\" + file_name

			if os.path.isfile(current_path+ "\\r\\" + file_name):
				reverse_file = current_path+ "\\r\\" + file_name
				
			if os.path.isfile(current_path+ "\\n\\" + file_name):
				null_file = current_path+ "\\n\\" + file_name
		elif version == "Linux":
			pass
		# forward file exist: patch applied
		if forward_file:
			magic_number = get_magic_number(forward_file)
			# PA file check method from "parse_cab_file.py" 
			if "0x500x410x330x30" in magic_number:
				# 	TODO: python delta_patch.py -i <base_file> -o <new_PA_file> <reverse_file> <forward_file>
				print(onlyfiles)
				print('base_file: ', base_file)
				print('forward_file: ', forward_file)
				print('reverse_file: ', reverse_file)
		# null file: new file added
		if null_file:
			# TODO: python delta_patch.py -n -o <new_PA_file> <null_file>
			applid = True
			print('base_file: ', base_file)
			print('null_file: ', null_file)

		# apply patches, !Important all three folders can exist at same time
		# if forward_path and reverse_path exist
		# if reverse only:
		#   TODO: something else? Not sure if this condition possible or not
		# if null_path
		# 	TODO: python delta_patch.py -n -o <new_PA_file> <null_file>

	if applid:
		sys.exit(0)