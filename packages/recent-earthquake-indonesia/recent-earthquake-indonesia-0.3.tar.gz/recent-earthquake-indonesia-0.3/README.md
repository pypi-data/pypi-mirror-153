# indonesia-recent-earthquake
This package will get the latest earthquake in Indonesia taken from BMKG | Meteorology, Climatology, and Geophysical Agency

## HOW IT WORK?
This package will scrape data from [bmkg](https://www.bmkg.go.id) to display the latest earthquake that occurred in Indonesia. This package use BeautifulSoup4 dan request. this package uses Beautifulsoup4 and Request to then produce output in the form of JSON which is ready to be used in web and mobile applications

## HOW TO USE
import gempa_terkini

if __name__ == "__main__":
    print('Aplikasi utama')
    result = gempa_terkini.ektraksi_data()
    gempa_terkini.tampilkan_data(result)

## Author
Fauzi Kurniawan