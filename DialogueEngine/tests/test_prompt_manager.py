import unittest
import sys
import os

# Temporarily add the parent directory to sys.path to allow importing prompt_manager
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ChatGPT.prompt_manager import PromptManager

class TestPromptManager(unittest.TestCase):
    def setUp(self):
        # Initialize a fresh PromptManager for each test
        self.manager = PromptManager()

    def test_initial_default_prompts(self):
        prompts = self.manager.get_all_prompts()
        self.assertIn("default", prompts)
        self.assertIn("math101", prompts)
        self.assertIn("history202", prompts)
        self.assertEqual(prompts["default"]["system_message"], "You are a helpful assistant.")

    def test_add_and_get_prompt(self):
        self.manager.add_prompt("new_course", "New system msg", "New user template: {user_query}")
        prompt = self.manager.get_prompt("new_course")
        self.assertIsNotNone(prompt)
        self.assertEqual(prompt["system_message"], "New system msg")
        self.assertEqual(prompt["user_message_template"], "New user template: {user_query}")

    def test_update_prompt(self):
        self.manager.add_prompt("math101", "Updated system msg", "Updated user template: {user_query}")
        prompt = self.manager.get_prompt("math101")
        self.assertIsNotNone(prompt)
        self.assertEqual(prompt["system_message"], "Updated system msg")

    def test_get_non_existent_prompt(self):
        prompt = self.manager.get_prompt("non_existent_course")
        self.assertIsNone(prompt)

    def test_get_all_prompts(self):
        all_prompts = self.manager.get_all_prompts()
        # Should contain default prompts + any added during tests (if not fresh instance)
        # Since setUp creates a fresh instance, it should only have default prompts initially
        self.assertEqual(len(all_prompts), 3) # default, math101, history202
        self.assertIn("default", all_prompts)
        self.assertIn("math101", all_prompts)
        self.assertIn("history202", all_prompts)

if __name__ == '__main__':
    unittest.main()
