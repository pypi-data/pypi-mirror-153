import bs4
import requests


class Bencana:
    def __init__(self, url, description):
        self.url = url
        self.description = description
        self.result = None

    def scraping_data(self):
        print('scraping_data not yet implemented')

    def show_data(self):
        print('show_data not yet implemented')

    def show_description(self):
        print(self.description)

    def run(self):
        self.scraping_data()
        self.show_data()


class BanjirTerkini(Bencana):
    def __init__(self, url):
        super(BanjirTerkini, self).__init__(url, 'NOT YET IMPLEMENTED, but it should return lates Flood in Indonesia')

    def show_description(self):
        print(f'\nUNDER CONSTRUCTION {self.description}')

class GempaTerkini(Bencana):
    def __init__(self, url):
        super(GempaTerkini, self).__init__(url, 'To get the latest Eartquake in Indonesia from bmkg.co.id')
    
    def scraping_data(self):
        try:
            content = requests.get(self.url)
        except Exception:
            return None

        if content.status_code == 200:
            soup = bs4.BeautifulSoup(content.text, 'html.parser')

            result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
            result = result.findChildren('li')

            i = 0
            date = None
            hours = None
            magnitude = None
            depth = None
            lu = None
            bt = None
            location = None
            felt = None

            for res in result:
                if i == 0:
                    time = res.text.split(', ')
                    date = time[0]
                    hours = time[1]
                elif i == 1:
                    magnitude = res.text
                elif i == 2:
                    depth = res.text
                elif i == 3:
                    coordinate = res.text.split(' - ')
                    lu = coordinate[0]
                    bt = coordinate[1]
                elif i == 4:
                    location = res.text
                elif i == 5:
                    felt = res.text

                i = i + 1

            data = dict()
            data['time'] = {'date': date, 'hours': hours}
            data['magnitude'] = magnitude
            data['depth'] = depth
            data['coordinate'] = {'lu': lu, 'bt': bt}
            data['location'] = location
            data['felt'] = felt
            self.result = data
        else:
            return None

    def show_data(self):
        if self.result is None:
            print('Data not found')
            return

        print(f"Date : {self.result['time']['date']}")
        print(f"Hours : {self.result['time']['hours']}")
        print(f"Magnitude : {self.result['magnitude']}")
        print(f"Depth : {self.result['depth']}")
        print(f"Coordinate : {self.result['coordinate']['lu']}, {self.result['coordinate']['bt']}")
        print(f"Location : {self.result['location']}")
        print(f"{self.result['felt']}")


if __name__ == '__main__':
    gempa = GempaTerkini('https://www.bmkg.go.id/')
    gempa.show_description()
    gempa.run()

    banjir = BanjirTerkini('NOT YET')
    banjir.show_description()
    banjir.run()
