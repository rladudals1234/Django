from django.db import models
from member.models import Member

# Create your models here.
class Board(models.Model):
    bno = models.AutoField(primary_key=True)
    # id -> ORM방식 객체저장이 가능해짐.
    member = models.ForeignKey(Member, on_delete=models.DO_NOTHING, null=True)  # 지워지면 null로 채움
    # id = models.CharField(max_length=50)
    btitle = models.CharField(max_length=1000)
    bcontent = models.TextField()
    bhit = models.IntegerField(default=0)
    bdate = models.DateTimeField(auto_now=True)
    
    # 답변달기 사용에 필요한 컬럼
    # bgroup, bstep, bindent
    bgroup = models.IntegerField(default=0)
    bstep = models.IntegerField(default=0)
    bindent = models.IntegerField(default=0)
    # 파일첨부
    bfile = models.CharField(max_length=100, default='')
    
    def __str__(self):
        return f"{self.bno},{self.btitle},{self.bcontent},{self.member.id},{self.bhit},{self.bfile},{self.bdate}"