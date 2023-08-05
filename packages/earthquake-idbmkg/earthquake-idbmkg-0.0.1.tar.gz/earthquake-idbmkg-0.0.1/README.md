# Realtime Indonesia Earthquake
This package will get the latest eartquake data from BMKG | Indonesia Meteorological, Climatological, and Geophysical Agency

## How it work?
This package will scrape from [BMKG](https://www.bmkg.go.id/) to get the latest earthquake happened in indonesia

This package will use BeautifullSoup4 and Request, to produce output from JSON and ready to used in Web or Mobile applications

## How to use

````
import gempaterkini

if __name__ == '__main__':
    print('Main app')
    print('\nLatest Earthquake data from BMKG | Indonesia Meteorological, Climatological, and Geophysical Agency\n')
    result = gempaterkini.extract_data()
    gempaterkini.show_data(result)
````

