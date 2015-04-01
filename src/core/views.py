from django.shortcuts import render

def index(request):

	template = "core/index.html"
	context = {}

	return render(request, template, context)