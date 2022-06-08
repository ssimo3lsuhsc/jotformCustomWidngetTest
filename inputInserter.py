import locale

from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString


class HouseholdIncomeLimit:
    def __init__(self, household_size: int, max_income: int, article: str = "a"):
        self.household_size = household_size
        self.max_income = max_income
        self.article = article

def main():
    locale.setlocale(locale.LC_ALL, "en-US")
    with open("jotFormCustomWidget.html", "r+", encoding="utf-8") as customWidget:
        customWidgetSoup = BeautifulSoup(customWidget, "html.parser")
        inputTag = customWidgetSoup.find("input")
        while inputTag is not None:
            labelTag = customWidgetSoup.find("label", attrs={
                "for": inputTag["id"]
                })
            if labelTag is not None:
                labelTag.decompose()
            inputTag.decompose()
            inputTag = customWidgetSoup.find("input")
        customWidgetSoup.smooth()
        fieldset = customWidgetSoup.find("fieldset")
        if type(fieldset.contents[-1]) == NavigableString:
            fieldset.contents[-1].extract()
        fieldset.append("\r\n    ")
        input_index = 1
        for householdIncomeLimit in [
            HouseholdIncomeLimit(2, 3939),
            HouseholdIncomeLimit(3, 4866),
            HouseholdIncomeLimit(4, 5793),
            HouseholdIncomeLimit(5, 6720),
            HouseholdIncomeLimit(6, 7646),
            HouseholdIncomeLimit(7, 7820),
            HouseholdIncomeLimit(8, 7994, "an"),
            HouseholdIncomeLimit(9, 8168)
        ]:
            div = customWidgetSoup.new_tag("div");

            div.append(customWidgetSoup.new_tag("input", attrs={
                "name": "household_income",
                "id": "household_income_" + str(input_index),
                "type": "radio",
                "value": "For " + householdIncomeLimit.article + " " + str(householdIncomeLimit.household_size) + "-person household, my monthly income is $" + locale.format_string("%d", householdIncomeLimit.max_income, grouping=True, monetary=True) + " or less."
            }))
            div.append(" ")
            label = customWidgetSoup.new_tag("label", attrs={
                "for": "household_income_" + str(input_index)
            })
            label.append("For " + householdIncomeLimit.article + " ")
            first_strong = customWidgetSoup.new_tag("strong")
            first_strong.append(str(householdIncomeLimit.household_size) + "-person household,")
            label.append(first_strong)
            label.append(" my monthly income is ")
            second_strong = customWidgetSoup.new_tag("strong")
            second_strong.append(locale.format_string("$%d or less.", householdIncomeLimit.max_income, grouping=True, monetary=True))
            label.append(second_strong)
            div.append(label)
            fieldset.append(div)
            fieldset.append("\r\n    ")
            input_index += 1
        fieldset.append(customWidgetSoup.new_tag("input", attrs={
            "name": "household_income",
            "id": "household_income_" + str(input_index),
            "type": "radio",
            "value": "My monthly income exceeds these options based on my household."
        }))
        fieldset.append(" ")
        label = customWidgetSoup.new_tag("label", attrs={
            "for": "household_income_" + str(input_index)
        })
        label.append("My monthly income exceeds these options based on my household.")
        fieldset.append(label)
        customWidget.seek(0, 0)
        customWidget.truncate(0)
        customWidget.seek(0, 0)
        customWidget.write(str(customWidgetSoup))

if __name__ == "__main__":
    main()