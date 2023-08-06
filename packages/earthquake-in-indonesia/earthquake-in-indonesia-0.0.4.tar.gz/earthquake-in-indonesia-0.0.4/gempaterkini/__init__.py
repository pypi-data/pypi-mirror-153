import requests
import bs4

"""
method = fungsi
field atribute = variable
"""


class Bencana:
    def __init__(self, url, description):
        self.description = description
        self.result = None
        self.url = url

    def scraping_data(self):
        pass

    def tampilkan_data(self):
        pass

    def run(self):
        self.scraping_data()
        self.tampilkan_data()


class GempaTerkini(Bencana):
    def __init__(self, url):
        super(GempaTerkini, self).__init__(url, 'To get the latest earthquake information in Indonesia from BMKG.go.id')

    def scraping_data(self):

        try:
            content = requests.get(self.url)
        except Exception:
            return None

        if content.status_code == 200:
            soup = bs4.BeautifulSoup(content.text, 'html.parser')
            result = soup.find('span', {'class': 'waktu'})
            result = result.text.split(', ')
            tanggal = result[0]
            waktu = result[1]

            result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
            result = result.findChildren('li')
            i = 0
            magnitudo = None
            ls = None
            bt = None
            kedalaman = None
            dirasakan = None
            lokasi = None

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
            self.result = hasil
        else:
            return None

    def tampilkan_data(self):
        if self.result is None:
            print("tidak bisa menampilkan data terkini")
            return
        print('Gempa Terakhir Berdasarkan BMKG')
        print(f"Tanggal {self.result['tanggal']}")
        print(f"Waktu {self.result['waktu']}")
        print(f"Magnitudo {self.result['magnitudo']}")
        print(f"Kedalaman {self.result['kedalaman']}")
        print(f"Lokasi {self.result['lokasi']}")
        print(f"Koordinat = LS = {self.result['koordinat']['ls']}, BT={self.result['koordinat']['bt']}")
        print(f"Dirasakan {self.result['dirasakan']}")


# if __name__ == '__main__':
# print('ini adalah package gempa terkini')
# print('hai')

if __name__ == '__main__':
    gempa_di_indonesia = GempaTerkini('https://bmkg.go.id')
    print('Deskripsi class Gempa Terkini', gempa_di_indonesia.description)
    gempa_di_indonesia.run()

    # gempa_di_dunia = GempaTerkini('https://bmkg.go.id')
    # print('Deskripsi class Gempa Dunia', gempa_di_dunia.description)
    # gempa_di_dunia.run()
    # gempa_di_indonesia.ekstraksi_data()
    # gempa_di_indonesia.tampilkan_data()
