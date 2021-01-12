from environs import Env
from pytimeparse import parse

from ptbot import Bot


def render_progressbar(total, iteration, prefix='', suffix='', length=10, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = '{0:.1f}'
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_user(bot, chat_id, message):
    bot.send_message(chat_id, message)


def notify_progress(secs_left, bot, chat_id, message_id, seconds):
    current_progress = render_progressbar(seconds, secs_left)
    message = f'Осталось {secs_left} секунд\n{current_progress}'
    bot.update_message(chat_id, message_id, message)


def parse_message(message, bot, chat_id, is_over_message):
    seconds = parse(message)
    if not seconds:
        bot.send_message(
            chat_id,
            'На сколько запустить таймер? (Примеры: 30s, 5m)')
        return
    message_id = bot.send_message(chat_id, f'Таймер запущен на {seconds} секунд')
    bot.create_countdown(seconds, notify_progress, bot=bot, chat_id=chat_id, message_id=message_id, seconds=seconds)
    bot.create_timer(seconds, notify_user, bot, chat_id, is_over_message)


def main():
    env = Env()
    env.read_env()
    bot_token = env('TG_BOT_TOKEN')
    chat_id = env('TG_CHAT_ID')
    is_over_message = 'Время вышло'
    bot = Bot(bot_token)
    bot.send_message(chat_id, 'Бот запущен!')
    bot.send_message(chat_id, 'На сколько запустить таймер?')
    bot.reply_on_message(parse_message, bot, chat_id, is_over_message)
    bot.run_bot()


if __name__ == '__main__':
    main()
