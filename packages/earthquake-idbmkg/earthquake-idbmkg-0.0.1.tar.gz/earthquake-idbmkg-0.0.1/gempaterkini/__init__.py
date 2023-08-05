import requests
from bs4 import BeautifulSoup


def extract_data():
    try:
        content = requests.get('https://www.bmkg.go.id/')
    except Exception:
        return None

    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')

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
        return data
    else:
        return None


def show_data(result):
    if result is None:
        print('Data not found')
        return

    print(f"Date : {result['time']['date']}")
    print(f"Hours : {result['time']['hours']}")
    print(f"Magnitude : {result['magnitude']}")
    print(f"Depth : {result['depth']}")
    print(f"Coordinate : {result['coordinate']['lu']}, {result['coordinate']['bt']}")
    print(f"Location : {result['location']}")
    print(f"{result['felt']}")


if __name__ == '__main__':
    result = extract_data()
    show_data(result)
