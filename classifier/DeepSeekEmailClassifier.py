# classifier.py
import requests
import json
from config import DEEPSEEK_CONFIG
from utils.email_parser import parse_email
from utils.prompt_engineer import build_classification_prompt, build_few_shot_classification_prompt


class DeepSeekEmailClassifier:
    def __init__(self, categories, examples_path):
        self.categories = categories
        self.examples = self._load_examples(examples_path)
        self.api_url = f"{DEEPSEEK_CONFIG['base_url']}/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {DEEPSEEK_CONFIG['api_key']}",
            "Content-Type": "application/json"
        }

    def _load_examples(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def classify(self, raw_email):
        email_data = parse_email(raw_email)
        # 构建示例部分
        examples_text = "\n\n".join(
            f"邮件:\n{ex['email']}\n类别: {ex['category']}"
            for ex in self.examples
        )

        # prompt = build_classification_prompt(email_data, self.categories)
        prompt = build_few_shot_classification_prompt(email_data, self.categories, examples_text)


        payload = {
            "model": DEEPSEEK_CONFIG["model"],
            "messages": [
                {"role": "system", "content": "你是一个专业的电子邮件分类助手"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 100
        }
        print(payload)

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=DEEPSEEK_CONFIG["timeout"]
            )
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"API调用失败: {str(e)}")
            return "unknown"


# 示例使用
if __name__ == "__main__":
    classifier = DeepSeekEmailClassifier(
        categories=["工作", "个人", "促销", "垃圾邮件", "重要"]
    )

    test_email = """
    From: 人力资源部 <hr@company.com>
    Subject: 关于年度绩效考核的通知
    Date: Mon, 20 May 2024 10:00:00 +0800

    各位同事：
    年度绩效考核将于下周开始，请按时提交相关材料。
    """

    print("分类结果:", classifier.classify(test_email))