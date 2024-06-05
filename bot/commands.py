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
        # TODO: WHEN THIS BUTTON IS INITIALIZED, THE COMMAND BUTTONS (Keywords, Jobs, Resume review)

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

  
    @bot.message_handler(commands=['addkeyword'])
    def handle_add_keyword(message):
        chat_id = message.chat.id
        bot.reply_to(message, "Please enter keywords separated by commas:")
        bot.register_next_step_handler(message, keywords_input, chat_id)

    def keywords_input(message, user_id):
        if verify_text_input(bot, message):
            keyword_texts = [kw.strip() for kw in message.text.split(",")]
            responses = [keyword.create_keyword(user_id, kw) for kw in keyword_texts]
            response_message = "\n".join(responses)
            bot.reply_to(message, response_message)
        else:
            bot.register_next_step_handler(message, keywords_input, user_id)

    @bot.message_handler(commands=['list_keywords'])
    def handle_list_keywords(message):
        chat_id = message.chat.id
        keywords = keyword.get_keywords(chat_id)
        if keywords:
            keywords_text = "\n".join([f"{keyword.id}: {keyword.keyword}" for keyword in keywords])
            bot.reply_to(message, f"Your keywords:\n{keywords_text}")
        else:
            bot.reply_to(message, "You have no keywords.")

    @bot.message_handler(commands=['update_keyword'])
    def handle_update_keyword(message):
        chat_id = message.chat.id
        keywords = keyword.get_keywords(chat_id)
        if keywords:
            keywords_text = "\n".join([f"{keyword.id}: {keyword.keyword}" for keyword in keywords])
            bot.reply_to(message, f"Your keywords:\n{keywords_text}\n\nEnter the keyword you want to update:")
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

    @bot.message_handler(commands=['delete_keyword'])
    def handle_delete_keyword(message):
        chat_id = message.chat.id
        keywords = keyword.get_keywords(chat_id)
        if keywords:
            keywords_text = "\n".join([f"{keyword.id}: {keyword.keyword}" for keyword in keywords])
            bot.reply_to(message, f"Your keywords:\n{keywords_text}\n\nEnter the keyword ID you want to delete:")
            bot.register_next_step_handler(message, delete_keyword_confirmation)
        else:
            bot.reply_to(message, "You have no keywords to delete.")

    def delete_keyword_confirmation(message):
        keyword_id = message.text
        bot.reply_to(message, f"Are you sure you want to delete keyword ID {keyword_id}? (yes/no)")
        bot.register_next_step_handler(message, delete_keyword, keyword_id)

    def delete_keyword(message, keyword_id):
        if message.text.lower() == 'yes':
            response = keyword.delete_keyword(keyword_id)
            bot.reply_to(message, "Keyword deleted successfully!" if response else "Keyword not found.")
        else:
            bot.reply_to(message, "Keyword deletion canceled.")

    
    @bot.message_handler(func=lambda m: True)
    def invalid_prompt(message):
        bot.reply_to(message, "Please use one of the buttons below to proceed.")

