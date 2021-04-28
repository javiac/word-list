# coding=utf-8

import pymongo
from bson.code import Code
import datetime
from dependency_injector.wiring import inject, Provide
from src.containers import Container
from src.contexts.words.word_service import WordService


def get_all(searchText, word_service: WordService = Provide[Container.word_service]):
    return word_service.get_words(searchText)


def delete(word_id, word_service: WordService = Provide[Container.word_service]):
    return word_service.delete(word_id)


def create(word, word_service: WordService = Provide[Container.word_service]):
    return word_service.create(word)


def sort(sorting_changes, word_service: WordService = Provide[Container.word_service]):
    word_service.sort(sorting_changes)


def update(id, word, word_service: WordService = Provide[Container.word_service]):
    return word_service.update(id, word)
