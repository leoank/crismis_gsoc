import click

@click.group()
def cli():
    pass

@cli.command(help='Train the model')
@click.option('--docker', is_flag=True, default=False, help='Train model inside docker')
def train(docker):
    if docker:
        pass
    else:
        pass


@cli.command(help='Testing model')
@click.option('--docker', is_flag=True, default=False, help='Run test inside docker')
def test(docker):
    if docker:
        pass
    else:
        pass

@cli.command(help='Run the algorithm')
@click.option('--docker', is_flag=True, default=False, help='Run algorithm inside docker')
def predict(docker):
    if docker:
        pass
    else:
        pass

@cli.command(help='Download datasets')
@click.option('--docker', is_flag=True, default=False, help='Download datasets inside docker')
def download(docker):
    if docker:
        pass
    else:
        pass