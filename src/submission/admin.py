from django.contrib import admin
from models import *

admin_list = [
    (Proposal,),
    (SubmissionChecklistItem,),
]

[admin.site.register(*t) for t in admin_list]
