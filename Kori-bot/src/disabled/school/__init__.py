from nonebot.permission import Permission
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot import on_command
# import requests
import datetime as dt
import math

school = on_command("school")

@school.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    result=""
    new_date = dt.datetime.now() #新建一个日期对象，默认现在的时间
    date0 = dt.datetime("2021-8-31 06:50:00") #设置过去的一个时间点，"yyyy-MM-dd HH:mm:ss"格式化日期
    dates = dt.datetime("2021-6-28 23:59:59")
    date1 = dt.datetime("2022-2-4 08:30:00")

    difftime0 = (date0 - new_date) #计算时间差
    difftime = difftime0/1000

    days = math.floor(difftime/86400) # 天  24*60*60*1000 
    hours = math.floor(difftime/3600)-24*days    # 小时 60*60 总小时数-过去的小时数=现在的小时数 
    minutes = math.floor(difftime%3600/60) # 分钟 -(day*24) 以60秒为一整份 取余 剩下秒数 秒数/60 就是分钟数
    seconds = math.floor(difftime%60)  # 以60秒为一整份 取余 剩下秒数

    # #  length = math.floor(Math.log10(date0 - new_date))+1
    # # ms = difftime0%(10**(length-1))
    # # total_s = (date0-dates)/1000

    max=64

    if (new_date<date0):

        pct=format((100-(difftime0/(date0-dates)*100)), '.3f')

        result=("距离开学(2021-9-1 06:50)还有 "+days+"天"+hours+"小时"+minutes+"分钟"+seconds+"秒 (即"+difftime+"秒) !\n")

        #+"["+"█"*(difftime/dates*10)+"░"*(10-(difftime/dates*10))+"]"
        # for i in range(max-math.floor(difftime0/(date0-dates))*max+1):
        #     result += "l"
        #     # result=result_
        
        # for i in range(((math.floor(difftime0/(date0-dates)*max))+1)):
        #     result+='.'
        #     # result=result_
        

        result+="假期已经过去了 "
        result+=(str(pct)+"%")
    else:
        pass
        # difftime*=-1
        # difftime0*=-1
        # days*=-1
        # hours*=-1
        # minutes*=-1
        # seconds*=-1
        # pct=(100-(difftime0/(date1-date0)*100)).toFixed(3)
        
        # result=("已经开学了 **`"+days+"`天`"+hours+"`小时`"+minutes+"`分钟`"+seconds+"`秒**  (即**`"+(difftime.toLocaleString())+"`秒**) !\n[**")
        
    #     for i in range((25-math.floor(difftime0/(date1-date0))*25)+1):
    #         result += "="
    #         # result=result_
        
    #     for i in range((math.floor(difftime0/(date1-date0)*25))+1):
    #         result+="   "
    
    
    # result+=(str(pct)+"%")
    
    