from django.db import models

# Create your models here.

class userInf(models.Model):
    user_id = models.IntegerField(primary_key=True, null=False)
    user_name = models.CharField(max_length = 30)
    user_grant = models.BooleanField(default=False) 
    user_sex = models.CharField(max_length = 5)
    user_image = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/no-img.jpg')
    user_grades = models.FloatField(default=0.0)
    user_passwd = models.CharField(max_length=100)
    def __str__(self):
        return self.user_name

class phonesInf(models.Model):
    phone_id = models.IntegerField(primary_key=True, null=False)
    admin_id = models.ForeignKey(userInf) 
    phone_type = models.CharField(max_length = 30)
    phone_image = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/no-img.jpg')
    phone_details = models.TextField() 
    def __str__(self):
        return self.phone_type

class workOrders(models.Model):
    order_id = models.IntegerField(primary_key=True, null=False)
    user_id = models.ForeignKey(userInf)
    phone_id = models.ForeignKey(phonesInf)
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
    user_id = models.ForeignKey(userInf)
    user_grade = models.FloatField()
    user_message =  models.TextField()
    ava_grade = models.FloatField()
    def __str__(self):
        return self.user_message

class aboutInf(models.Model):
    admin_id = models.ForeignKey(userInf)
    about_title = models.CharField(max_length = 30)
    about_image = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/no-img.jpg')
    about_content = models.TextField()
    def __str__(self):
        return self.user_title

    



