from concurrent.futures import ThreadPoolExecutor, Future, as_completed

import os
import re
import requests
import threading
import urllib3
from contextlib import AbstractContextManager
from dataclasses import dataclass
from enum import Enum
from io import TextIOWrapper
from typing import Optional, Union, List, Dict
from urllib.parse import urlparse, urljoin

from dnastack.client.service_registry.models import ServiceType
from dnastack.configuration.models import ServiceEndpoint
from ..common.events import Event

try:
    import pandas as pd

    _module_pandas_available = True
except ImportError:
    _module_pandas_available = False

from .base_client import BaseServiceClient
from ..exceptions import DRSDownloadException, DRSException

DRS_TYPE_V1_1 = ServiceType(group='org.ga4gh', artifact='drs', version='1.1.0')


class MissingOptionalRequirementError(RuntimeError):
    """ Raised when a optional requirement is not available """


class InvalidDrsUrlError(ValueError):
    """ Raised when the DRS URL is invalid """


class DrsApiError(RuntimeError):
    """ Raised when the DRS server responds an error """


class NoUsableAccessMethodError(RuntimeError):
    """ Raised when there is no usable access methods """


class DRSObject:
    """
    A class for a DRS resource

    :param url: The DRS url
    :raises ValueError if url is not a valid DRS url
    """

    __RE_VALID_DRS_OBJECT_ID = re.compile(r'^[^/#?]+$')

    def __init__(self, url: str):
        try:
            DRSObject.assert_valid_drs_url(url)
        except AssertionError:
            raise InvalidDrsUrlError("The provided url is not a valid DRS url")

        self.__url = url

    @staticmethod
    def get_adapter_type() -> str:
        return 'drs'

    @staticmethod
    def support_service_types() -> List[ServiceType]:
        return [
            ServiceType(group='org.ga4gh', artifact='drs', version='1.1.0'),
        ]

    @property
    def url(self):
        return self.__url

    @property
    def object_id(self) -> str:
        """
        Return the object ID from a drs url

        :param url: A drs url
        :return: The object ID extracted from the URL
        :raises: ValueError if there isn't a valid DRS Object ID
        """
        parsed_url = urlparse(self.url)
        return parsed_url.path.split("/")[-1]

    @property
    def drs_server_url(self) -> str:
        """
        Return the HTTPS server associated with the DRS url

        :param url: A drs url
        :return: The associated HTTPS server url
        """
        parsed_url = urlparse(self.url)
        return urljoin(f'https://{parsed_url.netloc}{"/".join(parsed_url.path.split("/")[:-1])}', 'ga4gh/drs/v1/')

    @staticmethod
    def assert_valid_drs_url(url: str):
        """Returns true if url is a valid DRS url"""
        parsed_url = urlparse(url)
        assert parsed_url.scheme == r'drs', f'The scheme of the given URL ({url}) is invalid.'
        assert len(parsed_url.path) > 2 and parsed_url.path.startswith(
            r'/'), f'The ID is not specified in the URL ({url}).'
        assert DRSObject.__RE_VALID_DRS_OBJECT_ID.search(
            parsed_url.path[1:]), f'The format of the ID ({parsed_url.path[1:]}) is not valid.'


@dataclass(frozen=True)
class DownloadOkEvent(Event):
    @property
    def drs_url(self):
        return self.details.get('drs_url')

    @property
    def content(self):
        return self.details.get('content')

    @property
    def output_file_path(self):
        return self.details.get('output_file_path')

    @classmethod
    def make(cls, **kwargs):
        return cls(kwargs)


@dataclass(frozen=True)
class DownloadProgressEvent(Event):
    @property
    def drs_url(self):
        return self.details.get('drs_url')

    @property
    def read_byte_count(self):
        return self.details.get('read_byte_count')

    @property
    def total_byte_count(self):
        return self.details.get('total_byte_count')

    @classmethod
    def make(cls, **kwargs):
        return cls(kwargs)


@dataclass(frozen=True)
class DownloadFailureEvent(Event):
    @property
    def drs_url(self):
        return self.details.get('drs_url')

    @property
    def reason(self):
        return self.details.get('reason')

    @property
    def error(self):
        return self.details.get('error')

    @classmethod
    def make(cls, **kwargs):
        return cls(kwargs)


def handle_file_response(download_file: str, data: Union[str, bytes]) -> str:
    # Decode the data to string if it is a FASTA/FASTQ file and the client receives as byte stream """
    if bool(re.search(r"\.(bam|fasta|fna|ffn|faa|frn|fa|fastq)$", download_file, re.I)) and isinstance(data, bytes):
        data = data.decode("utf-8")

    return data


def file_to_dataframe(download_file: str, data: Union[str, bytes]):
    """ Turn into dataframe for FASTA/FASTQ files, otherwise just return raw data """
    if bool(re.search(r"\.(bam|fasta|fna|ffn|faa|frn|fa|fastq)$", download_file, re.I)):
        if not _module_pandas_available:
            raise MissingOptionalRequirementError('pandas')

        data = data.split("\n", maxsplit=1)

        meta = data[0]
        sequence = data[1].replace("\n", "")  # remove newlines

        return pd.DataFrame({"meta": [meta], "sequence": [sequence]})

    return data


def get_filename_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.path.split("/")[-1]


class DownloadStatus(Enum):
    """An Enum to Describe the current status of a DRS download"""

    SUCCESS = 0
    FAIL = 1


class Blob(AbstractContextManager):
    def __init__(self, id: str, url: str):
        self.__id = id
        self.__url = url
        self.__pool: Optional[urllib3.PoolManager] = None
        self.__connection: Optional[TextIOWrapper] = None
        self.__name = urlparse(self.__url).path.split(r'/')[-1]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__connection and not self.__connection.closed:
            self.__connection.close()
        if self.__pool:
            self.__pool.clear()
        super().__exit__(exc_type, exc_val, exc_tb)

    @property
    def id(self):
        return self.__id

    @property
    def pool(self):
        if not self.__pool:
            self.__pool = urllib3.PoolManager()
        return self.__pool

    @property
    def connection(self):
        if not self.__connection or self.__connection.closed:
            self.__connection = self.pool.request('GET', self.__url, preload_content=False)
        return self.__connection

    @property
    def data(self) -> bytes:
        data = self.connection.read()
        self.__connection.close()
        return data

    @property
    def name(self) -> str:
        return self.__name

    def to_dataframe(self, force: bool = False):
        if self.is_fasta_or_fastq_data() or self.is_csv_data() or self.is_tsv_data() or force:
            # Automatically export the FASTA/FASTQ data as DataFrame object.
            if _module_pandas_available:
                return pd.read_csv(self.__url, sep='\t' if self.is_tsv_data() else ',')
            else:
                raise MissingOptionalRequirementError('pandas')
        else:
            raise ValueError('Unable to export as dataframe as the data is unlikely FASTA/FASTQ/CSV/TSV. You can bypass'
                             'the file type check by setting "force" to true.')

    def is_fasta_or_fastq_data(self):
        return bool(re.search(r"\.(bam|fasta|fna|ffn|faa|frn|fa|fastq)$", self.name, re.I))

    def is_csv_data(self):
        return bool(re.search(r"\.csv$", self.name, re.I))

    def is_tsv_data(self):
        return bool(re.search(r"\.tsv$", self.name, re.I))


class DrsClient(BaseServiceClient):
    """Client for Data Repository Service"""

    def __init__(self, endpoint: ServiceEndpoint):
        super().__init__(endpoint)

        # A lock to prevent race conditions on exit_codes objects
        self.__output_lock = threading.Lock()
        # lock to prevent race conditions for file output
        self.__exit_code_lock = threading.Lock()

        self._events.add_fixed_types('download-ok', 'download-progress', 'download-failure')

    @staticmethod
    def get_adapter_type():
        return 'drs'

    @staticmethod
    def get_supported_service_types() -> List[ServiceType]:
        return [
            DRS_TYPE_V1_1,
        ]

    def exit_download(self, url: str, status: DownloadStatus, message: str = "", exit_codes: dict = None) -> None:
        """
        Report a file download with a status and message

        :param url: The downloaded resource's url
        :param status: The reported status of the download
        :param message: A message describing the reason for setting the status
        :param exit_codes: A shared dict for all reports used by download_files
        """
        if exit_codes is not None:
            with self.__exit_code_lock:
                exit_codes[status][url] = message

    def get_download_url(self,
                         drs_url: str,
                         no_auth: bool = False) -> str:
        """
        Get the URL to download the DRS object
        """
        with self.create_http_session(suppress_error=True, no_auth=no_auth) as session:
            drs_object = DRSObject(drs_url)
            try:
                object_info_response = session.get(
                    urljoin(drs_object.drs_server_url, f'objects/{drs_object.object_id}'))
            except requests.exceptions.ConnectionError:
                raise DrsApiError(f'Connection Error')
            object_info_status_code = object_info_response.status_code

            if object_info_status_code != 200:
                if object_info_status_code == 404:
                    raise DrsApiError(f"DRS object does not exist")
                elif object_info_status_code == 403:
                    raise DrsApiError("Access Denied")
                else:
                    raise DrsApiError("There was an error getting object info from the DRS Client")

            object_info = object_info_response.json()

            if "access_methods" in object_info and object_info['access_methods']:
                for access_method in object_info["access_methods"]:
                    if access_method["type"] != "https":
                        continue
                    # try to use the access_id to get the download url
                    if "access_id" in access_method.keys():
                        object_access_response = session.get(urljoin(drs_object.drs_server_url,
                                                                     f'objects/{drs_object.object_id}/access/{access_method["access_id"]}'))
                        object_access = object_access_response.json()
                        access_url = object_access["url"]
                        self._logger.debug(f'DRS URL {drs_url} -> {access_url} (via access ID)')

                        return access_url
                    # if we have a direct access_url for the access_method, use that
                    elif "access_url" in access_method.keys():
                        access_url = access_method["access_url"]["url"]
                        self._logger.debug(f'DRS URL {drs_url} -> {access_url} (from access URL)')
                        return access_url

                # we couldn't find a download url, exit unsuccessful
                raise NoUsableAccessMethodError()
            else:
                raise NoUsableAccessMethodError()  # next page token, just return

    def get_blob(self, id: Optional[str] = None, url: Optional[str] = None, no_auth: bool = False) -> Blob:
        assert id or url, 'Please at least specify either "id" or "url".'
        assert (id and not url) or (not id and url), 'You can only specify either "id" or "url" but not both of them.'

        if id:
            parsed_base_url = urlparse(self.endpoint.url)
            drs_url = f'drs://{parsed_base_url.netloc}/{id}'
        else:
            drs_url = url

        try:
            download_url = self.get_download_url(drs_url, no_auth=no_auth)
        except InvalidDrsUrlError as e:
            self._logger.info(f'failed to download from {url}: {type(e).__name__}: {e}')
            self._events.dispatch('download-failure',
                                  DownloadFailureEvent.make(drs_url=url,
                                                            reason='Invalid DRS URL'))
            raise e  # Rethrow the error.
        except NoUsableAccessMethodError as e:
            self._logger.info(f'failed to download from {url}: {type(e).__name__}: {e}')
            self._events.dispatch('download-failure',
                                  DownloadFailureEvent.make(drs_url=url,
                                                            reason='No access method'))
            raise e  # Rethrow the error.
        except DrsApiError as e:
            self._logger.info(f'failed to download from {url}: {type(e).__name__}: {e}')
            self._events.dispatch('download-failure',
                                  DownloadFailureEvent.make(drs_url=url,
                                                            reason='Unexpected error while communicating with DRS API',
                                                            error=e))
            raise e  # Rethrow the error.

        return Blob(drs_url, download_url)

    def download_file(
            self,
            url: str,
            output_dir: str,
            display_progress_bar: bool = False,
            output_buffer_list: Optional[list] = None,
            exit_codes: Optional[dict] = None,
            no_auth: bool = False
    ) -> None:
        """
        Download a single DRS resource and output to a file or list

        :param url: The DRS resource url to download
        :param output_dir: The directory to download output to.
        :param display_progress_bar: Display a progress bar for the downloads to standard output
        :param output_buffer_list: If specified, output downloaded data to the list specified in the argument
        :param exit_codes: A shared dictionary of the exit statuses and messages

        .. note:: This will be deprecated in the future release. Please use the "download" method instead.
        """
        try:
            with self.get_blob(url=url, no_auth=no_auth) as output:
                if output_buffer_list is not None and isinstance(output_buffer_list, list):
                    # Append the result to the shared list.
                    try:
                        dataframe = output.to_dataframe()
                        with self.__output_lock:
                            output_buffer_list.append(dataframe)
                        self._events.dispatch('download-ok',
                                              DownloadOkEvent.make(drs_url=url,
                                                                   content=dataframe))
                    except MissingOptionalRequirementError as e:
                        self._events.dispatch('download-failure',
                                              DownloadFailureEvent.make(drs_url=url,
                                                                        reason='Missing optional requirement',
                                                                        error=e))
                        self.exit_download(
                            url,
                            DownloadStatus.FAIL,
                            f'Optional package not installed: {e}',
                            exit_codes
                        )

                        return
                    except ValueError:
                        data = output.data
                        with self.__output_lock:
                            output_buffer_list.append(data)
                        self._events.dispatch('download-ok',
                                              DownloadOkEvent.make(drs_url=url,
                                                                   content=data))
                else:
                    # Write to somewhere.
                    output_file_path = os.path.join(output_dir, output.name)
                    with open(output_file_path, "wb+") as dest:
                        stream_size = int(output.connection.headers["Content-Length"])
                        read_byte_count = 0
                        for chunk in output.connection.stream(1024):
                            read_byte_count += len(chunk)
                            dest.write(chunk)
                            self._events.dispatch('download-progress',
                                                  DownloadProgressEvent.make(drs_url=url,
                                                                             read_byte_count=read_byte_count,
                                                                             total_byte_count=stream_size)
                            )
                    self._events.dispatch('download-ok',
                                          DownloadOkEvent.make(drs_url=url,
                                                               output_file_path=output_file_path))

            self.exit_download(url, DownloadStatus.SUCCESS, "Download Successful", exit_codes)
        except (InvalidDrsUrlError, NoUsableAccessMethodError, DrsApiError) as e:
            self.exit_download(
                url,
                DownloadStatus.FAIL,
                f"{type(e).__name__}: {e}",
                exit_codes,
            )

    def download_files(
            self,
            urls: List[str],
            output_dir: str = os.getcwd(),
            display_progress_bar: bool = False,
            parallel_download: bool = True,
            out: List = None,
            no_auth: bool = False
    ) -> None:
        """
        Download a list of files and output either to files in the current directory or dump to a specified list

        :param urls: A list of DRS resource urls to download
        :param output_dir: The directory to download output to.
        :param display_progress_bar: Display a progress bar for the downloads to standard output
        :param out: If specified, output downloaded data to the list specified in the argument
        :raises: DRSDownloadException if one or more of the downloads fail
        """
        exit_codes = {status: {} for status in DownloadStatus}
        unique_urls = set(urls)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if parallel_download:
            # Define the maximum number of workers, limited to the number of CPUs.
            max_worker_count = os.cpu_count()
            if max_worker_count < 2:
                max_worker_count = 2

            future_to_url_map: Dict[Future, str] = dict()

            with ThreadPoolExecutor(max_workers=max_worker_count) as pool:
                for url in unique_urls:
                    # FIXME make self.download_file to return the data to retain the order of returning value and reduce
                    #  the overhead from locking.
                    future = pool.submit(
                        self.download_file,
                        url=url,
                        output_dir=output_dir,
                        output_buffer_list=out,
                        exit_codes=exit_codes,
                        no_auth=no_auth
                    )
                    future_to_url_map[future] = url

            # Wait for all tasks to complete
            for future in as_completed(future_to_url_map.keys()):
                future.result()
        else:
            for url in unique_urls:
                self.download_file(url=url,
                                   output_dir=output_dir,
                                   output_buffer_list=out,
                                   exit_codes=exit_codes,
                                   display_progress_bar=display_progress_bar)

        # at least one download failed, create exceptions
        failed_downloads = [
            DRSException(msg=msg, url=url)
            for url, msg in exit_codes.get(DownloadStatus.FAIL).items()
        ]
        if len(unique_urls) == len(failed_downloads):
            raise DRSDownloadException(failed_downloads)
        elif len(failed_downloads) > 0:
            self._logger.warning(f'{len(failed_downloads)} out of {len(unique_urls)} download(s) failed unexpectedly')
            index = 0
            for failed_download in failed_downloads:
                self._logger.warning(f'Failure #{index}: {failed_download}')
                index += 1


# This is for partial backward compatibility.
FilesClient = DrsClient
