from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from crm_cubedots.model.departments import Departments

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )

        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def users_profile_picture_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/project /<filename>
    
    data = instance.first_name +'_'+ str(instance.id)
    return 'users/{0}/{1}'.format(data, filename)

class Account(AbstractBaseUser,PermissionsMixin):
    FULL = 4
    MAJOR = 3
    MINOR = 2
    CONTROLLED = 1
    access_groups = [(FULL, 4), (MAJOR, 3), (MINOR, 2), (CONTROLLED, 1)]
    email             = models.EmailField(verbose_name="Email", max_length=60, unique=True)
    username          = models.CharField(max_length=30, unique=False,blank=True,null=True)
    date_joined       = models.DateTimeField(blank=True,null=True, verbose_name="Date of Joined")
    last_login        = models.DateTimeField(verbose_name="Last Login", auto_now=True)
    is_admin          = models.BooleanField(default=False)
    is_active         = models.BooleanField(default=True)
    is_staff          = models.BooleanField(default=False)
    is_superuser      = models.BooleanField(default=False)
    first_name        = models.CharField(_('first name'), max_length=50, blank=True)
    last_name         = models.CharField(_('last name'), max_length=50, blank=True)
    role              = models.CharField(verbose_name="Role", max_length=50, null=True)
    date_of_birth     = models.DateTimeField(blank=True,null=True, verbose_name="Date of Birth")
    avatar            = models.ImageField(upload_to=users_profile_picture_directory_path,blank=False,null=True,verbose_name="Image")
    designation       = models.CharField(verbose_name="Designation", max_length=50, null=True)
    contact_no        = models.CharField(blank=True, verbose_name="Phone Number", max_length=100)
    department        = models.ForeignKey(Departments,on_delete=models.CASCADE,null=True,related_name='DepartmentsId',verbose_name="Department Name", )
    team_name         = models.CharField(verbose_name="Team Name", max_length=60, null=True)
    team_leader       = models.CharField(verbose_name="Team Leader", max_length=60, null=True)
    manager_name      = models.CharField(verbose_name="Manager Name", max_length=60, null=True)
    status            = models.CharField(verbose_name="Status", max_length=60, null=True)
    date_exited       = models.DateTimeField(verbose_name="Date of Exited", blank=True,null=True)
    local_address     = models.CharField(verbose_name="Local Address", max_length=200, null=True)
    permanent_address = models.CharField(verbose_name="Permanent Address", max_length=200, null=True)
    gender            = models.CharField(verbose_name="Gender", max_length=20, null=True)
    blood_group       = models.CharField(verbose_name="Blood Group", max_length=10, null=True)
    skills            = models.CharField(verbose_name="Skills", max_length=200, null=True)
    qualifications    = models.CharField(verbose_name="Qualifications", max_length=100, null=True)
    access_group      = models.IntegerField(_('permission group'), choices=access_groups, default=CONTROLLED)
    postal_code       = models.IntegerField(verbose_name="Pin Code", blank=True, null=True)
    approval_status   = models.CharField(verbose_name="Approval Status", max_length=60, null=True)
    created_at        = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at        = models.DateTimeField(auto_now=True,blank=False, null=True)
    deleted_at        = models.DateTimeField(blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def has_access(self, level):
        return self.access_group >= level

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return str(self.first_name + ' ' + self.last_name) if self.first_name else ''



    @property
    def isUser(self):
        if self.role == 'user':  
            return True*1    
        return False*0 

    @property
    def isAdministrator(self):
        if self.role == 'administrator':  
            return True*1      
        return False*0 

    @property
    def isTl(self):
        if self.role == 'tl':  
            return True*1      
        return False*0 

    @property
    def isQa(self):
        if self.role == 'qa':  
            return True*1      
        return False*0   

    @property
    def isAdmin(self):
        if self.role == 'admin':  
            return True*1      
        return False*0    

    @property
    def isTlQa(self):
        if self.role == 'tl-qa':  
            return True*1      
        return False*0 
        
    @property
    def isHr(self):
        if self.role == 'hr':  
            return True*1      
        return False*0                   
     
