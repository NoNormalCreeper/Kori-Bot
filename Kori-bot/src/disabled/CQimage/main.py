
from os import path
import nonebot
import config

if __name__ == '__main__':
    
    nonebot.init(config)

    ######################
    #导入本插件
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'image'),
        'image'
    )
    ######################
    
    nonebot.run()

