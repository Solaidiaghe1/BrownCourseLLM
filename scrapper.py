import json
import os
import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://cs.brown.edu"
MAIN_URL = f"{BASE_URL}/courses/"
OUTPUT_PATH = "data/courses.json"

def get_main_courses():
    response = requests.get(COURSES_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    courses = []

    for row in soup.find_all("tr"):
        col = row.find_all("td")
        if len(col) < 2:
            continue
        course_code = col[0]
        title_cell = col[1]
        linkToCoursePage = course_code.find_all("a")

        if not linkToCoursePage or "href" not in linkToCoursePage.attrs:
            continue

        courseHM = {
            "course code": course_code.text.strip(),
            "title" : title_cell.text.strip(),
            "url": linkToCoursePage["href"]
        }

    courses.append(courseHM)

    return courses

def get_table_value(label, soup):
    for row in soup.find_all("tr"):
        col = row.find_all("td")

    if len(col) >=2 and label in col[0]:
        return col[1].text.strip()
    
    else: return "N/A"


def getDescription(soup):
    for paragraphs in soup.find_all("p"):
        text = paragraphs.text.strip()
        if len(text) > 50:
            return text

    return "N/A"

def scrapping(soup, course):
    page = requests.get(course["url"])
    secondSoup = BeautifulSoup(page.text, "html.parser")

    try:
        course["description"] = getDescription(secondSoup)
        course["instructor"] = get_table_value("Instructor(s):", secondSoup)
        course["meets"] = get_table_value("Meets:", secondSoup)
    except Exception as e:
        course["description"] = "N/A"
        course["instructor"] = "N/A"
        course["meets"] = "N/A"
