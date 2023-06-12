import sys

from connect import connection
from models import Author, Quote


def search_quote_from_name(user_args):
    name = user_args.split('name:')[1]
    # get obj Author from name to be sure everything is correct
    author = Author.objects.get(fullname=name)
    quotes = Quote.objects(author=author)
    for quote in quotes:
        print(quote.quote)


def search_quote_from_tag(user_args):
    tag_name = user_args.split('tag:')[1]
    quotes = Quote.objects.filter(tags__contains=tag_name)
    for quote in quotes:
        print(quote.quote)


def search_quote_from_tags(user_args):
    tags_names = user_args.split('tags:')[1]
    tags_list = tags_names.split(',')
    quotes = Quote.objects.filter(tags__in=tags_list)
    for quote in quotes:
        print(quote.quote)


def handle_argument(argument):
    if argument.startswith('name:'):
        return search_quote_from_name
    elif argument.startswith('tag:'):
        return search_quote_from_tag
    elif argument.startswith('tags:'):
        return search_quote_from_tags
    elif argument == 'exit':
        sys.exit()
    else:
        print('Unknown command!')


if __name__ == '__main__':
    while True:
        user_input = input('Write a query: ')
        command = handle_argument(user_input)
        command(user_input)
