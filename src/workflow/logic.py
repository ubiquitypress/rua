from django.db.models import Max

from core import models
from core import email

import json

def order_data(data, relations):
    ordered_data = []
    for relation in relations:
        if relation.element.name in data:
            ordered_data.append([relation.element.name, data[relation.element.name]])
    return ordered_data

def decode_json(json_data):
    return json.loads(json_data)

def encode_data(data):
    return json.dumps(data)

def create_new_review_round(book):
	latest_round = models.ReviewRound.objects.filter(book=book).aggregate(max=Max('round_number'))
	next_round = latest_round.get('max')+1 if latest_round.get('max') > 0 else 1
	return models.ReviewRound.objects.create(book=book, round_number=next_round)

def send_proposal_declone(proposal, email_text):
    from_email = models.Setting.objects.get(group__name='email', name='from_address')

    context = {
        'proposal': proposal,
    }

    email.send_email('[abp] Proposal Declined', context, from_email.value, proposal.owner.email, email_text)


    
