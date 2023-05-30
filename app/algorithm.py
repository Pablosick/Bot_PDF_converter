import zipfile
import os
import pythoncom
import docx2pdf
import shutil

from pathlib import Path

from win32com import client as wc


class Algorithm:
    """Внутренний процесс работы с файлами"""

    current_dir = str(Path.cwd())

    def transformation_file(self, path):
        """Разархивирование получаемого архива"""

        build_zip = zipfile.ZipFile(path)
        build_zip.extractall(f"{self.current_dir}\\all_files")
        build_zip.close()

    def zip_file_with_pdf(self):
        """Архивирование файла с pdf в архив"""

        with zipfile.ZipFile("pdf.zip", "w") as res_zip:
            for file in os.listdir(f"{self.current_dir}\\pdf_file"):
                res_zip.write(f"pdf_file\\{file}")

    def run_processing(self, zip_file):
        """Конвертирование файлов в pdf"""

        different_files = str(zip_file[:-4])
        self.mkdir_for_file()
        for file in os.listdir(f"{self.current_dir}\\all_files\\new_archive"):
            if file.lower().endswith(".docx") and not file.startswith("~"):
                pythoncom.CoInitialize()
                try:
                    docx2pdf.convert(f"all_files\\new_archive\\{file}", "pdf_file\\")
                finally:
                    pythoncom.CoUninitialize()
            elif file.lower().endswith(".doc"):
                self.mv_files(file, "Documents with 'doc' extension")
            else:
                self.mv_files(file, "Other")
        self.doc_in_docx()
        self.convert_doc_files()

    def mkdir_for_file(self):
        """Метод создаем папки для файлов с расширение .doc и .docx"""

        os.mkdir(f"{self.current_dir}\\Documents with 'doc' extension")
        os.mkdir(f"{self.current_dir}\\Folder for docx")
        os.mkdir(f"{self.current_dir}\\Other")

    def mv_files(self, file, name_new_dir):
        """Метод перемещает файлы, которые имеют расширение отличное от .docx в отдельные папки"""

        os.replace(
            f"{self.current_dir}\\all_files\\new_archive\\{file}",
            f"{self.current_dir}\\{name_new_dir}\\{file}",
        )

    def doc_in_docx(self):
        """Метод преобразовывает в .docx расширение.
        Также метод добавляет все файлы с расширение .doc в одну папку, а с расширение .docx в другую папку
        """

        path_doc_file = f"{self.current_dir}\\Documents with 'doc' extension"
        for doc_file in os.listdir(path_doc_file):
            try:
                pythoncom.CoInitialize()
                if not doc_file.startswith("~"):
                    word = wc.Dispatch("Word.Application")
                    doc = word.Documents.Open(
                        os.path.abspath(f"{path_doc_file}\\{doc_file}")
                    )
                    doc.SaveAs(
                        f"{self.current_dir}\\Folder for docx\\{doc_file[:-3]}.docx", 16
                    )
                    doc.Close()
            except:
                continue
            finally:
                pythoncom.CoUninitialize()

    def convert_doc_files(self):
        """Метод конвертирует файлы преобразованные из .doc в .docx"""

        for docx in os.listdir(f"{self.current_dir}\\Folder for docx"):
            pythoncom.CoInitialize()
            try:
                docx2pdf.convert(f"Folder for docx\\{docx}", "pdf_file\\")
            except:
                continue
            finally:
                pythoncom.CoUninitialize()

    def get_no_convert(self):
        """Метод возвратит наименования файлов, которые не были конвертированы"""

        return os.listdir(f"{self.current_dir}\\Other")

    def rename_dir(self):
        for rename_files in os.listdir(f"{self.current_dir}\\all_files"):
            os.rename(
                f"{self.current_dir}\\all_files\\{rename_files}",
                f"{self.current_dir}\\all_files\\new_archive",
            )

    def deleting_files(self):
        """Удаление файлов, с которыми была произведена работа"""

        shutil.rmtree("all_files\\new_archive")
        shutil.rmtree(f"Folder for docx")
        shutil.rmtree("Documents with 'doc' extension")
        shutil.rmtree("Other")
        os.remove(f"{self.current_dir}\\pdf.zip")
        for pdf_file in os.listdir(f"{self.current_dir}\\pdf_file"):
            os.remove(f"{self.current_dir}\\pdf_file\\{pdf_file}")

        for archive in os.listdir(f"{self.current_dir}\\archive"):
            os.remove(f"{self.current_dir}\\archive\\{archive}")
