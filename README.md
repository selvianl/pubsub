## Dockerizing

`docker build -t <tagname> .` <br>
`docker compose up`<br>

## Proje Detay

Başlangıç değerleri 1 adet RestaurantCategory, 1 adet Restaurant ve 1 adet Food olarak fixtures klasörü içindedir ve dockerize aşamasında db ye kayıt atar. <br>
Yeni data eklenmek istenirse modeller admin paneline register haldedir oradan oluşturulabilir.<br>

Postman collection ` pubsub.postman_collection.json ` içinde mevcuttur. <br>

Testler `python manage.py test --keepdb api.tests` şeklinde çalıştırabilir. <br>

Enviroment değerleri `.env` ve `.env.db` dosyalarında tanımlanmıştır.
