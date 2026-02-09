from dishka import make_async_container, Provider

from .providers import (
    db,
    config,
)
from .providers.domains import (
    admin_manages_products,
    admin_manages_purchase_tokens,
    customer_buys_products,
    common,
)

def setup_di():
    root_provider = Provider()

    for p in [
        db,
        config,
        admin_manages_purchase_tokens,
        admin_manages_products,
        customer_buys_products,
        common,
    ]:
        p.setup_provider(root_provider)

    return make_async_container(root_provider)
