from django.contrib import admin
from .models import Profile
from deposit.models import Deposit
from withdraw.models import Withdrawal
from transfer.models import Transfer
# Register your models here.

class DepositInline(admin.TabularInline):
    model = Deposit
    extra = 0
    readonly_fields = ('verified', 'profile', 'wallet_address', 'amount', 'wallet_type', 'created', 'usdt_amount',)
    
class WithdrawalInline(admin.TabularInline):
    model = Withdrawal
    extra = 0
    readonly_fields = ('verified', 'profile', 'wallet_address', 'amount', 'wallet_type', 'created', 'usdt_amount',)

class TransferInline(admin.TabularInline):
    model = Transfer
    extra = 0
    fk_name = 'profile'
    readonly_fields = ('transfer_profile','created', 'usdt_amount','transferred')
    


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines =[DepositInline,WithdrawalInline,TransferInline]
