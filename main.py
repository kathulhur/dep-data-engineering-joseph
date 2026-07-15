import os
import click
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

@click.group()
def cli():
    pass

@cli.group()
def dataset():
    pass

@dataset.group()
def comment():
    pass

@comment.command('load')
@click.argument('ids')
@click.option('--output-file', 'output_file', type=click.Path(path_type=Path), default=Path(os.getcwd()) / 'data' / 'raw' / 'comments.json')
def load_comments(ids, output_file: Path):
    from apify_client import ApifyClient
    import json
    dataset_ids = [id_attr.strip() for id_attr in ids.split(',')]

    apify_client = ApifyClient(os.getenv('APIFY_TOKEN'))
    comments = []
    for dataset_id in dataset_ids:
        click.echo(f'Downloading dataset {dataset_id}...')
        data = apify_client.dataset(dataset_id).list_items().items
        click.echo(f'Dataset {dataset_id} has been downloaded.\n')
        comments.extend(data)

    with output_file.open('w', encoding='utf-8') as f:
        json.dump(comments, f, ensure_ascii=False, indent=2)

@dataset.group()
def post():
    pass

@post.command('load')
@click.argument('ids')
@click.option('--output-file', 'output_file', type=click.Path(path_type=Path), default=Path(os.getcwd()) / 'data' / 'raw' / 'posts.json')
def load_posts(ids, output_file: Path):
    from apify_client import ApifyClient
    import json
    post_ids = [id_attr.strip() for id_attr in ids.split(',')]

    apify_client = ApifyClient(os.getenv('APIFY_TOKEN'))
    posts = []
    for dataset_id in post_ids:
        click.echo(f'Downloading post {dataset_id}...')
        data = apify_client.dataset(dataset_id).list_items().items
        click.echo(f'Posts dataset {dataset_id} has been downloaded.\n')
        posts.extend(data)

    with output_file.open('w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    counter = 1
    apify_directory = Path(os.getcwd()) / 'data' / 'apify'
    apify_directory.mkdir(exist_ok=True)

    while posts:
        subset = posts[:100]
        post_urls = [post['url'] + "\n" for post in subset]
        with (apify_directory / f'post_urls-{counter}').with_suffix('.txt').open('w') as f:
            f.writelines(post_urls)

        posts = posts[100:]
        counter += 1





if __name__ == '__main__':
    cli()