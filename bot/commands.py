from .functions import auth, keyword

# Define bot commands
def register_commands(bot):
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        start_text = """
        Welcome to the Job Scraping Bot!

        /help - Show available commands and usage information

        """
        bot.reply_to(message, start_text)

    @bot.message_handler(commands=['help'])
    def handle_help(message):
        help_text = """
        Available commands:
        /help - Show available commands
        /addkeyword - Set or update keywords for job filtering
        /searchjobs - Manually search for jobs using the set keywords
        /applyall - Automatically apply to all jobs that match the set keywords
        /savedjobs - View the list of saved jobs for later review or application
        /appliedjobs - View the list of jobs the user has applied to
        /listsources - View the current list of job sources (websites, Telegram channels, groups)
        /addsource - Add a new job source (website, Telegram channel, group)
        /removesource - Remove an existing job source from the list
        /setnotifications - Set preferences for job notifications (e.g., frequency, types of jobs)
        /analyzemyresume - Submit a resume for AI analysis and keyword suggestions
        /subscribe - Subscribe to the bot’s services after the free trial
        /status - Check the current subscription status
        /cancel - Cancel the current subscription



        For assistance, contact support or visit our website.
        """
        bot.reply_to(message, help_text)


    # @bot.message_handler(commands=["register"])
    # def handle_register(message):
    #     chat_id = message.chat.id
    #     print("Chat Id", chat_id)
    #     username = message.from_user.username
    #     if username is None:
    #         bot.reply_to(message, "Please set a username in your Telegram settings.")
    #         return

    #     bot.reply_to(message, "Please enter a password:")
    #     bot.register_next_step_handler(message, register_password, username)
        
    # def register_password(message, username):
    #     password = message.text
    #     response = auth.register_user(username, password)
    #     bot.reply_to(message, "Registration successful!" if response else "User already exists")

    # @bot.message_handler(commands=["login"])
    # def handle_login(message):
    #     chat_id = message.chat.id
    #     username = message.from_user.username
    #     if username is None:
    #         bot.reply_to(message, "Please set a username in your Telegram settings.")
    #         return
    #     bot.reply_to(message, "Please enter your password:")
    #     bot.register_next_step_handler(message, login_password, username)

    # def login_password(message, username):
    #     password = message.text
    #     response =  auth.authenticate_user(username, password)

    #     bot.reply_to(message, "Login successful!" if response else "Invalid username or password")
        
        

    @bot.message_handler(commands=['addkeyword'])
    def handle_add_keyword(message):
            chat_id = message.chat.id
           
            bot.reply_to(message, "Please enter a keyword:")
            bot.register_next_step_handler(message, key_word_input, chat_id)
       

    def key_word_input(message, user_id):
        keyword_text = message.text
        response = keyword.create_keyword(user_id, keyword_text)

        bot.reply_to(message, response)




    @bot.message_handler(commands=['list_keywords'])
    def handle_list_keywords(message):
        token = message.text.split(" ", 1)[1] if len(message.text.split(" ")) > 1 else None
        if token:
            user = get_user_by_token(token)
            if user:
                keywords = keyword.get_keywords(user.id)
                if keywords:
                    keywords_text = "\n".join([f"{keyword.id}: {keyword.keyword}" for keyword in keywords])
                    bot.reply_to(message, f"Your keywords:\n{keywords_text}")
                else:
                    bot.reply_to(message, "You have no keywords.")
            else:
                bot.reply_to(message, "Invalid session token.")
        else:
            bot.reply_to(message, "Please provide a session token.")

    @bot.message_handler(commands=['update_keyword'])
    def handle_update_keyword(message):
        token = message.text.split(" ", 1)[1] if len(message.text.split(" ")) > 1 else None
        if token:
            user = get_user_by_token(token)
            if user:
                parts = message.text.split(" ", 3)
                if len(parts) >= 4:
                    keyword_id = parts[2]
                    new_keyword_text = parts[3]
                    if keyword.update_keyword(keyword_id, new_keyword_text):
                        bot.reply_to(message, f"Keyword updated to '{new_keyword_text}'!")
                    else:
                        bot.reply_to(message, "Keyword not found.")
                else:
                    bot.reply_to(message, "Please provide keyword ID and new keyword text.")
            else:
                bot.reply_to(message, "Invalid session token.")
        else:
            bot.reply_to(message, "Please provide a session token.")

    @bot.message_handler(commands=['delete_keyword'])
    def handle_delete_keyword(message):
        token = message.text.split(" ", 1)[1] if len(message.text.split(" ")) > 1 else None
        if token:
            user = get_user_by_token(token)
            if user:
                keyword_id = message.text.split(" ", 2)[2] if len(message.text.split(" ")) > 2 else None
                if keyword_id and keyword.delete_keyword(keyword_id):
                    bot.reply_to(message, "Keyword deleted successfully!")
                else:
                    bot.reply_to(message, "Keyword not found.")
            else:
                bot.reply_to(message, "Invalid session token.")
        else:
            bot.reply_to(message, "Please provide a session token.")


    
