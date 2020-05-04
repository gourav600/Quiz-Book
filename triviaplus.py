'''
using discord.py version 1.0.0a
'''
import discord
import asyncio
import re
import multiprocessing
import threading
import concurrent

BOT_OWNER_ROLE = 'crowd control' # change to what you need
#BOT_OWNER_ROLE_ID = "701076599595860071"
  
 

 
oot_channel_id_list = [
    "693995490139963393",
	"696874639661596734",
	"698434961870553098",
	"459842150323060736",
	"555842456084676618",
	"700413759059001404"
]


answer_pattern = re.compile(r'(not|n)?([1-4]{1})(\?)?(cnf)?(\?)?$', re.IGNORECASE)

apgscore = 2
nomarkscore = 10
markscore = 1

async def update_scores(content, answer_scores):
    global answer_pattern

    m = answer_pattern.match(content)
    if m is None:
        return False

    ind = int(m[2])-1

    if m[1] is None:
        if m[3] is None:
            if m[4] is None:
                answer_scores[ind] += nomarkscore
            else: # apg
                if m[5] is None:
                    answer_scores[ind] += apgscore
                else:
                    answer_scores[ind] += markscore

        else: # 1? ...
            answer_scores[ind] += markscore

    else: # contains not or n
        if m[3] is None:
            answer_scores[ind] -= nomarkscore
        else:
            answer_scores[ind] -= markscore

    return True

class SelfBot(discord.Client):

    def __init__(self, update_event, answer_scores):
        super().__init__()
        global oot_channel_id_list
        self.oot_channel_id_list = oot_channel_id_list
        self.update_event = update_event
        self.answer_scores = answer_scores

    async def on_ready(self):
        print("======================")
        print("Trivia Duck Self Bot")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

    # @bot.event
    # async def on_message(message):
    #    if message.content.startswith('-debug'):
    #         await message.channel.send('d')

        def is_scores_updated(message):
            if message.guild == None or \
                str(message.channel.id) not in self.oot_channel_id_list:
                return False

            content = message.content.replace(' ', '').replace("'", "")
            m = answer_pattern.match(content)
            if m is None:
                return False

            ind = int(m[2])-1

            if m[1] is None:
                if m[3] is None:
                    if m[4] is None:
                        self.answer_scores[ind] += nomarkscore
                    else: # apg
                        if m[5] is None:
                            self.answer_scores[ind] += apgscore
                        else:
                            self.answer_scores[ind] += markscore

                else: # 1? ...
                    self.answer_scores[ind] += markscore

            else: # contains not or n
                if m[3] is None:
                    self.answer_scores[ind] -= nomarkscore
                else:
                    self.answer_scores[ind] -= markscore

            return True

        while True:
            await self.wait_for('message', check=is_scores_updated)
            self.update_event.set()

class Bot(discord.Client):

    def __init__(self, answer_scores):
        super().__init__()
        self.bot_channel_id_list = []
        self.embed_msg = None
        self.embed_channel_id = None
        self.answer_scores = answer_scores

        # embed creation
        self.embed=discord.Embed(title="Quiz Crowd", description="", color=0x00ff00)
        self.embed.add_field(name="**__Answer 1__**", value="0", inline=False)
        self.embed.add_field(name="**__Answer 2__**", value="0", inline=False)
        self.embed.add_field(name="**__Answer 3__**", value="0", inline=False)
        self.embed.set_footer(text=f"", \
            icon_url=" ")
        # await self.bot.add_reaction(embed,':Trivia_King_Official_Logo:')


    async def clear_results(self):
        for i in range(len(self.answer_scores)):
            self.answer_scores[i]=0

    async def update_embeds(self):

         

        one_check = ""
        two_check = ""
        three_check = ""
        four_check = ""
        

        lst_scores = list(self.answer_scores)

        highest = max(lst_scores)
#         lowest = min(lst_scores)
        answer = lst_scores.index(highest)+1
        best=":mag:"
         

        if highest > 0:
            if answer == 1:
                one_check = ":ballot_box_with_check:"
            else:
                one_check=""
            if answer ==1:
                best=":ballot_box_with_check:"
            if answer == 2:
                two_check = ":ballot_box_with_check:"
            else:
                two_check= ""
            if answer == 2:
                best=":ballot_box_with_check:"
            if answer == 3:
                three_check = ":ballot_box_with_check:"
            else:
                three_check= ""
            if answer == 3:
                best=":ballot_box_with_check:"
            if answer == 4:
              four_check = ":ballot_box_with_check:"
            else:
                four_check=""
            if answer == 4:
                best=":ballot_box_with_check:"
                
#         if lowest < 0:
#             if answer == 1:
#                 one_check = ""
#             if answer == 2:
#                 two_check = ""
#             if answer == 3:
#                 three_check = ""            
 
        self.embed.set_field_at(0, name="**__Answer 1__**", value="**{0}**{1}".format(lst_scores[0], one_check))
        self.embed.set_field_at(1, name="**__Answer 2__**", value="**{0}**{1}".format(lst_scores[1], two_check))
        self.embed.set_field_at(2, name="**__Answer 3__**", value="**{0}**{1}".format(lst_scores[2],three_check))

        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("Trivia Duck")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

        await self.clear_results()
        await self.update_embeds()
        await self.change_presence(activity=discord.Game(name='with Quiz Crowd'))

    async def on_message(self, message):

        # if message is private
        if message.author == self.user or message.guild == None:
            return

        if message.content.lower() == ".":
            await message.delete()
            if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
                self.embed_msg = None
                await self.clear_results()
                await self.update_embeds()
                self.embed_msg = \
                    await message.channel.send('',embed=self.embed)
                await self.embed_msg.add_reaction(":white_check_mark:")
                await self.embed_msg.add_reaction(":x:")
                self.embed_channel_id = message.channel.id
            else:
                await message.channel.send("**You Don't Have permission To Use This cmd!**")
            return

        if message.content.startswith('+help'):
          if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
           embed = discord.Embed(title="Help Commands", description="**How Run Bot**", color=0x00ff00)
           embed.add_field(name="Supported Game", value="**Work For HQ SwagIQ LBS  `.`**", inline=False)
           embed.add_field(name="when Question come put command", value="** `.` is command work for support game**", inline=False)
           await message.channel.send(embed=embed)

        # process votes
        if message.channel.id == self.embed_channel_id:
            content = message.content.replace(' ', '').replace("'", "")
            updated = await update_scores(content, self.answer_scores)
            if updated:
                await self.update_embeds()

def bot_with_cyclic_update_process(update_event, answer_scores):

    def cyclic_update(bot, update_event):
        f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
        while True:
            update_event.wait()
            update_event.clear()
            f.cancel()
            f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
            #res = f.result()

    bot = Bot(answer_scores)

    upd_thread = threading.Thread(target=cyclic_update, args=(bot, update_event))
    upd_thread.start()

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start('NzAxMDU4Njg2Mzk0ODI2ODAy.Xpr_qA.P3H0LKCy8mTBH4eptzzhkfr4ybI'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('NTI5MDY1OTU1MzI2Njg5Mjgy.Xpr9bA.I2fXpENr1G7uYRxb5CCRA-vS6uY',bot=False))
    loop.run_forever()

if __name__ == '__main__':

    # running bot and selfbot in separate OS processes

    # shared event for embed update
    update_event = multiprocessing.Event()

    # shared array with answer results
    answer_scores = multiprocessing.Array(typecode_or_type='i', size_or_initializer=4)

    p_bot = multiprocessing.Process(target=bot_with_cyclic_update_process, args=(update_event, answer_scores))
    p_selfbot = multiprocessing.Process(target=selfbot_process, args=(update_event, answer_scores))

    p_bot.start()
    p_selfbot.start()

    p_bot.join()
    p_selfbot.join()
