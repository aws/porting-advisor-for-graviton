import xlsxwriter
from ..manifester.manifester import Manifester
from .report import Report


class DependencyReport(Report):
    """Generates a CSV with just the dependencies found."""

    def __init__(self, root_directory, target_os='linux'):
        super().__init__(root_directory, target_os)
        self.send_filename = True
        self.self_process = True

    def process(self, args):
        manifester = Manifester()
        self.remarks.extend(manifester.scan_folder(args.root))

    def write(self, output_file, report_errors=False, report_remarks=True, include_summary=False):
        self.write_items(output_file, self.remarks)
    
    def write_items(self, output_file, items):
        workbook = xlsxwriter.Workbook(output_file)
        classified = {}

        for item in items:
            if item.tool not in classified:
                classified[item.tool] = [item]
            else:
                classified[item.tool].append(item)
        
        for tool in classified:
            worksheet = workbook.add_worksheet(tool)
            self._write_header(worksheet)
            dependencies = classified[tool]
            
            row = 1
            for dependency in dependencies:
                if dependency.version:
                    version = dependency.version
                else:
                    version = 'LATEST' 
                row_to_write = [dependency.name, version, dependency.tool, dependency.filename]
                col = 0
                for column in row_to_write:
                    worksheet.write(row, col, column)
                    col += 1
                row += 1
        workbook.close()

    def _write_header(self, worksheet):
        headers = ['component', 'version', 'origin', 'filename']
        col = 0
        for header in headers:
            worksheet.write(0, col, header)
            col += 1