"""The base docstr command line interface through ConfigArgParse."""
from datetime import datetime
import logging
import os


# TODO docstr safe writing of files to disc, iff necessary
def create_filepath(
    filepath,
    overwrite=False,
    datetime_fmt='_%Y-%m-%d_%H-%M-%S.%f',
):
    """Ensures the directories along the filepath exists. If the file exists
    and overwrite is False, then the datetime is appeneded to the filename
    while respecting the extention.

    Note
    ----
    If there is no file extension, determined via existence of a period at the
    end of the filepath with no filepath separator in the part of the path that
    follows the period, then the datetime is appeneded to the end of the file
    if it already exists.
    """
    # Check if file already exists
    if not overwrite and os.path.isfile(filepath):
        logging.warning(
            ' '.join([
                '`overwrite` is False to prevent overwriting existing files',
                'and there is an existing file at the given filepath: `%s`',
            ]),
            filepath,
        )

        # NOTE beware possibility of program writing the same file in parallel
        filepath = filename_append(
            filepath,
            datetime.now().strftime(datetime_fmt),
        )

        logging.warning('The filepath has been changed to: %s', filepath)
    else:
        # Ensure the directory exists
        dir_path = os.path.dirname(filepath)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

    return filepath



# TODO logging CAP module
def add_logging_args(parser, log_level='WARNING'):
    """Adds the logging args to the arg parser."""
    log_args = parser.add_argument_group('logging', 'Python logging arguments')

    log_args.add_argument(
        '--log_level',
        default=log_level,
        help='The log level to be logged.',
        choices=['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        dest='logging.level',
    )

    log_args.add_argument(
        '--log_filename',
        default=None,
        help='The log file to be written to.',
        dest='logging.filename',
    )

    log_args.add_argument(
        '--log_filemode',
        default='a',
        choices=['a', 'w', 'w+'],
        help='The filemode for writing to the log file.',
        dest='logging.filemode',
    )

    log_args.add_argument(
        '--log_format',
        default='%(asctime)s; %(levelname)s: %(message)s',
        help='The logging format.',
        dest='logging.format',
    )

    log_args.add_argument(
        '--log_datefmt',
        default=None,
        #default='%Y-%m-%d_%H-%M-%S',
        help='The logging date/time format.',
        dest='logging.datefmt',
    )

    log_args.add_argument(
        '--log_overwrite',
        action='store_true',
        help=' '.join([
            'If file already exists, giving this flag overwrites that log',
            'file if filemode is "w", otherwise the datetime is appended to',
            'the log filename to avoid overwriting the existing log file.',
        ]),
        dest='logging.overwrite',
    )


def set_logging(log_args):
    """Given an argparse.Namespace, initialize the python logging."""
    # Set logging configuration
    numeric_level = getattr(logging, log_args.level.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level given: {log_args.level}')

    if log_args.filename is not None:
        overwrite = (
            log_args.overwrite
            or log_args.filemode not in {'w', 'w+'}
        )

        log_args.filename = create_filepath(log_args.filename, overwrite)

        logging.basicConfig(
            filename=log_args.filename,
            filemode=log_args.filemode,
            level=numeric_level,
            format=log_args.format,
            datefmt=log_args.datefmt,
        )

        if log_args.filemode == 'a':
            # Adding some form of line break for ease of searching logs.
            logging.info('Start of new logging session.')
    else:
        logging.basicConfig(
            level=numeric_level,
            format=log_args.format,
            datefmt=log_args.datefmt,
        )
