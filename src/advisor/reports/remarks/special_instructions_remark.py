from ..report_item import ReportItem


class SpecialInstructionsRemark(ReportItem):
    def __init__(self, filename, library_name, special_instructions, details_url = None):
        description = f'using dependency library {library_name}.'

        if (special_instructions):
            description = ' '.join([description, special_instructions])
        if (details_url):
            description = ' '.join([description, f' more info at: {details_url}'])
        
        super().__init__(description, filename, item_type=ReportItem.NEUTRAL)
