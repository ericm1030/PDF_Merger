import sys
import io
import PySimpleGUI as sg
from pdfrw import PdfReader, PdfWriter, IndirectPdfDict
import re
from io import StringIO

# Simple and quick PDF Merger that can merge two pdf files.

custom_theme = {'BACKGROUND': '#f3f3f3',
                'TEXT': 'black',
                'INPUT': '#d9d9d9',
                'TEXT_INPUT': 'black',
                'SCROLL': '#9d9e9d',
                'BUTTON': ('white', '#0078d4'),
                'PROGRESS': ('#cce8ff', '#62a3d2'),
                'BORDER': 1,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}

# {'BACKGROUND': '#e8edeb',
#                 'TEXT': 'black',
#                 'INPUT': '#dedede',
#                 'TEXT_INPUT': 'black',
#                 'SCROLL': '#9d9e9d',
#                 'BUTTON': ('white', '#e00404'),
#                 'PROGRESS': ('#990000', '#CC8019'),
#                 'BORDER': 1,
#                 'SLIDER_DEPTH': 0,
#                 'PROGRESS_DEPTH': 0}
sg.theme_add_new('custom_theme', custom_theme)
sg.theme('custom_theme')

font = 'Segoe UI Variable Display'
font_size = 12
header_font_size = 16

def get_user_input():
    # GUI Layout
    layout = \
        [
            [sg.Text("Simple PDF Merger", font=('Segoe UI Historic', header_font_size), auto_size_text=True)],
            [sg.HorizontalSeparator()],
            [sg.Text("PDF 1: ", ), sg.Text(""), sg.FileBrowse(button_text="Browse", font=(font, font_size), size=(6, 1),
                                                              file_types=(("PDF Files", "*.pdf"),), key='-PDF1-', )],
            [sg.Text("PDF 2: "), sg.Text(""), sg.FileBrowse(button_text="Browse", font=(font, font_size), size=(6, 1),
                                                            file_types=(("PDF Files", "*.pdf"),), key='-PDF2-')],
            [sg.Text("Output File Name: "), sg.In(key='-FILENAME-'), sg.T(".pdf")],
            [sg.Text("Save Location: "),
             sg.FolderBrowse(button_text="Browse", font=(font, font_size), auto_size_button=True, key='-SAVE_LOC-')],
            [sg.Push(), sg.Exit(font=(font, font_size), ),
             sg.Button('Enter', font=(font, font_size), key='-ENTER-', bind_return_key=True), sg.Push()]
        ]

    window = sg.Window("PDF Merger", layout, element_justification='l', keep_on_top=True, font=(font, font_size),
                       icon='pdf.ico', finalize=True)

    user_input = {}

    # Event Loop
    while True:
        event, values = window.read()

        if event in ('Exit', sg.WIN_CLOSED):
            exit()

        if event == '-ENTER-':
            # If there is no input ignore that enter was pressed
            if values['-PDF1-'] == '' or values['-PDF2-'] == '':
                continue

            else:

                filename = values['-FILENAME-']
                filename = re.sub('[^a-zA-Z0-9\n\.]', '', filename)
                filename = values['-SAVE_LOC-'] + '/' + filename + ".pdf"
                print(f"{filename = }")

                user_input['filename'] = filename

                user_input['pdf1'] = values['-PDF1-']
                # sg.user_settings_set_entry('-pdf1-', values['-PDF1-'])

                user_input['pdf2'] = values['-PDF2-']
                # sg.user_settings_set_entry('-pdf2-', values['-PDF2-'])

            break

    return user_input


def merge_pdfs(pdfs, output_file_name):
    writer = PdfWriter()

    for input_file in pdfs:
        writer.addpages(PdfReader(input_file).pages)

    writer.trailer.Info = IndirectPdfDict(
        Title=output_file_name,
        Author='none',
        Subject='none',
        Creator='none',
    )
    writer.write(output_file_name)

    return None


def main():
    try:
        settings = get_user_input()

        filename = settings['filename']

        pdf_files = [settings['pdf1'], settings['pdf2']]
        print(f"{pdf_files = }")
        merge_pdfs(pdf_files, filename)

    except Exception as e:
        print(f"Exception: {e}")

    return None


if __name__ == "__main__":
    main()
