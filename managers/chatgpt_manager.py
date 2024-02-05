import os

import tiktoken
from openai import OpenAI
from rich import print


def num_tokens_from_messages(
    messages: list[dict[str, str]], model: str = "gpt-4"
) -> int:
    """Returns the number of tokens used by a list of messages.
    Copied with minor changes from: https://platform.openai.com/docs/guides/chat/managing-tokens
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
        num_tokens = 0
        for message in messages:
            num_tokens += (
                4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            )
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    except Exception:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not presently implemented for model {model}.
        # See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )


class ChatGPTManager:
    TOKEN_LIMIT = 8000

    def __init__(
        self, model: str = "gpt-3.5-turbo", first_system_prompt: str | None = None
    ):
        self.current_chat_history = []  # Stores the current conversation
        self.model = model
        try:
            self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        except TypeError:
            exit("Ooops! You forgot to set OPENAI_API_KEY in your environment!")
        if first_system_prompt is not None:
            self.FIRST_SYSTEM_MESSAGE = {
                "role": "system",
                "content": first_system_prompt,
            }
            self.current_chat_history.append(self.FIRST_SYSTEM_MESSAGE)

    # Asks a question with no chat history
    def chat(self, prompt: str | None = None) -> str | None:
        if prompt is not None:
            print("Didn't receive input!")
            return None

        # Check that the prompt is under the token context limit
        chat_question = [{"role": "user", "content": prompt}]
        if num_tokens_from_messages(chat_question, self.model) > self.TOKEN_LIMIT:
            print("The length of this chat question is too large for the GPT model")
            return None

        print("[yellow]\nAsking ChatGPT a question...")
        completion = self.client.chat.completions.create(
            model=self.model, messages=chat_question
        )

        # Process the answer
        chatgpt_answer = completion.choices[0].message.content
        print(f"[green]\n{chatgpt_answer}\n")
        return chatgpt_answer

    # Asks a question that includes the full conversation history
    def chat_with_history(self, prompt: str | None = None) -> str | None:
        if not prompt:
            print("Didn't receive input!")
            return None

        # Add our prompt into the chat history
        self.current_chat_history.append({"role": "user", "content": prompt})

        # Check total token limit. Remove old messages as needed
        print(
            f"[red]\nChat History has a current token length of {num_tokens_from_messages(self.current_chat_history, self.model)}"
        )
        while (
            num_tokens_from_messages(self.current_chat_history, self.model)
            > self.TOKEN_LIMIT
        ):
            self.current_chat_history.pop(
                1
            )  # We skip the 1st message since it's the system message
            print(
                f"[red]Popped a message! New token length is: {num_tokens_from_messages(self.current_chat_history, self.model)}"
            )

        print("[yellow]\nAsking ChatGPT a question...")
        completion = self.client.chat.completions.create(
            model=self.model, messages=self.current_chat_history
        )

        # Add this answer to our chat history
        self.current_chat_history.append(
            {
                "role": completion.choices[0].message.role,
                "content": completion.choices[0].message.content,
            }
        )

        # Process the answer
        chatgpt_answer = completion.choices[0].message.content
        print(f"[green]\n{chatgpt_answer}\n")
        return chatgpt_answer

    def start_new_conversation(self) -> None:
        self.current_chat_history = []
        self.current_chat_history.append(self.FIRST_SYSTEM_MESSAGE)
        return None


if __name__ == "__main__":
    first_system_promt = "For now on you are a college computer science professor, named ScottBot, and loves to answer students questions. Make sure you follow these rules at all times: 1. make responds only one paragraph long, 2. never generate code, use words instead"
    chatgpt_manager = ChatGPTManager(
        model="gpt-3.5-turbo", first_system_prompt=first_system_promt
    )
    chatgpt_answer = chatgpt_manager.chat_with_history(
        "Hey ScottBot, can you tell me what the cpu is?"
    )
    quit()
