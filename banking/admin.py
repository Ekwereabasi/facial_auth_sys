# from django.contrib import admin

# # Register your models here.


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Account, Transaction

# CustomUserAdmin class to manage CustomUser model
class CustomUserAdmin(UserAdmin):
    # Fields to display in the user list
    list_display = ('username', 'email', 'phone_number', 'is_staff', 'is_active')
    
    # Fields to search by in the user list
    search_fields = ('username', 'email', 'phone_number')
    
    # Adding custom fields (phone_number and profile_picture) to the user edit form
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'profile_picture')}),
    )
    
    # Adding inline Account management to the user edit page
    inlines = []

# AccountInline class to allow editing Account from within the CustomUser admin page
class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Account'
    fk_name = 'user'

# AccountAdmin class to manage Account model
class AccountAdmin(admin.ModelAdmin):
    # Fields to display in the account list
    list_display = ('user', 'account_type', 'balance')
    
    # Fields to search by in the account list
    search_fields = ('user__username', 'account_type')
    
    # Editable fields in the account edit form
    fields = ('user', 'account_type', 'balance')
    
    # Read-only fields in the account edit form
    readonly_fields = ('balance',)

# TransactionAdmin class to manage Transaction model
class TransactionAdmin(admin.ModelAdmin):
    # Fields to display in the transaction list
    list_display = ('account', 'transaction_type', 'amount', 'timestamp')
    
    # Fields to search by in the transaction list
    search_fields = ('account__user__username', 'transaction_type', 'description')
    
    # Fields to filter by in the transaction list
    list_filter = ('transaction_type', 'timestamp')
    
    # Editable fields in the transaction edit form
    fields = ('account', 'transaction_type', 'amount', 'description', 'timestamp')
    
    # Read-only fields in the transaction edit form
    readonly_fields = ('timestamp',)

# Register the models with their admin classes
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
