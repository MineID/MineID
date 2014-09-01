class UserObjectsMixin(object):
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
