import pytest

from metagen.metadata import Application, LayerTemplate

def test_element_duplicity():
    lt1 = LayerTemplate(applicationKey='app', nameInternal=f'lt', nameDisplay='lt')
    lt2 = LayerTemplate(applicationKey='app', nameInternal=f'lt', nameDisplay='lt')
    assert lt1.key == lt2.key



def test_stac_attribute_in_leaf():
    app = Application(name='test', nameInternal='test')
    assert hasattr(app, '_input_pars')
    assert app._input_pars == ['name', 'nameInternal']


def test_exlude_stac_attribute_from_leaf():
    app = Application(name='test', nameInternal='test')
    dict = app.dict()
    assert dict.get('_input_pars') is None


def test_to_dict():
    """testing of exluding atributes with none values except those specified as none during the inicialization"""
    lt = LayerTemplate(applicationKey=None, nameInternal='test')
    lt_dict = lt.to_dict()
    data = lt_dict.get('data')
    assert all([k in ['applicationKey', 'nameInternal'] for k in data.keys()])
    assert data.get('applicationKey') is None