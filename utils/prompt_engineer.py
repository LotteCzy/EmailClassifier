def build_classification_prompt(email_data, categories):
    return f"""请分析以下电子邮件并分类到最合适的类别中：

发件人：{email_data['from']}
主题：{email_data['subject']}
日期：{email_data['date']}

邮件内容：
{email_data['body']}

可选分类类别：{", ".join(categories)}

请只返回类别名称，不要包含任何其他解释或说明。"""

def build_few_shot_classification_prompt(email_data, categories, examples):
    return f"""请分析以下电子邮件并分类到最合适的类别中：

发件人：{email_data['from']}
主题：{email_data['subject']}
日期：{email_data['date']}

邮件内容：
{email_data['body']}

可选分类类别：{", ".join(categories)}

请只返回类别名称，不要包含任何其他解释或说明。
以下是电子邮件分类示例：

{examples}

"""