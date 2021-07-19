#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from telegram.ext import Dispatcher, CommandHandler

from utils.config_loader import config
from utils.callback import callback_delete_message
from utils.restricted import restricted

logger = logging.getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler('help', get_help))


@restricted
def get_help(update, context):
    message = 'ফাইল ক্লোন করার জন্য গুগল ড্রাইভ লিংক প্রেরণ করুন অথবা গুগল ড্রাইভ লিংক সহ মেসেজ ফোরওয়ার্ড করুন .\n' \
              '**সার্ভিস একাউন্ট ও ড্রাইভ/ফোল্ডার কনফিগার করা থাকতে হবে.\n\n' \
              '📚 কমান্ডসমূহ:\n' \
              ' │ /folders - নতুন ড্রাইভ/ফোল্ডার যোগ করার জন্য\n' \
              ' │ /sa - বট ইনবক্সে , সার্ভিস একাউন্টের জিপ ফাইল আপলোড করে এই কমান্ড ঐ ফাইলে রিপ্লে করুন.\n' \
              ' │ /help - এই কমান্ড গাইড দেখতে\n'
              ' │ /ban - কোন নির্দিষ্ট ব্যবহারকারীকে ব্লকলিস্টে যোগ করতে\n'
              ' │ /unban - কোন নির্দিষ্ট ব্যবহারকারীকে ব্লকলিস্টে বাদ দিতে\n'
    rsp = update.message.reply_text(message)
    rsp.done.wait(timeout=60)
    message_id = rsp.result().message_id
    if update.message.chat_id < 0:
        context.job_queue.run_once(callback_delete_message, config.TIMER_TO_DELETE_MESSAGE,
                                   context=(update.message.chat_id, message_id))
        context.job_queue.run_once(callback_delete_message, config.TIMER_TO_DELETE_MESSAGE,
                                   context=(update.message.chat_id, update.message.message_id))
