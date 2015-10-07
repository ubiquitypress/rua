def handle_copyedit_file(file, book, copyedit, kind):

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

	new_file = models.File(
		mime_type=file_mime,
		original_filename=original_filename,
		uuid_filename=filename,
		stage_uploaded=1,
		kind=kind,
		owner=copyedit.copyeditor,
	)
	new_file.save()

	return new_file

def handle_index_file(file, book, index, kind):

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

	new_file = models.File(
		mime_type=file_mime,
		original_filename=original_filename,
		uuid_filename=filename,
		stage_uploaded=1,
		kind=kind,
		owner=index.indexer,
	)
	new_file.save()

	return new_file


def handle_typeset_file(file, book, typeset, kind):

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

	new_file = models.File(
		mime_type=file_mime,
		original_filename=original_filename,
		uuid_filename=filename,
		stage_uploaded=1,
		kind=kind,
		owner=typeset.typesetter,
	)
	new_file.save()

	return new_file

