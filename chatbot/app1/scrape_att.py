from bs4 import BeautifulSoup
import requests
import pickle


def scrape(cls, rollno):
    url = 'http://attendance.mec.ac.in/view4stud.php?class=' + cls + '&submit=view'


    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # pattern = re.compile(r'CSU')
    # table = soup.find('table',{"class":"attn"})

    data = []
    row = soup.findAll("tr")[rollno + 1]
    data.append(row.contents[2].contents[0][5:])
    for i in range(3,11):
        data.append((float)(row.contents[i].contents[0]))


    # print(data)

    with open('att_data.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # with open('att_data.pickle', 'rb') as handle:
    #     b = pickle.load(handle)

    return data



