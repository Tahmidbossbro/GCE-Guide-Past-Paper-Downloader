from bs4 import BeautifulSoup
import requests
import os

subject_list = []
subject_code_list = []
year_list = []
papers_list = []
target_website = "https://gceguide.com/past-papers/"

response = requests.get(target_website)

soup = BeautifulSoup(response.text, 'html.parser')

O_level_link = f"https:{soup.find(name='div', id='pgc-9-1-1').find(name='a').get('href')}"
A_level_link = f"https:{soup.find(name='div', id='pgc-9-1-2').find(name='a').get('href')}"

target_course_page = A_level_link  # Change this for O And A Level

response_2 = requests.get(target_course_page)

soup_2 = BeautifulSoup(response_2.text, 'html.parser')

for link in soup_2.find(name='ul', class_='paperslist').find_all(name='li'):
    # subject = link.find(name='a').get('href').split()
    subject = link.find(name='a').get('href')
    subject_code_list.append(subject.split()[-1])
    subject_list.append(subject)

chosen_subject = subject_list[subject_code_list.index(f"({input('Type code: ')})")]  # Get Info

subject_page = f"{target_course_page}/{'%20'.join(chosen_subject.split())}/"  # Physics 37
try:
    parent_dir = "C:\\Users\Tahmid Newaz\Downloads"
    directory = chosen_subject
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
except FileExistsError:
    pass

response_3 = requests.get(subject_page)

soup_3 = BeautifulSoup(response_3.text, 'html.parser')

print("Downloading: ", chosen_subject)
for link in soup_3.find(name='ul', class_='paperslist').find_all(name='li'):
    year = link.find(name='a').get('href')
    page_link = f"{subject_page}/{year}/"

    response_4 = requests.get(page_link)

    soup_4 = BeautifulSoup(response_4.text, 'html.parser')
    try:
        parent_dir_2 = path
        directory_2 = year
        path_2 = os.path.join(parent_dir_2, directory_2)
        os.mkdir(path_2)
    except FileExistsError:
        pass

    for link2 in soup_4.find(name='ul', class_='paperslist').find_all(name='li'):
        download_link = f"{page_link}{link2.find(name='a').get('href')}"
        with open(f"{parent_dir_2}/{year}/{link2.find(name='a').get('href')}", "wb+") as file:
            res = requests.get(download_link)
            file.write(res.content)
