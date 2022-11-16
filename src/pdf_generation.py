from src.preprocess import load_config_file_and_fetch_usernames
from fpdf import FPDF



use_cases = {'favored_emojis_me': (10, 10, 30, 30),
             'favored_emojis_friend': (10, 200, 30, 30)
             }


def createPDF():
    pdf = FPDF()
    pdf.add_page()
    for image_name, shape in use_cases.items():
        image_path = dir + image_name + '.png'
        x, y, w, h = shape
        pdf.image(image_path, x, y, w, h)
    pdf.output("yourfile.pdf", "F")


if __name__ == '__main__':
    my_username, friend_username = load_config_file_and_fetch_usernames()
    dir = f'data/usecases/{my_username}_{friend_username}/'

    createPDF()
