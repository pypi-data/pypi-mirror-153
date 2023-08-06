import os


def prepare_sql_data(data):
    try:
        args = data.get('args', [])
        index = data['config']['argsIndex']
        if(len(args) > index):
            sql_data = {
                'query': args[index],
                'poSessionId': data.get('result', {}).get('poSessionId', '')
            }
            return sql_data
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] rasp.prepare_sql_data failed with error : {e}')
    return {}


def prepare_mysql_data(data):
    try:
        args = data.get('args', [])
        index = data['config']['argsIndex']
        if len(args) > index:
            query = args[index]
            if len(args) > index+1:
                values = args[index+1]
                if isinstance(values, dict):
                    for key, value in values.items():
                        query = query.replace("%({0})s".format(key), value)
                if isinstance(values, (list, tuple)):
                    for value in values:
                        query = query.replace("%s", value, 1)

            sql_data = {
                'query': query,
                'poSessionId': data.get('result', {}).get('poSessionId', '')
            }
            return sql_data
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] rasp.prepare_mysql_data failed with error : {e}')
    return {}


def prepare_lfi_data(data):
    try:
        args = data.get('args', [])
        index = data['config']['argsIndex']
        if(len(args) > index + 1):
            lfi_data = {
                'mode': 'write' if 'w' in args[index + 1] else 'read',
                'path': args[index],
                'realpath': os.path.realpath(args[index]),
                'poSessionId': data.get('result', {}).get('poSessionId', '')
            }
            return lfi_data
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] rasp.prepare_lfi_data failed with error : {e}')
    return {}


def prepare_shellShock_data(data):
    try:
        args = data.get('args', [])
        index = data['config']['argsIndex']
        if(len(args) > index):
            shellShock_data = {
                'command': args[index],
                'poSessionId': data.get('result', {}).get('poSessionId', '')
            }
            return shellShock_data
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] rasp.prepare_shellShock_data failed with error : {e}')
    return {}


def prepare_SSRF_data(data):
    try:
        args = data.get('args', [])
        index = data['config']['argsIndex']
        if len(args) > index + 1:
            return {
                'url': args[index + 1],
                'poSessionId': data.get('result', {}).get('poSessionId', '')
            }
        if len(args) > index:
            return {
                'url': args[index],
                'poSessionId': data.get('result', {}).get('poSessionId', '')
            }
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] rasp.prepare_SSRF_data failed with error : {e}')
    return {}
