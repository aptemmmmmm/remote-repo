def filter_strings(filter_func, string_list):
    return list(filter(filter_func, string_list))
filter_condition = lambda s: s.strip() and not s.startswith('a') and len(s) >= 5
strings = [
    "hello",
    "apple",
    "banana",
    "  ",
    "world",
    "a quick brown fox",
    "Python",
    "   ",
    "cat",
    "data"
]
def get_parser(**parser_kwargs):
    parser = argparse.ArgumentParser(**parser_kwargs)
    parser.add_argument(
        '-ss',
        nargs='+',
        metavar='String',
        help = 'please enter a string array',
        default = list()
    )

filtered_strings = filter_strings(filter_condition, strings)


print(filtered_strings)
