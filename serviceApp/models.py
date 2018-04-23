from django.db import models
#from django.contrib.auth.models import User
# Create your models here.


class userInf(models.Model):
    user_id = models.AutoField(primary_key=True, null=False)
    user_name = models.CharField(max_length = 30)
    user_grant = models.BooleanField(default=False) 
    user_sex = models.CharField(max_length = 5)
    user_mask = models.CharField(max_length=100)
    image_path = models.CharField(max_length = 255)
    user_grades = models.FloatField(default=0.0)
    user_passwd = models.CharField(max_length=100)
    def __str__(self):
        return self.user_name

class phonesInf(models.Model):
    phone_id = models.AutoField(primary_key=True, null=False)
    admin_id = models.ForeignKey(userInf,on_delete=models.DO_NOTHING) 
    phone_name = models.CharField(max_length = 30)
    image_path = models.CharField(max_length = 255)
    phone_details = models.TextField() 
    def __str__(self):
        return self.phone_name

class workOrders(models.Model):
    order_id = models.AutoField(primary_key=True, null=False)
    user_id = models.ForeignKey(userInf, on_delete=models.DO_NOTHING)
    phone_id = models.ForeignKey(phonesInf, on_delete=models.DO_NOTHING)
    order_title = models.CharField(max_length = 30)
    order_details = models.CharField(max_length = 255)
    order_status = models.BooleanField(default=False)
    order_grade = models.FloatField()
    order_time = models.DateTimeField(auto_now_add = True)
    
    class Meta:  #按时间下降排序
        ordering = ['-order_time']
    def __str__(self):
    	return self.order_title

class gradesInf(models.Model):
    user_id = models.ForeignKey(userInf, on_delete=models.DO_NOTHING)
    user_grade = models.FloatField()
    user_message =  models.TextField()
    ava_grade = models.FloatField()
    def __str__(self):
        return self.user_message

class aboutInf(models.Model):
    admin_id = models.ForeignKey(userInf, on_delete=models.DO_NOTHING)
    about_title = models.CharField(max_length = 30)
    image_path = models.CharField(max_length = 255)
    about_content = models.TextField()
    def __str__(self):
        return self.user_title

    



