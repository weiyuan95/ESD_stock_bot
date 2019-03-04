import requests
import csv
import time
from pprint import pprint

class StockBot:

    def __init__(self, api_token):

        self.base_url = f"https://api.telegram.org/bot{api_token}/"
        self.updates_url = f"{self.base_url}getUpdates"
        self.reply_url = f"{self.base_url}sendMessage"

        self.filename = "users.csv"
        self.highest_update_id = None
        self.first_run = True


    def serve_updates(self):

        if self.first_run:
            self.updates = requests.get(self.updates_url).json()["result"]

        else:
            payload = {
                        # the offset is the identifier of the first update to be returned: add 1 for next update
                        "offset": self.highest_update_id + 1,
                        "allowed_updates": ["message"],
                        "timeout": 10,
                        "disable_notification": True # disable notifications for now to avoid spam
                        }

            self.updates = requests.get(self.updates_url, params=payload).json()["result"]
       
        # print for dev purposes
        pprint(self.updates)

        if len(self.updates) > 0:
            # for the first update of the bot, we get the highest update id to offset future updates
            if self.first_run:
                self.highest_update_id = max(self.updates, key=lambda x: x["update_id"])["update_id"]

            self.parse_updates()

    def parse_updates(self):

        for update in self.updates:
            if not self.first_run:
                self.highest_update_id += 1

            message = update["message"]
            chat_id = message["chat"]["id"]
            # horribly inefficient since there is an I/O operation per msg, but whatever
            users = self.read_users()
            user_text = message["text"]

            if chat_id not in users and user_text == "/start":
                reply = "Thank you for using ESD Stock Bot.\n\nPlease input your trading portal username to link your telegram account to it."

            elif chat_id not in users:
                reply = "Thank you for registering. Please let us verify the username."
                self.reply_message(chat_id, reply)

                # TODO: check if the username is a valid one by calling some service (hosted on tibco)
                # for now, username is always valid
                reply = "Your username has been verified! You will now receive notifications."
                self.add_user(chat_id, user_text)

            elif chat_id in users:
                reply = "You have already registered for the notification service on this Telegram account.\n\n" \
                    "Please do not try to break the bot, thank you very much for trying though."


            self.reply_message(chat_id, reply)

        # after parsing updates for first run, change it to false
        if self.first_run:
            self.first_run = False
                

    def reply_message(self, chat_id, text):

        payload = {"chat_id": chat_id, "text": text}
        r = requests.get(self.reply_url, params=payload)
        return r.json()


    def read_users(self):
        """
        TODO:
        This function currently reads from a csv for testing.
        It should instead be calling a service (that hosts a db)
        to read the users that have registered for the notification service
        """

        with open(self.filename, newline="") as f:
            reader = csv.reader(f)
            # skip the header row of the csv file
            next(reader)
            # creates a dictionary of {chat_id: username, ...}
            return {int(row[0]): row[1] for row in reader}
            

    def add_user(self, user_id, chat_id):
        """
        TODO:
        This function currently writes to a csv for testing.
        It should instead be calling a service (that hosts a db)
        that checks if a username is valid, and then
        add the users that have registered for the notification service
        """

        with open(self.filename, "a", newline="") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow([user_id, chat_id])
            return True

        return False