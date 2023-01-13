from ..report_item import ReportItem
from .version_remark import VersionRemark


class DependencyVersionRemark(VersionRemark):
    def __init__(self,
                filename,
                lineno,
                library_name,
                details=None,
                min_version=None,
                recommended_version=None,
                installed_version=None,
                details_url=None,
                override_text=None,
                item_type=ReportItem.NEUTRAL):
        
        description = f'dependency library {library_name} is present.'

        super().__init__(filename=filename,
                        lineno=lineno,
                        name=library_name,
                        description=description,
                        details=details,
                        min_version=min_version,
                        recommended_version=recommended_version,
                        installed_version=installed_version,
                        details_url=details_url,
                        override_text=override_text,
                        item_type=item_type)