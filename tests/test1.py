import allure
from hamcrest import *
import requests
import pytest
import socket as s

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher


@pytest.yield_fixture
def socket():
    _socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    yield _socket
    _socket.close()


@pytest.fixture(scope='module')
def Server():
    class Dummy:
        host_port = 'localhost', 8081
        uri = 'http://%s:%s/' % host_port

    return Dummy


def test_server_connect(socket, Server):
    socket.connect(Server.host_port)
    assert socket


def test_dict():
    assert dict(foo='bar', baz=None).items() == dict(foo='bar', baz=None).items()


SOCKET_ERROR = s.error


def test_server_connect_two(socket, Server):
    assert_that(calling(socket.connect).with_args(Server.host_port), is_not(raises(SOCKET_ERROR)))


def has_content(item):
    return has_property('text', item if isinstance(item, BaseMatcher) else contains_string(item))


def has_status(status):
    return has_property('status_code', equal_to(status))


def test_server_response(Server):
    assert_that(requests.get(Server.uri), all_of(has_content('text not found'), has_status(501)))


def test_server_request(Server):
    text = 'Hello word!'
    assert_that(requests.get(Server.uri, params={'text': text}), all_of(
        has_status(200)
    ))


reverse_words = lambda words: [word[::-1] for word in words]


class BaseModifyMatcher(BaseMatcher):
    def __init__(self, item_matcher):
        self.item_matcher = item_matcher

    def _matches(self, item):
        if isinstance(item, self.instance) and item:
            self.new_item = self.modify(item)
            return self.item_matcher.matches(self.new_item)
        else:
            return False

    def describe_mismatch(self, item, mismatch_description):
        if isinstance(item, self.instance) and item:
            self.item_matcher.describe_mismatch(self.new_item, mismatch_description)
        else:
            mismatch_description.append_text('not %s, was: ' % self.instance) \
                .append_text(repr(item))

    def describe_to(self, description):
        description.append_text(self.description) \
            .append_text(' ') \
            .append_description_of(self.item_matcher)


import json as j

def is_json(item_match):
    """
    Example:
        >>> from hamcrest import *
        >>> is_json(has_entries('foo', contains('bar'))).matches('{"foo": ["bar"]}')
        True
    """
    class AsJson(BaseModifyMatcher):
        description = 'json with'
        modify = lambda _, item: j.loads(item)

    return AsJson(wrap_matcher(item_match))


@pytest.mark.parametrize('text', ['Hello word!', ' 440 005 ', 'one_word'])
def test_server_request(text, Server):
    assert_that(requests.get(Server.uri, params={'text': text}), all_of(
        has_status(200)
    ))


@pytest.mark.acceptance
def test_server_connect(socket, Server):
    assert_that(calling(socket.connect).with_args(Server.host_port), is_not(raises(SOCKET_ERROR)))


@pytest.mark.acceptance
def test_server_response(Server):
    assert_that(requests.get(Server.uri), all_of(has_content('text not found'), has_status(501)))


@allure.testcase('TESTCASE-1')
@pytest.mark.P1
def test_server_404(Server):
    assert_that(requests.get(Server.uri + 'not_found'), has_status(404))


@allure.step('some operation')
@pytest.mark.P2
def test_server_simple_request(Server):
    allure.attach('my attach', 'Hello, World')
    assert_that(requests.get(Server.uri + '?text=asdf'), has_content('fdsa'))


def pytest_configure(config):
    allure.environment(report='Allure report', browser=u'Я.Браузер')


@pytest.fixture(scope="session")
def app_host_name():
    host_name = "my.host.local"
    allure.environment(hostname=host_name)
    return host_name

