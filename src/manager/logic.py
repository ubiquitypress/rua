import random

def generate_password():

	alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	pw_length = 8
	mypw = ""

	for i in range(pw_length):
	    next_index = random.randrange(len(alphabet))
	    mypw = mypw + alphabet[next_index]

	return mypw