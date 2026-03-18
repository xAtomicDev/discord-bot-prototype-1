import importlib
import os
from discord.ext import commands

async def load_extensions(bot: commands.Bot):
    for root, _, files in os.walk(bot.ext_dir):
        for file in files:
            if not file.endswith(".py") or file == "__init__.py":
                continue

            module_path = (
                os.path.join(root, file)
                .replace("/", ".")
                .replace("\\", ".")
                .replace(".py", "")
            )

            module = importlib.import_module(module_path)

            if hasattr(module, "setup"):
                await bot.load_extension(module_path)
                bot.logger.info(f"Loaded extension {module_path}")
            else:
                bot.logger.trace(f"Extension/File {module_path} does not have a setup function")