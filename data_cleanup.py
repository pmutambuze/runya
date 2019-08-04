import json


def do_clean(language, output_raw_words=False):
	data = ""
	with open(f"raw_{language}.txt", 'rb') as file:
		print("Reading file...")
		data = str(file.read())

	print("Read done.")
	data = data.lower()
	print("Lowercase done.")
	data = data.replace(' ', "\n")
	print("Replace done.")
	final_data = ""
	for letter in data:
		if letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', "'", "’", '\n']:
			final_data += letter
		else:
			print("Skipping letter.")

	final_data = final_data.split("\n")
	final_data.sort()
	final_data = [word for word in final_data if word is not ""]

	dictionary = {}
	for word in final_data:
		try:
			dictionary[word] += 1
		except KeyError:
			dictionary[word] = 1

	with open(f"{language}.json", 'w') as file:
		print("Writing to .json file")
		file.write(str(json.dumps(dictionary)))
		print("Done.")

	if output_raw_words:
		raw_word_list = list(final_data)
		raw_words = "\n".join(raw_word_list)

		with open(f"{language}.txt", 'w') as file:
			print("Writing to .txt file")
			json.loads(json.dumps(dictionary), encoding='utf8')
			file.write(raw_words)


do_clean('runya')
do_clean('luganda', True)
