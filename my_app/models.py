
from django.db import models
from django.utils import timezone
class Users(models.Model):
  gen=[('',''),('Male','Male'),('Female','Female')]
  dep=[('',''),('BSIT','BSIT'),('BSHRM','BSHRM'),('BSED','BSED'),('CRIM','CRIM')]
  medstat=[('',''),('Physically Fit','Physically Fit'),('With Medical Condition','With Medical Condition')]
  year=[('',''),('Freshmen','Freshmen'),('Sophomore','Sophomore'),('Junior','Junior'),('Senior','Senior')]
  student_id = models.CharField(max_length=255, default=None, null=True, blank=True)
  firstname = models.CharField(max_length=255)
  middlename = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  birthday = models.DateField(max_length=255)
  age = models.CharField(max_length=255)
  address = models.CharField(max_length=255)
  gender = models.CharField(max_length=25,choices=gen,default='')
  year_level = models.CharField(max_length=20,choices=year,default='')
  department = models.CharField(max_length=25,choices=dep,default='', blank=True, null= True)
  email = models.EmailField(max_length=255)
  password = models.CharField(max_length=255)
  status = models.CharField(max_length=225)
  medical_status = models.CharField(max_length=200,choices=medstat, default='', blank=True, null= True)
  medical_condition = models.CharField(max_length=100, default="N/A", blank=True, null= True)
  medcert = models.ImageField(upload_to='medcert', blank=True, null= True)  
  user_type =  models.CharField(max_length=20)
  list_filter =  models.CharField(max_length=20)
  is_online = models.CharField(max_length=10,default='false')
  is_active = models.BooleanField(default=True)
  date_added = models.DateTimeField(default=timezone.now) 

  def __str__(self):
    return "%s %s"%(self.firstname,self.lastname)
  
class Admin(models.Model):
  email = models.EmailField(max_length=225)
  password = models.CharField(max_length=255)
  profile_pic = models.ImageField(upload_to='profile_pic')
  
class Category(models.Model):
  name = models.CharField(max_length=50)

class Inventory(models.Model):
  unit=[('',''),('Pieces','Pieces'),('Bottle','Bottle'),('Litter','Litter'),('Stab','Stab')]
  serial = models.IntegerField()
  item_name = models.CharField(max_length=255)
  purchase_date = models.DateField(max_length=255)
  # selling_price = models.FloatField(max_length=255)
  quantity = models.IntegerField()
  expiration = models.DateField(max_length=255)
  item_image = models.ImageField(upload_to='inventory')
  unit = models.CharField(max_length=255,choices=unit,default='')
  category = models.CharField(max_length=255, default='')
  remaining = models.IntegerField(default=0)
  status = models.CharField(max_length=225)

class Posts(models.Model):
  content = models.TextField(max_length=50000)
  title = models.CharField(max_length=255)
  date_posted = models.DateField(auto_now_add=True)
  posted_by = models.CharField(max_length=255,default="")

class Faculty(models.Model):
  gen=[('',''),('Male','Male'),('Female','Female')]
  dep=[('',''),('BSIT','BSIT'),('BSHRM','BSHRM'),('BSED','BSED'),('CRIM','CRIM')]
  medstat=[('',''),('Physically Fit','Physically Fit'),('With Medical Condition','With Medical Condition')]
  firstname = models.CharField(max_length=255)
  middlename = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  birthday = models.DateField(max_length=255)
  age = models.CharField(max_length=255)
  address = models.CharField(max_length=255)
  gender = models.CharField(max_length=25,choices=gen,default='')
  department = models.CharField(max_length=25,choices=dep,default='')
  email = models.EmailField(max_length=255)
  password = models.CharField(max_length=255)
  status = models.CharField(max_length=225)
  user_type =  models.CharField(max_length=20)

class Order(models.Model):
  item_name = models.CharField(max_length=255) 
  item_category = models.CharField(max_length=255) 
  serial = models.IntegerField()
  quantity = models.IntegerField()
  selling_price = models.FloatField(max_length=255,default=0)
  unit = models.CharField(max_length=255)
  student_name = models.CharField(max_length=100)
  total = models.FloatField(default=0)
  order_status = models.CharField(max_length=255) 
  order_date = models.DateTimeField(default=timezone.now)

class PostImage(models.Model):
  post_id = models.IntegerField()
  post_pic = models.ImageField(upload_to='post')

class ProfilePics(models.Model):
  prof_pic_of = models.CharField(max_length=50,default='')
  profile_pic = models.ImageField(upload_to='profile_pic')

class Comments(models.Model):
  post_id = models.IntegerField(default=0)
  commented_by = models.CharField(max_length=225,default="")
  comment = models.TextField(max_length=50000)

class Messages(models.Model):
  message = models.TextField(max_length=50000)
  message_from = models.CharField(max_length=30)
  message_to = models.CharField(max_length=30)
  date = models.DateField(auto_now_add=True)

class Reply(models.Model):
  msg_id = models.IntegerField(default=0)
  msgrep = models.TextField(max_length=50000)
  msgrep_from = models.CharField(max_length=30)
  msgrep_to = models.CharField(max_length=30)
  date = models.DateField(auto_now_add=True)

class CheckUpRecords(models.Model):
  rec_id = models.CharField(default='' , max_length=255)
  rec_email = models.EmailField(max_length=50)
  checkup_date = models.DateField(auto_now_add=True)
  blood_pressure = models.CharField(max_length=30)
  pulse_rate = models.CharField(max_length=100)
  respiratory_rate = models.CharField(max_length=100)
  temperature = models.CharField(max_length=30)
  other_info = models.TextField(max_length=50000)
  remark_after_checkup = models.TextField(max_length=50000)

class RegCode(models.Model):
  faculty=models.CharField(max_length=50,default="None")
  staff=models.CharField(max_length=50,default="None")
  nstp_coordinator=models.CharField(max_length=50,default="None")
  admin=models.CharField(max_length=50)
  rotc_coordinator=models.CharField(max_length=50,default="None")
  
class Search(models.Model):
  search = models.CharField(default='0', max_length=225)
 
class Editors(models.Model):
    editor_name = models.CharField(max_length=200)
    num_users = models.IntegerField()

    def __str__(self):
        return "{}-{}".format(self.editor_name, self.num_users) 

class Notifications(models.Model):
  medicine = models.ForeignKey(Inventory, on_delete=models.CASCADE)
  datetime = models.DateTimeField(auto_now_add=True)
  is_read = models.BooleanField(default=False)

  class DispenseGraph(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255)
    item_number = models.CharField(max_length=255)
    data_date = models.DateTimeField(default=timezone.now)
  