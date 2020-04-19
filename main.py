import logging
from masks.usersdata import Users
from telegram import InlineQueryResultArticle,InputTextMessageContent,InlineQueryResultLocation,InputLocationMessageContent,Bot,Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,InlineQueryHandler,Dispatcher
from masks.masks import MASKS
from uuid import uuid4,uuid1
from flask import Flask, request
import configparser
import os
import sys

APPNAME = 'cnwang-telegram-rotombot'  # for heroku hosting
VERSION = 0.5

config = configparser.ConfigParser()
config.read('config.ini')

app=Flask(__name__)

@app.route('/hook', methods=['POST'])
def hook():
    print ('called hook')
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return 'ok'

def hello(bot, update):
    txt=f'hello, {update.message.from_user.first_name}'
    update.message.reply_text(txt)
        
    bot.send_message(chat_id=update.effective_chat.id, text=txt)

def start(bot, update):
    bot.send_message(chat_id=update.effective_chat.id, text='I\'m bot')
def help(bot,update):
    txt=f'''
    ------------------------------------
    Masks finder   by cnwang.{VERSION}

    /mask child/adult/distance/max_count [sortkey]
    
    sortkey=[-]c|C|a|A|d|D

    this inline bot need ur location
    -----------------------------------
    '''
    bot.send_message(chat_id=update.effective_chat.id, text=txt)

def dumpUser(bot,update):

    bot.send_message(chat_id=update.effective_chat.id, text=allUsers.dumps())

def queryMask(bot,update):
    msg=update.message

    if allUsers.checkUser(msg.chat.username):
        loc = allUsers.getUserLoc(msg.chat.username)
        if  loc!=None :
            masks.getPharmaciesData()
            masks.setHome(loc)
            masks.filterOut()
            txt=masks.filteredS()
            print (txt)
            bot.send_message(chat_id=update.effective_chat.id, text=txt)

    else :
        txt='you need to provide location.'
        bot.send_message(chat_id=update.effective_chat.id, text=txt)
    pass

def msgHandler(bot, update):
    txt = 'I got a photo '
    bot.send_message(chat_id=update.effective_chat.id, text=txt)

def getLocation(bot, update):
    if update.edited_message:
        msg=update.edited_message
        edited=True
    else:
        msg=update.message
        edited=False
    txt=f'I got location from {msg.chat.username},(edit={edited}) ->{msg.location}'
    tmp={'name':msg.chat.username, 'loc':[msg.location['longitude'],msg.location['latitude']]}
    allUsers.addModUserLoc(tmp, msg.chat.id)
    #bot.send_message(chat_id=update.effective_chat.id, text=txt)
    logger.debug(txt)

def inlinequery(bot, update):
    query=update.inline_query.query.split(' ')
    if query[0].lower() in ('help','h'):
        result= input_message_content=InlineQueryResultArticle(id=uuid4(),title='HELP',
            input_message_content=InputTextMessageContent(message_text=f"""
            Mask Query by cnwang. Ver {VERSION}
            usage :
            @rotom406_bot child/adult/distance/maxcount
                find at least maxcount pharmacies which child and adult mask quanties within distance (km)
            """
            ))
        
        results=[result]
        update.inline_query.answer(results)
        return
    name = update.inline_query.from_user.username
    
    loc=update.inline_query.location
    
    if loc is None:
        loc={'longitude':120.997655,'latitude':24.776416}
       
    #logger.info(f'{name} \'s location is {loc}')   

    masks.setHome([loc['longitude'],loc['latitude']])
    
    if len(query)==1:
        sortKey='distance'
    else:
        sortKey=query[1]

    fields = query[0].split('/')
    if len(fields)==4:
        #print (query,sortKey, fields)
        hits=masks.findMasks(child=int(fields[0]),adult=int(fields[1]),distance=float(fields[2]),maxcount=int(fields[3]),sortKey=sortKey)
        #print (len(hits))
        if len(hits) != 0:
            print (f'doing filter ({len(hits)})...{masks.recordn2Str(0)} ')
        pass
    
        results=[]
        if len(hits)==0:
            results=[InlineQueryResultArticle(id=uuid4(),title='🈚️🈚️🈚️ NO FOUND 🈚️🈚️🈚️',input_message_content=InputTextMessageContent(u'請重新設定搜尋條件,因為要求太嚴苛了'))]
        else:
            for idx,hit in enumerate(hits):
                print(hit['name'])
                # macos, table/map, ios talble/map
                # InlineQueryResultLocation + input_message_content=InputTextMessageContent          O/X,O/X
                # InlineQueryResultLocation + input_message_content=InputLocationMessageContent     O/O,X/X                        
                # InlineQueryResultLocation +                                                        O/O,X/X 
                # InlineQueryResultLocation + input_message_content=InputTextMessageContent(+URL)   O/△,O/△

                #result=InlineQueryResultArticle(id=uuid4(),
                # title=masks.recordn2StrShort(idx),input_message_content=InputTextMessageContent(masks.recordn2Str(idx)))
                mapurl = f'https://www.google.com/maps/search/?api=1&query={hit["geometry"][1]},{hit["geometry"][0]}'
                result=InlineQueryResultLocation(id=uuid4(),
                    title=masks.recordn2StrShort(idx),
                    #title=str(idx),
                    latitude=float(hit['geometry'][1]),longitude=float(hit['geometry'][0]),
                    input_message_content=InputTextMessageContent(masks.recordn2Str(idx)+'\n'+mapurl),thumb_width=120,thumb_height=120
                    #input_message_content=InputLocationMessageContent(latitude=hit['geometry'][1],longitude=hit['geometry'][0], live_period=3600)
                    )
                logger.debug(f'{result.latitude},{result.input_message_content}')
                results.append(result)
        update.inline_query.answer(results)
        ret=allUsers.userAccess(name)
    else:
        result= input_message_content=InlineQueryResultArticle(id=uuid4(),title='兒童/成人/距離/顯示數量',
            input_message_content=InputTextMessageContent(message_text=f"""
            Mask Query by cnwang. Ver {VERSION}
            usage :
            @rotom406_bot child/adult/distance/maxcount
                find at least maxcount pharmacies which child and adult mask quanties within distance (km)
            """
            ))
        
        results=[result]
        update.inline_query.answer(results)
        return

def error(bot, update):
    """Log Errors caused by Updates."""
    logger.error('Update "%s" caused error "%s"', update, bot.error)
    
def echo(bot, update):
    print ('echo called')
    txt=update.message.text 
    if txt[0]!='💊':
        update.message.reply_text(update.message.text)

allUsers=Users()
masks=MASKS(home=[120.997655, 24.776416])
#location_handler = MessageHandler(Filters.location, location)
#dispatcher.add_handler(location_handler)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger=logging.getLogger('rotom406')
logger.setLevel(logging.DEBUG)
TOKEN = config['TELEGRAM']['token']
updater = Updater(token=TOKEN, use_context=True)
#mode = os.getenv('MODE')


#dispatcher = updater.dispatcher
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None)

dispatcher.add_handler(CommandHandler('hello', hello))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('dump', dumpUser))
dispatcher.add_handler(CommandHandler('mask', queryMask))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(MessageHandler(Filters.location,getLocation))
dispatcher.add_handler(MessageHandler(Filters.photo & (~Filters.forwarded),msgHandler))
dispatcher.add_handler(MessageHandler(Filters.text, echo))
dispatcher.add_handler(InlineQueryHandler(inlinequery))
dispatcher.add_error_handler(error)
mode = 'dev'
print (f'mode={mode}')
if  mode=='prod':
    logger.info('prod mode')
    def run(updater):
        print ('running prod')
        PORT=int(os.environ.get('PORT','5000'))        
        updater.start_webhook(listen='0.0.0.0', port=PORT,url_path=TOKEN)
        updater.bot.set_webhook(f'https://{APPNAME}.herokuapp.com/'+TOKEN)
        updater.idle()
elif mode == 'dev':
    logger.info('dev mode')
    def run(updater):
        print ('running dev')
        updater.start_polling()
else:
    logger.info('running heroku')
    PORT=int(os.environ.get('PORT','8443'))
    updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN)
    updater.bot.set_webhook(f'https://{APPNAME}.herokuapp.com/'+TOKEN)
    updater.idle()

if __name__ == "__main__":
    PORT=int(os.environ.get('PORT','8443'))
    app.run(debug=True,port=PORT,host='0.0.0.0')
#https://api.telegram.org/bot1151488827:AAEc7NUKdKb19yuJY4xW27UVzdu54TFEcoU/setWebhook?url=https://65437aed.ngrok.io/hook
#https://api.telegram.org/bot1151488827:AAEc7NUKdKb19yuJY4xW27UVzdu54TFEcoU/setWebhook?url=https://cnwang-telegram-rotombot.herokuapp.com/hook