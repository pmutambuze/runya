import json
import re


def clean(word):
	if len(word) < 0:
		return word
	if word[0] == "'":
		return clean(word[1:])
	if word[-1] == "'":
		return clean(word[:-1])
	return word


def do_clean(language, output_raw_words=False):
	data = ""
	with open(f"raw_{language}.txt", 'r') as file:
		print("Reading file...")
		data = file.read()

	print("Read done.")
	data = data.lower()
	print("Lowercase done.")
	data = data.replace(' ', "\n")
	print("Replace done.")
	final_data = re.sub(r"[^\w'’\n ]", '', data)
	final_data = re.sub(r"[\d_]", '', final_data)

	final_data = final_data.split("\n")
	final_data.sort()
	final_data = [clean(word) for word in final_data if word not in ["", "'", "\n"]]

	dictionary = {}
	for word in final_data:
		try:
			dictionary[word] += 1
		except KeyError:
			dictionary[word] = 1

	with open(f"src/data/{language}.json", 'w') as file:
		print("Writing to .json file")
		file.write(str(json.dumps(dictionary)))
		print("Done.")

	if output_raw_words:
		raw_word_list = list(final_data)
		raw_words = "\n".join(raw_word_list)

		with open(f"{language}.txt", 'w') as file:
			print("Writing to .txt file")
			file.write(raw_words)


if __name__ == '__main__':
	do_clean('runya')
	do_clean('luganda')
