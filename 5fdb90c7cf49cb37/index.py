from pydoc import cli
from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption
from function import function 
from os import system
import discord, asyncio 

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event 
async def on_ready():
    system('cls')
    print("READY")
    DiscordComponents(client)

@client.event
async def on_message(message):
    if message.author.bot:
        return False
    
    color_data = {
        'pink': discord.utils.get(message.guild.roles, name="핑크"),
        'mint': discord.utils.get(message.guild.roles, name="민트"),
        'yellow': discord.utils.get(message.guild.roles, name="노랑"),
        'purple': discord.utils.get(message.guild.roles, name="보랑"),
        'orange': discord.utils.get(message.guild.roles, name="주황"),
        'red': discord.utils.get(message.guild.roles, name="빨강")
    }

    if message.content.startswith("!데이터생성"):
        if message.channel.id != 975737700311253035: #수정필요
            return None
        sql, woogi = function.join_sql()
        if sql:
            woogi.execute(f"SELECT * FROM user_info WHERE user_id = {message.author.id}")
            sql.commit()
            result = woogi.fetchone()
            if result is None:
                woogi.execute(f"INSERT INTO user_info (user_id, user_name, point, daily, daily_check) values({message.author.id}, '{message.author.name}', {0}, {0}, {0})")
                sql.commit()
                sql.close()
                embed=discord.Embed(title=f"데이터 생성이 완료되었습니다")
                embed.add_field(name="보유 포인트", value=f"```0원```", inline=True)
                embed.add_field(name="출석일수", value=f"```0일```", inline=True)
                await message.reply(embed=embed)
            else:
                return await message.reply("> 데이터가 이미 존재합니다")
    elif message.content.startswith("!출석"):
        if message.channel.id != 975737700311253035: #수정필요
            return None
        sql, woogi = function.join_sql()
        if sql:
            data = function.check_data_user(message.author.id)
            if data:
                if data[4] == 1:
                    return await message.reply(f"> 이미 출석하셨습니다")
                
                woogi.execute(f"UPDATE user_info SET daily_check = 1 WHERE user_id = {message.author.id}")
                woogi.execute(f"UPDATE user_info SET daily = {data[4] + 1} WHERE user_id = {message.author.id}")
                sql.commit()
                sql.close()
                await message.reply(f"> 출석체크 완료! 현재 출석일수 : {data[4] + 1}일")
            else:
                return await message.reply(f"> 데이터를 생성 후 다시 시도해주세요")
        else:
            return await message.reply(f"> 데이터베이스 접속 실패") 
    elif message.content.startswith("!색상표구매"):
        sql, woogi = function.join_sql()
        data = function.check_data_user(message.author.id)
        if not sql:
            return await message.reply(f"> 데이터베이스 접속 실패") 

        if not data:
            return await message.reply(f"> 데이터를 생성 후 다시 시도해주세요")

        check = await message.reply(f"어떤 색상을 구매할까요?",
            components = [
                Select(
                placeholder = "선택하기",
                    options = [
                        SelectOption(label = "💖 빨강", value = "빨강"),
                        SelectOption(label = "🧡 주황", value = "주황"),
                        SelectOption(label = "💛 노랑", value = "노랑"),
                        SelectOption(label = "🤹‍♂️ 민트", value = "민트"),
                        SelectOption(label = "💜 보랑", value = "보랑"),
                        SelectOption(label = "💗 핑크", value = "핑크"),
                        SelectOption(label = "❌ 취소", value = "취소"),
                    ]
                )
            ],
        )

        try:
            interaction = await client.wait_for("select_option", timeout=30)
            if interaction.values[0] == "취소":
                await check.delete()
                return await message.reply(embed=discord.Embed(description="구매가 취소되었습니다", color=0xff0000))
        except:
            await check.delete()
            return await message.reply("30초 안에 선택하지 않아 유저정보 확인이 취소되었습니다")
        
        if interaction.values[0] == "빨강":
            await message.author.add_roles(color_data['red'])
            woogi.execute(f"UPDATE user_info SET red = 1 WHERE user_id = {message.author.id}")
        elif interaction.values[0] == "주황":
            await message.author.add_roles(color_data['orange'])
            woogi.execute(f"UPDATE user_info SET orange = 1 WHERE user_id = {message.author.id}")
        elif interaction.values[0] == "노랑":
            await message.author.add_roles(color_data['yellow'])
            woogi.execute(f"UPDATE user_info SET yellow = 1 WHERE user_id = {message.author.id}")
        elif interaction.values[0] == "민트":
            await message.author.add_roles(color_data['mint'])
            woogi.execute(f"UPDATE user_info SET mint = 1 WHERE user_id = {message.author.id}")
        elif interaction.values[0] == "보랑":
            await message.author.add_roles(color_data['purple'])
            woogi.execute(f"UPDATE user_info SET purple = 1 WHERE user_id = {message.author.id}")
        elif interaction.values[0] == "핑크":
            await message.author.add_roles(color_data['pink'])
            woogi.execute(f"UPDATE user_info SET pink = 1 WHERE user_id = {message.author.id}")

        await check.delete()
        await message.reply(f"{interaction.values[0]} 색상표가 구매되었습니다")

client.run("")