from django.db import models

# Create your models here.

class userInf(models.Model):
	userNo = models.IntegerField(primary_key=True, null=False)
	userPasswd = models.TextField()
	def __str__(self):
		return self.userPasswd

class myServerMap(models.Model):
    #userNo = models.ForeignKey(userInf)
    hostName = models.CharField(max_length = 30)
    IPAddress = models.GenericIPAddressField()
    hostUrl = models.URLField()
    hostPort = models.IntegerField()
    createTime = models.DateTimeField(auto_now_add = True)
    
    class Meta:  #按时间下降排序
        ordering = ['-createTime']
    def __str__(self):
    	return self.hostName



