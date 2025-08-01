from typing import Any
from ansible.errors import AnsibleError
from ansible.module_utils.basic import AnsibleModule
from passwork_common_v7 import pw_login

DOCUMENTATION = r'''
---
module: pw_pass_get

short_description: Модуль удаления пароля в passwork

options:
    api_server:
        description: HTTP путь до API сервера https://example.ru/api/v4
        required: true
        type: str
    access_token:
        description: Access API токен
        required: true
        type: str
    refresh_token:
        description: Refresh API токен
        required: false
        type: str
    master_key:
        description: Ключ шифрования для шифрования на стороне клиента
        required: false
        type: str
    password_id:
        description: ID пароля
        required: false
        type: str
    search_args:
        description: Аргументы поиска
        required: true
        type: dict

author:
    - Ширяев Дмитрий (dshi@efsystem.ru)
'''

RETURN = r'''
response:
    description: Ответ от сервера
    type: dict
    returned: always
'''

def _delete_password(api_server:str,access_token:str,refresh_token:str,master_key:str, password_id: str
):
    with pw_login(api_server,access_token,refresh_token,master_key) as pwClient:
        
        response = pwClient.call("DELETE", f"/api/v1/items/{password_id}")
        return response

def main():

    module = AnsibleModule(
        argument_spec={
            'api_server': {'required': True},
            'access_token': {'required': True, 'no_log': True},
            'refresh_token': {'required': False, 'no_log': True},
            'master_key': {'required': False, 'no_log': True},
            'password_id': {'required': False, 'no_log': True},
            'search_args': {
                'required': False,
                'type': 'dict',
                'options': {
                    'query': {
                        'required': True,
                    },
                    'tags': {
                        'required': False,
                        'type': 'list',
                        'default': [],
                    },
                    'colors': {
                        'required': False,
                        'type': 'list',
                        'elements': 'int',
                        'default': [],
                    },
                    'vault': {
                        'required': False,
                        'default': None,
                    },
                    'includeShared': {
                        'required': False,
                        'type': 'bool',
                        'default': False,
                    },
                    'includeShortcuts': {
                        'required': False,
                        'type': 'bool',
                        'default': False,
                    },
                },

            },
        },
        supports_check_mode=True,
    )

    result = {'changed': False, 'message': ''}
    if module.check_mode:
        module.exit_json(**result)

    api_server: str = module.params['api_server']
    access_token: str = module.params['access_token']
    refresh_token: str | None = module.params['refresh_token']
    master_key: str | None = module.params['master_key']
    password_id: dict | None = module.params['password_id']
    search_args: dict[str, Any] | None = module.params['search_args']

    if not password_id and not search_args:
        raise AnsibleError('Нужно указать либо "password_id", либо "search_args"')

    if password_id:

        result['response'] =_delete_password(api_server, access_token,refresh_token, master_key, password_id)
        
    module.exit_json(**result)


if __name__ == '__main__':
    main()
