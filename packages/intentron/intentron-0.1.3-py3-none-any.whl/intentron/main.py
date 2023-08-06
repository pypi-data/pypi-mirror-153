import click
from intentron.stages import (
    infer_job,
    draw_job,
    estimate_job,

    load_stage,
    parse_stage,
    fuse_stage,
    pipeline_stage
)


@click.group()
def main():
    pass


@main.command()
@click.argument('src')
@click.argument('dst')
def load(src, dst):
    load_stage(src, dst)


@main.command()
@click.argument('src')
@click.argument('dst')
@click.argument('fmt', default='all')
def parse(src, dst):
    print('parse')
    parse_stage(src, dst)


@main.command()
@click.argument('src')
@click.argument('dst')
def fuse(src, dst):
    fuse_stage(src, dst)


@main.command()
@click.argument('src')
@click.argument('dst')
def infer(src, dst):
    infer_job(src, dst)


@main.command()
@click.argument('src')
@click.argument('dst')
def estimate(src, dst):
    estimate_job(src, dst)


@main.command()
@click.argument('src')
@click.argument('dst')
def draw(src, dst):
    draw_job(src, dst)


@main.command()
@click.argument('src')
@click.argument('dst', required=False)
def pipeline(src, dst=None):
    pipeline_stage(src, dst)


if __name__ == '__main__':
    main()
