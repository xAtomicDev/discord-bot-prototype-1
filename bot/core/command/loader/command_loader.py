import importlib
import os
from discord.ext import commands

async def load_extensions(bot: commands.Bot):
    extension_root = os.path.abspath(bot.ext_dir)
    extension_package = os.path.basename(extension_root)

    for root, _, files in os.walk(bot.ext_dir):
        for file in files:
            if not file.endswith(".py") or file == "__init__.py":
                continue

            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, extension_root)
            module_name = os.path.splitext(relative_path)[0].replace(os.sep, ".")
            module_path = f"{extension_package}.{module_name}"

            module = importlib.import_module(module_path)

            if hasattr(module, "setup"):
                await bot.load_extension(module_path)
                bot.logger.info(f"Loaded extension {module_path}")
            else:
                bot.logger.warning(f"Extension/File {module_path} does not have a setup function")
