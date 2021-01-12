from environs import Env
from pytimeparse import parse

from ptbot import Bot
import pymorphy2


def render_progressbar(total, iteration, prefix='', suffix='', length=10, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = '{0:.1f}'
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(secs_left, bot, chat_id, message_id, seconds, matching_word):
    matched_word = matching_word.make_agree_with_number(secs_left).word
    current_progress = render_progressbar(seconds, secs_left)
    message = f'Осталось {secs_left} {matched_word}\n{current_progress}'
    bot.update_message(chat_id, message_id, message)
    if not secs_left:
        message = 'Время вышло'
        bot.send_message(chat_id, message)


def parse_message(message, bot, chat_id, matching_word):
    seconds = parse(message)
    if not seconds:
        bot.send_message(
            chat_id,
            'На сколько запустить таймер? (Примеры: 30s, 5m)')
        return
    matched_word = matching_word.make_agree_with_number(seconds).word
    message_id = bot.send_message(chat_id, f'Таймер запущен на {seconds} {matched_word}')
    bot.create_countdown(seconds, notify_progress, bot=bot, chat_id=chat_id, message_id=message_id, seconds=seconds, matching_word=matching_word)


def main():
    env = Env()
    env.read_env()
    bot_token = env('TG_BOT_TOKEN')
    chat_id = env.int('TG_CHAT_ID')
    bot = Bot(bot_token)
    bot.send_message(chat_id, 'Бот запущен!')
    morph = pymorphy2.MorphAnalyzer()
    matching_word = morph.parse('секунда')[0]
    bot.reply_on_message(parse_message, bot, chat_id, matching_word)
    bot.run_bot()


if __name__ == '__main__':
    main()
