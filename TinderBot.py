import telebot
from telebot import types

# Reemplaza 'YOUR_API_KEY' con tu clave API de Telegram
bot = telebot.TeleBot('6436706147:AAEKXSWQIeoCQI_xoK8wCaYhMlgihzjjrp8')

# Diccionario para almacenar perfiles de usuarios
user_profiles = {}

# Comando de inicio
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "¡Bienvenido a TinderBot! Crea tu perfil con /profile")

# Comando para crear perfil
@bot.message_handler(commands=['profile'])
def create_profile(message):
    bot.send_message(message.chat.id, "Por favor, envíame tu nombre:")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.from_user.id
    user_profiles[user_id] = {'name': message.text}
    bot.send_message(message.chat.id, "¿Cuál es tu edad?")
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    user_id = message.from_user.id
    user_profiles[user_id]['age'] = message.text
    bot.send_message(message.chat.id, "Describe brevemente tus intereses:")
    bot.register_next_step_handler(message, get_interests)

def get_interests(message):
    user_id = message.from_user.id
    user_profiles[user_id]['interests'] = message.text
    bot.send_message(message.chat.id, "¡Perfil creado exitosamente! Puedes buscar coincidencias con /find_match")

# Comando para buscar coincidencias
@bot.message_handler(commands=['find_match'])
def find_match(message):
    user_id = message.from_user.id
    if user_id not in user_profiles:
        bot.send_message(message.chat.id, "Primero debes crear tu perfil con /profile")
        return

    for other_user_id, profile in user_profiles.items():
        if other_user_id != user_id:
            markup = types.InlineKeyboardMarkup()
            like_button = types.InlineKeyboardButton("👍", callback_data=f'like_{other_user_id}')
            dislike_button = types.InlineKeyboardButton("👎", callback_data=f'dislike_{other_user_id}')
            markup.add(like_button, dislike_button)
            bot.send_message(
                message.chat.id,
                f"Nombre: {profile['name']}\nEdad: {profile['age']}\nIntereses: {profile['interests']}",
                reply_markup=markup
            )

# Manejo de botones de 'me gusta' o 'no me gusta'
@bot.callback_query_handler(func=lambda call: call.data.startswith('like_') or call.data.startswith('dislike_'))
def handle_like_dislike(call):
    action, other_user_id = call.data.split('_')
    user_id = call.from_user.id

    if action == 'like':
        bot.answer_callback_query(call.id, "¡Has dado un 'me gusta'!")
        # Aquí puedes agregar lógica para ver si es una coincidencia mutua
    elif action == 'dislike':
        bot.answer_callback_query(call.id, "Has dado un 'no me gusta'.")

# Inicia el bot
bot.polling()
