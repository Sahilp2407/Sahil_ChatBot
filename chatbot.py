from typing import List, Optional, Union
import asyncio
import random
from datetime import datetime
from wechaty import (
    MessageType, FileBox, RoomMemberQueryFilter, Wechaty, Contact, Room, Message, Image, MiniProgram
)

class CrazyBot(Wechaty):
    def __init__(self) -> None:
        super().__init__()
        self.login_user: Optional[Contact] = None
        self.roasts = [
            "Bro, even Google can't find your relevance!", 
            "You're so slow, even a snail overtook you in a race!", 
            "Your WiFi signal is stronger than your personality."
        ]
        self.rap_bars = [
            "Aye, I'm the king of the city, call me Baadshah!",
            "Street flow, Mumbai vibe, takin' over the game, no lie!",
            "Duniya ki soch choti, apna vision bada!"
        ]
        self.mumbai_slang = [
            "Kya re, tu full scene bana raha hai!", 
            "Ekdum zakkas, bhai!", 
            "Aye chhoti, kaisa hai re tu?"
        ]
    
    async def on_message(self, msg: Message) -> None:
        text = msg.text()
        from_contact = msg.talker()
        room = msg.room()
        
        if text.lower() == "roast me":
            await msg.say(random.choice(self.roasts))
        
        elif text.lower() == "rap battle":
            await msg.say(random.choice(self.rap_bars))
        
        elif text.lower() == "hey babe":
            await msg.say("Hey you! 😘 What’s up, handsome?")
        
        elif text.lower() == "send meme":
            meme = FileBox.from_url(
                "https://i.imgur.com/funny-meme.jpg", name="meme.jpg"
            )
            await msg.say(meme)
        
        elif text.lower() == "talk like a mumbaikar":
            await msg.say(random.choice(self.mumbai_slang))
        
        elif text.lower().startswith("bet"):
            amount = int(text.split()[1]) if len(text.split()) > 1 else 100
            result = random.choice(["win", "lose"])
            await msg.say(f"You {result} {amount * 2} coins! 💰" if result == "win" else f"You lost {amount} coins. 😭")
        
        elif text.lower() == "call me":
            call_img = FileBox.from_url(
                "https://i.imgur.com/fake-call.jpg", name="call.jpg"
            )
            await msg.say("Incoming call... ☎️")
            await msg.say(call_img)
        
        elif text.lower() == "who my real friends?" and room:
            members = await room.member_list()
            real_friends = random.sample(members, min(3, len(members)))
            real_friend_names = ", ".join([member.name for member in real_friends])
            await msg.say(f"Your real friends: {real_friend_names}")
        
        elif text.lower() == "time bomb" and room:
            await msg.say("You have 10 seconds to reply or get kicked! ⏳💣")
        
        elif datetime.now().hour == 3:  # Ghost mode at 3 AM
            await msg.say("👻 Boo! Someone is watching you... 😱")
    
    async def on_login(self, contact: Contact) -> None:
        self.login_user = contact
        await self.say(f"{contact.name} is now online! 🚀")
    
    async def on_room_join(self, room: Room, invitees: List[Contact], inviter: Contact, date: datetime) -> None:
        names = ", ".join([invitee.name for invitee in invitees])
        await room.say(f"Welcome {names} to the craziest WeChat group! 🎉")

    async def on_friendship(self, friendship) -> None:
        if friendship.type() == friendship.Type.RECEIVE:
            if "wechaty" in friendship.hello().lower():
                await friendship.accept()
        elif friendship.type() == friendship.Type.CONFIRM:
            contact = friendship.contact()
            await self.say(f"{contact.name} is now your friend! 🤝")

async def main():
    bot = CrazyBot()
    await bot.start()

asyncio.run(main())