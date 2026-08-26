from django.contrib import admin
from .models import FleetAircraft, Destination, MembershipTier, EmptyLegDeal, CharterInquiry, MembershipInquiry

@admin.register(FleetAircraft)
class FleetAircraftAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'range_nm', 'speed_mach', 'max_passengers', 'hourly_rate_usd', 'featured', 'order')
    list_filter = ('category', 'featured', 'manufacturer')
    search_fields = ('name', 'manufacturer', 'description')
    ordering = ('order', 'name')

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'airport_code', 'region', 'featured', 'order')
    list_filter = ('region', 'featured')
    search_fields = ('name', 'country', 'airport_code', 'fbo_terminal')
    ordering = ('order', 'name')

@admin.register(MembershipTier)
class MembershipTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'tier_key', 'annual_commitment', 'availability_guarantee', 'is_featured', 'order')
    ordering = ('order',)

@admin.register(EmptyLegDeal)
class EmptyLegDealAdmin(admin.ModelAdmin):
    list_display = ('origin_city', 'destination_city', 'departure_date', 'aircraft_name', 'regular_price_usd', 'empty_leg_price_usd', 'status')
    list_filter = ('status', 'aircraft_category')
    search_fields = ('origin_city', 'destination_city', 'aircraft_name')

@admin.register(CharterInquiry)
class CharterInquiryAdmin(admin.ModelAdmin):
    list_display = ('reference_code', 'full_name', 'trip_type', 'departure_city', 'arrival_city', 'departure_date', 'passenger_count', 'status', 'created_at')
    list_filter = ('status', 'trip_type', 'created_at')
    search_fields = ('reference_code', 'full_name', 'email', 'phone', 'departure_city', 'arrival_city')
    readonly_fields = ('reference_code', 'created_at')
    ordering = ('-created_at',)

@admin.register(MembershipInquiry)
class MembershipInquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'preferred_tier', 'email', 'phone', 'company', 'created_at')
    list_filter = ('preferred_tier', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'company')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
