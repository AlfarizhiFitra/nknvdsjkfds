import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import pydeck as pdk

st.set_page_config(page_title="Data COVID-19 Padang", layout="wide")

# --- DATA DUMMY: STATISTIK PER TAHUN ---
# Menampilkan tren zona merah di beberapa kecamatan utama di Padang
data_covid = pd.DataFrame({
    'tahun': [2020, 2020, 2020, 2021, 2021, 2021, 2022, 2022, 2022, 2023, 2023, 2023],
    'kecamatan': ['Padang Barat', 'Koto Tangah', 'Pauh', 'Padang Barat', 'Koto Tangah', 'Pauh', 'Padang Barat', 'Koto Tangah', 'Pauh', 'Padang Barat', 'Koto Tangah', 'Pauh'],
    'lat': [-0.9515, -0.8500, -0.9300, -0.9515, -0.8500, -0.9300, -0.9515, -0.8500, -0.9300, -0.9515, -0.8500, -0.9300],
    'lon': [100.3540, 100.3500, 100.4500, 100.3540, 100.3500, 100.4500, 100.3540, 100.3500, 100.4500, 100.3540, 100.3500, 100.4500],
    'kasus': [150, 200, 80, 450, 600, 300, 100, 150, 50, 10, 20, 5],
    'status_zona': ['Oranye', 'Merah', 'Kuning', 'Merah', 'Merah', 'Oranye', 'Kuning', 'Kuning', 'Hijau', 'Hijau', 'Hijau', 'Hijau']
})

# --- SIDEBAR & NAVIGASI ---
st.sidebar.title("Filter Data")
tahun_pilihan = st.sidebar.slider("Pilih Tahun:", 2020, 2023, 2021)
df_filtered = data_covid[data_covid['tahun'] == tahun_pilihan]

# --- HALAMAN UTAMA ---
st.title(f"📊 Pendataan Zona COVID-19 Kota Padang ({tahun_pilihan})")
st.markdown("Visualisasi ini menunjukkan pergerakan status zona per kecamatan berdasarkan jumlah kasus dummy.")

# Komponen Metrik
total_kasus = df_filtered['kasus'].sum()
zona_merah = len(df_filtered[df_filtered['status_zona'] == 'Merah'])

col1, col2, col3 = st.columns(3)
col1.metric("Total Kasus", total_kasus)
col2.metric("Kecamatan Zona Merah", zona_merah)
col3.metric("Tahun Pantau", tahun_pilihan)

# --- VISUALISASI PETA ---
tab1, tab2 = st.tabs(["🗺️ Peta Interaktif (Folium)", "🏗️ Visualisasi 3D (Pydeck)"])

with tab1:
    m = folium.Map(location=[-0.9000, 100.3800], zoom_start=11)
    for i, row in df_filtered.iterrows():
        warna = 'red' if row['status_zona'] == 'Merah' else 'orange' if row['status_zona'] == 'Oranye' else 'green'
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=row['kasus']/20, # Ukuran berdasarkan jumlah kasus
            color=warna,
            fill=True,
            fill_color=warna,
            popup=f"{row['kecamatan']}: {row['kasus']} Kasus"
        ).add_to(m)
    st_folium(m, width=1000, height=500)

with tab2:
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(latitude=-0.9000, longitude=100.3800, zoom=10, pitch=45),
        layers=[
            pdk.Layer(
                "ColumnLayer",
                df_filtered,
                get_position='[lon, lat]',
                get_elevation='kasus',
                elevation_scale=10,
                radius=500,
                get_fill_color="[255, kasus > 300 ? 0 : 150, 0, 150]",
                pickable=True
            ),
        ],
    ))

st.write("Data mentah untuk tahun yang dipilih:", df_filtered)
