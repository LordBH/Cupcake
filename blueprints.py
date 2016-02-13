from main.views import from_main
from reg.views import from_reg
from chats.views import from_chats


blueprints = (

    from_main,
    from_reg,
    from_chats,

)
