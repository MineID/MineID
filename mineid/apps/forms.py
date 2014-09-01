from provider.oauth2.forms import ClientForm


class ClientForm(ClientForm):
    def full_clean(self):
        # Make it mutable
        self.data = self.data.copy()

        # Adds missing http(s)://
        self._prefix_with_http('url')
        self._prefix_with_http('redirect_uri')

        return super(ClientForm, self).full_clean()

    def _prefix_with_http(self, field):
        url = self.data.get(field, '')
        if not url.startswith('http://') and not url.startswith('https://'):
            self.data[field] = 'http://' + url
