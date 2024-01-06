import discord
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from discord.ext import commands
import json
import os

os.chdir('/app/ChartBot')
DATA_DIR="/app/ChartBot/saved dataframe"
PROJECT_DIR="/app"
class Chart(commands.Cog, name='Chart'):
    """
    Chart.py is a discord bot that allows you to create dataframe, output chart, etc.
    """
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client
    #Create a new dataframe
    @commands.hybrid_command(name="creatdf", description="Creade a new dataframe")
    async def createdf(
        self,
        ctx,
        arg1: str,
        arg2:str
        ):
        """create a new dataframe"""
        curdir=f"{DATA_DIR}/{arg1}"
        columns=arg2.split(",")
            #create directory
        os.mkdir(curdir)
        os.chdir(curdir)
        #create json file
        df_create = {"name": arg1}
        for i in range(len(columns)):
            df_create[f"Column{i+1}"] = columns[i]

        with open(f'{arg1}.json', encoding="utf-8", mode='w') as df_info:
            json.dump(df_create, df_info)
            #return created info
        await ctx.send(f"dataframe '{arg1}' has been created")
        for i in range (len(columns)):
            await ctx.send()
        os.chdir(PROJECT_DIR)

    #add index to current dataframe
    @commands.hybrid_command(name="appenddf", description="add new index to an exist dataframe")
    async def appenddf(
        self,
        ctx,
        arg1: str,
        arg2: str,
        arg3: str
        ):
        """the function is for adding index into an existed sataframe"""
        curdir=f"{DATA_DIR}/{arg1}"
        try:
            #open directory
            os.chdir(curdir)
            #read dataframe
            df_info = open(f'{arg1}.json', encoding="utf-8", mode='r')
            df_append=json.load(df_info)#load json file
            df_append["Column1_index"].append(float(arg2))
            df_append["Column2_index"].append(float(arg3))
            df_info.close()
            #write dataframe
            with open(f'{arg1}.json',encoding="utf-8", mode='w') as df_info:
                json.dump(df_append, df_info)
            df_info = json.load(open(f'{arg1}.json', encoding="utf-8", mode='r'))
            column_1=df_info["Column1"]
            column_2=df_info["Column2"]
            index1=df_info["Column1_index"]
            index2=df_info["Column2_index"]
            await ctx.send(f"dataframe '{arg1}' has been updated, Current '{column_1}' index: '{index1}', '{column_2}': '{index2}'")
        except SyntaxError as ex :
            if os.path.isdir(curdir is True):
                await ctx.send("dataframe not found!")
            else:    
                template = f'An exception of type {0} occurred. Arguments:\n{1!r}'
                message = template.format(type(ex).__name__, ex.args)
                await ctx.send(message)
            
        os.chdir(PROJECT_DIR)

    #output dataframe
    @commands.hybrid_command(name="outputdf",description="print out an exist dataframe")
    async def outputdf(self, ctx, arg1: str):
        curdir=f"{DATA_DIR}/{arg1}"
        try:
            #open directory
            os.chdir(curdir)
            df_info = json.load(open(f'{arg1}.json', encoding="etf-8", mode='r'))

            df_output = pd.DataFrame({
            df_info['Column1'] : df_info['Column1_index'],
            df_info['Column2'] : df_info['Column2_index'],
            })
            await ctx.send(f"dataframe '{df_info['name']}' \n {df_output}")
        except SyntaxError as ex :
            if (os.path.isdir(curdir is True)):
                await ctx.send("dataframe not found!")
            else:    
                template = f'An exception of type {0} occurred. Arguments:\n{1!r}'
                message = template.format(type(ex).__name__, ex.args)
                await ctx.send(message)
        os.chdir(PROJECT_DIR)

    @commands.hybrid_command(name="outputchart", description="output the chart of an exist dataframe")
    #arg1=name
    #arg2=color
    #arg3=mode(0: line chart; 1: Bar Chart)
    async def outputchart(
        self,
        ctx,
        arg1: str,
        arg2: str,
        arg3: str
        ):
        """
        output the chart of an exist dataframe
        """
        try:
            curdir=f"{DATA_DIR}/{arg1}"
            color=arg2
            title=arg1
            os.chdir(curdir)
            df_info = json.load(open(f'{arg1}.json', encoding="utf-8", mode='r'))
            x_label=df_info['Column1']
            y_label=df_info['Column2']
            x_index = df_info['Column1_index']
            y_index = df_info['Column2_index']
            #create chart
            if arg3 == "0":
                plt.plot(x_index, y_index, color)
            elif arg3 == "1":
                x_int=[int(x) for x in x_index]
                y_int=[int(y) for y in y_index]
                plt.bar(x_int, y_int, color=color)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.title(title)
            #save chart
            if os.path.exists('{curdir}/{title}output'):
                if os.path.isfile('{curdir}/{title}output/{title}.png'):
                    os.remove(f"{curdir}/{title}output/{title}.png")
                    plt.savefig(f"{curdir}/{title}output/{title}.png")
                else:
                    plt.savefig(f"{curdir}/{title}output/{title}.png")
            else:
                os.mkdir(f'{curdir}/{title}output')
                os.chmod(f'{curdir}/{title}output', 0o777)
                plt.savefig(f"{curdir}/{title}output/{title}.png")
            pic_send=discord.File(f"{curdir}/{title}output/{title}.png")
            await ctx.send(file=pic_send)            
            os.chdir(PROJECT_DIR)
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
    async def deldf(self, ctx, arg1: str):
        """
        delete an exist dataframe
        """
        try:
            curdir=f"{DATA_DIR}/{arg1}"
            os.chmod(f'{curdir}', 0o777)
            os.remove(f"{curdir}/{arg1}.json")
            os.rmdir(f'{curdir}')
            await ctx.send("Dataframe removed successfully")
        except SyntaxError as ex :
            template = f'An exception of type {0} occurred. Arguments:\n{1!r}'
            message = template.format(type(ex).__name__, ex.args)
            await ctx.send(f'unable to remove dataframe, reason:{message}')
    
async def setup (client):
    await client.add_cog(Chart(client))
    #set font
    matplotlib.rc('font', family='Microsoft JhengHei')