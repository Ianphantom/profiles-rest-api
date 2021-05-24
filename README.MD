# Tugas Proyek 2 Pemograman Integratif
Proyek ini dibuat dengan menggunakan Django, Django REST Framework, Python, Vagrant, VirtualBox. Proyek ini membuat sebuah REST API yang dapat menghandle : 
- Creating and updating user profiles.
- Login and authentication.
- Posting status updates.
- Viewing status update feeds.
# Cara Deployment pada server
- Pada server kamu, jalankan
```curl
curl -sL https://raw.githubusercontent.com/Ianphantom/profiles-rest-api/main/deploy/setup.sh | sudo bash -
```
- Pastikan kamu menambahkan ALLOWED_HOST pada profiles_project/settings.py  
berikut adalah contohnya
```python
ALLOWED_HOSTS = [
    'ec2-18-220-49-43.us-east-2.compute.amazonaws.com',
    '127.0.0.1'
]
```
- untuk melakukan update pada kode yang baru saja ditambahkan  
`cd /usr/local/apps/profiles-rest-api/`  
`sudo sh ./deploy/update.sh`

- setelah server berjalan, selanjutnya membuat sebuah superuser
```
sudo /env/bin/python manage.py createsuperuser
```
# Cara penggunaan API

## Endpoint List
Catatan : Hasil response dari server bisa beragam, tetapi mengikuti struktur seperti yang ada pada contoh
### `POST` /api/profile -> untuk membuat akun baru  

Body Request :
```json
{
    "email": "youemailadress@email.com",
    "name": "yourName",
    "password": "yourPassword"
}
```
- jika berhasil maka server akan merespon dengan :  
`Status Code` : `201`  
Response Body :
```json
{
    "id": 6,
    "email": "yourEmail@email.com",
    "name": "yourName"
}
```
- Jika email sudah digunakan maka server akan merespon dengan :  
`Status Code` : `400`  
Response Body :
```json
{
    "email": [
        "user profile with this email already exists."
    ]
}
```
- Jika user memasukkan email yang tidak valid maka server akan merespon dengan :  
`Status Code` : `400`  
Response Body :
```json
{
    "email": [
        "Enter a valid email address."
    ]
}
```
### `GET` /api/profile -> untuk melihat semua daftar profiles
- server akan mengembalikan respons jika berhasil :  
`Status Code` : `200`
Response Body :
```json
[
    {
        "id": 1,
        "email": "yourEmail@email.com",
        "name": "yourName"
    }
]
```

### `GET` /api/profile/{userID} -> untuk melihat profile user berdasarkan ID
- server akan mengembalikan respons jika berhasil :  
`Status Code` : `200`  
Response Body : 
```json
{
    "id": 1,
    "email": "yourEmail@email.com",
    "name": "yourName"
}
```
- jika tidak ada id, maka server akan merespons dengan :  
`Status Code` : `404`  
Response Body :
```json
{
    "detail": "Not found."
}
```

### `PUT` atau `PATCH` /api/profile/{userID} -> untuk mengupdate profile
Untuk melakukan update, dibutuhkan token terlebih dahulu. Untuk mendapatkan token, user boleh login terlebih dahulu. Token akan digunakan pada header. Setiap user hanya bisa mengupdate profile masing masing.  
Header Request :  Token `yourTokenHere`  
Body Request :  
```json
{
    "id": 1,
    "email": "ian22@gmail.com",
    "name": "yourName12312312213",
    "password": "123"
}
```
- jika berhasil, maka server akan merespon dengan :
`Status Code` : `200`   
Response Body :  
```json
{
    "id": 1,
    "email": "ian22@gmail.com",
    "name": "yourName12312312213"
}
```
- Jika user hendak mengubah data selain milik diri sendiri maka server akan merespon dengan :
```json
{
    "detail": "Invalid token."
}
```
- Jika user belum login, dan hendak mengubah data profile maka server akan merespon dengan :  
`Status Code` : `401`  
```json
{
    "detail": "Authentication credentials were not provided."
}
```
- Jika user tidak memasukkan data secara lengkap saat menggunakan PUT maka server akan merespon dengan :  
`Status Code` : `400`
```json
{
    "password": [
        "This field is required."
    ]
}
```

### `DELETE` /api/profile/{userID} -> untuk menghapus profile
Untuk melakukan penghapusan profile, setiap user harus menggunakan kode token yang bisa didapat setelah login terlebih dahulu. Setiap user hanya mempunyai hak unutk menghapus profile sendiri-sendiri  
Header Request :  Token `yourTokenHere` 
- Jika berhasil, maka server akan merespon dengan :  
`Status Code` : `200`
- Jika kode token tidak sesuai, maka server akan merespon dengan :  
```json
{
    "detail": "Invalid token."
}
```
- Jika user belum melakukan login dan mencoba melakukan delete, maka server akan merespon dengan :  
`Status Code` : `401`  
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### `GET` /api/login/
- Server akan mengembalikan respons
```json
{
    "detail": "Method \"GET\" not allowed."
}
```
### `POST` /api/login/ -> untuk melakukan login
Body Request : 
```json
{
    "username": "youemailadress@email.com",
    "password": "yourPassword"
}
```
- jika kredensial yang dimasukkan user tidak cocok, maka server akan merespon dengan :  
`Status Code` : `400`  
Response Body  
```json
{
    "non_field_errors": [
        "Unable to log in with provided credentials."
    ]
}
```
- jika berhasil maka server akan merespon dengan :
`Status Code` : `200`  
Response Body
```json
{
    "token": "0599557d14d4e22c7f33b92580317cadd5fbe5a8"
}
```
Token tersebut akan digunakan untuk autentikasi.



### `POST` /api/feed/ -> Mengupload feed terbaru
Header Request :  Token `yourTokenHere`  
Body Request :
```json
{
    "status_text": "Masukkan status kamu disini"
}
```
- jika user belum melakukan login atau user tidak menggunakan kode token maka server akan merespon dengan : 
`Status Code` : `401`
```json
{
    "detail": "Authentication credentials were not provided."
}
```
- jika berhasil maka server akan merespon dengan : 
`Status Code` : `201`
Response Body :
```json
{
    "id": 1,
    "user_profile": 8,
    "status_text": "Ini adalah sebuah status baru untuk kamu",
    "created_on": "2021-05-23T22:54:44.390364Z"
}
```

### `GET` /api/feed/ -> melihat daftar feed yang tersedia
Header Request :  Token `yourTokenHere`  
- jika user belum melakukan login atau user tidak menggunakan kode token maka server akan merespon dengan : 
`Status Code` : `401`
```json
{
    "detail": "Authentication credentials were not provided."
}
```

- jika autentikasi berhasil, maka server akan merespon :
`Status Code` : `200`
```json
[
    {
        "id": 1,
        "user_profile": 8,
        "status_text": "Ini adalah sebuah status baru untuk kamu",
        "created_on": "2021-05-13T10:23:17.890194Z"
    }
]
```

### `GET` /api/feed/{feedID} -> melihat feed berdasarkan ID feed
Header Request :  Token `yourTokenHere`  
- server akan membalas dengan :
`Status Code` : `200`
Response Body :
```json
{
    "id": 1,
    "user_profile": 8,
    "status_text": "Ini adalah sebuah status baru untuk kamu",
    "created_on": "2021-05-13T10:23:17.890194Z"
}
```
- jika user belum melakukan login atau user tidak menggunakan kode token maka server akan merespon dengan : 
`Status Code` : `401`  
Response Body
```json
{
    "detail": "Authentication credentials were not provided."
}
```

-jika user berusaha mengkases feed yang tidak tersedia maka server akan membalas dengan :
`Status Code` : `404`  
Response Body 
```json 
{
    "detail": "Not found."
}
```


### `PUT` atau `PATCH` /api/feed/{feedID} -> melakukan update pada feed tertentu
kita hanya bisa melakukan update pada feed yang merupakan feed kepemilikan kita. Kita tidak bisa melakukan update pada feed milik orang lain  
Header Request :  Token `yourTokenHere`
*jika ingin menggunakan PATCH*
Body request : 
```json
{
    "id": 4,
    "user_profile": 8,
    "status_text": "Masukkan status kamu disini lalu sudah di update",
    "created_on": "2021-05-23T22:54:44.390364Z"
}
```
*jika ingin menggunakan PUT*
```json
{
    "status_text": "Masukkan status kamu disini lalu sudah di update",
}
```
- jika user belum melakukan login atau user tidak menggunakan kode token maka server akan merespon dengan : 
`Status Code` : `401`
```json
{
    "detail": "Authentication credentials were not provided."
}
```

- jika user mencoba mengupdate yang bukan miliknya, maka server akan merespon dengan :
`Status Code` : `200`  
Response Body
```json
{
    "detail": "You do not have permission to perform this action."
}
```

- Jika berhasil server akan membalas dengan :
`Status Code` : `200`  
Response Body :
```json
{
    "id": 4,
    "user_profile": 8,
    "status_text": "Masukkan status kamu disini lalu sudah di update",
    "created_on": "2021-05-23T22:54:44.390364Z"
}
```

### `DELETE` /api/feed/{feedID} -> melakukan update pada feed tertentu
Untuk delete, kita juga hanya bisa melakukan penghapusan terhadap feed yang kita miliki, kita tidak bisa melakukan delete terhadap feed orang lain
Header Request :  Token `yourTokenHere`
- jika user belum melakukan login atau user tidak menggunakan kode token maka server akan merespon dengan : 
`Status Code` : `401`
```json
{
    "detail": "Authentication credentials were not provided."
}
```
- jika user mencoba mendelete yang bukan miliknya, maka server akan merespon dengan :
`Status Code` : `200`  
Response Body
```json
{
    "detail": "You do not have permission to perform this action."
}
```
- Jika berhasil maka server akan merespon dengan :
`Status Code` : `200`