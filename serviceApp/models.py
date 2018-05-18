from django.db import models
#from django.contrib.auth.models import User
# Create your models here.


class userInf(models.Model):
    user_id = models.AutoField(primary_key=True, null=False)
    user_name = models.CharField(max_length = 30)
    user_nickname = models.CharField(max_length = 30)
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
    admin_id = models.ForeignKey(userInf,related_name='phones_admin',on_delete=models.DO_NOTHING) 
    phone_name = models.CharField(max_length = 30)
    image_path = models.CharField(max_length = 255)
    phone_details = models.TextField() 
    def __str__(self):
        return self.phone_name

class workOrders(models.Model):
    order_id = models.AutoField(primary_key=True, null=False)
    user_id = models.ForeignKey(userInf,related_name='work_user', on_delete=models.DO_NOTHING)
    server_id = models.ForeignKey(userInf,related_name='work_server',on_delete=models.DO_NOTHING)
    phone_id = models.ForeignKey(phonesInf, on_delete=models.DO_NOTHING)
    order_title = models.CharField(max_length = 30)
    order_details = models.CharField(max_length = 255)
    order_status = models.BooleanField(default=False)
    grade_status = models.BooleanField(default=False)
    order_grade = models.FloatField(default='0.0')
    order_time = models.DateTimeField(auto_now_add = True)
    class Meta:  #按时间下降排序
        ordering = ['-order_time']
    def __str__(self):
    	return self.order_title

class commitDetails(models.Model):
    commit_id = models.ForeignKey(workOrders,related_name='commit_order', on_delete=models.DO_NOTHING)
    commit_from = models.ForeignKey(userInf, related_name='commit_from_user', on_delete=models.DO_NOTHING)
    commit_to = models.ForeignKey(userInf,related_name='commit_to_user', on_delete=models.DO_NOTHING)
    commit_details = models.CharField(max_length = 255)
    commit_status = models.BooleanField(default=False)
    commit_time = models.DateTimeField(auto_now_add = True)
    
    class Meta:  #按时间下降排序
        ordering = ['commit_time']
    def __str__(self):
    	return self.commit_details


class gradesInf(models.Model):
    grade_id = models.ForeignKey(workOrders,related_name='grade_order', on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(userInf,related_name='grade_user', on_delete=models.DO_NOTHING)
    server_id = models.ForeignKey(userInf, on_delete=models.DO_NOTHING)
    user_grade = models.FloatField()
    user_message =  models.TextField()
    grade_time = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.user_message

class aboutInf(models.Model):
    admin_id = models.ForeignKey(userInf,related_name='about_admin',  on_delete=models.DO_NOTHING)
    about_title = models.CharField(max_length = 30)
    image_path = models.CharField(max_length = 255)
    about_content = models.TextField()
    def __str__(self):
        return self.about_title


    
class carParts(models.Model):
    partId = models.AutoField(primary_key=True, null=False)
    personId = models.ForeignKey(userInf,related_name='admin_user',  on_delete=models.DO_NOTHING)
    partName = models.CharField(max_length = 40)
    partNumber = models.IntegerField()
    partType = models.CharField(max_length = 10)
    partSize = models.CharField(max_length = 40)
    partPrice = models.FloatField()
    partDate = models.DateTimeField(auto_now_add = True)  
    def __str__(self):
        return self.partName

class repairInfo(models.Model):
    repairId = models.AutoField(primary_key=True, null=False)
    repairName = models.CharField(max_length = 40)
    totalPrice = models.FloatField()
    repairDetails = models.CharField(max_length = 255)
    partDetails = models.CharField(max_length = 255)
    repairDate = models.DateTimeField(auto_now_add = True)
    personId = models.ForeignKey(userInf,related_name='repair_user',  on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.repairName
'''
class repairDetails(models.Model):
    detailsId = models.ForeignKey(repairInfo,related_name='repair_id',  on_delete=models.DO_NOTHING)
    detailPartId = models.ForeignKey(carParts,related_name='part_id',  on_delete=models.DO_NOTHING)
    partName = models.CharField(max_length = 40)
    partNum = models.IntegerField()
    sigleTotalPrice = models.FloatField()
'''