import logging

from hutch_python.cache import LoadCache
from hutch_python.load_conf import default_class_namespace
from hutch_python.utils import extract_objs

logger = logging.getLogger(__name__)


def test_load_cache_integration():
    logger.debug('test_load_cache_integration')
    cache = LoadCache('fake.db')
    cache(obj1=1, obj2=2, obj3=3)
    objs = extract_objs()
    assert objs['obj1'] == 1
    assert objs['obj2'] == 2
    assert objs['obj3'] == 3
    default_class_namespace(int, 'nums', cache)
    assert cache.objs.nums.obj1 == 1
    assert cache.objs.nums.obj2 == 2
    assert cache.objs.nums.obj3 == 3


def test_load_cache_importable():
    logger.debug('test_load_cache_importable')
    cache = LoadCache('fake2.db')
    cache(one=1)

    import hutch_python.db
    assert hutch_python.db.one == 1
