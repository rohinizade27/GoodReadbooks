import requests, xmltodict, validators,re, pprint
from json import loads, dumps


class GoodreadsAPIClient:


    # initialize default values when class object get created
    def __init__(self):
        self.key = 'EtDX7jIXSlCYIpv4DLlzg'
        self.base_url = "https://www.goodreads.com/book/show/"
        self.result_dict = dict()
        self.RESPONSE_DICT_KEYS = ['title','average_rating','ratings_count',\
                                   'num_pages','image_url','publication_year','authors']

    def validate_url(self,book_url):
        """
        This methid validate the url pass by user,
        if url is not valid it will raise InvalidGoodreadsURL exception
        :rtype: none
        """
        if validators.domain(book_url):
            raise Exception("InvalidGoodreadsURL")

        if not self.base_url == book_url[:len(self.base_url)]:
            raise Exception("InvalidGoodreadsURL")

        regex = re.compile(self.base_url+'([0-9].-*)')
        if regex.findall(book_url)[0] == "":
            raise Exception('InvalidGoodreadsURL')

    def get_good_books_response(self,book_url):
        """
        Purpose of this method is to get response data from goodbooks APIs
        and convert xml reponse in dict
        :rtype: dict (conveted dict response)
        """
        b_id = book_url.split('/')[-1]
        params = {'key': self.key}
        method = 'GET'
        request_url = self.base_url + str(b_id) + '/'
        # goodreadbooks api call
        response = requests.request(method, request_url, params=params)
        if response.status_code != 200:
            raise Exception('InvalidGoodreadsURL')
        # convert xml response in dict format
        data_dict = xmltodict.parse(response.content)
        converted_response = loads(dumps(data_dict.get('GoodreadsResponse').get('book')))
        return converted_response

    def get_book_details(self,book_url: str):
        """
        This method takes book_url as argument,calls goodreadbooks api to get book information
        and return book information in dict format
        :rtype: dict
        """
        try:
            # validate url
            self.validate_url(book_url)
            # get goodreadbooks API response
            response_data = self.get_good_books_response(book_url)
            # generate dict for book information
            for key in self.RESPONSE_DICT_KEYS:
                if key == 'authors':
                    authors = response_data.get('authors').get('author')
                    if isinstance(authors, list):
                        authors_name = ""
                        for author in authors:
                            authors_name = authors_name + str(author.get('name')) + ","
                            self.result_dict['authors'] = authors_name
                    else:
                        self.result_dict['authors'] = response_data.get('authors').get('author').get('name')
                else:
                    self.result_dict.update({key:response_data.get(key)})
        except Exception:
            print("Invalid url pattern..please enter valid url..")
            return "Invalid url pattern..please enter valid url.."
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.result_dict)
        return self.result_dict


b = GoodreadsAPIClient()
b.get_book_details("https://www.goodreads.com/book/show/12067.Good_Omens")
