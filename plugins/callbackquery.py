from info import filters,CHANNELS,OWNER_ID
import uuid    
import asyncio 
import time,re,os,subprocess, json,shutil
from utils import get_gdrive_link,add_link,User
from botii  import Bot0
import requests
from moviepy.editor import VideoFileClip
from plugins.database import db
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import logging
logger = logging.getLogger(__name__)

@Bot0.on_message(filters.command('logger') & filters.owner)
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))
        
@Bot0.on_message((filters.regex('^gdrove.*') | filters.regex('^https://drive.google.com/file.*')) & filters.private )
async def group62(client, message):
    azb="start"
    botusername=await client.get_me()
    nyva=botusername.username  
    nyva=str(nyva)
    group_id = await db.is_bot_exist(nyva)
    id1=int(message.id)
    if not(await db.is_gdrive_exist(message.from_user.id,group_id)):
        await message.reply_text("Samahani mpendwa nunua movie au series yoyote kutoka kwa admin mwenye robot huyu ndio tutaweza kufanyia kaz link ýako")
        return
    if message.text.startswith("https://drive.google.com/file") and " " not in message.text.strip():
        id = message.text.replace("https://drive.google.com/file/d/","").split("/")[0]
        await add_link( id+"##"+str(message.from_user.id) ,nyva)
        await message.reply_text("Tumepokea link yako tunaifanyia kazi")
        return
    elif message.text.strip() == "gdrave":
        dir = '/app/'
        for files in os.listdir(dir):
            path = os.path.join(dir, files)
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(path)
        return
    elif message.text.strip() != "gdrove":
        await message.reply_text("boss umekosea hakiki tena link hii hakisha haina nafasi katikati na hujaongeza neno lolote mbele")
        return
    dir = '/gdrive/'
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)
    
    cnt=0
    jkz=[]
    while azb=="start":  
        path="/gdrive/"
        az="dfg"
        filez=await get_gdrive_link(nyva)
        for link in filez:
            if link.id.split("##")[1] not in jkz:
                az="bz"
                user_id=int(link.id.split("##")[1])
                jkz.append(user_id)
                id=link.id.split("##")[0]
        if az=="dfg":
            jkz=[]
            await asyncio.sleep(120)
            continue
        mkv22=await client.send_message(text="downloading.... kuwa na subra tunadownload kwenye computer yangu kisha tuapload telegram ",chat_id=user_id)
        URL = "https://docs.google.com/uc?export=download&confirm=1"
        def startp(URL,id):
            session = requests.Session()
            response = session.get(URL, params={"id": id}, stream=True)
            token=None
            for key, value in response.cookies.items():
                if key.startswith("download_warning"):
                    token = value  
            if token:
                params = {"id": id, "confirm": token}
                response = session.get(URL, params=params, stream=True)
            return response
        response = startp(URL,id)
        if 'signin' in response.url:
            await User.collection.delete_one({'_id':id+"##"+str(user_id)})
            await asyncio.sleep(120)
            await mkv22.reply_text("🚫TAFADHALI kabadilishe hii link iwe iwe shared to everyone kisha itume tena kama huelew muulize @hrm45")
            continue
        try:
            header = response.headers['Content-Disposition']
        except:
            await asyncio.sleep(120)
            await User.collection.delete_one({'_id':id+"##"+str(user_id)})
            await add_link( id+"##"+str(user_id) ,nyva)
            await mkv22.delete()
            continue
        file_name = re.search(r'filename="(.*)"', header).group(1)
        file_name=file_name.replace("+255-753-129-900","")
        async def startr():
            with open(path+file_name, "wb") as f:
                total_length = response.headers.get('content-length')
                if total_length is None: # no content length header
                    f.write(response.content)
                else:
                    dl = 0
                    ab=[]
                    total_length = int(total_length)
                    for data in response.iter_content(chunk_size=4096):
                        dl += len(data)
                        f.write(data)
                        f.flush()
                        a = int(10 * dl / total_length)
                        await asyncio.sleep(1)
                        text2=f"downloading [▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️]\nName:{file_name}\nkwenye computer yangu "
                        if a not in ab:
                            ab.append(a)
                            text2=text2.replace("▫️",'▪️',a)
                            await mkv22.edit_text(text=f"{text2}")   
        await startr()
        await asyncio.sleep(1)
        try:
            clip = VideoFileClip(path+file_name)
            duration = clip.duration
            clip.save_frame("/app/frame1.jpeg",t=(int(duration))/2)
            thumb="/app/frame1.jpeg"
        except:
            duration = 0
            thumb = None
        ab=[]
        async def progress(current, total):
            text2=f"Uploading [▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️]\nName:{file_name}\nTo Telegram"
            a = int(current * 10 / total)
            if a not in ab:
                ab.append(a)
                text2=text2.replace("▫️",'▪️',a)
                await mkv22.edit_text(text=f"{text2}")
        await client.send_video(chat_id=user_id, video=open(path + file_name, 'rb'),duration=int(duration),file_name=file_name,caption=file_name,thumb=thumb,progress = progress)
        mkv22.delete()
        #await message.reply_text(f"{response}hi")
        os.remove(path+file_name)
        try:
            os.remove("/app/frame1.jpeg")
        except:
            pass
        await User.collection.delete_one({'_id':id+"##"+str(user_id)})

        await asyncio.sleep(1)
        cnt+=1
        if cnt==3:
            await asyncio.sleep(300)
