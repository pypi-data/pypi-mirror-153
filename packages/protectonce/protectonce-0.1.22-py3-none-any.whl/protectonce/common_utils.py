
def is_action_blocked(data):
    try:
        return data['result'] and isinstance(data['result'], dict) and data['result'].get('action', '') in ['block', 'abort', 'redirect']
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] common_utils.is_action_blocked failed with error {e}')
    return False
