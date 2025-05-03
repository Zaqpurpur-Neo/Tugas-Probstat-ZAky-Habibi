from flask import Flask, jsonify, render_template
import json
import math
app = Flask(__name__)

def load_data():
    with open('data.json', 'r') as data:
        return json.load(data)

def nilai_uts(data):
    array = []
    for item in data:
        array.append(item["uts"])
    array.sort()
    return array

def nilai_minimum(data):
    minimum = 0
    for i in range(0, len(data)):
        if i == 0 or data[i] < minimum:
            minimum = data[i]
    return minimum

def nilai_maximum(data):
    maximum = 0
    for i in range(0, len(data)):
        if i == 0 or data[i] > maximum:
            maximum = data[i]
    return maximum

def median(data):
    banyak = len(data)
    if banyak % 2 == 0:
        jumlah = data[int(banyak/2)] + data[int((banyak/2) + 1)]
        return jumlah/2
    else:
        return data[int(banyak/2)]

def kuartil_1(data):
    banyak = len(data)
    q1_data = []
    for i in range(0, int(banyak/2)):
        q1_data.append(data[i])
    return median(q1_data)

def kuartil_3(data):
    banyak = len(data)
    idx_1 = int(banyak/2)
    q3_data = []
    if banyak % 2 != 0:
        idx_1 += 1
    
    for i in range(idx_1, banyak):
        q3_data.append(data[i])
    return median(q3_data)

def varians(data):
    rata_rata = sum(data)/len(data)
    sigma = 0
    for item in data:
        sigma += pow(item - rata_rata, 2)
    varians = sigma/(len(data) - 1)
    return varians

def standar_deviasi(data):
    rata_rata = sum(data)/len(data)
    sigma = 0
    for item in data:
        sigma += pow(item - rata_rata, 2)
    simpangan_baku = math.sqrt(sigma/(len(data) - 1))
    return simpangan_baku

def statistic_data(data):
    nilai = nilai_uts(data)
    return {
        "len": len(nilai),
        "data_urut": nilai,# ", ".join(str(i) for i in nilai),
        "min": nilai_minimum(nilai),
        "max": nilai_maximum(nilai),
        "range": int(nilai_maximum(nilai) - nilai_minimum(nilai)),
        "mean": sum(nilai)/len(nilai),
        "median": median(nilai),
        "standar_deviasi": standar_deviasi(nilai),
        "varians": varians(nilai),
        "mid_range": (nilai_maximum(nilai) + nilai_minimum(nilai))/2,
        "q1": kuartil_1(nilai),
        "q2": median(nilai),
        "q3": kuartil_3(nilai),
        "iqr": kuartil_3(nilai) - kuartil_1(nilai)
    }

@app.route('/')
def home():
    data = load_data()
    statistic = statistic_data(data)
    return render_template('home.html', data_mahasiswa=data, statistik=statistic)

@app.route('/api/data')
def api():
    return load_data()

if __name__ == "__main__":
    app.run(debug=True)

