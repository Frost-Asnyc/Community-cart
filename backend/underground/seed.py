from datetime import datetime, timezone
from decimal import Decimal

from bson.decimal128 import Decimal128

from app import create_app
from extensions import db
from models import User
from underground.database import MARKETPLACE_ID, get_underground_products
from underground.schemas import underground_product_schema

DEMO_PRODUCTS = (
    {
        "seed_key": "alt-fashion-satin-twist-mini-dress",
        "name": "Forever 21 Satin Twist-Front Strapless Mini Dress",
        "description": "Adult women's mini dress. Approximate reference price in KES; retailer stock and checkout are not connected.",
        "price": "1300",
        "category": "Alternative Fashion",
        "subcategory": "Mini Dresses",
        "image": "https://www.forever21.com/cdn/shop/files/01371120-01-2_front.png?v=1771970833&width=1024",
        "availability": True,
    },
    {
        "seed_key": "alt-fashion-pink-strapless-mini-dress",
        "name": "Forever 21 Pink Strapless Mini Dress",
        "description": "Adult women's short strapless dress. Catalog reference price is approximate; retailer stock and checkout are not connected.",
        "price": "4680",
        "category": "Alternative Fashion",
        "subcategory": "Mini Dresses",
        "image": "https://www.forever21.com/cdn/shop/files/01409726-04-1_styledfront_1.jpg?v=1784668401&width=1000",
        "availability": True,
    },
    {
        "seed_key": "alt-fashion-gia-red-satin-mini-dress",
        "name": "Gia Red Satin Strapless Mini Dress",
        "description": "Adult women's satin mini dress. Approximate reference price in KES; retailer stock and checkout are not connected.",
        "price": "10270",
        "category": "Alternative Fashion",
        "subcategory": "Mini Dresses",
        "image": "https://bohopink.com/cdn/shop/files/gia-red-satin-strapless-mini-dress.jpg?v=1762465234&width=960",
        "availability": True,
    },
    {
        "seed_key": "alt-fashion-vs-bandeau-bra",
        "name": "Victoria's Secret Push-Up Wireless Bandeau Strapless Bra",
        "description": "Plain product-only photo, no model. Approximate reference price in KES; store stock and checkout are not connected.",
        "price": "7794",
        "category": "Alternative Fashion",
        "subcategory": "Underwear",
        "image": "https://www.victoriassecret.com/p/760x1013/png/zz/26/04/16/01/1126525065H8_OF_F.jpg",
        "availability": True,
    },
    {
        "seed_key": "alt-fashion-vs-cotton-thong",
        "name": "Victoria's Secret Logo Cotton Thong Panty",
        "description": "Plain product-only photo, no model. Approximate reference price in KES; store stock and checkout are not connected.",
        "price": "1625",
        "category": "Alternative Fashion",
        "subcategory": "Underwear",
        "image": "https://www.victoriassecret.com.au/dw/image/v2/BLPL_PRD/on/demandware.static/-/Sites-vs-master-catalog/default/dwa6294376/large/1124446274FO_OF_F.jpg?sh=1500&sm=fit&sw=1500",
        "availability": True,
    },
    {
        "seed_key": "alt-fashion-vs-seamless-panties",
        "name": "Victoria's Secret Seamless Panties",
        "description": "Product-only assortment photo, no models. Approximate reference price in KES; store stock and checkout are not connected.",
        "price": "1625",
        "category": "Alternative Fashion",
        "subcategory": "Underwear",
        "image": "https://www.victoriassecret.com/images/vsweb/fe7d8110-0df1-4142-8d66-51145416d8e4/071526-fc-panty-party.jpg",
        "availability": True,
    },
    {
        "seed_key": "alt-fashion-kilimall-black-two-piece-bikini",
        "name": "Women’s Black Halter Two-Piece Bikini Set",
        "description": "Two-piece swimsuit from a Kilimall Kenya listing. Listed price shown in KES; seller stock and checkout are not connected to this demo API.",
        "price": "600",
        "category": "Alternative Fashion",
        "subcategory": "Two-Piece Swimwear",
        "image": "https://img.kilimall.com/c/obs/seller/9892/goods_image/240723143404_6e6126373b1da71c8aa988f1eddd9554.jpg",
        "availability": True,
    },
    {
        "seed_key": "alt-fashion-shein-black-two-piece-bikini",
        "name": "Halter Neck Side-Tie Two-Piece Bikini",
        "description": "Two-piece swimwear listing. Approximate reference price in KES; retailer stock and checkout are not connected.",
        "price": "980",
        "category": "Alternative Fashion",
        "subcategory": "Two-Piece Swimwear",
        "image": "https://img.ltwebstatic.com/images3_pi/2023/10/30/ce/1698630142b422cdc40ee48083825da975a258e684_thumbnail_600x.jpg",
        "availability": True,
    },
    {
        "seed_key": "alt-fashion-forever21-hello-kitty-cellphone-bag",
        "name": "Forever 21 Hello Kitty Cellphone Bag",
        "description": "Crochet crossbody phone purse. Approximate reference price in KES; retailer stock and checkout are not connected.",
        "price": "1037",
        "category": "Alternative Fashion",
        "subcategory": "Purses",
        "image": "https://www.forever21.com/cdn/shop/files/Large-01287578-01-1_front.jpg?v=1751586585&width=1000",
        "availability": True,
    },
    {
        "seed_key": "alt-fashion-forever21-hello-kitty-water-bottle-sling",
        "name": "Forever 21 Hello Kitty Water Bottle Sling Bag",
        "description": "Small crossbody sling bag. Approximate reference price in KES; retailer stock and checkout are not connected.",
        "price": "647",
        "category": "Alternative Fashion",
        "subcategory": "Purses",
        "image": "https://www.forever21.com/cdn/shop/files/Large-01275241-01-1_front.jpg?crop=center&height=1200&v=1751585518&width=1200",
        "availability": True,
    },
    {
        "seed_key": "energy-monster-original-green",
        "name": "Monster Energy Original Green",
        "description": "Monster Energy Original Green (OG). Approximate KES reference price; retail stock is not connected.",
        "price": "389",
        "category": "Energy Drinks",
        "subcategory": "Monster Energy",
        "image": "https://web-assests.monsterenergy.com/mnst/be642d6a-2c3c-4978-a985-56ef9df7eae1.png",
        "availability": True,
    },
    {
        "seed_key": "energy-ghost-og",
        "name": "GHOST Energy OG",
        "description": "GHOST Energy OG. Approximate KES reference price; retail stock is not connected.",
        "price": "389",
        "category": "Energy Drinks",
        "subcategory": "GHOST Energy",
        "image": "https://drinkghost.com/cdn/shop/files/OGRight_9721ee23-546f-4786-ad3e-93003161de6a_200x.webp?v=1756221881",
        "availability": True,
    },
    {
        "seed_key": "nightlife-dubai-table-request-sample",
        "name": "Dubai, 8 PM — Table Request for 5",
        "description": "KES 15,000 per person estimate. Example request only; no venue reservation or live availability is attached. Confirm the price and booking directly with a venue.",
        "price": "15000",
        "category": "Nightlife & Entertainment",
        "subcategory": "Booking Example",
        "image": "https://www.timeoutdubai.com/cloud/timeoutdubai/2023/02/15/STAY-by-Yannick-Alleno-Dining-Room-1024x768.jpg",
        "availability": True,
    },
    {
        "seed_key": "motorsports-dubai-autodrome-info",
        "name": "Dubai Autodrome — Track Location",
        "description": "Venue directory card for Dubai Autodrome in Motor City, Dubai. This is not a ticket or booking; check the official venue for current activities and availability.",
        "price": "8500",
        "category": "Motorsports",
        "subcategory": "Race Track Locations",
        "image": "https://www.musco.com/wp-content/uploads/2024/04/autodrome_2.jpg",
        "availability": True,
    },
    {
        "seed_key": "motorsports-yas-marina-circuit-info",
        "name": "Yas Marina Circuit — Track Location",
        "description": "Venue directory card for Yas Marina Circuit on Yas Island, Abu Dhabi. This is not a ticket or booking; check the official venue for current activities and availability.",
        "price": "12000",
        "category": "Motorsports",
        "subcategory": "Race Track Locations",
        "image": "https://cdn.getyourguide.com/img/location/560518b280a83.jpeg/99.jpg",
        "availability": True,
    },
)


# These generated catalog entries are illustrative price and location references.
# They are not connected to venue booking, track schedules, or live availability.
_NIGHTLIFE_IMAGES = (
    "https://tcdn.mindtrip.ai/images/677054/1bbvory.png",
    "https://www.bestrooftop.com/storage/public/restaurants/8066-kilele-nyama/profile/gallery/ibis-kilele-nyama-20.jpg",
    "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/29/a0/3a/46/caption.jpg?h=1200&s=1&w=1200",
    "https://back.voyages.carrefour.fr/admin/TS/fckUserFiles/Image/Produits/PREPACKAGE/KENYA/BAOBAB/baobab-restaurant2.jpg",
    "https://www.safarireiser.no/assets/components/phpthumbof/cache/sandsatnomadinside-view-of-the-sands-at-nomad-restaurant.3f898f2356692f7aeb955dc58a7cd320.jpg",
    "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/1a/7a/99/8f/dining-with-a-view-of.jpg?h=1800&s=1&w=2400",
    "https://www.kayak.com/rimg/himg/f4/0d/19/ice-2583405-9f5348-639536.jpg?crop=true&height=607&width=836",
    "https://media.staticontent.com/media/pictures/4ee1a900-82c6-489e-bce3-01fdfb53c5a1",
    "https://nexara-dubai.com/blog-images/dubai-luxury-restaurant-panoramic-city-view.webp",
    "https://b.zmtcdn.com/data/pictures/0/202310/6cd2b4305ac5e2f533b10ed6a38b1d14.jpg",
    "https://www.banyantree.com/assets/2024-12/MR_BT-Website-1920x1080-13.jpg",
    "https://cdn.prod.website-files.com/66db00fc66a77b1567526e7f/6711ae5055e2f69834ac061d_stay-dubai-restaurant2.webp",
    "https://merchandiseuganda.com/girogup/2019/06/protea-hotel-kampala-merchandise-uganda18.jpg",
    "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/0b/55/a9/ed/humidor-terrace.jpg?h=-1&s=1&w=700",
    "https://cdn.prod.website-files.com/58dcf22aee8a7c646f3023f0/598da41090707d00013b0a50_kisiwa5-small.jpg",
    "https://www.cenizaro.com/theresidence/zanzibar/dining-masthead.jpg",
    "https://static.wixstatic.com/media/196173_ab2f0f4eb0144bc497cb742e0f68fe8e~mv2.jpg/v1/fill/w_1920%2Ch_1536%2Cal_c%2Cq_90%2Cusm_0.66_1.00_0.01%2Cenc_avif%2Cquality_auto/196173_ab2f0f4eb0144bc497cb742e0f68fe8e~mv2.jpg",
    "https://www.neptunehotels.com/wp-content/uploads/2022/08/Beach-terrace-Restaurant-1200x900.jpg.webp",
    "https://www.skr.de/fileadmin/_processed_/6/5/restaurant_e3546f4ba4.jpg",
    "https://dcontent.inviacdn.net/shared/img/web-1200x1024/2020/2/7/d64/24027549-jacaranda-indian-ocean-beach-resort.jpg",
    "https://pbs.twimg.com/media/D1ECCb2XQAAPGwB.jpg",
    "https://www.ticati.com/img/hotel/2591473s.jpg",
    "https://cdn2.cenizaro.com/images/zanzibar/dining-masthead.jpg?width=1200",
    "https://images.trvl-media.com/lodging/10000000/9250000/9242200/9242138/w5991h3990x0y4-809b92df.jpg?impolicy=resizecrop&ra=fit&rw=598",
    "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/27/aa/25/b4/agness-zanzibar.jpg?h=-1&s=1&w=1200",
    "https://pub-5bcc3edf34304d04b59dc91e1ad9d2fd.r2.dev/tortoisepath.com/uploads/2024/01/03161015/Club-Smooth-Accra-Ghana-TortoisePathcom-4-jpeg.webp",
    "https://cdn.mahlatini.com/The-Nines-Restaurant-Cape-Town.jpg",
    "https://www.utopiacapetown.co.za/wp-content/uploads/2019/04/Utopia_Restautant_15-683x1024.jpg",
    "https://mariamshittu.com/wp-content/uploads/2023/04/5996f-img_5966.jpg?h=1024&w=768",
    "https://sabiabuja.com/wp-content/uploads/2024/05/Gras-Lagos.png",
)
_MOTORSPORT_IMAGES = (
    "https://www.musco.com/wp-content/uploads/2024/04/autodrome_2.jpg",
    "https://cdn.getyourguide.com/img/location/560518b280a83.jpeg/99.jpg",
    "https://media.oneturf.news/media/attachments/1747209093207_bahrain-grand-prix-at-night.jpeg",
    "https://webcms.listmag.com/listmag/uploads/images/2024/10/11/2162836.jpg",
    "https://cdn.sanity.io/images/fnx611yr/productionv2/c17c3584e2c06d9f625aef5a80abc85efe98e4f2-4858x2733.jpg?auto=format&w=1200",
    "https://www.webbaviation.co.uk/aerial/_data/i/galleries/Northamptonshire/Silverstone_Circuit/silverstone-eb16957-la.jpg",
    "https://images.motorsport-magazin.com/images/960/540/q_80/0549475.jpg",
    "https://assets.simpleviewinc.com/simpleview/image/fetch/c_fill%2Ch_650%2Cq_75%2Cw_972/https%3A/assets.simpleviewinc.com/simpleview/image/upload/v1/clients/austin/Picture1_099cff6b-b10a-495e-a5ae-564bddd6c0dc.png",
    "https://www.f1-world.ru/tracks/shanghai_bird_2018.jpg",
    "https://cdn.guerinsportivo.it/images/2024/07/19/084017775-fb678899-494f-445d-a8fb-62ad22f729e5.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/6/6f/Autodromo_Nazionale_Monza%2C_April_22%2C_2018_SkySat_%28cropped%29.jpg",
)

_BOOKING_REQUESTS = (
    ("Nairobi", "7 PM", 2, 4500), ("Nairobi", "8 PM", 4, 7000),
    ("Nairobi", "9 PM", 5, 9500), ("Mombasa", "7 PM", 2, 5000),
    ("Mombasa", "8 PM", 4, 8500), ("Diani", "8 PM", 3, 9000),
    ("Kisumu", "7 PM", 4, 6000), ("Nakuru", "8 PM", 5, 7500),
    ("Dubai", "7 PM", 2, 11000), ("Dubai", "9 PM", 4, 18000),
    ("Abu Dhabi", "8 PM", 3, 14000), ("Doha", "9 PM", 5, 16000),
    ("Kampala", "7 PM", 2, 5500), ("Kampala", "9 PM", 6, 12000),
    ("Dar es Salaam", "8 PM", 4, 8500), ("Zanzibar", "7 PM", 2, 10000),
    ("Kigali", "8 PM", 4, 9000), ("Lagos", "9 PM", 5, 17000),
    ("Accra", "8 PM", 3, 12500), ("Cape Town", "7 PM", 4, 15000),
    ("Johannesburg", "9 PM", 6, 18000), ("Mombasa", "9 PM", 5, 11000),
    ("Nairobi", "10 PM", 6, 13000), ("Dubai", "10 PM", 8, 26000),
    ("Abu Dhabi", "9 PM", 5, 21000), ("Doha", "8 PM", 2, 12000),
    ("Kigali", "9 PM", 2, 7000), ("Accra", "10 PM", 6, 22000),
    ("Cape Town", "9 PM", 5, 20000), ("Zanzibar", "8 PM", 4, 19000),
)

_RACE_TRACKS = (
    ("Bahrain International Circuit", "Sakhir, Bahrain", 9500),
    ("Jeddah Corniche Circuit", "Jeddah, Saudi Arabia", 11000),
    ("Lusail International Circuit", "Lusail, Qatar", 10000),
    ("Autódromo José Carlos Pace", "São Paulo, Brazil", 8000),
    ("Circuit of The Americas", "Austin, Texas, USA", 13500),
    ("Shanghai International Circuit", "Shanghai, China", 9000),
    ("Hungaroring", "Mogyoród, Hungary", 8500),
    ("Autodromo Nazionale Monza", "Monza, Italy", 12000),
    ("Circuit de Spa-Francorchamps", "Stavelot, Belgium", 12500),
    ("Silverstone Circuit", "Silverstone, United Kingdom", 14000),
    ("Suzuka International Racing Course", "Suzuka, Japan", 11500),
    ("Circuit de Monaco", "Monte Carlo, Monaco", 22000),
    ("Marina Bay Street Circuit", "Singapore", 18500),
    ("Albert Park Grand Prix Circuit", "Melbourne, Australia", 14500),
    ("Circuit Gilles-Villeneuve", "Montréal, Canada", 13000),
    ("Autódromo Hermanos Rodríguez", "Mexico City, Mexico", 10500),
    ("Miami International Autodrome", "Miami, Florida, USA", 16500),
    ("Circuit de Barcelona-Catalunya", "Montmeló, Spain", 11500),
    ("Circuit Zandvoort", "Zandvoort, Netherlands", 12500),
    ("Fuji Speedway", "Oyama, Japan", 9000),
    ("Sepang International Circuit", "Sepang, Malaysia", 7500),
    ("Circuit de la Sarthe", "Le Mans, France", 13500),
    ("Daytona International Speedway", "Daytona Beach, USA", 12000),
    ("Nürburgring", "Nürburg, Germany", 11000),
    ("Kyalami Grand Prix Circuit", "Midrand, South Africa", 8500),
    ("Phillip Island Grand Prix Circuit", "Ventnor, Australia", 9000),
    ("Mugello Circuit", "Scarperia e San Piero, Italy", 10500),
    ("Brands Hatch", "West Kingsdown, United Kingdom", 8000),
    ("Imola Circuit", "Imola, Italy", 10000),
    ("Red Bull Ring", "Spielberg, Austria", 11500),
)

DEMO_PRODUCTS += tuple(
    {
        "seed_key": f"nightlife-table-request-{index:02d}",
        "name": f"{city}, {time} — Table Request for {guests}",
        "description": f"KES {price:,} per person estimate. Example request only; no venue reservation or live availability is attached. Confirm details directly with a venue.",
        "price": str(price),
        "category": "Nightlife & Entertainment",
        "subcategory": "Booking Example",
        "image": _NIGHTLIFE_IMAGES[index - 1],
        "availability": True,
    }
    for index, (city, time, guests, price) in enumerate(_BOOKING_REQUESTS, start=1)
)

DEMO_PRODUCTS += tuple(
    {
        "seed_key": f"motorsports-track-location-{index:02d}",
        "name": f"{circuit} — Track Location",
        "description": f"{location}. Illustrative race-track image and KES {price:,} per-person activity estimate only; this is not a ticket or booking, and the image may not show this exact venue. Confirm current activities and prices with the official circuit.",
        "price": str(price),
        "category": "Motorsports",
        "subcategory": "Race Track Locations",
        "image": _MOTORSPORT_IMAGES[(index - 1) % len(_MOTORSPORT_IMAGES)],
        "availability": True,
    }
    for index, (circuit, location, price) in enumerate(_RACE_TRACKS, start=1)
)




# Brand-specific product packshots and catalog-reference KES prices.
# Product availability remains a preview flag; live retailer inventory is not connected.
_PRODUCT_IMAGES = {
    "energy-red-bull": "https://www.kroger.com/product/images/xlarge/front/0061126999100",
    "energy-celsius": "https://i.honey-images.com/v4/200_3196c141aa5925997d3115dc6872d123.jpg",
    "energy-bang": "https://www.kroger.com/product/images/xlarge/front/0061076486365",
    "energy-rockstar": "https://images-cdn.ubuy.co.id/634fec591f0c133d931087b0-rockstar-original-energy-drink-16-oz-4.jpg",
    "energy-c4": "https://musclefoodsusa.com/wp-content/uploads/2020/03/c4batch.png",
    "energy-alani-nu": "https://webimages.theisens.com/asset/be8d85c4-c53d-4955-9915-ae29f4420398/Base/51326.jpg?width=256",
    "energy-reign": "https://www.instacart.com/image-server/1864x1864/www.instacart.com/assets/domains/product-image/file/large_a76255e9-a35f-4cfa-8f67-3642a98adc5b.png",
    "energy-nos": "https://d2lnr5mha7bycj.cloudfront.net/product-image/file/large_06d03e77-f7e5-4bfe-82d8-8a6127b269d2.PNG",
    "energy-5hour": "https://i5.walmartimages.com/seo/5-hour-ENERGY-Shot-Regular-Strength-Berry-4-Count_b03c48ab-11ee-4276-a2ec-ec04d8f56de3.48ea3b80a653c0152a0b2e1ff4593d09.jpeg",
    "energy-prime": "https://cdn.xxl.se/filespin/fab449343ad94315888ca93db62ea7ec?bgcolor=efefef&quality=75&resize=3840%2C3840",
    "energy-full-throttle": "https://i5.walmartimages.com/asr/a2b81678-0fc9-4835-a6e9-4b49e3a31176.e31a152d55cba629eaffba2cbbbf17b7.jpeg",
    "energy-kickstart": "https://i5.walmartimages.com/seo/Mountain-Dew-Kickstart-Energy-Drink-Orange-Citrus-Flavor-16-fl-oz-Can_d65dbe39-7ddc-4856-987d-79e82207a5c0.280ce4a029f53325e828bfe2e10165f2.jpeg",
    "energy-baya": "https://m.media-amazon.com/images/I/71qwZwmS1BL.jpg",
    "energy-venom": "https://cdn.shopify.com/s/files/1/0588/2701/4293/files/DW105670-24.png?v=1753405417",
    "energy-bloom": "https://i5.walmartimages.com/seo/BLOOM-SPARKLING-ENERGY-CRISP-APPLE-SINGLE-CAN-12OZ_18c960d2-5100-4cd2-baac-d67dd8c18321.968f86b07fd499cbd4a57ea557f3c3f1.png",
    "energy-zevia": "https://d2lnr5mha7bycj.cloudfront.net/product-image/file/large_97f29ac6-2cab-43cd-a124-f8ff15beb56b.jpg",
    "energy-gfuel": "https://www.sweet-joint.com/cdn/shop/files/Gfuel-Energy-Drink-Fazeberry.png?v=1768635527",
    "energy-amp": "https://www.instacart.com/assets/domains/product-image/file/large_43299c0a-8d82-4b01-8db4-6c2bb5786743.png",
    "spirit-titos": "https://supermercadosnacional.com/media/catalog/product/2/1/2156261-1.jpg",
    "spirit-smirnoff": "https://hebmx.vtexassets.com/arquivos/ids/786989-800-800?aspect=true&height=800&v=638591787068170000&width=800",
    "spirit-absolut": "https://m.media-amazon.com/images/I/51eqJ23xGML._AC_SL1500_.jpg",
    "spirit-grey-goose": "https://thebarrel.au/cdn/shop/files/Grey-Goose-Vodka.png?v=1684999001",
    "spirit-ketel-one": "https://cdn.shoplightspeed.com/shops/643460/files/31876603/spirits-ketel-one-vodka-750ml.jpg",
    "spirit-svedka": "https://i5.walmartimages.com/seo/SVEDKA-Vodka-750-ml-Bottle-40-ABV_5da3970e-14f5-4931-9ee9-b09371d7302a.69c26ef32888ace943683c92e077eef1.jpeg",
    "spirit-new-amsterdam": "https://images.gopuff.com/resize/cf/version%3D1_2%2Cformat%3Dauto%2Cfit%3Dscale-down%2Cquality%3D70%2Cwidth%3D1600%2Cheight%3D1600/https%3A/images.gopuff.com/blob/gopuffcatalogstorageprod/catalog-images-container/resize/cf/version%3D1_2%2Cformat%3Dauto%2Cfit%3Dscale-down%2Cwidth%3D800%2Cheight%3D800/0ebaba94-81b3-4edd-a01d-7996a1e6ca86.png",
    "spirit-skyy": "https://elitclub.kz/upload/images/88084_163986_04.jpg",
    "spirit-ciroc": "https://digitalcontent.api.tesco.com/v2/media/ghs/157a8dbb-bdd9-4f76-a849-f7e98ea29411/0872fe2d-a520-423d-a983-8e3c005fe3e2_1091460546.jpeg",
    "spirit-deep-eddy": "https://cdn11.bigcommerce.com/s-t5ovgcn8tc/images/stencil/640w/products/28547/44264/70f439717110d952c69ba999fdb0e4a96209f71f__78207.1.jpg",
    "spirit-jack-daniels": "https://cdn11.bigcommerce.com/s-q90i85/images/stencil/1280x1280/products/100/1222/jd__22999.1682749666.png?c=2",
    "spirit-jim-beam": "https://dojiw2m9tvv09.cloudfront.net/79333/product/dsc088896379.jpg?123=&t=1783192131",
    "spirit-crown-royal": "https://bdliquorwine.com/cdn/shop/products/Crown-Royal-Canadian-Whiskey-Crown-Royal-1610022369_d750a798-fbc0-46cd-9a79-1db6bf4e4452_2000x.jpg?v=1631046394",
    "spirit-fireball": "https://d2lnr5mha7bycj.cloudfront.net/product-image/file/large_6cd036de-4b2e-4497-9f4c-3c9aa4b0239a.jpg",
    "spirit-makers-mark": "https://boozeshop.ph/cdn/shop/files/Maker_sMark750ml.png?v=1744277639",
    "spirit-jameson": "https://cdn.shopify.com/s/files/1/0573/0549/7766/files/jamesonirishwhiskey.webp?v=1722637029",
    "spirit-buffalo-trace": "https://s.yimg.com/ny/api/res/1.2/4faqsK8cuTuqKFr5ncpuqA--/YXBwaWQ9aGlnaGxhbmRlcjt3PTk2MDtoPTk2MA--/https%3A/media.zenfs.com/en/apartment_therapy_269/524c55de253b6297bc9de630ffd336ff",
    "spirit-bulleit": "https://daydram.com/cdn/shop/files/BulleitBourbon.png?v=1740443398",
    "spirit-woodford": "https://www.mensjournal.com/.image/MjA1NDMzMzE1MTc0MzkzODEy/woodford-reserve-kentucky-straight-bourbon-whiskey.png?profile=w2560&x=50&y=50",
    "spirit-evan-williams": "https://cdn.shopify.com/s/files/1/0635/3289/2418/files/buy-evan-williams-bourbon__11459.jpg?v=1687156448",
    "spirit-wild-turkey": "https://sailinliquor.com/cdn/shop/files/246429151.png?v=1763944659",
    "spirit-four-roses": "https://whisky.nl/media/catalog/product/f/o/four-roses-bourbon-whiskey-70cl.jpg?height=1400&image-type=image&store=whisky_nl&width=1400",
    "spirit-knob-creek": "https://www.thebarreltap.com/cdn/shop/files/knob-creek-9-year-bourbon-whiskey-100-proof-the-barrel-tap-www-thebarreltap-com.jpg?v=1691179497",
    "spirit-basil-hayden": "https://target.scene7.com/is/image/Target/GUEST_28ab4260-28a1-4c03-848e-d69ff2b3c363",
    "spirit-johnnie-walker": "https://executiveretailshops.com/cdn/shop/files/Johnnie-Walker-Red-Label.jpg?v=1700158169",
    "spirit-dewars": "https://heavyliquor.com/cdn/shop/files/res_644ccccbb471389b7385f2a149ae859f.jpg?v=1764421405",
    "spirit-glenlivet": "https://api-runner.a-ok.app/static/images/aok2_9-R806zJO6pTvaRGAHEjmHOvyUQ4J5VMnhDmwbrTZEo_-PigMZvdCN6UeESjtF0O4ytbCHA36MnvLcRjdjgukktc75i5nG8sW88FrdA5vWTmtIbgrcbhcbA8qUvPZYoCNCcNmqubU73Of7BVv4U_Yt6ZhzBxuoaPuRh3ZXn7oRCDHqnB54",
    "spirit-patron": "https://www.binnys.com/globalassets/catalogs/binnys/11/1147/114731/114731.jpg?bgcolor=fff&height=690&rmode=BoxPad&width=690",
    "spirit-don-julio": "https://whiskyandwhiskey.com/cdn/shop/files/don-julio-blanco-tequila__001_bf2e4865-3b92-4a82-8bab-36e7c845d781.jpg?v=1762056885&width=1200",
    "spirit-casamigos": "https://whiskyandwhiskey.com/cdn/shop/files/casamigos-blanco-tequila__001_409b8dc7-bbbd-46e9-b088-70ecd431d044.jpg?v=1762056877&width=2048",
    "spirit-jose-cuervo": "https://images.tcdn.com.br/img/img_prod/1383230/tequila_jose_cuervo_especial_ouro_750ml_1875_1_21d7f3906f09d1e08b8f00b5c613421b.jpg",
    "spirit-espolon": "https://www.vinello.de/media/image/5e/23/de/blanco-tequila-espolon-tequilaovYnYGcjvxVk5.png",
    "spirit-1800": "https://secretbottleshop.co.uk/cdn/shop/files/a87d1baa-d795-4aa9-84e6-00b38221a9d9.jpg?v=1741792104",
    "spirit-herradura": "https://tiendaynnaf.com/wp-content/uploads/2022/09/Plata-Herradura.webp",
    "spirit-teremana": "https://i5.walmartimages.cl/asr/a8628c01-d459-401a-ae4c-1ba9e862c3a5.931d856989d85397db96617352c973d0.png?odnBg=ffffff&odnHeight=2000&odnWidth=2000",
    "spirit-bacardi": "https://wine.sothebys.com/cdn/shop/files/BSRM75.jpg?v=1726587127",
    "spirit-captain-morgan": "https://caskcartel.com/cdn/shop/products/CaptainMorganSpiced_1400x.jpg?v=1569248935",
    "spirit-malibu": "https://assets.superliquor.co.nz/thumbs/0018159.png",
    "spirit-kraken": "https://spliquor.ca/cdn/shop/files/TheKrakenBlackSpicedRum750mL.jpg?v=1772129771",
    "spirit-sailor-jerry": "https://raretequilas.com/cdn/shop/products/Studio_Project-2022-05-27T104744.179_1200x1200.jpg?v=1660770580",
    "spirit-cruzan": "https://www.bswliquor.com/cdn/shop/files/CZ_Batch1_PDP_Card_Option1_R03_1000x1000_AgedLight_png.webp?v=1753126211",
    "spirit-tanqueray": "https://thewinebox.biz/wp-content/uploads/2022/02/tanqueray-london-dry-gin.png",
    "spirit-bombay-sapphire": "https://www.divinodrinks.com/740-large_default/gin-bombay-saphir.jpg",
    "spirit-beefeater": "https://www.campoluzenoteca.com/8525-large_default/beefeater.jpg",
    "spirit-hendricks": "https://mrliquor.com.au/cdn/shop/products/Hendrick_s_Gin_700mL-1.jpg?v=1573617605",
    "spirit-gordons": "https://centurywines.com.sg/cdn/shop/files/CWS00684_Gordon_sGin700ml_550x.jpg?v=1761292694",
    "spirit-baileys": "https://www.centrobibite.it/2395-thickbox_default/liquore-baileys-original-irish-cream-1-lt.jpg",
    "spirit-jagermeister": "https://boozeone.ph/cdn/shop/files/95.png?v=1696384136&width=1500",
    "spirit-hennessy": "https://i5.walmartimages.com/seo/Hennessy-VS-Cognac-750-ml-Glass-Bottle-40-ABV_42cd752f-e7e8-4009-b570-e29c528a8403.adf5a428f4d806ed94f723c642e8d1ef.png?odnBg=FFFFFF&odnHeight=768&odnWidth=768",
    "spirit-kahlua": "https://www.wholesales.co.ug/wp-content/uploads/2019/03/pral28.jpg.jpg",
    "rtd-white-claw": "https://images.gopuff.com/blob/gopuffcatalogstorageprod/catalog-images-container/resize/cf/version%3D1_2%2Cformat%3Dauto%2Cfit%3Dscale-down%2Cwidth%3D800%2Cheight%3D800/c127f1c2-10c1-495b-8ffd-c70c66803e92-background_removed.png",
    "rtd-truly": "https://www.trulyhardseltzer.com/app_media/trulyredux/products/new-product-cans/pho_everyday_productshot_can_rlime_111518.file?h=1520&hash=DAF76B1725247391EF0111B83AB97EF4D932D6C6&la=en&w=1468",
    "rtd-high-noon": "https://images.gopuff.com/blob/gopuffcatalogstorageprod/catalog-images-container/resize/cf/version%3D1_0%2Cformat%3Dauto%2Cfit%3Dscale-down%2Cwidth%3D800%2Cheight%3D800/a024a5d1-1046-46e7-81b0-e5679d34bfc8.png",
    "rtd-cutwater": "https://assets.liquidcommerce.co/catalog/partner/img/1f76b184-2006-440f-ad00-f81b8eff2601.jpg",
    "rtd-buzzballz": "https://bankswinesandspirits.com/cdn/shop/files/buzzballz-passionfruit-martini-spirits-cocktail-200ml-1168583665.png?v=1747839438",
    "rtd-twisted-tea": "https://d2j6dbq0eux0bg.cloudfront.net/images/31078077/5110460679.jpg",
    "rtd-smirnoff-ice": "https://res.cloudinary.com/promenade-prod/image/upload/b_rgb%3Affffff%2Cc_pad%2Cd_alcohol%3Avendor%3Aglobal%3Acatalog%3Aproduct%3Aimage-placeholder.png%2Cdpr_2.0%2Cf_auto%2Cfl_preserve_transparency%2Ch_450%2Cq_auto%2Cw_450/v1623282038/alcohol/vendor/100181/catalog/product/2/0/20210609044013_file_60c0eeed6438d_60c0ef03574aa.jpeg",
    "rtd-mikes-hard": "https://www.kroger.com/product/images/xlarge/front/0063598500024",
    "rtd-surfside": "https://store.statesidevodka.com/cdn/shop/products/surfside-front_1e388430-489b-42ca-801e-2c241db74a64_1200x1200.png?v=1707495267",
    "rtd-nutrl": "https://thebeerman.ca/storage/2024/02/553164.jpg",
    "rtd-fresca": "https://photos-us.bazaarvoice.com/photo/2/cGhvdG86Y29uc3RlbGxhdGlvbmJyYW5kcw/d6ff5ece-c2b8-5abc-8637-057e81ff0586",
    "rtd-vizzy": "https://www.vizzyhardseltzer.com/sites/vizzyhardseltzer/files/2022-02/VIZZY_ExtendedCanGaurd_1200x940_RGB_0.png",
    "rtd-press": "https://www.bevindustry.com/ext/resources/2019/New-Products/June/PressPear_web.png?height=635&t=1561566775&width=1200",
    "rtd-jd-coke": "https://www.brown-forman.com/sites/default/files/styles/576x576_no_cropping/public/salsify_images/b81e20846abbeefad3de8dc5231364ec73a8e8bc.png?itok=ffwoexu8",
    "rtd-crown-royal": "https://www.reservebar.com/_next/image?q=75&url=https%3A%2F%2Fassets.liquidcommerce.co%2Fcatalog%2Fpartner%2Fimg%2F42d20f90-eaa9-4335-aba7-565f3603ec1e.jpg&w=1920",
    "rtd-four-loko": "https://cdn11.bigcommerce.com/s-h556z48a5y/images/stencil/1280x1280/products/5610/11579/84980600116__41265.1619118565.jpg?c=1",
    "rtd-seagrams": "https://images.gopuff.com/blob/gopuffcatalogstorageprod/catalog-images-container/resize/cf/version%3D1_2%2Cformat%3Dauto%2Cfit%3Dscale-down%2Cwidth%3D800%2Cheight%3D800/88dab124-f4dd-45d7-a432-7d26a8e023d5-padded.png",
    "rtd-topo-chico": "https://www.deeliver.co.za/cdn/shop/files/topo-chico-hard-seltzer-tangy-lemon-lime-6-pack-2.jpg?v=1687017282&width=1000"
}

_MARKET_PRODUCTS = (
    ("energy-red-bull", "Red Bull Energy Drink", "Energy Drinks", "Can", "250"),
    ("energy-celsius", "Celsius Sparkling Orange Energy Drink", "Energy Drinks", "Can", "400"),
    ("energy-bang", "Bang Energy Star Blast", "Energy Drinks", "Can", "350"),
    ("energy-rockstar", "Rockstar Original Energy Drink", "Energy Drinks", "Can", "300"),
    ("energy-c4", "C4 Energy Sour Batch Bros", "Energy Drinks", "Can", "400"),
    ("energy-alani-nu", "Alani Nu Cosmic Stardust", "Energy Drinks", "Can", "400"),
    ("energy-reign", "Reign Total Body Fuel Tropical Storm", "Energy Drinks", "Can", "350"),
    ("energy-nos", "NOS Original Energy Drink", "Energy Drinks", "Can", "300"),
    ("energy-5hour", "5-hour Energy Berry Shot", "Energy Drinks", "Energy Shots", "350"),
    ("energy-prime", "Prime Energy Blue Raspberry", "Energy Drinks", "Can", "350"),
    ("energy-full-throttle", "Full Throttle Original Citrus", "Energy Drinks", "Can", "300"),
    ("energy-kickstart", "Mountain Dew Kickstart Orange Citrus", "Energy Drinks", "Can", "250"),
    ("energy-baya", "Starbucks Baya Energy Mango Guava", "Energy Drinks", "Can", "350"),
    ("energy-venom", "Venom Energy Black Cherry Kiwi", "Energy Drinks", "Can", "250"),
    ("energy-bloom", "Bloom Sparkling Energy Crisp Apple", "Energy Drinks", "Can", "350"),
    ("energy-zevia", "Zevia Energy Kola", "Energy Drinks", "Can", "300"),
    ("energy-gfuel", "G FUEL Fazeberry Energy Drink", "Energy Drinks", "Can", "350"),
    ("energy-amp", "Mountain Dew Amp Original Citrus", "Energy Drinks", "Can", "300"),
    ("spirit-titos", "Tito's Handmade Vodka 750 mL", "Spirits", "Vodka", "3500"),
    ("spirit-smirnoff", "Smirnoff No. 21 Vodka 750 mL", "Spirits", "Vodka", "2200"),
    ("spirit-absolut", "Absolut Vodka 750 mL", "Spirits", "Vodka", "3200"),
    ("spirit-grey-goose", "Grey Goose Vodka 750 mL", "Spirits", "Vodka", "8500"),
    ("spirit-ketel-one", "Ketel One Vodka 750 mL", "Spirits", "Vodka", "4200"),
    ("spirit-svedka", "Svedka Vodka 750 mL", "Spirits", "Vodka", "2800"),
    ("spirit-new-amsterdam", "New Amsterdam Vodka 750 mL", "Spirits", "Vodka", "2200"),
    ("spirit-skyy", "SKYY Vodka 750 mL", "Spirits", "Vodka", "2800"),
    ("spirit-ciroc", "Cîroc Vodka 750 mL", "Spirits", "Vodka", "9000"),
    ("spirit-deep-eddy", "Deep Eddy Original Vodka 750 mL", "Spirits", "Vodka", "3900"),
    ("spirit-jack-daniels", "Jack Daniel's Old No. 7 Tennessee Whiskey 750 mL", "Spirits", "Whiskey & Bourbon", "4000"),
    ("spirit-jim-beam", "Jim Beam Bourbon 750 mL", "Spirits", "Whiskey & Bourbon", "3200"),
    ("spirit-crown-royal", "Crown Royal Deluxe Canadian Whisky 750 mL", "Spirits", "Whiskey & Bourbon", "6000"),
    ("spirit-fireball", "Fireball Cinnamon Whisky 750 mL", "Spirits", "Whiskey & Bourbon", "2500"),
    ("spirit-makers-mark", "Maker's Mark Bourbon 750 mL", "Spirits", "Whiskey & Bourbon", "5300"),
    ("spirit-jameson", "Jameson Irish Whiskey 750 mL", "Spirits", "Whiskey & Bourbon", "4600"),
    ("spirit-buffalo-trace", "Buffalo Trace Bourbon 750 mL", "Spirits", "Whiskey & Bourbon", "4500"),
    ("spirit-bulleit", "Bulleit Bourbon 750 mL", "Spirits", "Whiskey & Bourbon", "5200"),
    ("spirit-woodford", "Woodford Reserve Bourbon 750 mL", "Spirits", "Whiskey & Bourbon", "6500"),
    ("spirit-evan-williams", "Evan Williams Bourbon 750 mL", "Spirits", "Whiskey & Bourbon", "3000"),
    ("spirit-wild-turkey", "Wild Turkey 101 Bourbon 750 mL", "Spirits", "Whiskey & Bourbon", "4000"),
    ("spirit-four-roses", "Four Roses Bourbon 750 mL", "Spirits", "Whiskey & Bourbon", "4200"),
    ("spirit-knob-creek", "Knob Creek 9 Year Bourbon 750 mL", "Spirits", "Whiskey & Bourbon", "5800"),
    ("spirit-basil-hayden", "Basil Hayden's Bourbon 750 mL", "Spirits", "Whiskey & Bourbon", "6500"),
    ("spirit-johnnie-walker", "Johnnie Walker Red Label Scotch Whisky 750 mL", "Spirits", "Whiskey & Bourbon", "3800"),
    ("spirit-dewars", "Dewar's White Label Scotch Whisky 750 mL", "Spirits", "Whiskey & Bourbon", "3800"),
    ("spirit-glenlivet", "The Glenlivet 12 Year Single Malt Scotch 750 mL", "Spirits", "Whiskey & Bourbon", "7500"),
    ("spirit-patron", "Patrón Silver Tequila 750 mL", "Spirits", "Tequila", "9000"),
    ("spirit-don-julio", "Don Julio Blanco Tequila 750 mL", "Spirits", "Tequila", "9500"),
    ("spirit-casamigos", "Casamigos Blanco Tequila 750 mL", "Spirits", "Tequila", "8500"),
    ("spirit-jose-cuervo", "José Cuervo Especial Gold Tequila 750 mL", "Spirits", "Tequila", "3500"),
    ("spirit-espolon", "Espolòn Blanco Tequila 750 mL", "Spirits", "Tequila", "5500"),
    ("spirit-1800", "1800 Silver Tequila 750 mL", "Spirits", "Tequila", "6500"),
    ("spirit-herradura", "Herradura Plata Tequila 750 mL", "Spirits", "Tequila", "7500"),
    ("spirit-teremana", "Teremana Blanco Tequila 750 mL", "Spirits", "Tequila", "6000"),
    ("spirit-bacardi", "Bacardí Superior White Rum 750 mL", "Spirits", "Rum", "3000"),
    ("spirit-captain-morgan", "Captain Morgan Original Spiced Rum 750 mL", "Spirits", "Rum", "3200"),
    ("spirit-malibu", "Malibu Original Coconut Rum 750 mL", "Spirits", "Rum", "3000"),
    ("spirit-kraken", "The Kraken Black Spiced Rum 750 mL", "Spirits", "Rum", "5500"),
    ("spirit-sailor-jerry", "Sailor Jerry Spiced Rum 750 mL", "Spirits", "Rum", "4500"),
    ("spirit-cruzan", "Cruzan Aged Light Rum 750 mL", "Spirits", "Rum", "3500"),
    ("spirit-tanqueray", "Tanqueray London Dry Gin 750 mL", "Spirits", "Gin", "4500"),
    ("spirit-bombay-sapphire", "Bombay Sapphire Gin 750 mL", "Spirits", "Gin", "5000"),
    ("spirit-beefeater", "Beefeater London Dry Gin 750 mL", "Spirits", "Gin", "4200"),
    ("spirit-hendricks", "Hendrick's Gin 750 mL", "Spirits", "Gin", "8000"),
    ("spirit-gordons", "Gordon's London Dry Gin 750 mL", "Spirits", "Gin", "3000"),
    ("spirit-baileys", "Baileys Original Irish Cream 750 mL", "Spirits", "Liqueurs & Cognac", "3800"),
    ("spirit-jagermeister", "Jägermeister Herbal Liqueur 700 mL", "Spirits", "Liqueurs & Cognac", "4200"),
    ("spirit-hennessy", "Hennessy VS Cognac 750 mL", "Spirits", "Liqueurs & Cognac", "8500"),
    ("spirit-kahlua", "Kahlúa Coffee Liqueur 700 mL", "Spirits", "Liqueurs & Cognac", "3500"),
    ("rtd-white-claw", "White Claw Surge Lime Hard Seltzer", "Mixed Drinks & Hard Seltzers", "Hard Seltzers", "350"),
    ("rtd-truly", "Truly R. Lime Hard Seltzer", "Mixed Drinks & Hard Seltzers", "Hard Seltzers", "350"),
    ("rtd-high-noon", "High Noon Lemon Vodka Soda", "Mixed Drinks & Hard Seltzers", "Vodka Sodas", "450"),
    ("rtd-cutwater", "Cutwater Piña Colada Canned Cocktail", "Mixed Drinks & Hard Seltzers", "Canned Cocktails", "650"),
    ("rtd-buzzballz", "BuzzBallz Passionfruit Martini", "Mixed Drinks & Hard Seltzers", "Canned Cocktails", "450"),
    ("rtd-twisted-tea", "Twisted Tea Original Hard Iced Tea", "Mixed Drinks & Hard Seltzers", "Malt Beverages", "350"),
    ("rtd-smirnoff-ice", "Smirnoff Ice Original", "Mixed Drinks & Hard Seltzers", "Malt Beverages", "350"),
    ("rtd-mikes-hard", "Mike's Hard Lemonade Original", "Mixed Drinks & Hard Seltzers", "Malt Beverages", "350"),
    ("rtd-surfside", "Surfside Iced Tea + Vodka", "Mixed Drinks & Hard Seltzers", "Vodka Sodas", "450"),
    ("rtd-nutrl", "Nütrl Lemon Vodka Soda", "Mixed Drinks & Hard Seltzers", "Vodka Sodas", "450"),
    ("rtd-fresca", "Fresca Mixed Vodka Spritz", "Mixed Drinks & Hard Seltzers", "Canned Cocktails", "450"),
    ("rtd-vizzy", "Vizzy Hard Seltzer", "Mixed Drinks & Hard Seltzers", "Hard Seltzers", "350"),
    ("rtd-press", "PRESS Pear Chamomile Hard Seltzer", "Mixed Drinks & Hard Seltzers", "Hard Seltzers", "450"),
    ("rtd-jd-coke", "Jack Daniel's & Coca-Cola", "Mixed Drinks & Hard Seltzers", "Canned Cocktails", "450"),
    ("rtd-crown-royal", "Crown Royal Whisky & Cola", "Mixed Drinks & Hard Seltzers", "Canned Cocktails", "450"),
    ("rtd-four-loko", "Four Loko Gold", "Mixed Drinks & Hard Seltzers", "Malt Beverages", "450"),
    ("rtd-seagrams", "Seagram's Escapes Jamaican Me Happy", "Mixed Drinks & Hard Seltzers", "Malt Beverages", "350"),
    ("rtd-topo-chico", "Topo Chico Tangy Lemon Lime Hard Seltzer", "Mixed Drinks & Hard Seltzers", "Hard Seltzers", "400"),
)

DEMO_PRODUCTS += tuple(
    {
        "seed_key": key,
        "name": name,
        "description": (
            ("Age-restricted alcoholic beverage. " if category in ("Spirits", "Mixed Drinks & Hard Seltzers") else "")
            + f"Approximate KES {int(price):,} reference price; photo shows the named product. Retail stock and checkout are not connected."
        ),
        "price": price,
        "category": category,
        "subcategory": subcategory,
        "image": _PRODUCT_IMAGES[key],
        "availability": True,
    }
    for key, name, category, subcategory, price in _MARKET_PRODUCTS
)

def seed_underground_products(collection, vendor_ids, now=None):
    vendor_ids = tuple(vendor_ids)
    if not vendor_ids or any(type(vendor_id) is not int or vendor_id < 1 for vendor_id in vendor_ids):
        raise ValueError("At least one existing positive integer user ID is required.")

    created_at = now or datetime.now(timezone.utc)
    for index, seed_product in enumerate(DEMO_PRODUCTS):
        product = {
            key: value
            for key, value in seed_product.items()
            if key != "seed_key"
        }
        validated = underground_product_schema.load(
            {
                **product,
                "vendor_id": vendor_ids[index % len(vendor_ids)],
            }
        )
        validated["price"] = Decimal128(Decimal(validated["price"]))
        validated.update(
            marketplace=MARKETPLACE_ID,
            average_rating=0.0,
            seed_key=seed_product["seed_key"],
        )

        collection.update_one(
            {
                "marketplace": MARKETPLACE_ID,
                "seed_key": seed_product["seed_key"],
            },
            {
                "$set": validated,
                "$setOnInsert": {"created_at": created_at},
            },
            upsert=True,
        )

    return len(DEMO_PRODUCTS)


def seed_database():
    app = create_app()
    with app.app_context():
        vendor_ids = [
            user_id
            for (user_id,) in db.session.query(User.id).order_by(User.id).all()
        ]
        if not vendor_ids:
            raise RuntimeError(
                "Create at least one Community Cart user before seeding Underground."
            )

        count = seed_underground_products(
            get_underground_products(),
            vendor_ids,
        )
        print(f"Synchronized {count} Underground demo catalog products.")


if __name__ == "__main__":
    seed_database()
