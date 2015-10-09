from django.shortcuts import redirect, render, get_object_or_404
from core.decorators import is_editor, is_book_editor, is_book_editor_or_author
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.core.urlresolvers import reverse

from core import models, log, logic as core_logic
from workflow import logic as workflow_logic
from editor import logic
from revisions import models as revision_models
from review import models as review_models
from manager import models as manager_models


@is_editor
def editor_dashboard(request):

	if request.POST:
		order = request.POST.get('order')
		filterby = request.POST.get('filter')
		search = request.POST.get('search')
	else:
		filterby = None
		search = None
		order = 'title'

	query_list = []

	if filterby:
		query_list.append(Q(stage__current_stage=filterby))

	if search:
		query_list.append(Q(title__contains=search) | Q(subtitle__contains=search) | Q(prefix__contains=search))

	if filterby:
		book_list = models.Book.objects.filter(publication_date__isnull=True).filter(*query_list).exclude(stage__current_stage='declined').order_by(order)
	else:
		book_list = models.Book.objects.filter(publication_date__isnull=True).exclude(stage__current_stage='declined').order_by(order)

	template = 'editor/dashboard.html'
	context = {
		'book_list': book_list,
		'recent_activity': models.Log.objects.all().order_by('-date_logged')[:15],
		'notifications': models.Task.objects.filter(assignee=request.user, completed__isnull=True).order_by('due'),
		'order': order,
		'filterby': filterby,
	}

	return render(request, template, context)


@is_book_editor
def editor_submission(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id)

	if request.POST and 'review' in request.POST:
		workflow_logic.create_new_review_round(book)
		book.stage.review = timezone.now()
		book.stage.current_stage = 'review'
		book.stage.save()

		if book.stage.current_stage == 'review':
			log.add_log_entry(book=book, user=request.user, kind='review', message='Submission moved to Review', short_name='Submission in Review')

		messages.add_message(request, messages.SUCCESS, 'Submission has been moved to the review stage.')

		return redirect(reverse('editor_review', kwargs={'submission_id': book.id}))

	template = 'editor/submission.html'
	context = {
		'submission': book,
		'active': 'user_submission',
		'author_include': 'editor/submission_details.html',
		'submission_files': 'editor/submission_files.html'
	}

	return render(request, template, context)

@is_book_editor
def editor_tasks(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id)

	tasks = logic.get_submission_tasks(book, request.user)

	template = 'editor/submission.html'
	context = {
		'submission': book,
		'active': 'user_submission',
		'author_include': 'shared/tasks.html',
		'tasks': tasks,
	}

	return render(request, template, context)

@is_book_editor
def editor_review(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	review_rounds = models.ReviewRound.objects.filter(book=book).order_by('-round_number')

	if request.POST and 'new_round' in request.POST:
		new_round = logic.create_new_review_round(book)
		return redirect(reverse('editor_review_round', kwargs={'submission_id': submission_id, 'round_number': new_round.round_number}))
	elif request.POST and 'move_to_editing' in request.POST:
		if not book.stage.editing:
			log.add_log_entry(book=book, user=request.user, kind='editing', message='Submission moved to Editing.', short_name='Submission in Editing')
		book.stage.editing = timezone.now()
		book.stage.current_stage = 'editing'
		book.stage.save()
		return redirect(reverse('editor_editing', kwargs={'submission_id': submission_id}))

	template = 'editor/submission.html'
	context = {
		'submission': book,
		'author_include': 'editor/review_revisions.html',
		'review_rounds': review_rounds,
		'revision_requests': revision_models.Revision.objects.filter(book=book, revision_type='review')
	}

	return render(request, template, context)

@is_book_editor
def editor_review_round(request, submission_id, round_number):
	book = get_object_or_404(models.Book, pk=submission_id)
	review_round = get_object_or_404(models.ReviewRound, book=book, round_number=round_number)
	reviews = models.ReviewAssignment.objects.filter(book=book, review_round__book=book, review_round__round_number=round_number)

	review_rounds = models.ReviewRound.objects.filter(book=book).order_by('-round_number')
	internal_review_assignments = models.ReviewAssignment.objects.filter(book=book, review_type='internal', review_round__round_number=round_number).select_related('user', 'review_round')
	external_review_assignments = models.ReviewAssignment.objects.filter(book=book, review_type='external', review_round__round_number=round_number).select_related('user', 'review_round')

	template = 'editor/submission.html'
	context = {
		'submission': book,
		'author_include': 'editor/review_revisions.html',
		'submission_files': 'editor/view_review_round.html',
		'review_round': review_round,
		'review_rounds': review_rounds,
		'round_id': round_number,
		'revision_requests': revision_models.Revision.objects.filter(book=book, revision_type='review'),
		'internal_review_assignments': internal_review_assignments,
		'external_review_assignments': external_review_assignments,
	}

	return render(request, template, context)

@is_book_editor
def add_review_files(request, submission_id, review_type):
	submission = get_object_or_404(models.Book, pk=submission_id)

	if request.POST:
		files = models.File.objects.filter(pk__in=request.POST.getlist('file'))
		for file in files:
			if review_type == 'internal':
				submission.internal_review_files.add(file)
			else:
				submission.external_review_files.add(file)

		messages.add_message(request, messages.SUCCESS, '%s files added to Review' % files.count())

		return redirect(reverse('editor_review_round', kwargs={'submission_id': submission_id, 'round_number': submission.get_latest_review_round()}))

	template = 'editor/add_review_files.html'
	context = {
		'submission': submission,
	}

	return render(request, template, context)

@is_book_editor
def editor_add_reviewers(request, submission_id, review_type, round_number):

	submission = get_object_or_404(models.Book, pk=submission_id)
	reviewers = models.User.objects.filter(profile__roles__slug='reviewer')
	review_forms = review_models.Form.objects.all()
	committees = manager_models.Group.objects.filter(group_type='review_committee')
	review_round = get_object_or_404(models.ReviewRound, book=submission, round_number=round_number)

	if request.POST:
		reviewers = User.objects.filter(pk__in=request.POST.getlist('reviewer'))
		committees = manager_models.Group.objects.filter(pk__in=request.POST.getlist('committee'))
		review_form = review_models.Form.objects.get(ref=request.POST.get('review_form'))
		due_date = request.POST.get('due_date')
		email_text = request.POST.get('message')

		if request.FILES.get('attachment'):
			attachment = handle_file(request.FILES.get('attachment'), submission, 'misc', request.user)
		else:
			attachment = None

		# Handle reviewers
		for reviewer in reviewers:
			logic.handle_review_assignment(submission, reviewer, review_type, due_date, review_round, request.user, email_text, attachment)

		# Handle committees
		for committee in committees:
			members = manager_models.GroupMembership.objects.filter(group=committee)
			for member in members:
				logic.handle_review_assignment(submission, member.user, review_type, due_date, review_round, request.user, email_text, attachment)

		# Tidy up and save
		if review_type == 'internal' and not submission.stage.internal_review:
			submission.stage.internal_review = timezone.now()
			submission.stage.save()
			log.add_log_entry(book=submission, user=request.user, kind='review', message='Internal Review Started', short_name='Submission entered Internal Review')

		elif review_type == 'external' and not submission.stage.external_review:
			submission.stage.external_review = timezone.now()
			submission.stage.save()
			log.add_log_entry(book=submission, user=request.user, kind='review', message='External Review Started', short_name='Submission entered External Review')

		submission.review_form = review_form
		submission.save()

		return redirect(reverse('view_review', kwargs={'submission_id': submission.id}))

	template = 'editor/add_reviewers.html'
	context = {
		'reviewers': reviewers,
		'committees': committees,
		'active': 'new',
		'email_text': models.Setting.objects.get(group__name='email', name='review_request'),
		'review_forms': review_forms,
		'submission': submission,
	}

	return render(request, template, context)

@is_book_editor
def editor_review_assignment(request, submission_id, round_id, review_id):

	submission = get_object_or_404(models.Book, pk=submission_id)
	review_assignment = get_object_or_404(models.ReviewAssignment, pk=review_id)
	review_rounds = models.ReviewRound.objects.filter(book=submission).order_by('-round_number')
	result = review_assignment.results
	relations = review_models.FormElementsRelationship.objects.filter(form=result.form)
	data_ordered = workflow_logic.order_data(workflow_logic.decode_json(result.data), relations)

	template = 'editor/submission.html'
	context = {
		'author_include': 'editor/review_revisions.html',
		'submission_files': 'shared/view_review.html',
		'submission': submission,
		'review': review_assignment,
		'data_ordered': data_ordered,
		'result': result,
		'active': 'review',
		'review_rounds': review_rounds,
		'revision_requests': revision_models.Revision.objects.filter(book=submission, revision_type='review'),
	}

	return render(request, template, context)

@is_book_editor
def editor_editing(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id)

	if request.POST and request.GET.get('start', None):
		action = request.GET.get('start')

		if action == 'copyediting':
			book.stage.copyediting = timezone.now()
			log.add_log_entry(book=book, user=request.user, kind='editing', message='Copyediting has commenced.', short_name='Copyediting Started')
		elif action == 'indexing':
			book.stage.indexing = timezone.now()
			log.add_log_entry(book=book, user=request.user, kind='editing', message='Indexing has commenced.', short_name='Indexing Started')
		elif action == 'production':
			book.stage.production = timezone.now()
			book.stage.current_stage = 'production'
			log.add_log_entry(book=book, user=request.user, kind='production', message='Submission moved to Production', short_name='Submission in Production')
			book.stage.save()
			return redirect(reverse('editor_production', kwargs={'submission_id': submission_id}))

		book.stage.save()
		return redirect(reverse('editor_editing', kwargs={'submission_id': submission_id}))

	template = 'editor/submission.html'
	context = {
		'submission': book,
		'author_include': 'editor/editing.html',
	}

	return render(request, template, context)

@is_book_editor
def editor_production(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	typeset_assignments = models.TypesetAssignment.objects.filter(book=book)

	if request.POST and request.GET.get('start', None):
		if request.GET.get('start') == 'typesetting':
			book.stage.typesetting = timezone.now()
			book.stage.save()

	template = 'workflow/production/view.html'
	context = {
		'active': 'production',
		'submission': book,
		'format_list': models.Format.objects.filter(book=book).select_related('file'),
		'chapter_list': models.Chapter.objects.filter(book=book).select_related('file'),
		'typeset_assignments': typeset_assignments,
	}

	return render(request, template, context)

@is_book_editor
def decline_submission(request, submission_id):

	submission = get_object_or_404(models.Book, pk=submission_id)

	if request.POST and 'decline' in request.POST:
		submission.stage.declined = timezone.now()
		submission.stage.current_stage = 'declined'
		submission.stage.save()
		messages.add_message(request, messages.SUCCESS, 'Submission declined.')
		return redirect(reverse('editor_dashboard'))

	template = 'editor/decline_submission.html'
	context = {
		'submission': submission,
	}

	return render(request, template, context)

@is_book_editor
def delete_review_files(request, submission_id, review_type, file_id):
	submission = get_object_or_404(models.Book, pk=submission_id)
	file = get_object_or_404(models.File, pk=file_id)

	if review_type == 'internal':
		submission.internal_review_files.remove(file)
	else:
		submission.external_review_files.remove(file)

	return redirect(reverse('editor_review_round', kwargs={'submission_id': submission_id, 'round_number': submission.get_latest_review_round()}))

@is_book_editor
def editor_status(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id)

	template = 'editor/submission.html'
	context = {
		'submission': book,
		'active': 'user_submission',
		'author_include': 'shared/status.html',
		'submission_files': 'shared/messages.html',
		'timeline': core_logic.build_time_line(book),
	}

	return render(request, template, context)
