from __future__ import print_function
from sendMail import send_message, create_message
import datetime
import re
import feedparser
from personal_variables import receiver_mail_address, sender_mail_address, feed_urls

now = datetime.datetime.now()
date_str = str(now.date())


def strip_html(text):
    return re.sub("<[^<]+?>", "", text)


def get_arxiv_mail(feed_url):
    """Generates the body content of email.

    Args:
        feed_url: Link to arxiv RSS feed of a particular subject class (ex: http://arxiv.org/rss/cs.SE for Computer Science - Software Engineering)

    Returns:
        str: email body listing relevant papers
    """
    feed = feedparser.parse(feed_url)
    msg = ["<h1>arXiv results for {}</h1>".format(date_str)]

    for entry in feed.entries:
        msg.append("<h2>{}</h2>".format(entry.title))
        msg.append("<h3>{}</h3>".format(strip_html(entry.author)))
        msg.append("<p>{}</p>".format(strip_html(entry.description)))
        num = "arXiv:" + entry["id"].split("/")[-1]
        link = '<a href="{}">{}</a>'.format(entry["id"], num)
        pdf_link = '[<a href="{}">pdf</a>]'.format(entry.id.replace("abs", "pdf"))
        msg.append(link + " " + pdf_link)
    msg = "".join(msg)
    return msg


def send_todays_arxiv(sender, to):
    """Sends arxiv papers of interest via email.

    Args:
        sender: email address of the sender
        to: email address of the recipient

    Returns:
        str[]: list of IDs for each email sent.
    """
    msg_ids = []
    for feed_url in feed_urls:
        message_text = get_arxiv_mail(feed_url)
        subject = "Today's arXiv {}".format(date_str)
        message = create_message(sender, to, subject, message_text)
        sent_message_id = send_message(message)
        msg_ids.append(sent_message_id)
    return msg_ids


def main():
    return send_todays_arxiv(sender=sender_mail_address, to=receiver_mail_address)


if __name__ == "__main__":
    main()
