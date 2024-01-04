import discord
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from discord.ext import commands
import json
import os

os.chdir(f'/app/ChartBot')
Datadir="/app/ChartBot/saved dataframe"
Projectdir="/app"
class Chart(commands.Cog, name='Chart'):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client

          

    #Create a new dataframe
    @commands.hybrid_command(name="creatdf", description="Creade a new dataframe")
    async def createdf(ctx, arg1: str, arg2:str):
        curdir=f"{Datadir}/{arg1}"
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
        os.chdir(Projectdir)

    #add index to current dataframe
    @commands.hybrid_command(name="appenddf", description="add new index to an exist dataframe")
    async def appenddf(ctx, arg1: str, arg2: str, arg3: str):
        curdir=f"{Datadir}/{arg1}"
        try:
            #open directory
            os.chdir(curdir)
            #read dataframe
            df_info = open(f'{arg1}.json', mode='r')
            df_append=json.load(df_info)#load json file
            df_append["Column1_index"].append(float(arg2))
            df_append["Column2_index"].append(float(arg3))
            df_info.close()
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
        os.chdir(Projectdir)

    #output dataframe
    @commands.hybrid_command(name="outputdf",description="print out an exist dataframe")
    async def outputdf(ctx, arg1: str):
        curdir=f"{Datadir}/{arg1}"
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
        os.chdir(Projectdir)

    @commands.hybrid_command(name="outputchart", description="out put the chart of an exist dataframe")
    #arg1=name
    #arg2=colour
    #arg3=mode(0: line chart; 1: Bar Chart)
    async def outputchart(ctx, arg1: str, arg2: str, arg3: str):
        try:
            curdir=f"{Datadir}/{arg1}"
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
            
            os.chdir(Projectdir)
        except:
            await ctx.send("Failed to output chart")

    @commands.hybrid_command(name="closefigma")
    async def closefigma(self, ctx):
        plt.close()
        await ctx.send("Figma closed successfully")

    #delete dataframe
    @commands.hybrid_command(name="deldf",description="delete an exist dataframe")
    async def deldf(ctx, arg1: str):
        try:    
            curdir=f"{Datadir}/{arg1}"
            os.chmod(f'{curdir}', 0o777)
            os.remove(f"{curdir}/{arg1}.json")
            os.rmdir(f'{curdir}')
            await ctx.send("Dataframe removed successfully")
        except:
            await ctx.send("Failed to remove dataframe")
    
async def setup (client):
    await client.add_cog(Chart(client))
    
    
    #set font
    matplotlib.rc('font', family='Microsoft JhengHei')