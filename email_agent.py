# email_agent.py
import imaplib
import email
import ssl
import time
from imap_tools import MailBox, AND
from classifier.DeepSeekEmailClassifier import DeepSeekEmailClassifier

class EmailClassificationAgent:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.classifier = DeepSeekEmailClassifier(
            categories=["会议邀请", "问卷调查", "工单流程审批", "个人", "促销", "垃圾邮件", "重要"],
            examples_path= "data/few_shot_examples.json"
        )


    def run(self):
        """主运行循环"""
        print("启动邮件分类Agent...")
        while True:
            self.process_unread_emails()
            time.sleep(30)  # 每5分钟检查一次


    def process_unread_emails(self):
        """处理未读邮件"""
        try:
            with self._connect() as mail:
                mail.select('inbox')
                status, messages = mail.search(None, 'ALL')
                if status != 'OK' or not messages[0]:
                    return

                for num in messages[0].split():
                    self._process_single_email(mail, num)
        except Exception as e:
            print(f"处理邮件时出错: {str(e)}")


    def _connect(self):
        """连接IMAP服务器"""
        imaplib.Commands['ID'] = ('AUTH')
        mail = imaplib.IMAP4_SSL('imap.163.com')  # 以163邮箱为例
        mail.login(self.email, self.password)
        args = ("name", "lotteczy", "contact", "lotteczy@163.com", "version", "1.0.0", "vendor", "lotteczyEmailClient")
        typ, dat = mail._simple_command('ID', '("' + '" "'.join(args) + '")')
        return mail


    def _process_single_email(self, mail, num):
        """处理单封邮件"""
        status, data = mail.fetch(num, '(RFC822)')
        if status != 'OK':
            return

        raw_email = data[0][1].decode('utf-8')
        category = self.classifier.classify(raw_email)
        print(f"邮件 {num} 分类为: {category}")

        # 移动到对应文件夹
        self._move_email(mail, num, category)


    def _move_email(self, mail, num, category):
        """移动邮件到指定文件夹"""
        folder_map = {
            "会议邀请": "INBOX/Meeting",
            "问卷调查": "INBOX/Questionnaire",
            "工单流程审批": "INBOX/Approval",
            "个人": "INBOX/Personal",
            "促销": "INBOX/Promotions",
            "垃圾邮件": "INBOX/Spam",
            "重要": "INBOX/Important"
        }

        target_folder = folder_map.get(category, 'INBOX/Other')
        try:
            # 创建文件夹（如果不存在）
            mail.create(target_folder)
        except:
            pass

        # 复制邮件并标记为已读
        mail.copy(num, target_folder)
        mail.store(num, '+FLAGS', '\\Seen')


if __name__ == "__main__":
    # 使用前需在邮箱设置中启用IMAP并获取授权码
    agent = EmailClassificationAgent(
        email="xxxxx@163.com",
        password="xxxxxx"  # 不是登录密码，是IMAP授权码
    )
    agent.run()