from discord.ext.commands.errors import CommandError

class WrongChannelError(CommandError):
    """Exception raised when a command is attempted to be invoked
    from a channel it's not supposed to
    """
    def __init__(self,goodChannel):
        super().__init__(message="Mauvais chan, essaie dans : " + goodChannel.mention)