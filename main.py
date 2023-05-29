import telebot
from telebot import types

from app.algorithm import Algorithm

from src.bot_enum.menu_information import MenuButton, Information
from src.private.token import TOKEN


class ConverterPDF:
    app = Algorithm()

    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

    def run(self):
        @self.bot.message_handler(commands=["start"])
        def start(message):
            """Стартовый интерфейс"""

            dimensions = types.InlineKeyboardMarkup(row_width=1)
            menu_button = types.InlineKeyboardButton(
                MenuButton.CONVERT_PDF.value, callback_data="button"
            )
            menu_button2 = types.InlineKeyboardButton(
                MenuButton.INSTRUCTION.value, callback_data="button2"
            )
            dimensions.add(menu_button, menu_button2)
            self.bot.send_message(
                message.chat.id,
                f"<b>Привет, {message.chat.first_name}✋ </b>\nЯ могу преобразовать все твои файлы в "
                f"PDF🗂 "
                f"\nНажми на кнопку "
                f'"КОНВЕРТИРОВАТЬ В PDF"⬇️🔥\n'
                f'Чтобы узнать подробнее нажми на кнопку <u>"ИНСТРУКЦИЯ"🕹 </u>',
                reply_markup=dimensions,
                parse_mode="HTML",
            )

        @self.bot.message_handler(content_types=["text"])
        def text(message):
            """Обработка любых сообщений"""

            dimensions = types.InlineKeyboardMarkup(row_width=1)
            but_menu = types.InlineKeyboardButton(
                MenuButton.BUT_MENU.value, callback_data="button2"
            )
            dimensions.add(but_menu)
            self.bot.send_message(message.chat.id, Information.DIF_MES.value, reply_markup=dimensions)

        @self.bot.callback_query_handler(func=lambda callback: callback.data)
        def check_callback(callback):
            """Работа при нажатии на кнопки"""

            if callback.data == "button":
                self.bot.send_message(
                    callback.message.chat.id, Information.CONVERT.value
                )
            elif callback.data == "button2":
                dimensions = types.InlineKeyboardMarkup(row_width=1)
                get_instruction = types.InlineKeyboardButton(
                    MenuButton.INSTRUCTION_ON_WORK.value, callback_data="button3"
                )
                get_formats = types.InlineKeyboardButton(
                    MenuButton.FORMAT.value, callback_data="button4"
                )
                but_back = types.InlineKeyboardButton(
                    MenuButton.GO_TO_CONVERT.value, callback_data="button"
                )
                dimensions.add(get_instruction, get_formats, but_back)
                self.bot.send_message(
                    callback.message.chat.id,
                    Information.INSTRUCTION.value,
                    parse_mode="HTML",
                    reply_markup=dimensions,
                )
            elif callback.data == "button3":
                in_keyboard = types.InlineKeyboardMarkup(row_width=1)
                button_back = types.InlineKeyboardButton(
                    MenuButton.BACK.value, callback_data="button2"
                )
                in_keyboard.add(button_back)
                self.bot.send_message(
                    callback.message.chat.id,
                    Information.GET_INSTRUCTION.value,
                    parse_mode="HTML",
                    reply_markup=in_keyboard,
                )
                self.bot.send_document(
                    callback.message.chat.id,
                    open(
                        f"{self.app.current_dir}\\instruction\\instruction.docx", "rb"
                    ),
                )

            elif callback.data == "button4":
                in_keyboard_back = types.InlineKeyboardMarkup(row_width=1)
                button_back = types.InlineKeyboardButton(
                    MenuButton.BACK.value, callback_data="button2"
                )
                in_keyboard_back.add(button_back)
                self.bot.send_message(
                    callback.message.chat.id,
                    Information.FORMAT.value,
                    reply_markup=in_keyboard_back,
                )

        @self.bot.message_handler(content_types=["document"])
        def get_archive(message):
            """Обработка архива"""

            next_keyboard = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton(
                MenuButton.BACK.value, callback_data="button"
            )
            next_keyboard.add(button_back)
            file_info = self.bot.get_file(message.document.file_id)
            download_file = self.bot.download_file(file_info.file_path)
            path_archive = (
                f"{self.app.current_dir}\\archive\\" + message.document.file_name
            )
            with open(path_archive, "wb") as new_file:
                new_file.write(download_file)
            self.app.transformation_file(path_archive)
            self.bot.send_message(
                message.chat.id,
                f"🛠Подождите, пожалуйста, идет процесс конвертации файлов архива: "
                f" '{message.document.file_name}'...",
            )
            self.app.run_processing(message.document.file_name)
            self.bot.send_message(message.chat.id, Information.RES_CONVERT_FILE.value)
            self.app.zip_file_with_pdf()
            self.bot.send_document(
                message.chat.id, open(f"{self.app.current_dir}\\pdf.zip", "rb")
            )
            no_convert_files = ", ".join(self.app.get_no_convert())
            self.bot.send_message(message.chat.id, f"❌Файлы, которые не удалось конвертировать: {no_convert_files}")
            self.app.deleting_files(message.document.file_name)
            self.bot.send_message(
                message.chat.id,
                Information.BUTTON_BACK.value,
                reply_markup=next_keyboard, parse_mode="HTML"
            )

        self.bot.polling(none_stop=True)


bot = ConverterPDF(TOKEN)
bot.run()
