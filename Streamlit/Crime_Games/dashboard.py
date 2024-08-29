import requests
import warnings
import streamlit
import encryption
from PIL import Image
from io import BytesIO

warnings.filterwarnings('ignore') 

# Konfigurasi awal streamlit
streamlit.set_page_config(
    page_title = 'Games Detective', 
    page_icon = '🔎', 
    layout = 'wide'
)

def markdown_html(rows, text):
    rows.markdown(
        text,
        unsafe_allow_html = True
    )
    
def garis_pemisah(count):
    line = str()
    for i in range(1, count):
        line += '─'
    return(line)
    
def teks_pemisah_halaman():
    _, row, _ = streamlit.columns([1, 15, 1])
    teks_pemisah = f'<br><br><p align="center" style="font-size: 25px;">{garis_pemisah(15)}  📸 📰 🔎 📝 🗂️ 📼 {garis_pemisah(15)}<br><br></p>'
    markdown_html(row, text = teks_pemisah)
    
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

def aturan_main():
    _, row1, _, row2, _ = streamlit.columns([0.5, 3, 0.1, 7, 0.1])
    
    image_url = "https://raw.githubusercontent.com/bachtiyarma/Python/main/Streamlit/Crime%20Games/Detective-2.png"
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    
    # Mengubah ukuran gambar 121 292
    desired_width = 207
    desired_height = 500
    resized_img = img.resize((desired_width, desired_height))
    
    # Menampilkan gambar dengan ukuran yang diubah
    row1.image(resized_img, use_column_width = False)

    text = """
    <ol>
        <li>Gunakan <code>console.cloud.google.com</code> untuk melakukan perhitungan (<i>querying</i>)</li>    
        <li>Nama Tabel yang digunakan <code>bigquery-public-data.london_crime.crime_by_lsoa</code></li>
        <li>Periode Data yang digunakan hanya dari tahun Januari 2008 hingga Desember 2016</li>
        <li>Jika jawaban berupa bilangan real (float) maka bulatkan menjadi 2 angka dibelakang koma</li>
        <li>Teka - teki akan terbongkar jika semua jawaban yang diinput dan di submit benar</li>
        
    </ol>
    """
    markdown_html(row2, '<br><h3>Rules :</h3>')
    markdown_html(row2, text = note_rectangle())
    row2.write(
        recommendation_rectangle(text),
        unsafe_allow_html = True
    )
    
def clue_number_1():
    _, row, _ = streamlit.columns([0.1, 7.2, 0.1])
    _, row1, _, row2, _ = streamlit.columns([3.1, 4, 1.2, 4, 1])
    
    image_url = "https://raw.githubusercontent.com/bachtiyarma/Python/main/Streamlit/Crime%20Games/Crime-1.jpg"
    row.image(image_url, use_column_width = True)
    
    answer1A = row1.selectbox(
        'Pilih Tahun',
        list(range(2008, 2017)),
        key = 'Answer1A'
    )
    
    answer1B = row2.number_input(
        'Jumlah Kriminalitas (Pada Tahun Dipilih)', 
        value = None, 
        placeholder = 'Type a number...',
        key = 'Answer1B',
        format = '%.0f'
    )
    
    try:
        answer1B = int(round(answer1B, 0))
    except:
        pass
    
    teks_pemisah_halaman()
    return(answer1A, answer1B)

def clue_number_2():
    _, row, _ = streamlit.columns([0.1, 7.2, 0.1])
    _, row1, _, row2, _ = streamlit.columns([0.7, 4, 1.2, 4, 3.1])
     
    image_url = "https://raw.githubusercontent.com/bachtiyarma/Python/main/Streamlit/Crime%20Games/Crime-2.jpg"
    row.image(image_url, use_column_width = True)
    
    months = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ]
    
    answer2A = row1.selectbox(
        'Pilih Bulan',
        months,
        key = 'Answer2A'
    )
    
    answer2B = row2.selectbox(
        'Pilih Tahun',
        list(range(2008, 2017)),
        key = 'Answer2B'
    )
    
    teks_pemisah_halaman()
    return(answer2A, answer2B)

def clue_number_3():
    _, row, _ = streamlit.columns([0.1, 7.2, 0.1])
    _, row1, _, row2, _ = streamlit.columns([3.1, 4, 0.5, 4.7, 1])
     
    image_url1 = "https://raw.githubusercontent.com/bachtiyarma/Python/main/Streamlit/Crime%20Games/Crime-3.jpg"
    row.image(image_url1, use_column_width = True)
    
    image_url2 = "https://raw.githubusercontent.com/bachtiyarma/Python/main/Streamlit/Crime%20Games/London-Map-Crime.png"
    row2.image(image_url2, use_column_width = True)
    
    borough = ['Barking and Dagenham', 'Barnet', 'Bexley', 'Brent', 'Bromley',
       'Camden', 'City of London', 'Croydon', 'Ealing', 'Enfield',
       'Greenwich', 'Hackney', 'Hammersmith and Fulham', 'Haringey',
       'Harrow', 'Havering', 'Hillingdon', 'Hounslow', 'Islington',
       'Kensington and Chelsea', 'Kingston upon Thames', 'Lambeth',
       'Lewisham', 'Merton', 'Newham', 'Redbridge',
       'Richmond upon Thames', 'Southwark', 'Sutton', 'Tower Hamlets',
       'Waltham Forest', 'Wandsworth', 'Westminster']
    
    answer3A = row1.selectbox(
        'Wilayah',
        borough,
        key = 'Answer3A'
    )
    
    markdown_html(row1, '<br>')
    
    answer3B = row1.number_input(
        'Jumlah Kriminalitas Terjadi di Daerah Tersebut (2008 - 2016)', 
        value = None, 
        placeholder = 'Type a number...',
        key = 'Answer3B',
        format = '%.0f'
    )
    
    try:
        answer3B = int(round(answer3B, 0))
    except:
        pass
    
    teks_pemisah_halaman()
    return(answer3A, answer3B)

def clue_number_4():
    _, row, _ = streamlit.columns([0.1, 7.2, 0.1])
    _, row1, _, row2, _, row3, _ = streamlit.columns([0.6, 3, 0.1, 3, 0.1, 3, 2.2])
     
    image_url = "https://raw.githubusercontent.com/bachtiyarma/Python/main/Streamlit/Crime%20Games/Crime-4.jpg"
    row.image(image_url, use_column_width = True)
    
    major_crime = ['Burglary', 'Criminal Damage', 'Drugs', 'Fraud or Forgery',
       'Other Notifiable Offences', 'Robbery', 'Sexual Offences',
       'Theft and Handling', 'Violence Against the Person']
    
    answer4A = row1.selectbox(
        'Pilih Major Crime',
        major_crime,
        key = 'Answer4A'
    )
    
    answer4B = row2.number_input(
        'Total Kriminalitas', 
        value = None, 
        placeholder = 'Type a number...',
        key = 'Answer4B',
        format = '%.0f'
    )
    
    try:
        answer4B = int(round(answer4B, 0))
    except:
        pass
    
    answer4C = row3.number_input(
        'Presentase Kriminalitas Tersebut % (dari Total)', 
        value = None, 
        placeholder = 'Type a number...',
        key = 'Answer4C'
    )
    
    
    teks_pemisah_halaman()
    return(answer4A, answer4B, answer4C)

def final_answer(all_answer):
    _, row1, _ = streamlit.columns([1, 7.2, 1])
    _, row2, _ = streamlit.columns([5.7, 2, 5.3])
    
    teks1 = '''
        <p align="center" style="font-size: 45px;">
            <b>Who Are We?</b>
        </p>
    '''
    row1.write(
        f'{teks1}',
        unsafe_allow_html = True
    )
    
    clicked = row2.button('Submit Answer')
    markdown_html(row1, text = note_rectangle())
    
    if(clicked):
        encrypted = 'vF2veKSs5I5Ea12dVJb+vTR4GPpfonqSi9f0ZoYzwNM='
        hashed_key = encryption.hash_key(all_answer.encode('utf-8'), 'sha256')
        try:
            decrypted = encryption.decrypt_ecb(encrypted, hashed_key)
        except:
            decrypted = hashed_key
            
        
        teks2 = f'''
            <p align="center" style="font-size: 35px;">
                <b>{decrypted}</b>
            </p>
        '''
        row1.write(
            recommendation_rectangle(f'{teks2}'),
            unsafe_allow_html = True
        )

def header():
    _, row1, _, = streamlit.columns([0.1, 7.2, 0.1])
    
    image_url = "https://raw.githubusercontent.com/bachtiyarma/Python/main/Streamlit/Crime%20Games/Header%20Crime.png"
    row1.image(image_url, use_column_width = True)
    
    teks = 'Kejahatan semakin merajalela di London akhir-akhir ini. Kami menduga dalang dibalik tindak kriminal ini dilakukan secara berkelompok. Dugaan sementara adalah gangster. Ah.. Gangster ini sangat sulit dilacak karena mereka cukup tertutup dan rapi dalam melakukan setiap tindak kejahatannya. Namun, setelah dilakukan pemeriksaan secara menyeluruh, kami menemukan secarik kertas bertuliskan kode rahasia seperti berikut<br><p align="center"><b>vF2veKSs5I5Ea12dVJb+vTR4GPpfonqSi9f0ZoYzwNM=</b></p><p align="justify">Kami mencurigai pesan dibalik kode tersebut adalah nama gangster yang ingin kami selidiki. Kita tidak dapat melakukannya sendiri, kami perlu bantuanmu untuk memecahkan misteri ini. Kamu hanya perlu menganalisa pola kejahatan yang telah kami kumpulkan pertanyaannya. Jika kamu dapat menjawab semua pertanyaan ini dengan tepat, maka nama gangster akan muncul (dibagian paling bawah) dan segera laporkan ke kami atas pemecahan teka-teki tersebut dan bersama kami menumpas kejahatan yang selama ini meresahkan masyarakat</p>'
    teks = f'''
            <p align="justify" style="font-size: 11x;">
                {teks}
            </p>
        '''
    row1.write(
        recommendation_rectangle(f'{teks}'),
        unsafe_allow_html = True
    )

if __name__ == "__main__" :
    header()
    aturan_main()
    teks_pemisah_halaman()
    
    answer1A, answer1B = clue_number_1()
    answer2A, answer2B = clue_number_2()
    answer3A, answer3B = clue_number_3()
    answer4A, answer4B, answer4C = clue_number_4()
    
    all_answer = [answer1A, answer1B, answer2A, answer2B, answer3A, answer3B, answer4A, answer4B, answer4C] 
    all_answer = [str(ans) for ans in all_answer]
    all_answer = "".join(all_answer)
    
    final_answer(all_answer)
    
