"""
enable users to create chart via discord bot
"""
import os
import json
import discord
import matplotlib.pyplot as plt
import matplotlib
from discord.ext import commands
import dataframe

#set font
matplotlib.rc('font', family='Microsoft JhengHei')
DATA_DIR="/app/data/saved dataframe"
class Chart(commands.Cog, name='Chart'):
    """
    Chart.py is a discord bot that allows you to create dataframe, output chart, etc.
    """
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client
    #Create a new dataframe(ok)
    @commands.hybrid_command(name="createdf", description="Creade a new dataframe")
    async def createdf(self,ctx,name: str,arg2:str):
        """create a new dataframe"""
        df_dir=f"{DATA_DIR}/{name}"
        data=f"{DATA_DIR}/{name}/{name}.json"
        columns=arg2.split(",")
        #create directory
        if os.path.isdir(df_dir) is True:
            if os.path.isfile(data) is True:
                await ctx.send(f"dataframe '{name}' already exists!")
        else:
            #create directory
            os.makedirs(df_dir)
            os.chmod(f'{df_dir}', 0o777)
            #create json file
            df_create = []
            for i in range (len(columns)):
                df_create.append({f'{columns[i]}' : 'N/A'})
            #use pandas' orient: 'records'
            with open(data, encoding="utf-8", mode='w') as df_info:
                json.dump(df_create, df_info)#return created info
            await ctx.send(f"dataframe '{name}' has been created, index = {columns}")

    #add index to current dataframe(ok)
    @commands.hybrid_command(name="appenddf", description="add new index to an exist dataframe")
    async def appenddf(self,ctx,name: str,arg2: str):
        """
        the function is for adding index into an existed dataframe
        """
        df_dir=f"{DATA_DIR}/{name}"
        data=f'{DATA_DIR}/{name}/{name}.json'
        index=arg2.split(",")
        try:
            #read dataframe
            df_info = open(data, encoding="utf-8", mode='r')
            #there problem here: it should be loaded into dict instead of str
            df_append=json.load(df_info)#load json file
            #3. check the type of the index
            for i in range (len(df_append)):
                df = df_append[i]
                d = list(df.keys())
                dict_key = d[0]
                dict_value = df[dict_key]
                if  dict_value == "N/A":
                    df[dict_key] = [float(index[i])]
                else:
                    df[dict_key].append((float(index[i])))
            df_info.close()
            #write dataframe
            with open(file=data, encoding="utf-8", mode='w') as df_info:
                json.dump(df_append, df_info)
            df_info = json.load(open(data, encoding="utf-8", mode='r'))
            await ctx.send(f"dataframe '{name}' has been updated")
            for i in range (len(index)):
                df = df_append[i]
                d = list(df.keys())
                dict_key = d[0]
                dict_value = df[dict_key]
                await ctx.send(f"{dict_key} value = {dict_value}")
        except SyntaxError as ex :
            if os.path.isdir(df_dir is True):
                await ctx.send("dataframe not found!")
            else:
                template = f'An exception of type {0} occurred. Arguments:\n{1!r}'
                message = template.format(type(ex).__name__, ex.args)
                await ctx.send(message)

    #output dataframe
    @commands.hybrid_command(name="outputdf",description="print out an exist dataframe")
    async def outputdf(self, ctx, name: str):
        """_summary_
        Args:
            ctx (_type_): _description_
            name (str): _description_
        """
        data=f"{DATA_DIR}/{name}/{name}.json"
        df_dir=f"{DATA_DIR}/{name}"
        try:
            #open directory
            df_output = dataframe.writedf(data)
            await ctx.send(f"dataframe '{name}' \n {df_output}")
        except SyntaxError as ex :
            if os.path.isdir(df_dir is True):
                await ctx.send("dataframe not found!")
            else:
                template = f'An exception of type {0} occurred. Arguments:\n{1!r}'
                message = template.format(type(ex).__name__, ex.args)
                await ctx.send(message)
                
    @commands.hybrid_command(name="outputchart", description="output the chart of an exist dataframe")
    async def outputchart(self,ctx,title: str,color: str,mode: str):
        """
        output the chart of an exist dataframe
        """
        try:
            df_dir=f"{DATA_DIR}/{title}"
            data=f"{DATA_DIR}/{title}/{title}.json"
            df_info = json.load(open(data, encoding="utf-8", mode='r'))
            x_label=df_info['Column1']
            y_label=df_info['Column2']
            x_index = df_info['Column1_index']
            y_index = df_info['Column2_index']
            #create chart
            if mode == "0":
                plt.plot(x_index, y_index, color)
            elif mode == "1":
                x_int=[int(x) for x in x_index]
                y_int=[int(y) for y in y_index]
                plt.bar(x_int, y_int, color=color)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.title(title)
            #save chart
            if os.path.exists(f'{df_dir}/{title}output'):
                if os.path.isfile(f'{df_dir}/{title}output/{title}.png'):
                    os.remove(f"{df_dir}/{title}output/{title}.png")
                    plt.savefig(f"{df_dir}/{title}output/{title}.png")
                else:
                    plt.savefig(f"{df_dir}/{title}output/{title}.png")
            else:
                os.mkdir(f'{df_dir}/{title}output')
                os.chmod(f'{df_dir}/{title}output', 0o777)
                plt.savefig(f"{df_dir}/{title}output/{title}.png")
            pic_send=discord.File(f"{df_dir}/{title}output/{title}.png")
            await ctx.send(file=pic_send)
        except SyntaxError as ex :
            template = f'An exception of type {0} occurred. Arguments:\n{1!r}'
            message = template.format(type(ex).__name__, ex.args)
            await ctx.send(f'unable to output chart!, reason:{message}')

    @commands.hybrid_command(name="closefigma")
    async def closefigma(self, ctx):
        """
        close figma, end the edit of chart
        """
        plt.close()
        await ctx.send("Figma closed successfully")

    #delete dataframe
    @commands.hybrid_command(name="deldf",description="delete an exist dataframe")
    async def deldf(self, ctx, name: str):
        """
        delete an exist dataframe
        """
        try:
            data=f"{DATA_DIR}/{name}"
            df_dir=f"{DATA_DIR}/{name}/{name}.json"
            os.remove(df_dir)
            os.rmdir(data)
            await ctx.send("Dataframe removed successfully")
        except SyntaxError as ex :
            template = f'An exception of type {0} occurred. Arguments:\n{1!r}'
            message = template.format(type(ex).__name__, ex.args)
            await ctx.send(f'unable to remove dataframe, reason:{message}')
async def setup (client):
    """
    Loads the cog Chart into the bot.

    This is automatically called by commands.Bot.load_extension() and **is not meant to be called directly**.

    Args:
        client (commands.Bot): The bot to load the cog into.
    """
    
    await client.add_cog(Chart(client))
    