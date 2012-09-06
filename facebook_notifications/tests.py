from django.test import TestCase

from facebook_notifications import notifications


class TestNotification(TestCase):
    def test_creating_valid_notification(self):
        notification = self._create_notification(recipient="123",
                                                 target="http://example.com/",
                                                 template="Test notification")
        self.assertEqual(notification.recipient, "123")
        self.assertEqual(notification.target, "http://example.com/")
        self.assertEqual(notification.template, "Test notification")

    def test_if_template_is_stripped(self):
        notification = self._create_notification(
            template="    Test notification.    ",
        )
        self.assertEqual(notification.template, "Test notification.")

    def test_if_empty_recipient_is_invalid(self):
        self.assertInvalidNotification(recipient="")

    def test_if_non_url_target_is_invalid(self):
        self.assertInvalidNotification(target="invalid target")

    def test_if_relative_url_target_is_invalid(self):
        self.assertInvalidNotification(target="/relative/target/")

    def test_if_empty_template_is_invalid(self):
        self.assertInvalidNotification(template="")

    def test_if_very_long_template_is_invalid(self):
        self.assertInvalidNotification(template=500 * "a")

    def _create_notification(self, recipient="123",
                             target="http://example.com/",
                             template="Test notification."):
        return notifications.Notification(recipient, target, template)

    def assertInvalidNotification(self, **kwargs):
        self.assertRaises(notifications.NotificationException,
                          self._create_notification,
                          **kwargs)
