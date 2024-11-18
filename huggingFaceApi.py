import aiohttp

class ChatBot:
    def __init__(self, api_key, model="Qwen/Qwen2.5-Coder-32B-Instruct", temperature=0.5, max_tokens=512, top_p=0.7):
        """
        Инициализация ChatBot с Hugging Face API.

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
        self.messages = []  # История общения

    async def ask(self, user_message):
        """
        Отправляет запрос к модели и возвращает только последний ответ, без истории чата.

        :param user_message: Сообщение пользователя.
        :return: Ответ модели (только последний текст).
        """
        # Формируем данные для отправки
        payload = {
            "inputs": user_message,  # Передаем только текущее сообщение
            "parameters": {
                "temperature": self.temperature,
                "max_new_tokens": self.max_tokens,
                "top_p": self.top_p,
            },
        }

        # Асинхронно отправляем запрос к API
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, headers=self.headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()

                    # Проверяем структуру данных и извлекаем только ответ
                    if isinstance(data, list) and "generated_text" in data[0]:
                        return data[0]["generated_text"]
                    elif isinstance(data, dict) and "generated_text" in data:
                        return data["generated_text"]
                    else:
                        raise ValueError(f"Unexpected response format: {data}")
                else:
                    error_message = await response.text()
                    raise Exception(f"Error from API: {response.status}, {error_message}")

        # Асинхронно отправляем запрос к API
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, headers=self.headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()

                    # Проверяем структуру данных
                    if isinstance(data, list) and "generated_text" in data[0]:
                        assistant_response = data[0]["generated_text"]
                    elif isinstance(data, dict) and "generated_text" in data:
                        assistant_response = data["generated_text"]
                    else:
                        raise ValueError(f"Unexpected response format: {data}")

                    self.messages.append(f"Assistant: {assistant_response}")
                    return self.messages
                else:
                    error_message = await response.text()
                raise Exception(f"Error from API: {response.status}, {error_message}")

    def clear_history(self):
        """
        Очищает историю сообщений.
        """
        self.messages = []