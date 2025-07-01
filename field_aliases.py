field_aliases = {
    # --- Общие данные ---
    "age": {"возраст", "сколько мне лет", "мне лет", "годы", "год", "дата рождения", "день рождения"},
    "gender": {"пол", "мужчина или женщина", "мужской", "женский"},
    "nationality": {"национальность", "гражданство", "страна"},
    "height_cm": {"рост", "какой у меня рост", "см", "сантиметры"},
    "weight_kg": {"вес", "вес тела", "килограммы", "кг"},
    "eye_color": {"цвет глаз", "глаза"},
    "hair_color": {"цвет волос", "волосы"},
    "shoe_size_eu": {"размер обуви", "обувь", "размер ноги"},
    "clothing_top": {"размер верха одежды", "размер рубашки", "верх", "кофта"},
    "clothing_bottom": {"размер низа одежды", "размер штанов", "штаны", "джинсы"},
    "hat_size": {"размер головного убора", "шапка", "обхват головы"},

    # 🍿 Кино
    "favorite_genre": {"жанр", "жанры", "жанр кино", "жанры кино", "жанр фильма", "жанры фильмов", "жанр кинематографа", "жанровая принадлежность", "жанровый стиль", "любимый жанр", "любимые жанры", "предпочитаемый жанр", "люблю жанры", "кино-жанр", "киношный жанр", "стиль фильма", "направление кино", "жанр кинокартин", "вид фильма", "genre", "genres", "movie genre", "film genre", "cinema genre", "type of movie", "film category", "story type"},
    "favorite_movie": {"фильм", "фильмы", "любимый фильм", "любимые фильмы", "любимые кинокартины", "фильмы которые нравятся", "кино", "кинцо", "картина", "кинофильм", "киномувик", "лучшая картина", "люблю фильм", "фильмы по душе", "кинолента", "любимый мувик", "movie", "movies", "film", "films", "motion picture", "cinema", "movie title", "movie name", "picture"},
    "favorite_actor": {"актер", "актёр", "актриса", "актёры", "актрисы", "любимые актеры", "любимый актер", "любимая актриса", "любимые актрисы", "кинозвезда", "звезда кино", "исполнитель роли", "персонаж", "звезды кино", "любимые исполнители", "люблю актера", "люблю актрису", "movie star", "film star", "cinema star", "star", "actor", "actors", "actress", "actresses", "performer", "cast"},
    "favorite_director": {"режиссёр", "режиссер", "режиссёры", "режиссеры", "любимый режиссер", "любимые режиссеры", "автор фильма", "постановщик", "снял фильм", "снял(а)", "кто снял", "снимал", "создатель фильма", "режиссура", "мастер постановки", "автор картины", "director", "directors", "film director", "movie director", "filmmaker", "cinema creator", "producer"},

    # 🎵 Музыка
    "favorite_song": {"песня", "песни", "любимая песня", "любимые песни", "трек", "треки", "композиция", "мелодия", "музыкальное произведение", "сингл", "хит", "запись", "что слушаю", "что нравится слушать", "любимая мелодия", "song", "songs", "track", "tracks", "hit", "single", "composition", "melody", "tune", "record"},
    "favorite_band": {"группа", "группы", "любимая группа", "любимые группы", "исполнитель", "исполнители", "музыкальная группа", "артист", "артисты", "вокалист", "вокалисты", "коллектив", "музыкант", "музыканты", "band", "bands", "music group", "group", "artist", "artists", "singer", "singers", "performer", "musician", "musicians", "solo artist", "duo"},
    "music_preference": {"жанр музыки", "жанры музыки", "музыкальный жанр", "музыкальные жанры", "музыкальные предпочтения", "предпочитаемые жанры", "любимая музыка", "музыка которую люблю", "музыка по вкусу", "жанровые предпочтения", "что слушаю", "что нравится в музыке", "music genre", "music genres", "genre", "genres", "music style", "style of music", "music preference", "music taste", "favorite genres", "favorite music"},

    # 🍽️ Еда и напитки
    # --- Виртуальные группы ---
    "all_food_preferences": {"какие блюда я люблю", "что я люблю есть", "моя еда", "что люблю из еды", "моя любимая еда", "предпочтения в еде", "что ем", "еда", "любимые блюда", "вся еда", "пища", "все про еду", "favorite_dishes"},

    "favorite_cuisine": {"кухня", "кухни", "любимая кухня", "национальная кухня", "еда народов", "cuisine", "cuisines"},
    "favorite_soups": {"суп", "супы", "первое", "горячее", "жидкое блюдо", "бульон", "уха", "крем-суп", "пюре-суп", "суп-пюре",  "наваристый суп", "борщ", "щи", "солянка", "рассольник", "куриный суп", "грибной суп", "гороховый суп", "щи с капустой", "борщ с мясом", "овощной суп", "мясной суп", "суп с лапшой", "суп с фрикадельками", "харчо", "суп харчо", "уха", "щи зелёные", "окрошка", "томатный суп", "суп с фасолью", "сырный суп", "луковый суп", "суп с брокколи", "чечевичный суп", "чоудер", "минестроне", "бульон с гренками", "рамэн", "мисо суп", "фо", "том ям", "суп с водорослями", "суп с тофу", "суп кимчи", "удон", "soup", "soups", "hot soup", "broth", "chicken soup", "pea soup", "cream soup", "puree soup", "cheese soup", "tomato soup", "noodle soup", "mushroom soup", "lentil soup", "onion soup", "minestrone", "chowder", "ramen", "miso soup", "pho", "tom yum", "udon soup", "kimchi soup"},
    "favorite_macaroni": {"макароны", "лапша", "итальянская лапша", "макарошки", "спагетти", "феттуччине", "тальятелле", "пельтине", "пенне", "ригатони", "трубочки", "ракушки", "каннелони", "равиоли", "тортеллини", "фарфалле", "орекьетте", "капеллини", "фузилли", "бабочки", "вермишель", "гнёзда", "гнездо", "шайбочки", "лепестки", "noodles", "spaghetti", "fettuccine", "tagliatelle", "penne", "rigatoni", "macaroni", "shells", "tubes", "lasagna", "cannelloni", "ravioli", "tortellini", "farfalle", "orecchiette", "fusilli", "angel hair", "pasta nests"},
    "favorite_pasta_recipes": {"макароны по-флотски", "паста","болоньезе", "паста болоньезе", "альфредо", "паста альфредо", "карбонара", "паста карбонара", "арабьята", "аматричана", "маринара", "песто", "паста с песто", "четыре сыра", "4 сыра", "паста 4 сыра", "помодоро", "путанеска", "нормадо", "фунги", "неаполитана", "паста с грибами", "паста с курицей", "паста с морепродуктами", "паста с креветками", "паста с лососем", "паста с тунцом", "сливочная паста", "томатная паста", "паста с сыром", "паста с овощами", "острая паста", "лазанья", "lasagna", "bolognese", "alfredo", "carbonara", "arrabbiata", "amatriciana", "marinara", "pesto", "four cheese", "4 cheese", "fungi", "puttanesca", "napolitana", "creamy pasta", "tomato pasta", "spicy pasta", "chicken pasta", "seafood pasta", "shrimp pasta", "mushroom pasta", "cheese pasta", "veggie pasta", "tuna pasta", "salmon pasta","pasta"},
    "favorite_dumplings": {"пельмени", "вареники", "манты", "хинкали", "гёдза", "гёдза", "гёза", "чучвара", "позы", "буузы", "дамплинги", "азиатские пельмени", "жареные пельмени", "dumplings", "dumpling", "manti", "khinkali", "gyoza", "mandu", "wontons", "baozi", "shumai", "xiao long bao", "steamed dumplings", "fried dumplings", "meat dumplings", "potato dumplings", "cherry dumplings", "cottage cheese dumplings"},
    "favorite_salads": {"салат", "салаты", "салатик", "любимый салат", "вкусный салат", "овощной салат", "зелёный салат", "свежий салат", "домашний салат", "салат с курицей", "салат с тунцом", "салат с яйцом", "салат с крабовыми палочками", "салат с грибами", "цезарь", "греческий салат", "оливье", "винегрет", "селёдка под шубой", "капрезе", "нисуаз", "рукола с пармезаном", "кобб", "чука", "морковча", "салат чука", "буррата", "salad", "salads", "vegetable salad", "green salad", "fresh salad", "caesar", "caesar salad", "greek salad", "olivier", "vinaigrette", "shuba", "caprese", "nicoise", "cobb salad", "chuka salad", "tuna salad", "egg salad", "chicken salad", "crab salad", "mushroom salad", "mozzarella salad"},
    "favorite_pizza": {"пицца", "пиццы", "пицца с сыром", "пицца с мясом", "пицца с грибами", "вкусная пицца", "итальянская пицца", "толстая пицца", "тонкая пицца", "домашняя пицца", "маргарита", "пепперони", "четыре сыра", "4 сыра", "карбонара", "гавайская", "барбекю", "мясная", "вегетарианская", "овощная", "с курицей", "с колбасой", "с беконом", "с ветчиной", "с морепродуктами", "с ананасами", "неаполитанская", "римская", "кальцоне", "закрытая пицца", "pizza", "pizzas", "margherita", "pepperoni", "cheese pizza", "4 cheese", "four cheese", "carbonara", "hawaiian", "bbq", "meat pizza", "veggie pizza", "chicken pizza", "seafood pizza", "ham pizza", "pineapple pizza", "neapolitan", "roman", "calzone", "stuffed crust"},
    "favorite_baked": {"выпечка", "выпеченные изделия", "мучное", "булочные изделия", "хлебобулочные изделия", "хлеб", "батон", "багет", "чиабатта", "лепёшка", "лепешка", "лаваш", "хлебцы", "хлеб на закваске", "бородинский", "зерновой хлеб", "черный хлеб", "белый хлеб", "bread", "loaf", "baguette", "ciabatta", "flatbread", "pita", "sourdough", "rye bread", "wheat bread", "булочка", "булочки", "сдоба", "плюшка", "улитка", "круассан", "бриошь", "калач", "булочка с корицей", "синнабон", "с начинкой", "слойка", "плюшки", "bun", "buns", "cinnamon roll", "croissant", "brioche", "pastry", "danish", "swirl bun", "пирог", "пироги", "пирожок", "пирожки", "пирог с начинкой", "яблочный пирог", "капустный пирог", "курник", "расстегай", "шарлотка", "галета", "киш", "самса", "хачапури", "pie", "pies", "filled pie", "meat pie", "apple pie", "cabbage pie", "quiche", "galette", "samsa", "khachapuri", "charlotte", "слойка", "слойки", "слойка с яблоками", "слойка с повидлом", "пончик", "пончики", "эклер", "эклеры", "профитроли", "тарт", "маффин", "маффины", "кекс", "кексы", "печенье", "песочное", "орешки с начинкой", "puff", "puffs", "donut", "donuts", "eclair", "profiteroles", "tart", "muffin", "muffins", "cupcake", "cookie", "shortbread"},
    "favorite_eggs": {"омлет", "яичница", "глазунья", "скрэмбл", "вареное яйцо", "omelet", "scrambled eggs", "fried egg", "egg", "eggs", "boiled egg"},
    "fast_food": {"фастфуд", "быстрая еда", "уличная еда", "стритфуд", "еда на ходу", "быстрый перекус", "junk food", "street food", "fast food", "takeaway", "take-out", "бургер", "бургеры", "гамбургер", "чизбургер", "дабл чиз", "веган бургер", "сэндвич", "сэндвичи", "бутерброд", "хот-дог", "хотдоги", "hot dog", "burger", "cheeseburger", "hamburger", "sandwich", "sub", "club sandwich", "шаурма", "шаверма", "донер", "донер-кебаб", "ролл", "shawarma", "doner", "wrap", "gyros", "тако", "такос", "буррито", "кесадилья", "начос", "taco", "tacos", "burrito", "quesadilla", "nachos", "mexican wrap", "картошка фри", "фри", "по-деревенски", "наггетсы", "куриные крылышки", "луковые кольца", "кукурузные палочки", "сырные шарики", "french fries", "fries", "potato wedges", "nuggets", "chicken wings", "onion rings", "cheese balls", "corn sticks"},
    "favorite_grains": {"крупа", "крупы", "каша", "каши", "любимая каша", "варёная крупа", "злаки", "злаковое", "гарнир", "гарниры", "рис", "плов", "гречка", "гречневая каша", "овсянка", "овсяная каша", "перловка", "перловая каша", "манка", "манная каша", "пшено", "пшённая каша", "кукурузная каша", "ячневая каша", "булгур", "кускус", "чечевица", "чечевичная каша", "rice", "pilaf", "buckwheat", "oatmeal", "porridge", "semolina", "millet", "barley", "cornmeal", "bulgur", "couscous", "lentils", "grain", "grains", "groats"},
    "favorite_meat": {"мясо", "мясное", "мясное блюдо", "жаркое", "тушеное мясо", "запечённое мясо", "курица", "цыпленок", "куриное мясо", "куриные крылья", "бедро", "филе", "индейка", "утка", "говядина", "свинина", "телятина", "баранина", "кролик", "фарш", "ветчина", "грудинка", "карбонад", "пастрами",  "meat", "red meat", "white meat", "chicken", "turkey", "duck", "beef", "pork", "veal", "lamb", "rabbit", "bacon", "ham", "brisket", "pastrami", "cold cuts"},
    "favorite_fish": {"рыба", "рыбка", "рыбное", "рыбное блюдо", "рыбные блюда", "жареная рыба", "запечённая рыба", "отварная рыба", "солёная рыба", "копчёная рыба", "вяленая рыба", "рыба гриль", "рыба в кляре", "рыба на пару", "лосось", "семга", "форель", "треска", "судак", "окунь", "карп", "хек", "дорадо", "скумбрия", "тунец", "палтус", "осётр", "щука", "минтай", "камбала", "сардина", "анчоус", "килька", "корюшка", "икра", "чёрная икра", "красная икра", "caviar", "black caviar", "red caviar", "fish", "fish dish", "grilled fish", "baked fish", "fried fish", "steamed fish", "smoked fish", "salted fish", "dried fish", "salmon", "trout", "cod", "pike", "perch", "carp", "haddock", "hake", "mackerel", "tuna", "halibut", "sturgeon", "pike-perch", "anchovy", "sardine", "dorado", "flounder", "white fish"},
    "favorite_seafood": {"морепродукты", "морская еда", "морская кухня", "дар моря", "морской деликатес", "креветка", "креветки", "тигровые креветки", "королевские креветки", "мидия", "мидии", "кальмар", "кальмары", "осминог", "осьминоги", "краб", "крабы", "крабовое мясо", "омар", "лангуст", "лобстер", "морской гребешок", "гребешки", "улитки", "трепанг", "морской ёж", "морской коктейль", "seafood", "seafood dish", "shrimp", "prawns", "tiger shrimp", "king prawns", "mussels", "scallops", "squid", "calamari", "octopus", "crab", "crab meat", "lobster", "langoustine", "roe", "sea urchin", "sea snail", "sea cucumber", "shellfish", "seafood mix", "seafood cocktail"},
    "favorite_sushi": {"суши", "роллы", "суши-роллы", "sushi", "rolls", "sushi rolls", "филадельфия", "ролл филадельфия", "калифорния", "ролл калифорния", "спайси ролл", "темпура ролл", "ролл с угрём", "ролл с тунцом", "ролл с лососем", "ролл с крабом", "ролл с авокадо", "ролл с креветкой", "ролл с сыром", "ролл с огурцом", "philadelphia", "california", "dragon roll", "green dragon", "black dragon", "spicy roll", "tempura roll", "eel roll", "tuna roll", "salmon roll", "crab roll", "shrimp roll", "cheese roll", "avocado roll", "cucumber roll", "маки", "нори-маки", "футо-маки", "хосо-маки", "урамаки", "нигири", "гунканы", "сашими", "makizushi", "maki", "futomaki", "hosomaki", "uramaki", "nigiri", "gunkan", "sashimi", "запечённые роллы", "роллы с икрой", "роллы с соусом", "запечённые суши", "темпура суши", "роллы в кунжуте", "роллы без нори","baked rolls", "rolls with caviar", "tempura sushi", "no-nori rolls", "sesame rolls"},
    "hot_dishes": {"горячее", "мясное блюдо", "мясные блюда", "второе блюдо", "основное блюдо", "тёплое блюдо", "основное на обед", "горячее мясное", "тёплое овощное", "домашняя еда", "блюдо с гарниром", "запечённое", "hot dish", "main course", "warm dish", "homemade dish", "hearty meal", "голубцы", "фаршированные перцы", "тушёная капуста", "тушёная картошка", "жареная картошка с луком", "пюре с подливой", "жареная капуста", "жареные овощи", "гречка с мясом", "рис с подливой", "картошка с подливой", "stuffed cabbage", "stuffed peppers", "braised cabbage", "braised potatoes", "fried potatoes", "fried vegetables", "buckwheat with gravy", "котлеты", "тефтели", "биточки", "зразы", "митболы", "фрикадельки", "котлеты по-киевски", "куриные котлеты", "мясные котлеты", "капустные котлеты", "cutlets", "meatballs", "minced patties", "zrazy", "chicken patties", "vegetable patties", "гуляш", "жаркое", "бефстроганов", "мясо в соусе", "печень с луком", "курица в сметане", "говядина в подливе", "почки в соусе", "фрикасе", "goulash", "stroganoff", "stew", "beef stew", "chicken fricassee", "liver with onions", "мясная запеканка", "овощная запеканка", "картофельная запеканка", "кабачковая запеканка", "курица по-французски", "рыба под сыром", "рыба в духовке", "овощи с сыром", "meat casserole", "vegetable bake", "baked fish", "baked chicken", "cheesy bake", "рататуй", "мусака", "паэлья", "шницель", "рагу", "овощное рагу", "мясное рагу", "курица в томатном соусе", "телятина тушёная", "говядина с луком", "жаркое по-домашнему", "кастрюльное блюдо", "stew", "vegetable stew", "beef ragout", "meat stew", "casserole dish", "холодец", "заливное", "мясо в желе", "рыба в желе", "мясо в горшочке", "мясо по-французски", "язык в соусе", "отбивная", "куриная грудка", "свиная отбивная", "aspic", "meat jelly", "french-style meat", "pork chop", "pot meat", "beef tongue in sauce"},
    "favorite_desserts": {"десерт", "десерты", "сладкое", "вкусняшка", "сладости", "что-нибудь сладкое", "что-то к чаю", "dessert", "desserts", "sweet", "sweets", "treat", "sweet treat", "торт", "тортики", "чизкейк", "медовик", "наполеон", "шоколадный торт", "ягодный торт", "эклер", "эклеры", "профитроли", "капкейк", "капкейки", "маффин", "маффины", "пирожное", "пирожные", "брауни", "брауни с орехами", "cake", "cheesecake", "medovik", "napoleon cake", "chocolate cake", "eclair", "profiterole", "cupcake", "muffin", "brownie", "pastry", "mini cake", "мороженое", "эскимо", "рожок", "фруктовый лёд", "пломбир", "сорбет", "ice cream", "gelato", "popsicle", "sorbet", "ice lolly", "cone", "халва", "рахат-лукум", "пахлава", "чак-чак", "зефир", "мармелад", "турецкие сладости", "восточные сладости", "halva", "turkish delight", "baklava", "lokum", "marshmallow", "fruit jelly", "шоколад", "шоколадка", "горький шоколад", "молочный шоколад", "конфеты", "батончики", "трюфели", "карамель", "chocolate", "candy", "candies", "truffle", "candy bar", "snickers", "twix", "мусс", "пудинг", "творожный десерт", "панна котта", "тирамису", "крем", "желе", "mousse", "pudding", "tiramisu", "custard", "cream", "jelly", "panna cotta"},
    "favorite_fruits_and_berries": {"фрукты", "фрукт", "ягоды", "свежие фрукты", "сезонные фрукты", "fruits", "fruit", "fresh fruit", "апельсин", "апельсины", "мандарин", "мандаринки", "грейпфрут", "лимон", "лайм", "orange", "mandarin", "tangerine", "grapefruit", "lemon", "lime", "яблоко", "яблоки", "груша", "груши", "apple", "apples", "pear", "pears", "слива", "сливы", "персик", "персики", "нектарин", "абрикос", "абрикосы", "plum", "plums", "peach", "peaches", "nectarine", "apricot", "apricots", "банан", "бананы", "ананас", "ананасы", "манго", "папайя", "киви", "авокадо", "гуава", "питахайя", "питайя", "драконий фрукт", "личи", "рамбутан", "бананчик", "мангостин", "кокос", "банан с йогуртом", "banana", "pineapple", "mango", "papaya", "kiwi", "avocado", "dragonfruit", "pitaya", "lychee", "rambutan", "guava", "mangosteen", "coconut", "клубника", "земляника", "малина", "ежевика", "черника", "голубика", "вишня", "черешня", "смородина", "клюква", "брусника", "strawberry", "raspberry", "blueberry", "blackberry", "cherry", "sour cherry", "currant", "cranberry", "lingonberry", "berry", "berries", "виноград", "зелёный виноград", "тёмный виноград", "кишмиш", "grape", "grapes", "white grapes", "red grapes", "raisin", "seedless grapes", "сухофрукты", "курага", "чернослив", "изюм", "финики", "инжир", "dried fruits", "dried apricot", "prunes", "raisins", "dates", "figs"},
    "favorite_vegetables": {"овощ", "овощи", "овощной", "овощи на гарнир", "свежие овощи", "vegetables", "veggie", "veggies", "морковь", "морковка", "картошка", "картофель", "свёкла", "свекла", "редис", "редька", "пастернак", "топинамбур", "carrot", "potato", "beet", "beetroot", "radish", "parsnip", "jerusalem artichoke", "капуста", "белокочанная капуста", "краснокочанная капуста", "брокколи", "цветная капуста", "брюссельская капуста", "пекинская капуста", "romanesco", "broccoli", "cauliflower", "cabbage", "red cabbage", "brussels sprouts", "napa cabbage", "шпинат", "салат", "латук", "руккола", "щавель", "кинза", "петрушка", "укроп", "базилик", "лук зеленый", "зелень", "spinach", "lettuce", "arugula", "sorrel", "parsley", "cilantro", "dill", "basil", "green onion", "herbs", "leafy greens", "помидор", "помидоры", "томаты", "томат", "черри", "перец", "болгарский перец", "чёрный перец", "перец чили", "баклажан", "кабачок", "цуккини", "патиссон", "tomato", "cherry tomato", "pepper", "bell pepper", "chili pepper", "eggplant", "zucchini", "squash", "pattypan squash", "горошек", "зелёный горошек", "фасоль", "стручковая фасоль", "нут", "соя", "бобы", "peas", "green peas", "beans", "kidney beans", "string beans", "lentils", "chickpeas", "soybeans", "legumes", "лук", "репчатый лук", "красный лук", "шалот", "чеснок", "onion", "red onion", "shallot", "garlic", "огурец", "огурцы", "кукуруза", "авокадо", "артишок", "топинамбур", "редиска", "кукуруза сладкая", "цуккини", "огурец маринованный", "cucumber", "pickled cucumber", "corn", "avocado", "artichoke", "radish"},
    "diet_preference": {"диета", "диеты", "предпочтения по диете", "питание", "стиль питания", "режим питания", "diet", "diets", "eating habits", "nutrition"},
    "favorite_drink": {"напиток", "напитки", "любимый напиток", "любимые напитки", "питье", "что пить", "drinks", "drink", "beverage", "beverages", "чай", "кофе", "латте", "капучино", "эспрессо", "американо", "матча", "какао", "горячий шоколад", "tea", "coffee", "latte", "cappuccino", "espresso", "matcha", "hot chocolate", "cocoa", "сок", "соки", "морс", "компот", "газировка", "лимонад", "фанта", "кола", "пепси", "ice tea", "cold brew", "juice", "juices", "soda", "soft drink", "lemonade", "fanta", "cola", "pepsi", "iced tea", "cold coffee", "молоко", "молочные напитки", "кефир", "йогурт", "айран", "ряженка", "сыворотка", "milk", "dairy drink", "yogurt", "kefir", "buttermilk", "протеиновый коктейль", "протеин", "энергетик", "изотоник", "BCAA", "электролиты", "protein shake", "protein drink", "energy drink", "sports drink", "isotonic", "bcaa", "electrolyte drink", "пиво", "вино", "шампанское", "сидр", "коктейль", "виски", "ром", "ликёр", "водка", "текила", "мартини", "джин", "беллис", "алкоголь", "спиртное", "beer", "wine", "champagne", "cider", "cocktail", "whiskey", "rum", "liqueur", "vodka", "tequila", "martini", "gin", "alcohol", "alcoholic drink"},
    "favorite_restaurant_cafe_bars": {"ресторан", "рестораны", "любимый ресторан", "любимые рестораны", "заведение", "заведения", "место где поесть", "где поесть", "куда сходить поесть", "место для еды", "ресторанчик", "ресторанчики", "ресторанное место", "restaurant", "restaurants", "diner", "eatery", "place to eat", "кафе", "кафешка", "кафешки", "кофейня", "кофейни", "coffee shop", "cafe", "cafes", "coffeeshop", "бар", "бары", "паб", "пабы", "пивная", "пивнушка", "алкоплейс", "bar", "bars", "pub", "pubs", "beer house", "tavern", "фастфуд", "фаст-фуд", "мак", "макдональдс", "бургерная", "шаурмячная", "пиццерия", "забегаловка", "fast food", "mcdonald's", "burger place", "shawarma place", "pizza place", "pizza parlor", "takeaway", "take-out", "доставка еды", "доставка", "еды на дом", "еда с собой", "delivery", "takeout", "food delivery", "to-go", "суши-бар", "суши", "суши ресторан", "японский ресторан", "азиатский ресторан", "итальянский ресторан", "sushi bar", "sushi place", "sushi restaurant", "italian restaurant", "asian restaurant", "kitchen""макдональдс", "mcdonalds", "mcdonald's", "макдак", "mcdak", "бургер кинг", "burger king", "kfc", "кефси", "кефц", "кей эф си", "старбакс", "starbucks", "сабвэй", "subway", "доминос", "domino's", "dominos", "папа джонс", "papa johns", "папа джон", "пицца хат", "pizza hut", "тако белл", "taco bell", "шоколадница", "кофе хаус", "кофехаус", "даблби", "double b", "doubleb", "кавказская пленница", "кавкафе", "кофемания", "coffeemania", "иль патио", "il patio", "кофе лайк", "coffeelike", "яндекс лавка кафе", "lavka cafe", "лавка", "вкусно и точка", "вкусно — и точка", "теремок", "teremok", "му-му", "му му", "му", "my-my", "ёбидоёби", "ebidoebi", "ёби", "тануки", "tanuki", "якитория", "yakitoria", "фрайдис", "tgi friday's", "tgi fridays", "джон джоли", "john joly", "бургер герл", "burger girl", "крошка картошка", "kroshka kartoshka", "суши вок", "sushi wok", "воккер", "wokker", "туда суши", "tuda sushi", "япоша", "yaposha", "суши шоп", "sushi shop", "якитория", "yakitoria", "фудбенд", "foodband",  "додо пицца", "dodo pizza", "папа джонс", "papa john's", "пиццафабрика", "pizza fabrika", "пицца темпо", "pizza tempo", "black star burger", "blackstar burger", "бургер клаб", "burger club", "шаурма лавка", "шаурмания", "шаверма пати", "шаверма", "kitchen", "суши точка", "суши ленд", "суши мастер"},

    # 🧴 Уход
    "haircare": {"уход за волосами", "волосы уход", "уход для волос", "волосы", "волосяной уход", "шампунь", "бальзам", "кондиционер", "маска для волос", "укладка", "стайлинг", "сыворотка для волос", "haircare", "hair care", "hair", "shampoo", "conditioner", "hair mask", "hair serum", "hair treatment", "styling"},
    "skincare": {"уход за лицом", "лицо уход", "уход для лица", "лицо", "лицевая кожа", "крема", "маски", "сыворотка", "очищение", "пилинг", "крем для лица", "сыворотка для лица", "тонер", "мицеллярная вода", "скраб", "увлажнение лица", "skincare", "skin care", "face care", "face", "moisturizer", "serum", "toner", "cleanser", "peeling", "face mask", "face cream"},
    "bodycare": {"уход за телом", "тело уход", "уход для тела", "тело", "кожа тела", "лосьон", "гель для душа", "скраб для тела", "масло для тела", "мыло", "увлажнение тела", "антиперспирант", "дезодорант", "bodycare", "body care", "body", "body lotion", "shower gel", "body scrub", "body butter", "soap", "moisturizer", "deodorant"},
    "perfume": {"парфюм", "духи", "аромат", "туалетная вода", "парфюмерия", "одеколон", "эссенция", "запах", "флакон духов", "персональный аромат", "парф", "perfume", "parfum", "fragrance", "cologne", "eau de toilette", "scent"},
    "homecare": {"бытовая химия", "уход за домом", "домашние принадлежности", "домашняя химия", "чистящие средства", "уборка", "мытьё", "средства для уборки", "стирка", "порошок", "освежитель", "запах для дома", "домашняя чистота", "homecare", "home care", "cleaning", "household", "detergent", "cleaner", "laundry", "air freshener", "cleaning supplies"},

    # 👗 Внешность и одежда
    "style": {"стиль", "мода", "лук", "образ", "внешний вид", "look", "style", "outfit", "appearance"},
    "underwear": {"нижнее белье", "белье", "трусы", "трусики", "трусы женские", "трусы мужские", "лифчик", "лифчики", "бра", "бюстгальтер", "бюстгалтер", "бюстгальтеры", "panties", "underwear", "bra", "bras", "lingerie", "intimates"},
    "tops": {"топ", "топы", "майка", "майки", "футболка", "футболки", "лонгслив", "лонгсливы", "рубашка", "рубашки", "водолазка", "водолазки", "свитшот", "свитшоты", "худи", "толстовка", "толстовки", "кофта", "кофты", "блузка", "блузки", "shirt", "shirts", "t-shirt", "t-shirts", "tee", "tees", "tank", "tank top", "tops", "sweatshirt", "hoodie", "blouse", "crop top"},
    "bottoms": {"штаны", "штанов", "брюки", "брюк", "джинсы", "джинс", "леггинсы", "легинсы", "джоггеры", "шорты", "шорт", "юбка", "юбки", "бриджи", "капри", "юбчонка", "pants", "trousers", "jeans", "shorts", "leggings", "joggers", "skirt", "skirts", "capris", "bottoms"},
    "outerwear": {"верхняя одежда", "куртка", "куртки", "пальто", "плащ", "жилет", "ветровка", "jacket", "jackets", "coat", "coats", "trench", "vest", "outerwear", "overcoat"},
    "shoes": {"обувь", "ботинок", "ботинки", "ботильоны", "туфля", "туфли", "кроссовок", "кроссовки", "кеды", "слипоны", "мокасины", "сандалия", "сандалии", "босоножка", "босоножки", "шлепки", "шлёпки", "тапок", "тапки", "сапог", "сапоги", "угги", "валенки", "груверы", "обувка", "обувочка", "шузы", "шуз", "обувной стиль", "shoe", "shoes", "sneaker", "sneakers", "trainers", "boots", "boot", "heels", "flats", "sandals", "slippers", "loafers", "moccasins", "slip-ons", "slides", "flip-flops", "platforms"},
    "accessories": {"украшение", "украшения", "подарок украшения", "ювелирное украшение", "ювелирные изделия", "ювелирка", "драгоценности", "драгоценное украшение", "аксессуары", "бижутерия", "стильное украшение", "роскошное украшение", "дизайнерское украшение", "кольцо", "кольца", "обручальное кольцо", "помолвочное кольцо", "серьги", "серёжки", "пусеты", "гвоздики", "висячие серьги", "кольца в ушах", "ожерелье", "цепочка", "цепь", "подвеска", "кулон", "браслет", "браслеты", "чокер", "брошь", "броши", "зажим", "булавка", "перстень", "кафф", "колье", "анклет", "наушники-украшения", "золотое кольцо", "серебряный браслет", "золото", "серебро", "платина", "бриллианты", "изумруды", "жемчуг", "камни", "минералы", "фианиты", "драгоценный металл", "драгоценный камень", "кристаллы", "камушки", "jewelry", "jewel", "jewels", "jewelry gift", "ring", "rings", "engagement ring", "wedding ring", "bracelet", "bracelets", "necklace", "necklaces", "pendant", "pendants", "choker", "earrings", "studs", "dangling earrings", "hoop earrings", "brooch", "brooches", "chain", "chains", "accessories", "gold", "silver", "platinum", "diamond", "emerald", "pearl", "precious stone", "gem", "stone", "crystal", "set of jewelry", "boxed jewelry", "gift set", "luxury jewelry", "fashion jewelry"},
    "bags": {"сумка", "сумки", "сумочка", "рюкзак", "рюкзаки", "клатч", "торба", "баул", "авоська", "bag", "bags", "backpack", "purse", "handbag", "clutch", "tote", "crossbody", "shoulder bag", "fanny pack"},

    # 🎨 Хобби и интересы
    "hobbies": {"хобби", "увлечение", "увлечения", "любимые занятия", "что люблю делать", "интересы", "чем занимаюсь", "досуг", "времяпрепровождение", "в свободное время", "развлечения", "hobby", "hobbies", "interests", "pastime", "free time activity", "leisure", "fun", "things I enjoy""активности", "впечатления", "эмоции", "подарок эмоции", "spa", "день в spa", "массаж", "парный массаж", "спа-комплекс", "хаммам", "баня", "расслабление", "ароматерапия", "вино и сыр", "дегустация", "чайная церемония", "wine tasting", "tea ceremony", "wellness day", "relax day", "couple retreat", "romantic spa", "кулинарный мастер-класс", "мастеркласс по выпечке", "приготовление суши", "коктейльный мастер-класс", "бариста-класс", "гончарный круг", "рисование", "живопись вином", "каллиграфия", "мастер-класс по флористике", "мыловарение", "рисование на холсте","cooking class", "art class", "floristics", "pottery workshop", "painting masterclass", "поход", "пикник", "кемпинг", "прогулка", "конная прогулка", "велопрогулка", "рыбалка", "катание на лодке", "байдарки", "SUP-доски", "загородный отдых", "прогулка на яхте", "яхта", "катер", "полет на воздушном шаре", "на природе", "на даче", "в лесу", "на озере", "hiking", "yachting", "boating", "paddleboarding", "horse riding", "прыжок с парашютом", "полет в аэротрубе", "банджи-джампинг", "тарзанка", "дельтаплан", "параплан", "полёт на самолете", "пилотирование", "полет на вертолете", "авиасимулятор", "экстремальные гонки", "ралли", "картинг", "дрифт-тренировка", "вождение спорткара", "внедорожник", "offroad", "джип-трофи", "покататься на квадроцикле", "снегоходы", "лазертаг", "пейнтбол", "стрельба из лука", "тир", "стрельба из оружия", "мечи и доспехи", "арчеритаг", "скалодром", "зиплайн", "rope park", "skydiving", "bungee", "paragliding", "flying experience", "gun range", "drift training", "race car", "paintball", "quad biking", "air tunnel", "helicopter tour", "extreme adventure", "adrenaline experience", "квест", "квест-комната", "подарочный квест", "эксклюзивный квест", "психологический квест", "ужастик", "escape room", "интерактивная игра", "настольная игра", "виртуальная реальность", "VR-игра", "AR-игра", "реалити-квест", "role play", "детективное шоу", "вечер в масках", "театр-ужин"},
    "conversation_topics": {"темы для бесед", "тема для беседы", "разговорные темы", "топики", "интересные темы", "про что поговорить", "что обсудить", "вопросы для беседы", "topics for conversation", "conversation topics", "talking points", "chat topics"},
    "sports_preferences": {"спорт", "виды спорта", "любимые виды спорта", "спортивные предпочтения", "чем занимаюсь из спорта", "активности", "фитнес", "активный отдых", "тренировки", "физкультура", "sports", "sport", "fitness", "training", "exercise", "physical activity", "sports preferences", "active hobbies"},
    "concerts": {"концерт", "концерты", "живые выступления", "живой звук", "живуха", "гиг", "мероприятия", "музыкальные шоу", "выступления", "сходить на концерт", "live music", "concert", "concerts", "gig", "live show", "performance"},
    "exhibitions": {"выставка", "выставки", "музей", "музеи", "экспозиция", "экспозиции", "галерея", "галереи", "арт-пространство", "art show", "art fair", "museum", "museums", "exhibition", "exhibitions", "gallery", "galleries", "art space"},
    "theater_preferences": {"театр", "театры", "поход в театр", "спектакль", "спектакли", "представление", "представления", "шоу", "перформанс", "сценическое искусство", "theater", "theatre", "performance", "show", "drama", "stage play", "musical"},
    "seminars": {"семинар", "семинары", "форум", "форумы", "мастеркласс", "мастерклассы", "лекция", "лекции", "воркшоп", "обучающее мероприятие", "интенсив", "курсы", "образование", "обучение", "seminar", "seminars", "masterclass", "masterclasses", "lecture", "lectures", "workshop", "training", "course", "bootcamp", "forum", "conference"},
    "favorite_quotes": {"любимая цитата", "любимые цитаты", "цитата", "цитаты", "фраза", "фразы", "высказывание", "мем", "мемы", "любимые выражения", "цитаты из фильмов", "мотивационные фразы", "quotes", "favorite quote", "favorite quotes", "phrases", "catchphrases", "memes", "saying", "sayings", "quote of the day"},
    "favorite_books": {"любимая книга", "любимые книги", "книга", "книги", "автор", "авторы", "писатели", "литература", "чтиво", "что читаю", "что люблю читать", "books", "book", "author", "authors", "favorite author", "reading", "literature", "novels", "bestsellers"},

    # ✈️ Путешествия
    "travel_places": {"путешествие", "путешествия", "путешествую", "путешествовал", "поездки", "поездка", "куда хочу поехать", "где был", "поездка мечты", "люблю путешествовать", "любимые места", "любимые направления", "места отдыха", "популярные места", "любимые города", "любимые страны","города", "город", "страна", "страны", "курорты", "острова", "пляжи", "на природе", "в горах", "в лесу", "travel", "travels", "trip", "trips", "journey", "vacation", "holiday", "destination", "destinations", "places to go", "favorite places", "cities", "countries", "resorts", "islands", "beach", "mountains", "nature"},

    # 💪 Здоровье
    "fitness": {"фитнес", "спорт", "физическая активность", "тренировка", "тренировки", "занятие спортом", "физкультура", "нагрузка", "движение", "зарядка", "упражнения", "активный образ жизни", "спортзал", "зал", "тренажеры", "бег", "йога", "плавание", "кардио", "силовые упражнения", "fitness", "workout", "exercise", "training", "physical activity", "gym", "gym training", "sport", "run", "jogging", "cardio", "strength", "yoga", "swimming", "crossfit", "movement"},
    "relax_methods": {"отдых", "релакс", "расслабление", "методы расслабления", "способы отдыха", "как расслабляюсь", "расслабляюсь так", "чем отдыхаю", "отдых после работы", "перезагрузка", "релаксация",  "медитация", "тишина", "прогулка", "природа", "горячая ванна", "ничего не делание", "relax", "relaxation", "rest", "chilling", "meditation", "recovery", "recharge", "nap", "walk", "nature", "silence", "bathing", "soothing", "unwind", "de-stress", "calm down"},

    # 💼 Профессия
    "career": {"профессия", "работа", "род занятий", "чем занимаюсь", "специализация", "чем зарабатываю", "сфера деятельности", "должность", "карьера", "профдеятельность", "career", "job", "occupation", "work", "employment", "position", "field", "role", "specialty", "what I do"},
    "professional_interests": {"профессиональные интересы", "интересы по работе", "интересы в карьере", "чем интересуюсь профессионально", "карьерные цели", "направления развития", "интересующие сферы", "интересы в профессии", "professional interests", "career interests", "field of interest", "work-related interests", "career goals"},

    # # 🌸 Цветы
    "favorite_flowers": {"цветок", "цветы", "живые цветы", "свежие цветы", "букет", "букеты", "букет цветов", "букет в подарок", "композиция из цветов", "цветочная композиция", "композиция в коробке", "цветочная коробка", "цветы в коробке", "цветы в корзине", "корзина с цветами", "цветы в вазе", "в цветочной упаковке", "цветы с лентой", "подарочные цветы", "букет на праздник", "розы", "роза", "тюльпан", "тюльпаны", "пионы", "пион", "орхидея", "орхидеи", "лилия", "лилии", "ромашка", "ромашки", "гвоздика", "гвоздики", "хризантема", "хризантемы", "ирис", "ирисы", "альстромерии", "нарцисс", "нарциссы", "гортензия", "гортензии", "сирень", "лава́нда", "эустома", "фрезия", "анемоны", "гладиолусы", "камелии", "астры", "ранункулюсы", "амариллис", "лизиантус", "полевые цветы", "сезонные цветы", "садовые цветы", "экзотические цветы", "редкие цветы", "душистые цветы", "синие цветы", "белые цветы", "розовые цветы", "красные цветы", "сухоцветы", "flowers", "flower", "bouquet", "bouquets", "floral gift", "flower gift", "flower arrangement", "flower box", "hatbox flowers", "floral box", "basket of flowers", "gift flowers", "romantic bouquet", "bridal bouquet", "anniversary flowers", "birthday flowers", "valentine bouquet", "rose bouquet", "tulip bouquet", "peony bouquet", "wildflowers", "fresh flowers", "cut flowers", "seasonal bouquet", "floral present", "blossom", "flower surprise", "hand-tied bouquet", "floristics", "mini bouquet", "giant bouquet", "chic flowers", "elegant flowers"}
    
}

# --- Построение field_to_column на основе синонимов ---
field_to_column = {}
for internal_field, synonyms in field_aliases.items():
    # Добавим сам ключ как допустимое имя
    field_to_column[internal_field.lower()] = internal_field
    for synonym in synonyms:
        field_to_column[synonym.lower()] = internal_field

# --- Все внутренние поля ---
all_fields = set(field_to_column.values())

# --- Человекочитаемые названия ---
field_names = {
    field: field.replace("_", " ").capitalize()
    for field in all_fields
}

# --- Обратное сопоставление: человекочитаемое → внутреннее имя ---
name_to_field = {
    v.lower(): k for k, v in field_names.items()
}

# --- Поля, к которым можно прикреплять изображения ---
fields_with_images = {
    # 🍿 Кино
    "favorite_movie",
    "favorite_actor",
    "favorite_director",

    # 🎵 Музыка
    "favorite_song",
    "favorite_band",

    # 🍽️ Еда и напитки
    "favorite_cuisine",
    "favorite_soups",
    "favorite_macaroni",
    "favorite_pasta_recipes",
    "favorite_dumplings",
    "favorite_salads",
    "favorite_pizza",
    "favorite_baked",
    "favorite_eggs",
    "fast_food",
    "favorite_grains",
    "favorite_meat",
    "favorite_fish",
    "favorite_seafood",
    "favorite_sushi",
    "hot_dishes",
    "favorite_desserts",
    "favorite_fruits_and_berries",
    "favorite_vegetables",
    "favorite_drink",
    "favorite_restaurant_cafe_bars", 

    # 🧴 Уход
    "haircare",
    "skincare",
    "bodycare",
    "perfume",
    "homecare",

    # 👗 Внешность и одежда
    "style",
    "underwear",
    "tops",
    "bottoms",
    "outerwear",
    "shoes",
    "accessories",
    "bags",

    # 🎨 Хобби и интересы
    "hobbies",
    "conversation_topics",
    "sports_preferences",
    "concerts",
    "exhibitions",
    "theater_preferences",
    "seminars",
    "favorite_books",

    # ✈️ Путешествия
    "travel_places",

    # 💪 Здоровье
    "fitness",
    "relax_methods",

    # 💼 Профессия
    "career",
    "professional_interests",

    # 🌸 Цветы
    "favorite_flowers",
}


# --- Функция нормализации: преобразует поле от GPT или пользователя в внутреннее имя поля ---
def normalize_field(raw_field: str) -> str | None:
    raw = raw_field.strip().lower()

    # 1. Если это уже внутреннее имя поля (ключ в field_aliases) — возвращаем как есть
    if raw in field_aliases:
        return raw

    # 2. Иначе ищем среди синонимов
    return field_to_column.get(raw)