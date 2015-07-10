from django.contrib import admin
from models import *

admin_list = [
    (Proposal,),
    (SubmissionChecklistItem,),
    (ProposalReview,),
]

[admin.site.register(*t) for t in admin_list]
