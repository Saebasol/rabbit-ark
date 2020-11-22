import pytest

from rabbitark.rabbitark import RabbitArk


@pytest.fixture
def rabbitark(option):
    return RabbitArk(option)
