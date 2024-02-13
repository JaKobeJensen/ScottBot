import unittest

from managers import ChatGPTManager


class TestChatGPTManager(unittest.TestCase):

    def __init__(self):
        self.chatgpt_manager = ChatGPTManager(
            model="gpt-3.5-turbo",
            first_system_prompt="Make sure to give only a one sentence response. Try to be as concise as possible.",
        )

    def test_start_new_conversation(self):
        self.chatgpt_manager.current_chat_history.append(
            {"role": "user", "content": "Hello"}
        )
        self.chatgpt_manager.current_chat_history.append(
            {"role": "assistant", "content": "Hello there!"},
        )
        self.chatgpt_manager.start_new_conversation()
        self.assertEqual(len(self.chatgpt_manager.current_chat_history), 1)

    def test_no_prompt_chat(self):
        self.assertIsNone(self.chatgpt_manager.chat(prompt=""))

    def test_no_prompt_chat_with_history(self):
        self.assertIsNone(self.chatgpt_manager.chat_with_history(prompt=""))

    def test_chat(self):
        prompt = "Explain what a cow is."

        print("[yellow]\nAsking ChatGPT the question...")
        response = self.chatgpt_manager.chat(prompt)
        print(f"[green]{response}\n")
        self.assertEqual(type(response), str)

    def test_chat_history(self):
        first_prompt = "Explain what a cow is."
        second_prompt = "Are they mammals?"
        third_prompt = "Can we eat them?"

        print("[yellow]\nAsking ChatGPT the first question...")
        first_response = self.chatgpt_manager.chat(first_prompt)
        print(f"[green]{first_response}\n")
        self.assertEqual(type(first_response), str)

        print("[yellow]\nAsking ChatGPT the second question...")
        second_response = self.chatgpt_manager.chat(second_prompt)
        print(f"[green]{second_response}\n")
        self.assertEqual(type(second_response), str)

        print("[yellow]\nAsking ChatGPT the third question...")
        third_response = self.chatgpt_manager.chat(third_prompt)
        print(f"[green]{third_response}\n")
        self.assertEqual(type(third_response), str)

        chat_history = [
            self.chatgpt_manager.FIRST_SYSTEM_MESSAGE,
            {"role": "user", "content": first_prompt},
            {"role": "assistant", "content": first_response},
            {"role": "user", "content": second_prompt},
            {"role": "assistant", "content": second_response},
            {"role": "user", "content": third_prompt},
            {"role": "assistant", "content": third_response},
        ]
        self.assertListEqual(self.chatgpt_manager.current_chat_history, chat_history)


if __name__ == "__main__":
    unittest.main
