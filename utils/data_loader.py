import os
import pandas as pd
from email.parser import Parser


def load_enron_dataset(path):
    emails = []
    labels = []

    for root, dirs, files in os.walk(path):
        for file in files:
            try:
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    email = Parser().parsestr(f.read())
                    emails.append(email.get_payload())
                    labels.append(os.path.basename(root))  # 文件夹名作为标签
            except:
                continue

    return pd.DataFrame({'text': emails, 'label': labels})