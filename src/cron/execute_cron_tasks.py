from core import models

from django.utils import timezone
from datetime import timedelta

from pprint import pprint

def remind_unaccepted_reviews(task):
	days = int(models.Setting.objects.get(group__name='cron', name='remind_unaccepted_reviews').value)
	dt = timezone.now()
	target_date = dt + timedelta(days=days)
	print target_date

	books = models.Book.objects.filter(stage__current_stage='review')

	for book in books:
		reviews = models.ReviewAssignment.objects.filter(book=book, review_round__round_number=book.get_latest_review_round(), accepted__isnull=True, declined__isnull=True, due=target_date.date)
		pprint(reviews)

def remind_accepted_reviews(task):
	pass

def remind_overdue_reviews(task):
	pass

def reminder_overdue_revisions(task):
	pass
	
