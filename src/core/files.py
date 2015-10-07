from django.shortcuts import Http404
from django.conf import settings

from core import models

import mimetypes as mime
from uuid import uuid4
import os

def handle_onetasker_file(file, book, assignment, kind):

	original_filename = str(file._get_name())
	filename = str(uuid4()) + str(os.path.splitext(original_filename)[1])
	folder_structure = os.path.join(settings.BASE_DIR, 'files', 'books', str(book.id))

	if not os.path.exists(folder_structure):
		os.makedirs(folder_structure)

	path = os.path.join(folder_structure, str(filename))
	fd = open(path, 'wb')
	for chunk in file.chunks():
		fd.write(chunk)
	fd.close()

	file_mime = mime.guess_type(filename)

	try:
		file_mime = file_mime[0]
		if not file_mime:
			file_mime = 'unknown'
	except IndexError:
		file_mime = 'unknown'

	owner = get_owner(assignment)

	new_file = models.File(
		mime_type=file_mime,
		original_filename=original_filename,
		uuid_filename=filename,
		stage_uploaded=1,
		kind=kind,
		owner=owner,
	)
	new_file.save()

	return new_file



### Helpers ###
def get_owner(assignment):

	if assignment.type() == 'copyedit':
		return assignment.copyeditor
	elif assignment.type() == 'typesetting':
		return assignment.typesetter
	elif assignment.type() == 'indexing':
		return assignment.indexer
	else:
		raise Http404
