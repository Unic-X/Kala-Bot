import aioschedule as schedule,asyncio
from discord.ext import commands
import time

async def job_that_executes_once():
    # Do some work that only needs to happen once...
    return schedule.CancelJob
async def send_message(ctx,content):
    try:
        ctx.author.send(f"You had a remainder set of {content}")
    except:
        ctx.send(f"You had a remainder set of {content} ")

class Schedule(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    async def sc(self,ctx,time,repeat="False",*,message):
        if repeat.lower()=="false":
            schedule.every().at(time).do(job_that_executes_once)
        elif repeat.lower()=="true":
            schedule.every(time).at(time).do(message)

schedule.every().day.at('20:22').do(job_that_executes_once)


async def job(message='stuff', n=1):
    print("Asynchronous invocation (%s) of I'm working on:" % n, message)
    asyncio.sleep(1)

for i in range(1,3):
    schedule.every(1).seconds.do(job, n=i)
schedule.every(5).to(10).days.do(job)
schedule.every().hour.do(job, message='things')
schedule.every().day.at("10:30").do(job)
loop = asyncio.get_event_loop()
while True:
    loop.run_until_complete(schedule.run_pending())
    time.sleep(0.1)