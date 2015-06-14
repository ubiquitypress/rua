from django.db import models

class Form(models.Model):

	name = models.CharField(max_length=100)
	ref = models.CharField(max_length=20, help_text='for proposals: press_code-proposal eg. sup-proposal')
	intro_text = models.TextField(max_length=1000, help_text='Accepts HTML. Para elements should be wrapped in paragraph tags or they will not have fonts.')
	completion_text = models.TextField(max_length=1000, help_text='Accepts HTML. Para elements should be wrapped in paragraph tags or they will not have fonts.')
	fields = models.ManyToManyField('FormElement', through='FormElementsRelationship')

	def __unicode__(self):
		return u'%s' % self.name

class FormResult(models.Model):
	form = models.ForeignKey(Form)
	data = models.TextField()
	date = models.DateField(auto_now_add=True)

	def __unicode__(self):
		return '%s' % (self.form.name)

class FormElement(models.Model):
	field_choices = (
		('text', 'Text Field'),
		('textarea', 'Text Area'),
		('check', 'Check Box'),
		('select', 'Select'),
		('email', 'Email'),
		('upload', 'Upload'),
		('date', 'Date'),
	)

	name = models.CharField(max_length=100)
	choices = models.CharField(max_length=500, null=True, blank=True, help_text='Seperate choices with the bar | character.')
	field_type = models.CharField(max_length=100, choices=field_choices)
	required = models.BooleanField()

	def __unicode__(self):
		return '%s' % (self.name)

	def __repr__(self):
		return '<FormElement %s>' % (self.name)

class FormElementsRelationship(models.Model):
	form = models.ForeignKey(Form)
	element = models.ForeignKey(FormElement)
	order = models.IntegerField()
	element_class = models.CharField(max_length=20, null=True, blank=True)
	help_text = models.TextField(max_length=1000, null=True, blank=True)

	def __unicode__(self):
		return '%s: %s' % (self.form.name, self.element.name)

	def __repr__(self):
		return '<FormElementsRelation %s: %s' % (self.form.name, self.element.name)

	class Meta:
		ordering = ('order',)
