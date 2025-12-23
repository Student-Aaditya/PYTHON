# sync_service.py
from db_utils import get_all_tables, fetch_table_data
from json_format import save_table_json
from merge_json import merge_all

def sync_all():
    tables = get_all_tables()

    for table in tables:
        data = fetch_table_data(table)
        save_table_json(table, data)

    merge_all()
    print("✅ Sync completed")
