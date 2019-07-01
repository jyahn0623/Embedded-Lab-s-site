from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

def save_pic_user(instance, name):
    return "{0}/{1}".format("Profile", name)


class RankPicture(models.Model):
    r_rankcode = models.CharField(max_length=5)
    r_images = models.ImageField(null=True)

class Profile(models.Model):
    p_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    p_name = models.CharField(max_length=5, verbose_name="이름")
    p_grade = models.CharField(max_length=1, verbose_name="학년")
    p_rank = models.CharField(default="재학생", max_length=5, verbose_name="신분", choices=(('재학생', '재학생'), ('졸업생', '졸업생'), ('실장', '실장')))
    p_rank_pic = models.OneToOneField("Main.RankPicture", verbose_name="계급 사진", on_delete=models.DO_NOTHING, null=True)
    p_birth_date = models.DateField(verbose_name="생년월일", null=True)
    p_picture = models.ImageField(verbose_name="사진", null=True, upload_to=save_pic_user)

    


class Board(models.Model):
    b_title = models.CharField(max_length=50, verbose_name="제목")
    b_category = models.CharField(max_length=5, choices=(('정보', '정보'), ('기타', '기타') ), verbose_name="분류", default="정보")
    b_content = models.CharField(max_length=300, verbose_name="내용")
    b_date=models.DateTimeField(auto_now_add=True, verbose_name="작성일", null=True)
    b_user=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자", null=True)
    b_isNotice = models.BooleanField(default=False, verbose_name="공지 여부")

class Schedule(models.Model):
    s_user = models.CharField(max_length=50)
    s_date = models.DateTimeField(null=True)
    s_finished_date = models.DateTimeField(null=True)
    s_content = models.CharField(max_length=50)



class BoardFiles(models.Model):
    b_board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)
    b_file = models.FileField(verbose_name="파일", upload_to="Board")
    
class GuestBook(models.Model):
    g_name = models.CharField(max_length=5)
    g_email = models.CharField(max_length=30)
    g_title = models.CharField(max_length=20)
    g_content = models.CharField(max_length=50)
    g_date = models.DateTimeField(auto_now_add=True)
    g_ip = models.CharField(max_length=20)

  