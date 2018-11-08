from django.shortcuts import render
import json
# Create your views here.
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import Show, Movie, Booking, Seat, Theatre

def index(request):
    movies = set()
    theatres = set()
    for show in Show.objects.all():
        movies.add(show.movie)
    for theatre in Theatre.objects.all():
        theatres.add(theatre)
    return render(request, 'index.html', {"user": request.user, "movies": movies, "theatres": theatres})

def theatre(request, theatre_id):
    theatre = Theatre.objects.get(id=theatre_id)
    shows = Show.objects.filter(theatre=theatre)
    data = []
    for show in shows:
        flag = False
        for block in data:
            if block['movie'] == show.movie.name:
                date_flag = False
                for per_day in block['per_day']:
                    if per_day['date'] == show.get_date():
                        screen_flag = False
                        for screen in per_day['screens']:
                            if screen['screen_name'] == show.screen.name:
                                screen['shows'].append({"show_id": show.id, "time": show.get_time()})
                                screen_flag = True
                        if not screen_flag:
                            per_day['screens'].append({"screen_name": show.screen.name, "shows": [{"show_id": show.id, "time": show.get_time()}]})
                        date_flag = True
                        flag = True
                if not date_flag:
                    block['per_day'].append({
                        "date": show.get_date(), 
                        "day": show.get_day(), 
                        "screens": [
                            {   "screen_name": show.screen.name, 
                                "shows": [
                                {   "show_id": show.id, 
                                    "time": show.get_time()
                                }
                                ]
                            }
                        ]
                    })
                    flag = True
        if not flag:
            data.append({
                "movie": show.movie.name, 
                "movie_image": show.movie.small_image, 
                "per_day": [
                    {   "date": show.get_date(), 
                        "day": show.get_day(), 
                        "screens": [
                            {   "screen_name": show.screen.name, 
                                "shows": [
                                    {
                                        "show_id": show.id, 
                                        "time": show.get_time() 
                                    }
                                ] 
                            }
                        ] 
                    }
                ] 
                })
    dates = []
    for show in shows:
        flag = False
        for date in dates:
            if show.get_date() == date['date']:
                flag = True
        if not flag:
            dates.append({"date": show.get_date(), "day": show.get_day()})
    dates = sorted(dates, key=lambda k: k['date']) 
    with open("data.json", "w") as file:
        json.dump(data, file)
    return render(request, 'theatre.html', {'user': request.user, 'theatre': theatre, 'data': data, 'dates': dates, 'first_date': dates[0]['date']})

def movie(request, movie_name):
    movie = Movie.objects.get(name=movie_name)
    shows = Show.objects.filter(movie=movie)
    data = []
    for show in shows:
        date_flag = False
        for block in data:
            if show.get_date() == block['date']:
                date_flag = True

                time_flag = False
                for screen in block['screens']:
                    if show.screen.name == screen['name']:
                        screen['shows'].append({"show_id": show.id, "time": show.get_time()})
                        time_flag = True
                if not time_flag:
                    block['screens'].append({"name": show.screen.name, "theatre": show.screen.theatre.name, "shows": [{"show_id": show.id, "time": show.get_time()}]})

        if not date_flag:
            data.append({"date": show.get_date(), "day": show.get_day(), "screens": [{"name": show.screen.name, "theatre": show.screen.theatre.name, "shows": [{"show_id": show.id, "time": show.get_time()}]}] })

    with open('data.json', 'w') as file:
        json.dump(data, file)

    return render(request, 'movie.html', {'user': request.user, 'movie': movie, 'data': data})

def show(request):
    if request.user.is_authenticated:
        show_id = request.GET['show_id']
        show = Show.objects.get(id=show_id)
        screen = show.screen
        seats = []

        for seat in screen.seats.all():
            flag = True
            for block in seats:
                if block['row'] == seat.row_id:
                    block['column'].append({"cell": seat.row_id+seat.column_id, "status": False})
                    flag = False
            if flag:
                seats.append({"row": seat.row_id, "column": [{"cell": seat.row_id+seat.column_id, "status": False}]})

        bookings = Booking.objects.filter(show=show)
        booked_seats = set()
        for booking in bookings:
            for seat in booking.seats.all():
                booked_seats.add(seat.row_id+seat.column_id)
        booked_seats = sorted(booked_seats)

        for booked_seat in booked_seats:
            for block in seats:
                for cell in block['column']:
                    if booked_seat == cell['cell']:
                        cell['status'] = True

        with open('data.json', 'w') as file:
            json.dump(seats, file) 

        return render(request, 'show.html', {'user': request.user, 'screen': screen, 'movie': show.movie, 'seats': seats, 'show_id': show_id, 'tickets': request.GET['tickets']})
    
    return redirect('/')

def book(request):
    if request.method == 'POST' and request.user.is_authenticated:
        seats = request.POST['seats'].split(',')
        print(seats)
        show = Show.objects.get(id=request.POST['show_id'])
        user = request.user
        booked_seats = set()
        for booking in Booking.objects.filter(show=request.POST['show_id']):
            for seat in booking.seats.all():
                booked_seats.add(seat.row_id+seat.column_id)
        booked_seats = sorted(booked_seats)
        for seat in seats:
            if seat == booked_seats:
                return HttpResponse("Error")
        booking = Booking()
        booking.show = show
        booking.user = user
        booking.save()
        for seat in seats:
            s = Seat.objects.get(row_id=seat[0], column_id=seat[1:])
            booking.seats.add(s)
        booking.save()
        return redirect('/booking_info/')
    return redirect('/')

def booking_info(request):
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user)
        data = []
        for booking in reversed(bookings):
            seats = ''
            for seat in booking.seats.all():
                seats += str(seat) + ', '
            seats = seats[:-2]
            data.append({'booking': booking, 'seats': seats, 'date': booking.show.get_day_date(), 'time': booking.show.get_time(), 'tickets': len(booking.seats.all())})
        return render(request, 'booking.html', {'user': request.user, 'data': data})
   
    return redirect('/')