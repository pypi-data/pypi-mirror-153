import re

def parseInput(input_string):
    input_string = input_string.lower()
    regexp = r"(\d+(.\d+)?\s+)?([a-z]{3})\s+((to|-)\s+)?([a-z]{3})"
    matches = re.search(regexp, input_string)
    if matches is not None:
        parse_dict = { 'val': matches[1], \
                'curr_from': matches[3], \
                'curr_to': matches[6] }
        return parse_dict
    else:
        print("Unable to parse input")

if __name__ == '__main__':
    parseInput("100.67 EUR to INR")
    parseInput("EUR to USD")
