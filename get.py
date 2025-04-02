import os
from pypushdeer import PushDeer
cps = os.environ["CPS"]
push_key = os.environ["PUSHDEER"]
pushdeer = PushDeer(pushkey=push_key)
pushdeer.send_text("查看", desp=cps)
