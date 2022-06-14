import re
from collections import Counter
import cv2
import numpy
import pymongo
import pytesseract
from PIL import Image
from django_filters import rest_framework as filters
from rest_framework.exceptions import APIException
from app.settings import MONGO_URI
from quotes.models import Quote


class TextDetectionError(APIException):
    status_code = 415
    default_detail = "Sorry, the text couldn't be recognized from this image. Please upload another image"


def get_text_from_picture(image_file):
    image = Image.open(image_file)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, config=custom_config, lang='hye+eng+rus')
    return text


def recognize_text(file_name):
    image = Image.open(file_name)
    open_cv_image = numpy.asarray(image)
    image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 201, 100)

    # Dilate to combine adjacent text contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # Find contours, highlight text areas, and extract ROIs
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    areas = [cv2.contourArea(c) for c in cnts if cv2.contourArea(c) > 100000]
    recognized_text_array = []
    ROI_number = 0
    for c in cnts:
        if cv2.contourArea(c) > 100000:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(image, (x, y), (x + w, y + h), (107, 0, 0), 3)
            ROI = image[y:y + h, x:x + w]
            text = pytesseract.image_to_string(ROI, lang='eng', config=r'--oem 3 --psm 6')
            filter_text = [sentence for sentence in re.sub('[^A-Za-z0-9,.]+', ' ', text).lower().strip().split('.') if
                           len(sentence) > 0]
            recognized_text_array.extend(filter_text)
            ROI_number += 1
    # cv2.imshow('thresh', thresh)
    # cv2.imshow('dilate', dilate)
    # cv2.imshow('image', image)
    # cv2.waitKey()
    return recognized_text_array


def get_text_from_book(recognized_array):
    client = pymongo.MongoClient(MONGO_URI)
    db = client.social_reading_db
    sent = db.sentence_sentence
    search_result = []
    i = 1
    for sentence in recognized_array:
        if len(sentence) > 10:
            for el in sent.find({"text": {"$regex": sentence, "$options": "-i"}}):
                book_head = '-'.join(el.get('index_name').split('-')[:2]) + "-"
                search_result.append(book_head)
                i += 1
    search_result = Counter(search_result).most_common(10)
    book_id, percent = 0, 0.0
    author, title, text = '', '', ''
    if len(search_result) == 0:
        raise TextDetectionError()
    else:
        for el in sent.find({"index_name": {"$regex": search_result[0][0], "$options": "-i"}}):
            percent = "{:.2f}".format(el.get('id') / 30733 * 100)
            t = el.get('text')
            book_id = el.get('book_id')
            if t[0].isdigit():
                text += f"<h3>{el.get('index_name')}</h3>" + '\n' + f"<p>{t}</p>" + '\n'
            else:
                header_index = re.search(r"\d", t).start() - 1
                header = f'<b>{t[:header_index]}</b>'
                t = t[header_index + 1:]
                text += f"<h1>{header}</h1>" + "\n" + f"<h3>{el.get('index_name')}</h3>" + "\n" + f"<p>{t}</p>"

        books = db.library_book.find({'id': book_id})
        for book in books:
            author = book.get('author')
            title = book.get('title')

    return text, percent, author, title


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class QuoteFilter(filters.FilterSet):
    author_id = CharFilterInFilter(field_name='author', lookup_expr='in')
    id = CharFilterInFilter(field_name='id', lookup_expr='in')
    category = CharFilterInFilter(field_name='book_category', lookup_expr='in')

    class META:
        model = Quote
        fields = ('author', 'book_category', 'id')
