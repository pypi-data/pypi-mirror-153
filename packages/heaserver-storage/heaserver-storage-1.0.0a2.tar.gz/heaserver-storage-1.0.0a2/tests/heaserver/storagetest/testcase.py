"""
Creates a test case class for use with the unittest library that is built into Python.
"""
from heaserver.service.testcase.mockmongotestcase import get_test_case_cls_default
from heaserver.storage import service
from heaobject.user import NONE_USER
from heaserver.service.testcase.expectedvalues import ActionSpec

db_store = {
    service.MONGODB_STORAGE_COLLECTION: [{
        'id': '666f6f2d6261722d71757578',
        'created': '2022-05-02',
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'standard',
        'invited': [],
        'modified': '2022-05-02',
        'name': 'standard',
        'owner': NONE_USER,
        'shares': [],
        'source': None,
        'type': 'heaobject.storage.AWSStorage',
        'arn': 'a:123456',
        'storage_bytes': 1024.00,
        'min_storage_duration': 30,
        'object_count': 10,
        'object_init_modified': '2022-05-01',
        'object_last_modified': '2022-05-02',
        'volume_id': '666f6f2d6261722d71757578'
    },
        {
            'id': '0123456789ab0123456789ab',
            'created': '2022-05-02',
            'derived_by': None,
            'derived_from': [],
            'description': None,
            'display_name': 'Glacier',
            'invited': [],
            'modified': '2022-05-02',
            'name': 'Glacier',
            'owner': NONE_USER,
            'shared_with': [],
            'source': None,
            'type': 'heaobject.storage.AWSStorage',
            'arn': 'a:123456789',
            'storage_bytes': 1024.00,
            'min_storage_duration': 30,
            'object_count': 100,
            'object_init_modified': '2022-05-01',
            'object_last_modified': '2022-05-02',
            'volume_id': '0123456789ab0123456789ab'
        }

    ],
    'filesystems': [{
        'id': '666f6f2d6261722d71757578',
        'created': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'Amazon Web Services',
        'invited': [],
        'modified': None,
        'name': 'amazon_web_services',
        'owner': NONE_USER,
        'shared_with': [],
        'source': None,
        'type': 'heaobject.volume.AWSFileSystem',
        'version': None
    }],
    'volumes': [{
        'id': '666f6f2d6261722d71757578',
        'created': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'My Amazon Web Services',
        'invited': [],
        'modified': None,
        'name': 'amazon_web_services',
        'owner': NONE_USER,
        'shared_with': [],
        'source': None,
        'type': 'heaobject.volume.Volume',
        'version': None,
        'file_system_name': 'amazon_web_services',
        'credential_id': None  # Let boto3 try to find the user's credentials.
    }]}
TestCase = get_test_case_cls_default(coll=service.MONGODB_STORAGE_COLLECTION,
                                     wstl_package=service.__package__,
                                     href='http://localhost:8080/storage/',
                                     fixtures=db_store,
                                     get_actions=[ActionSpec(name='heaserver-storage-storage-get-properties',
                                                             rel=['properties']),
                                                  ActionSpec(name='heaserver-storage-storage-open',
                                                             url='/storage/{id}/opener',
                                                             rel=['opener']),
                                                  ActionSpec(name='heaserver-storage-storage-duplicate',
                                                             url='/storage/{id}/duplicator',
                                                             rel=['duplicator'])
                                                  ],
                                     get_all_actions=[ActionSpec(name='heaserver-storage-storage-get-properties',
                                                                 rel=['properties']),
                                                      ActionSpec(name='heaserver-storage-storage-open',
                                                                 url='/storage/{id}/opener',
                                                                 rel=['opener']),
                                                      ActionSpec(name='heaserver-storage-storage-duplicate',
                                                                 url='/storage/{id}/duplicator',
                                                                 rel=['duplicator'])],
                                     duplicate_action_name='heaserver-storage-storage-duplicate-form')
