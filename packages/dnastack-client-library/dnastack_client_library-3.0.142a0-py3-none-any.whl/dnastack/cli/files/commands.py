import click
import os
from typing import List, Dict

from .local_client_repository import LocalClientRepository
from ..utils import command, ArgumentSpec, echo_result
from ...client.drs import DownloadOkEvent, DownloadFailureEvent, DownloadProgressEvent


@click.group('files')
def drs_command_group():
    """ Interact with Data Repository Service """


@command(
    drs_command_group,
    specs=[
        ArgumentSpec(
            name='quiet',
            arg_names=['-q', '--quiet'],
            help='Download files quietly',
            required=False,
        ),
        ArgumentSpec(
            name='input_file',
            arg_names=['-i', '--input-file'],
            help='Input file',
            required=False,
            as_option=True,
        ),
        ArgumentSpec(
            name='output_dir',
            arg_names=['-o', '--output-dir'],
            help='Output directory',
            required=False,
            as_option=True,
        ),
        ArgumentSpec(
            name='urls',
            help='DRS URLs, e.g., drs://<host>/<id>',
            required=False,
            nargs=-1,
        )
    ]
)
def download(endpoint_id: str,
             urls: List[str],
             output_dir: str = os.getcwd(),
             input_file: str = None,
             quiet: bool = False,
             no_auth: bool = False):
    """
    Download files with DRS urls, e.g., drs://<hostname>/<id>, per Data Repository Service (DRS) Specification 1.1.0.

    See https://ga4gh.github.io/data-repository-service-schemas/preview/release/drs-1.1.0/docs/#_drs_uris.
    """
    download_urls = []

    if len(urls) > 0:
        download_urls = list(urls)
    elif input_file:
        with open(input_file, "r") as infile:
            download_urls = filter(None, infile.read().split("\n"))  # need to filter out invalid values
    else:
        if not quiet:
            click.echo("Enter one or more URLs. Press q to quit")

        while True:
            try:
                url = click.prompt("", prompt_suffix="", type=str)
                url = url.strip()
                if url[0] == "q" or len(url) == 0:
                    break
            except click.Abort:
                break

            download_urls.append(url)

    drs = LocalClientRepository.get(endpoint_id)

    def display_ok(event: DownloadOkEvent):
        if not quiet:
            print()
        echo_result(None, 'green', 'complete', event.drs_url)
        if event.output_file_path:
            click.secho(f' → Saved as {event.output_file_path}', dim=True)

    def display_failure(event: DownloadFailureEvent):
        if not quiet:
            print()
        echo_result(None, 'red', 'failed', event.drs_url)
        if event.reason:
            click.secho(f' ● Reason: {event.reason}', dim=True)
        if event.error:
            click.secho(f' ● Error: {type(event.error).__name__}: {event.error}', dim=True)

    drs.events.on('download-ok', display_ok)
    drs.events.on('download-failure', display_failure)

    stats: Dict[str, DownloadProgressEvent] = dict()

    if quiet:
        drs.download_files(urls=download_urls,
                           output_dir=output_dir,
                           display_progress_bar=(not quiet),
                           no_auth=no_auth)
    else:
        with click.progressbar(label='Downloading...', color=True, length=1) as progress:
            def update_progress(event: DownloadProgressEvent):
                stats[event.drs_url] = event

                # Update the progress bar.
                position = 0
                total = 0

                for e in stats.values():
                    position += e.read_byte_count
                    total += e.total_byte_count

                progress.pos = position
                progress.length = total if total > 0 else 1

                progress.render_progress()

            drs.events.on('download-progress', update_progress)
            drs.download_files(urls=download_urls,
                               output_dir=output_dir,
                               display_progress_bar=(not quiet),
                               no_auth=no_auth)
