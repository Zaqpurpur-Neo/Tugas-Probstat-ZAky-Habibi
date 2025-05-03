from flask import Flask, jsonify, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import base64
import io

from pandas.io.formats.format import math
matplotlib.use('Agg')

app = Flask(__name__)

df = pd.read_csv('IPK_Mhs.csv')
all_data = {
    "df_table": None,
    "keys": [],
    "data": [],
    "graphic": None
}

def nilai_kekuatan(r):
    label_kekuatan = ["Sangat Lemah", "Lemah", "Lemah", "Kuat", "Sangat Kuat"]
    nilai_r = abs(r)
    if nilai_r >= 0.00 and nilai_r <= 0.199:
        return label_kekuatan[0]
    elif nilai_r >= 0.20 and nilai_r <= 0.399:
        return label_kekuatan[1]
    elif nilai_r >= 0.40 and nilai_r <= 0.599:
        return label_kekuatan[2]
    elif nilai_r >= 0.60 and nilai_r <= 0.799:
        return label_kekuatan[3]
    elif nilai_r >= 0.80 and nilai_r <= 1.00:
        return label_kekuatan[4]


def linear_regresion():
    #  [Lama Belajar (Jam), IPK Semester 2] 
    key = [all_data["keys"][1], all_data["keys"][2]]
    fig, ax = plt.subplots()

    df = all_data["df_table"]
    x = df[key[0]].values 
    y = df[key[1]].values


    x_rata = x.mean()
    y_rata = y.mean()
    
    numerator = ((x - x_rata) * (y - y_rata)).sum()
    denominator = ((x - x_rata) ** 2).sum()
    b = numerator / denominator
    a = y_rata - (b * x_rata)

    y_prediksi = a + (b * x)

    sigma_xy = (x * y).sum()
    sigma_x = x.sum()
    sigma_y = y.sum()
    sigma_x_kuadrat_dalam = (x ** 2).sum()
    sigma_x_kuadrat_luar = sigma_x ** 2
    sigma_y_kuadrat_dalam = (y ** 2).sum()
    sigma_y_kuadrat_luar = sigma_y ** 2
    
    n = len(x)
    pembilang = (n * sigma_xy) - (sigma_x * sigma_y)
    penyebut = math.sqrt(((n * sigma_x_kuadrat_dalam) - sigma_x_kuadrat_luar) * ((n * sigma_y_kuadrat_dalam) - sigma_y_kuadrat_luar))
    r = (pembilang/penyebut)

    label_kekuatan = nilai_kekuatan(r)
    arah = "positif" if r > 0 else "negatif"

    thitung = ( r * math.sqrt(n - 2) )/math.sqrt(1 - ((r) ** 2))
    ttable = 2.074
    
    ax.scatter(x, y, color="blue", label="Data Asli")
    ax.plot(x, y_prediksi, color="red", label="Regresi Linear")
    plt.xlabel(key[0])
    plt.ylabel(key[1])
    plt.title(f'Regresi Linear {key[0]} dengan {key[1]}')
    ax.legend()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(fig)

    data_uri = f"data:image/png;base64,{image_base64}"
    return {
        "gambar": data_uri,
        "a": round(a, 2), "b": round(b, 2), "r": round(r, 4), "n": n,
        "t-hitung": round(thitung, 3), "t-tabel": round(ttable, 3), 
        "label_kekuatan": label_kekuatan,
        "arah": arah
    }

@app.route('/')
def home():
    all_data["df_table"] = df
    if len(all_data["data"]) == 0:
        all_data["keys"] = df.columns.values
        all_data["data"] = df.values.tolist()
        all_data["keys"][1] = all_data["keys"][1] + " (X)"
        all_data["keys"][2] = all_data["keys"][2] + " (Y)"

    data_linear = linear_regresion()
    return render_template('home.html', columns=all_data["keys"], data=all_data["data"], graph=data_linear["gambar"], perhitungan=data_linear)

if __name__ == "__main__":
    app.run(debug=True)

