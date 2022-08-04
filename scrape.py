import requests
import datetime
import pandas as pd
from requests_html import HTML
import os

BASE_DIR = os.path.dirname(__file__)

def url_to_txt(url, save = False):
    r = requests.get(url)
    #success
    if r.status_code == 200:
        html_text = r.text
        if save:
            with open(f"bo_worldwide.html", 'w') as f:
                f.write(html_text)
        return html_text
    return None

def parse_and_extract(url, name= "2020"):

    text = url_to_txt(url)
    if not text:
        return
    r_html = HTML(html=text)
    table_class = ".imdb-scroll-table"
    # table_class = "#table" when looking for an id
    r_table = r_html.find(table_class)
    # print(r_table)
    table_data = []
    header_names = []
    if len(r_table) == 0:
        return False
    parsed_table = r_table[0]
    rows = parsed_table.find("tr")
    # print the text of an element using .text
    header_row = rows[0]
    header_names = [x.text for x in header_row.find("th")]
    for row in rows[1:]:
        # print(row.text)
        cols = row.find("td")
        row_data = []
        for i, col in enumerate(cols):
            # print(i, col.text, "\n\n")
            row_data.append(col.text)
        table_data.append(row_data)
    df = pd.DataFrame(table_data, columns= header_names)
    path = os.path.join(BASE_DIR, "data")
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, f"{name}.csv")
    df.to_csv(filepath, index=False)
    return True

def run(start_year= datetime.datetime.now().year, years_ago = 0):
    assert isinstance(start_year, int)
    assert isinstance(years_ago, int)
    assert len(str(start_year)) == 4
    for i in range(years_ago + 1):
        url = f"https://www.boxofficemojo.com/year/world/{start_year - i}/"
        finished = parse_and_extract(url, name = f"movie{start_year-i}")
        if finished:
            print(f"finished: {start_year - i}")
        else:
            print("not found")
if __name__ == "__main__":
    run()