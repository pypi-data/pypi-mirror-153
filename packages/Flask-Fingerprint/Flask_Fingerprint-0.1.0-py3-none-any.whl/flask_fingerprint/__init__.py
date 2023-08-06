import os
import re
import json
import logging
import hashlib

from typing import Any, Dict, Optional

from flask import Flask, current_app

from .helpers import get_hash, is_allowed


logger = logging.getLogger(__name__)


__all__ = [
    # Helpers
    'get_hash',
    'is_allowed',
]


class Fingerprint:
    """
    Flask extension for fingerprinting static assets
    """

    def __init__(self, app: Optional[Flask] = None, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Creates 'Fingerprint' instance

        :param app: Flask.app.Flask Current application
        :param config: dict Configuration object

        :return: None
        """

        # Apply configuration
        self.config = config or {}

        # Initialize extension
        if app is not None:
            self.init_app(app)


    def init_app(self, app: Flask, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Integrates extension with 'Flask' application

        :param app: Flask.app.Flask Current application
        :param config: dict Configuration object

        :return: None
        """

        # Print debugging information
        logger.debug(self.config)

        # Create data array
        self.manifest: Dict[str, str] = {}

        # If 'query' mode deactivated ..
        if not self.config.get('query', False):
            # .. attempt to ..
            try:
                # .. determine manifest file
                manifest_file: str = self.config.get('manifest', os.path.join(app.static_folder, 'manifest.json'))

                # .. load its contents
                with app.open_resource(manifest_file) as file:
                    self.manifest: Dict[str, str] = json.load(file)

                logger.debug('Busting assets using "{}"'.format(manifest_file))

            # .. otherwise ..
            except:
                # .. report back
                logger.debug('Busting assets manually')

        # If no data available ..
        if not self.manifest:
            # .. iterate over static assets
            for root, dirs, filenames in os.walk(app.static_folder):
                # Iterate over files
                for filename in filenames:
                    # Determine file extension
                    extension = os.path.splitext(filename)[1]

                    # Skip unallowed file extensions
                    if not is_allowed(extension, self.config.get('extensions', ['css', 'js'])):
                        continue

                    # Build filepath
                    path = os.path.join(root, filename)

                    # Determine relative path to original file
                    rel_path = os.path.relpath(path, app.static_folder)

                    # If file was hashed before ..
                    if get_hash(filename):
                        # .. use it directly
                        rev_path = rel_path

                    # .. otherwise ..
                    else:
                        # .. generate file hash ..
                        with open(path, 'rb') as file:
                            # .. from its contents
                            file_hash = hashlib.md5(file.read()).hexdigest()

                        # Determine hash size
                        hash_size = self.config.get('hash_size', 8)

                        # If shorter than length of file hash ..
                        if hash_size < len(file_hash):
                            # .. adjust file hash accordingly
                            file_hash = file_hash[:hash_size]

                        logger.debug('Computing hash "{}" for file "{}"'.format(file_hash, path))

                        # Build relative path to busted file
                        rev_path = rel_path.replace(extension, '.' + file_hash + extension)

                    # Store both variants in manifest
                    self.manifest[rel_path] = rev_path


        @app.url_defaults
        def fingerprint(endpoint: str, values: Dict[str, Any]) -> None:
            """
            Replaces static assets with their busted revisions

            :param endpoint: str Endpoint type
            :param values: dict File information

            :return: None
            """

            # Hook into static file URL generation
            if endpoint == 'static':
                # Get static folder name
                static_folder = os.path.basename(current_app.static_folder)

                # Fetch busted filename for current file ..
                # (1) .. without prefix, eg 'scripts/main.js'
                filename = self.manifest.get(values.get('filename'))

                # (2) .. prefixing static folder name, eg 'static/scripts/main.js'
                if filename is None:
                    filename = self.manifest.get(os.path.join(static_folder, values.get('filename')))

                    if filename is not None:
                        filename = os.path.relpath(filename, static_folder)

                if filename is not None:
                    # If 'query' mode enabled ..
                    if self.config.get('query', False):
                        # .. use file hash as query parameter
                        values['v'] = get_hash(filename)

                    # .. otherwise ..
                    else:
                        # .. replace unbusted with busted filename
                        values['filename'] = filename
