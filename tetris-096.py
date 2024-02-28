import numpy as np
import pandas as pd
import altair as alt
import streamlit as st

st.set_page_config(
    page_title = 'Pengaruh Penanaman Modal dalam Mengurangi Tingkat Pengangguran Terbuka di Jawa Barat'
    ,layout='wide'
)

st.title('Pengaruh Penanaman Modal dalam Mengurangi Tingkat Pengangguran Terbuka di Jawa Barat')
st.caption('oleh: Mashithoh Putri NI')

# Tabbing
tab1, tab2, tab3 = st.tabs(['**Latar Belakang dan Hipotesa**', '**Data Visualisasi**', '**Kesimpulan dan Saran**'])

with tab1:
    st.header('Latar Belakang')
    st.write("""
Indonesia sebagai negara berkembang yang memiliki letak strategis menjadi salah satu alasan mengapa para investor ingin menanamkan modal untuk berinvestasi.
Selain itu, adanya Sumber Daya Manusia yang melimpah dianggap sebagai sebuah nilai tambah dalam menjalankan proyek investasinya.
             
Apa itu penanaman modal? berdasarkan **Pasal 1 angka 1 UU 25/2007**, penanaman modal adalah segala bentuk kegiatan menanam modal,
baik oleh penanam modal dalam negeri maupun penanam modal asing untuk melakukan usaha di wilayah negara Republik Indonesia.
             
Disisi lain, Jawa Barat sebagai provinsi dengan jumlah penduduk terbanyak di Indonesia, banyak dilirik oleh para investor untuk berinvestasi.
Namun, apakah hal ini memberikan efek yang signifikan dalam menurunkan jumlah pengangguran terbuka di provinsi tersebut?
""")
    
    st.header('Hipotesa')
    st.markdown("""
    1. Bagaimana sebaran data penanaman modal di Provinsi Jawa Barat berdasarkan Kota/Kabupaten?
    2. Bagaimana sebaran data penanaman modal di Provinsi Jawa Barat berdasarkan Sektor Usaha?
    3. Bagaimana trend penanaman modal di Provinsi Jawa barat dalam rentang waktu 2012-2021?
    4. Adakah hubungan antara tingkat penyerapan tenaga kerja dari penanaman modal dengan tingkat pengangguran terbuka di provinsi Jawa Barat?
""")

with tab2:
    st.header('Dashboard Penanaman Modal di Jawa Barat Tahun 2012-2021')
    st.markdown('---')

# Read the data
    df1 = pd.read_csv('https://drive.google.com/uc?export=download&id=17h7sBOGsdJlXF2UCNw6KKa9__vbtDsyy')

# Convert 'tahun' column to datetime
    df1['tahun'] = pd.to_datetime(df1['tahun'], format='%Y')

# Calculate current and previous year
    CURR_YEAR = max(df1['tahun'].dt.year)
    PREV_YEAR = CURR_YEAR - 1
    # st.write(CURR_YEAR)

# Pivot the data
    data = pd.pivot_table(
        data=df1,
        index='tahun',
        aggfunc={
            'jumlah_proyek_asing':'sum',
            'jumlah_proyek_domestik':'sum',
            'nilai_investasi_asing':'sum',
            'nilai_investasi_domestik':'sum',
            'penyerapan_tk_proyek_asing' : 'sum',
            'penyerapan_tk_proyek_domestik' : 'sum',
        }
    ).reset_index()

# Calculate total projects for each year
    data['proyek'] = data['jumlah_proyek_asing'] + data['jumlah_proyek_domestik']
    data['investasi'] = data['nilai_investasi_asing'] + data['nilai_investasi_domestik']
    data['penyerapan_tk'] = data['penyerapan_tk_proyek_asing'] + data['penyerapan_tk_proyek_domestik']
    
    # st.dataframe(data)

# Function to format large numbers
    def format_big_number(num):
        if num >= 1e9:
            return f"{num / 1e9:.2f} Mld"
        elif num >= 1e6:
            return f"{num / 1e6:.2f} Mio"
        elif num >= 1e3:
            return f"{num / 1e3:.2f} K"
        else:
            return f"{num:.2f}"
    
    mx_proyek, mx_investasi, mx_penyerapan_tk = st.columns(3)
    
    # st.write(CURR_YEAR)

    with mx_proyek:
    # Filter data for the current and previous years
        curr_year_data = data[data['tahun'].dt.year == CURR_YEAR]
        prev_year_data = data[data['tahun'].dt.year == PREV_YEAR]

    # Check if there is data for the current year
        if not curr_year_data.empty:
        # If there is data, get the project count for the current year
            curr_proyek = curr_year_data['proyek'].values[0]
        else:
        # If there is no data, set the project count for the current year to 0
            curr_proyek = 0

    # Check if there is data for the previous year
        if not prev_year_data.empty:
        # If there is data, get the project count for the previous year
            prev_proyek = prev_year_data['proyek'].values[0]
        else:
        # If there is no data, set the project count for the previous year to 0
            prev_proyek = 0

    # Calculate the percentage difference between the current and previous years' project counts
        if prev_proyek != 0:
            proyek_diff_pct = 100.0 * (curr_proyek - prev_proyek) / prev_proyek
        else:
            proyek_diff_pct = 0

    # Display the metrics
        st.metric('Jumlah Proyek', value=format_big_number(curr_proyek), delta=f'{proyek_diff_pct:.2f}%')
    
    with mx_investasi:
    # Filter data for the current and previous years
        curr_year_data = data[data['tahun'].dt.year == CURR_YEAR]
        prev_year_data = data[data['tahun'].dt.year == PREV_YEAR]

    # Check if there is data for the current year
        if not curr_year_data.empty:
        # If there is data, get the project count for the current year
            curr_investasi = curr_year_data['investasi'].values[0]
        else:
        # If there is no data, set the project count for the current year to 0
            curr_investasi = 0

    # Check if there is data for the previous year
        if not prev_year_data.empty:
        # If there is data, get the project count for the previous year
            prev_investasi = prev_year_data['investasi'].values[0]
        else:
        # If there is no data, set the project count for the previous year to 0
            prev_investasi = 0

    # Calculate the percentage difference between the current and previous years' project counts
        if prev_investasi != 0:
            investasi_diff_pct = 100.0 * (curr_investasi - prev_investasi) / prev_investasi
        else:
            investasi_diff_pct = 0

    # Display the metrics
        st.metric('Nilai Investasi', value=format_big_number(curr_investasi), delta=f'{investasi_diff_pct:.2f}%')
    
    with mx_penyerapan_tk:
    # Filter data for the current and previous years
        curr_year_data = data[data['tahun'].dt.year == CURR_YEAR]
        prev_year_data = data[data['tahun'].dt.year == PREV_YEAR]

    # Check if there is data for the current year
        if not curr_year_data.empty:
        # If there is data, get the project count for the current year
            curr_penyerapan_tk = curr_year_data['penyerapan_tk'].values[0]
        else:
        # If there is no data, set the project count for the current year to 0
            curr_penyerapan_tk = 0

    # Check if there is data for the previous year
        if not prev_year_data.empty:
        # If there is data, get the project count for the previous year
            prev_penyerapan_tk = prev_year_data['penyerapan_tk'].values[0]
        else:
        # If there is no data, set the project count for the previous year to 0
            prev_penyerapan_tk = 0

    # Calculate the percentage difference between the current and previous years' project counts
        if prev_penyerapan_tk != 0:
            penyerapan_tk_diff_pct = 100.0 * (curr_penyerapan_tk - prev_penyerapan_tk) / prev_penyerapan_tk
        else:
            penyerapan_tk_diff_pct = 0

    # Display the metrics
        st.metric('Jumlah Penyerapan Tenaga Kerja', value=format_big_number(curr_penyerapan_tk), delta=f'{penyerapan_tk_diff_pct:.2f}%')
    
    st.markdown('---')
    # st.write(df1)

    # Buat pilihan tahun menggunakan list unik dari kolom tahun
    tahun_pilihan = sorted(df1['tahun'].dt.year.unique())

    # Buat selectbox untuk memilih tahun
    tahun_terpilih = st.selectbox("Pilih Tahun", tahun_pilihan)

    # Tambahkan subheader
    st.subheader("Sebaran Data Jumlah Proyek Penanamana Modal per Kab/Kota di Jawa Barat Tahun {}".format(tahun_terpilih))

    # Filter data berdasarkan tahun yang dipilih
    df_terfilter = df1[df1['tahun'] == tahun_terpilih]

    # Membuat bar chart interaktif
    bar_chart = alt.Chart(df1).transform_fold(
        ['jumlah_proyek_asing', 'jumlah_proyek_domestik'],
        as_=['Kategori', 'Jumlah Proyek']
    ).mark_bar().encode(
        y='nama_kabupaten_kota:N',
        x='Jumlah Proyek:Q',
        color='Kategori:N',
        tooltip=['nama_kabupaten_kota', 'jumlah_proyek_asing', 'jumlah_proyek_domestik']
    ).interactive().properties(
    width=800,  # atur lebar grafik
    height=400  # atur tinggi grafik
    )

    bar_chart

    # Read the data
    df2 = pd.read_csv('https://drive.google.com/uc?export=download&id=1ipT-cUlTdfpW1JUKfwcZt9G80fTUGHzx')
    
    # Convert 'tahun' column to datetime
    df2['tahun'] = pd.to_datetime(df2['tahun'], format='%Y')
    # st.write(df2)

    # Buat pilihan tahun menggunakan list unik dari kolom tahun
    tahun_pilihan = sorted(df2['tahun'].dt.year.unique())

    # Buat selectbox untuk memilih tahun
    tahun_terpilih = st.selectbox("Tahun", tahun_pilihan)

    # Tambahkan subheader
    st.subheader("Sebaran Data Jumlah Proyek Penanaman Modal per Sektor Usaha di Jawa Barat Tahun {}".format(tahun_terpilih))

    # Filter data berdasarkan tahun yang dipilih
    df_terfilter = df2[df2['tahun'] == tahun_terpilih]

    # Membuat bar chart interaktif
    bar_chart = alt.Chart(df2).transform_fold(
        ['jumlah_proyek_asing', 'jumlah_proyek_domestik'],
        as_=['Kategori', 'Jumlah Proyek']
    ).mark_bar().encode(
        y='kategori_sektor_usaha:N',
        x='Jumlah Proyek:Q',
        color='Kategori:N',
        tooltip=['kategori_sektor_usaha', 'jumlah_proyek_asing', 'jumlah_proyek_domestik']
    ).interactive().properties(
    width=800,
    height=400
    )

    bar_chart

    st.markdown('---')
    st.subheader("Trend Data Penanaman Modal di Jawa Barat Tahun 2012-2021")
    # st.write(df2)
    # print(df2.dtypes)

    # Menambahkan kolom tahun sebagai index
    df2['tahun'] = pd.to_datetime(df2['tahun'])
    df2['tahun'] = pd.to_datetime(df2['tahun']).dt.year
    df2 = df2.set_index('tahun')

    # Menggabungkan data investasi asing dan domestik
    proyek_df = df2.groupby('tahun')[['jumlah_proyek_asing', 'jumlah_proyek_domestik']].sum().reset_index()
    investasi_df = df2.groupby('tahun')[['nilai_investasi_asing', 'nilai_investasi_domestik']].sum().reset_index()
    penyerapan_tk_df = df2.groupby('tahun')[['penyerapan_tk_proyek_asing', 'penyerapan_tk_proyek_domestik']].sum().reset_index()

    # Dictionary untuk menyimpan DataFrame berdasarkan variabel yang dipilih
    dataframes = {
        'Proyek': proyek_df,
        'Investasi': investasi_df,
        'Penyerapan Tenaga Kerja': penyerapan_tk_df
    }

    # Tambahkan select box untuk memilih variabel
    variabel_selected = st.selectbox("Pilih Grafik", list(dataframes.keys()))

    # Filter dataframe berdasarkan pilihan pengguna
    filtered_df = dataframes[variabel_selected]

    # Membuat grafik garis interaktif dengan Altair
    grafik = alt.Chart(filtered_df, width=700, height=400).mark_line(point={"size": 100}).encode(
        x='tahun:O',
        y=alt.Y('value:Q', title=variabel_selected),
        color='variable:N',
        tooltip=['tahun:T', 'value:Q', 'variable:N']
    ).transform_fold(
        fold=list(filtered_df.columns[1:]),
        as_=['variable', 'value']
    ).interactive()

    # Tampilkan grafik menggunakan Streamlit
    st.altair_chart(grafik, use_container_width=True)

    st.markdown('---')
    st.subheader('Korelasi Penanaman Modal dengan Tingkat Pengangguran Terbuka di Provinsi Jawa Barat')
    st.write("""**Tingkat pengangguran terbuka** adalah persentase jumlah pengangguran terhadap jumlah angkatan kerja.
             Angkatan Kerja adalah penduduk usia kerja (15 tahun ke atas) yang bekerja atau punya pekerjaan,
             namun sementara tidak bekerja, dan penggangguran.
             """)
    df3 = pd.read_csv('https://drive.google.com/uc?export=download&id=130L_5cIG6l7n8mTLXxGJDPhYzsprS6bi')
    # st.write(df3)

    # Membuat scatter plot
    scatter_plot = alt.Chart(df3).mark_circle().encode(
        x=alt.X('tingkat_penyerapan_tk', title='Tingkat Penyerapan Tenaga Kerja (dalam %)'),
        y=alt.Y('tingkat_pengangguran_terbuka', title='Tingkat Pengangguran Terbuka (dalam %)')
    )

    # Membuat garis korelasi linear
    linear_regression = alt.Chart(df3).transform_regression(
        'tingkat_penyerapan_tk', 'tingkat_pengangguran_terbuka'  # Perbaiki penulisan nama kolom di sini
    ).mark_line(color='red').encode(
        x='tingkat_penyerapan_tk',
        y='tingkat_pengangguran_terbuka'
    )

    # Menampilkan scatter plot dan garis korelasi linear
    (scatter_plot + linear_regression).properties(
        title='Garis Korelasi Linear',
        width=1000,
        height=800
    )
    scatter_plot + linear_regression

    # Menghitung korelasi antara variabel 'tingkat_pengangguran_terbuka' dan 'tingkat_penyerapan_tk'
    correlation = df3['tingkat_penyerapan_tk'].corr(df3['tingkat_pengangguran_terbuka'])
    st.write("Nilai korelasi:", correlation)

with tab3:
    st.header('Kesimpulan')
    st.markdown("""
    1. proyek penanaman modal di Provinsi Jawa Barat belum tersebar rata, ada kabupaten/kota yang kurang dilirik oleh para investor.
    2. Berdasarkan sektor usaha, sektor perdagangan dan reparasi mendapat penanaman modal yang paling banyak, baik dari investor asing maupun domestik.
       Sementara sektor lainnya cenderung normal.
    3. Trend jumlah proyek baik asing maupun domestik meningkat dari tahun 2012-2021.
       Disisi lain, trend penyerap  an tenaga kerja melalui proyek-proyek tersebut bererak fluktuatif.
    4. Adanya proyek penanaman modal di Provinsi Jawa Barat sedikit mengurangi jumlah pengangguran di daerah tersebut.
""")
    
    st.header('Saran')
    st.markdown("""
    Bagi para pemangku kepentingan, mungkin bisa melirik kabupaten/kota atau sektor usaha yang belum banyak mendapatkan penanaman modal.
    
    Mengingat jumlah pengangguran terbuka di Provinsi Jawa Barat tidak hanya terpusat pada beberapa kabupaten/kota,
    dan tentunya setiap orang yang belum bekerja (sedang mencari pekerjaan) memiliki kemampuan berbeda di setiap sektor usahanya.
""")
