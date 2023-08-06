import sys, os
from .args import parseInput
from . import core

def about():
    return NotImplemented

def convert(arg_str):
    data_dict = parseInput(arg_str)

    if data_dict is None:
        return

    in_val = data_dict['val']
    if in_val == None:
        in_val = 1
    else:
        in_val = float(in_val)

    curr_from = data_dict['curr_from'].upper()
    curr_to = data_dict['curr_to'].upper()

    if "--update" in arg_str or not os.path.exists(core.FILEURL):
        # update the currency file
        print("Updating..")
        core.update_rates()
    else:
        # check if update is required
        days_since_mod = core.get_days_since_modified()
        if (days_since_mod.days > core.UPDATE_THRESHOLD):
            core.update_rates()

    rate_dict = core.parse_xml(core.FILEURL)
    try:
        out_val = core.convert(in_val, curr_from, curr_to, rate_dict)
    except KeyError:
        print(f"Unknown currency, this tool only supports the following {len(core.CURRENCY_LIST)} currencies: ")
        print(", ".join(_ for _ in core.CURRENCY_LIST))
        return

    core.pretty_print(in_val, curr_from, out_val, curr_to)

if __name__ == '__main__':
    # if running as a script, form a single string from the arguments
    arg_input = " ".join(_ for _ in sys.argv)
    convert(arg_input)
