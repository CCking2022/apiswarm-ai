import imaplib
import email
from email.header import decode_header
import time
import datetime
import re
import os
import random
from dotenv import load_dotenv
from typing import Optional, Tuple, List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import zipfile
import tempfile

class EmailBot:
    """
    邮件机器人类
    实现定时收取邮件、识别主人命令、切换聊天状态、动态调整检查间隔、下载任务附件等功能
    """
    
    def __init__(self, cfg):
        """初始化邮件机器人"""
        # 不再需要 load_dotenv()，配置全部来自 cfg
        self.cfg = cfg

        # 👉 修改2：从 cfg 读取所有配置
        # 邮箱服务器配置
        self.imap_server = cfg["imap_server"]
        self.imap_port = cfg["imap_port"]
        
        self.smtp_server = cfg["smtp_server"]
        self.smtp_port = cfg["smtp_port"]
        
        # 邮箱账号和密码
        self.email_address = cfg["email_address"]
        self.email_password = cfg["email_password"]
        
        # 主人邮箱地址
        self.master_email = cfg["master_email"]
                
        # 检查间隔范围（秒）
        self.check_min_interval = cfg["check_min"]
        self.check_max_interval = cfg["check_max"]
        
        # 任务保存目录
        self.task_dir = "tasks"
        
        # 状态变量
        self.processed_email_ids = set()
        self.running = False

        # 系统状态
        self.system_status = ""
        
        # 初始化
        self._initialize()
    
    def _initialize(self):
        """初始化系统资源"""
        os.makedirs(self.task_dir, exist_ok=True)
    
    def get_current_interval(self) -> int:
        """获取当前检查间隔（秒）"""
        return random.randint(self.check_min_interval, self.check_max_interval)

    def clean_email_content(self, content: str) -> str:
        """清理邮件内容：去除所有空格、制表符和空行"""
        content = re.sub(r'[ \t]+', '', content)
        lines = content.splitlines()
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        return '\n'.join(non_empty_lines)
    
    def extract_command_and_args(self, content: str) -> Tuple[Optional[str], List[str]]:
        """
        从邮件内容提取命令和参数
        规则：按第一个 : 分割 → 前=命令，后=参数(按,分割)
        无命令 → args = []
        """
        if not content or not content.strip():
            return None, []

        if ":" in content:
            command_part, args_part = content.split(":", 1)
            command = command_part.strip()
            args_str = args_part.strip()
        else:
            command = content.strip()
            args_str = ""

        if not command:
            return None, []

        args = []
        if args_str:
            args = [item.strip() for item in args_str.split(",") if item.strip()]

        return command, args
    
    def decode_email_header(self, header: str) -> str:
        """解码邮件主题等头部信息"""
        if not header:
            return ""
        
        decoded_parts = decode_header(header)
        decoded_string = ""
        
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                try:
                    decoded_string += part.decode(encoding or 'utf-8')
                except:
                    decoded_string += part.decode('gbk', errors='replace')
            else:
                decoded_string += part
        
        return decoded_string
    
    def get_email_body_and_attachments(self, msg) -> Tuple[str, List[Tuple[str, bytes]]]:
        """从邮件对象中提取纯文本正文和所有附件"""
        body = ""
        attachments = []
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode('utf-8')
                    except:
                        try:
                            body = part.get_payload(decode=True).decode('gbk')
                        except:
                            body = part.get_payload(decode=True).decode('latin-1', errors='replace')
                
                elif "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        filename = self.decode_email_header(filename)
                        file_content = part.get_payload(decode=True)
                        attachments.append((filename, file_content))
        else:
            try:
                body = msg.get_payload(decode=True).decode('utf-8')
            except:
                try:
                    body = msg.get_payload(decode=True).decode('gbk')
                except:
                    body = part.get_payload(decode=True).decode('latin-1', errors='replace')
        
        return body, attachments
    
    def save_attachments(self, attachments: List[Tuple[str, bytes]]) -> List[str]:
        """保存附件到tasks目录"""
        saved_files = []
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for filename, content in attachments:
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_{timestamp}{ext}"
            file_path = os.path.join(self.task_dir, new_filename)
            
            with open(file_path, 'wb') as f:
                f.write(content)
            
            saved_files.append(file_path)
            print(f"✅ 附件已保存: {file_path}")
        
        return saved_files
    
    def process_master_email(self, msg, email_id: str) -> None:
        """处理来自主人邮箱的邮件"""
        subject = self.decode_email_header(msg["Subject"])
        sender = self.decode_email_header(msg["From"])
        body, attachments = self.get_email_body_and_attachments(msg)
        
        command, args = self.extract_command_and_args(subject)
        
        if command:
            self.execute_command(command, args, attachments, email_id)

    def execute_command(self, command: str, args: List[str], attachments: List[Tuple[str, bytes]], email_id: str) -> None:
        """执行预定命令"""
        command = command.lower()
        processed = False  # 标记是否成功处理
        
        if command == "newtask":
            print("⚠️ 执行命令: 新任务")
            if attachments:
                print(f"⚠️ 发现 {len(attachments)} 个附件，正在保存到task目录...")
                saved_files = self.save_attachments(attachments)
                print(f"✅ 任务清单已保存，共 {len(saved_files)} 个文件")
                processed = True
            else:
                print("⚠️ 警告：没有找到任务清单附件")
                processed = True
        
        elif command == "download":
            print(f"⚠️ 执行命令: 发送结果（打包output下的文件夹：{args}）")
            self.send_download_zipfile(args, email_id=email_id)
            processed = True
        
        elif command == "status":
            print("⚠️ 执行命令: 返回系统状态")
            self.send_status(email_id=email_id)
            processed = True

        # ======================
        # 只有成功处理命令，才标记为已读
        # ======================
        if processed:
            self.mark_email_as_seen(email_id)

    def mark_email_as_seen(self, email_id: str):
        """把指定邮件在邮箱里标记为已读"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.email_address, self.email_password)
            mail.select("INBOX")
            mail.store(email_id, '+FLAGS', '\\Seen')
            mail.logout()
            print(f"✅ 邮件 {email_id} 已标记为已读")
        except Exception as e:
            print(f"❌ 标记已读失败: {e}")

    def send_download_zipfile(self, args: List[str], email_id: str = None) -> None:
        subject = "下载指定文件夹"
        content = "附件为指定文件夹的压缩包，请查收。"

        if not args:
            self.send_mail_to_master("错误", "未指定文件夹名称", email_id=email_id)
            return

        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_root = os.path.join(base_dir, "output")

        # output 不存在 → 直接返回
        if not os.path.isdir(output_root):
            self.send_mail_to_master("提示", "output 文件夹不存在，无法下载", email_id=email_id)
            return

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
            zip_path = tmp.name

        packed_count = 0
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for folder_name in args:
                folder_path = os.path.join(output_root, folder_name)
                if not os.path.isdir(folder_path):
                    print(f"❌  子文件夹不存在：{folder_path}")
                    continue

                for root, _, files in os.walk(folder_path):
                    for f in files:
                        file_full = os.path.join(root, f)
                        arc_name = os.path.relpath(file_full, output_root)
                        zf.write(file_full, arc_name)
                        packed_count += 1

        if packed_count == 0:
            os.unlink(zip_path)
            self.send_mail_to_master("提示", "指定文件夹均为空或不存在", email_id=email_id)
            return

        with open(zip_path, "rb") as f:
            zip_data = f.read()
        os.unlink(zip_path)

        # ====================== 重点：生成 文件夹名+时间戳.zip ======================
        folder_name_str = "_".join(args)  # 多个文件夹用下划线连接
        timestamp = time.strftime("%Y%m%d_%H%M%S")  # 时间格式：20250521_153022
        zip_filename = f"{folder_name_str}_{timestamp}.zip"  # 最终附件名

        attachments = [(zip_filename, zip_data)]
  
        self.send_mail_to_master(subject, content, email_id=email_id, attachments=attachments)
        
    def send_status(self, email_id: str) -> None:
        subject = "蜂群状态"
        content = f"当前时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += f"{self.system_status}"
        
        self.send_mail_to_master(subject, content.strip(), email_id=email_id)
        
    def send_mail_to_master(self, subject: str, content: str, email_id: str = None, attachments: list = None):
        """
        发邮件 / 回复邮件
        - 传入 email_id → 自动回复该邮件
        - 不传入 → 普通发送
        """
        try:
            msg = MIMEMultipart()
            msg["From"] = self.email_address
            msg["To"] = self.master_email

            # ====================== 回复邮件逻辑 ======================
            if email_id is not None:
                with imaplib.IMAP4_SSL(self.imap_server, self.imap_port) as mail:
                    mail.login(self.email_address, self.email_password)
                    mail.select("INBOX")
                    status, data = mail.fetch(email_id, "(RFC822)")
                    if status == "OK" and isinstance(data[0], tuple):
                        orig_msg = email.message_from_bytes(data[0][1])
                        orig_subject = self.decode_email_header(orig_msg["Subject"])
                        if not orig_subject.startswith("Re:"):
                            subject = f"Re: {orig_subject}"

                        msg["In-Reply-To"] = orig_msg.get("Message-ID", "")
                        msg["References"] = orig_msg.get("Message-ID", "")

            msg["Subject"] = subject
            msg.attach(MIMEText(content, "plain", "utf-8"))

            if attachments:
                for filename, file_data in attachments:
                    # 1. 改成标准 zip 类型，不要用 octet-stream
                    part = MIMEBase("application", "zip")
                    part.set_payload(file_data)
                    encoders.encode_base64(part)
                    # ====================== 核心修复 ======================
                    # 这一行就是你要加的【正确写法】，替换原来那行
                    part.add_header(
                        "Content-Disposition",
                        "attachment",
                        filename=filename  # 不要写在字符串里！
                    )
                    msg.attach(part)
        
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.email_address, self.email_password)
                #只给主人（self.master_email）发邮件！！！其他一律不发！！！否则会把压缩包发给别人！！！
                server.sendmail(self.email_address, self.master_email, msg.as_string())

            print(f"✅ 邮件已发送: {subject}")

        except Exception as e:
            print(f"❌ 发邮件失败: {e}")
            
    def check_emails(self) -> None:
        """检查并收取新邮件"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.email_address, self.email_password)
            mail.select("INBOX")
            status, messages = mail.search(None, 'UNSEEN')
            
            if status != 'OK':
                mail.logout()
                return
            
            email_ids = messages[0].split()
            if not email_ids:
                mail.logout()
                return
            
            for email_id in email_ids:
                if email_id in self.processed_email_ids:
                    continue
                
                status, msg_data = mail.fetch(email_id, "(RFC822)")
                if status != "OK":
                    continue
                
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        from_header = self.decode_email_header(msg["From"])
                        sender_email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', from_header)
                        
                        if sender_email:
                            sender_email = sender_email.group()

                            #只处理主人邮件（self.master_email）！！！其他一律不管！！！否则会接收他人指令！！！
                            if sender_email.lower() == self.master_email.lower():
                                self.process_master_email(msg, email_id)
                
                self.processed_email_ids.add(email_id)
            
            mail.logout()
        
        except Exception as e:
            print(f"❌ [{datetime.datetime.now()}] 收取邮件错误: {str(e)}")
    
