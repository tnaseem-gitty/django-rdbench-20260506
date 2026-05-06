from django.test import TestCase, override_settings
from django.contrib.messages import constants
from django.contrib.messages.storage.base import Message

class MessageLevelTagTest(TestCase):
    def test_level_tag_updates_with_override_settings(self):
        # Default tag for INFO level
        message = Message(constants.INFO, 'Test message')
        self.assertEqual(message.level_tag, 'info')

        # Override the MESSAGE_TAGS setting
        new_tags = {constants.INFO: 'custom_info'}
        with override_settings(MESSAGE_TAGS=new_tags):
            # Check if the level_tag property reflects the new setting
            self.assertEqual(message.level_tag, 'custom_info')

        # Check if it reverts back to the default after the context manager
        self.assertEqual(message.level_tag, 'info')

    def test_multiple_messages_with_override_settings(self):
        # Create messages with different levels
        info_message = Message(constants.INFO, 'Info message')
        warning_message = Message(constants.WARNING, 'Warning message')

        # Default tags
        self.assertEqual(info_message.level_tag, 'info')
        self.assertEqual(warning_message.level_tag, 'warning')

        # Override the MESSAGE_TAGS setting
        new_tags = {
            constants.INFO: 'custom_info',
            constants.WARNING: 'custom_warning',
        }
        with override_settings(MESSAGE_TAGS=new_tags):
            # Check if both messages reflect the new settings
            self.assertEqual(info_message.level_tag, 'custom_info')
            self.assertEqual(warning_message.level_tag, 'custom_warning')

        # Check if they revert back to the defaults
        self.assertEqual(info_message.level_tag, 'info')
        self.assertEqual(warning_message.level_tag, 'warning')

print("Test file created successfully.")
