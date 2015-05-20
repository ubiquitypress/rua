from core import models

def add_log_entry(book, user, kind, message, short_name):
	new_log_entry = models.Log(book=book, user=user, kind=kind, message=message, short_name=short_name)
	new_log_entry.save()
	return new_log_entry