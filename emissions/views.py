# emissions/views.py
# emissions/views.py

from django.shortcuts import render , redirect 
from django.contrib.auth.decorators import login_required
from .models import Action
from .forms import RegisterForm
from django.http import JsonResponse
from django.db.models import Sum
import requests
from .models import EmissionLog

@login_required
def dashboard(request):
    actions = Action.objects.filter(user=request.user)
    total_saved = sum(action.co2_saved_kg for action in actions)
    return render(request, 'dashboard.html', {
        'total_saved': total_saved
    })
def register(request):
    return render(request, 'registration/register.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after registration (optional)
            return redirect('home')  # or wherever you want to send user after signup
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
    
         

# Emission Factors (example values, adjust as per your data)
EMISSIONS_FACTORS = {
    'car': 0.25,  # g CO2 per km for gasoline cars
    'plane': 0.15,  # g CO2 per mile for flights
    'methane': 0.5,  # methane emissions factor for landfill (kg CO2 per kg of waste)
    'electricity': 0.2,  # g CO2 per kWh
    'tree_sequestration': 22,  # kg CO2 sequestered per tree per year
}

# Function to calculate emissions for traveling
def calculate_travel_emissions(distance, travel_type='car'):
    if travel_type == 'car':
        return distance * EMISSIONS_FACTORS['car']
    elif travel_type == 'plane':
        return distance * EMISSIONS_FACTORS['plane']
    else:
        return 0

# Function to calculate emissions from waste management
def calculate_waste_emissions(waste_amount, waste_type='landfill'):
    if waste_type == 'landfill':
        return waste_amount * EMISSIONS_FACTORS['methane']
    else:
        return 0  # You could add more waste types like recycling if needed

# Function to calculate saved energy emissions
def calculate_saved_energy_emissions(energy_saved_kWh):
    return energy_saved_kWh * EMISSIONS_FACTORS['electricity']

# Function to calculate carbon sequestration through eco projects (e.g., trees planted)
def calculate_eco_project_emissions(trees_planted):
    return trees_planted * EMISSIONS_FACTORS['tree_sequestration']

# View to handle emissions calculation
def calculate_emissions(request):
    if request.method == 'POST':
        try:
            # Get data from the form (or from API, depending on how you send it)
            distance = float(request.POST.get('distance', 0))
            travel_type = request.POST.get('travel_type', 'car')
            waste_amount = float(request.POST.get('waste_amount', 0))
            energy_saved_kWh = float(request.POST.get('energy_saved_kWh', 0))
            trees_planted = int(request.POST.get('trees_planted', 0))

            # Calculate emissions for each category
            travel_emissions = calculate_travel_emissions(distance, travel_type)
            waste_emissions = calculate_waste_emissions(waste_amount)
            energy_saved_emissions = calculate_saved_energy_emissions(energy_saved_kWh)
            eco_project_emissions = calculate_eco_project_emissions(trees_planted)

            # Total Emissions
            total_emissions = travel_emissions + waste_emissions + energy_saved_emissions - eco_project_emissions

            # Return the results as JSON
            return JsonResponse({
                'travel_emissions': travel_emissions,
                'waste_emissions': waste_emissions,
                'energy_saved_emissions': energy_saved_emissions,
                'eco_project_emissions': eco_project_emissions,
                'total_emissions': total_emissions
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    # If GET request, just show the form
   
    return render(request, 'calculation_form.html')  # Render the form if GET request


def terminal(request):
    data = {}
    for category in ['travel', 'energy', 'food', 'waste']:
        total = EmissionLog.objects.filter(category=category).aggregate(Sum('saved'))['saved__sum'] or 0
        data[category] = round(total, 2)

    context = {
        'data': data,
        'total_emissions': sum(data.values()),
        'emission_list': list(data.values())
    }

    return render(request, 'terminal.html', context)
CARBON_FACTORS = {
    'car': 0.192,  # kg/km
    'bus': 0.105,
    'train': 0.041,
    'electric_car': 0.060,
    'walk': 0,
    'bicycle': 0
}

def log_action(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        amount = float(request.POST.get('amount'))
        emitted = 0
        saved = 0

        if category == 'travel':
            used = request.POST.get('used')        # transport used
            baseline = request.POST.get('baseline')  # what they would’ve used

            used_emission = CARBON_FACTORS.get(used, 0) * amount
            base_emission = CARBON_FACTORS.get(baseline, 0) * amount
            emitted = used_emission
            saved = base_emission - used_emission

        # Add similar logic for 'energy', 'food', 'waste' if needed

        EmissionLog.objects.create(
            category=category,
            amount=amount,
            emitted=emitted,
            saved=saved
        )

    return redirect('terminal')

def blog(request):
    news_url = 'https://newsapi.org/v2/everything'
    weather_url = 'https://api.openweathermap.org/data/2.5/weather'

    # 🔐 Use your real keys
    news_params = {
        'q': 'climate change environment',
        'language': 'en',
        'apiKey': '0ff7d43500a74d898c1c78e3ffe25f69'
    }

    weather_params = {
        'q': 'Lahore',
        'appid': '3c50a02efc74a53ded676fffd96e8e6a',
        'units': 'metric'
    }

    news_data = requests.get(news_url, params=news_params).json()
    weather_data = requests.get(weather_url, params=weather_params).json()

    articles = news_data.get('articles', [])[:5]
    temperature = weather_data.get('main', {}).get('temp')
    humidity = weather_data.get('main', {}).get('humidity')
    aqi = 50 + (hash(request.user.username) % 100)  # Simulated AQI

    return render(request, 'blog.html', {
        'articles': articles,
        'temp': temperature,
        'humidity': humidity,
        'aqi': aqi
    })

def eco_page(request):
    return render(request, 'eco.html')

def csr_page(request):
    return render(request, 'csr_page.html')