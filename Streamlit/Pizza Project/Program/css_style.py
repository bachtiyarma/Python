# Membuat Border Shape CSS
def rectangular_shape(
    font_size,
    text_color,
    border_radius,
    background_color,
    text
        
):
    shape_text = f'''
        <div style=
            "padding:20px;
            color:{text_color};
            margin:10;
            font-size:{font_size}%;
            text-align:center;
            display:fill;
            border-radius:{border_radius}px;
            background-color:{background_color};
            overflow:hidden;
            font-weight:700">
            {text}
        </div>
    '''
    return(shape_text)

def name_header():
    name_header_text = '''
        <p align="center" style="font-size: 25px;">
            <a style="color: #f3c681;" href="https://www.linkedin.com/in/bachtiyarma/">
                <b>Bachtiyar M. Arief</b> 
            </a>
        </p>
    '''
    return(name_header_text)
    
# Mewarnai subtitle
def subtitle(
    text,
    color = '#dc6b29',
    font_size = 30, 
):
    subtitle_text = f'<b><span style="color:{color}; font-size: {font_size}px;">{text}</span></b>'
    return (subtitle_text)

# Membuat scorecard
def score_card():
    score_card_text = """
        <style>
            .score-card {
                border-radius: 10px;
                padding: 10px;
                text-align: left;
                border: 1px solid #FF0000;
            }
        
            .score-label {
                font-size: 22px;
                color: #0E91A1;
                margin-bottom: 1px;
                margin-left: 5px;
                font-family: Arial;
            }
        
            .revenue-value {
                font-size: 40px;
                color: #75d06c;
                font-weight: bold;
                margin-top: -15px;
                margin-left: 5px;
                font-family: Arial;
            }
        </style>
    """
    return(score_card_text)

def summary_rectangle(name, value):
    text = f'''
        <div class="score-card">
            <div class="score-label">{name}</div>
            <div class="revenue-value">{value}</div>
        </div>
    '''
    return(text)
    
# Membuat Note
def note_rectangle():
    note_rectangle_text = """
        <style>
            .notes{
                border-radius: 10px;
                padding: 10px;
                text-align: left;
                background-color: #f6f7f8;
            }
        
            .notes-text {
                font-size: 15px;
                color: #000000;
                margin-bottom: 1px;
                margin-left: 5px;
                font-family: Arial;
            }
        
        </style>
    """
    return(note_rectangle_text)

def recommendation_rectangle(teks):
    text = f'''
        <div class="notes">
            <div class="notes-text">
                <p align="justify">{teks}</p>
            </div>
        </div>
        <br><br>
    '''
    return(text)