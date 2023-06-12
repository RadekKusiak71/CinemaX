# CinemaX

CinemaX to aplikacja napisana w Django do zarządzania kinem.

## Wykorzystane technologie:

- Django
- Python
- HTML
- CSS
- Bootstrap
- Requests

## Instalacja:

1. Pobierz repozytorium.
2. Utwórz wirtualne środowisko wewnątrz projektu.
3. Zainstaluj wymagane pakiety z pliku requirements.txt. W folderze z aktywowanym wirtualnym środowiskiem wykonaj polecenie:
   ```
   pip install -r requirements.txt
   ```
4. Uruchom serwer. W folderze z serwerem i aktywowanym wirtualnym środowiskiem wykonaj polecenie:
   ```
   py manage.py runserver
   ```
5. W przeglądarce otwórz stronę localhost:8000.

## Użyte API:

- [The Movie Database](https://www.themoviedb.org/)

## Autorzy:

- Radosław Kusiak
- Szymon Drzycimski

## Template i podpięte do nich widoki:

- base.html - bazowy szablon HTML, który jest rozszerzany w innych szablonach.
- home.html - widok klasy HomePage.
- register.html - widok klasy RegisterRequest.
- login.html - widok klasy LoginRequest.
- movies_list_api.html - widok klasy MovieListAPI.
- movie_creator.html - widok klasy MovieCreator.
- movies_created.html - widok klasy MoviesCreated.
- movie_seat_reservation.html - widok klasy MovieRoom.
- reservation_details.html - widok klasy ReservationDetailsPage.
- reservation_page.html - widok klasy ReservationPage.

## Opisy klas w pliku `views.py`:

### 1. Klasa `FormValidation` (klasa abstrakcyjna)

Klasa abstrakcyjna `FormValidation` definiuje interfejs do walidacji formularzy. Zawiera jedną abstrakcyjną metodę `form_validation`, która musi być zaimplementowana w klasach dziedziczących.

### 2. Klasa `APIFetcher`

Klasa `APIFetcher` odpowiada za pobieranie danych z API Tmdb. Przy inicjalizacji otrzymuje adres URL API oraz konkretny endpoint. Metoda `fetch_data` wysyła żądanie HTTP do API i zwraca odpowiedź w formacie JSON. Metoda `__str__` zwraca informacje o adresie URL API i endpointu.

### 3. Klasa `HomePage` (dziedziczy po `View`)

Klasa `HomePage` obsługuje wyświetlanie strony głównej. Metoda `get` pobiera wszystkie filmy z bazy danych i przekazuje je do szablonu `home.html` jako kontekst.

Url:
```
path('', views.HomePage.as_view(), name='home_page'),
```

### 4. Klasa `RegisterRequest` (dziedziczy po `FormValidation` i `View`)

Klasa `RegisterRequest` obsługuje rejestrację użytkownika. Metoda `get` renderuje formularz rejestracji, a metoda `

post` obsługuje przesłanie formularza. Metoda `form_validation` sprawdza poprawność danych formularza, tworzy nowego użytkownika i profil użytkownika, a następnie przekierowuje na stronę logowania lub wyświetla odpowiedni komunikat w przypadku niepowodzenia.

Url:
```
path('register/', views.RegisterRequest.as_view(), name='register_page'),
```

### 5. Klasa `LoginRequest` (dziedziczy po `FormValidation` i `View`)

Klasa `LoginRequest` obsługuje logowanie użytkownika. Metoda `get` renderuje formularz logowania, a metoda `post` obsługuje przesłanie formularza. Metoda `form_validation` sprawdza poprawność danych logowania, uwierzytelnia użytkownika i przekierowuje na stronę główną lub wyświetla odpowiedni komunikat w przypadku niepowodzenia.

Url:
```
path('login/', views.LoginRequest.as_view(), name='login_page'),
```

### 6. Klasa `LogoutRequest` (dziedziczy po `View`)

Klasa `LogoutRequest` obsługuje wylogowanie użytkownika. Metoda `get` wylogowuje użytkownika i przekierowuje na stronę główną.

Url:
```
path('logout/', views.LogoutRequest.as_view(), name='logout_req'),
```

### 7. Klasa `MovieListAPI` (dziedziczy po `View`)

Klasa `MovieListAPI` obsługuje wyświetlanie listy filmów pobranych z API Tmdb. Metoda `get` renderuje stronę API z listą filmów. Metoda `get_movie_list` pobiera dane filmów z API Tmdb i zwraca je jako kontekst do szablonu `movie_list_api.html`.

Url:
```
path('movies_api/', views.MovieListAPI.as_view(), name='movies_api_page'),
```

### 8. Klasa `MovieCreator` (dziedziczy po `FormValidation` i `View`)

Klasa `MovieCreator` obsługuje tworzenie filmów przez administratora. Metoda `get` renderuje formularz tworzenia filmu, a metoda `post` obsługuje przesłanie formularza. Metoda `form_validation` sprawdza poprawność danych formularza, tworzy nowy film i przekierowuje na stronę szczegółów filmu lub wyświetla odpowiedni komunikat w przypadku niepowodzenia.

Url:
```
path('movies_api/creator/<str:pk>', views.MovieCreator.as_view(), name='movie_creator_page'),
```

### 9. Klasa `MoviesCreated` (dziedziczy po `View`)

Klasa `MoviesCreated` obsługuje wyświetlanie listy filmów utworzonych przez admina. Metoda `get` renderuje stronę z utworzonymi filmami pobranymi z bazy danych oraz obsługuje metody GET `get_next_day`, `get_previous_day`, `get_date`, które pozwalają na przechodzenie na poszczególne dni. Klasa obsługuje również metodę `post`, która jest dostępna tylko

 dla adminów i pozwala na usunięcie filmu.

Url:
```
path('movies/', views.MoviesCreated.as_view(), name='movies_page'),
```

### 10. Klasa `MovieRoom` (dziedziczy po `View`)

Klasa `MovieRoom` obsługuje rezerwację miejsc na seansie filmowym. Metoda `get` renderuje stronę rezerwacji miejsc na podstawie identyfikatora filmu. Metoda `get_room` generuje tablicę 6x6 miejsc siedzących w sali kinowej. Metoda `get_taken_seats` pobiera z bazy danych informacje o zajętych miejscach dla danego filmu.

Url:
```
path('movies/<int:movie_id>/', views.MovieRoom.as_view(), name='movie_room_page'),
```

### 11. Klasa `ReservationPage` (dziedziczy po `FormValidation` i `View`)

Klasa `ReservationPage` obsługuje wprowadzanie danych do rezerwacji. Metoda `get` renderuje formularz rezerwacji miejsc na podstawie numeru miejsca, numeru rzędu i identyfikatora filmu. Metoda `post` obsługuje przesłanie formularza rezerwacji, sprawdza poprawność danych, tworzy nową rezerwację i przekierowuje na stronę potwierdzenia lub wyświetla odpowiedni komunikat w przypadku niepowodzenia.

Url:
```
path('movies/<int:movie_id>/<int:seat_num>/<int:row_num>', views.ReservationPage.as_view(), name='reservation_page'),
```

### 12. Klasa `ReservationDetailsPage` (dziedziczy po `View`)

Klasa `ReservationDetailsPage` obsługuje wyświetlanie szczegółów rezerwacji przez użytkownika. Metoda `get` pobiera dane o biletach na podstawie identyfikatora biletu i przekazuje je do szablonu `reservation_details.html` jako kontekst. Metoda `post` obsługuje potwierdzenie lub anulowanie rezerwacji przez użytkownika.

Url:
```
path('reservation/details/<int:ticket_id>/', views.ReservationDetailsPage.as_view(), name='reservation_details_page'),
```
