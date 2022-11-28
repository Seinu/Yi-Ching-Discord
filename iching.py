
import requests
import random
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord import File
from PIL import Image
import time
from discord.ui import Button, View
import json
import asyncio
import sqlite3
import cv2
from gtts import gTTS
import subprocess
import os, wave

import numpy as np

cnt = 0
def cleanup():
    os.system("rm output.mp4")
    os.system("rm 1.mp3")
    os.system("rm 2.mp3")
    os.system("rm 1.ts")
    os.system("rm 2.ts")

def mk_coin_image(l):
    image0 = Image.open('img/coin0.gif')
    image1 = Image.open('img/coin1.gif')
    image0_size = image0.size
    image1_size = image1.size
    new_image = Image.new('RGBA',(3*image1_size[0], image1_size[1]), (255,255,255, 0))
   

    if(l[0] == 0):
        new_image.paste(image0,(0,0))
    if(l[0] == 1):
        new_image.paste(image1,(0,0))
    if(l[1] == 0):
        new_image.paste(image0,(image1_size[0],0))
    if(l[1] == 1):
        new_image.paste(image1,(image1_size[0],0))
    if(l[2] == 0):
        new_image.paste(image0,((image1_size[0]*2),0))
    if(l[2] == 1):
        new_image.paste(image1,((image1_size[0]*2),0))

    #rgba = new_image.convert("RGBA")

    #datas = rgba.getdata()
    #newData = []
    #for item in datas:
    #    if item[0] == 255 and item[1] == 255 and item[2] == 255:
    #        newData.append((255, 255, 255, 0))
    #    else:
    #        newData.append(item)
    #    rgba.putdata(newData)
    new_image.save("tmp/row.gif","gif", transparency=0)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_read():
    global id
    con = sqlite3.connect('iching.db')
    con.row_factory = dict_factory
    cur = con.cursor()
    res = cur.execute('SELECT * FROM iching WHERE id = ' + str(id))

    dct = res.fetchone()
    print(dct['name']+"\nThe Judgement of "+dct['name']+" is " +dct['judgement']+"\nThe Image of "+dct['name']+" is " +dct['image']+"")

    return dct['name']+"\nThe Judgement of hexagram "+str(id)+" "+dct['name']+" is " +dct['judgement']+"\nThe image of hexagram "+str(id)+" "+dct['name']+" is " +dct['image']+""

def coin_flip():
    c_list = []
    for _ in range(3):
        k = random.randint(0, 1) # decide on a k each time the loop runs
        c_list.append(k)
    print(c_list)
    return c_list
    
def yarrow_calc():
    c_list = random.randrange(6, 10)
    #for _ in range(3):
    #    k = random.randint(0, 1) # decide on a k each time the loop runs
    #    c_list.append(k)
    print(c_list)
    return c_list

def line(lst):
    heads = 0
    tails = 0
    s = ''
 
    for x in range(len(lst)):
        if(lst[x] == 0):
            heads += 1
        if(lst[x] == 1):
            tails += 1

    if(heads == 2 and tails == 1):
        s = "lesser yang"
    if(heads == 1 and tails == 2):
        s = "lesser yin"
    if(heads == 0 and tails == 3):
        s = "greater yang"
    if(heads == 3 and tails == 0):
        s = "greater yin"

    return s

def yarrow_line(lst):
    heads = 0
    tails = 0
    s = ''
 
    #for x in range(len(lst)):
    #    if(lst[x] == 0):
    #        heads += 1
    #    if(lst[x] == 1):
    #        tails += 1

    if(lst == 7):
        s = "lesser yang"
    if(lst == 8):
        s = "lesser yin"
    if(lst == 9):
        s = "greater yang"
    if(lst == 6):
        s = "greater yin"

    return s

intents = discord.Intents.all() # or .all() if you ticked all, that is easier
intents.members = True # If you ticked the SERVER MEMBERS INTENT

bot = commands.Bot(command_prefix = '!', intents=intents)

id = 0

def gen_hexagram(lst):
    l = []
    for x in range(len(lst)):
        if(lst[x] == "lesser yang" or lst[x] == "greater yang"):
            print("yang")
            l.append(1)
        if(lst[x] == "lesser yin" or lst[x] == "greater yin"):

            print("yin")
            l.append(0)

    print(l)
    global id
    if l == [1,1,1,1,1,1]:
        id = 1
    if l == [0,0,0,0,0,0]:
        id = 2
    if l == [1,0,0,0,1,0]:
        id = 3
    if l == [0,1,0,0,0,1]:
        id = 4
    if l == [1,1,1,0,1,0]:
        id = 5
    if l == [0,1,0,1,1,1]:
        id = 6
    if l == [0,1,0,0,0,0]:
        id = 7
    if l == [0,0,0,0,1,0]:
        id = 8
    if l == [1,1,1,0,1,1]:
        id = 9
    if l == [1,1,0,1,1,1]:
        id=10
    if l == [1,1,1,0,0,0]:
        id = 11
    if l == [0,0,0,1,1,1]:
        id = 12
    if l == [1,0,1,1,1,1]:
        id = 13
    if l == [1,1,1,1,0,1]:
        id = 14
    if l == [0,0,1,0,0,0]:
        id = 15
    if l == [0,0,0,1,0,0]:
        id = 16
    if l == [1,0,0,1,1,0]:
        id = 17
    if l == [0,1,1,0,0,1]:
        id = 18
    if l == [1,1,0,0,0,0]:
        id = 19
    if l == [0,0,0,0,1,1]:
        id = 20
    if l == [1,0,0,1,0,1]:
        id = 21
    if l == [1,0,1,0,0,1]:
        id = 22
    if l == [0,0,0,0,0,1]:
        id = 23
    if l == [1,0,0,0,0,0]:
        id = 24
    if l == [1,0,0,1,1,1]:
        id = 25
    if l == [1,1,1,0,0,1]:
        id = 26
    if l == [1,0,0,0,0,1]:
        id = 27
    if l == [0,1,1,1,1,0]:
        id = 28
    if l == [0,1,0,0,1,0]:
        id = 29
    if l == [1,0,1,1,0,1]:
        id = 30
    if l == [0,0,1,1,1,0]:
        id = 31
    if l == [0,1,1,1,0,0]:
        id == 32
    if l == [0,0,1,1,1,1]:
        id = 33
    if l == [1,1,1,1,0,0]:
        id = 34
    if l == [0,0,0,1,0,1]:
        id = 35
    if l == [1,0,1,0,0,0]:
        id = 36
    if l == [1,0,1,0,1,1]:
        id = 37
    if l == [1,1,0,1,0,1]:
        id = 38
    if l == [0,0,1,0,1,0]:
        id = 39
    if l == [0,1,0,1,0,0]:
        id = 40
    if l == [1,1,0,0,0,1]:
        id = 41
    if l == [1,0,0,0,1,1]:
        id = 42
    if l == [1,1,1,1,1,0]:
        id = 43
    if l == [0,1,1,1,1,1]:
        id = 44
    if l == [0,0,0,1,1,0]:
        id = 45
    if l == [0,1,1,0,0,0]:
        id = 46
    if l == [0,1,0,1,1,0]:
        id = 47
    if l == [0,1,1,0,1,0]:
        id = 48
    if l == [1,0,1,1,1,0]:
        id = 49
    if l == [0,1,1,1,0,1]:
        id = 50
    if l == [1,0,0,1,0,0]:
        id = 51
    if l == [0,0,1,0,0,1]:
        id = 52
    if l == [0,0,1,0,1,1]:
        id = 53
    if l == [1,1,0,1,0,0]:
        id = 54
    if l == [1,0,1,1,0,0]:
        id = 55
    if l == [0,0,1,1,0,1]:
        id = 56
    if l == [0,1,1,0,1,1]:
        id = 57
    if l == [1,1,0,1,1,0]:
        id = 58
    if l == [0,1,0,0,1,1]:
        id = 59
    if l == [1,1,0,0,1,0]:
        id = 60
    if l == [1,1,0,0,1,1]:
        id = 61
    if l == [0,0,1,1,0,0]:
        id = 62
    if l == [1,0,1,0,1,0]:
        id = 63
    if l == [1,0,1,0,1,0]:
        id = 64
    print("id is " + str(id))


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def purge(ctx, limit: int):
    await ctx.channel.purge(limit=limit)
    await ctx.message.delete()

#bot listeners and commands
@bot.command()
async def iching(ctx):
    global cnt
    cnt = 0
    hexagram_lst = []
    lst = coin_flip()
    mk_coin_image(lst)
    hexagram_lst.append(line(lst))
    button = Button(label="Flip Coins again", style=discord.ButtonStyle.green)

    async def button_callback(interaction):

        global id
        global cnt
        lst = coin_flip()
        mk_coin_image(lst)
        hexagram_lst.append(line(lst))
        #await ctx.channel.purge(limit=limit)
        #await ctx.message.delete()
        if(cnt < 5):
           await interaction.response.send_message('```' + line(lst) + '```',file=discord.File('tmp/row.gif'), view=view)
        else:
            #yang = _ _ _
            #yin =  _   _
            await interaction.response.send_message('```' + line(lst) + '```',file=discord.File('tmp/row.gif'))
            print(hexagram_lst)
            gen_hexagram(hexagram_lst)
            print(get_read())
            await purge(ctx,6)
            await ctx.send("",file=discord.File('img/highres/'+str(id)+'.png'))
            await ctx.send(get_read())

        cnt += 1

    button.callback = button_callback

    view = View()
    view.add_item(button)

        
    await ctx.send('```' + line(lst) + '```',file=discord.File('tmp/row.gif'), view=view)
    cnt += 1

#bot listeners and commands
@bot.command()
async def yarrow(ctx):
    global cnt
    cnt = 0
    hexagram_lst = []
    lst = yarrow_calc()

    hexagram_lst.append(yarrow_line(lst))
    button = Button(label="Collect Yarrow Sticks", style=discord.ButtonStyle.green)

    async def button_callback(interaction):

        global id
        global cnt
        lst = yarrow_calc()
        hexagram_lst.append(yarrow_line(lst))
        #await ctx.channel.purge(limit=limit)
        #await ctx.message.delete()
        if(cnt < 5):
           await interaction.response.send_message('```' + str(yarrow_line(lst)) + "\n" + str(lst) + ' Yarrow Sticks leftover.```', view=view)
        else:
            #yang = _ _ _
            #yin =  _   _
            await interaction.response.send_message('```' + str(yarrow_line(lst)) + "\n" + str(lst) + ' Yarrow Sticks leftover.```')
            print(hexagram_lst)
            gen_hexagram(hexagram_lst)
            print(get_read())
            await purge(ctx,6)
            await ctx.send("",file=discord.File('img/highres/'+str(id)+'.png'))
            await ctx.send(get_read())

        cnt += 1

    button.callback = button_callback

    view = View()
    view.add_item(button)

        
    await ctx.send('```' + str(yarrow_line(lst)) + "\n" + str(lst) + ' Yarrow Sticks leftover.```', view=view)
    cnt += 1

@bot.command()
async def yiching(ctx):
    cnt = 0
    global id
    hexagram_lst = []
    lst = yarrow_calc()

    hexagram_lst.append(yarrow_line(lst))
    for x in range(5):
        global id
        lst = yarrow_calc()
        hexagram_lst.append(yarrow_line(lst))
        print(hexagram_lst)
        gen_hexagram(hexagram_lst)

    print(get_read())
    cleanup()
    tts = gTTS("Welcome to Yi Ching, today we will ask the yi ching about the future...  ", lang='en')
    tts.save("1.mp3")
    #subprocess.run(["ffmpeg", "-i", "", "-i","1.mp3", "-shortist", "-vcodec", "libx264", "1.mp4"])
    subprocess.run(["ffmpeg","-ignore_loop", "0", "-i", "./video/intro.gif", "-i", "1.mp3","-map", "0:v:0?", "-map", "1:a:0", "-r", "12.5","-shortest", "1.ts"])
    tts = gTTS("Your reading is hexagram " +str(id)+ " " + get_read())
    tts.save("2.mp3")
    # idle_index = 0
    # file_name = "response.wav"
    # f = wave.open(file_name, 'rb')
    # params = f.getparams()
    # nchannels, sampwidth, framerate, nframes = params[:4]
    # str_data  = f.readframes(nframes)  
    # f.close()  
    # wave_data = np.frombuffer(str_data, dtype = np.short)  
    # wave_data.shape = -1,2  
    # wave_data = wave_data.T  

    # N = 30 # num of bars
    # num = nframes

    # the_switch = False

    # resolution = (100, 100)
    # codec = cv2.VideoWriter_fourcc(*'mp4v') 
    # filename = "movie.mp4"

    # out = cv2.VideoWriter(filename, codec, 12.5, resolution)
    # out.write('img/highres/'+str(id)+'.gif')

    print(["ffmpeg", "loop", "1", "-i", "/img/highres/"+str(id)+".png", "-i", "response.mp3","-map", "0:v:0?", "-map", "1:a:0", "-r", "12.5", "-vcodec", "libx264", "output.mp4"])
    
    #subprocess.run(["ffmpeg", "-loop", "1", "-y", "-i", "./img/highres/"+str(id)+".png", "-i","response.mp3", "-shortist", "-vcodec", "libx264", "2.mp4"])
    subprocess.run(["ffmpeg", "-loop", "1", "-y", "-i", "./img/highres/"+str(id)+".png", "-i", "2.mp3","-map", "0:v:0?", "-map", "1:a:0", "-r", "12.5","-shortest", "2.ts"])
    
    #subprocess.run(["mp4box", "-cat", "1.mp4", "-cat", "2.mp4", "output.mp4"])
    subprocess.run(["ffmpeg", "-i", "concat:1.ts|2.ts", "-c", "copy", "-vcodec", "libx264", "output.mp4"])
    #ffmpeg -f concat -safe 0 -i mylist.txt -c copy output.mp4
    
    await ctx.channel.send(file=discord.File('./output.mp4'))


bot.run('Discord Bot Token')