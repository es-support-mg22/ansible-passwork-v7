from typing import Any
from ansible.module_utils.basic import AnsibleModule
from passwork_common_v7 import (
  pw_login, 
  get_vault, 
  get_folder
  )

DOCUMENTATION = r'''
---
module: pw_folder_create

short_description: Модуль для создания папки в passwork

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
    folder_args:
        description: Аргументы папки
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

def _password_folder_create(
    api_server: str,
    access_token: str,
    refresh_token: str | None,
    master_key: str | None,
    folder_args: dict[str, Any]
):
        with pw_login(api_server,access_token,refresh_token,master_key) as pwClient:
            
            vault = folder_args.pop('vault', None)
            vault_id = get_vault(pwClient,  vault)['id']
            folder_args['vaultId'] = vault_id

            parent_folder: str | None = folder_args.pop('parent', None)
            if parent_folder is not None:
                folder_args['parentFolderId'] = get_folder(pwClient,parent_folder,vault_id,None)['id']
                
            response=pwClient.call("POST", f"/api/v1/folders", payload = folder_args)
            return response
        

def main():

    module = AnsibleModule(
        argument_spec={
            'api_server': {'required': True},
            'access_token': {'required': True, 'no_log': True},
            'refresh_token': {'required': False, 'no_log': True},
            'master_key': {'required': False, 'no_log': True},
            'folder_args': {
                'required': True,
                'type': 'raw',
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
    folder_args: dict[str, Any] = module.params['folder_args']

    result['response'] = _password_folder_create(api_server, access_token, refresh_token, master_key, folder_args)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
