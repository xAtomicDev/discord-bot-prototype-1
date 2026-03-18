from discord.ext import commands
from discord import app_commands

class TicketCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="create-ticket", description="Crea un ticket")
    async def create_ticket(self, interaction):
        await interaction.response.send_message("Ticket creado")

async def setup(bot):
    await bot.add_cog(TicketCommands(bot))