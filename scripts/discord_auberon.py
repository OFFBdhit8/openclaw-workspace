#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Discord 机器人 - Auberon
角色：工作室第一位员工，专业高冷，统筹一切
"""

import os
import asyncio
import discord
from discord.ext import commands

# ============ 配置区域 ============
# 你提供的 Token（用户 Token 或 Bot Token）
DISCORD_TOKEN = "G_uCTy.v7CO9DLbD1bCYWzDj7nue36EIs1329q39z7gDM"

# 服务器和频道 ID
GUILD_ID = YOUR_GUILD_ID  # 服务器 ID
CHANNEL_ID = YOUR_DISCORD_CHANNEL_ID  # 频道 ID

# Auberon 的角色设定
BOT_NAME = "Auberon"
BOT_DESCRIPTION = "工作室第一位员工，专业高冷，统筹一切"
BOT_PREFIX = "!"  # 命令前缀

# =================================

# 设置 intents（权限）
intents = discord.Intents.default()
intents.message_content = True  # 需要读取消息内容
intents.guilds = True
intents.messages = True

# 创建 bot
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents, description=BOT_DESCRIPTION)

@bot.event
async def on_ready():
    """机器人启动后的回调"""
    print(f"✅ {BOT_NAME} 已上线！")
    print(f"🤖 机器人名称: {bot.user.name}")
    print(f"🆔 用户 ID: {bot.user.id}")
    print(f"📺 当前状态: {bot.is_ready()}")
    
    # 获取服务器信息
    guild = bot.get_guild(GUILD_ID)
    if guild:
        print(f"\n🏠 已连接到服务器: {guild.name} (ID: {guild.id})")
    else:
        print(f"\n⚠️ 无法连接到服务器 ID: {GUILD_ID}，请检查服务器 ID 是否正确")
    
    # 尝试发送启动消息到指定频道
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        print(f"\n📢 已找到目标频道 ID: {CHANNEL_ID}")
        await channel.send(f"👋 大家好！我是 **{BOT_NAME}**，工作室第一位员工。\n\n💼 专业高冷，统筹一切。\n有任何工作室相关的问题，请随时找我。")
    else:
        print(f"\n⚠️ 无法找到频道 ID: {CHANNEL_ID}，请检查频道 ID 是否正确")
        print(f"   可能原因：机器人尚未被邀请到该服务器")

@bot.command(name="hello", aliases=["hi", "你好"])
async def hello(ctx):
    """打招呼命令"""
    await ctx.send(f"👋 你好。我是 **{BOT_NAME}**。\n\n💼 工作室第一位员工，统筹一切。\n有工作要安排吗？")

@bot.command(name="status", aliases=["状态"])
async def status(ctx):
    """查看工作室状态"""
    embed = discord.Embed(
        title=f"📊 {BOT_NAME} 工作状态",
        description="一切正常运转中",
        color=discord.Color.blue()
    )
    embed.add_field(name="🆔 身份", value="工作室第一位员工", inline=True)
    embed.add_field(name="💼 职责", value="统筹一切", inline=True)
    embed.add_field(name="⚡ 状态", value="随时待命", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="plan", aliases=["计划", "安排"])
async def plan(ctx, *, task: str = None):
    """制定计划/安排任务"""
    if not task:
        await ctx.send(f"📋 用法：`{BOT_PREFIX}plan <任务内容>`")
        return
    
    responses = [
        f"收到。我会统筹安排：{task}",
        f"明白，已记录任务：{task}。我会统筹处理。",
        f"收到。{task} 这件事，我来处理。",
    ]
    import random
    response = random.choice(responses)
    await ctx.send(f"📋 **{response}**")

@bot.command(name="report", aliases=["汇报", "工作报告"])
async def report(ctx):
    """工作报告"""
    embed = discord.Embed(
        title=f"📋 {BOT_NAME} 工作报告",
        description="每日工作汇总",
        color=discord.Color.green()
    )
    embed.add_field(name="✅ 已完成", value="工作室日常运营统筹\n跨部门协调沟通\n任务分配与进度跟进", inline=False)
    embed.add_field(name="🔄 进行中", value="待处理事务", inline=False)
    embed.add_field(name="📌 待处理", value="等待指令", inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    """处理消息事件"""
    # 忽略机器人自己的消息
    if message.author == bot.user:
        return
    
    # 处理 @ 提及
    if bot.user.mentioned_in(message):
        responses = [
            "📋 收到。有何指示？",
            "💼 我在。有什么事？",
            "⚡ 统筹中。说明你的需求。",
        ]
        import random
        await message.channel.send(random.choice(responses))
    
    # 继续处理命令
    await bot.process_commands(message)

# 运行机器人
if __name__ == "__main__":
    print("=" * 50)
    print(f"🚀 正在启动 {BOT_NAME}...")
    print(f"📝 角色设定: {BOT_DESCRIPTION}")
    print("=" * 50)
    
    try:
        bot.run(DISCORD_TOKEN)
    except discord.errors.LoginFailure:
        print("❌ 登录失败！请检查 Token 是否正确")
        print("   - 如果是用户 Token，可能已过期或无效")
        print("   - 如果是 Bot Token，请确认是通过开发者门户创建的 Bot Token")
    except Exception as e:
        print(f"❌ 运行出错: {e}")
