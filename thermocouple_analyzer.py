import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Data Thermocouple (Tidak ada perubahan) ---
thermocouples = {
    "Type B": {
        "material": "Platinum 30% Rhodium – Platinum 6% Rhodium",
        "wire_color": {"ANSI": "Plus: Gray, Minus: Gray", "IEC": "Plus: White, Minus: White"},
        "temp_range": (0, 1820), "voltage_curve": lambda T: 0.005 * T, "tolerance": 0.25
    },
    "Type E": {
        "material": "Chromel – Constantan",
        "wire_color": {"ANSI": "Plus: Purple, Minus: Red", "IEC": "Plus: Violet, Minus: White"},
        "temp_range": (-200, 900), "voltage_curve": lambda T: 0.061 * T, "tolerance": 0.5
    },
    "Type J": {
        "material": "Iron – Constantan",
        "wire_color": {"ANSI": "Plus: Black, Minus: White", "IEC": "Plus: Black, Minus: White"},
        "temp_range": (-210, 760), "voltage_curve": lambda T: 0.055 * T, "tolerance": 0.5
    },
    "Type K": {
        "material": "Chromel – Alumel",
        "wire_color": {"ANSI": "Plus: Yellow, Minus: Red", "IEC": "Plus: Green, Minus: White"},
        "temp_range": (-200, 1372), "voltage_curve": lambda T: 0.041 * T, "tolerance": 0.5
    },
    "Type N": {
        "material": "Nicrosil – Nisil",
        "wire_color": {"ANSI": "Plus: Orange, Minus: Red", "IEC": "Plus: Pink, Minus: White"},
        "temp_range": (-200, 1300), "voltage_curve": lambda T: 0.039 * T, "tolerance": 0.5
    },
    "Type R": {
        "material": "Platinum 13% Rhodium – Platinum",
        "wire_color": {"ANSI": "Plus: Black, Minus: Red", "IEC": "Plus: Orange, Minus: White"},
        "temp_range": (0, 1768), "voltage_curve": lambda T: 0.010 * T, "tolerance": 0.25
    },
    "Type S": {
        "material": "Platinum 10% Rhodium – Platinum",
        "wire_color": {"ANSI": "Plus: Black, Minus: Red", "IEC": "Plus: Orange, Minus: White"},
        "temp_range": (0, 1768), "voltage_curve": lambda T: 0.009 * T, "tolerance": 0.25
    },
    "Type T": {
        "material": "Copper – Constantan",
        "wire_color": {"ANSI": "Plus: Blue, Minus: Red", "IEC": "Plus: Brown, Minus: White"},
        "temp_range": (-200, 400), "voltage_curve": lambda T: 0.043 * T, "tolerance": 0.5
    }
}

# --- Antarmuka Pengguna Streamlit ---
st.set_page_config(page_title="Thermocouple Analyzer", layout="wide", initial_sidebar_state="expanded")
st.title("🌡️ Thermocouple Analyzer")
st.markdown("Aplikasi web untuk menganalisis dan memvisualisasikan data thermocouple secara interaktif.")

# Input widgets di sidebar
st.sidebar.header("Input Parameter")
t_type = st.sidebar.selectbox("Pilih Tipe Thermocouple:", options=list(thermocouples.keys()))
temperature = st.sidebar.number_input("Masukkan Suhu (°C):", value=25.0, format="%.1f")
measured_mv = st.sidebar.number_input("Masukkan Tegangan Terukur (mV):", value=0.0, format="%.3f")

# Tombol untuk memicu analisis
if st.sidebar.button("⚙️ Analisis & Visualisasi", use_container_width=True):
    data = thermocouples[t_type]
    v_expected = data["voltage_curve"](temperature)
    minT, maxT = data["temp_range"]
    tolerance = data["tolerance"]

    # --- Tampilkan Hasil ---
    col1, col2 = st.columns([1, 1.5]) # Membuat dua kolom untuk tata letak

    with col1:
        st.subheader(f"📌 Informasi: {t_type}")
        st.markdown(f"**Material:** `{data['material']}`")
        st.markdown(f"**Rentang Suhu:** `{minT}°C` – `{maxT}°C`")
        st.markdown("**Warna Kabel (Standar):**")
        st.markdown(f"  - **ANSI:** `{data['wire_color']['ANSI']}`")
        st.markdown(f"  - **IEC:** `{data['wire_color']['IEC']}`")

        st.subheader("📊 Hasil Analisis")
        st.metric(label="Suhu Input", value=f"{temperature:.1f} °C")

        if not (minT <= temperature <= maxT):
            st.warning(f"Suhu {temperature}°C berada di luar rentang kerja efektif thermocouple ({minT}°C – {maxT}°C).")

        st.metric(label="Tegangan Standar (Diharapkan)", value=f"{v_expected:.3f} mV")
        st.metric(label="Tegangan Terukur", value=f"{measured_mv:.3f} mV")

        dev = abs(v_expected - measured_mv)
        
        st.subheader("✅ Kesimpulan")
        if dev <= tolerance:
            st.success(f"Perbedaan **{dev:.3f} mV** masih dalam batas toleransi ({tolerance:.2f} mV). Thermocouple kemungkinan berfungsi baik.")
        else:
            st.error(f"Perbedaan **{dev:.3f} mV** melebihi batas toleransi ({tolerance:.2f} mV). Ada indikasi penyimpangan atau kerusakan.")

    with col2:
        st.subheader("📈 Grafik Tegangan vs. Suhu")
        
        # Buat data untuk plot
        T_vals = np.linspace(minT, maxT, 400)
        V_vals = data["voltage_curve"](T_vals)

        # Buat plot menggunakan Matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(T_vals, V_vals, label=f"Kurva Ideal {t_type}", color='royalblue', linewidth=2)
        ax.axvline(temperature, color='dimgray', linestyle='--', label=f'Suhu Input ({temperature}°C)')
        ax.scatter(temperature, v_expected, color='limegreen', s=100, zorder=5, label=f"Standar: {v_expected:.3f} mV")
        ax.scatter(temperature, measured_mv, color='crimson', s=100, zorder=5, label=f"Terukur: {measured_mv:.3f} mV")

        ax.set_title(f"Grafik Karakteristik Thermocouple {t_type}", fontsize=16, weight='bold')
        ax.set_xlabel("Suhu (°C)", fontsize=12)
        ax.set_ylabel("Tegangan (mV)", fontsize=12)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend(fontsize=10)
        ax.set_xlim(minT, maxT)
        plt.tight_layout()

        # Tampilkan plot di Streamlit
        st.pyplot(fig)
else:
    st.info("💡 Masukkan parameter di sidebar kiri dan klik tombol untuk memulai analisis.")
