from discord_api import DiscordClient, applications


class Client(DiscordClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_listener("interaction_create", self.on_interaction)
        self.slash_commands = {}
    
    def slash_command(self, name: str, description: str, *, options: dict):
        def decorator(function):
            self.slash_commands[name] = function
            app_command = applications.Command(name=name, description=description)
            for p in signature(function).parameters.values():
                if p.name == "interaction":
                    continue
                if p.default == None:
                    required = True
                else:
                    required = False
                app_command.add_option(applications.CommandOption(name=p.name, description=options[p.name], required=required))
            self.application.commands.append(app_command)
            return function
        return decorator
        
    async def on_interaction(self, interaction):
        if interaction.command is not None:
            if interaction.command.name in self.slash_commands:
                kwargs = interaction.command.options or {}
                await self.slash_commands[interaction.command.name](interaction, **kwargs)
