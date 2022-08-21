from bs4 import BeautifulSoup
import html5lib
from typing import Dict, List, Tuple
from requests import request


def get_soup(question_id: int):
    resp = request("GET", "https://www.bomcondutor.pt/questao/" + str(question_id))
    page = resp._content
    return BeautifulSoup(page, "html5lib")


def get_question(soup) -> str:
    question_div = soup.find("div", {"class": "question-text"})
    question_text = question_div.find("div", {"class": "text"}).contents[0]
    return question_text


def get_answers(soup) -> List[Tuple[str, str]]:
    ret = []
    answer_divs = soup.findAll("span", {"class": "answer-text"})
    for answer in answer_divs:
        ret.append((answer.previous_element, answer.next_element))
    return ret


def get_script_(soup):
    script = soup.findAll("script")
    for item in script:
        if "bcrypt" in str(item):
            return item


def get_script(id):
    replace: str = """ 
    var e = lazyLoadImage();
    var objects = document.getElementsByClassName("answer");
    for (var obj of objects) {
        console.log(obj.classList);
        if (obj.classList.contains(e)) {
            obj.classList.add("bg-blue-300");
        }
    }
    </script>      """
    return (
        str(get_script_(id))
        .split("return String.fromCharCode(e)};")[0]
        .split("<script>")[1]
    )


def get_enc_string(script, id):
    return script.split("bc" + str(id) + "(\"")[1].split('");')[0]

def get_image_link(soup):
    link = soup.find("div","question-image").contents[1].attrs['href']
    return "https://www.bomcondutor.pt" + link
if __name__ == "__main__":
    print(get_image_link(get_soup(1234)))
