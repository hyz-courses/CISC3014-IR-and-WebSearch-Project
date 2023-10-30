import re

# local imports
import __stock_terms__


# Turns quote info keys-value pairs
def resolve_quote_info_data(quote_info, language, use_exact_value=True, round_level=3):
    quote_info_data = {}
    for td in quote_info:
        # Item title: e.g. Highest price of today
        item_title = td.xpath("./text()").get()
        item_title = re.sub(r'[：,\s]', '', item_title)  # Remove useless symbols
        if language == "EN" and item_title in __stock_terms__.terms:    # Translate
            item_title = __stock_terms__.terms[item_title]

        # Item data: e.g. 25 billion
        data = td.xpath(".//span/text()").get()
        if use_exact_value:
            data = string_to_numeric(data, round_level)
        quote_info_data[item_title] = data

    return quote_info_data


# Enter a number string, output a number.
# E.g. If this string is "100万", then the result should be 1,000,000
def string_to_numeric(numstr, round_level):
    # Possible units: 万，亿，万亿，% (Percentage)
    pattern = r'(\d+(\.\d+)?)(万|亿|万亿|\%)?'  # Matching rules
    match = re.search(pattern, numstr)

    if match:
        # Number part
        number = float(match.group(1))
        # Unit part
        unit = match.group(3)
        if unit in __stock_terms__.units_CN:
            number *= __stock_terms__.units_CN[unit]

        # Keep the hundredth digit
        return round(number, round_level)
    else:
        return None


