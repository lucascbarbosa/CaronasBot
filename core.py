from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
import telegram
from datetime import datetime

# TESTAR ADD IDA/VOLTA PARA OUTROS USUARIOS E O /IDA/VOLTA . TESTAR O ENVIO DE MENSAGENS.


class Bot_Caronas():
    def __init__(self, caronas_ida, caronas_volta, preço_diurno, preço_noturno):
        self.caronas_ida = caronas_ida
        self.caronas_volta = caronas_volta
        self.preço_diurno = preço_diurno
        self.preço_noturno = preço_noturno

    def ajuda(self, bot, update):
        response_message = """
    /add ida/volta [hh:mm] [descricao] para oferecer carona de volta.\n      Ex: /add ida 7:30 Até o Mundial.\n/remover ida/volta [hh:mm] para remover oferta de carona de ida.\n      Ex: /remover volta 8:00.\n/ida ou /volta para mostrar caronas pra ida/volta oferecidas.\n/entrou ou /saiu ida/volta [quantidade] para diminuir ou aumentar o numero de vagas da carona.\n      Ex: /saiu ida 3, /entrou volta 1.\n/set_preco diurno/noturno [reais.centavos] para informar o valor da carona diurna/noturna.\n       Ex: /set_preco diurno 7.0.\n/preco diurno/noturno para saber o valor da carona diurna/noturna.\n/find [hh:mm(ida),hh:mm(volta)] pra procurar caronas nos horários informados, e mandar mensagem pros motoristas.\n\n       Criado por Lucas Costa Barbosa github: @lucascbarbosa"""
        update.message.reply_text(response_message)

    def regras(self, bot, update):
        regras = """Regras: .\n--> Caronas para o dia seguinte podem ser oferecidas ou pedidas após as 19hrs. \n--> No grupo é proibido conversas paralelas. O único assunto permitido é o oferecimento e procura de caronas. Caso tenha uma notícia ou dúvida importante do trânsito, segurança ou da faculdade a ser compartilhada, usar [OFF] antes da mensagem. São proibidas imagens, vídeos e stickers.\n--> A ajuda de custo para o motorista é de 8 reais por pessoa.\n--> Seja pontual e evite cancelar em cima da hora, caso seja necessário, avise os demais da carona e tenha empatia caso alguém faça com você.\n--> Solicitamos nome e foto de perfil liberado para maior segurança.\n--> Seja cordial, ações machistas, homofóbicas ou racistas dentro das caronas e denunciadas não serão toleradas e resultarão em expulsão do grupo."""
        update.message.reply_text(regras)

    def add(self, bot, update, args, user_data, chat_data):
        sentido = args[0].lower()
        descricao = ' '.join(args[2:])
        username = update.message.from_user['username']
        user_id = update.message.from_user['id']

        time_hour = datetime.now().hour
        week_day = datetime.now().weekday()
        horario = args[1]

        if int(time_hour) < 19 and int(horario.split(':')[0]) > 19 and week_day != 6:
            update.message.reply_text(
                'Só é possível oferecer caronas a partir das 19h.')
        else:
            if sentido == 'ida':
                for horario, username, user_id, descriçao, vagas in self.caronas_ida:
                    if username == user:
                        update.message.reply_text(
                            'Você já ofertou uma carona para ida.')
                        return

                self.caronas_ida.append(
                    [horario, username, user_id, descricao, 4])
                update.message.reply_text('Carona de ida adiconada')

            if sentido == 'volta':
                for horario, username, user_id, descriçao, vagas in self.caronas_volta:
                    if username == user:
                        update.message.reply_text(
                            'Você já ofertou uma carona para volta.')
                        return

                self.caronas_volta.append(
                    [horario, username, user_id, descricao, 4])
                update.message.reply_text('Carona de volta adiconada')

    def ida(self, bot, update):
        update.message.reply_text('Horários de Ida:')
        for horario, username, user_id, descricao, vagas in self.caronas_ida:
            msg = 'Horário: ' + horario + ' - Motorista: @' + \
                str(username) + ' - Descrição: ' + \
                descricao + ' - Vagas: ' + str(vagas)
            bot.sendMessage(chat_id=update.message.chat_id, text=msg)

    def volta(self, bot, update):
        update.message.reply_text('Horários de Volta:')
        for horario, username, user_id, descricao, vagas in self.caronas_volta:
            msg = 'Horário: '+str(horario) + ' - Motorista: @' + str(username) + \
                ' - Descrição: ' + descricao + ' - Vagas: ' + str(vagas)
            bot.sendMessage(chat_id=update.message.chat_id, text=msg)

    def saiu(self, bot, update, args, user_data, chat_data):
        sentido = args[0].lower()
        qtd = int(args[1])
        username = update.message.from_user['username']
        if sentido == 'ida':
            for i in range(len(self.caronas_ida)):
                if self.caronas_ida[i][1] == username:
                    if self.caronas_ida[i][4]+qtd > 4:
                        update.message.reply_text("Número máximo excedido.")
                    else:
                        self.caronas_ida[i][4] += qtd
                        update.message.reply_text(
                            "%s pessoas sairam na carona da ida." % str(qtd))

        if sentido == 'volta':
            for i in range(len(self.caronas_volta)):
                if self.caronas_volta[i][1] == username:
                    if self.caronas_volta[i][4]+qtd > 4:
                        update.message.reply_text("Número máximo excedido.")
                    else:
                        self.caronas_volta[i][4] += qtd
                        update.message.reply_text(
                            "%s pessoas sairam na carona da volta." % str(qtd))

    def entrou(self, bot, update, args, user_data, chat_data):
        sentido = args[0].lower()
        qtd = int(args[1])
        username = update.message.from_user['username']
        print(sentido, qtd, username)
        if sentido == 'ida':
            for i in range(len(self.caronas_ida)):
                if self.caronas_ida[i][1] == username:
                    if self.caronas_ida[i][4]-qtd < 0:
                        update.message.reply_text("Número mínimo alcançado.")
                    else:
                        self.caronas_ida[i][4] -= qtd
                        update.message.reply_text(
                            "%s pessoas entraram na carona da ida." % str(qtd))
        if sentido == 'volta':
            for i in range(len(self.caronas_volta)):
                if self.caronas_volta[i][1] == username:
                    if self.caronas_volta[i][4]-qtd < 0:
                        update.message.reply_text("Número mínimo alcançado.")
                    else:
                        self.caronas_volta[i][4] -= qtd
                        update.message.reply_text(
                            "%s pessoas entraram na carona da volta." % str(qtd))

    def getVagas(self, bot, update, args, user_data, chat_data):
        user_id = update.message.from_user['id']
        username = update.message.from_user['username']
        sentido = args[0].lower()
        if sentido == 'ida':
            for i in range(len(self.caronas_ida)):
                if self.caronas_ida[i][1] == username:
                    vagas = self.caronas_ida[i][4]
                    bot.send_message(
                        chat_id=user_id, text='Vagas da carona de ida: %s' % str(vagas))

        if sentido == 'volta':
            for i in range(len(self.caronas_volta)):
                if self.caronas_volta[i][1] == username:
                    vagas = self.caronas_volta[i][4]
                    bot.send_message(
                        chat_id=user_id, text='Vagas da carona de volta: %s' % str(vagas))

    def remover(self, bot, update, args, user_data, chat_data):
        sentido = args[0].lower()
        username = update.message.from_user['username']
        if sentido == 'ida':
            for i in range(len(self.caronas_ida)):
                if self.caronas_ida[i][1] == username:
                    self.caronas_ida.remove(self.caronas_ida[i])
                    update.message.reply_text('Carona de ida removida')

        if sentido == 'volta':
            horario = args[1]
            for i in range(len(self.caronas_volta)):
                if self.caronas_volta[i][1] == username:
                    update.message.reply_text('Carona de volta removida')
                    self.caronas_volta.remove(self.caronas_volta[i])

    def setPreço(self, bot, update, args, user_data, chat_data):
        turno = args[0].lower()
        if turno == 'diurno':
            chat_id = update.message.chat_id
            user_id = update.message.from_user['id']
            user = bot.get_chat_member(chat_id, user_id)
            status = user['status']
            if status == 'creator' or status == 'administrator':
                self.preço_diurno = float(args[1])
                update.message.reply_text('Preço da carona diurna modificado.')
            else:
                bot.sendMessage(chat_id=update.message.chat_id,
                                text='Você não possui permissão.')

        if turno == 'noturno':
            chat_id = update.message.chat_id
            user_id = update.message.from_user['id']
            user = bot.get_chat_member(chat_id, user_id)
            status = user['status']
            if -status == 'administrator':
                self.preço_noturno = float(args[1])
                update.message.reply_text(
                    'Preço da carona noturna modificado.')
            else:
                bot.sendMessage(chat_id=update.message.chat_id,
                                text='Você não possui permissão.')

    def getPreço(self, bot, update, args):
        turno = args[0].lower()
        if turno == 'diurno':
            msg = "O preço da carona diurna é de %s0 reais" % str(
                self.preço_diurno)
            update.message.reply_text(msg)
        if turno == 'noturno':
            msg = "O preço da carona noturna é de %s0 reais" % str(
                self.preço_noturno)
            update.message.reply_text(msg)

    def findCaronas(self, bot, update, args, user_data):
        meu_user = update.message.from_user['username']
        ida, volta = args[0].split(',')

        for i in range(len(self.caronas_ida)):
            horario = self.caronas_ida[i][0]
            user_id = self.caronas_ida[i][2]
            if horario == ida:
                msg = 'Mensagem de @%s: Oi, tem vaga pra ida?' % (
                    str(meu_user))
                bot.sendMessage(chat_id=user_id, text=msg)

        for i in range(len(self.caronas_volta)):
            horario = self.caronas_volta[i][0]
            user_id = self.caronas_volta[i][2]
            if horario == volta:
                msg = 'Mensagem de @%s: Oi, tem vaga pra volta?' % (
                    str(meu_user))
                bot.sendMessage(chat_id=user_id, text=msg)


def main():
    # Create the Updater and pass it your bot's token.
    token = '934527625:AAH9aLXWYVloq4U1Pch1VeDM4zPvA_ncwoU'
    caronas_ida = []
    caronas_volta = []
    preço_diurno = 0
    preço_noturno = 0

    # initiliaze class that contains the callback functions for caronas
    bot_car = Bot_Caronas(caronas_ida, caronas_volta,
                          preço_diurno, preço_noturno)
    updater = Updater(token=token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram

    dispatcher.add_handler(
        CommandHandler('help', bot_car.ajuda)
    )

    dispatcher.add_handler(
        CommandHandler('regras', bot_car.regras)
    )

    dispatcher.add_handler(
        CommandHandler('add', bot_car.add, pass_args=True,
                       pass_user_data=True, pass_chat_data=True)
    )

    dispatcher.add_handler(
        CommandHandler('ida', bot_car.ida)
    )

    dispatcher.add_handler(
        CommandHandler('volta', bot_car.volta)
    )

    dispatcher.add_handler(
        CommandHandler('remover', bot_car.remover, pass_args=True,
                       pass_user_data=True, pass_chat_data=True)
    )

    dispatcher.add_handler(
        CommandHandler('entrou', bot_car.entrou, pass_args=True,
                       pass_user_data=True, pass_chat_data=True)
    )

    dispatcher.add_handler(
        CommandHandler('saiu', bot_car.saiu, pass_args=True,
                       pass_user_data=True, pass_chat_data=True)
    )

    dispatcher.add_handler(
        CommandHandler('vagas', bot_car.getVagas, pass_args=True,
                       pass_user_data=True, pass_chat_data=True)
    )

    dispatcher.add_handler(
        CommandHandler('set_preco', bot_car.setPreço, pass_args=True,
                       pass_chat_data=True, pass_user_data=True)
    )

    dispatcher.add_handler(
        CommandHandler('preco', bot_car.getPreço, pass_args=True)
    )

    dispatcher.add_handler(
        CommandHandler('find', bot_car.findCaronas,
                       pass_args=True, pass_user_data=True)
    )

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    main()