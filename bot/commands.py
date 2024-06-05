from .functions import auth, keyword

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
        """
        Adds a new keyword for a specific user
        """
        # TODO: A USER SHOULD BE ABLE TO ADD MULTIPLE KEYWORDS SEPERATED BY A COMMA
        chat_id = message.chat.id
        
        bot.reply_to(message, "Please enter a keyword:")
        bot.register_next_step_handler(message, key_word_input, chat_id)
       

    def key_word_input(message, user_id):
        """
        Handles the keyword input
        """
        if verify_text_input(bot, message):
            keyword_text = message.text
            response = keyword.create_keyword(user_id, keyword_text)

            bot.reply_to(message, response)
        else:
            bot.register_next_step_handler(message, key_word_input, user_id)
        
 




    @bot.message_handler(commands=['list_keywords'])
    def handle_list_keywords(message):
        """
        Gets all of the keywords of a specific user
        """
        chat_id = message.chat.id
        keywords = keyword.get_keywords(chat_id)
        if keywords:
            keywords_text = "\n".join([f"{keyword.id}: {keyword.keyword}" for keyword in keywords])
            bot.reply_to(message, f"Your keywords:\n{keywords_text}")
        else:
            bot.reply_to(message, "You have no keywords.")
        
  
    @bot.message_handler(commands=['update_keyword'])
    def handle_update_keyword(message):
        """
        Handles updating/editing a specific keyword
        """
        # TODO: DISPLAY ALL KEYWORDS


        old_keyword_text = message.text
        
        bot.reply_to(message, "Please enter a new keyword:")
        bot.register_next_step_handler(message, update_new_keyword_input, old_keyword_text)

    def update_new_keyword_input(message, old_keyword_text):
        new_keyword_text = message.text
        response = keyword.update_keyword(old_keyword_text, new_keyword_text)

        if response:
            bot.reply_to(message, response)
        else:
            bot.reply_to(message, "Keyword not found.")




    @bot.message_handler(commands=['delete_keyword'])
    def handle_delete_keyword(message):
        """
        Handles deleting a keyword
        """
        # TODO: THERE SHOULD BE A VERIFICATION STEP BEFORE PROCEEDING ("Are you sure you want to delete this keyword?")
       
        response =  keyword.delete_keyword(message.text)
        if response :
            bot.reply_to(message, "Keyword deleted successfully!")
        else:
            bot.reply_to(message, "Keyword not found.")


    
