import urlparse


class FacebookNotificationsException(Exception):
    pass


class NotificationException(FacebookNotificationsException):
    pass


class Notification(object):
    def __init__(self, recipient, target, template):
        self.recipient = recipient
        self.target = target
        self.template = template

        self._clean_template()
        self._validate_if_recipient_is_not_empty()
        self._validate_if_target_is_absolute_url()
        self._validate_template()

    def _clean_template(self):
        self.template = self.template.strip()

    def _validate_if_recipient_is_not_empty(self):
        if not self.recipient:
            raise NotificationException("Recipient could not be empty.")

    def _validate_if_target_is_absolute_url(self):
        parsed_target = urlparse.urlparse(self.target)
        if parsed_target.scheme not in ['http', 'https']:
            raise NotificationException(
                "target is not valid url with domain and scheme."
            )

    def _validate_template(self):
        self._validate_if_template_is_not_empty()
        self._validate_if_template_is_not_to_long()

    def _validate_if_template_is_not_empty(self):
        if not self.template:
            raise NotificationException("template should not be empty.")

    def _validate_if_template_is_not_to_long(self):
        # MAX_LENGHT is defined in Facebook docs:
        # https://developers.facebook.com/docs/app_notifications/
        MAX_LENGTH = 180
        if len(self.template) > MAX_LENGTH:
            raise NotificationException(
                "template is longer than %d characters" % MAX_LENGTH
            )
