import locale, re

from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString

current_tag_match = None


def main():
    locale.setlocale(locale.LC_ALL, "en-US")
    with open("ehs_scholarship_application.html", "r+", encoding="utf-8") as scholarship_application:
        scholarship_application_soup = BeautifulSoup(scholarship_application, "html.parser")
        inputTag = scholarship_application_soup.find(match_input)
        while inputTag is not None:
            label_tag = inputTag.find_next_sibling("label", attrs={
                "for": inputTag["id"]
            })
            label_tag.clear(True)
            first_strong_tag = scholarship_application_soup.new_tag("strong")
            first_strong_tag.append(current_tag_match.group("first_strong"))
            second_strong_tag = scholarship_application_soup.new_tag("strong")
            second_strong_tag.append(current_tag_match.group("second_strong"))
            label_tag.extend([
                "For " + current_tag_match.group("article") + " ",
                first_strong_tag,
                " my monthly income is ",
                second_strong_tag
            ])

        scholarship_application.seek(0, 0)
        scholarship_application.truncate(0)
        scholarship_application.seek(0, 0)
        scholarship_application.write(str(scholarship_application_soup))


def match_input(tag: Tag):
    if tag.name.lower() != "input" or tag["type"].lower() != "radio":
        return False
    current_tag_match = re.match(r"^For (?P<article>an?) (?P<first_strong>(?P<household_size>\d+)-person household,) my monthly income is (?P<second_strong>\$(?P<max_monthly_income>\d{1,3}(?:,\d{3})*) or less.)$", tag["value"])
    return current_tag_match is not None


if __name__ == "__main__":
    main()