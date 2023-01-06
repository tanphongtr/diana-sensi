from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from django.template.loader import render_to_string
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(name='Task Example')
def task_example(params):
    pass

@shared_task(name='Sendmail')
def task_sendmail(email, code, location):
    logger.info(f'task_sendmail({email}, {code}, {location})')
    try:
        send_mail(
            'Diana Express - Redeem Code',
            f'''
Thân gửi Quý khách hàng,

Cảm ơn Quý khách hàng đã tham gia trải nghiệm chuyến tàu Diana Express tại {location} và nhận được 01 mã số may mắn với cơ hội trúng thưởng 01 chuyến du lịch hấp dẫn do nhãn hàng Diana Unicharm tổ chức.

Mã số của Quý khách hàng là: {code}

Quý khách hàng vui lòng không chia sẻ mã số này để đảm bảo quyền lợi của mình.

Xin trân trọng cảm ơn!

(*) Lưu ý: Đây là thư gửi tự động, vui lòng không phản hồi thư.
            ''',
            'dianaexpress@dianacoolfresh.com',
            [email],
            fail_silently=False,
        )
    except:
        raise task_sendmail.retry(max_retries=3)

