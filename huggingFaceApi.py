import aiohttp

class ChatBot:
    def __init__(self, api_key, model="Qwen/Qwen2.5-Coder-32B-Instruct", temperature=0.5, max_tokens=512, top_p=0.7):
        """
        Initializes ChatBot with Hugging Face API.

        :param api_key: Hugging Face API access token.
        :param model: Model name.
        :param temperature: Temperature parameter for randomness control.
        :param max_tokens: Maximum number of tokens in the response.
        :param top_p: Probability sampling threshold.
        """
        """
        Инициализирует ChatBot с Hugging Face API.

        :param api_key: Токен доступа к API Hugging Face.
        :param model: Название модели.
        :param temperature: Параметр температуры для контроля случайности.
        :param max_tokens: Максимальное количество токенов в ответе.
        :param top_p: Порог вероятностного семплирования.
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.api_url = f"https://api-inference.huggingface.co/models/{model}"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.messages = []

    async def ask(self, user_message):
        """
        Sends a request to the model and returns only the last response, without chat history.

        :param user_message: User message.
        :return: Model response (only the last text).
        """
        """
        Отправляет запрос к модели и возвращает только последний ответ, без истории чата.

        :param user_message: Сообщение пользователя.
        :return: Ответ модели (только последний текст).
        """
        payload = {
            "inputs": user_message,
            "parameters": {
                "temperature": self.temperature,
                "max_new_tokens": self.max_tokens,
                "top_p": self.top_p,
            },
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, headers=self.headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()

                    if isinstance(data, list) and "generated_text" in data[0]:
                        return data[0]["generated_text"]
                    elif isinstance(data, dict) and "generated_text" in data:
                        return data["generated_text"]
                    else:
                        raise ValueError(f"Unexpected response format: {data}")
                else:
                    error_message = await response.text()
                    raise Exception(f"Error from API: {response.status}, {error_message}")

    def clear_history(self):
        """
        Clears the message history.
        """
        """
        Очищает историю сообщений.
        """
        self.messages = []
