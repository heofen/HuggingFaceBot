import tempfile

async def create_temp_html_file(text: str, title: str = "Shovel", css: str = None) -> str:
    """
    Создаёт временный HTML-файл с заданным текстом и CSS.

    :param text: Текст для вставки в HTML-документ.
    :param title: Заголовок страницы.
    :param css: Пользовательские CSS-стили.
    :return: Путь к временно созданному HTML-файлу.
    """
    # Базовые стили для светлой и тёмной тем
    default_css = """
    :root {
        --bg-color: #121212;
        --text-color: #e0e0e0;
        --header-color: #bb86fc;
        --button-bg: #333;
        --button-text: #e0e0e0;
    }

    body.light {
        --bg-color: #f9f9f9;
        --text-color: #333;
        --header-color: #555;
        --button-bg: #ddd;
        --button-text: #333;
    }

    body {
        background-color: var(--bg-color);
        color: var(--text-color);
        font-family: Arial, sans-serif;
        line-height: 1.6;
        padding: 20px;
        transition: background-color 0.3s, color 0.3s;
    }
    h1, h2, h3 {
        color: var(--header-color);
    }
    p {
        margin-bottom: 10px;
    }
    pre {
        background-color: #2e2e2e;
        padding: 10px;
        border-radius: 5px;
        overflow-x: auto;
        white-space: pre-wrap;
        color: var(--text-color);
    }
    body.light pre {
        background-color: #f0f0f0;
        color: #333;
    }
    .theme-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: var(--button-bg);
        color: var(--button-text);
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s, color 0.3s;
    }
    .theme-toggle:hover {
        opacity: 0.8;
    }
    """

    styles = css if css else default_css

    # Функция для форматирования текста
    def format_text(input_text: str) -> str:
        formatted_lines = []
        for line in input_text.splitlines():
            # Убираем лишние пробелы и добавляем табуляцию
            formatted_line = "&emsp;" + line.replace("    ", "&emsp;")
            formatted_lines.append(formatted_line)
        return "<br>".join(formatted_lines)
    
    # Форматируем входной текст
    formatted_text = format_text(text)
    
    # Генерация HTML-документа
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>{styles}</style>
    </head>
    <body class="dark">
        <button class="theme-toggle" onclick="toggleTheme()">Сменить тему</button>
        <pre>{formatted_text}</pre>

        <script>
        // Функция для переключения темы
        function toggleTheme() {{
            const body = document.body;
            const isDark = body.classList.toggle('light');
            if (isDark) {{
                localStorage.setItem('theme', 'light');
            }} else {{
                localStorage.setItem('theme', 'dark');
            }}
        }}

        // Устанавливаем тему при загрузке страницы
        (function() {{
            const savedTheme = localStorage.getItem('theme');
            if (savedTheme === 'light') {{
                document.body.classList.add('light');
            }}
        }})();
        </script>
    </body>
    </html>
    """
    
    # Создание временного файла
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8")
    temp_file.write(html)
    temp_file.close()
    
    return temp_file.name
