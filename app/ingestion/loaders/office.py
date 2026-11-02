import logfire
from unstructured.partition.auto import partition

def parse_office(file_path:str):
    with logfire.span("office document parsing",filename=file_path):
        try:
            elements=partition(filename=file_path)
            full_text='\n'.join([str(el) for el in elements])

            if not full_text.strip():
                logfire.warning(f"Unstructured returned empty text for {file_path}")
            else:
                logfire.info(f"Successfully parsed {file_path}")

            return full_text
        except Exception as e:
            logfire.error(f"Error parsing office document: {e}")
            raise e