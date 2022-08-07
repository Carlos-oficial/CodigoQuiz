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


# {'parser_class': None,

#  'name': 'a',
#   'namespace': 'http://www.w3.org/1999/xhtml',
#   '_namespaces': {},
#   'prefix': None,
#   'sourceline': 307,
#   'sourcepos': 68,
#   'known_xml': False,
#   'attrs': {'data-lightbox': 'question',
#   'href': '/assets/images/questions/1234.jpg'},
#   'contents': ['\n',
#   <img alt="Questão IMT: Esta situação pode ser particularmente perigosa à circulação." class="question-image" src="/assets/images/questions/1234.jpg" title="Clique para ampliar a imagem"/>,
#   '\n'],
#   'parent': <div class="question-image">
# <a data-lightbox="question" href="/assets/images/questions/1234.jpg">
# <img alt="Questão IMT: Esta situação pode ser particularmente perigosa à circulação." class="question-image" src="/assets/images/questions/1234.jpg" title="Clique para ampliar a imagem"/>
# </a>
# <div class="magnify"><i class="fa fa-search-plus"></i></div>
# </div>,
#  'previous_element': '\n', 'next_element': '\n', 'next_sibling': '\n', 'previous_sibling': '\n', 'hidden': False, 'can_be_empty_element': False, 'cdata_list_attributes': {'*': ['class', 'accesskey', 'dropzone'], 'a': ['rel', 'rev'], 'link': ['rel', 'rev'], 'td': ['headers'], 'th': ['headers'], 'form': ['accept-charset'], 'object': ['archive'], 'area': ['rel'], 'icon': ['sizes'], 'iframe': ['sandbox'], 'output': ['for']}, 'preserve_whitespace_tags': {'pre', 'textarea'}, 'interesting_string_types': (<class 'bs4.element.NavigableString'>, <class 'bs4.element.CData'>)}
