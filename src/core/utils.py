from pprint import pprint

def get_referrer(request):
	pprint (request.__dict__)
	for i in request:
		pprint (i)