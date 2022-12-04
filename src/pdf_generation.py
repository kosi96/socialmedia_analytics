from fpdf import FPDF

USE_CASES = {
    'overall_freq': (5, 30, 200, 90),

    'favored_emojis_me': (5, 130, 55, 60),
    'favored_emojis_friend': (55, 130, 55, 60),

    'response_time_me': (110, 130, 55, 60),
    'response_time_friend': (150, 130, 55, 60),

    'daily_freq': (5, 200, 200, 90),
}


def generate_pdf(name, dir, my_custom_name, friend_custom_name):
    pdf = FPDF()
    pdf.set_font('Arial', 'B', 16)
    pdf.add_page()
    pdf.image('data/visualization/BACKGROUND/bg_23272C.png', 0, 0, 210, 297)  # add background
    pdf.set_text_color(255, 255, 255)
    pdf.set_draw_color(255, 255, 255)
    pdf.cell(190, 10, f'{my_custom_name} vs {friend_custom_name}', 1, 0, 'C')

    for image_name, shape in USE_CASES.items():
        image_path = dir + image_name + '.png'
        x, y, w, h = shape
        pdf.image(image_path, x, y, w, h)
    pdf.output(name, "F")

