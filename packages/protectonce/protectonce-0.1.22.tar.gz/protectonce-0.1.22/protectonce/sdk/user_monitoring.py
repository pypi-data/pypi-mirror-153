from ..core_interface import invoke_core_method
from ..rules.handlers import cls
from ..rules.handlers import http_server

data = {
        "config": {
            "property": "__poSessionId"
        }
    }
def __get_session_id():
    return cls.get_property(data)


def report_signup(user_name):
    """input parameters user_name as string"""
    if not isinstance(user_name, str):
        print(
            "[PROTECTONCE_WARN] protectonce.report_signup: 'user_name' should be string")
        return
    try:
        po_session_id = __get_session_id().get('poSessionId', '')
        signup_data = {"data": {
            "poSessionId": po_session_id,
            "userName": user_name
        }}
        result, out_data_type, out_data_size = invoke_core_method(
            "userMonitoring.storeSignUpData", signup_data)
        print(f'Result_actions=={result}')
        result["config"] = data["config"]
        http_server.cancel_request(result)
    except Exception as e:
        print(
            f"[PROTECTONCE_WARN] protectonce.report_signup: Error occured while handling signup data : {e}")

def report_login(status, user_name):
    """input parameters status as boolean 'True' or 'False' and user_name as string"""

    if not isinstance(user_name, str) or not isinstance(status, bool):
        print(
            "[PROTECTONCE_WARN] protectonce.report_login: 'user_name' and 'status' should be boolean either 'True' or 'False'")
        return

    try:
        po_session_id = __get_session_id().get('poSessionId', '')
        login_data = {"data": {
            "poSessionId": po_session_id,
            "success": status,
            "userName": user_name
        }}
        result, out_data_type, out_data_size = invoke_core_method(
            "userMonitoring.storeLoginData", login_data)
        result["config"] = data["config"]
        http_server.cancel_request(result)
    except Exception as e:
        print(
            f"[PROTECTONCE_WARN] protectonce.report_login: Error occured while handling login data : {e}")

def report_auth(user_name, traits=None):
    """input parameters user_name as string traits is optional"""
    if not isinstance(user_name, str):
        print(
            "[PROTECTONCE_WARN] protectonce.report_auth: 'user_name' should be string")
        return
    try:
        po_session_id = __get_session_id().get('poSessionId', '')
        auth_data = {"data": {
            "poSessionId": po_session_id,
            "userName": user_name
        }}
        result, out_data_type, out_data_size = invoke_core_method(
            "userMonitoring.identify", auth_data)
        result["config"] = data["config"]
        http_server.cancel_request(result)
    except Exception as e:
        print(
            f"[PROTECTONCE_WARN] protectonce.report_auth: Error occured while handling authentication data : {e}")

def is_user_blocked(user_name, traits=None):
    """input parameters user_name as string traits is optional"""
    if not isinstance(user_name, str):
        print(
            "[PROTECTONCE_WARN] protectonce.is_user_blocked: 'user_name' should be string")
        return
    try:
        po_session_id = __get_session_id().get('poSessionId', '')
        user_data = {"data": {
            "poSessionId": po_session_id,
            "userName": user_name
        }}
        result, out_data_type, out_data_size = invoke_core_method(
            "userMonitoring.checkIfBlocked", user_data)
        result["config"] = data["config"]
        http_server.cancel_request(result)
    except Exception as e:
        print(
            f"[PROTECTONCE_WARN] protectonce.is_user_blocked: Error occured while checking is user blocked : {e}")