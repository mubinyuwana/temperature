#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output

# Data thermocouple dengan informasi tambahan
thermocouples = {
    "Type B": {
        "material": "Platinum 30% Rhodium – Platinum 6% Rhodium",
        "wire_color": {
            "ANSI": "Plus: Gray, Minus: Gray",
            "IEC": "Plus: White, Minus: White"
        },
        "temp_range": (0, 1820),
        "voltage_curve": lambda T: 0.005 * T,
        "tolerance": 0.25
    },
    "Type E": {
        "material": "Chromel – Constantan",
        "wire_color": {
            "ANSI": "Plus: Purple, Minus: Red",
            "IEC": "Plus: Violet, Minus: White"
        },
        "temp_range": (-200, 900),
        "voltage_curve": lambda T: 0.061 * T,
        "tolerance": 0.5
    },
    "Type J": {
        "material": "Iron – Constantan",
        "wire_color": {
            "ANSI": "Plus: Black, Minus: White",
            "IEC": "Plus: Black, Minus: White"
        },
        "temp_range": (-210, 760),
        "voltage_curve": lambda T: 0.055 * T,
        "tolerance": 0.5
    },
    "Type K": {
        "material": "Chromel – Alumel",
        "wire_color": {
            "ANSI": "Plus: Yellow, Minus: Red",
            "IEC": "Plus: Green, Minus: White"
        },
        "temp_range": (-200, 1372),
        "voltage_curve": lambda T: 0.041 * T,
        "tolerance": 0.5
    },
    "Type N": {
        "material": "Nicrosil – Nisil",
        "wire_color": {
            "ANSI": "Plus: Orange, Minus: Red",
            "IEC": "Plus: Pink, Minus: White"
        },
        "temp_range": (-200, 1300),
        "voltage_curve": lambda T: 0.039 * T,
        "tolerance": 0.5
    },
    "Type R": {
        "material": "Platinum 13% Rhodium – Platinum",
        "wire_color": {
            "ANSI": "Plus: Black, Minus: Red",
            "IEC": "Plus: Orange, Minus: White"
        },
        "temp_range": (0, 1768),
        "voltage_curve": lambda T: 0.010 * T,
        "tolerance": 0.25
    },
    "Type S": {
        "material": "Platinum 10% Rhodium – Platinum",
        "wire_color": {
            "ANSI": "Plus: Black, Minus: Red",
            "IEC": "Plus: Orange, Minus: White"
        },
        "temp_range": (0, 1768),
        "voltage_curve": lambda T: 0.009 * T,
        "tolerance": 0.25
    },
    "Type T": {
        "material": "Copper – Constantan",
        "wire_color": {
            "ANSI": "Plus: Blue, Minus: Red",
            "IEC": "Plus: Brown, Minus: White"
        },
        "temp_range": (-200, 400),
        "voltage_curve": lambda T: 0.043 * T,
        "tolerance": 0.5
    }
}

dropdown_type = widgets.Dropdown(options=thermocouples.keys(), description="Tipe:")
input_temp = widgets.FloatText(value=25.0, description="Suhu (°C):")
input_measured_mv = widgets.FloatText(value=0.0, description="mV Terukur:")
btn_generate = widgets.Button(description="Generate", button_style='success')
output = widgets.Output()

def generate_clicked(b):
    with output:
        clear_output()
        t_type = dropdown_type.value
        temperature = input_temp.value
        measured_mv = input_measured_mv.value

        data = thermocouples[t_type]
        v_expected = data["voltage_curve"](temperature)
        minT, maxT = data["temp_range"]
        tolerance = data["tolerance"]

        print(f"📌 Thermocouple Type: {t_type}")
        print(f"🔧 Material: {data['material']}")
        print(f"🎨 Wire Colors:")
        print(f"   • ANSI: {data['wire_color']['ANSI']}")
        print(f"   • IEC : {data['wire_color']['IEC']}")
        print(f"🌡️ Suhu Input: {temperature:.1f} °C")
        print(f"📏 Rentang Suhu: {minT} °C – {maxT} °C")

        if not (minT <= temperature <= maxT):
            print("⚠️ Suhu di luar batas kerja thermocouple!")

        print(f"⚡ Tegangan Standar: {v_expected:.3f} mV")
        print(f"🧪 Tegangan Terukur: {measured_mv:.3f} mV")

        dev = abs(v_expected - measured_mv)
        if dev <= tolerance:
            print(f"✅ Perbedaan {dev:.3f} mV masih dalam toleransi ({tolerance:.2f} mV). Thermocouple OK.")
        else:
            print(f"❌ Perbedaan {dev:.3f} mV melebihi toleransi ({tolerance:.2f} mV). Ada kemungkinan penyimpangan.")

        T_vals = np.linspace(minT, maxT, 300)
        V_vals = data["voltage_curve"](T_vals)

        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(T_vals, V_vals, label="Kurva Thermocouple", color='blue', linewidth=2)
        ax.axvline(temperature, color='gray', linestyle='--', label='Suhu Input')
        ax.scatter(temperature, v_expected, color='green', label="Tegangan Standar", zorder=5, s=80)
        ax.scatter(temperature, measured_mv, color='red', label="Tegangan Terukur", zorder=5, s=80)

        ax.set_title(f"Tegangan vs Suhu – Thermocouple {t_type}", fontsize=14)
        ax.set_xlabel("Suhu (°C)")
        ax.set_ylabel("Tegangan (mV)")
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend()
        plt.tight_layout()
        plt.show()

btn_generate.on_click(generate_clicked)
display(dropdown_type, input_temp, input_measured_mv, btn_generate, output)

