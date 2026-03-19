from discord.ext import commands
from discord import app_commands
import discord

from modules.tickets.views import TicketView

class TicketCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="create-ticket", description="Crea un ticket")
    async def create_ticket(self, interaction: discord.Interaction):
        await interaction.response.send_message("🎫 Ticket creado")
        
        
class TicketPanel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="panel", description="Crear panel de tickets")
    async def panel(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎫 Sistema de Tickets",
            description="Selecciona una opción del menú para continuar.",
            color=discord.Color.blue()
        )

        embed.set_footer(text="Soporte 24/7")

        await interaction.response.send_message(
            embed=embed,
            view=TicketView()
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(TicketCommands(bot))
    await bot.add_cog(TicketPanel(bot))