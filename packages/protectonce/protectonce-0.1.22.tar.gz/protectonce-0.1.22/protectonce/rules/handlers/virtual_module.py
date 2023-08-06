from ..types.class_rule import ClassRule


class VirtualModule(object):
    _virtual_modules = {}

    def __init__(self, rule) -> None:
        super().__init__()
        self._rule = rule
        self._interceptor = None

    @staticmethod
    def register(rule) -> None:
        intercept = rule.get('intercept', {})
        module = intercept.get('module', '')
        if not module:
            print('intercept.module is must for creation of virtual module')

        virtual_modules = VirtualModule._virtual_modules.get(module, None)
        if not virtual_modules:
            virtual_modules = []

        virtual_modules.append(VirtualModule(rule))
        VirtualModule._virtual_modules[module] = virtual_modules

    @staticmethod
    def create(data) -> None:
        try:
            config = data.get('config', {})
            virtual_modules = VirtualModule.__get_cached_module(config)

            args = data.get('args', [])
            result = data.get('result', None)
            context = VirtualModule.__get_context(config, args, result)

            if not virtual_modules or not context:
                return

            for virtual_module in virtual_modules:
                virtual_module.__add_interceptors(context)
        except Exception as e:
            print(
                f'[PROTECTONCE_ERROR] virtual_module.VirtualModule.create failed with error {e}')

    @staticmethod
    def __get_cached_module(config):
        module = config.get('virtualModule', '')
        if not module:
            return None

        return VirtualModule._virtual_modules[module]

    @staticmethod
    def __get_context(config, args, result):
        # TODO: What if context is in kwargs??
        index = config.get('moduleInstanceIndex', -1)
        if index == -1 and result:
            return result

        return args[index]

    def __add_interceptors(self, context):
        self._class_rule = ClassRule(self._rule, context)
        self._class_rule.add_instrumentation()
        pass
