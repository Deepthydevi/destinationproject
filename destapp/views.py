from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.permissions import AllowAny
from django.shortcuts import render, get_object_or_404, redirect
from .forms import DestinationForm
from .models import Destination
from rest_framework import generics
from .serializers import DestinationSerializer
import requests

class DestinationCreate(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [AllowAny]

class DestinationDetail(generics.RetrieveAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class DestinationUpdate(generics.RetrieveUpdateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class DestinationDelete(generics.DestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class DestinationSearch(generics.ListAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

    def get_queryset(self):
        name = self.kwargs.get('place_name')
        return Destination.objects.filter(Name__icontains=name)

def add_destination(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data to the database
            form.save()

            # Prepare data for API request
            api_url = 'http://127.0.0.1:8000/create/'
            data = form.cleaned_data
            files = {'image': request.FILES['image']}

            try:
                # Send a POST request to the external API
                response = requests.post(api_url, data=data, files=files)

                if response.status_code == 201:
                    messages.success(request, 'Destination added and data sent successfully.')
                    return redirect('index')
                else:
                    messages.error(request, f'Error: {response.status_code} - {response.text}')
            except requests.RequestException as e:
                messages.error(request, f'Error during API request: {str(e)}')
        else:
            messages.error(request, 'Form is not valid')
    else:
        form = DestinationForm()

    return render(request, 'add_destination.html', {'form': form})

def update_destination(request, id):
    # Retrieve the existing destination instance or return a 404 error if not found
    destination = get_object_or_404(Destination, id=id)

    if request.method == 'POST':
        # Retrieve form data
        place_name = request.POST.get('place_name')
        weather = request.POST.get('weather')
        state = request.POST.get('state')
        district = request.POST.get('district')
        google_map_link = request.POST.get('google_map_link')
        description = request.POST.get('description')

        # Handle file uploads
        image = request.FILES.get('image') if 'image' in request.FILES else destination.image

        # Update the destination instance with new data
        destination.place_name = place_name
        destination.weather = weather
        destination.state = state
        destination.district = district
        destination.google_map_link = google_map_link
        destination.description = description
        destination.image = image

        try:
            # Save the updated destination to the database
            destination.save()

            # Prepare data for API request
            api_url = f'http://127.0.0.1:8000/update/{id}/'
            data = {
                'place_name': place_name,
                'weather': weather,
                'state': state,
                'district': district,
                'google_map_link': google_map_link,
                'description': description
            }
            files = {'image': image} if image else {}

            # Send a PUT request to the external API
            response = requests.put(api_url, data=data, files=files)

            if response.status_code == 200:
                messages.success(request, 'Destination updated and data sent successfully.')
                return redirect('/')
            else:
                messages.error(request, f'Error: {response.status_code} - {response.text}')
        except requests.RequestException as e:
            messages.error(request, f'Error during API request: {str(e)}')
    else:
        # For GET requests, render the form with the existing destination data
        pass

    return render(request, 'update_destination.html', {'destination': destination})


def destination_fetch(request, id):
    api_url = f'http://127.0.0.1:8000/detail/{id}/'
    try:
        response = requests.get(api_url)
        print(f"Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        if response.status_code == 200:
            destination_data = response.json()
            print(f"Destination Data: {destination_data}")
            return render(request, 'destination_fetch.html', {'destination': destination_data})
        else:
            return render(request, 'destination_fetch.html',
                          {'error_message': f'Error: {response.status_code} - {response.text}'})

    except requests.RequestException as e:
        return render(request, 'destination_fetch.html', {'error_message': f'Error during API request: {str(e)}'})

def destination_delete(request, id):
    api_url = f'http://127.0.0.1:8000/delete/{id}/'
    response = requests.delete(api_url)
    if response.status_code == 204:  # No Content
        print(f'Item with ID {id} has been deleted')
    else:
        print(f'Failed to delete item. Status code: {response.status_code}')
    return redirect('/')


def index(request):
    # Fetch all TouristDestination objects from the database
    destinations_list = Destination.objects.all()

    # Pagination setup
    paginator = Paginator(destinations_list, 6)  # Show 10 destinations per page
    page = request.GET.get('page')  # Get the page number from the query parameters

    try:
        destinations = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        destinations = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        destinations = paginator.page(paginator.num_pages)

    # Fetch data from the API
    api_url = 'http://127.0.0.1:8000/details/{id}/'  # Replace with the correct API URL
    api_data = []
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            api_data = response.json()  # Assuming the API returns a JSON array
        else:
            print(f'Error fetching data from API: {response.status_code}')
    except requests.RequestException as e:
        print(f'Error during API request: {str(e)}')

    # Pass both the database and API data to the template
    context = {
        'destinations': destinations,
        'api_destinations': api_data,
    }
    return render(request, 'index.html', context)
