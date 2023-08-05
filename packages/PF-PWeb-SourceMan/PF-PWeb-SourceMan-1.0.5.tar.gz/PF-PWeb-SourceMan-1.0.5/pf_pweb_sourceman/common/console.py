import click


class Console:

    def log(self, text):
        print(text)

    def green(self, text, bold=False):
        click.echo(click.style(text, fg='green', bold=bold))

    def blue(self, text, bold=False):
        click.echo(click.style(text, fg='blue', bold=bold))

    def red(self, text, bold=False):
        click.echo(click.style(text, fg='red', bold=bold))

    def yellow(self, text, bold=False):
        click.echo(click.style(text, fg='yellow', bold=bold))

    def magenta(self, text, bold=False):
        click.echo(click.style(text, fg='magenta', bold=bold))

    def cyan(self, text, bold=False):
        click.echo(click.style(text, fg='cyan', bold=bold))

    def get_message_format(self, text):
        message = ">> " + str(text)
        return message

    def error(self, message):
        return self.red(self.get_message_format(message), True)

    def success(self, message):
        return self.green(self.get_message_format(message), True)

    def info(self, message):
        return self.blue(self.get_message_format(message), True)


console = Console()
