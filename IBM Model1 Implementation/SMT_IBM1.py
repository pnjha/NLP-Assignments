from nltk.translate import AlignedSent
from nltk.translate import IBMModel1
import codecs
import re

def print_dict(dictionary):
	for key in dictionary.items():
		print(key[0])

def read_file(file_name):
	temp_dict = {}
	sentence_list = []
	with codecs.open(file_name, encoding='utf-8') as file:
	    for line in file:
	    	sentence_list.append(line)
	    	l = re.split("\s",line)
	    	for item in l:
	    		temp_dict[item] = 0
	return temp_dict, sentence_list

def initialize_translation_probabilty(english_dict,hindi_dict):
	temp_dict = {}
	for eng_word, val1 in english_dict.items():
		temp_dict[eng_word] = {}
		for hindi_word, val2 in hindi_dict.items():
			temp_dict[eng_word][hindi_word] = 0.1
	return temp_dict

def initialize_count_total(english_dict,hindi_dict):
	total = {}
	count = {}
	for eng_word, val1 in english_dict.items():
		count[eng_word] = {}
		for hindi_word, val2 in hindi_dict.items():
			total[hindi_word] = 0
			count[eng_word][hindi_word] = 0
	return count,total

def perform_learning(translational_probenglish_dict,english_dict,hindi_dict,english_list, hindi_list):

	interation = 100
	while(interation>0):

		interation -= 1
		count, total = initialize_count_total(english_dict,hindi_dict)
		for i in range(len(english_list)):
			eng = re.split("\s",english_list[i])
			hindi = re.split("\s",hindi_list[i])
			stotal = {}
			for e in eng:
				stotal[e] = 0
				for h in hindi:
					stotal[e] += translational_prob[e][h]
			for e in eng:
				for h in hindi:
					count[e][h] += translational_prob[e][h]/stotal[e]
					total[h] += translational_prob[e][h]/stotal[e]

		for h,val1 in hindi_dict.items():
			for e,val2 in english_dict.items():
				translational_prob[e][h] = count[e][h]/total[h]

	return translational_prob

def create_corpus(english_list,hindi_list):
	corpus = []
	for i in range(len(english_list)):
		corpus.append(AlignedSent(re.split("\s",english_list[i]),re.split("\s",hindi_list[i])))
	return corpus

def get_alignment_error_rate(refernce_model,alignment):
	aer = 0
	for i in range(len(english_list)):
		ref = refernce_model.alignment
	
		aer += alignment_error_rate(ref, test)

	# ref = Alignment([(0, 0), (1, 1), (2, 2)])
	# test = Alignment([(0, 0), (1, 2), (2, 1)])
	return aer/(len(english_list))

hindi_dict, hindi_list = read_file('dev.hi')
english_dict, english_list = read_file('dev.en')
translational_prob = initialize_translation_probabilty(english_dict,hindi_dict)
translational_prob = perform_learning(translational_prob,english_dict,hindi_dict,english_list,hindi_list)

ibm1 = IBMModel1(bitext, 5)

for item , val in english_dict.items():
	word = ""
	max_prob = 0
	for words, prob in translational_prob[item].items():
		if prob > max_prob:
			word = words
			max_prob = prob

	english_dict[item] = word


print(english_dict)
