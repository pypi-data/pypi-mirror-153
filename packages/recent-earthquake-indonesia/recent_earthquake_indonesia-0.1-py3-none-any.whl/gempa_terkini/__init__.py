import requests
from bs4 import BeautifulSoup


def ektraksi_data():
    """
    Tanggal       : 23 Mei 2022
    Waktu         : 19:32:02 WIB
    Magnitudo     : 4.9
    Kedalaman     : 41 km
    Lokasi        : LAT: 4.61 LON : 102.75
    Pusat Gempa   : Pusat gempa berada di laut 25 km baratdaya Bengkulu Selatan
    Dirasakan     : Dirasakan (Skala MMI): IV Manna, IV Argamakmur, IV Lampung Barat,
                    III-IV Kepahiang, III-IV Kota Bengkulu.
    :return:
    """
    try:
        content = requests.get('https://www.bmkg.go.id/')
    except Exception:
        return None
    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')
        result = soup.find('span', {'class': 'waktu'})
        result = result.text.split(', ')
        tanggal = result[0]
        waktu = result[1]

        result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        result = result.findChildren('li')

        i = 0
        magnitudo = None
        kedalaman = None
        ls = None
        bt = None
        lokasi = None
        dirasakan = None

        for res in result:
            if i == 1:
                magnitudo = res.text
            elif i == 2:
                kedalaman = res.text
            elif i == 3:
                koordinat = res.text.split(' - ')
                ls = koordinat[0]
                bt = koordinat[1]
            elif i == 4:
                lokasi = res.text
            elif i == 5:
                dirasakan = res.text
            i = i + 1

        hasil = dict()
        hasil['tanggal'] = tanggal
        hasil['waktu'] = waktu
        hasil['magnitudo'] = magnitudo
        hasil['kedalaman'] = kedalaman
        hasil['koordinat'] = {'ls': ls, 'bt': bt}
        hasil['lokasi'] = lokasi
        hasil['dirasakan'] = dirasakan
        return hasil
    else:
        return None


def tampilkan_data(result):
    if result is None:
        print('Tidak menemukan data gempa terkini')
        return
    print("Gempa terakhir berdasarkan BMKG")
    print(f"Tanggal {result['tanggal']}")
    print(f"waktu {result['waktu']}")
    print(f"Magnitudo {result['magnitudo']}")
    print(f"Kedalaman {result['kedalaman']}")
    print(f"koordinat: ls= {result['koordinat']['ls']} bt= {result['koordinat']['bt']}")
    print(f"Lokasi {result['lokasi']}")
    print(f"{result['dirasakan']}")


if __name__ == "__main__":
    result = ektraksi_data()
    tampilkan_data(result)
