import traceback


def set_property_to_instance(data):
    setattr(data['instance'], data['config']['property'], data['result'])

def map_stack_trace(stack_frame):
    return {
        'fileName': stack_frame.filename,
        'functionName': stack_frame.name,
        'lineNumber': stack_frame.lineno
    }

def get_stack_trace(data):
    try: 
        result = data.get('result', {})
        events = result.get('events', None)
        if isinstance(events, list):
            if result.get('shouldCollectStacktrace', None):
                stack_trace = traceback.extract_stack().copy()
                filtered_stack_trace = list(filter(lambda stack_frame: 'protectonce' not in stack_frame.filename, stack_trace))
                mapped_stack_trace = list(map(map_stack_trace, filtered_stack_trace))
                for event in events:
                    event['stackTrace'] = mapped_stack_trace
            return events
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] basic.get_stack_trace failed with error : {e}')
    
    return []