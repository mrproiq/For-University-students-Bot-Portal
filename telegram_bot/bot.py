from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

import os
chat_id= os.getenv("CHAT_ID")
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from announcements.models import Announcement
from schedules.models import Schedule, Grade
from users.models import Student


def start_handler(update, context):
    buttons = [
        [
            KeyboardButton(text='Announcement'),
            KeyboardButton(text='Schedule'),
        ],
        [   KeyboardButton(text='Info'),
            KeyboardButton(text='Baholar'),
         ]
    ]
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text="Menu:",
        reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    )




def announcements_handler(update, context):
    message = update.message.text

    if message == "Announcement":
        announcements = Announcement.objects.all().order_by('-created_at')

        # Paginatsiya — har sahifada 1 ta e’lon
        paginator = Paginator(announcements, 1)
        page_number = context.user_data.get('announcement_page', 1)
        page = paginator.get_page(page_number)

        if page.object_list.exists():
            for announcement in page.object_list:
                text = f"{announcement.title}\n\n{announcement.message}"
                update.message.reply_text(text)

            # Agar keyingi sahifa bo'lsa, tugma chiqaramiz
            buttons = []
            if page.has_previous():
                buttons.append(
                    InlineKeyboardButton("⬅️ Oldingi", callback_data=f"announcement_page_{page_number-1}")
                )
            if page.has_next():
                buttons.append(
                    InlineKeyboardButton("Keyingi ➡️", callback_data=f"announcement_page_{page_number+1}")
                )

            if buttons:
                update.message.reply_text(
                    "Sahifani tanlang:",
                    reply_markup=InlineKeyboardMarkup([buttons])
                )
        else:
            update.message.reply_text("Hozircha e'lonlar yo'q.")

def announcement_pagination_handler(update, context):
    query = update.callback_query
    query.answer()

    # page raqamini olish
    page_number = int(query.data.split('_')[-1])
    context.user_data['announcement_page'] = page_number

    announcements = Announcement.objects.all().order_by('-created_at')
    paginator = Paginator(announcements, 1)
    page = paginator.get_page(page_number)

    text = ""
    for announcement in page.object_list:
        text += f"{announcement.title}\n\n{announcement.message}\n\n"

    buttons = []
    if page.has_previous():
        buttons.append(
            InlineKeyboardButton("⬅️ Oldingi", callback_data=f"announcement_page_{page_number-1}")
        )
    if page.has_next():
        buttons.append(
            InlineKeyboardButton("Keyingi ➡️", callback_data=f"announcement_page_{page_number+1}")
        )

    query.edit_message_text(
        text=text or "E'lonlar yo'q",
        reply_markup=InlineKeyboardMarkup([buttons]) if buttons else None
    )


def schedule_handler(update, context):
    message = update.message.text

    if message == "Schedule":
        days = [
            ('monday', 'Monday'),
            ('tuesday', 'Tuesday'),
            ('wednesday', 'Wednesday'),
            ('thursday', 'Thursday'),
            ('friday', 'Friday'),
            ('saturday', 'Saturday'),
        ]

        buttons = []

        for day_code, day_name in days:
            buttons.append([InlineKeyboardButton(text=day_name, callback_data=f"day_{day_code}")])

        update.message.reply_text(
            "Hafta kunini tanlang:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

def schedule_day_handler(update, context):
    query = update.callback_query
    query.answer()

    day_code = query.data.replace("day_", "")
    schedules = Schedule.objects.filter(week_day=day_code).select_related("subject", "teacher")

    if schedules.exists():
        text = f"{day_code.capitalize()} dars jadvali:\n\n"
        for schedule in schedules:
            if schedule.teacher:
                teacher_name = f"{schedule.teacher.user.first_name} {schedule.teacher.user.last_name}"
            else:
                teacher_name = "O'qituvchi yo'q"

            text += f"{schedule.start_time.strftime('%H:%M')} - {schedule.end_time.strftime('%H:%M')}: {schedule.subject.name} ({teacher_name})\n"
        query.edit_message_text(text)
    else:
        query.edit_message_text("Bu kunga darslar topilmadi.")


def my_info(update, context):
    message = update.message.text
    if message == "Info":
        chat_id = update.effective_user.id
        try:
            student = Student.objects.select_related('user', 'group', 'faculty').get(telegram_id=chat_id)
            text = (
                f"ID: {student.telegram_id}\n"
                f"IF: {student.user.first_name} {student.user.last_name}\n"
                f"Fakultet: {student.faculty.name if student.faculty else 'Yo‘q'}\n"
                f"Guruh: {student.group.name if student.group else 'Yo‘q'}\n"
                f"Kurs: {student.get_level_display()}\n"
                f"Tel: {student.phone_number}"
            )
        except ObjectDoesNotExist:
            text = "Siz ro'yxatdan o'tmagansiz"

        update.message.reply_text(text)

def my_grades(update, context):
    message = update.message.text
    if message == "Baholar":
        chat_id = update.effective_user.id
        try:
            student = Student.objects.get(telegram_id=chat_id)
            grades = Grade.objects.filter(student=student).select_related('subject')

            if grades.exists():
                text = "Sizning baholaringiz:\n\n"
                for grade in grades:
                    text += f"{grade.subject.name}: {grade.score}\n"
            else:
                text = "Siz hali baholanmagansiz."
        except ObjectDoesNotExist:
            text = "Siz ro‘yxatdan o‘tmagansiz!"

        update.message.reply_text(text)





def main():
    bot_token = os.getenv("BOT_TOKEN")
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(MessageHandler(Filters.regex("^Info$"), my_info))
    dispatcher.add_handler(MessageHandler(Filters.regex("^Baholar$"), my_grades))
    dispatcher.add_handler(MessageHandler(Filters.text("Schedule"), schedule_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, announcements_handler))
    dispatcher.add_handler(CallbackQueryHandler(announcement_pagination_handler, pattern="^announcement_page_"))

    dispatcher.add_handler(CallbackQueryHandler(schedule_day_handler, pattern="^day_"))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()