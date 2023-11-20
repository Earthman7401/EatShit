import discord
from discord.ext import commands
import json 
from core import Cog_Extension

class TodoList(Cog_Extension):
    # Initialization 
    def __init__(self, bot):
        self.todo = []
        
    # Add item
    @commands.command()
    async def AddTodoList(self, ctx, item):
        self.todo.append(item)
        await ctx.send("待辦事項已新增") 

    # Remove item
    @commands.command()
    async def RemoveTodoList(self, ctx, item):
        if item in self.todo:
            self.todo.remove(item)
        else:
            await ctx.send("此待辦事項不存在") 

    # Sort todolist
    @commands.command()
    async def SortTodoList(self, ctx):
        if len(self.todo):
            self.todo.sort()
            for item in self.todo:
                await ctx.send(item) 
        else:
            await ctx.send("沒有任何代辦事項")
            

    # Clear todolist
    @commands.command()
    async def ClearTodoList(self, ctx):
       self.todo.clear()

async def setup(bot):
    await bot.add_cog(TodoList(bot))