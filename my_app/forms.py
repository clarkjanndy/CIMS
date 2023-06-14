from django import forms
from django.forms import PasswordInput
from .models import RegCode,Admin, Users,Comments,Inventory,Posts,Order,PostImage,ProfilePics,Messages,CheckUpRecords,Search

from . models import Category
from datetime import date
# class ImageForm(forms.ModelForm):
#     """Form for the image model"""
#     class Meta:
#         model = Image
#         fields = ('title', 'image')

class RegCodeForm(forms.ModelForm):
    class Meta:
        model = RegCode
        fields = ['faculty','staff','nstp_coordinator','admin','rotc_coordinator']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
        widgets = {'comment':forms.Textarea(attrs={'class':'post_comment'})}

class UsersForm(forms.ModelForm):
    student_id = forms.CharField(max_length=255)
    
    class Meta:
        model = Users
        fields = ('student_id','firstname','middlename','lastname','birthday','age','address','gender','year_level','department','email','password','medcert','medical_status','medical_condition')
        widgets = {'password':forms.PasswordInput(),'birthday':forms.DateInput(attrs={'type':'date'}),'gender':forms.Select(attrs={'class':'reg_input'}),'medical_status':forms.Select(attrs={'class':'reg_input'}),'year_level':forms.Select(attrs={'class':'reg_input'}),'department':forms.Select(attrs={'class':'reg_input'})}

class UsersV2Form(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('firstname','middlename','lastname','birthday','age','address','gender','year_level','department','email','password')
        widgets = {'password':forms.PasswordInput(),'birthday':forms.DateInput(attrs={'type':'date'}),'gender':forms.Select(attrs={'class':'reg_input'}),'medical_status':forms.Select(attrs={'class':'reg_input'}),'year_level':forms.Select(attrs={'class':'reg_input'}),'department':forms.Select(attrs={'class':'reg_input'})}
    
  
class CheckupForm(forms.ModelForm):
    class Meta:
        model = CheckUpRecords
        fields = ['blood_pressure','pulse_rate','respiratory_rate','temperature','other_info','remark_after_checkup']
        widgets = {'other_info':forms.Textarea(attrs={'class':'remarks_content'}),'remark_after_checkup':forms.Textarea(attrs={'class':'remarks_content'})}

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('firstname', 'middlename','lastname','birthday','age','address','gender','department','email','password','medcert','medical_status','medical_condition')
        # widgets = {'password':forms.PasswordInput(),'birthday':forms.DateInput(attrs={'type':'date'})}

class EditUsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('firstname', 'middlename','lastname','birthday','age','address','gender','department','email','medical_status','medical_condition')
        widgets = {'password':forms.PasswordInput(),'birthday':forms.DateInput(attrs={'type':'date'})}

class AdminRegForm(forms.ModelForm):
    admin_code=forms.CharField(min_length=8,widget=PasswordInput)
    class Meta:
        model = Admin
        widgets = {'password':forms.PasswordInput()}
        fields = ('email','password','profile_pic')

class LoginForm(forms.Form):
    email=forms.CharField(label='Enter Email Address:',max_length=100)
    password=forms.CharField(label='Enter Password',widget=PasswordInput)

class InventoryForm(forms.ModelForm):
    
    category = forms.ChoiceField(choices=[])
    class Meta:
        model=Inventory
        fields=('item_name','category','purchase_date','unit','quantity','expiration','item_image')
        widgets = {'purchase_date':forms.DateInput(attrs={'type':'date'}),
                  'expiration':forms.DateInput(attrs={'type':'date'}),
                  }
    
    def clean_expiration(self):
        expiration = self.cleaned_data['expiration']
        # Check if the date is in the past
        if expiration < date.today():
            raise forms.ValidationError("Expiration date cannot be in the past.")
        return expiration
    
    def __init__(self, *args, **kwargs):
        super(InventoryForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = [(x.name, x.name) for x in Category.objects.all().order_by('name')]

class AddStockForm(forms.ModelForm):
    class Meta:
        model=Inventory
        fields=('quantity',)

class MessageForm(forms.ModelForm):
    class Meta:
        model=Messages
        fields=['message','message_to']
        widgets = {'message':forms.Textarea(attrs={'class':'post_content'})}
        
class PostForm(forms.ModelForm):
    class Meta:
        model=Posts
        fields=('content',)
        widgets = {'content':forms.Textarea(attrs={'class':'post_content'})}

class PostImageForm(forms.ModelForm):
    class Meta:
        model=PostImage
        fields=['post_pic']
        
        
# class ProjectImageForm(forms.ModelForm):
#     class Meta:
#         model = PostImage
#         fields = ['image']
#         widgets = {
#             'image': ClearableFileInput(attrs={'multiple': True}),
#         }

class OrderForm(forms.ModelForm):
    class Meta:
        model= Order
        fields= ('serial','quantity')

class ProfilePicForm(forms.ModelForm):
    class Meta:
        model= ProfilePics
        fields=['profile_pic']
        
class SearchForm(forms.ModelForm):
    class Meta:
        model = Search
        fields=['search']