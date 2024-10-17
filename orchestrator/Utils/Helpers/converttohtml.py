from typing import List
from pydantic import BaseModel

class HTMLTableGenerator:
    @staticmethod
    def convert_to_html(data: List[BaseModel]) -> str:
        if not data:
            return "<p>No data available to display.</p>"        
        field_names = data[0].model_fields.keys()
        html_table = """<table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%;"><thead><tr>"""
        for field in field_names:
            if field != "entity_id":
                html_table += f"<th>{field.replace('_', ' ').title()}</th>"
        html_table += """</tr></thead><tbody>"""
        for item in data:
            html_table += "<tr>"
            for field in field_names:        
                if field != "entity_id":         
                    value = getattr(item, field)
                    html_table += f"<td>{value if value is not None else 'N/A'}</td>"
            html_table += "</tr>"
        html_table += """</tbody></table>"""
        return html_table.replace("\n", "")