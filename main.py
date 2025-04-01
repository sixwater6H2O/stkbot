from pypushdeer import PushDeer
import os
import time
push_key = os.environ["PUSHDEER"]
pushdeer = PushDeer(pushkey=push_key)

##测试存活时间
i = 10
while (i):
    msg = "倒计时：" + str(i)
    pushdeer.send_text("倒计时", desp=msg)
    i-=1
    time.sleep(60)
    
# pushdeer.send_markdown("# hello world", desp="**optional** description in markdown")
# pushdeer.send_image("https://github.com/easychen/pushdeer/raw/main/doc/image/clipcode.png")
# pushdeer.send_image(
#     "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVQYV2NgYAAAAAMAAWgmWQ0AAAAASUVORK5CYII=")
