import math


class Helpers():
    pass


class Pagination(Helpers):

    @staticmethod
    def get_range(paginator, obj, num_of_pages=7):
        index = paginator.page_range.index(obj.number)
        max_index = len(paginator.page_range)
        num = num_of_pages / 2
        if index < math.floor(num):
            page_range = paginator.page_range[:num_of_pages]
        elif index > max_index - math.ceil(num):
            page_range = paginator.page_range[max_index-num_of_pages:]
        else:
            page_range = paginator.page_range[index-math.floor(num):index+math.ceil(num)]
        return page_range


def main():
    pass


if __name__ == '__main__':
    main()
