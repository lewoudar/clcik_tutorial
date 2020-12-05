"""Implementation of a CLI capable of downloading multiple images concurrently"""
from pathlib import Path
from typing import List

import anyio
import click
import httpx
from rich.console import Console
from rich.progress import Progress, TaskID


def get_image_urls(path: Path) -> List[str]:
    images = []
    with path.open() as f:
        for line in f:
            line = line.strip(' \n')
            if not line:
                continue
            images.append(line)
    return images


async def download_image(
        progress: Progress, task_id: TaskID, image_url: str, destination: Path
) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.get(image_url)
        if response.status_code >= 400:
            progress.console.print(f'image [blue]{image_url}[/] could not be downloaded')
            progress.update(task_id, advance=1)
            return

        path = destination / image_url.split('/')[-1]
        path.write_bytes(response.content)
        progress.update(task_id, advance=1)


async def worker(
        image_urls: List[str], progress: Progress, task_id: TaskID, destination: str
) -> None:
    destination = Path(destination).resolve()
    if not destination.is_dir():
        destination.mkdir()

    async with anyio.create_task_group() as tg:
        for image_url in image_urls:
            await tg.spawn(download_image, progress, task_id, image_url, destination)


@click.version_option('0.1.0', message='%(prog)s version %(version)s')
@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('file', type=click.Path(exists=True, dir_okay=False))
@click.argument('destination', type=click.Path(file_okay=False, writable=True))
def cli(destination, file):
    """
    Downloads multiple images given their urls in FILE and store them in DESTINATION.

    FILE is the file containing urls for images to download. The file must contains one url
    per line

    DESTINATION is the folder that will store the downloaded images. If it does not exist, imdgl
    will create it automatically. Take care that the path provided does not have permission issues
    for the current user.
    """
    path = Path(file)
    if path.stat().st_size == 0:
        raise click.UsageError('FILE must not be empty')

    console = Console()
    image_urls = get_image_urls(path)
    with Progress(console=console) as progress:
        task_id = progress.add_task('Downloading', total=len(image_urls))
        anyio.run(worker, image_urls, progress, task_id, destination)

    console.print('Downloads are finished! :glowing_star:')
