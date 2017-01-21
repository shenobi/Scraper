#!/usr/bin/env python
import urllib
import re
import argparse
import sys

b_comment = "<!--"
e_comment = "-->"
email_pattern = r'[\w\.-]+@[\w\.-]+'

def main(url, email, comment):
    try:
        if url.find("http") < 0:
            url = "http://"+url
        page = urllib.urlopen(url).read()
        print "Url: {}\n".format(url)
        if email:
            print "--------------Emails----------------"
            emails = re.findall(email_pattern, page)
            if emails:
                for e in emails:
                    print e
            else:
                print "Emails not found\n"

        if comment:
            comments = []
            print "--------------Comments--------------"
            while True:
                start_index = page.find(b_comment)
                if start_index != -1:
                    end_index = page.find(e_comment, start_index)
                    comments.append(page[start_index:end_index + len(e_comment)])
                    page = page[end_index + len(e_comment):]
                else:
                    break
            if comments:
                for c in comments:
                    print c
            else:
                print "Comments not found"
    except IOError as ioerr:
        print "Unable to connect"
    except Exception as err:
        print "Invalid url specifed"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch emails and comments in HTML page', usage=argparse.SUPPRESS)
    email = None
    comment = None

    parser.add_argument('url', type=str, help='URL to look for')
    parser.add_argument('-e', '--emails', help='Search for emails', action='store_true')
    parser.add_argument('-c', '--comments', help='Search for comments', action='store_true')
    args = parser.parse_args()
    if not args.url:
        parser.error("Missed Url")
    if args.emails:
        email = True
    if args.comments:
        comment = True
    if not email and not comment:
        print "Not action provided (-e,--email or -c,--comments)"
    else:
        main(args.url, email, comment)


