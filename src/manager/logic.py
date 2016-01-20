import random

from core import models, email, log

def generate_password():

	alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	pw_length = 8
	mypw = ""

	for i in range(pw_length):
	    next_index = random.randrange(len(alphabet))
	    mypw = mypw + alphabet[next_index]

	return mypw

def send_new_user_ack(email_text, new_user, code):
	from_email = models.Setting.objects.get(group__name='email', name='from_address')

	context = {
		'base_url': models.Setting.objects.get(group__name='general', name='base_url').value,
		'user': new_user,
		'code': code,
	}

	email.send_email('New User : Profile Detail', context, from_email.value, new_user.email, email_text)