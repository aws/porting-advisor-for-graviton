from ..report_item import ReportItem
from .version_remark import VersionRemark


class ToolVersionRemark(VersionRemark):
    def __init__(self,
                description,
                min_version,
                recommended_version=None,
                installed_version=None,
                details_url=None,
                override_text=None,
                item_type=ReportItem.POSITIVE):
        
        super().__init__(filename=None,
                        lineno=None,
                        name=None,
                        description=description,
                        details=None,
                        min_version=min_version,
                        recommended_version=recommended_version,
                        installed_version=installed_version,
                        details_url=details_url,
                        override_text=override_text,
                        item_type=item_type)