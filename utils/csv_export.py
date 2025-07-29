# utils/csv_export.py
import io

def export_to_csv(df):
    buffer = io.StringIO()
    df.to_csv(buffer, index=False, encoding='utf-8')
    buffer.seek(0)
    return buffer.getvalue()