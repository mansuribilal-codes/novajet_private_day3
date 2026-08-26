from django.db import models
from django.contrib.auth.models import User
import uuid

class FleetAircraft(models.Model):
    CATEGORY_CHOICES = [
        ('light', 'Light Jet'),
        ('midsize', 'Midsize Jet'),
        ('super_midsize', 'Super Midsize Jet'),
        ('heavy', 'Heavy Jet'),
        ('ultra_long_range', 'Ultra Long Range'),
    ]

    name = models.CharField(max_length=120)
    manufacturer = models.CharField(max_length=100)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES, default='ultra_long_range')
    tagline = models.CharField(max_length=255)
    description = models.TextField()
    
    # Specs
    range_nm = models.IntegerField(help_text="Nautical Miles (nm)")
    speed_mach = models.DecimalField(max_digits=4, decimal_places=2, help_text="e.g. 0.90")
    max_passengers = models.IntegerField()
    cabin_height = models.CharField(max_length=50, default="6 ft 2 in")
    cabin_width = models.CharField(max_length=50, default="8 ft 0 in")
    cabin_length = models.CharField(max_length=50, default="54 ft")
    baggage_cu_ft = models.IntegerField(default=195, help_text="Cubic feet")
    hourly_rate_usd = models.IntegerField(default=12000)
    
    # Media
    exterior_image = models.URLField(max_length=600)
    interior_image = models.URLField(max_length=600)
    
    # Features list (stored as newline separated text)
    amenities = models.TextField(help_text="Newline separated list of luxury cabin amenities")
    
    featured = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Fleet Aircraft"
        verbose_name_plural = "Fleet Aircraft"

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    @property
    def amenities_list(self):
        return [item.strip() for item in self.amenities.split('\n') if item.strip()]

    @property
    def range_km(self):
        return int(self.range_nm * 1.852)


class Destination(models.Model):
    REGION_CHOICES = [
        ('middle_east', 'Middle East'),
        ('europe', 'Europe'),
        ('americas', 'Americas'),
        ('asia_pacific', 'Asia Pacific'),
        ('caribbean_islands', 'Exotic & Islands'),
    ]

    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    airport_code = models.CharField(max_length=20, help_text="e.g. DXB / OMDB")
    fbo_terminal = models.CharField(max_length=150, help_text="e.g. Jetex Executive Lounge")
    region = models.CharField(max_length=40, choices=REGION_CHOICES, default='europe')
    tagline = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(max_length=600)
    
    flight_time_london = models.CharField(max_length=50, default="6h 45m")
    flight_time_ny = models.CharField(max_length=50, default="12h 30m")
    featured = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.airport_code})"


class MembershipTier(models.Model):
    TIER_CHOICES = [
        ('access', 'Access Tier'),
        ('prestige', 'Prestige Tier'),
        ('sovereign', 'Sovereign Tier'),
    ]

    tier_key = models.CharField(max_length=30, choices=TIER_CHOICES, unique=True)
    name = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    annual_commitment = models.CharField(max_length=100)
    hourly_rate_info = models.CharField(max_length=150)
    availability_guarantee = models.CharField(max_length=100, default="24 Hours Notice")
    perks = models.TextField(help_text="Newline separated perks")
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    @property
    def perks_list(self):
        return [item.strip() for item in self.perks.split('\n') if item.strip()]


class EmptyLegDeal(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending', 'Under Inquiry'),
        ('booked', 'Booked'),
    ]

    origin_city = models.CharField(max_length=100)
    origin_code = models.CharField(max_length=20)
    destination_city = models.CharField(max_length=100)
    destination_code = models.CharField(max_length=20)
    departure_date = models.CharField(max_length=60)
    aircraft_name = models.CharField(max_length=120)
    aircraft_category = models.CharField(max_length=60)
    passenger_capacity = models.IntegerField(default=12)
    regular_price_usd = models.IntegerField()
    empty_leg_price_usd = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.origin_city} -> {self.destination_city} ({self.aircraft_name})"

    @property
    def savings_percent(self):
        if self.regular_price_usd > 0:
            diff = self.regular_price_usd - self.empty_leg_price_usd
            return int((diff / self.regular_price_usd) * 100)
        return 0


class CharterInquiry(models.Model):
    TRIP_TYPES = [
        ('one_way', 'One Way'),
        ('round_trip', 'Round Trip'),
        ('multi_city', 'Multi-City'),
        ('empty_leg', 'Empty Leg'),
    ]

    STATUS_CHOICES = [
        ('new', 'New Inquiry'),
        ('contacted', 'Contacted / Sourcing'),
        ('confirmed', 'Booked & Confirmed'),
        ('archived', 'Archived'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='charter_inquiries')
    reference_code = models.CharField(max_length=30, unique=True, editable=False)
    trip_type = models.CharField(max_length=20, choices=TRIP_TYPES, default='one_way')
    departure_city = models.CharField(max_length=150)
    arrival_city = models.CharField(max_length=150)
    departure_date = models.CharField(max_length=50)
    departure_time = models.CharField(max_length=50, blank=True, default="Flexible / Any Time")
    return_date = models.CharField(max_length=50, blank=True, null=True)
    passenger_count = models.IntegerField(default=4)
    preferred_category = models.CharField(max_length=100, blank=True, default="Ultra Long Range")
    
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=60)
    catering_preferences = models.CharField(max_length=255, blank=True)
    special_requests = models.TextField(blank=True)
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Charter Inquiry"
        verbose_name_plural = "Charter Inquiries"

    def save(self, *args, **kwargs):
        if not self.reference_code:
            short_id = uuid.uuid4().hex[:6].upper()
            self.reference_code = f"NVJ-{short_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference_code} | {self.full_name} ({self.departure_city} -> {self.arrival_city})"


class MembershipInquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='membership_inquiries')
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=60)
    company = models.CharField(max_length=150, blank=True)
    preferred_tier = models.CharField(max_length=100)
    annual_flight_hours = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Membership Inquiry"
        verbose_name_plural = "Membership Inquiries"

    def __str__(self):
        return f"{self.full_name} - {self.preferred_tier} ({self.created_at.strftime('%Y-%m-%d')})"
