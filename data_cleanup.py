import json

def do_clean():
	data = ""
	with open("raw.txt", 'r') as file:
		print("Reading file...")
		data = file.read()

	print("Read done.")
	data = data.lower()
	print("Lowercase done.")
	data = data.replace(' ', "\n")
	print("Replace done.")
	final_data = ""
	for letter in data:
		if letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', "’", '\n']:
			final_data += letter
		else:
			print("Skipping letter.")

	final_data = final_data.split("\n")
	final_data.sort()
	final_data = [word for word in final_data if not word is ""]

	dictionary = {}
	for word in final_data:
		try:
			dictionary[word] += 1
		except KeyError:
			dictionary[word] = 1

	# final_data_list = final_data
	final_data = "\n".join(final_data)





	with open("results.txt", 'w') as file:
		print("Writing to file")
		# file.write(str(json.dumps(dictionary)))
		file.write(final_data)
		# file.write(str(final_data_list))
		print("Done.")

do_clean()
