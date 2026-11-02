import logfire
from pypdf import PdfReader

def parse_pdf(file_path:str)->str:
    with logfire.span("Pdf parsing",filename=file_path):
        try:
            reader=PdfReader(file_path)
            total_pages=len(reader.pages)
            logfire.info(f"PDF has {total_pages} pages")

            text_parts:list[str]=[]
            blank_pages:list[int]=[]

            for i,page in enumerate(reader.pages):
                text=page.extract_text()
                if text.strip():
                    text_parts.append(text)
                else:
                    blank_pages.append(i+1)
            
            # Fallback:use pdfplumber for any pages pypdf returned empty text
            if blank_pages:
                logfire.info(f"pypdf returned blank on pages {blank_pages}-retrying with pdfplumber")
                try:
                    import pdfplumber
                    with pdfplumber.open(file_path) as pdf:
                        for page_num in blank_pages:
                            page=pdf.pages[page_num-1]
                            text=page.extract_text()
                            if text.strip():
                                text_parts.append(text)
                except Exception as e:
                    logfire.error(f"Error parsing PDF with pdfplumber: {e}")
            
            full_text="\n".join(text_parts)

            if not full_text.strip():
                logfire.warning(f"No text extracted from {file_path}")
            else:
                logfire.info(f'extracted {len(full_text)} charecters')

            return full_text
        except Exception as e:
            logfire.error(f"pdf parsed failed for {file_path}:{e}")
            raise e