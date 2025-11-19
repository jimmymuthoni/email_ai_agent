import re

class EmailCollector:
    """class to collect and process emails"""
    def __init__(self):
        pass

    def chunck_text(self,text, max_length=1000):
        """
        This mothod normalize text(email) and return list of chunks
        normalize unicode characters to ASCII rep
        remove sequence of >> used in forwarded emails
        remove sequence of dashes, underscore and spaces
        stripping white space
        replace url with single space or remoce them
        normalize white space into singlr space
        """
        text = text.encode("ascii","ignore").decode("ascii")
        text = re.sub(r"\s*(?:>\s*){2,}"," ",text)
        text = re.sub(r"-{3,}"," ",text)
        text = re.sub(r"_{3}"," ",text)
        text = re.sub(r"\s{2,}"," ", text)
        text = re.sub(r"\s+"," ", text)
        text = re.sub(r"https?://\S+|www\.\S+","",text)
        text = re.sub(r"\s+"," ",text).split()

        # Split text into sentences while preserving punctuation
        sentences = re.split(r"(?<=[.!?]) +",text)
        chunks = []
        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 < max_length:
                current_chunk += (sentence + " ").strip()
            else:
                chunks.append(current_chunk)
        if current_chunk:
            chunks.append(current_chunk)

        return chunks


