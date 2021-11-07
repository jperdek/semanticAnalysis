from bs4 import BeautifulSoup


def verify_html(text):
    processed_html = BeautifulSoup(text, "html.parser")
    if processed_html.find() is None:
        return False
    else:
        return True