import json
import os
import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://cs.brown.edu"
MAIN_URL = f"{BASE_URL}/courses/"
OUTPUT_PATH = "data/courses.json"

def get_main_courses():
    response = requests.get(MAIN_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    courses = []

    for row in soup.find_all("tr"):
        col = row.find_all("td")
        if len(col) < 2:
            continue
        course_code = col[0]
        title_cell = col[1]
        linkToCoursePage = course_code.find("a")

        if not linkToCoursePage or "href" not in linkToCoursePage.attrs:
            continue

        relative_url = linkToCoursePage["href"]
        if not relative_url.startswith("/courses/info/"):
            continue  # Skip unrelated or broken links

        courseHM = {
            "course code": course_code.text.strip(),
            "title" : title_cell.text.strip(),
            "url": BASE_URL + relative_url
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

def scrapping(course):
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

    return course

def savingCoursesJson(courses, path = OUTPUT_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as file:
        json.dump(courses, file, indent=2)
        print("saved " + len(courses) + " courses")
        

if __name__ == "__main__":
    print("🚀 Starting scrape...")
    raw_courses = get_main_courses()
    all_courses = []

    for i, course in enumerate(raw_courses):
        print(f"🔍 Scraping ({i+1}/{len(raw_courses)}): {course['course code']} - {course['title']}")
        detailed = scrapping(course)
        all_courses.append(detailed)
        time.sleep(0.5)  # polite delay

    print(f"✅ Saved {len(course)} courses to {OUTPUT_PATH}")


    savingCoursesJson(all_courses)