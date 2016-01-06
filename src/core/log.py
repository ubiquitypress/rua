from core import models

def add_log_entry(book, user, kind, message, short_name):
	new_log_entry = models.Log(book=book, user=user, kind=kind, message=message, short_name=short_name)
	new_log_entry.save()
	return new_log_entry

def add_proposal_log_entry(proposal, user, kind, message, short_name):
	new_log_entry = models.Log(proposal=proposal, user=user, kind=kind, message=message, short_name=short_name)
	new_log_entry.save()
	return new_log_entry
	
def add_email_log_entry(book, subject, from_address, to, bcc, cc, content,attachment):
	log_dict = {
		'book': book,
		'subject': subject,
		'from_address':from_address,
		'to': to if to else '',
		'cc': cc if cc else '',
		'bcc': bcc if bcc else '',
		'content': content,
	}
	new_log_entry = models.EmailLog(**log_dict)
	new_log_entry.save()
	new_log_entry.attachment.add(attachment)
	new_log_entry.save()
	return new_log_entry