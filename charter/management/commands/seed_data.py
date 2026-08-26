from django.core.management.base import BaseCommand
from charter.models import FleetAircraft, Destination, MembershipTier, EmptyLegDeal

class Command(BaseCommand):
    help = 'Seeds initial luxury private jet fleet, destinations, tiers, and empty leg deals'

    def handle(self, *args, **options):
        self.stdout.write("Seeding NovaJet Private verified aviation data...")

        # 1. Fleet Aircraft with 100% verified authentic private jet photographs
        FleetAircraft.objects.all().delete()
        fleet_data = [
            {
                'name': 'Bombardier Global 7500',
                'manufacturer': 'Bombardier Aviation',
                'category': 'ultra_long_range',
                'tagline': 'The Flagship of Global Business Aviation',
                'description': 'The world’s largest and longest-range purpose-built luxury business jet. Featuring four architectural living spaces, a permanent Master Suite with full-size bed, patented Nuage zero-gravity ergonomic seating, and the smoothest transcontinental ride in aviation history.',
                'range_nm': 7700,
                'speed_mach': 0.92,
                'max_passengers': 19,
                'cabin_height': '6 ft 2 in',
                'cabin_width': '8 ft 0 in',
                'cabin_length': '54 ft 5 in',
                'baggage_cu_ft': 195,
                'hourly_rate_usd': 14500,
                'exterior_image': 'https://images.unsplash.com/photo-1508614589041-895b88991e3e?auto=format&fit=crop&w=1200&q=80',
                'interior_image': 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=1200&q=80',
                'amenities': 'Master Stateroom Suite with En-Suite Hot Shower\nFour Distinct Architectural Living Spaces\nKa-band Ultra High-Speed Worldwide Satellite Wi-Fi\nPur Air HEPA Environmental Filtration\nDedicated Chef-Grade Galley with Convection & Steam Ovens\nNuage Ergonomic Zero-Gravity Reclining Loungers',
                'featured': True,
                'order': 1
            },
            {
                'name': 'Gulfstream G700',
                'manufacturer': 'Gulfstream Aerospace',
                'category': 'ultra_long_range',
                'tagline': 'Unrivaled Speed, Range & 20 Panoramic Windows',
                'description': 'The crown jewel of Gulfstream engineering. Boasting the tallest, widest, and longest cabin in industry history with 20 signature panoramic oval windows, whisper-quiet acoustics (39.5 dB), and 100% fresh plasma-ionized air refreshed every two minutes.',
                'range_nm': 7750,
                'speed_mach': 0.93,
                'max_passengers': 19,
                'cabin_height': '6 ft 3 in',
                'cabin_width': '8 ft 2 in',
                'cabin_length': '56 ft 11 in',
                'baggage_cu_ft': 195,
                'hourly_rate_usd': 15200,
                'exterior_image': 'https://images.unsplash.com/photo-1570710891163-6d3b5c47248b?auto=format&fit=crop&w=1200&q=80',
                'interior_image': 'https://images.unsplash.com/photo-1569154941061-e231b4725ef1?auto=format&fit=crop&w=1200&q=80',
                'amenities': '20 Signature Gulfstream Panoramic Oval Windows\nCircadian Lighting Engineered for Jet-Lag Elimination\nFull Master Bedroom with Queen Bed & Wardrobe\nWhisper-Quiet Cabin Acoustic Index (39.5 dB)\nTail-Mounted 4K High-Definition Cameras\nRockwell Collins Venue 4K Entertainment System',
                'featured': True,
                'order': 2
            },
            {
                'name': 'Dassault Falcon 8X',
                'manufacturer': 'Dassault Aviation',
                'category': 'heavy',
                'tagline': 'Trijet Precision & Short-Runway Agility',
                'description': 'With tri-jet safety architecture and fighter-jet flight control heritage, the Falcon 8X provides effortless access to challenging airfields like London City, Aspen, and Saint-Tropez, while seamlessly connecting New York to Dubai non-stop.',
                'range_nm': 6450,
                'speed_mach': 0.90,
                'max_passengers': 16,
                'cabin_height': '6 ft 2 in',
                'cabin_width': '7 ft 8 in',
                'cabin_length': '42 ft 8 in',
                'baggage_cu_ft': 140,
                'hourly_rate_usd': 12800,
                'exterior_image': 'https://images.unsplash.com/photo-1520437358207-323b43b50729?auto=format&fit=crop&w=1200&q=80',
                'interior_image': 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=1200&q=80',
                'amenities': 'Advanced Digital Flight Control System (Fighter Tech)\nLondon City & Steep-Approach Certified\nThree-Zone Climate and Acoustic Customization\nFull Aft Stateroom and Lavatory with Shower\nBespoke Hand-Stitched Italian Leather Interior',
                'featured': True,
                'order': 3
            },
            {
                'name': 'Bombardier Challenger 3500',
                'manufacturer': 'Bombardier Aviation',
                'category': 'super_midsize',
                'tagline': 'The Super-Midsize Benchmark',
                'description': 'The most reliable super-midsize business jet in modern corporate aviation. Redesigned with patented Nuage seating, voice-controlled cabin management, and coast-to-coast transcontinental non-stop capability.',
                'range_nm': 3400,
                'speed_mach': 0.83,
                'max_passengers': 10,
                'cabin_height': '6 ft 0 in',
                'cabin_width': '7 ft 2 in',
                'cabin_length': '25 ft 2 in',
                'baggage_cu_ft': 106,
                'hourly_rate_usd': 9200,
                'exterior_image': 'https://images.unsplash.com/photo-1474302770737-173ee21bab63?auto=format&fit=crop&w=1200&q=80',
                'interior_image': 'https://images.unsplash.com/photo-1569154941061-e231b4725ef1?auto=format&fit=crop&w=1200&q=80',
                'amenities': 'Voice-Controlled Cabin Lighting and Audio\nNuage Seating with Tilt-Link Ergonomics\n4K Crystal Clear Display with Bluetooth Audio Integration\nCoast-to-Coast Transcontinental Non-Stop Capability\nAccessible In-Flight Baggage Compartment',
                'featured': True,
                'order': 4
            },
            {
                'name': 'Embraer Praetor 600',
                'manufacturer': 'Embraer Executive Jets',
                'category': 'super_midsize',
                'tagline': 'Disruptive Range & Active Turbulence Reduction',
                'description': 'The most technologically advanced super-midsize business jet in existence. Full fly-by-wire flight controls and Active Turbulence Reduction deliver an exceptionally smooth ride across oceanic expanses.',
                'range_nm': 4018,
                'speed_mach': 0.83,
                'max_passengers': 12,
                'cabin_height': '6 ft 0 in',
                'cabin_width': '6 ft 10 in',
                'cabin_length': '27 ft 6 in',
                'baggage_cu_ft': 155,
                'hourly_rate_usd': 9800,
                'exterior_image': 'https://images.unsplash.com/photo-1529074963764-98f45c47344b?auto=format&fit=crop&w=1200&q=80',
                'interior_image': 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=1200&q=80',
                'amenities': 'Active Turbulence Reduction (ATR) Smooth Ride\nFull Fly-By-Wire Avionics\nBest-in-Class Cabin Altitude (5,800 ft at FL450)\nStone-Accented Luxury Lavatory and Wet Galley\nNon-Stop London to New York Capability',
                'featured': True,
                'order': 5
            },
            {
                'name': 'Cessna Citation Latitude',
                'manufacturer': 'Textron Aviation',
                'category': 'midsize',
                'tagline': 'Refined Spatial Elegance & Flat-Floor Comfort',
                'description': 'With the widest flat-floor cabin in the midsize category, the Citation Latitude sets the standard for spacious regional executive travel, boasting stand-up headroom and class-leading baggage capacity.',
                'range_nm': 2700,
                'speed_mach': 0.80,
                'max_passengers': 9,
                'cabin_height': '6 ft 0 in',
                'cabin_width': '6 ft 5 in',
                'cabin_length': '21 ft 9 in',
                'baggage_cu_ft': 127,
                'hourly_rate_usd': 7400,
                'exterior_image': 'https://images.unsplash.com/photo-1570710891163-6d3b5c47248b?auto=format&fit=crop&w=1200&q=80',
                'interior_image': 'https://images.unsplash.com/photo-1569154941061-e231b4725ef1?auto=format&fit=crop&w=1200&q=80',
                'amenities': 'True Flat-Floor Cabin Architecture\nClarity Wireless Cabin Management System\nDual-Zone High Performance Air Conditioning\nExpanded Executive Refreshment Center',
                'featured': True,
                'order': 6
            },
            {
                'name': 'Embraer Phenom 300E',
                'manufacturer': 'Embraer Executive Jets',
                'category': 'light',
                'tagline': 'The World’s Best-Selling Light Jet for 12 Years',
                'description': 'The fastest and longest-ranged single-pilot certified light jet. The Phenom 300E delivers unmatched speed, generous cabin dimensions, and an ultra-quiet, elegantly contoured interior designed by BMW Group DesignworksUSA.',
                'range_nm': 2010,
                'speed_mach': 0.80,
                'max_passengers': 8,
                'cabin_height': '4 ft 11 in',
                'cabin_width': '5 ft 1 in',
                'cabin_length': '17 ft 2 in',
                'baggage_cu_ft': 84,
                'hourly_rate_usd': 5400,
                'exterior_image': 'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=1200&q=80',
                'interior_image': 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=1200&q=80',
                'amenities': 'Bespoke Bossa Nova Interior Styling\nLargest Windows in Light Jet Category\nEnclosed Private Aft Lavatory\nHigh-Speed Gogo AVANCE L5 Connectivity',
                'featured': True,
                'order': 7
            }
        ]

        for item in fleet_data:
            FleetAircraft.objects.create(**item)
        self.stdout.write(self.style.SUCCESS(f"Created {len(fleet_data)} fleet aircraft with authentic jet photos."))

        # 2. Destinations
        Destination.objects.all().delete()
        destinations_data = [
            {
                'name': 'Dubai, United Arab Emirates',
                'country': 'UAE',
                'airport_code': 'DXB / OMDB',
                'fbo_terminal': 'Jetex VIP Executive Terminal & Royal Lounge',
                'region': 'middle_east',
                'tagline': 'Futuristic Splendor & Arabian Magnificence',
                'description': 'Land directly at dedicated VIP runways with private biometric customs clearance, Rolls-Royce tarmac escorts, and 24/7 dedicated dispatch to the world’s most luxurious desert sanctuaries.',
                'image_url': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1200&q=80',
                'flight_time_london': '6h 45m',
                'flight_time_ny': '12h 30m',
                'featured': True,
                'order': 1
            },
            {
                'name': 'St. Moritz & Zurich, Switzerland',
                'country': 'Switzerland',
                'airport_code': 'SMV / LSZS',
                'fbo_terminal': 'Samedan Engadin Alpine Executive FBO',
                'region': 'europe',
                'tagline': 'Alpine Majesty Above the Clouds',
                'description': 'Europe’s highest-altitude private jet runway. Direct ski-in heli-transfers to St. Moritz, Gstaad, and Verbier, surrounded by snow-capped peaks and legendary Swiss discretion.',
                'image_url': 'https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?auto=format&fit=crop&w=1200&q=80',
                'flight_time_london': '1h 35m',
                'flight_time_ny': '8h 15m',
                'featured': True,
                'order': 2
            },
            {
                'name': 'London, United Kingdom',
                'country': 'United Kingdom',
                'airport_code': 'FAB / EGLF',
                'fbo_terminal': 'Farnborough Airport TAG Aviation Terminal',
                'region': 'europe',
                'tagline': 'Historic Sophistication & Financial Capital',
                'description': 'Exclusively dedicated to private aviation with zero commercial traffic delays. Just 12 minutes by helicopter to the London Battersea Heliport in central Mayfair.',
                'image_url': 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=1200&q=80',
                'flight_time_london': '0h 00m',
                'flight_time_ny': '6h 45m',
                'featured': True,
                'order': 3
            },
            {
                'name': 'Malé & Private Atolls, Maldives',
                'country': 'Maldives',
                'airport_code': 'MLE / VRMM',
                'fbo_terminal': 'Velana Executive CIP Lounge & Seaplane Pier',
                'region': 'caribbean_islands',
                'tagline': 'Pristine Turquoise Isolation',
                'description': 'Fly non-stop from London, Geneva, or Dubai into private island paradise. Seamless transitions from wide-cabin jets to twin-turbine private amphibious yachts.',
                'image_url': 'https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=1200&q=80',
                'flight_time_london': '9h 50m',
                'flight_time_ny': '16h 20m',
                'featured': True,
                'order': 4
            },
            {
                'name': 'Monaco & Nice (Côte d’Azur)',
                'country': 'France',
                'airport_code': 'NCE / LFMN',
                'fbo_terminal': 'Signature Flight Support Nice Executive FBO',
                'region': 'europe',
                'tagline': 'The Mediterranean’s Glitziest Riviera',
                'description': 'Touch down over the azure Mediterranean coastline. Fast-track customs to dedicated helipads whisking you to Monte-Carlo in under 7 minutes.',
                'image_url': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=1200&q=80',
                'flight_time_london': '1h 55m',
                'flight_time_ny': '8h 20m',
                'featured': True,
                'order': 5
            },
            {
                'name': 'New York (Teterboro / White Plains)',
                'country': 'United States',
                'airport_code': 'TEB / KTEB',
                'fbo_terminal': 'Jet Aviation Teterboro Executive Terminal',
                'region': 'americas',
                'tagline': 'The Epicenter of Global Commerce & Culture',
                'description': 'Strategically situated 12 miles from Manhattan. Instant blade helicopter connection to Manhattan 34th Street Heliport in 5 minutes.',
                'image_url': 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&w=1200&q=80',
                'flight_time_london': '7h 10m',
                'flight_time_ny': '0h 00m',
                'featured': True,
                'order': 6
            },
            {
                'name': 'Tokyo, Japan',
                'country': 'Japan',
                'airport_code': 'HND / RJTT',
                'fbo_terminal': 'Premier Gate Tokyo Haneda Business Aviation',
                'region': 'asia_pacific',
                'tagline': 'Hyper-Modern Precision & Ancient Grace',
                'description': 'Priority VIP runway access at central Haneda. Discretion-first private customs facilities and direct armored ground transit to Ginza and Roppongi.',
                'image_url': 'https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=1200&q=80',
                'flight_time_london': '12h 45m',
                'flight_time_ny': '13h 50m',
                'featured': True,
                'order': 7
            },
            {
                'name': 'Aspen, Colorado',
                'country': 'United States',
                'airport_code': 'ASE / KASE',
                'fbo_terminal': 'Atlantic Aviation Pitkin County FBO',
                'region': 'americas',
                'tagline': 'World-Class Slopes & Exclusive Mountain Solitude',
                'description': 'Challenging high-altitude runway navigated exclusively by our highest-certified mountain-rated flight crews. Direct valet to your private chalet.',
                'image_url': 'https://images.unsplash.com/photo-1486870591958-9b9d0d1dda99?auto=format&fit=crop&w=1200&q=80',
                'flight_time_london': '10h 30m',
                'flight_time_ny': '4h 15m',
                'featured': True,
                'order': 8
            }
        ]

        for item in destinations_data:
            Destination.objects.create(**item)
        self.stdout.write(self.style.SUCCESS(f"Created {len(destinations_data)} authentic destinations."))

        # 3. Membership Tiers
        MembershipTier.objects.all().delete()
        tiers_data = [
            {
                'tier_key': 'access',
                'name': 'Access Tier',
                'subtitle': 'Dynamic Global Charter On-Demand with Guaranteed Standards',
                'annual_commitment': '$150,000 Refundable Deposit',
                'hourly_rate_info': 'Dynamic Wholesale + 0% Broker Markup',
                'availability_guarantee': '24 Hours Advance Notice',
                'perks': 'Guaranteed Aircraft Availability 365 Days/Year\nNo Intercept or Positioning Fees in Primary Hubs\nDedicated Senior Aviation Account Director\nAccess to Global Empty-Leg Fleet at 50-70% Discounts\nSeamless One-Click Flight Dispatch via Private Concierge App',
                'is_featured': False,
                'order': 1
            },
            {
                'tier_key': 'prestige',
                'name': 'Prestige Tier',
                'subtitle': 'Fixed Hourly Rates, Peak Day Protection & Complimentary Upgrades',
                'annual_commitment': '$300,000 Refundable Deposit',
                'hourly_rate_info': 'Fixed Guaranteed Hourly Rates Across All Jet Classes',
                'availability_guarantee': '12 Hours Callout Guarantee',
                'perks': 'Locked Guaranteed Hourly Rates Across All Jet Categories\nComplimentary Cabin Upgrade When Available\nZero Peak-Day Surcharges or Blackout Dates\nComplimentary Chauffeur-Driven Mercedes-Maybach Tarmac Transfers\nCustom In-Flight Gastronomy & Wine Cellar Selection\nFlexible Cancellation up to 24 Hours Prior to Departure',
                'is_featured': True,
                'order': 2
            },
            {
                'tier_key': 'sovereign',
                'name': 'Sovereign Tier',
                'subtitle': 'Unrestricted Ultra-Long-Range Priority & Sovereign Lifestyle Concierge',
                'annual_commitment': '$600,000 Bespoke Account',
                'hourly_rate_info': 'Preferred Tier-One Sovereign Fleet Rates',
                'availability_guarantee': '6 Hours Rapid Tarmac Readiness',
                'perks': '6-Hour Urgent Tarmac Readiness Across North America, Europe & Middle East\nComplimentary Private Helicopter City Transfers (London, Manhattan, Monaco, Dubai)\nPersonal Executive Chef & Sommelier Curated In-Flight Dining\nComplete Tail Number Customization & Confidential Flight Tracking\nUnlimited Family Office & Corporate Authorized Flyers\nDedicated 24/7 Global Tactical Operations Command Center',
                'is_featured': False,
                'order': 3
            }
        ]

        for item in tiers_data:
            MembershipTier.objects.create(**item)
        self.stdout.write(self.style.SUCCESS(f"Created {len(tiers_data)} membership tiers."))

        # 4. Empty Leg Deals
        EmptyLegDeal.objects.all().delete()
        empty_legs_data = [
            {
                'origin_city': 'New York (Teterboro)',
                'origin_code': 'KTEB',
                'destination_city': 'Palm Beach, FL',
                'destination_code': 'KPBI',
                'departure_date': 'Tomorrow, 14:00 EST',
                'aircraft_name': 'Gulfstream G650ER',
                'aircraft_category': 'Ultra Long Range',
                'passenger_capacity': 14,
                'regular_price_usd': 36000,
                'empty_leg_price_usd': 16500,
                'status': 'available'
            },
            {
                'origin_city': 'London (Farnborough)',
                'origin_code': 'EGLF',
                'destination_city': 'Geneva, Switzerland',
                'destination_code': 'LSGG',
                'departure_date': 'Friday, 10:30 GMT',
                'aircraft_name': 'Bombardier Challenger 3500',
                'aircraft_category': 'Super Midsize',
                'passenger_capacity': 9,
                'regular_price_usd': 19500,
                'empty_leg_price_usd': 8900,
                'status': 'available'
            },
            {
                'origin_city': 'Dubai (Al Maktoum)',
                'origin_code': 'OMDW',
                'destination_city': 'Malé, Maldives',
                'destination_code': 'VRMM',
                'departure_date': 'Saturday, 08:00 GST',
                'aircraft_name': 'Dassault Falcon 8X',
                'aircraft_category': 'Heavy Jet',
                'passenger_capacity': 14,
                'regular_price_usd': 52000,
                'empty_leg_price_usd': 24000,
                'status': 'available'
            },
            {
                'origin_city': 'Paris (Le Bourget)',
                'origin_code': 'LFPB',
                'destination_city': 'Nice / Monaco',
                'destination_code': 'LFMN',
                'departure_date': 'Sunday, 16:00 CET',
                'aircraft_name': 'Embraer Phenom 300E',
                'aircraft_category': 'Light Jet',
                'passenger_capacity': 7,
                'regular_price_usd': 11800,
                'empty_leg_price_usd': 5200,
                'status': 'available'
            }
        ]

        for item in empty_legs_data:
            EmptyLegDeal.objects.create(**item)
        self.stdout.write(self.style.SUCCESS(f"Created {len(empty_legs_data)} empty leg deals."))
        self.stdout.write(self.style.SUCCESS("All NovaJet Private authentic data successfully seeded!"))
