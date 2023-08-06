#!/usr/bin/env python

import os
import argparse
import getpass
import openai_summarizer
import sys
from datetime import datetime

def error(message, exit: bool = False):
    print(message, file=sys.stderr)
    if exit:
        sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(description="Summarize emails using OpenAI's bot.")
    parser.add_argument(
        "-m", 
        "--mailhost", 
        help="The IMAP server to connect to.", 
        required=True,
        type=str
    )
    parser.add_argument(
        "-u", 
        "--email", 
        help="The email address to read emails of.", 
        required=True,
        type=str
    )
    parser.add_argument(
        "--password",
        default=os.getenv('EMAIL_SUMMARIZER_MAIL_PASSWORD'),
        help="The password for the email.",
        type=str
    )
    parser.add_argument(
        "--apikey",
        default=os.getenv('OPENAI_API_KEY'),
        help="The API key from OpenAI.",
        type=str
    )
    parser.add_argument(
        "--prompt-password", 
        action=argparse.BooleanOptionalAction,
        help="Accept password for the email from stdin.", 
    )
    parser.add_argument(
        "--prompt-apikey", 
        action=argparse.BooleanOptionalAction,
        help="Accept OpenAI api key from stdin.", 
    )
    opts = parser.parse_args()
    
    if opts.password is None and opts.prompt_password:
        opts.password = getpass.getpass(prompt=f"Enter the password for {opts.email}:\n")
    if opts.apikey is None and opts.prompt_apikey:
        opts.apikey = getpass.getpass(prompt=f"Enter the OpenAI api key:\n")
    if opts.password is None:
        error("No password specified. Use `--prompt-password` for accepting password of the email from stdin. Or set the `EMAIL_SUMMARIZER_MAIL_PASSWORD` environment variable before running this script.")
    if opts.apikey is None:
        error("No OpenAI API key specified. Use `--prompt-apikey` for accepting the OpenAI api key from stdin. Or set the `OPENAI_API_KEY` environment variable before running this script.")
    if opts.apikey is None and opts.password is None:
        error("Need email credentials and OpenAI api key to run this script.", exit=True)

    return opts


def main():
    opts = parse_args()

    mailbox = openai_summarizer.Mailbox(opts.mailhost, opts.email, opts.password)
    openai_client = openai_summarizer.EmailSummarizerClient(apikey=opts.apikey)
    email_msgs = list(mailbox.fetch_new_messages())

    if len(email_msgs) == 0:
        print(f"No new messages found as of {datetime.now().isoformat()}")
    else:
        print(f"Found {len(email_msgs)} unread emails. Here are their summaries.")
        print(f"Please note that these emails will be marked as read as they have been accessed now.\n\n")
        for email_msg in email_msgs:
            summary = email_msg.summarize(client=openai_client)
            print(f"From: {email_msg.from_}")
            print(f"To: {email_msg.to}")
            print(f"Date: {email_msg.date}")
            print(f"Subject: {email_msg.subject}")
            print(f"Summary: {summary}\n")
            print("========================\n\n")

if __name__ == '__main__':
    main()

