
class Roles(object):
    def process_request(self, request):
        request.user_roles = [role.slug for role in request.user.profile.roles.all()]