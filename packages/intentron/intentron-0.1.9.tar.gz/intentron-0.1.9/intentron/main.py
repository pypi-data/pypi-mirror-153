import click
from intentron.stages import *


@click.group()
def main():
    pass


@main.command()
@click.argument('src')
def crop(src):
    crop_stage(src)


@main.command()
@click.argument('src')
def check(src):
    check_stage(src)


@main.command()
@click.argument('src')
@click.argument('dst')
@click.argument('cam')
def separate(src, dst, cam):
    separate_stage(src, dst, cam)


@main.command()
@click.argument('src')
@click.argument('dst')
def load(src, dst):
    load_stage(src, dst)


@main.command()
@click.argument('src')
@click.argument('dst')
def parse(src, dst):
    parse_stage(src, dst)


@main.command()
@click.argument('src')
@click.argument('dst')
def fuse(src, dst):
    fuse_stage(src, dst)


@main.command()
@click.argument('src')
@click.argument('dst')
def gather(src, dst):
    gather_stage(src, dst)


@main.command()
@click.argument('src')
@click.argument('dst', required=False)
def pipeline(src, dst=None):
    pipeline_stage(src, dst)


if __name__ == '__main__':
    main()
