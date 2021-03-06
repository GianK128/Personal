from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, CommandHandler, ConversationHandler, Filters, CallbackContext
import pymysql as sql

#Bot de Telegram interactivo mediante ConversationHandler con comandos basicos para una Base de Datos. (25/06/2020)
#   ConversationHandler tiene 3 'partes' que usar: entry_points, states, y fallback
#   - entry_points: es una lista de Handlers que se chequean cada update para entrar a la conversacion.
#   - states: es un dictionary con cada estado y los Handlers que avanzaran la conversacion.
#   - fallback: es la lista de Handlers que se chequea si todos los Handlers de states tiraron False.
#   Para informacion mas especifica conviene ver la documentacion, este codigo es basura.
#Hay varias partes del codigo que se tienen que cambiar si se quiere adaptar a otra base pero espero que sirva de guía.

#Token id del bot
botToken = "1348664736:AAHO9qQEuKZIHgNf4jWFglyl7EPFCajnYAc" #El token de tu bot

#Crear conexion con la DB
conexion = sql.connect(
    host = "localhost",                     #Tu host
    user = "root",                          #Tu user
    password = "G170902F",                  #Tu contraseña
    db = "GABINETE_ABOGADOS"                #Tu DB
)

#Cursor (busca los datos en la db)
cursor = conexion.cursor()

#Esta lista va a guardar los datos para posterior uso
dataList = []

#Definir estados de las conversaciones
SELECTDB, SELECTFUNC, SELECTTYPE, SELECTWHERE = range(4)
INSERTDB, INSERTEND = range(2)
DELETEDB, DELETEEND = range(2)

#Funcion que forma una string por tabla (modificar segun los datos de cada DB)
def formatTable(table):
    txt = ""
    tabla = dataList[0]

    if (tabla == "Procuradores"):
        for i in table:
            txt += "Matricula: " + str(i[1]) + "\n"
            txt += "Nombre: " + i[2] + "\n"
            txt += "DNI: " + str(i[3]) + "\n"
            txt += "Dirección: " + i[4] + "\n"
            txt += "Teléfono: " + str(i[5]) + "\n\n" 
        return txt
    elif (tabla == "Clientes"):
        for i in table:
            txt += "Nro. Cliente: " + str(i[1]) + "\n"
            txt += "Nombre: " + i[2] + "\n"
            txt += "DNI: " + str(i[3]) + "\n"
            txt += "Dirección: " + i[4] + "\n"
            txt += "Teléfono: " + str(i[5]) + "\n\n" 
        return txt
    else:
        return 'Error inesperado en el formato de tabla'

def start(update, context):
    update.message.reply_text(
        'Buenas. Soy el bot para probar conversaciones.\nPodés usar /help para ver los comandos disponibles.'
    )

def bothelp(update, context):
    update.message.reply_text(
        'Lista de comandos:\n/select - Abre menú para buscar en la base de datos.\n/insert - Abre menú para insertar registros en la base de datos.\n/delete - Abre menú para borrar registros de la base (por matrícula/número de cliente).'
    )

#|====================Conversacion para SELECT====================|
#Elegir Base de Datos
def convSelectInit(update, context):
    reply_kb = [['Procuradores', 'Clientes']]

    update.message.reply_text(
        '¿De que tabla se quiere fijar los registros?',
        reply_markup = ReplyKeyboardMarkup(reply_kb, one_time_keyboard = True)
    )

    return SELECTDB

#Elegir si SELECT total o especifico
def convSelectDB(update, context):
    db = update.message.text
    dataList.insert(0, db)
    reply_kb = [['Todos', 'Específico']]

    update.message.reply_text(
        'En la tabla ' + db.lower() + ', ¿Desea sacar todos los registros o alguno en especifico?',
        reply_markup = ReplyKeyboardMarkup(reply_kb, one_time_keyboard = True)
    )

    return SELECTFUNC

#SELECT total de la tabla
def convSelectFetchall(update, context):
    dataList.insert(1, "*")
    keyword = update.message.text

    cmd = "SELECT "+ dataList[1] +" FROM "+ dataList[0] +";"
    cursor.execute(cmd)

    out = formatTable(cursor.fetchall())

    if (out != ""):
        update.message.reply_text(out)
    else:
        update.message.reply_text('No hay registros coincidentes.')

    dataList.clear()
    return ConversationHandler.END

#SELECT especificoS
def convSelectFetch(update, context):
    dataList.insert(1, "*")

    if (dataList[0] == "Procuradores"):
        reply_kb = [['Matrícula', 'Nombre Abog.']]
    elif (dataList[0] == "Clientes"):
        reply_kb = [['Número Cliente', 'Nombre Cliente']]

    update.message.reply_text(
        '¿Como desea buscar su registro en la tabla?',
        reply_markup = ReplyKeyboardMarkup(reply_kb, one_time_keyboard = True)
    )

    return SELECTTYPE

def convSelectClientes(update, context):
    txt = update.message.text
    if (txt == "Número Cliente"):
        dataList.insert(2, "nro_cliente")
    else:
        dataList.insert(2, "nombre_cliente")

    update.message.reply_text(
        'Ingrese la/s palabra/s clave que desea buscar.'
    )

    return SELECTWHERE

def convSelectProc(update, context):
    txt = update.message.text
    if (txt == "Matrícula"):
        dataList.insert(2, "nro_mat")
    else:
        dataList.insert(2, "nombre_proc")

    update.message.reply_text(
        'Ingrese la/s palabra/s clave que desea buscar.'
    )

    return SELECTWHERE

#Busqueda final SELECT
def convSelectEnd(update, context):
    keyword = update.message.text

    cmd = "SELECT "+ dataList[1] +" FROM "+ dataList[0] +" WHERE "+ dataList[2] +" LIKE '%"+ keyword + "%';"
    cursor.execute(cmd)

    out = formatTable(cursor.fetchall())

    if (out != ""):
        update.message.reply_text(out)
    else:
        update.message.reply_text('No hay registros coincidentes.')

    dataList.clear()
    return ConversationHandler.END

#|====================Conversacion para INSERT====================|
#Seleccion de DB
def convInsertInit(update, context):
    reply_kb = [['Procuradores', 'Clientes']]

    update.message.reply_text(
        '¿A qué base de datos desea insertar un registro?',
        reply_markup = ReplyKeyboardMarkup(reply_kb, one_time_keyboard = True)
    )

    return INSERTDB

#Luego de seleccion de DB
def convInsertDB(update, context):
    db = update.message.text
    dataList.insert(0, db)

    if (db == "Procuradores"):
        update.message.reply_text(
            'Inserte los datos a ingresar separado por guiones. Con el siguiente formato:\nmatricula-nombre-dni-direccion-telefono'
        )
    else:
        update.message.reply_text(
            'Inserte los datos a ingresar separado por guiones. Con el siguiente formato:\nnumerocliente-nombre-dni-direccion-telefono'
        )

    return INSERTEND

#INSERT final en la DB
def convInsertEnd(update, context):
    #Dividir la string en argumentos
    txt = update.message.text
    argsList = txt.split("-")

    #Chequear que el usuario haya dado 5 argumentos
    if (len(argsList) != 5):
        update.message.reply_text(
            'Hubo un error en el ingreso de datos (faltan datos). Intente nuevamente llamando a /insert'
        )
        return ConversationHandler.END

    db = dataList[0]
    nro = argsList[0]
    nombre = argsList[1]
    dni = argsList[2]
    dire = argsList[3]
    tel = argsList[4]

    if (db == "Procuradores"):
        cmd = "INSERT INTO Procuradores(nro_mat, nombre_proc, dni_proc, dir_proc, tel_proc) VALUES ("+ nro +",'"+ nombre +"',"+ dni +",'"+ dire +"',"+ tel +");"
    elif (db == "Clientes"):
        cmd = "INSERT INTO Clientes(nro_cliente, nombre_cliente, dni_cliente, dir_cliente, tel_cliente) VALUES ("+ nro +",'"+ nombre +"',"+ dni +",'"+ dire +"',"+ tel +");"

    try:
        cursor.execute(cmd)
        update.message.reply_text(
            'Registro guardado con exito.'
        )
    except:
        update.message.reply_text(
            'Hubo un error al ingresar el registro.'
        )

    #Hacer commit y limpiar la lista
    conexion.commit()
    dataList.clear()
    return ConversationHandler.END

#|====================Conversacion para DELETE====================|
#Seleccion de DB
def convDeleteInit(update, context):
    reply_kb = [['Procuradores', 'Clientes']]

    update.message.reply_text(
        '¿De qué base de datos desea eliminar un registro?',
        reply_markup = ReplyKeyboardMarkup(reply_kb, one_time_keyboard = True)
    )

    return DELETEDB

#Luego de la seleccion de DB
def convDeleteDB(update, context):
    dataList.insert(0, update.message.text)

    update.message.reply_text(
        'Está por eliminar un registro segun su matricula/numero de cliente, solo se aceptan numeros como respuesta.\nSi está seguro, escriba el número.\nSi no, puede usar /cancel para denegar la acción.'
    )

    return DELETEEND

#DELETE final
def convDeleteEnd(update, context):
    txt = update.message.text
    db = dataList[0]

    if (db == "Procuradores"):
        cmd = "DELETE FROM Procuradores WHERE nro_mat = " + txt + ";"
    elif (db == "Clientes"):
        cmd = "DELETE FROM Clientes WHERE nro_cliente = " + txt + ";"

    try:
        cursor.execute(cmd)
        update.message.reply_text(
            'Registro eliminado con exito.'
        )
    except:
        update.message.reply_text(
            'Hubo un error al eliminar el registro.'
        )

    return ConversationHandler.END

#Cancelar conversaciones
def convCancel(update, context):
    update.message.reply_text('La acción fue cancelada.')
    return ConversationHandler.END

#|==============================MAIN==============================|
def main():
    updater = Updater(token = botToken, use_context = True)   #CallBackContext pasa cierta data a las funciones
    dp = updater.dispatcher

    #Conversacion para SELECT
    conv_select = ConversationHandler(
        entry_points = [CommandHandler("select", convSelectInit)],

        states = {
            #Seleccionar DB
            SELECTDB: [MessageHandler(Filters.regex('^(Procuradores|Clientes)$'), convSelectDB)],

            #Seleccionar como traer los registros
            SELECTFUNC: [MessageHandler(Filters.regex('^Todos$'), convSelectFetchall),
                         MessageHandler(Filters.regex('^(Específico)$'), convSelectFetch)],

            #De aca en adelante es una parte opcional, es solo para hacer mas comodo al usuario.
            #Seleccionar por cual dato buscar los registros
            SELECTTYPE: [MessageHandler(Filters.regex('^(Número Cliente|Nombre Cliente)$'), convSelectClientes),
                         MessageHandler(Filters.regex('^(Matrícula|Nombre Abog.)$'), convSelectProc)],

            #Seleccionar el dato del que se deben buscar coincidencias
            SELECTWHERE: [MessageHandler(Filters.all, convSelectEnd)]
        },

        fallbacks = [CommandHandler("cancel", convCancel)]
    )

    #Conversacion para INSERT
    conv_insert = ConversationHandler(
        entry_points = [CommandHandler("insert", convInsertInit)],

        states = {
            #Seleccionar DB
            INSERTDB: [MessageHandler(Filters.regex('^(Procuradores|Clientes)$'), convInsertDB)],

            #Escribir datos para ingresar
            INSERTEND: [MessageHandler(Filters.all, convInsertEnd)]
        },

        fallbacks = [CommandHandler("cancel", convCancel)]
    )

    #Conversacion para DELETE
    conv_delete = ConversationHandler(
        entry_points = [CommandHandler("delete", convDeleteInit)],

        states = {
            DELETEDB: [MessageHandler(Filters.regex('^(Procuradores|Clientes)$'), convDeleteDB)],

            DELETEEND: [MessageHandler(Filters.regex('^[0-9]$'), convDeleteEnd)]
        },

        fallbacks = [CommandHandler("cancel", convCancel)]
    )

    #Añadir los Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", bothelp))
    dp.add_handler(conv_select)
    dp.add_handler(conv_insert)
    dp.add_handler(conv_delete)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()