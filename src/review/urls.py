from django.urls import re_path

from .views import (
    RequestedReviewerDecisionEmail,
    review,
    review_complete,
    review_complete_no_redirect,
    review_request_declined,
    ReviewCompletionEmail,
    reviewer_dashboard,
    reviewer_decision,
)
from review.logic import generate_review_form

urlpatterns = [
    re_path(
        r'dashboard/$',
        reviewer_dashboard,
        name='reviewer_dashboard'
    ),
    re_path(  # Reviewer decision.
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/assignment/'
        r'(?P<review_assignment_id>\d+)/decision/$',
        reviewer_decision,
        name='reviewer_decision_without'
    ),
    re_path(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/assignment/'
        r'(?P<review_assignment_id>\d+)/decision/(?P<decision>[-\w]+)/$',
        reviewer_decision,
        name='reviewer_decision_with'
    ),
    re_path(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/assignment/'
        r'(?P<review_assignment_id>\d+)/access_key/(?P<access_key>[-\w+]+)/'
        r'decision/$',
        reviewer_decision,
        name='reviewer_decision_without_access_key'
    ),
    re_path(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/assignment/'
        r'(?P<review_assignment_id>\d+)/access_key/(?P<access_key>[-\w+]+)/'
        r'decision/(?P<decision>[-\w]+)/$',
        reviewer_decision,
        name='reviewer_decision_with_access_key'
    ),
    re_path(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/assignment/'
        r'(?P<review_assignment_id>\d+)/decision-email/'
        r'(?P<decision>accept|decline)/$',
        RequestedReviewerDecisionEmail.as_view(),
        name='reviewer_decision_email'
    ),
    re_path(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/assignment/'
        r'(?P<review_assignment_id>\d+)/decision-email/'
        r'(?P<decision>accept|decline)/access_key/(?P<access_key>[-\w+]+)/$',
        RequestedReviewerDecisionEmail.as_view(),
        name='reviewer_decision_email_with_access_key'
    ),
    re_path(  # Review.
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/review-round/'
        r'(?P<review_round>\d+)/access_key/(?P<access_key>[-\w+]+)/$',
        review,
        name='review_with_access_key'
    ),
    re_path(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/'
        r'review-round/(?P<review_round>\d+)/$',
        review,
        name='review_without_access_key'
    ),
    re_path(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/'
        r'review-round/(?P<review_round>\d+)/assignment/'
        r'(?P<review_assignment_id>\d+)/completion-email/$',
        ReviewCompletionEmail.as_view(),
        name='review_completion_email'
    ),
    re_path(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)'
        r'/review-round/(?P<review_round>\d+)/assignment/'
        r'(?P<review_assignment_id>\d+)/completion-email/'
        r'access_key/(?P<access_key>[-\w+]+)/$',
        ReviewCompletionEmail.as_view(),
        name='review_completion_email_with_access_key'
    ),
    re_path(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/review-round/'
        r'(?P<review_round>\d+)/complete/$',
        review_complete,
        name='review_complete'
    ),
    re_path(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/review-round/'
        r'(?P<review_round>\d+)/access_key/(?P<access_key>[-\w+]+)/complete/$',
        review_complete,
        name='review_complete_with_access_key'
    ),
    re_path(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/review-round/'
        r'(?P<review_round>\d+)/complete/no-redirect/$',
        review_complete_no_redirect,
        name='review_complete_no_redirect'
    ),
    re_path(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/review-round/'
        r'(?P<review_round>\d+)/access_key/(?P<access_key>[-\w+]+)/'
        r'complete/no-redirect/$',
        review_complete_no_redirect,
        name='review_complete_with_access_key_no_redirect'
    ),
    re_path(
        r'^review/review-request-declined/$',
        review_request_declined,
        name='review_request_declined'
    ),
    re_path(  # Other.
        r'^download/(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/'
        r'assignment/(?P<review_id>\d+)/$',
        generate_review_form,
        name='generate_review_form'
    ),
    re_path(
        r'^download/(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/'
        r'assignment/(?P<review_id>\d+)/access_key/(?P<access_key>[-\w+]+)/$',
        generate_review_form,
        name='generate_review_form_access_key'
    ),
]
