import json
import math
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import FleetAircraft, Destination, MembershipTier, EmptyLegDeal, CharterInquiry, MembershipInquiry

# Global airport coordinates for real Great Circle distance calculation
AIRPORT_COORDINATES = {
    'LONDON': {'name': 'London Farnborough (FAB)', 'lat': 51.2758, 'lon': -0.7763, 'code': 'FAB'},
    'NEW YORK': {'name': 'New York Teterboro (TEB)', 'lat': 40.8501, 'lon': -74.0608, 'code': 'TEB'},
    'DUBAI': {'name': 'Dubai Al Maktoum (DWC)', 'lat': 24.8960, 'lon': 55.1713, 'code': 'DWC'},
    'GENEVA': {'name': 'Geneva Cointrin (GVA)', 'lat': 46.2381, 'lon': 6.1090, 'code': 'GVA'},
    'NICE': {'name': 'Nice Côte d’Azur (NCE)', 'lat': 43.6653, 'lon': 7.2150, 'code': 'NCE'},
    'MALE': {'name': 'Malé Velana (MLE)', 'lat': 4.1918, 'lon': 73.5291, 'code': 'MLE'},
    'TOKYO': {'name': 'Tokyo Haneda (HND)', 'lat': 35.5494, 'lon': 139.7798, 'code': 'HND'},
    'ASPEN': {'name': 'Aspen Pitkin (ASE)', 'lat': 39.2232, 'lon': -106.8689, 'code': 'ASE'},
    'PALM BEACH': {'name': 'Palm Beach Intl (PBI)', 'lat': 26.6832, 'lon': -80.0956, 'code': 'PBI'},
    'PARIS': {'name': 'Paris Le Bourget (LBG)', 'lat': 48.9694, 'lon': 2.4414, 'code': 'LBG'},
    'SINGAPORE': {'name': 'Singapore Seletar (XSP)', 'lat': 1.4169, 'lon': 103.8653, 'code': 'XSP'},
    'ZURICH': {'name': 'Zurich Kloten (ZRH)', 'lat': 47.4582, 'lon': 8.5555, 'code': 'ZRH'},
    'ST MORITZ': {'name': 'Samedan St. Moritz (SMV)', 'lat': 46.5342, 'lon': 9.8841, 'code': 'SMV'},
    'LOS ANGELES': {'name': 'Van Nuys Los Angeles (VNY)', 'lat': 34.2098, 'lon': -118.4899, 'code': 'VNY'},
}

def calculate_distance_nm(lat1, lon1, lat2, lon2):
    r = 3440.065  # Earth radius in nautical miles
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(r * c)

@ensure_csrf_cookie
def home_view(request):
    fleet = FleetAircraft.objects.all()
    destinations = Destination.objects.all()
    tiers = MembershipTier.objects.all()
    empty_legs = EmptyLegDeal.objects.filter(status='available')

    categories = [
        {'key': 'all', 'label': 'All Flagships', 'count': fleet.count()},
        {'key': 'ultra_long_range', 'label': 'Ultra Long Range', 'count': fleet.filter(category='ultra_long_range').count()},
        {'key': 'heavy', 'label': 'Heavy Jets', 'count': fleet.filter(category='heavy').count()},
        {'key': 'super_midsize', 'label': 'Super Midsize', 'count': fleet.filter(category='super_midsize').count()},
        {'key': 'midsize', 'label': 'Midsize', 'count': fleet.filter(category='midsize').count()},
        {'key': 'light', 'label': 'Light Jets', 'count': fleet.filter(category='light').count()},
    ]

    context = {
        'fleet': fleet,
        'destinations': destinations,
        'tiers': tiers,
        'empty_legs': empty_legs,
        'categories': categories,
        'airport_options': list(AIRPORT_COORDINATES.keys()),
    }
    return render(request, 'index.html', context)


def developer_view(request):
    developer_info = {
        'name': 'MOHAMMED BILAL MANSURI',
        'title': 'Full Stack Web Developer (Python / Django)',
        'phone': '+919723918213',
        'email': 'mansuribilal9792@gmail.com',
        'linkedin': 'https://www.linkedin.com/in/mohammed-bilal-mansuri-972013204',
        'linkedin_display': 'linkedin.com/in/mohammed-bilal-mansuri-972013204',
        'github': 'https://github.com/mansuribilal-codes',
        'github_display': 'github.com/mansuribilal-codes',
        'profile_image': 'https://sulead.in/static/img/Bilal_Mansuri.jpg',
        'bio': 'Passionate Full Stack Developer specializing in high-performance Python, Django, REST APIs, modern reactive frontend engineering, and building world-class client-ready digital platforms.',
        'skills': [
            'Python & Django Architecture',
            'Full Stack Web Development',
            'RESTful APIs & Database Optimization',
            'Modern Frontend UI/UX (HTML5, CSS3, GSAP, Three.js)',
            'JavaScript / TypeScript & Performance Tuning',
            'Scalable Cloud Deployment & DevOps'
        ]
    }
    return render(request, 'developer.html', {'dev': developer_info})


# =========================================================================
# Authentication Views (Login, Register, Logout)
# =========================================================================

@require_http_methods(["POST"])
def auth_login_api(request):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        username_or_email = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if not username_or_email or not password:
            return JsonResponse({'success': False, 'error': 'Please provide username and password.'}, status=400)

        # Check if login with email
        user = authenticate(request, username=username_or_email, password=password)
        if user is None:
            # Try finding user by email
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            return JsonResponse({
                'success': True,
                'username': user.username,
                'full_name': user.get_full_name() or user.username,
                'message': f'Welcome aboard, VIP {user.get_full_name() or user.username}.'
            })
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials. Please verify your username/email and password.'}, status=401)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
def auth_register_api(request):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        full_name = data.get('full_name', '').strip()

        if not username or not email or not password:
            return JsonResponse({'success': False, 'error': 'Username, email, and password are required.'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Username is already registered.'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Email address is already associated with an account.'}, status=400)

        first_name = full_name.split()[0] if full_name else username
        last_name = " ".join(full_name.split()[1:]) if len(full_name.split()) > 1 else ""

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        login(request, user)

        return JsonResponse({
            'success': True,
            'username': user.username,
            'full_name': user.get_full_name() or user.username,
            'message': f'Account created successfully. Welcome to NovaJet Private, {user.username}.'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def auth_logout_view(request):
    logout(request)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse({'success': True, 'message': 'Logged out successfully.'})
    return redirect('charter:home')


# =========================================================================
# Flight Operations & Charter APIs
# =========================================================================

@require_http_methods(["POST"])
def submit_charter_api(request):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        full_name = data.get('full_name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        departure_city = data.get('departure_city', '').strip()
        arrival_city = data.get('arrival_city', '').strip()
        departure_date = data.get('departure_date', '').strip()
        departure_time = data.get('departure_time', 'Flexible / Any Time').strip()
        return_date = data.get('return_date', '').strip()
        trip_type = data.get('trip_type', 'one_way')
        passenger_count = int(data.get('passenger_count', 4))
        preferred_category = data.get('preferred_category', 'Ultra Long Range')
        catering_preferences = data.get('catering_preferences', '').strip()
        special_requests = data.get('special_requests', '').strip()

        # Validation
        if not full_name or not email or not phone or not departure_city or not arrival_city or not departure_date:
            return JsonResponse({
                'success': False,
                'error': 'Please provide all mandatory flight parameters (Name, Contact, Route, and Date).'
            }, status=400)

        inquiry = CharterInquiry.objects.create(
            user=request.user if request.user.is_authenticated else None,
            trip_type=trip_type,
            departure_city=departure_city,
            arrival_city=arrival_city,
            departure_date=departure_date,
            departure_time=departure_time,
            return_date=return_date if return_date else None,
            passenger_count=passenger_count,
            preferred_category=preferred_category,
            full_name=full_name,
            email=email,
            phone=phone,
            catering_preferences=catering_preferences,
            special_requests=special_requests,
            status='new'
        )

        return JsonResponse({
            'success': True,
            'reference_code': inquiry.reference_code,
            'client_name': inquiry.full_name,
            'route': f"{inquiry.departure_city} ➔ {inquiry.arrival_city}",
            'date': inquiry.departure_date,
            'message': 'Your mission flight brief has been transmitted to NovaJet Global Operations Command. A dedicated Flight Director will contact you within 15 minutes.'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
def submit_membership_api(request):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        full_name = data.get('full_name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        company = data.get('company', '').strip()
        preferred_tier = data.get('preferred_tier', 'Prestige Tier').strip()
        annual_flight_hours = data.get('annual_flight_hours', '50-100 Hours').strip()
        notes = data.get('notes', '').strip()

        if not full_name or not email or not phone:
            return JsonResponse({
                'success': False,
                'error': 'Name, Email, and Phone number are required to process membership applications.'
            }, status=400)

        inquiry = MembershipInquiry.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            phone=phone,
            company=company,
            preferred_tier=preferred_tier,
            annual_flight_hours=annual_flight_hours,
            notes=notes
        )

        return JsonResponse({
            'success': True,
            'client_name': inquiry.full_name,
            'tier': inquiry.preferred_tier,
            'message': f'Thank you. Your dossier for {inquiry.preferred_tier} has been presented to the NovaJet Sovereign Admissions Committee. An invitation package will be dispatched.'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def route_calculator_api(request):
    origin = request.GET.get('origin', 'LONDON').upper().strip()
    destination = request.GET.get('destination', 'DUBAI').upper().strip()

    orig_data = AIRPORT_COORDINATES.get(origin, AIRPORT_COORDINATES['LONDON'])
    dest_data = AIRPORT_COORDINATES.get(destination, AIRPORT_COORDINATES['DUBAI'])

    distance_nm = calculate_distance_nm(orig_data['lat'], orig_data['lon'], dest_data['lat'], dest_data['lon'])
    distance_km = round(distance_nm * 1.852)

    avg_speed_kts = 490
    flight_time_hours = distance_nm / avg_speed_kts + 0.35
    hours = int(flight_time_hours)
    minutes = int((flight_time_hours - hours) * 60)
    flight_time_str = f"{hours}h {minutes:02d}m"

    if distance_nm > 4000:
        recommended_tier = "Ultra Long Range"
        recommended_jet = "Bombardier Global 7500 / Gulfstream G700"
        cruise_alt = "FL470 - FL510 (Above All Weather)"
        fuel_stops = "0 (Non-Stop Transcontinental)"
    elif distance_nm > 2500:
        recommended_tier = "Heavy / Super Midsize Jet"
        recommended_jet = "Dassault Falcon 8X / Bombardier Challenger 3500"
        cruise_alt = "FL430 - FL450"
        fuel_stops = "0 (Direct Flight)"
    elif distance_nm > 1200:
        recommended_tier = "Super Midsize / Midsize Jet"
        recommended_jet = "Embraer Praetor 600 / Citation Latitude"
        cruise_alt = "FL410 - FL450"
        fuel_stops = "0 (Direct Flight)"
    else:
        recommended_tier = "Light Jet"
        recommended_jet = "Embraer Phenom 300E"
        cruise_alt = "FL390 - FL410"
        fuel_stops = "0 (Direct Flight)"

    return JsonResponse({
        'origin': orig_data,
        'destination': dest_data,
        'distance_nm': distance_nm,
        'distance_km': distance_km,
        'flight_time': flight_time_str,
        'recommended_tier': recommended_tier,
        'recommended_jet': recommended_jet,
        'cruise_alt': cruise_alt,
        'fuel_stops': fuel_stops,
        'co2_offset': '100% Carbon Neutral Verified'
    })


def fleet_api(request):
    category = request.GET.get('category', 'all')
    queryset = FleetAircraft.objects.all()
    if category != 'all':
        queryset = queryset.filter(category=category)

    data = []
    for jet in queryset:
        data.append({
            'id': jet.id,
            'name': jet.name,
            'manufacturer': jet.manufacturer,
            'category': jet.get_category_display(),
            'tagline': jet.tagline,
            'description': jet.description,
            'range_nm': jet.range_nm,
            'range_km': jet.range_km,
            'speed_mach': float(jet.speed_mach),
            'max_passengers': jet.max_passengers,
            'cabin_height': jet.cabin_height,
            'cabin_width': jet.cabin_width,
            'cabin_length': jet.cabin_length,
            'baggage_cu_ft': jet.baggage_cu_ft,
            'hourly_rate_usd': jet.hourly_rate_usd,
            'exterior_image': jet.exterior_image,
            'interior_image': jet.interior_image,
            'amenities': jet.amenities_list,
        })
    return JsonResponse({'fleet': data})
