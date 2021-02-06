from bs4 import BeautifulSoup
import requests

page1 = requests.get("https://www.petsmartcharities.ca/find-a-pet-results?city_or_zip=toronto%2C%20on&species=cat&geo_range=250&breed_id=&hair&age=&sex&color_id")
soup1 = BeautifulSoup(page1.content, "html.parser")
pic1 = soup1.find('div', attrs={"class": "pet-result"})
img1 = pic1.find('img')
img = img1.get('src')
print(img)
name1 = soup1.find('div', attrs={"class": "pet-name"})
print(name1.text)
breed1 = soup1.find('div', attrs={"class": "pet-breed"})
print(breed1.text)
location1 = soup1.find('span', attrs={"class": "pet-addr-city-state clearfix"})
print(location1.text)
# brd1 is brief_description1
brd1 = soup1.find('div', attrs={"class": "age-sex-size"})
print(brd1.text)

page1 = requests.get("https://www.petsmartcharities.ca/find-a-pet-results/21498826")
soup1 = BeautifulSoup(page1.content, "html.parser")
pic1 = soup1.find('div', attrs={"class": "pet-images"})
img1 = pic1.find('img')
img = img1.get('src')
print(img)
soup1.find()
catdesc1 = soup1.find('div', attrs={"class": "pet-description"})
print(catdesc1.text)
