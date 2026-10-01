import requests
from bs4 import BeautifulSoup


def search_incruit(keyword, pages=1):
    jobs = []
    for page in range(pages):
        page = page * 30

        url = f"https://search.incruit.com/list/search.asp?col=job&kw={keyword}&startno={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        lis = soup.find_all("li", class_="c_col")

        for li in lis:
            company = li.find("a", class_="cpname").text
            title = li.find("div", class_="cell_mid").find("div", class_="cl_top").find("a").text
            location = li.find("div", class_="cl_md").find_all("span")[0].text
            link = li.find("div", class_="cell_mid").find("div", class_="cl_top").find("a").get("href")

            job_data = {
                "company": company,
                "title": title,
                "location": location,
                "link": link
            }
            jobs.append(job_data)

    return jobs

def search_jobkorea(keyword):
    jobs = []

    url = "https://www.jobkorea.co.kr/Top100/?Main_Career_Type=1&Search_Type=1&BizJobtype_Bctgr_Code=0&BizJobtype_Bctgr_Name=%EC%A7%81%EB%AC%B4+%EC%A0%84%EC%B2%B4&BizJobtype_Code=0&BizJobtype_Name=%EC%A0%84%EC%B2%B4&Major_Big_Code=0&Major_Big_Name=%EC%A0%84%EA%B3%B5+%EC%A0%84%EC%B2%B4&Major_Code=0&Major_Name=%EC%A0%84%EC%B2%B4&Edu_Level_Code=9&Edu_Level_Name=%ED%95%99%EB%A0%A5+%EC%A0%84%EC%B2%B4&Edu_Level_Name=%ED%95%99%EB%A0%A5+%EC%A0%84%EC%B2%B4&MidScroll=0&duty-depth1=on"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    keyword = keyword.strip().lower()

    links = soup.find_all("a", href=True)
    seen = set()

    for link_tag in links:
        href = link_tag.get("href", "")
        title = link_tag.get_text(" ", strip=True)

        if not title or len(title) < 3:
            continue

        if "/Recruit/GI_Read/" not in href and "GI_Read" not in href:
            continue

        if keyword and keyword not in title.lower():
            parent = link_tag.find_parent("li") or link_tag.find_parent("div")
            parent_text = parent.get_text(" ", strip=True).lower() if parent else ""
            if keyword not in parent_text:
                continue

        if href.startswith("/"):
            href = "https://www.jobkorea.co.kr" + href

        if href in seen:
            continue
        seen.add(href)

        parent = link_tag.find_parent("li") or link_tag.find_parent("div")
        text = parent.get_text(" ", strip=True) if parent else ""

        company = ""
        location = ""
        
        lines = [x.strip() for x in text.split("  ") if x.strip()]
        if lines:
            for line in lines:
                if line != title and len(line) <= 40:
                    if "지원" not in line and "마감" not in line and "정규직" not in line:
                        company = line
                        break

        regions = [
            "서울", "경기", "인천", "대전", "대구", "부산", "광주", "울산",
            "세종", "충북", "충남", "전북", "전남", "경북", "경남", "강원", "제주"
        ]
        for region in regions:
            if region in text:
                location = region
                break

        jobs.append({
            "company": company,
            "title": title,
            "location": location,
            "link": href,
            "site": "잡코리아"
        })

    return jobs[:100]
