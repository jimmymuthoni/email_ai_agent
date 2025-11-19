import imaplib
from email import policy
from email.parser import BytesParser
from datetime import datetime
import os
import re
import argparse
from bs4 import BeautifulSoup
import lxml
from dotenv import load_dotenv
import chardet

load_dotenv()

def chunk_text(text, max_length=1000):
    """fnction to process email texts and split then to chunks"""
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"\s*(?:>\s*){2,}", " ", text)
    text = re.sub(r"-{3,}", " ", text)
    text = re.sub(r"_{3,}", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    sentences = re.split(r"(?<=[.!?]) +", text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 < max_length:
            current_chunk += (sentence + " ").strip()
        else:
            chunks.append(current_chunk)
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def save_chunks_to_vault(chunks):
    vault_path = "vault.txt"
    with open(vault_path, "a", encoding="utf-8") as vault_file:
        for chunk in chunks:
            vault_file.write(chunk.strip() + "\n")


def get_text_from_html(html_content):
    soup = BeautifulSoup(html_content, "lxml")
    return soup.get_text()


def safe_decode(payload, charset=None):
    """decoding the emails"""
    if payload is None:
        return ""
    try:
        if charset:
            return payload.decode(charset)
        return payload.decode("utf-8")
    except Exception:
        detected = chardet.detect(payload)["encoding"]
        try:
            return payload.decode(detected or "utf-8", errors="replace")
        except Exception:
            return payload.decode("utf-8", errors="replace")


def save_plain_text_content(email_bytes, email_id):
    """save the decoded emails"""
    msg = BytesParser(policy=policy.default).parsebytes(email_bytes)
    text_content = ""

    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            payload = part.get_payload(decode=True)
            charset = part.get_content_charset() or "utf-8"

            if ctype == "text/plain":
                decoded = safe_decode(payload, charset)
                text_content += decoded

            elif ctype == "text/html":
                decoded_html = safe_decode(payload, charset)
                text_content += get_text_from_html(decoded_html)

    else:
        payload = msg.get_payload(decode=True)
        charset = msg.get_content_charset() or "utf-8"

        if msg.get_content_type() == "text/plain":
            text_content = safe_decode(payload, charset)

        elif msg.get_content_type() == "text/html":
            decoded_html = safe_decode(payload, charset)
            text_content = get_text_from_html(decoded_html)

    chunks = chunk_text(text_content)
    save_chunks_to_vault(chunks)
    return text_content


def search_and_process_emails(imap_client, email_source, search_keyword, start_date, end_date):
    """function that search ang process my emails"""
    search_criteria = "ALL"
    if start_date and end_date:
        search_criteria = f'(SINCE "{start_date}" BEFORE "{end_date}")'
    if search_keyword:
        search_criteria += f' BODY "{search_keyword}"'

    print(f"Using search criteria for {email_source}: {search_criteria}")
    typ, data = imap_client.search(None, search_criteria)

    if typ == "OK":
        email_ids = data[0].split()
        print(f"Found {len(email_ids)} emails matching criteria in {email_source}.")

        for num in email_ids:
            typ, email_data = imap_client.fetch(num, "(RFC822)")
            if typ == "OK":
                email_id = num.decode("utf-8")
                print(f"Downloading and processing email ID: {email_id} from {email_source}")
                save_plain_text_content(email_data[0][1], email_id)
            else:
                print(f"Failed to fetch email ID: {num.decode('utf-8')}")

    else:
        print(f"No emails found in {email_source}.")


def main():
    parser = argparse.ArgumentParser(description="Search and process emails.")
    parser.add_argument("--keyword", default="")
    parser.add_argument("--startdate")
    parser.add_argument("--enddate")
    args = parser.parse_args()

    start_date = None
    end_date = None

    if args.startdate and args.enddate:
        try:
            start_date = datetime.strptime(args.startdate, "%d.%m.%Y").strftime("%d-%b-%Y")
            end_date = datetime.strptime(args.enddate, "%d.%m.%Y").strftime("%d-%b-%Y")
        except ValueError as e:
            print(f"Date error: {e}")
            return
    elif args.startdate or args.enddate:
        print("Both dates required.")
        return

    gmail_username = os.getenv("GMAIL_USERNAME")
    gmail_password = os.getenv("GMAIL_PASSWORD")

    M = imaplib.IMAP4_SSL("imap.gmail.com")
    M.login(gmail_username, gmail_password)
    M.select("inbox")

    search_and_process_emails(M, "Gmail", args.keyword, start_date, end_date)

    M.logout()


if __name__ == "__main__":
    main()
