from logos_cdi.abstract import AbstractContextManager, AbstractContainer


class MiddlewareContextManager(AbstractContextManager):

    def __init__(self, context: AbstractContainer, config_obj: object, config_name: str):
        super().__init__(context)
        self.config_name = config_name
        self.middlewares_config = getattr(config_obj, config_name, [])
        self.context_managers = {}

    async def __aenter__(self) -> AbstractContainer:
        context = self.context
        for context_manager_service in self.middlewares_config:
            self.context_managers[context_manager_service] = context.get(context_manager_service)
            context = await self.context_managers[context_manager_service].__aenter__()
        return context

    async def __aexit__(self, *args, **kwargs):
        for context_manager in self.context_managers.values():
            await context_manager.__aexit__(*args, **kwargs)
