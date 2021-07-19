#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from telegram.ext import Dispatcher, CommandHandler

from utils.callback import callback_delete_message
from utils.config_loader import config
from utils.restricted import restricted

logger = logging.getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler('start', start))


@restricted
def start(update, context):
    rsp = update.message.reply_text('🔺 আপনার সার্ভিস একাউন্ট (SA) গুলো জিপ করে জিপ ফাইলটি প্রদান করুন এবং আপলোড করার সময় সাবজেক্ট এ /sa লিখে দিন\n'
                                    '📂 এরপর আপনার আপলোড ফোল্ডার সেট করুন, /folders কমান্ডের মাধ্যমে\n'
                                    '🔗 সব কনফিগার করা হলে শুধু গুগল ড্রাইভ লিংক সেন্ড/ ফরোওয়ার্ড করলেই ফাইল ক্লোন করা যাবে.')
    rsp.done.wait(timeout=60)
    message_id = rsp.result().message_id
    if update.message.chat_id < 0:
        context.job_queue.run_once(callback_delete_message, config.TIMER_TO_DELETE_MESSAGE,
                                   context=(update.message.chat_id, message_id))
        context.job_queue.run_once(callback_delete_message, config.TIMER_TO_DELETE_MESSAGE,
                                   context=(update.message.chat_id, update.message.message_id))
