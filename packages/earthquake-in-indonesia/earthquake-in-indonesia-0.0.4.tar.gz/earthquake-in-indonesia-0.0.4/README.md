# latest-information-earthquake-update--indonesia
this package will scrape information in website Indonesian Agency for Meteorology, Climatology, and Geophysics (BMKG)

## HOW IT WORKS
This package will help you to retrieve data from the [BMKG](https://www.bmkg.go.id) Website, to get the latest information on the last earthquake in Indonesia, and generate JSON output to be applied to the web or mobile aplication


### HOW TO USE

```
import gempaterkini

if __name__ == '__main__':
    print('aplikasi utama')
    result = gempaterkini.ekstraksi_data()
    gempaterkini.tampilkan_data(result)
```

### Author : Hendra Kusuma
