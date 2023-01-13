from ..report_item import ReportItem
from ...helpers.version_comparer import VersionComparer


class VersionRemark(ReportItem):
    def __init__(self,
                filename,
                lineno,
                name,
                description=None,
                details=None,
                min_version=None,
                recommended_version=None,
                installed_version=None,
                details_url=None,
                override_text=None,
                item_type=ReportItem.NEUTRAL):
        
        if override_text:
            description = override_text
        
        else:
            meets_min_version = False
            if description == None:
                description = f'{name} is present.'
            
            if details:
                description = ' '.join([description, details])
            if min_version:
                description = ' '.join([description, f'min version {min_version} is required.'])
                if installed_version and VersionComparer.compare(installed_version, min_version) >= 0:
                    item_type = ReportItem.POSITIVE
                    meets_min_version = True
                elif installed_version:
                    item_type = ReportItem.NEGATIVE
            if recommended_version:
                description = ' '.join([description, f'version {recommended_version} or above is recommended.'])
                if installed_version and VersionComparer.compare(installed_version, recommended_version) >= 0:
                    item_type = ReportItem.POSITIVE
                elif installed_version and not meets_min_version:
                    item_type = ReportItem.NEGATIVE
            if installed_version:
                description = ' '.join([description, f'we detected that you have version {installed_version}.'])
            if details_url:
                description = ' '.join([description, f'see {details_url} for more details.'])

        super().__init__(filename=filename,
                         description=description,
                         lineno=lineno,
                         item_type=item_type)