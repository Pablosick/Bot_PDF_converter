from enum import Enum


class MenuButton(Enum):
    CONVERT_PDF = "КОНВЕРТИРОВАТЬ В PDF"
    INSTRUCTION = "📖ИНСТРУКЦИЯ"
    BACK = "◀Назад"
    INSTRUCTION_ON_WORK = "📖ИНСТРУКЦИЯ ПО РАБОТЕ"
    FORMAT = "🗝ФОРМАТ"
    GO_TO_CONVERT = "⚙️ПЕРЕЙТИ К КОНВЕРТАЦИИ "
    BUT_MENU = "🔆МЕНЮ"


class Information(Enum):
    CONVERT = "Чтобы конвертировать файлы в PDF, пришли мне архив🗄"
    INSTRUCTION = """Чтобы конвертировать файлы в PDF, нужно архивировать все файлы 🗄
‼️Я работаю только с файлами, которые имеют расширение zip.
📤Рекомендую скачать файловый архиватор 7zip (если его нет): https://www.7-zip.org/download.html
                    
                    
☑️Если вы хотите получить файла по установке и примером работы, нажмите кнопку - ИНСТРУКЦИЯ ПО РАБОТЕ
☑️Если вы хотите узнать формат, который я могу с конвертировать в PDF,
нажмите кнопку - ФОРМАТ"""
    GET_INSTRUCTION = "⚡️Ниже будет выслано руководство с установкой и отправкой zip файла, нажмите кнопку - <u>'назад'</u>:"
    FORMAT = """📌Файлы, которые я могу конвертировать должны иметь формат .docx/.DOCX или .doc/.DOC
🧹Файлы, которые имеют расширение иное от представленного выше⬆️ не будут конвертированы.
🔍В результирующем сообщение вы увидите на экране, что это за файлы"""
    RES_CONVERT_FILE = "📁Вот Ваши конвертированные файлы:"
    BUTTON_BACK = '🌪Если Вам требуется конвертация еще одного архива, нажмите кнопку <u>"Назад"</u>'
    DIF_MES = "Я не знаю, как отвечать на это сообщение"
