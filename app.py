import streamlit as st
import pandas as pd
import pydeck as pdk
import folium
from streamlit_folium import st_folium
import numpy as np

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Geo-Spasial Master App", layout="wide")

# --- NAVIGASI SIDEBAR ---
# Gabungan konsep dari selectbox.ipynb
st.sidebar.title("Navigasi Tugas")
menu = st.sidebar.radio(
    "Pilih Modul Visualisasi:",
    ["🏠 Beranda", "📊 Widget Interaktif", "🏗️ Peta 3D (Pydeck)", "🗺️ Peta GeoJSON (Folium)"]
)

# --- HALAMAN 1: BERANDA ---
if menu == "🏠 Beranda":
    st.title("Aplikasi Integrasi Visualisasi Data Geo-Spasial")
    st.write("Aplikasi ini menggabungkan materi dari 4 notebook menjadi satu kesatuan.")
    st.info("Gunakan menu di sidebar untuk berpindah antar modul.")
    
    # Konsep metric untuk ringkasan data
    c1, c2, c3 = st.columns(3)
    c1.metric("Kota Fokus", "Padang")
    c2.metric("Teknologi", "Streamlit")
    c3.metric("Data", "Geo-JSON")

# --- HALAMAN 2: WIDGET (Konsep dari widgetslider & selectbox.ipynb) ---
elif menu == "📊 Widget Interaktif":
    st.title("Eksperimen Widget Slider & Selectbox")
    
    # Konsep dari widgetslider.ipynb
    tahun = st.slider("Pilih Tahun Analisis", 2015, 2025, 2020)
    st.write(f"Tahun yang dipilih: **{tahun}**")
    
    # Konsep dari selectbox.ipynb
    kota = st.selectbox("Pilih Kota:", ["Padang", "Bukittinggi", "Payakumbuh", "Solok"])
    if kota == "Padang":
        st.success("Padang adalah ibu kota Sumatera Barat")
    elif kota == "Bukittinggi":
        st.info("Bukittinggi terkenal dengan Jam Gadang")
    else:
        st.warning(f"Menampilkan data untuk {kota}")

# --- HALAMAN 3: PETA TITIK (Alternatif Pydeck) ---
elif menu == "🏗️ Peta 3D (Pydeck)":
    st.title("Visualisasi Titik Koordinat")
    st.write("Menampilkan titik lokasi menggunakan komponen bawaan st.map().")
    
    # Data dari pydeck.ipynb (Koordinat Padang)
    data_padang = pd.DataFrame({
        "lat": [-0.9471],
        "lon": [100.4172]
    })

    # Menggunakan st.map yang lebih stabil untuk lingkungan Colab
    st.map(data_padang, zoom=11)
    st.info("Catatan: st.map digunakan sebagai alternatif yang lebih ringan untuk lingkungan Colab.")

# --- HALAMAN 4: FOLIUM (Konsep dari Untitled39.ipynb) ---
elif menu == "🗺️ Peta GeoJSON (Folium)":
    st.title("Peta GeoJSON & Color Picker")
    
    # Komponen Interaktif tambahan
    warna = st.color_picker("Pilih Warna Wilayah", "#3498db")
    
    # Data Dummy GeoJSON
    geojson_data = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {"nama": "Wilayah Latihan"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[100.35, -0.90], [100.45, -0.90], [100.45, -1.00], [100.35, -1.00], [100.35, -0.90]]]
            }
        }]
    }

    m = folium.Map(location=[-0.9471, 100.4172], zoom_start=11)
    folium.GeoJson(
        geojson_data,
        style_function=lambda x: {
            "fillColor": warna,
            "color": "black",
            "weight": 2,
            "fillOpacity": 0.5
        }
    ).add_to(m)

    st_folium(m, width=800, height=500)
