
from typing import List

from os import linesep as osLineSep


from click import command
from click import option
from click import version_option
from click import format_filename
from click import echo as clickEcho
from click import secho as clickSEcho

__version__ = "0.1.1"

INPUT_SUFFIX:  str = '.csv'
OUTPUT_SUFFIX: str = '.md'

COMMA:             str = ','
COMMENT_INDICATOR: str = '#'
HEADER_INDICATOR:  str = 'Repository'

INDEX_HEADER:       int = 0
INDEX_ISSUE_NUMBER: int = 2
INDEX_DESCRIPTION:  int = 4
INDEX_URL:          int = 8


class Epr2Md:

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

    def convert(self):
        issueLines: List[str] = self._getIssueLines()
        clickEcho(f'Lines read: {len(issueLines)}')

        with open(self._outputFileName, 'w') as outputFile:
            for issueLine in issueLines:
                if issueLine == '':
                    continue

                issuePieces:      List[str] = issueLine.split(COMMA)
                headerIndicator: str        = issuePieces[INDEX_HEADER]
                if headerIndicator == HEADER_INDICATOR:
                    continue

                issueNumber: str = issuePieces[INDEX_ISSUE_NUMBER]
                url:         str = issuePieces[INDEX_URL]
                description: str = issuePieces[INDEX_DESCRIPTION]
                mdLine:      str = f'* [{issueNumber}]({url}) {description}{osLineSep}'
                # clickEcho(f'{mdLine}')
                outputFile.write(mdLine)

    def _getValidIssueNumber(self, issueLine: str) -> str:
        """"""

    def _getIssueLines(self) -> List[str]:

        with open(self._inputFileName, "r") as inputFile:
            clickEcho(f'Reading: {format_filename(self._inputFileName)}')
            cvsData: str = inputFile.read()

            clickEcho(f'Characters read: {len(cvsData)}')
            issueLines: List[str] = cvsData.split(osLineSep)

        return issueLines


@command()
@version_option(version=f'{__version__}', message='%(version)s')
@option('-i', '--input-file', required=True, help='The input .csv file to convert.')
@option('-o', '--output-file', required=False, help='The output markdown file.')
def commandHandler(input_file: str, output_file: str):

    epr2md: Epr2Md = Epr2Md(inputFileName=input_file, outputFileName=output_file)

    epr2md.convert()


if __name__ == "__main__":

    commandHandler()
