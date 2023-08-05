
import zlib


from click import command
from click import option
from click import version_option
from click import format_filename
from click import echo as clickEcho
from click import secho as clickSEcho

__version__ = "0.1.1"

INPUT_SUFFIX:  str = '.put'
OUTPUT_SUFFIX: str = '.xml'


class Pyut2XML:

    def __init__(self, inputFileName: str, outputFileName: str):

        if INPUT_SUFFIX in inputFileName:
            self._inputFileName: str = inputFileName
        else:
            self._inputFileName = f'{inputFileName}{INPUT_SUFFIX}'
        if outputFileName is None:
            clickSEcho('Using input file name as base for output file name', bold=True)
            baseName: str = inputFileName.replace(INPUT_SUFFIX, '')
            self._outputFileName = f'{baseName}{OUTPUT_SUFFIX}'
        elif OUTPUT_SUFFIX in outputFileName:
            self._outputFileName: str = outputFileName
        else:
            self._outputFileName = f'{outputFileName}{OUTPUT_SUFFIX}'

    def decompress(self):
        try:
            with open(self._inputFileName, "rb") as inputFile:
                clickEcho(f'Inflating: {format_filename(self._inputFileName)}')
                compressedData: bytes = inputFile.read()

                clickEcho(f'Bytes read: {len(compressedData)}')
                xmlBytes:  bytes = zlib.decompress(compressedData)  # has b'....' around it
                xmlString: str   = xmlBytes.decode()

                clickEcho(f'Writing {len(xmlString)} bytes to {format_filename(self._outputFileName)}')
                with open(self._outputFileName, 'w') as outputFile:
                    outputFile.write(xmlString)
        except (ValueError, Exception) as e:
            clickEcho(f'Error:  {e}')


@command()
@version_option(version=f'{__version__}', message='%(version)s')
@option('-i', '--input-file', required=True, help='The input .put file to decompress.')
@option('-o', '--output-file', required=False, help='The output xml file.')
def commandHandler(input_file: str, output_file: str):

    pyut2XML: Pyut2XML = Pyut2XML(inputFileName=input_file, outputFileName=output_file)

    pyut2XML.decompress()


if __name__ == "__main__":

    commandHandler()
