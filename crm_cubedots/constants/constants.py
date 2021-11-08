STATUS =(
    ("","Select"),
    ("active", "active"),
    ("completed", "completed"),
    ("on-hold", "on-hold"),
    ("upcoming", "upcoming"),
)
 
PARENT_ID = (
    ("","Select"),
    ("0","Main Category"),
)

TASK_PARENT_ID = (
    ("","Select"),
    ("0","Main Task"),
)

USER_ROLE =(
    ("","Select"),
    ("user", "User"),
    ("hr", "HR"),
    ("hr_admin", "HR Admin"),
    ("tl", "TL"),
    ("qa", "QA"),
    ("admin", "Admin"),
    ("administrator", "Administrator"),
)

ACTIVE_STATUS =(
    ("","Select"),
    ("active", "active"),
    ("inactive", "In-active"),
)

GENDER =(
    ("","Select"),
    ("male", "Male"),
    ("female", "Female"),
)

APPROVAL_ADMIN =(
    ("pending", "Un-completed"),
)

APPROVAL_HR =(
    ("completed", "Completed"),
)

YES_NO = (
    ("","Select"),
    ("0","No"),
    ("1", "Yes"),
    
)

TASK_STATUS = (
    ("","Select"),
    ('active' , 'active'),
        ('delayed_due_to_cubedots' , 'delayed_due_to_cubedots'),
        ('delayed_due_to_client' , 'delayed_due_to_client'),
        ('delayed_due_to_without_resource' , 'delayed_due_to_without_resource'),
        ('delayed_due_to_client_satisfaction' , 'delayed_due_to_client_satisfaction'),
        ('on_time' , 'on_time'),
        ('on_hold_due_to_cubedots' , 'on_hold_due_to_cubedots'),
        ('on_hold_due_to_client' , 'on_hold_due_to_client'),
        ('completed' , 'completed'),
)

TASK_PROCESS_STATUS = (
    ("","Select"),
    ('unassigned' , 'unassigned'),
        ('assigned' , 'assigned'),
        ('user_started' , 'user_started'),
        ('forwarded_to_tl' , 'forwarded_to_tl'),
        ('tl_started' , 'tl_started'),
        ('tl_rejected' , 'tl_rejected'),
        ('forwarded_to_qc' , 'forwarded_to_qc'),
        ('qc_started' , 'qc_started'),
        ('qc_rejected' , 'qc_rejected'),
        ('completed' , 'completed'),
)

SELECT = (
    ("","Select"),
)

BLOOD_GROUPS = (
        ('','Select'),
        ('o+' , 'O positive'),
        ('o-' , 'O negative'),
        ('a+' , 'A positive'),
        ('a-' , 'A negative'),
        ('b+' , 'B positive'),
        ('b-' , 'B negative'),
        ('ab+' , 'AB positive'),
        ('ab-' , 'AB negative'),
)
PRIORITY = (
        ('','Select'),
        ('extreme high','Extreme High'),
        ('high','High'),
        ('medium','Medium'),
        ('low','Low'),
)

USER_TASK_PROCESS_STATUS = {
    'user_started' : 'user_started',
    'assigned' : 'assigned',
    'unassigned' : 'unassigned',
    'forwarded_to_tl' : 'forwarded_to_tl',
    'tl_started' : 'tl_started',
    'tl_rejected' : 'tl_rejected',
    'forwarded_to_qc' : 'forwarded_to_qc',
    'qc_started' : 'qc_started',
    'qc_rejected' : 'qc_rejected',
    'completed' : 'completed',
    }

user_task_process_status_list_access = [
    {'user_started' : 'start'},
    {'forwarded_to_tl' : 'submit'}
    ]
tl_task_process_status_list_access = [
        {'tl_started' : 'start'},
        {'tl_rejected' : 'reject'},
        {'forwarded_to_qc' : 'forward'},
    ]
qa_task_process_status_list_access = [
        {'qc_started' : 'start'},
        {'qc_rejected' : 'reject'},
        {'completed' : 'complete'},
]
user_task_process_status_timer_view_access = [
        'assigned',
        'user_started',
        'tl_rejected',
        'qc_rejected',
]
tl_task_process_status_timer_view_access = [
        'tl_started',
        'forwarded_to_tl',
]
qa_task_process_status_timer_view_access = [
        'qc_started',
        'forwarded_to_qc',
]
tl_as_user_task_process_status_list_access = [
        {'tl_started' : 'start'},        
        {'forwarded_to_qc' : 'submit'},
]
tl_as_user_task_process_status_timer_view_access = [
        'assigned',
        'tl_started',
        'qc_rejected',      
]
qa_as_user_task_process_status_list_access = [
        {'qc_started' : 'start'},        
        {'completed' : 'completed'},
]
qa_as_user_task_process_status_timer_view_access = [
        'assigned',
        'qc_started',
       'completed',      
]

LEAVES_APPROVAL = [
    ('','Select'),
    ('rejected','Reject'),
    ('approved','Approve')
]