import logfire

def parse_text(file_path:str)->str:
    with logfire.span("text parsed",filename=file_path):
        try:
            with open(file_path,'r',encoding='utf-8',errors='ignore') as f:
                return f.read()
        except Exception as e:
            logfire.error(f"Text parsed failed:{e}")
            raise e