import os
import smtplib
from email.header import Header, make_header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

from typing import List

"""
Reply codes in numerical order[td]

Code	Meaning
200	(nonstandard success response, see rfc876)
211	System status, or system help reply
214	Help message
220	<domain> Service ready
221	<domain> Service closing transmission channel
250	Requested mail action okay, completed
251	User not local; will forward to <forward-path>
354	Start mail input; end with <CRLF>.<CRLF>
421	<domain> Service not available, closing transmission channel
450	Requested mail action not taken: mailbox unavailable
451	Requested action aborted: local error in processing
452	Requested action not taken: insufficient system storage
500	Syntax error, command unrecognised
501	Syntax error in parameters or arguments
502	Command not implemented
503	Bad sequence of commands
504	Command parameter not implemented
521	<domain> does not accept mail (see rfc1846)
530	Access denied (???a Sendmailism)
550	Requested action not taken: mailbox unavailable
551	User not local; please try <forward-path>
552	Requested mail action aborted: exceeded storage allocation
553	Requested action not taken: mailbox name not allowed
554	Transaction failed
Reply codes grouped by command[td]

Command	Code	Description
connect
220	<domain> Service ready
421	<domain> Service not available, closing transmission channel
HELO
250	Requested mail action okay, completed
500	Syntax error, command unrecognised
501	Syntax error in parameters or arguments
504	Command parameter not implemented
521	<domain> does not accept mail [rfc1846]
421	<domain> Service not available, closing transmission channel
EHLO
250	Requested mail action okay, completed
550	Not implemented
500	Syntax error, command unrecognised
501	Syntax error in parameters or arguments
504	Command parameter not implemented
421	<domain> Service not available, closing transmission channel
MAIL
250	Requested mail action okay, completed
552	Requested mail action aborted: exceeded storage allocation
451	Requested action aborted: local error in processing
452	Requested action not taken: insufficient system storage
500	Syntax error, command unrecognised
501	Syntax error in parameters or arguments
421	<domain> Service not available, closing transmission channel
RCPT
250	Requested mail action okay, completed
251	User not local; will forward to <forward-path>
550	Requested action not taken: mailbox unavailable
551	User not local; please try <forward-path>
552	Requested mail action aborted: exceeded storage allocation
553	Requested action not taken: mailbox name not allowed
450	Requested mail action not taken: mailbox unavailable
451	Requested action aborted: local error in processing
452	Requested action not taken: insufficient system storage
500	Syntax error, command unrecognised
501	Syntax error in parameters or arguments
503	Bad sequence of commands
521	<domain> does not accept mail [rfc1846]
421	<domain> Service not available, closing transmission channel
DATA
354	Start mail input; end with <CRLF>.<CRLF>
451	Requested action aborted: local error in processing
554	Transaction failed
500	Syntax error, command unrecognised
501	Syntax error in parameters or arguments
503	Bad sequence of commands
421	<domain> Service not available, closing transmission channel
received data
250	Requested mail action okay, completed
552	Requested mail action aborted: exceeded storage allocation
554	Transaction failed
451	Requested action aborted: local error in processing
452	Requested action not taken: insufficient system storage
RSET
200	(nonstandard success response, see rfc876)
250	Requested mail action okay, completed
500	Syntax error, command unrecognised
501	Syntax error in parameters or arguments
504	Command parameter not implemented
421	<domain> Service not available, closing transmission channel
SEND
250	Requested mail action okay, completed
552	Requested mail action aborted: exceeded storage allocation
451	Requested action aborted: local error in processing
452	Requested action not taken: insufficient system storage
500	Syntax error, command unrecognised
501	Syntax error in parameters or arguments
502	Command not implemented
421	<domain> Service not available, closing transmission channel
SOML
250	Requested mail action okay, completed
552	Requested mail action aborted: exceeded storage allocation
451	Requested action aborted: local error in processing
452	Requested action not taken: insufficient system storage
500	Syntax error, command unrecognised
501	Syntax error in parameters or arguments
502	Command not implemented
421	<domain> Service not available, closing transmission channel
SAML
250	Requested mail action okay, completed
552	Requested mail action aborted: exceeded storage allocation
451	Requested action aborted: local error in processing
452	Requested action not taken: insufficient system storage
500	Syntax error, command unrecognised
501	Syntax error in parameters or arguments
502	Command not implemented
421	<domain> Service not available, closing transmission channel
VRFY
250	Requested mail action okay, completed
251	User not local; will forward to <forward-path>
550	Requested action not taken: mailbox unavailable
551	User not local; please try <forward-path>
553	Requested action not taken: mailbox name not allowed
500	Syntax error, command unrecognised
501	Syntax error in parameters or arguments
502	Command not implemented
504	Command parameter not implemented
421	<domain> Service not available, closing transmission channel
EXPN
250	Requested mail action okay, completed
550	Requested action not taken: mailbox unavailable
500	Syntax error, command unrecognised
501	Syntax error in parameters or arguments
502	Command not implemented
504	Command parameter not implemented
421	<domain> Service not available, closing transmission channel
HELP
211	System status, or system help reply
214	Help message
500	Syntax error, command unrecognised
501	Syntax error in parameters or arguments
502	Command not implemented
504	Command parameter not implemented
421	<domain> Service not available, closing transmission channel
NOOP
200	(nonstandard success response, see rfc876)
250	Requested mail action okay, completed
500	Syntax error, command unrecognised
421	<domain> Service not available, closing transmission channel
QUIT
221	<domain> Service closing transmission channel
500	Syntax error, command unrecognised
TURN
250	Requested mail action okay, completed
502	Command not implemented
500	Syntax error, command unrecognised
503	Bad sequence of commands

"""


class Mailer:
    """
    usage:
     host = "smtp.exmail.qq.com"
    sender = "xxxx@yyy.com"
    port = 25
    password = "123456"
    receiver = ["www@qq.com"]
    cc = ["ccc@vvv.com"]

    mailer = Mailer(sender, password)
    mailer.send_mail(
    "测试邮件标题",
     "邮件内容",
      receiver,
       cc_aadrs=cc,
       attachment_files=[
            "/aaa/bb/good.pdf"
            "/aaa/bb/好样的.png"
            "/aaa/bb/不一样.mp3"
            "/aaa/bb/attach_zip.zip"
    ])
    """

    def __init__(self, sender: str, password: str, username: str = None, host: str = "smtp.exmail.qq.com",
                 port: int = 25):
        self.host = host
        self.port = port

        assert self.is_email(sender), "sender不像是邮箱"
        self.sender = sender
        self.password = password
        self.username = username if username is not None else self.sender.split('@')[0]

        self.server = smtplib.SMTP(self.host, self.port)

    @staticmethod
    def is_email(email_address: str):
        return "@" in email_address

    def login(self):
        try:
            res = self.server.login(self.sender, self.password)
        except Exception as e:
            print("登录逻辑抛出了异常")
            raise e
        return res

    def connect(self):
        try:
            res = self.server.connect(self.host, self.port)
        except Exception as e:
            print("链接邮箱服务抛出异常")
            raise e
        return res

    @staticmethod
    def attach(file):
        """
        发送邮件需要携带的附件，文件绝对路径
        :param file:
        :return:
        """
        if not os.path.exists(file):
            raise FileNotFoundError('文件{}不存在～'.format(file))

        if not os.path.isfile(file):
            raise FileNotFoundError('目标{}不是一个文件'.format(file))

        file_name = os.path.basename(file)
        with open(file, 'rb') as f:
            part = MIMEApplication(f.read())
            # 中文等特殊字符集要特殊处理
            part.add_header('Content-Disposition', 'attachment',
                            fileName="%s" % make_header([(file_name, 'UTF-8')]).encode('UTF-8'))
            return part
            # msg.attach(part)

    def send_mail(self, subject: str, content: str, to_addrs: List[str], cc_aadrs: List[str] = None,
                  subtype='mixed',
                  text_subtype='plain',
                  attachment_files: List[str] = None):

        """

        :param subject:
        :param content:
        :param to_addrs:
        :param cc_aadrs:
        :param subtype:
        :param text_subtype:
        :param attachment_files:
        :param kwargs:
        :return:
        """

        """
        邮件头信息
        """
        msgobj = MIMEMultipart(_subtype=subtype, text_subtype=text_subtype)
        msgobj['Subject'] = Header(subject, "utf-8")
        msgobj['From'] = self.sender
        msgobj['To'] = ",".join(to_addrs)
        msgobj['cc'] = ",".join(cc_aadrs) if cc_aadrs else ""

        """
        邮件内容
        """
        text = MIMEText(content, _charset='utf-8')
        # plain text
        msgobj.attach(text)

        """
        附加附件
        """
        # 如果有附件
        if attachment_files:
            for file in attachment_files:
                msgobj.attach(self.attach(file))

        """
        to list 需要包含 to+cc的总量
        """
        to_addrs = list(set(to_addrs + cc_aadrs)) if cc_aadrs else to_addrs
        # self.connect()
        self.login()
        self.server.sendmail(self.sender, to_addrs=to_addrs, msg=msgobj.as_string())


if __name__ == '__main__':
    pass
