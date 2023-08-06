import io
import urllib
import zipfile
import logging

from . import LOGGER_NAME
from .HTTPCalller import HTTPCaller

log = logging.getLogger(LOGGER_NAME)


class DatalakeHandler:
    def __init__(self):
        self.caller = HTTPCaller()

    def search_file(self, file_name, file_type=None, group_name=None, size=100, from_page=0):
        '''
        Searching Method to find files on the datalake of the current stage
        for given file name, and optionally group_name or type

        :param file_name: name of the file stored on the lake group
        :param file_type: datalake file type: NCSV, SOURCE, JUPYTER, ...
        :param group_name: group on datalake where to search; if None, in the entire datalake
        :param size: size of the results to return, most recent first
        :param from_page: iteration parameter

        :return: the file matches on the datalake and their attributes
        '''

        log.debug(f'Search file: {file_name} of type {file_type} on group {group_name}')

        # Prepare query parameters
        init_query = {"name": file_name, "type": file_type, "uuid": None, "groupName": group_name}
        query = format_query(init_query)

        path = f'/file/search?size={size}&from={from_page}&query={query}'
        r = self.caller.get(path)

        log.debug(f'{r.url} \n {r.request.headers} \n {r.json()}')
        return r.json()

    def get_info_from_id(self, file_id):
        '''
        Searching Method to find the metadata of the file with given ID

        :param file_id: ID of the file form datalake
        :return: the file metadata as dictionary
        '''
        log.debug(f'Get Info from Id: {file_id}')

        path = f'/file/search?size=1&from=0&query=uuid%3D{file_id}'
        r = self.caller.get(path)

        log.debug(f'{r.url} \n {r.request.headers} \n {r.json()}')

        return r.json()

    def download_by_id(self, file_id, dest_file_name=None, save=False, unzip=False):
        '''
        Download the file according to its file_id from the datalake.

        If Save == True, it saved the file locally to the path provided in dest_file_name,
        otherwise with the original name in the root folder.

        If save == False, it returns a io.BytesIO object (that can be read for example as csv by pandas).

        :param file_id: hash ID of the file on the dalake
        :param dest_file_name: file name as saved on the hard disk drive. Default is None (meaning the original name of the file)
        :param: save: if True, saves the file locally with dest_file_name, otherwise return a BytesIO object
        :param unzip: if True, unzip the file (if saved as .tar or .zip on the lake) after saving it locally

        :return: None if file is saved locally, io.BytesIO object otherwise
        '''

        # Retrieve the file on the Datalake (S3)
        path = '/file/' + file_id

        # Get headers for S3 request
        data_headers = self.caller.get(path, headers={}).headers
        log.debug('Data Headers: {}'.format(data_headers))

        if 'Location' not in data_headers.keys():
            raise ConnectionError('No Location field found in the data headers')

        else:
            # Get the file ID from S3 service
            file_response = self.caller.get_from_S3(data_headers['Location'])

        if save:
            # Download & Save the file locally
            log.info(f'Download File by Id: {file_id}')

            # Take file name if None is passed
            if dest_file_name is None:
                # Look for the file metadata based on ID
                try:
                    file_meta = self.get_info_from_id(file_id)['items'][0]
                except:
                    log.error('No file_meta - nothing can be found in items field.')
                    raise Exception('No file_meta - nothing can be found in items field.')

                log.debug('File metadata found on datalake from ID: {}'.format(file_meta))
                dest_file_name = file_meta['fileName']

            # save the file to the current folder
            with open(dest_file_name, "wb") as input_file:
                input_file.write(file_response.content)

                log.info('Downloaded File saved as {}'.format(dest_file_name))

            if unzip:
                with zipfile.ZipFile(dest_file_name, 'r') as zip_ref:
                    zip_ref.extractall()
                log.info('Archive file unzipped')

            log.info('File with ID {} downloaded and saved as {}'.format(file_id, dest_file_name))
            return None

        else:
            # Keep the file as io.BytesIO object
            log.info('File obtained from Datalake as BytesIO object')
            return io.BytesIO(file_response.content)

    def download_by_name(self, file_name, group_name, file_type=None, dest_file_name=None, save=False, unzip=False):
        '''
        Download a file from the data lake given its name & group.
        It returns by default the most recent occurency of the file.

        If group is None, it returns the file according to its name only, the most recent one from any group.
        If file_type is 'SOURCE' by default

        If Save == True, it saved the file locally to the path provided in dest_file_name,
        otherwise with the original name in the root folder.
        If save == False, it returns a io.BytesIO object (that can be read for example as csv by pandas).

        :param: file_name: the name of file to download
        :param: group_name: the name of the datalake group. if None, it takes the file from any group
        :param: file_type: file type of the file on the DataLake - SOURCE, NCSV, GDP ...
        :param: dest_file_name: file name as saved on the hard disk drive. Default is None (meaning the original name of the file)
        :param: save: if True, saves the file locally with dest_file_name, otherwise return a BytesIO object
        :param unzip: if True, unzip the file (if saved as .tar or .zip on the lake) after saving it locally

        :return:
        '''

        log.info(f'Download File by Name: {file_name} of type {file_type} from group {group_name}')

        # Look for the file on the datalake
        query = self.search_file(file_name=file_name, file_type=file_type, group_name=group_name)
        log.debug(f'Download by name: {query}')

        if 'items' not in query:
            raise ValueError('Encountered problem with downloading file : {}'.format(query['message']))

        if len(query['items']) == 0:
            raise ValueError(
                'No file {} found on group {} with type {}: {}'.format(file_name, group_name, file_type, query))

        else:
            # Download by ID of the found file
            fid = query['items'][0]['fid']
            return self.download_by_id(file_id=fid, dest_file_name=dest_file_name, save=save, unzip=unzip)

    def upload_file(self, file, group_name, file_upload_name=None, file_type='SOURCE', partial_update=False):
        '''
        Upload the file to the datalake group with the given type (SOURCE as default)

        :param: file: either the path on the disk of the file to upload either the object directly
        :param: group_name: the name of the datalake group. if None, goes to the group where the pipeline is saved
        :param: file_upload_name: if not None, upload the file on the datalake with a different name
        :param: file_type: file type to save the file in the lake - SOURCE (default), NCSV ...

        :return: file unique ID on the datalake & the name on the datalake
        '''

        # Raise an error if the passed file is an object in RAM & no upload name was given
        if (not isinstance(file, str)) and (file_upload_name is None):
            raise ValueError('If uploading a file from RAM the file_upload_name must be given')

        # Get the uploaded file name from path (original name) if none was passed
        file_name = file.split('/')[-1] if (file_upload_name is None) and isinstance(file, str) else file_upload_name

        log.info(f'Upload File with Name: {file_name} of type {file_type} to group {group_name}')

        p_u = [{"name":"PARTIAL_UPDATE","value":"true"}] if partial_update is True else []

        # PAYLOAD for the upload of the file
        payload = {"groupName": group_name,
                   "fileName": file_name,
                   "fileType": file_type,
                   "fields": p_u}

        log.debug(f'Payload: {payload}')

        return self.caller.file_uploader(payload, file), file_name


# ---------------------
# HELPER functions
# --------------------
def format_query(init_query):
    '''Properly Format the query dictionary for the API Call'''

    query = {}

    for key, value in init_query.items():
        if value is not None:
            query[key] = value

    # Format as a string for http request
    s = ''
    for key, value in dict.items(query):
        s += '{}={}&'.format(key, value)

    # Encode for URL
    encoded_s = urllib.parse.quote(s[:-1])

    log.debug(f'Formatting query. \nInitial query: {init_query} \nFormatted query: {encoded_s}')

    return encoded_s
