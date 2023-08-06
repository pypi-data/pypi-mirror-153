from .matcher import arc
from .handlers import (
    pre_handler,
    help_handler,
    bind_handler,
    assets_update_handler,
    unbind_handler,
    info_handler,
    recent_handler,
    b30_handler,
    best_handler,
    song_handler,
    random_handler,
    post_handler,
)


arc.handle()(pre_handler)
arc.handle()(help_handler)
arc.handle()(bind_handler)
arc.handle()(assets_update_handler)
arc.handle()(unbind_handler)
arc.handle()(info_handler)
arc.handle()(recent_handler)
arc.handle()(b30_handler)
arc.handle()(best_handler)
arc.handle()(song_handler)
arc.handle()(random_handler)
arc.handle()(post_handler)
