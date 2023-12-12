import discord
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from discord.ext import commands
import json
import os,sys,stat

predir=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
os.chdir(f'{predir}/ChartBot')
#readfile
with open('setting.json', mode='r') as jfile:
    jdata=json.load(jfile)
#file is stored as dictionary
#set font
matplotlib.rc('font', family='Microsoft JhengHei')

intents = discord.Intents.all()
client = commands.Bot(command_prefix='*',intents=intents)

class Chart(commands.cog):
    def __init__(self,client):
        self.client = client

    #Create a new dataframe
    @commands.command()
    async def createdf(ctx, arg1, arg2):
        curdir=f"{jdata['Dataset Directory']}/{arg1}"
        '''try:'''
        columns=arg2.split(",")
            #create directory
        os.mkdir(curdir)
        os.chdir(curdir)
        #create json file
        df_create = {"name": arg1}
        for i in range(len(columns)):
            df_create[f"Column{i+1}"] = columns[i]

        with open(f'{arg1}.json', mode='w') as df_info:
            json.dump(df_create, df_info)
            #return created info
        await ctx.send(f"dataframe '{arg1}' has been created")
        for i in range (len(columns)):
            await ctx.send()
        os.chdir(jdata["Project Directory"])

    #add index to current dataframe
    @commands.command()
    async def appenddf(ctx, arg1, arg2, arg3):
        curdir=f"{jdata['Dataset Directory']}/{arg1}"
        try:
            #open directory
            os.chdir(curdir)
            #read dataframe
            df_info = open(f'{arg1}.json', mode='r')
            df_append=json.load(df_info)#load json file
            df_append["Column1_index"].append(float(arg2))
            df_append["Column2_index"].append(float(arg3))
            df_info.close
            #write dataframe
            with open(f'{arg1}.json', mode='w') as df_info:
                json.dump(df_append, df_info)
            df_info = json.load(open(f'{arg1}.json', mode='r'))
            Column1=df_info["Column1"]
            Column2=df_info["Column2"]
            index1=df_info["Column1_index"]
            index2=df_info["Column2_index"]
            await ctx.send(f"dataframe '{arg1}' has been updated, Current '{Column1}' index: '{index1}', '{Column2}': '{index2}'")
        except:
            await ctx.send("dataframe not found!")
        os.chdir(jdata["Project Directory"])

    #output dataframe
    @commands.command()
    async def outputdf(ctx, arg1):
        curdir=f"{jdata['Dataset Directory']}/{arg1}"
        try:
            #open directory
            os.chdir(curdir)
            df_info = json.load(open(f'{arg1}.json', mode='r'))

            df_output = pd.DataFrame({
            df_info['Column1'] : df_info['Column1_index'],
            df_info['Column2'] : df_info['Column2_index'],
            })
            await ctx.send(f"dataframe '{df_info['name']}' \n {df_output}")
        except:
            await ctx.send("dataframe not found!")
        os.chdir(jdata["Project Directory"])

    @commands.command()
    #arg1=name
    #arg2=colour
    #arg3=mode(0: line chart; 1: Bar Chart)
    async def outputchart(ctx, arg1, arg2, arg3):
        try:
            curdir=f"{jdata['Dataset Directory']}/{arg1}"
            Colour=arg2
            Title=arg1
            os.chdir(curdir)
            df_info = json.load(open(f'{arg1}.json', mode='r'))
            xLabel=df_info['Column1']
            yLabel=df_info['Column2']
            xIndex = df_info['Column1_index']
            yIndex = df_info['Column2_index']
            #create chart
            if arg3 == "0":
                plt.plot(xIndex, yIndex, Colour)
            elif arg3 == "1":
                xInt=[int(x) for x in xIndex]
                yInt=[int(y) for y in yIndex]
                plt.bar(xInt, yInt, color=Colour)
            plt.xlabel(xLabel)
            plt.ylabel(yLabel)
            plt.title(Title)
            #save chart
            if os.path.exists('{curdir}/{Title}output'):
                if os.path.isfile('{curdir}/{Title}output/{Title}.png'):
                    os.remove(f"{curdir}/{Title}output/{Title}.png")
                    plt.savefig(f"{curdir}/{Title}output/{Title}.png")
                else:
                    plt.savefig(f"{curdir}/{Title}output/{Title}.png")
            else:
                os.mkdir(f'{curdir}/{Title}output')
                os.chmod(f'{curdir}/{Title}output', 0o777)
                plt.savefig(f"{curdir}/{Title}output/{Title}.png")
            pic_send=discord.File(f"{curdir}/{Title}output/{Title}.png")
            await ctx.send(file=pic_send)
            
            os.chdir(jdata["Project Directory"])
        except:
            await ctx.send("Failed to output chart")

    @commands.command()
    async def closefigma(ctx):
        plt.close()
        await ctx.send("Figma closed successfully")

    #delete dataframe
    @commands.command()
    async def deldf(ctx, arg1):
        try:    
            curdir=f"{jdata['Dataset Directory']}/{arg1}"
            os.chmod(f'{curdir}', 0o777)
            os.remove(f"{curdir}/{arg1}.json")
            os.rmdir(f'{curdir}')
            await ctx.send("Dataframe removed successfully")
        except:
            await ctx.send("Failed to remove dataframe")
    
    def setup (client):
        client.add_cog(Chart(client))