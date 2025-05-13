# Импорт необходимых модулей
import sys  # Для вывода ошибок в стандартный поток ошибок
from bs4 import BeautifulSoup  # Основной инструмент для парсинга HTML
import requests  # Для выполнения HTTP-запросов
from docx import Document
from docx.shared import Inches


class Parser():
    """Класс для парсинга содержимого веб-страниц."""

    def __init__(self, url=None):
        """Инициализация парсера.

        Args:
            url (str, optional): URL страницы для парсинга. Если не указан,
                               будет запрошен при вызове метода run().
        """
        self.url = url  # Сохраняем URL как атрибут класса

    def run(self):
        """Основной метод выполнения парсинга страницы.

        Returns:
            str: Извлеченный текст страницы или None в случае ошибки.
        """
        # Получаем URL - либо из атрибута объекта, либо через ввод пользователя
        url = self.url if self.url else input("Введите URL: ")

        try:
            # Выполняем GET-запрос с таймаутом 10 секунд
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Проверяем успешность запроса

            # Создаем объект BeautifulSoup для парсинга HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Ищем основные содержательные теги (article или main)
            main_tags = soup.find_all(['p', 'article', 'main'])

            if main_tags:
                # Если нашли основные теги, очищаем их от ненужных элементов
                text_parts = []  # Список для хранения текстовых фрагментов
                for tag in main_tags:
                    # Удаляем скрипты, стили и другие ненужные элементы
                    for element in tag.find_all(['script', 'style', 'nav', 'footer',
                                                 'header', 'aside', 'button', 'a']):
                        element.decompose()  # Полностью удаляем элемент из DOM
                    # Извлекаем текст с сохранением переносов строк
                    text_parts.append(tag.get_text(separator='\n', strip=True))
                # Объединяем все фрагменты текста
                text = '\n\n'.join(text_parts)
            else:
                # Если основных тегов нет, очищаем всю страницу
                for element in soup.find_all(['script', 'style', 'meta', 'link',
                                              'nav', 'footer', 'header', 'aside',
                                              'button', 'a']):
                    element.decompose()
                # Извлекаем текст со всей страницы
                text = soup.get_text(separator='\n', strip=True)

            # Выводим результат через специальный метод
            self.word_file(text)
            return text  # Возвращаем текст для возможного дальнейшего использования

        except Exception as e:
            # Выводим ошибку в stderr и возвращаем None
            print(f"Ошибка: {str(e)}", file=sys.stderr)
            return None

    def word_file(self, text):
        """Создает docx файл с текстом из сайта.

        Args:
            text (str): Текст для добавления в файл
        """
        # Определяем базовое имя файла
        base_name = "result"
        extension = ".docx"
        counter = 1

        # Ищем первое свободное имя файла
        while True:
            file_name = f"{base_name}_{counter}{extension}"
            if not os.path.exists(file_name):
                break
            counter += 1

        # Создаем и сохраняем документ
        document = Document()
        document.add_paragraph(text)
        document.save(file_name)
        print(f"Документ сохранен как {file_name}")
        return file_name

parser = Parser()
parser.run()




