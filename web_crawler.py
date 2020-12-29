import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver


class Review:
    def __init__(self, comment, date, star, good, bad):
        self.comment = comment
        self.date = date
        self.star = star
        self.good = good
        self.bad = bad

    def show(self):
        print(f"내용: {self.comment} \n날짜: {self.date} \n별점: {self.star} \n좋아요: {self.good} \n싫어요: {self.bad}")
        print("----------------------------------------------------------------")

def movie_search(movie_title):
    driver = webdriver.Edge()
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=" + movie_title
    soup = BeautifulSoup(urllib.requqest.urlopen(url).read(), "html.parser")

    movie_info = soup.find("h3", class_="movie_info section")
    title = movie_info.select("a > strong").text
    
    
    
def review_crawl(url):
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    review_list = []
    title = soup.find('h3', class_='h_movie').find("a").text

    driver = webdriver.Edge()
    driver.get(url)
    driver.switch_to.frame("pointAfterListIframe")

    page_num = 2

    while page_num < 11:
        r = driver.page_source
        soup = BeautifulSoup(r, "html.parser")
        div = soup.find("div", class_="score_result")
        data_list = div.select("ul > li")
        for review in data_list:
            star = review.find("div", class_="star_score").text.strip()
            reply = review.find("div", class_="score_reple")
            comment = reply.find("p").text.strip()
            if comment[:3] == "관람객":
                comment = comment[3:].strip()
            date = reply.select("dt > em")[1].text.strip()
            button = review.find("div", class_="btn_area")
            sympathy = button.select("strong")
            good = sympathy[0].text
            bad = sympathy[1].text
            review_list.append(Review(comment, date, star, good, bad))
            driver.find_element_by_xpath('//*[@id="pagerTagAnchor' + str(page_num) + '"]').click()
        page_num += 1


    return title, review_list


title, review_list = review_crawl("https://movie.naver.com/movie/bi/mi/point.nhn?code=36944")

print(f"제목: {title}")

for review in review_list:
    review.show()
