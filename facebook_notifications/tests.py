from django.test import TestCase
import facepy
import ludibrio

from facebook_notifications import notifications


class TestNotification(TestCase):
    def test_creating_valid_notification(self):
        notification = self._create_notification(recipient="123",
                                                 target="foo/bar/",
                                                 template="Test notification")
        self.assertEqual(notification.recipient, "123")
        self.assertEqual(notification.target, "foo/bar/")
        self.assertEqual(notification.template, "Test notification")

    def test_if_template_is_stripped(self):
        notification = self._create_notification(
            template="    Test notification.    ",
        )
        self.assertEqual(notification.template, "Test notification.")

    def test_if_empty_recipient_is_invalid(self):
        self.assertInvalidNotification(recipient="")

    def test_if_url_target_is_invalid(self):
        self.assertInvalidNotification(target="http://www.google.pl")

    def test_if_absolute_path_target_is_invalid(self):
        self.assertInvalidNotification(target="/relative/target/")

    def test_if_empty_template_is_invalid(self):
        self.assertInvalidNotification(template="")

    def test_if_very_long_template_is_invalid(self):
        self.assertInvalidNotification(template=500 * "a")

    def _create_notification(self, recipient="123",
                             target="foo/bar/",
                             template="Test notification."):
        return notifications.Notification(recipient, target, template)

    def assertInvalidNotification(self, **kwargs):
        self.assertRaises(notifications.NotificationError,
                          self._create_notification,
                          **kwargs)


class TestNotificationSender(TestCase):
    def test_sending_notification(self):
        with ludibrio.Mock() as graph:
            graph.post('123/notifications',
                       href='foo/bar/',
                       template='test test test')
        sender = notifications.NotificationSender(graph)
        notification = notifications.Notification('123',
                                                  'foo/bar/',
                                                  'test test test')
        sender.send(notification)
        graph.validate()

    def test_throwing_exceptions(self):
        graph = self._get_graph_stub_raising_facepy_error()
        sender = notifications.NotificationSender(graph)
        self.assertRaises(notifications.SenderError,
                          sender.send,
                          ludibrio.Dummy())

    def _get_graph_stub_raising_facepy_error(self):
        def raise_exception(*args, **kwargs):
            raise facepy.FacepyError("test")
        with ludibrio.Stub() as graph:
            graph.post >> raise_exception
        return graph
