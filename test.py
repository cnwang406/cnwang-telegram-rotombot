from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,InlineQueryHandler
from telegram import InlineQueryResultArticle,InputTextMessageContent,InlineQueryResultLocation,InputLocationMessageContent
import logging
from masks.usersdata import Users
from masks.masks import MASKS
from uuid import uuid4,uuid1

VERSION = 0.1
def hello(bot, update):
    print (type(bot), type(update))
    update.message.reply_text(
        f'hello, {update.message.from_user.first_name}')

def start(update, context):
    print (type(update))
    print (type(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text='I\'m bot')
def help(update, context):
    txt=f'''
    ------------------------------------
    Masks finder   by cnwang.{VERSION}

    /mask child/adult/distance/max_count [sortkey]
    
    sortkey=[-]c|C|a|A|d|D

    this inline bot need ur location
    -----------------------------------
    '''
    context.bot.send_message(chat_id=update.effective_chat.id, text=txt)

def dumpUser(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=allUsers.dumps())

def queryMask(update, context):
    msg=update.message

    if allUsers.checkUser(msg.chat.username):
        loc = allUsers.getUserLoc(msg.chat.username)
        if  loc!=None :
            masks.getPharmaciesData()
            masks.setHome(loc)
            masks.filterOut()
            txt=masks.filteredS()
            print (txt)
            context.bot.send_message(chat_id=update.effective_chat.id, text=txt)

    else :
        txt='you need to provide location.'
        context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
    pass
def echo(update, context):
    msg = update.message
    #txt = f'{msg.text} --> {update},// {context}'
    #context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
    txt2= f'I got message from {msg.chat.username}'
    context.bot.send_message(chat_id=885644313, text=txt2)
def msgHandler(update, context):
    txt = f'I got a photo --> {update}'
    context.bot.send_message(chat_id=update.effective_chat.id, text=txt)

def getLocation(update, context):
    if update.edited_message:
        msg=update.edited_message
        edited=True
    else:
        msg=update.message
        edited=False
    txt=f'I got location from {msg.chat.username},(edit={edited}) ->{msg.location}'
    tmp={'name':msg.chat.username, 'loc':[msg.location['longitude'],msg.location['latitude']]}
    allUsers.addModUserLoc(tmp)
    context.bot.send_message(chat_id=update.effective_chat.id, text=txt)

def inlinequery(update, context):
    query=update.inline_query.query.split(' ')
    #if (update.inline_query.hasOwnProperty('location')):
    #    loc=update.inline_query.location
    #else:
    #    loc={'longitude':120.997655,'latitude':24.776416}
    loc=update.inline_query.location
#    print(update.inline_query, type(update.inline_query),loc)
    if loc is None:
        loc={'longitude':120.997655,'latitude':24.776416}
       
    logging.info(f'location is {loc}')
       
    #loc = update.inline_query.location
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

                results.append(result)
        update.inline_query.answer(results)
        #logging.info('----')
        #logging.info(results)
def error(update, context):
    """Log Errors caused by Updates."""

    logging.warning('Update "%s" caused error "%s"', update, context.error)

allUsers=Users()
masks=MASKS(home=[120.997655, 24.776416])
#location_handler = MessageHandler(Filters.location, location)
#dispatcher.add_handler(location_handler)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


updater = Updater(token='1151488827:AAEc7NUKdKb19yuJY4xW27UVzdu54TFEcoU', use_context=True)
#updater=Updater('TOKEN', use_context=True)
dispatcher = updater.dispatcher

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
updater.start_polling()

updater.idle()


