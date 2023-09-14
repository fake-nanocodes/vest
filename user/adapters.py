from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        # Override this method to prevent sending the email
        msg = self.render_mail(template_prefix, email, context)
        print(msg)
