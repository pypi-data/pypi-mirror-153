from typing import Dict

from openmodule.config import settings
from openmodule.core import init_openmodule, shutdown_openmodule, OpenModuleCore
from openmodule_test.health import HealthTestMixin


class OpenModuleCoreTestMixin(HealthTestMixin):
    """
    Mixin which creates a core, zmq, and health mixin
    """

    init_kwargs: Dict = {}
    core: OpenModuleCore

    def get_init_kwargs(self):
        return self.init_kwargs

    def setUp(self):
        super().setUp()
        self.init_kwargs.setdefault("sentry", False)
        self.init_kwargs.setdefault("dsgvo", False)
        self.core = init_openmodule(
            config=self.zmq_config(),
            context=self.zmq_context(),
            **self.get_init_kwargs()
        )
        self.addCleanup(shutdown_openmodule)
        self.zmq_client.subscribe(b"healthz")
        self.wait_for_health(self.core.config.NAME)
