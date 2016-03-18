from threading import Thread
from reg.tools import check_online


list_of_thread = (

    Thread(target=check_online),

)
