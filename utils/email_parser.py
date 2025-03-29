import email
from email.policy import default


def parse_email(raw_email):
    """解析原始邮件内容"""
    msg = email.message_from_string(raw_email, policy=default)

    return {
        'from': msg['from'],
        'to': msg['to'],
        'subject': msg['subject'],
        'date': msg['date'],
        'body': get_email_body(msg)
    }


def get_email_body(msg):
    """提取邮件正文内容"""
    body = []
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                body.append(part.get_payload(decode=True).decode('utf-8', errors='ignore'))
    else:
        body.append(msg.get_payload(decode=True).decode('utf-8', errors='ignore'))
    return "\n".join(body)