import math
import pandas as pd


class Helpers():
    pass


class Pagination(Helpers):

    @staticmethod
    def get_range(paginator, obj, num_of_pages=7):
        index = paginator.page_range.index(obj.number)
        print('index: ', index)
        max_index = len(paginator.page_range)
        print('max_index: ', max_index)
        num = num_of_pages / 2
        print('num of pages /2: ', num)
        if index < math.floor(num):
            print('1')
            page_range = paginator.page_range[:num_of_pages]
        elif index > max_index - math.ceil(num):
            print('2')
            page_range = paginator.page_range[max_index-num_of_pages:]
        else:
            print('3')
            page_range = paginator.page_range[index-math.floor(num):index+math.ceil(num)]
        return page_range


def main():
    pass


if __name__ == '__main__':
    main()
