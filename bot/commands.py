from .functions import auth, keyword, group, channel
from telebot import types

def verify_text_input(bot, message):
    if message.text and len(message.text) > 1: 
        return True
    bot.reply_to(message, "Please enter a valid input (min: 2 characters):")
    return False

# Define bot commands
def register_commands(bot):
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        start_text = """
        Welcome to the Job Scraping Bot! \nSelect an option below:
        """
        # TODO: WHEN THIS BUTTON IS INITIALIZED, THE COMMAND BUTTONS (Keywords, Jobs, Resume review)
        markup = types.ReplyKeyboardMarkup()


        startbtn1 = types.KeyboardButton('🔑 Keywords')
        startbtn2 = types.KeyboardButton('💼 Jobs')
        startbtn3 = types.KeyboardButton('👥 Groups')
        startbtn4 = types.KeyboardButton('📺 Channels')
        startbtn5 = types.KeyboardButton('📝 Resume review(coming soon...)')
        
        markup.row(startbtn1, startbtn2)
        markup.row(startbtn3, startbtn4)
        markup.row(startbtn5)



        bot.reply_to(message, start_text, reply_markup=markup)

    
    # KEYWORD SECTION
    @bot.message_handler(func=lambda message: message.text == "🔑 Keywords")
    def handle_keywords(message):
        markup = types.ReplyKeyboardMarkup()

        go_back = types.KeyboardButton("⬅️ Go back") #TODO
        btn1 = types.KeyboardButton('➕ Add keyword')
        btn2 = types.KeyboardButton('👀 List keywords')
        btn3 = types.KeyboardButton('🖋 Update keyword')
        btn4 = types.KeyboardButton("🗑 Delete keyword")

        markup.row(go_back)
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.reply_to(message, "Manage keywords:", reply_markup=markup)

    

    @bot.message_handler(func=lambda message: message.text == "➕ Add keyword")
    def handle_add_keyword(message):
        user_id = message.chat.id
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.reply_to(message, "Please enter keywords separated by commas:", reply_markup=markup)
        bot.register_next_step_handler(message, keywords_input, user_id)

    def keywords_input(message, user_id):
        if verify_text_input(bot, message):
            keyword_texts = [kw.strip() for kw in message.text.split(",")]
            responses = [keyword.create_keyword(user_id, kw) for kw in keyword_texts]
            response_message = "\n".join(responses)
            bot.reply_to(message, response_message)
        else:
            bot.register_next_step_handler(message, keywords_input, user_id)

    @bot.message_handler(func=lambda message: message.text == '👀 List keywords')
    def handle_list_keywords(message):
        user_id = message.chat.id
        keywords = keyword.get_keywords(user_id)
        if keywords:
            keywords_text = "\n".join([f"{keyword.id}: {keyword.keyword}" for keyword in keywords])
            bot.reply_to(message, f"Your keywords:\n{keywords_text}")
        else:
            bot.reply_to(message, "You have no keywords.")

    @bot.message_handler(func=lambda message: message.text == '🖋 Update keyword')
    def handle_update_keyword(message):
        user_id = message.chat.id
        keywords = keyword.get_keywords(user_id)
        if keywords:
            keywords_text = "\n".join([f"{keyword.id}: {keyword.keyword}" for keyword in keywords])
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.reply_to(message, f"Your keywords:\n{keywords_text}\n\nEnter the keyword you want to update:", reply_markup=markup)
            bot.register_next_step_handler(message, update_old_keyword_input)
        else:
            bot.reply_to(message, "You have no keywords to update.")

    def update_old_keyword_input(message):
        old_keyword_text = message.text
        bot.reply_to(message, "Please enter the new keyword:")
        bot.register_next_step_handler(message, update_new_keyword_input, old_keyword_text)

    def update_new_keyword_input(message, old_keyword_text):
        new_keyword_text = message.text
        response = keyword.update_keyword(old_keyword_text, new_keyword_text)
        bot.reply_to(message, response if response else "Keyword not found.")

    @bot.message_handler(func=lambda message: message.text == '🗑 Delete keyword')
    def handle_delete_keyword(message):
        user_id = message.chat.id
        keywords = keyword.get_keywords(user_id)
        if keywords:
            keywords_text = "\n".join([f"{keyword.id}: {keyword.keyword}" for keyword in keywords])
            markup = types.ReplyKeyboardRemove(selective=False)

            bot.reply_to(message, f"Your keywords:\n{keywords_text}\n\nEnter the keyword ID you want to delete:", reply_markup=markup)
            bot.register_next_step_handler(message, delete_keyword_confirmation)
        else:
            bot.reply_to(message, "You have no keywords to delete.")

    def delete_keyword_confirmation(message):
        keyword_id = message.text
        markup = types.ReplyKeyboardMarkup(row_width=2)
        btn1 = types.KeyboardButton('Yes')
        btn2 = types.KeyboardButton('No')


        markup.add(btn1, btn2)
        bot.reply_to(message, f"Are you sure you want to delete keyword ID {keyword_id}?", reply_markup=markup)
        bot.register_next_step_handler(message, delete_keyword, keyword_id)

    def delete_keyword(message, keyword_id):
        markup = types.ReplyKeyboardRemove(selective=False)

        if message.text.lower() == 'yes':
            response = keyword.delete_keyword(keyword_id)
            bot.reply_to(message, f"Keyword deleted successfully!" if response else "Keyword not found.", reply_markup=markup)
        else:
            bot.reply_to(message, "Keyword deletion canceled.", reply_markup=markup)

    # JOBS SECTION
    @bot.message_handler(func=lambda message: message.text == "💼 Jobs")
    def handle_jobs(message):
        markup = types.ReplyKeyboardMarkup()
        go_back = types.KeyboardButton("⬅️ Go back") 
        # btn1 = types.KeyboardButton('Search jobs')
        btn2 = types.KeyboardButton('🎒 Saved jobs')
        btn3 = types.KeyboardButton('📝 Applied jobs')

        markup.row(go_back)
        markup.row(btn2, btn3)
        bot.reply_to(message, "Manage jobs:", reply_markup=markup)
    
    

    # GROUPS SECTION
    @bot.message_handler(func=lambda message: message.text == "👥 Groups")
    def handle_groups(message):
        markup = types.ReplyKeyboardMarkup()
        go_back = types.KeyboardButton("⬅️ Go back") 
        btn1 = types.KeyboardButton('➕ Add group')
        btn2 = types.KeyboardButton('👀 List groups')
        btn3 = types.KeyboardButton('🖋 Update group')
        btn4 = types.KeyboardButton("🗑 Delete group")
        markup.row(go_back)
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)  
        bot.reply_to(message, "Manage groups:", reply_markup=markup)

    @bot.message_handler(func=lambda message: message.text == "➕ Add group")
    def handle_add_group(message):
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.reply_to(message, "Please enter the group ID:", reply_markup=markup)
        bot.register_next_step_handler(message, save_group_id)

    def save_group_id(message):
        pass



    # CHANNELS SECTION
    @bot.message_handler(func=lambda message: message.text == "📺 Channels")
    def handle_channels(message):
        markup = types.ReplyKeyboardMarkup()
        go_back = types.KeyboardButton("⬅️ Go back") 
        btn1 = types.KeyboardButton('➕ Add channel')
        btn2 = types.KeyboardButton('👀 List channels')
        btn3 = types.KeyboardButton('🖋 Update channel')
        btn4 = types.KeyboardButton("🗑 Delete channel")
        markup.row(go_back)
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)  
        bot.reply_to(message, "Manage channels:", reply_markup=markup)


    
    @bot.message_handler(func=lambda message: message.text == '➕ Add channel')
    def handle_add_channel(message):
        user_id = message.chat.id
        print("user id", message)
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.reply_to(message, "Please enter channel username/ID:", reply_markup=markup)
        bot.register_next_step_handler(message, channels_input, user_id)

    def channels_input(message, user_id):
        if verify_text_input(bot, message):
            channel_id = message.text

            if message.text[:12] == "https://t.me":
                channel_id = message.text[13:]
            elif message.text[:1] == "@":
                channel_id = message.text[1:]
            
            response = channel.create_channel(user_id, channel_id)
            bot.reply_to(message, response)
        else:
            bot.register_next_step_handler(message, channels_input, user_id)


    @bot.message_handler(func=lambda message: message.text == '👀 List channels')
    def handle_list_channels(message):
        user_id = message.chat.id
        channels = channel.get_channels(user_id)
        if channels:
            channels_id = "\n".join([f"{channel.id}: {channel.channel_id}" for channel in channels])
            bot.reply_to(message, f"Your channels:\n{channels_id}")
        else:
            bot.reply_to(message, "You have no channels.")


    @bot.message_handler(func=lambda message: message.text == '🖋 Update channel')
    def handle_update_channel(message):
        user_id = message.chat.id
        channels = channel.get_channels(user_id)
        if channels:
            chanels_id = "\n".join([f"{channel.id}: {channel.channel_id}" for channel in channels])
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.reply_to(message, f"Your channels:\n{chanels_id}\n\nEnter the channel you want to update:", reply_markup=markup)
            bot.register_next_step_handler(message, update_old_channel_id)
        else:
            bot.reply_to(message, "You have no channels to update.")

    def update_old_channel_id(message):
        old_keyword_text = message.text
        bot.reply_to(message, "Please enter the new channel username/id:")
        bot.register_next_step_handler(message, update_new_channel_id, old_keyword_text)

    def update_new_channel_id(message, old_keyword_text):
        new_keyword_text = message.text
        response = channel.update_channel(old_keyword_text, new_keyword_text)
        bot.reply_to(message, response if response else "Channel not found.")



    @bot.message_handler(func=lambda message: message.text == '🗑 Delete channel')
    def handle_delete_channel(message):
        user_id = message.chat.id
        channels = channel.get_channels(user_id)
        if channels:
            channels_id = "\n".join([f"{channel.id}: {channel.channel_id}" for channel in channels])
            markup = types.ReplyKeyboardRemove(selective=False)

            bot.reply_to(message, f"Your channels:\n{channels_id}\n\nEnter the Channel ID you want to delete:", reply_markup=markup)
            bot.register_next_step_handler(message, delete_channel_confirmation)
        else:
            bot.reply_to(message, "You have no channels to delete.")

    def delete_channel_confirmation(message):
        id = message.text
        markup = types.ReplyKeyboardMarkup(row_width=2)
        btn1 = types.KeyboardButton('Yes')
        btn2 = types.KeyboardButton('No')


        markup.add(btn1, btn2)
        bot.reply_to(message, f"Are you sure you want to delete channel ID - {id}?", reply_markup=markup)
        bot.register_next_step_handler(message, delete_channel, id)

    def delete_channel(message, id):
        markup = types.ReplyKeyboardRemove(selective=False)

        if message.text.lower() == 'yes':
            response = channel.delete_channel(id)
            bot.reply_to(message, f"Channel deleted successfully!" if response else "Channel not found.", reply_markup=markup)
        else:
            bot.reply_to(message, "Channel deletion canceled.", reply_markup=markup)


    


    # RESUME REVIEW SECTION
    @bot.message_handler(func=lambda message: message.text == "📝 Resume review(coming soon...)")
    def handle_resume_review(message):
        bot.reply_to(message, "Resume review is coming soon! Stay tuned for updates.")

    # GO BACK FUNCTION
    @bot.message_handler(func=lambda message: message.text == "⬅️ Go back")
    def handle_go_back(message):
        handle_start(message)

    # INVALID PROMPT
    @bot.message_handler(func=lambda m: True)
    def invalid_prompt(message):
        bot.reply_to(message, "Please use one of the buttons below to proceed.")

