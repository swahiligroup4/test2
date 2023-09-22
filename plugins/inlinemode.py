from botii import Bot0
import re
import ast 
from plugins.database import db
from pyrogram.types import (
    InlineQuery,
    CallbackQuery,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineKeyboardButton,
    InlineQueryResultPhoto,
    InlineQueryResultCachedDocument
)
from utils import is_user_exist,get_search_results,Media,is_subscribed
from info import filters,OWNER_ID,CHANNELS
@Bot0.on_inline_query(filters.inline)
async def give_filter(client, query):
    botusername=await client.get_me()
    nyva=botusername.username
    group_id= await db.is_bot_exist(nyva)
    hjkl = f'{group_id}##{query.from_user.id}'  
    userdetails1= await is_user_exist(hjkl,nyva)
    text = query.query.strip()
    db_sts =await db.get_db_status(group_id)
    ban = await db.get_ban_status(group_id) 
    gd1 = db_sts['user_link']
    offset = int(query.offset or 0)
    documents, next_offset = await get_search_results(text,
                                              group_id = group_id,
                                              max_results=10,
                                              offset=offset)
    results = []
    
    for document in documents:
        id3 = document.id
        reply_text = document.reply
        button = document.btn
        alert = document.price
        file_status = document.grp
        fileid = document.file
        keyword = document.text.split('.dd#.',1)[0]
        msg_type = document.type
        descp = document.descp.split('.dd#.')[1]
        acs = document.descp.split('.dd#.')[0]
        if button =="[]":
            reply_markup = None
        else:
            reply_markup = InlineKeyboardMarkup(eval(button))
        if reply_text:
            reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")
        if acs == 'x':  
            if fileid == 'None':
                try:
                   
                    result = InlineQueryResultArticle(
                        title=keyword.upper(),
                        input_message_content=InputTextMessageContent(message_text = reply_text, disable_web_page_preview = True,
                            ),
                        description=descp,
                        reply_markup = reply_markup
                    )
                except:
                    continue
            elif msg_type == 'Photo' and not(file_status.startswith('normal')):
                try:
                    result = InlineQueryResultPhoto(
                        photo_url = fileid,
                        title = keyword.upper(),
                        description = descp,
                        caption = reply_text+'\nBonyeza **DOWNLOAD** kuipakua',
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('📤 Download', url=f"https://t.me/{nyva}?start=subinps_-_-_-_{id3}")]])if group_id != query.from_user.id else InlineKeyboardMarkup([[InlineKeyboardButton('📤 Download', url=f"https://t.me/{nyva}?start=subinps_-_-_-_{id3}")],[InlineKeyboardButton(' Edit', url=f"https://t.me/{nyva}?start=xsubinps_-_-_-_{id3}")]])
                    )
                except:
                    continue
            elif msg_type == 'Photo':
                try:
                    result = InlineQueryResultPhoto(
                        photo_url= fileid,
                        title = keyword.upper(),
                        description = descp,
                        caption = reply_text or '',
                        reply_markup=reply_markup
                    )
                except:
                    continue
            elif fileid and not(file_status.startswith('normal')) :
                try:
                    result = InlineQueryResultCachedDocument(
                        document_file_id = fileid,
                        title = keyword.upper(),
                        description = descp,
                        caption = reply_text+'\nBonyeza **DOWNLOAD** kuipakua' or "",          
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('📤 Download', url=f"https://t.me/{nyva}?start=subinps_-_-_-_{id3}")]])if group_id != query.from_user.id else InlineKeyboardMarkup([[InlineKeyboardButton('📤 Download', url=f"https://t.me/{nyva}?start=subinps_-_-_-_{id3}")],[InlineKeyboardButton(' Edit', url=f"https://t.me/{nyva}?start=xsubinps_-_-_-_{id3}")]])
                    )
                except:
                    continue
            elif fileid:
                try:
                    result = InlineQueryResultCachedDocument(
                        document_file_id = fileid,
                        title = keyword.upper(),
                        description = descp,
                        caption = reply_text or "",
                        
                        reply_markup=reply_markup
                    )
                except:
                    continue
            else:
                continue

            results.append(result) 
    if len(results) != 0:
        switch_pm_text = f"Total {len(results)} Matches"
    else:
        switch_pm_text = "No matches"
    if next_offset == '':
        title =f"Mpendwa {query.from_user.first_name}"
        results.append(InlineQueryResultArticle(
            title=title,
            input_message_content=InputTextMessageContent(message_text = f"Mpendwa [{query. from_user.first_name}](tg://user?id={query.from_user.id})\nKama movie yako haipo ntumie Mara moja jina lake kisha subir ntakujibu nkishaiadd kwenye database bonyeza kitufe hapo chini kutuma kisha ukurasa unaofuata bonyeza start kisha ntumie jina LA muv au series au nyimbo unayotafta", disable_web_page_preview = True),
            description=f'Hapa ndiyo mwisho wa  matokeo yetu kutoka kwenye database\nBonyeza hapa kama haipo kupata maelezo zaidi',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Bonyeza hapa kutuma', url=f"{gd1}")]])
        ))
    try:
        await query.answer(results=results,
            is_personal = True,
            cache_time=300,
            next_offset=str(next_offset))
    except Exception as e:
        logging.exception(str(e))
        await query.answer(results=[], is_personal=True,
            cache_time=cache_time,
            switch_pm_text=str(e)[:63],
            switch_pm_parameter="error")
    return
        
       
@Bot0.on_callback_query(filters.regex(r"^(alertmessage):(\d):(.*)"))
async def alert_msg(client, callback):
    regex = r"^(alertmessage):(\d):(.*)"
    matches = re.match(regex, callback.data)
    i = matches.group(2)
    id = matches.group(3)
    filter = {'id': id}
    cursor = Media.find(filter)
    filedetails = await cursor.to_list(length=1)
    for alert in filedetails:
        alerts = alert.alert
    if alerts:
        alerts = ast.literal_eval(alerts)
        alert = alerts[int(i)]
        alert = alert.replace("\\n", "\n").replace("\\t", "\t")
        try:
            await callback.answer(alert,show_alert=True)
        except:
            pass
    return
