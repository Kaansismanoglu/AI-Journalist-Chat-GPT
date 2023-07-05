import csv
import os
import re
import time
from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup

# Create your views here.

def index(request):
     target_url = "https://www.duhuliye.com"
     resp = requests.get(target_url).content
     soup = BeautifulSoup(resp, "html.parser")
     divs = soup.find("div", {"class": "container mt-3"}).find_all("div", {"class": "swiper-slide"})

     postlist = []

     for div in divs:
          link_element = div.find("a", {"class": "bg-dark"})
          title = link_element.get("title") if link_element else ""
          link = link_element.get("href") if link_element else ""
          image_element = div.find("img", {"class": "img-fluid"})
          image = image_element.get("src") if image_element else ""

          if link:
               target_url_then = target_url + link
               resp_then = requests.get(target_url_then).content
               soup_then = BeautifulSoup(resp_then, "html.parser")
               list2 = soup_then.find("div", {"class": "col-lg-8"}).find_all("div", {"class": "card border-0"})
               for div in list2:
                    content_element = div.find("div", {"class": "article-text text-black container-padding"})
                    content = content_element.text if content_element else ""
                    content_text = re.sub(r'\s+', ' ', content)
                    words = content_text.split()
                    truncated_text = ' '.join(words[:30])
                    postlist.append({'title': title, 'link': target_url + link, 'image': image, "content": truncated_text + "..."})
                    
     # # Kalan Haberleri yazma
     divs2 = soup.find("div", {"class": "row g-2 mb-3"}).find_all("div", {"class": "col-lg-4"})
     postlist2 = []
     for div in divs2:
          link_element2 = div.find("a", {"class": "d-block img-hover-zoom"})
          title2 = link_element2.get("title") if link_element2 else ""
          link2 = link_element2.get("href") if link_element2 else ""
          image_element2 = div.find("img", {"class": "d-block img-fluid"})
          image2 = image_element2.get("src") if image_element2 else ""

          if link2:
               target_url_then2 = target_url + link2
               resp_then2 = requests.get(target_url_then2).content
               soup_then2 = BeautifulSoup(resp_then2, "html.parser")
               list3 = soup_then2.find("div", {"class": "col-lg-8"}).find_all("div", {"class": "card border-0"})
               for div in list3:
                    content_element2 = div.find("div", {"class": "article-text text-black container-padding"})
                    content2 = content_element2.text if content_element2 else ""
                    content_text2 = re.sub(r'\s+', ' ', content2)
                    words2 = content_text2.split()
                    truncated_text2 = ' '.join(words2[:30])
                    postlist2.append({'title': title2, 'link': target_url + link2, 'image': image2, "content": truncated_text2 + "..."})
                         
     context = {
          'postlist': postlist,
          'postlist2': postlist2,
     }

     return render(request, 'pages/index.html', context)
 
def aipage(request):
     target_url = "https://www.duhuliye.com"
     resp = requests.get(target_url).content
     soup = BeautifulSoup(resp, "html.parser")
     divs = soup.find("div", {"class": "container mt-3"}).find_all("div", {"class": "swiper-slide"})

     postlist = []

     for div in divs:
          link_element = div.find("a", {"class": "bg-dark"})
          title = link_element.get("title") if link_element else ""
          link = link_element.get("href") if link_element else ""
          image_element = div.find("img", {"class": "img-fluid"})
          image = image_element.get("src") if image_element else ""

          if link:
               target_url_then = target_url + link
               resp_then = requests.get(target_url_then).content
               soup_then = BeautifulSoup(resp_then, "html.parser")
               list2 = soup_then.find("div", {"class": "col-lg-8"}).find_all("div", {"class": "card border-0"})
               for div in list2:
                    content_element = div.find("div", {"class": "article-text text-black container-padding"})
                    content = content_element.text if content_element else ""
                    content_text = re.sub(r'\s+', ' ', content)
                    words = content_text.split()
                    truncated_text = ' '.join(words[:30])
                    if not any(post['title'] == title and post['link'] == target_url + link for post in postlist):
                         postlist.append({'title': title, 'link': target_url + link, 'image': image, "content": content_text + "..."})
                         
     divs2 = soup.find("div", {"class": "row g-2 mb-3"}).find_all("div", {"class": "col-lg-4"})
     postlist2 = []
     for div in divs2:
          link_element2 = div.find("a", {"class": "d-block img-hover-zoom"})
          title2 = link_element2.get("title") if link_element2 else ""
          link2 = link_element2.get("href") if link_element2 else ""
          image_element2 = div.find("img", {"class": "d-block img-fluid"})
          image2 = image_element2.get("src") if image_element2 else ""

          if link2:
               target_url_then2 = target_url + link2
               resp_then2 = requests.get(target_url_then2).content
               soup_then2 = BeautifulSoup(resp_then2, "html.parser")
               list3 = soup_then2.find("div", {"class": "col-lg-8"}).find_all("div", {"class": "card border-0"})
               for div in list3:
                    content_element2 = div.find("div", {"class": "article-text text-black container-padding"})
                    content2 = content_element2.text if content_element2 else ""
                    content_text2 = re.sub(r'\s+', ' ', content2)
                    words2 = content_text2.split()
                    truncated_text2 = ' '.join(words2[:30])
                    if not any(post['title'] == title2 and post['link'] == target_url + link2 for post in postlist2):
                         postlist2.append({'title': title2, 'link': target_url + link2, 'image': image2, "content": content_text2 + "..."})
     context = {
          'postlist': postlist,
          'postlist2': postlist2,
     }
     folder_path = os.path.dirname(os.path.abspath(__file__))
     filename = "datas.csv"
     file_path = os.path.join(folder_path, filename)

     existing_data = []
     if os.path.exists(file_path):
          with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
               reader = csv.DictReader(csvfile)
               existing_data = list(reader)

     # Mevcut verileri yeni haberlerle birleştirme
     all_data = existing_data + postlist + postlist2

     # Benzersiz haber kontrolü
     unique_data = []
     for data in all_data:
          if data not in unique_data:
               unique_data.append(data)

     # CSV dosyasına yazma
     with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
          writer = csv.DictWriter(csvfile, fieldnames=['title', 'link', 'image', 'content'])
          writer.writeheader()
          writer.writerows(unique_data)

     print("Haberler başarıyla güncellendi.")
     return render(request, 'pages/aipage.html', context)

