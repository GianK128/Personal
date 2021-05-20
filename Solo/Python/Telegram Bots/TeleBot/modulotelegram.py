# KEBERLEIN, Gian Franco - circa Sept. - Oct. 2020

from telegram import ReplyKeyboardMarkup, Bot
from telegram.ext import Updater, MessageHandler, CommandHandler, ConversationHandler, Filters
import pruebamodulo as server   #Aca importar el archivo del server

#/start - mensaje de bienvenida -
#/help - devuelve los comandos disponibles -
#/login - pide mail, contraseña y agarra el chat id -
#/estados - llama al servidor para que le devuelva los estados de los sensores -
#/alarma - desplega un replykb para desactivar o activar la alarma -
#/config - mostrar los dispositivos que se intentaron conectar y preguntar si se quiere conectar -

#TODO:  ver si se puede implementar check de usuario para caso de meterlo en un grupo
#       ver si se puede meter un timeout en las conversaciones
#       ACOMODAR LAS LLAMADAS A LA BD

#'Estados' para los dict de las conversaciones
DEVICE_CHECK_PASS, DEVICE_SELECT_MODE, DEVICE_SELECT_ONE, DEVICE_CONFIG_2, DEVICE_NAME = range(5)
LOGINUSER, LOGINPASSWORD, LOGINPASSWORDCONFIRM, LOGINEND = range(4)
SETTINGPASSWORDCHECK, SETTINGALARM = range(2)
STATESCALLFORUSER = 0

#Aca guarda datos temporales (?)
userdata = []           #Datos de usuario para chequeos
deviceList = [[]]       #Datos de dispositivos que llega del server
deviceSet = [[]]        #Datos de dispositivos que se van a enviar al server

#Flag de 'dispositivos quieren conectarse'
devicesReady = False

#Clase del bot
class TeleBot():
    #Declarar previamente, aunque no es necesario (?)
    bot = None

    #Constructor - toma un token (único) y lo establece para este bot
    def __init__(self, idToken):
        self.bot = Bot(idToken)
    
    #Enviar mensaje a una chat_id especifica
    def SendMessageToChat(self, chatID, txt):
        self.bot.sendMessage(chatID, txt)

    #Notificación de disp. intentando conectarse - levantar el flag de 'devicesReady'
    def NotifyDeviceReady(self, chatID):
        global devicesReady
        self.bot.sendMessage(chatID, "Un dispositivo intenta conectarse. Puede usar /config para establecerlo como suyo.")
        devicesReady = True

    #Arrancar el bot y dejarlo corriendo
    def StartBot(self):
        #updater y dispatcher
        updater = Updater(bot = self.bot, use_context = True)
        dp = updater.dispatcher

        #Conv. de login
        convLogin = ConversationHandler(
            entry_points = [CommandHandler("login", cnvLoginStart)],
        
            states = {
                LOGINUSER: [MessageHandler(Filters.regex('[a-zA-Z]+[@]+[a-zA-Z]+(.com-ar|.com)$'), cnvLoginEnteredUser)],

                LOGINPASSWORD: [MessageHandler(Filters.all, cnvLoginEnteredPass)],

                LOGINPASSWORDCONFIRM: [MessageHandler(Filters.all, cnvLoginConfirmedPass)],

                LOGINEND: [MessageHandler(Filters.regex('[a-zA-Z]'), cnvLoginEnd)]
            },

            fallbacks = [CommandHandler("cancel", convCancel)]
        )

        #Conv. de estados de alarma
        convAlarmStates = ConversationHandler(
            entry_points = [CommandHandler("estados", convStatesStart)],

            states = {
                STATESCALLFORUSER: [MessageHandler(Filters.regex('[a-zA-Z]'), convStatesCheckPass)],
            },

            fallbacks = [CommandHandler("cancel", convCancel)]
        )

        #Conv. de activacion de alarma
        convAlarmSet = ConversationHandler(
            entry_points = [CommandHandler("alarma", convSettingStart)],

            states = {
                SETTINGPASSWORDCHECK: [MessageHandler(Filters.regex('[a-zA-Z]'), convSettingPassCheck)],

                SETTINGALARM: [MessageHandler(Filters.regex('^Activar$'), convSettingSetOnAlarm),
                                MessageHandler(Filters.regex('^Desactivar$'), convSettingSetOffAlarm)]
            },

            fallbacks = [CommandHandler("cancel", convCancel)]
        )

        #Conv. de config. de dispositivos
        convDeviceSet = ConversationHandler(
            entry_points = [CommandHandler("config", convDeviceStart)],

            states = {
                DEVICE_CHECK_PASS: [MessageHandler(Filters.all, convDeviceCheckPass)],

                DEVICE_SELECT_MODE: [
                    MessageHandler(Filters.regex('^Ver lista$'), convDeviceShowList),
                    MessageHandler(Filters.regex('^Abandonar$'), convDeviceLeave)
                ],

                DEVICE_SELECT_ONE: [MessageHandler(Filters.regex('^[0-9]+$'), convDeviceConfig)],

                DEVICE_CONFIG_2: [
                    MessageHandler(Filters.regex('^Sí$'), convDeviceConfigAccepted),
                    MessageHandler(Filters.regex('^No$'), convDeviceConfigDenied)
                ],

                DEVICE_NAME: [MessageHandler(Filters.regex('^[a-zA-Z]$'), convDeviceConfigNamed)]
            }
        )

        #Handlers
        dp.add_handler(CommandHandler("start", startMessage))
        dp.add_handler(CommandHandler("help", helpMessage))
        dp.add_handler(convAlarmStates)
        dp.add_handler(convAlarmSet)
        dp.add_handler(convDeviceSet)
        dp.add_handler(convLogin)

        #Arrancar a actualizar
        updater.start_polling()

#=========================CONVERSACIONES CON EL BOT=========================#

def startMessage(update, context):
    update.message.reply_text("Bienvenido al AlarmaBot. Use /help para ver una lista de comandos, o /login para establecer su usuario.")

def helpMessage(update, context):
    update.message.reply_text("Lista de comandos: " +
    "\n/help - despliega esta lista de comandos." + 
    "\n/login - comienza la configuración de usuario." + 
    "\n/estados - muestra los sensores conectados y sus estados." + 
    "\n/alarma - activar o desactivar la alarma." + 
    "\n/config - abre la configuracion de dispositivos que intentan conectarse.")

#==========CONVERSACION PARA ESTADOS DE ALARMA==========#
# - El bot chequea si este chat_id ya esta registrado, si no lo esta, cancela la operación.
# - Si lo está, el bot pide una confirmación de contraseña.
# - Si el usuario ingresa bien su contraseña, se le pide al server una lista de sensores conectados.
# - Para terminar, despliega esta lista con formato de lista (obviamente).

def convStatesStart(update, context):
    #Se llama funcion del server para chequear si existe el chatID en la base -->
    #<-- Regresa una bool 'idExists'
    idExists = True                                         #TODO: reemplazar por la funcion del server
    
    if idExists:
        update.message.reply_text("Ingrese su contraseña.")
        return STATESCALLFORUSER
    else:
        update.message.reply_text("Debe crear un usuario primero. Use /login.")
        return ConversationHandler.END

def convStatesCheckPass(update, context):
    password = update.message.text
    chatID = update.message.chat_id

    #Llamar a la funcion para chequear si la contraseña de este ID es correcta -->
    #<-- Regresa una bool 'passConfirm'
    passConfirm = True

    if passConfirm:
        #Llamar funcion del server que devuelva una lista con datos de los sensores -->
        #<-- Se guarda en una matriz 'sensorData'
        #TODO: funcion para formatear todos los datos de sensorData y responder con esa string
        return ConversationHandler.END
    else:
        update.message.reply_text("Contraseña incorrecta, intente nuevamente. Puede cancelar la operación con /cancel.")
        return STATESCALLFORUSER

#==========CONVERSACION SET ALARMA==========#
# - El bot chequea si este chat_id ya esta registrado, si no lo esta, cancela la operación.
# - Si lo está, el bot pide una confirmación de contraseña.
# - Si el usuario ingresa bien su contraseña, se le pregunta si desea activar o desactivar la alarma general.
# - Tanto como si se activa o desactiva, se llama una funcion del server para realizar la acción.

def convSettingStart(update, context):
    #Se llama funcion del server para chequear si existe el chatID en la base -->
    #<-- Regresa una bool 'idExists'
    idExists = True                                         #TODO: reemplazar por la funcion del server
    
    if idExists:
        update.message.reply_text("Ingrese su contraseña.")
        return SETTINGPASSWORDCHECK
    else:
        update.message.reply_text("Debe crear un usuario primero. Use /login.")
        return ConversationHandler.END

def convSettingPassCheck(update, context):
    password = update.message.text
    chatID = update.message.chat_id

    #Llamar a la funcion para chequear si la contraseña de este ID es correcta -->
    #<-- Regresa una bool 'passConfirm'
    passConfirm = True

    if passConfirm:
        reply_kb = [["Activar", "Desactivar"]]

        update.message.reply_text(
            "Contraseña correcta. ¿Qué desea hacer con su alarma?",
            reply_markup = ReplyKeyboardMarkup(reply_kb, one_time_keyboard = True)    
        )

        return SETTINGALARM
    else:
        update.message.reply_text("Contraseña incorrecta, intente nuevamente. Puede cancelar la operación con /cancel.")
        return SETTINGPASSWORDCHECK

def convSettingSetOnAlarm(update, context):
    #Llamar funcion de encender alarma del servidor -->
    return ConversationHandler.END

def convSettingSetOffAlarm(update,context):
    #Llamar funcion de apagar alarma del servidor -->
    return ConversationHandler.END

#==========CONVERSACION PARA LOGIN==========#
# - El bot pide un e-mail, para empezar.
# - El bot chequea si este chat_id ya está registrado, si lo está, cancela la operación.
# - Si no lo está, el bot pide una contraseña.
# - Si el usuario ingresa bien su contraseña, se le pide una confirmación de la misma.
# - Si el usuario confirma bien su contraseña, se le pide un nombre de usuario.
# - Todos estos datos, que fueron guardados en una lista, son enviados al server para guardar en la base.
# - Esto se hace llamando una función del server que haga esto mismo.

def cnvLoginStart(update, context):
    update.message.reply_text("Ingrese su correo electrónico. Ejemplo: prueba@gmail.com")
    return LOGINUSER

def cnvLoginEnteredUser(update, context):
    global userdata
    #Se llama funcion del server para chequear si existe el chatID en la base -->
    #<-- Devuelve una bool 'idExists'
    idExists = True

    if idExists:
        update.message.reply_text("Se detectó que usted ya tiene un usuario. Use /help para ver los comandos disponibles.")
    else:
        userdata.insert(0, update.message.text)
        update.message.reply_text("Correo valido. Ingrese una contraseña.")
        return LOGINPASSWORD

def cnvLoginEnteredPass(update, context):
    global userdata
    userdata.insert(1, update.message.text)
    update.message.reply_text("Ingrese nuevamente la contraseña.")
    return LOGINPASSWORDCONFIRM

def cnvLoginConfirmedPass(update, context):
    global userdata

    passwordC = userdata[1]
    password = update.message.text

    if password == passwordC:
        update.message.reply_text("Contraseña validada. ¿Cómo desea llamar su usuario? (solo letras a-z y mayúsculas).")
        return LOGINEND
    else:
        update.message.reply_text("Contraseña incorrecta, intente nuevamente.")
        return LOGINPASSWORDCONFIRM

def cnvLoginEnd(update, context):
    global userdata

    userdata.insert(2, update.message.text)
    userdata.insert(3, update.message.chat_id)

    update.message.reply_text("Registro exitoso. Bienvenido, {0}".format(userdata[2]))
    #Llamar función del server para guardar estos datos -->

    userdata.clear()
    return ConversationHandler.END

#==========CONVERSACION DE CONFIG.==========#
# - El bot chequea si este chat_id ya está registrado, si no lo está, cancela la operación.
# - Si lo está, el bot pide una confirmación de contraseña.
# - Si el usuario ingresa bien su contraseña, se le pregunta si desea ver la lista de dispositivos para conectar.
# - Si el usuario confirma, se despliega la lista (en formato), y se le pide que por índice elija un dispositivo.
# - El bot chequea que el indice no esté vacío, y pregunta si desea conectar el dispositivo o borrarlo.
# - Si se dice que no:
#   - El dispositivo es eliminado de la lista y se pregunta si desea volver a la lista o terminar.
#   - Tambien, si ya no quedan dispositivos, se envía la lista al server y se corta el trámite.
# - Si se dice que si:
#   - Se le pide al usuario que le ingrese un nombre al dispositivo y se lo ingresa a la lista 'deviceSet'
#   - Se le pregunta al usuario si desea ver la lista o terminar.
#   - Tambien, si ya no quedan dispositivos, se envía la lista al server y se corta el trámite.

def formatMessage(dList):
    finalMessage = "Estos dispositivos se intentaron conectar:"
    #TODO: se podria implementar un diccionario acá para agilizar las cosas.
    
    for i in dList:
        finalMessage += "\n{0}. MAC del disp.: {1}. Tiempo de conexión: {2}.".format(i + 1, dList[i][0], dList[i][1])
    
    finalMessage += "\nElija el que quiere configurar tipeando el número de la lista."
    return finalMessage

def convDeviceStart(update, context):
    #Se llama funcion del server para chequear si existe el chatID en la base -->
    #<-- Regresa una bool 'idExists'
    idExists = True                                         #TODO: reemplazar por la funcion del server
    
    if idExists:
        update.message.reply_text("Ingrese su contraseña.")
        return DEVICE_CHECK_PASS
    else:
        update.message.reply_text("Debe crear un usuario primero. Use /login.")
        return ConversationHandler.END

def convDeviceCheckPass(update, context):
    password = update.message.text
    chatID = update.message.chat_id
    #Llamar a la funcion para chequear si la contraseña de este ID es correcta -->
    #<-- Regresa una bool 'passConfirm'
    passConfirm = True

    if passConfirm:
        reply_kb = [['Ver lista','Abandonar']]
        update.message.reply_text("Contraseña correcta. ¿Qué desea hacer?", 
            reply_markup = ReplyKeyboardMarkup(reply_kb, one_time_keyboard = True)
        )

        return DEVICE_SELECT_MODE
    else:
        update.message.reply_text("Contraseña incorrecta. Intente nuevamente o abandone con /cancel")
        return DEVICE_CHECK_PASS

def convDeviceShowList(update, context):
    #TODO: se podria optimizar en tiempo ocupando mas espacio creo...
    global deviceList
    global devicesReady

    if devicesReady:
        #Se llama a la función que devuelve los dispositivos para conectar -->
        #<-- Se guarda en la deviceList

        strDisp = formatMessage(deviceList)
        update.message.reply_text(strDisp)

        return DEVICE_SELECT_ONE
    else:
        update.message.reply_text("Ningún dispositivo está intentando conectarse. Operación terminada.")
        return ConversationHandler.END

def convDeviceConfig(update, context):
    global deviceList
    index = int(update.message.text) - 1

    if not deviceList[index]:
        if not deviceList:
            update.message.reply_text("Error: matriz vacía.")
            return ConversationHandler.END
        else:
            update.message.reply_text("No hay dispositivo en ese indice de lista.")

            reply_kb = [['Ver lista','Abandonar']]
            update.message.reply_text("¿Cómo desea continuar?", 
                reply_markup = ReplyKeyboardMarkup(reply_kb, one_time_keyboard = True)
            )
            
            return DEVICE_SELECT_MODE
    else:
        global deviceSet
        disp = deviceList[index][0]

        reply_kb = [['Sí', 'No']]
        update.message.reply_text("Se seleccionó el dispositivo {0}.\n¿Quiere conectarlo?".format(disp),
            reply_markup = ReplyKeyboardMarkup(reply_kb, one_time_keyboard = True)
        )

        deviceList[index:index+1] = []
        deviceSet.append(disp)

        return DEVICE_CONFIG_2

def convDeviceConfigDenied(update, context):
    global deviceList, deviceSet
    deviceSet[-1:len(deviceSet)] = []

    if not deviceList:
        #Llamar funcion para entregarle la lista de dispositivos conectados al server -->

        update.message.reply_text("Ya no hay mas dispositivos. Operación terminada")
        return ConversationHandler.END
    else:
        reply_kb = [['Ver lista','Abandonar']]

        update.message.reply_text("Se decidió no conectar este dispositivo.\n¿Cómo desea continuar?",
            reply_markup = ReplyKeyboardMarkup(reply_kb, one_time_keyboard = True)
        )
        return DEVICE_SELECT_MODE

def convDeviceConfigAccepted(update, context):
    update.message.reply_text("Se decidió conectar este dispositivo. ¿Con qué nombre desea guardarlo?")
    return DEVICE_NAME

def convDeviceConfigNamed(update, context):
    global deviceList, deviceSet
    update.message.reply_text("Nombre guardado correctamente.")

    #No se habla de la siguiente linea de codigo...
    deviceSet[-1].insert(len(deviceSet[-1]), update.message.text)

    if not deviceList:
        #Llamar funcion para entregarle la lista de dispositivos conectados al server -->

        update.message.reply_text("Ya no hay mas dispositivos. Operación terminada")
        return ConversationHandler.END
    else:
        reply_kb = [['Ver lista','Abandonar']]

        update.message.reply_text("Se terminó de configurar este dispositivo.\n¿Cómo desea continuar?",
            reply_markup = ReplyKeyboardMarkup(reply_kb, one_time_keyboard = True)
        )
        return DEVICE_SELECT_MODE

def convDeviceLeave(update, context):
    global deviceList, deviceSet

    deviceList.clear()
    #Llamar funcion para entregarle la lista de dispositivos conectados al server -->
    deviceSet.clear()

    update.message.reply_text("Operación terminada.")
    return ConversationHandler.END

#==========CANCELAR CONVERSACION==========#
# - Este callback cancela casi todos las conversaciones y limpia las listas y matrices.
def convCancel(update, context):
    global userdata, deviceList, deviceSet

    userdata.clear()
    deviceList.clear()
    deviceSet.clear()

    update.message.reply_text("Operacion cancelada.")
    return ConversationHandler.END