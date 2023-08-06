import pytest
from uuid import uuid4

from metagen.metadata import Application, LayerTemplate
from metagen.register import PandasRegister
from test.test_components import layer_template_1


# @pytest.fixture(autouse=True)
# def layer_template_1():
#     return LayerTemplate(applicationKey='app', nameInternal=f'lt1', nameDisplay='lt1')


@pytest.fixture(autouse=True)
def layer_template_2():
    return LayerTemplate(applicationKey='app', nameInternal=f'lt2', nameDisplay='lt2')


@pytest.fixture(autouse=True)
def pandas_register(layer_template_1, layer_template_2):
    register = PandasRegister()
    register.add(layer_template_1)
    register.add(layer_template_2)
    return register


def test_pandas_register_add(pandas_register, layer_template_2):
    assert pandas_register.table['element'][1]() == layer_template_2


def test_pandas_register_get_by_uuid(pandas_register, layer_template_2):
    assert pandas_register.get_by_uuid(layer_template_2.key) == layer_template_2


def test_pandas_register_get_by_hash(pandas_register, layer_template_1):
    assert pandas_register.get_by_hash(hash(layer_template_1)) == layer_template_1


def test_pandas_register_get_by_name(pandas_register, layer_template_2):
    assert pandas_register.get_by_name(layer_template_2.nameInternal) == layer_template_2


def test_pandas_register_get_by_name(pandas_register, layer_template_2):
    assert pandas_register.check_register(layer_template_2) is True
    assert pandas_register.check_register(uuid4()) is False