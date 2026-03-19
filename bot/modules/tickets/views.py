from bot.core.namespace_id import NamespaceID
import discord
from discord.ext import commands
from discord import app_commands


class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Soporte", description="Abrir ticket de soporte", emoji="🛠️"),
            discord.SelectOption(label="Ventas", description="Consulta de compras", emoji="💰"),
            discord.SelectOption(label="Reportes", description="Reportar un usuario", emoji="🚨"),
        ]

        super().__init__(
            custom_id=NamespaceID("ticket", "select").build(),
            placeholder="Selecciona el tipo de ticket...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        opcion = self.values[0]

        await interaction.response.send_message(
            f"Elegiste: {opcion}",
            ephemeral=True
        )


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())


async def setup(bot):
    bot.add_view(TicketView())