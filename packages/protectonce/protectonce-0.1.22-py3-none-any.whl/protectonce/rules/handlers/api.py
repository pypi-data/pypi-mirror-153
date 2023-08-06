import os


def get_flask_routes(data):
    try:
        if not data:
            return []
        args = data.get('args', [])
        index = data['config']['argsIndex']
        if(len(args) > index):
            paths = [args[index]]
            if(not paths):
                return []
            if("/static/<path:filename>" in paths):  # skipping default path set by flask
                return []
            methods = data['kwargs'].get('methods', None)
            host = os.uname()[1]
            routeData = [{'paths': paths, 'methods': ["GET"]
                          if methods is None else methods, 'host': host}]
            return routeData
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] api.get_flask_routes failed with error {e}')
        return []


def get_flask_params(data):
    try:
        flask_server = data.get('instance', None)
        po_session_id = data.get('result', {}).get('poSessionId', None)
        if(not po_session_id or not flask_server or not hasattr(flask_server, 'jinja_env') or not hasattr(flask_server.jinja_env, 'globals')):
            return {}
        request = flask_server.jinja_env.globals['request']
        return {
            'poSessionId': po_session_id,
            'requestPath': request.url_rule.rule,
            'pathParams': request.view_args
        }
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] api.get_flask_params failed with error : {e}')
        return {}


def get_django_params(data):
    try:
        args = data.get('args', [])
        index = data['config']['argsIndex']
        if(len(args) > index and hasattr(args[index], 'resolver_match') and hasattr(args[index].resolver_match, 'route')):
            return {
                'poSessionId': data.get('result', {}).get('poSessionId', ''),
                'requestPath': args[index].resolver_match.route,
                'pathParams': data.get('kwargs', None)
            }
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] api.get_django_params failed with error : {e}')
    return {}


def get_django_routes(data):
    try:
        host = os.uname()[1]
        if not data:
            return []
        args = data.get('args', [])
        index = data['config']['argsIndex']
        if(len(args) > index + 1):
            path = args[index]
            view = args[index + 1]
            if(not hasattr(view, 'view_class')):
                return [{
                    'paths': [path],
                    'methods': [
                        "GET",
                        "POST",
                        "PUT",
                        "PATCH",
                        "DELETE",
                        "HEAD",
                        "OPTIONS",
                        "TRACE",
                    ],
                    'host': host
                }]
            methods = list(set(dir(view.view_class)) & set(
                view.view_class.http_method_names))
            return [{'paths': [path], 'methods': list(map(lambda method: method.upper(), methods)), 'host': host}]
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] api.get_django_routes failed with error : {e}')
    return []

def parse_qs_plus(_dict):
	data = {}
	if(type(_dict) != dict):
		return _dict
	for k,v in _dict.items():
		if (type(v) == list):
			if (len(v) == 0):
				data[k] = []
			elif (len(v) == 1):
				data[k] = v[0]
			else:
				_list = []
				for item in v:
					_list.append(parse_qs_plus(item))
				data[k] = _list
		else:
			data[k] = v
	return data

def get_flask_formdata(data):
    try :
        flask_server = data.get('instance', None)
        po_session_id = data.get('result', {}).get('poSessionId', None)
        if(not po_session_id or not flask_server or not hasattr(flask_server, 'jinja_env') or not hasattr(flask_server.jinja_env, 'globals')):
            return {}
        request = flask_server.jinja_env.globals['request']

        d = request.__dict__
        stream = d["stream"]
       
        request._load_form_data()
        
        d["stream"] = stream
        form_data = flask_server.jinja_env.globals
        
        form_data["fields"] = parse_qs_plus(dict(d["form"].lists()))
        form_data["filesFieldNames"] = list(d["files"].keys())
        filenames = set()
        combined_size = 0
        for fstore in d["files"].values():
            fn = fstore.filename
            if fn:
                filenames.add(fn)
            cl = fstore.content_length
            if cl is not None:
                combined_size += cl
        form_data["filenames"] = list(filenames)
        form_data["combinedFileSize"] = combined_size
        return {
            'formData': form_data,
            'poSessionId': po_session_id
        }
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] get_flask_formdata failed with error : {e}')
        return {}

def get_django_formdata(data):
    try:
        po_session_id = data.get('result', {}).get('poSessionId', None)
        args = data.get('args', [])
        index = data['config']['argsIndex']
        if(len(args) > index):
            form_data = {}
            form_data['request'] = args[index]
            form_data['fields'] = args[index].POST.dict()
            form_data['filesFieldNames'] = list(args[index].FILES.keys())
            form_data['filenames'] = [v.name for v in args[index].FILES.values()]
            form_data['combinedFileSize'] = sum([v.size for v in args[index].FILES.values() if v.size is not None])        
            return {
                'formData': form_data,
                'poSessionId': po_session_id
            }
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] api.get_django_formdata failed with error : {e}')
    return {}