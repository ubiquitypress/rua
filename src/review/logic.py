
def get_editors(review_assignment):
	press_editors = review_assignment.book.press_editors.all()
	series_editor = review_assignment.book.series.editor

	press_editor_list = [{'editor': editor, 'isSeriesEditor': False} for editor in press_editors]

	if series_editor:
		series_editor_list = [{'editor': series_editor, 'isSeriesEditor': True}]
	else:
		series_editor_list = []

	return (press_editor_list + series_editor_list)


def has_additional_files(submission):
	additional_files = [_file for _file in submission.files.all() if _file.kind == 'additional']
	return True if additional_files else False