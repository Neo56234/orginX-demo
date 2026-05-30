"""
Seed 54 Bangladesh misinformation incidents into known_cases with embeddings + tsvector.
Run inside the worker container:
  python seed_incidents.py
"""
import sys
import logging
from datetime import date

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger("seed_incidents")

sys.path.insert(0, "/app")

from app.database import SessionLocal
from app.models import KnownCase
from sqlalchemy import text

INCIDENTS = [
    # CATEGORY 1: July-August 2024 Quota Reform Protests
    {"title_en": "Police and Chhatra League shooting from rooftop during quota reform protests", "title_bn": "কোটা আন্দোলনে ছাদের ওপর থেকে পুলিশ ও ছাত্রলীগের গুলি", "false_claim_en": "Shooting happening right now in Bangladesh — today's incident", "false_claim_bn": "বাংলাদেশে এখনই গুলি চলছে — আজকের ঘটনা", "actual_origin_country": "Bangladesh", "actual_origin_city": "Dhaka", "actual_origin_date": "2024-07-19", "debunk_source": "july_movement_2024", "debunk_url": "https://rumourscanner.com", "keywords": ["quota reform", "july 2024", "chhatra league", "police", "shooting", "rooftop", "কোটা আন্দোলন", "ছাত্রলীগ", "গুলি"]},
    {"title_en": "Chhatra League attacks unarmed students in Ramganj with police present", "title_bn": "রামগঞ্জে পুলিশের উপস্থিতিতে ছাত্রলীগের হামলা", "false_claim_en": "Students being attacked in Bangladesh right now — today's incident", "false_claim_bn": "বাংলাদেশে ছাত্রদের ওপর হামলা হচ্ছে — আজকের ঘটনা", "actual_origin_country": "Bangladesh", "actual_origin_city": "Ramganj, Lakshmipur", "actual_origin_date": "2024-07-18", "debunk_source": "july_movement_2024", "debunk_url": "https://rumourscanner.com", "keywords": ["ramganj", "lakshmipur", "chhatra league", "unarmed students", "july 2024", "রামগঞ্জ", "লক্ষ্মীপুর"]},
    {"title_en": "Chhatra League rampage against unarmed students in Cumilla — 4 August 2024", "title_bn": "কুমিল্লায় ছাত্রলীগের তাণ্ডব — ৪ আগস্ট ২০২৪", "false_claim_en": "Students being attacked in Bangladesh today — ongoing incident", "false_claim_bn": "বাংলাদেশে আজকে ছাত্রদের ওপর হামলা হচ্ছে", "actual_origin_country": "Bangladesh", "actual_origin_city": "Cumilla", "actual_origin_date": "2024-08-04", "debunk_source": "july_movement_2024", "debunk_url": "https://rumourscanner.com", "keywords": ["cumilla", "comilla", "chhatra league", "4 august 2024", "কুমিল্লা", "ছাত্রলীগ", "তাণ্ডব"]},
    {"title_en": "Abu Sayed shot dead by police during Rangpur quota protest", "title_bn": "রংপুরে কোটা আন্দোলনে পুলিশের গুলিতে আবু সায়েদ নিহত", "false_claim_en": "Student killed by army in fake military crackdown — not police", "false_claim_bn": "সেনাবাহিনীর গুলিতে ছাত্র নিহত", "actual_origin_country": "Bangladesh", "actual_origin_city": "Rangpur", "actual_origin_date": "2024-07-16", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com/abu-sayed-rangpur", "keywords": ["abu sayed", "rangpur", "quota protest", "police shooting", "july 16 2024", "আবু সায়েদ", "রংপুর"]},
    {"title_en": "2018 quota reform protest footage recycled as July 2024 protests", "title_bn": "২০১৮ সালের কোটা আন্দোলনের ভিডিও ২০২৪ সালের বলে প্রচার", "false_claim_en": "This video shows the July 2024 quota movement — live footage", "false_claim_bn": "এটি ২০২৪ সালের কোটা আন্দোলনের লাইভ ভিডিও", "actual_origin_country": "Bangladesh", "actual_origin_city": "Dhaka", "actual_origin_date": "2018-04-08", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["2018 quota reform", "recycled footage", "2024 claimed", "পুরনো ভিডিও", "২০১৮", "কোটা"]},
    {"title_en": "Pakistan PTI protest footage (2023) falsely shared as Bangladesh quota protest 2024", "title_bn": "পাকিস্তানের পিটিআই বিক্ষোভের ভিডিও বাংলাদেশের বলে ছড়ানো", "false_claim_en": "Massive protest in Bangladesh against the government — quota movement 2024", "false_claim_bn": "বাংলাদেশে সরকারবিরোধী বিশাল বিক্ষোভ", "actual_origin_country": "Pakistan", "actual_origin_city": "Lahore", "actual_origin_date": "2023-11-26", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["pakistan", "PTI", "lahore protest", "quota movement", "পাকিস্তান", "পিটিআই"]},
    {"title_en": "India CAA protest footage (2019) shared as Bangladesh quota reform protest 2024", "title_bn": "ভারতের সিএএ বিক্ষোভের ভিডিও বাংলাদেশের বলে দাবি", "false_claim_en": "Police crackdown on protesters in Bangladesh — quota movement", "false_claim_bn": "বাংলাদেশে বিক্ষোভকারীদের ওপর পুলিশের দমন", "actual_origin_country": "India", "actual_origin_city": "Delhi", "actual_origin_date": "2019-12-15", "debunk_source": "alt_news", "debunk_url": "https://altnews.in", "keywords": ["india", "CAA protest", "2019", "Bangladesh claimed", "ভারত", "সিএএ", "দিল্লি"]},
    {"title_en": "Hefazat-e-Islam 2013 Dhaka footage shared as quota protest 2024", "title_bn": "২০১৩ সালের হেফাজতের ভিডিও ২০২৪ কোটা আন্দোলনের বলে প্রচার", "false_claim_en": "Massive clash in Dhaka during quota reform protests 2024", "false_claim_bn": "২০২৪ কোটা আন্দোলনে ঢাকায় ব্যাপক সংঘর্ষ", "actual_origin_country": "Bangladesh", "actual_origin_city": "Dhaka", "actual_origin_date": "2013-05-05", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["hefazat", "2013", "motijheel", "recycled", "2024 claimed", "হেফাজত", "মতিঝিল"]},
    {"title_en": "Indian Army vehicle footage shared as Bangladesh Army crackdown on students", "title_bn": "ভারতীয় সেনাবাহিনীর ভিডিও বাংলাদেশ সেনাবাহিনীর বলে প্রচার", "false_claim_en": "Bangladesh Army deployed against students during quota protests", "false_claim_bn": "কোটা আন্দোলনে বাংলাদেশ সেনাবাহিনী মোতায়েন", "actual_origin_country": "India", "actual_origin_city": "Kashmir", "actual_origin_date": "2021-05-10", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["indian army", "kashmir", "bangladesh army claimed", "সেনাবাহিনী", "কাশ্মীর"]},
    {"title_en": "Narayanganj attack on quota protesters falsely shown as Dhaka University incident", "title_bn": "নারায়ণগঞ্জের হামলার ভিডিও ঢাকা বিশ্ববিদ্যালয়ের বলে প্রচার", "false_claim_en": "Quota protesters attacked inside Dhaka University campus", "false_claim_bn": "ঢাকা বিশ্ববিদ্যালয় ক্যাম্পাসে হামলা", "actual_origin_country": "Bangladesh", "actual_origin_city": "Narayanganj", "actual_origin_date": "2024-07-17", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["narayanganj", "dhaka university", "quota protest", "wrong location", "নারায়ণগঞ্জ"]},

    # CATEGORY 2: August 2024 — Hasina Resignation
    {"title_en": "India celebration footage shared as Bangladesh celebrating Hasina resignation", "title_bn": "ভারতের উৎসবের ভিডিও বাংলাদেশে হাসিনার পদত্যাগের উদযাপন বলে প্রচার", "false_claim_en": "Bangladeshis celebrating Sheikh Hasina resignation in the streets", "false_claim_bn": "হাসিনার পদত্যাগে বাংলাদেশের রাস্তায় উৎসব", "actual_origin_country": "India", "actual_origin_city": "Kolkata", "actual_origin_date": "2024-06-04", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["india celebration", "hasina resignation", "Kolkata", "ভারত", "হাসিনা পদত্যাগ"]},
    {"title_en": "Myanmar coup military footage (2021) shared as Bangladesh Army takeover August 2024", "title_bn": "মিয়ানমার সামরিক অভ্যুত্থানের ভিডিও বাংলাদেশের বলে প্রচার", "false_claim_en": "Bangladesh Army staging a coup after Hasina resignation", "false_claim_bn": "হাসিনার পদত্যাগের পর বাংলাদেশ সেনাবাহিনীর অভ্যুত্থান", "actual_origin_country": "Myanmar", "actual_origin_city": "Naypyidaw", "actual_origin_date": "2021-02-01", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["myanmar coup", "army takeover", "2021", "Bangladesh claimed", "মিয়ানমার", "সামরিক অভ্যুত্থান"]},
    {"title_en": "Old BNP rally footage shared as post-Hasina victory celebration August 2024", "title_bn": "বিএনপির পুরনো র‍্যালির ভিডিও হাসিনা-পরবর্তী বিজয় উদযাপন বলে প্রচার", "false_claim_en": "Massive celebration rally in Dhaka after Sheikh Hasina resigned", "false_claim_bn": "হাসিনার পদত্যাগের পর ঢাকায় বিশাল উদযাপন", "actual_origin_country": "Bangladesh", "actual_origin_city": "Dhaka", "actual_origin_date": "2022-10-10", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["BNP rally", "2022", "hasina resignation", "victory rally", "বিএনপি", "পুরনো সমাবেশ"]},
    {"title_en": "Pakistan celebration footage shared as Bangladesh after August 5, 2024", "title_bn": "পাকিস্তানের উদযাপনের ভিডিও বাংলাদেশের বলে প্রচার", "false_claim_en": "Pakistan celebrating fall of Sheikh Hasina government", "false_claim_bn": "বাংলাদেশে হাসিনা সরকারের পতনে পাকিস্তানে উদযাপন", "actual_origin_country": "Pakistan", "actual_origin_city": "Karachi", "actual_origin_date": "2024-08-06", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["pakistan celebration", "hasina fall", "2024", "পাকিস্তান", "হাসিনা পতন"]},

    # CATEGORY 3: 2021 Cumilla Hindu Temple Violence
    {"title_en": "India temple attack footage shared as Cumilla Bangladesh Hindu persecution 2021", "title_bn": "ভারতের মন্দিরে হামলার ভিডিও কুমিল্লার ঘটনা বলে প্রচার", "false_claim_en": "Hindus being attacked and temples destroyed in Cumilla Bangladesh right now", "false_claim_bn": "কুমিল্লায় হিন্দুদের ওপর হামলা ও মন্দির ভাঙচুর হচ্ছে এখনই", "actual_origin_country": "India", "actual_origin_city": "Tripura", "actual_origin_date": "2021-10-27", "debunk_source": "boom_live", "debunk_url": "https://boomlive.in", "keywords": ["cumilla", "hindu temple", "2021", "india tripura", "কুমিল্লা", "মন্দির হামলা"]},
    {"title_en": "2012 Ramu Buddhist temple attack footage recycled as 2021 Cumilla incident", "title_bn": "২০১২ সালের রামু বৌদ্ধ মন্দির হামলার ভিডিও ২০২১ এর বলে প্রচার", "false_claim_en": "New wave of religious minority attacks in Bangladesh 2021", "false_claim_bn": "বাংলাদেশে ২০২১ সালে ধর্মীয় সংখ্যালঘুদের ওপর নতুন হামলা", "actual_origin_country": "Bangladesh", "actual_origin_city": "Ramu, Cox's Bazar", "actual_origin_date": "2012-09-29", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["ramu", "2012", "buddhist temple", "recycled 2021", "রামু", "বৌদ্ধ মন্দির"]},
    {"title_en": "Pakistani mosque attack video shared as Hindu temple attack in Bangladesh", "title_bn": "পাকিস্তানে মসজিদে হামলার ভিডিও বাংলাদেশে মন্দির হামলার বলে প্রচার", "false_claim_en": "Religious site being destroyed in Bangladesh — minority community under attack", "false_claim_bn": "বাংলাদেশে ধর্মীয় স্থান ধ্বংস", "actual_origin_country": "Pakistan", "actual_origin_city": "Peshawar", "actual_origin_date": "2021-03-12", "debunk_source": "afp_factcheck", "debunk_url": "https://factcheck.afp.com", "keywords": ["pakistan mosque", "peshawar", "bangladesh minority claimed", "পাকিস্তান", "মসজিদ হামলা"]},

    # CATEGORY 4: 2022 Pakistan Floods
    {"title_en": "Pakistan Sindh flood footage (2022) shared as Bangladesh Sylhet flood", "title_bn": "পাকিস্তানের সিন্ধু প্রদেশের বন্যার ভিডিও বাংলাদেশের সিলেটের বলে প্রচার", "false_claim_en": "Massive flooding in Sylhet Bangladesh — people stranded", "false_claim_bn": "বাংলাদেশের সিলেটে ভয়াবহ বন্যা", "actual_origin_country": "Pakistan", "actual_origin_city": "Sindh", "actual_origin_date": "2022-08-25", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["pakistan sindh flood", "sylhet claimed", "2022", "পাকিস্তান", "সিন্ধু", "বন্যা", "সিলেট"]},
    {"title_en": "Kerala India flood footage shared as Bangladesh Haor region flooding", "title_bn": "ভারতের কেরালার বন্যার ভিডিও বাংলাদেশের হাওর অঞ্চলের বলে প্রচার", "false_claim_en": "Unprecedented flooding in Bangladesh haor area — thousands displaced", "false_claim_bn": "বাংলাদেশের হাওর অঞ্চলে অভূতপূর্ব বন্যা", "actual_origin_country": "India", "actual_origin_city": "Kerala", "actual_origin_date": "2018-08-16", "debunk_source": "boom_live", "debunk_url": "https://boomlive.in", "keywords": ["kerala flood", "india", "haor bangladesh", "কেরালা", "হাওর", "বন্যা"]},
    {"title_en": "2017 Bangladesh flood footage recycled as 2022 Sylhet-Sunamganj flood", "title_bn": "২০১৭ সালের বন্যার ভিডিও ২০২২ সালের সুনামগঞ্জের বন্যা বলে প্রচার", "false_claim_en": "Sylhet floods are the worst in 100 years — 2022", "false_claim_bn": "সিলেটে শতবর্ষের মধ্যে সবচেয়ে ভয়াবহ বন্যা ২০২২", "actual_origin_country": "Bangladesh", "actual_origin_city": "Sylhet", "actual_origin_date": "2017-06-15", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["2017 flood", "sylhet", "sunamganj", "recycled 2022", "পুরনো বন্যার ভিডিও"]},
    {"title_en": "China flood footage (Zhengzhou 2021) shared as Bangladesh flash flood", "title_bn": "চীনের বন্যার ভিডিও বাংলাদেশের আকস্মিক বন্যার বলে প্রচার", "false_claim_en": "Flash flood sweeps through Bangladesh city — cars swept away", "false_claim_bn": "বাংলাদেশের শহরে আকস্মিক বন্যা", "actual_origin_country": "China", "actual_origin_city": "Zhengzhou", "actual_origin_date": "2021-07-20", "debunk_source": "afp_factcheck", "debunk_url": "https://factcheck.afp.com", "keywords": ["china flood", "zhengzhou", "2021", "Bangladesh flash flood", "চীন", "বন্যা"]},

    # CATEGORY 5: COVID Misinfo
    {"title_en": "Chinese hospital overflow footage shared as Bangladesh hospital COVID crisis", "title_bn": "চীনের হাসপাতালের ভিডিও বাংলাদেশের কোভিড সংকটের বলে প্রচার", "false_claim_en": "Bangladesh hospitals overwhelmed — COVID patients dying in corridors", "false_claim_bn": "বাংলাদেশের হাসপাতাল পরিপূর্ণ — কোভিড রোগী মরছে", "actual_origin_country": "China", "actual_origin_city": "Wuhan", "actual_origin_date": "2020-02-01", "debunk_source": "afp_factcheck", "debunk_url": "https://factcheck.afp.com", "keywords": ["wuhan hospital", "china", "COVID Bangladesh", "উহান", "চীন", "কোভিড"]},
    {"title_en": "Italian cemetery drone footage shared as Bangladesh mass COVID graves", "title_bn": "ইতালির কবরস্থানের ড্রোন ভিডিও বাংলাদেশে গণকবরের বলে প্রচার", "false_claim_en": "Mass graves being dug in Bangladesh for COVID victims", "false_claim_bn": "বাংলাদেশে কোভিড আক্রান্তদের জন্য গণকবর খোঁড়া হচ্ছে", "actual_origin_country": "Italy", "actual_origin_city": "Bergamo", "actual_origin_date": "2020-03-18", "debunk_source": "boom_live", "debunk_url": "https://boomlive.in", "keywords": ["italy cemetery", "bergamo", "mass grave", "COVID Bangladesh", "ইতালি", "গণকবর"]},
    {"title_en": "India oxygen shortage hospital footage shared as Bangladesh COVID crisis 2021", "title_bn": "ভারতের অক্সিজেন সংকটের ভিডিও বাংলাদেশের কোভিড সংকট বলে প্রচার", "false_claim_en": "Bangladesh hospitals running out of oxygen — COVID patients dying", "false_claim_bn": "বাংলাদেশের হাসপাতালে অক্সিজেন শেষ", "actual_origin_country": "India", "actual_origin_city": "Delhi", "actual_origin_date": "2021-04-25", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["india oxygen shortage", "Delhi", "2021", "Bangladesh hospital", "অক্সিজেন সংকট"]},

    # CATEGORY 6: Rohingya
    {"title_en": "Myanmar military atrocity footage shared as Bangladeshi security force action", "title_bn": "মিয়ানমার সেনাবাহিনীর নৃশংসতার ভিডিও বাংলাদেশের নিরাপত্তা বাহিনীর বলে প্রচার", "false_claim_en": "Bangladesh security forces committing atrocities against Rohingya in camps", "false_claim_bn": "বাংলাদেশের নিরাপত্তা বাহিনী রোহিঙ্গা শিবিরে নৃশংসতা", "actual_origin_country": "Myanmar", "actual_origin_city": "Rakhine", "actual_origin_date": "2017-08-28", "debunk_source": "afp_factcheck", "debunk_url": "https://factcheck.afp.com", "keywords": ["myanmar military", "rohingya", "rakhine", "Bangladesh claimed", "মিয়ানমার", "রোহিঙ্গা"]},
    {"title_en": "India Assam NRC detention footage shared as Rohingya deportation from Bangladesh", "title_bn": "ভারতের আসামের এনআরসি আটকের ভিডিও বাংলাদেশ থেকে রোহিঙ্গা বহিষ্কারের বলে প্রচার", "false_claim_en": "Bangladesh deporting Rohingya refugees — mass deportation", "false_claim_bn": "বাংলাদেশ রোহিঙ্গা শরণার্থীদের বহিষ্কার করছে", "actual_origin_country": "India", "actual_origin_city": "Assam", "actual_origin_date": "2019-08-31", "debunk_source": "alt_news", "debunk_url": "https://altnews.in", "keywords": ["india assam", "NRC", "rohingya deportation", "আসাম", "এনআরসি", "রোহিঙ্গা"]},
    {"title_en": "Old Palestine conflict footage shared as Rohingya crisis in Bangladesh", "title_bn": "ফিলিস্তিনের পুরনো সংঘর্ষের ভিডিও বাংলাদেশে রোহিঙ্গা সংকটের বলে প্রচার", "false_claim_en": "Rohingya people being bombed and killed in Bangladesh", "false_claim_bn": "বাংলাদেশে রোহিঙ্গাদের বোমা মেরে হত্যা করা হচ্ছে", "actual_origin_country": "Palestine", "actual_origin_city": "Gaza", "actual_origin_date": "2014-07-20", "debunk_source": "afp_factcheck", "debunk_url": "https://factcheck.afp.com", "keywords": ["palestine", "gaza", "rohingya bangladesh", "ফিলিস্তিন", "গাজা", "রোহিঙ্গা"]},
    {"title_en": "2017 Rohingya exodus footage recycled as new displacement crisis 2023", "title_bn": "২০১৭ সালের রোহিঙ্গা বাস্তুচ্যুতির ভিডিও ২০২৩ সালের নতুন সংকট বলে প্রচার", "false_claim_en": "New wave of Rohingya refugees entering Bangladesh 2023", "false_claim_bn": "বাংলাদেশে রোহিঙ্গা শরণার্থীদের নতুন ঢল ২০২৩", "actual_origin_country": "Myanmar", "actual_origin_city": "Cox's Bazar border", "actual_origin_date": "2017-09-01", "debunk_source": "afp_factcheck", "debunk_url": "https://factcheck.afp.com", "keywords": ["rohingya exodus", "2017", "cox's bazar", "recycled 2023", "রোহিঙ্গা", "কক্সবাজার"]},

    # CATEGORY 7: Pakistan footage
    {"title_en": "Pakistan Army parade footage shared as Bangladesh Army", "title_bn": "পাকিস্তান সেনাবাহিনীর প্যারেডের ভিডিও বাংলাদেশ সেনাবাহিনীর বলে প্রচার", "false_claim_en": "Bangladesh Army parade — powerful display of military strength", "false_claim_bn": "বাংলাদেশ সেনাবাহিনীর কুচকাওয়াজ", "actual_origin_country": "Pakistan", "actual_origin_city": "Rawalpindi", "actual_origin_date": "2023-03-23", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["pakistan army parade", "rawalpindi", "bangladesh army claimed", "পাকিস্তান সেনাবাহিনী"]},
    {"title_en": "Karachi rain and flooding shared as Dhaka waterlogging", "title_bn": "করাচির বৃষ্টি ও বন্যার ভিডিও ঢাকার জলাবদ্ধতার বলে প্রচার", "false_claim_en": "Dhaka streets completely flooded after heavy rain", "false_claim_bn": "ভারী বৃষ্টির পর ঢাকার রাস্তা সম্পূর্ণ ডুবে গেছে", "actual_origin_country": "Pakistan", "actual_origin_city": "Karachi", "actual_origin_date": "2022-07-10", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["karachi rain", "flooding", "dhaka waterlogging", "করাচি", "ঢাকা জলাবদ্ধতা"]},
    {"title_en": "Pakistan police crackdown on PTI supporters shared as Bangladesh political violence", "title_bn": "পাকিস্তানে পিটিআই সমর্থকদের ওপর পুলিশের দমনের ভিডিও বাংলাদেশের বলে প্রচার", "false_claim_en": "Political activists being beaten by police in Bangladesh", "false_claim_bn": "বাংলাদেশে রাজনৈতিক কর্মীদের পুলিশ পিটাচ্ছে", "actual_origin_country": "Pakistan", "actual_origin_city": "Islamabad", "actual_origin_date": "2023-05-09", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["pakistan PTI", "police crackdown", "islamabad", "bangladesh claimed", "পাকিস্তান"]},
    {"title_en": "Geo News Pakistan broadcast shown as live Bangladesh news coverage", "title_bn": "পাকিস্তানের জিও নিউজের সম্প্রচার বাংলাদেশের সংবাদ বলে প্রচার", "false_claim_en": "Live news from Bangladesh showing current unrest", "false_claim_bn": "বাংলাদেশের লাইভ সংবাদ — দেশে চলমান অস্থিরতা", "actual_origin_country": "Pakistan", "actual_origin_city": "Karachi", "actual_origin_date": "2024-05-09", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["geo news", "pakistan", "bangladesh news claimed", "জিও নিউজ", "পাকিস্তান"]},
    {"title_en": "Lahore PTI rally footage shared as massive Dhaka protest", "title_bn": "লাহোরের পিটিআই র‍্যালির ভিডিও ঢাকার বিশাল বিক্ষোভ বলে প্রচার", "false_claim_en": "Millions in Dhaka streets — largest protest in Bangladesh history", "false_claim_bn": "ঢাকার রাস্তায় লক্ষ লক্ষ মানুষ", "actual_origin_country": "Pakistan", "actual_origin_city": "Lahore", "actual_origin_date": "2022-10-29", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["lahore rally", "PTI", "dhaka protest", "লাহোর", "পিটিআই", "ঢাকা"]},

    # CATEGORY 8: India footage
    {"title_en": "West Bengal election violence 2021 shared as Bangladesh political violence", "title_bn": "২০২১ সালে পশ্চিমবঙ্গের নির্বাচনী সহিংসতার ভিডিও বাংলাদেশের বলে প্রচার", "false_claim_en": "Political violence erupting in Bangladesh after election results", "false_claim_bn": "নির্বাচনের ফলাফলের পর বাংলাদেশে রাজনৈতিক সহিংসতা", "actual_origin_country": "India", "actual_origin_city": "West Bengal", "actual_origin_date": "2021-05-02", "debunk_source": "boom_live", "debunk_url": "https://boomlive.in", "keywords": ["west bengal", "election violence", "2021", "bangladesh claimed", "পশ্চিমবঙ্গ"]},
    {"title_en": "Manipur violence footage (2023) shared as Hindu persecution in Bangladesh", "title_bn": "মণিপুরের সহিংসতার ভিডিও বাংলাদেশে হিন্দু নির্যাতনের বলে প্রচার", "false_claim_en": "Hindus being persecuted and attacked in Bangladesh", "false_claim_bn": "বাংলাদেশে হিন্দুদের নির্যাতন ও আক্রমণ", "actual_origin_country": "India", "actual_origin_city": "Manipur", "actual_origin_date": "2023-05-04", "debunk_source": "afp_factcheck", "debunk_url": "https://factcheck.afp.com", "keywords": ["manipur", "india", "hindu persecution", "bangladesh claimed", "মণিপুর", "হিন্দু নির্যাতন"]},
    {"title_en": "India farmer protest 2021 footage shared as Bangladesh movement", "title_bn": "ভারতের কৃষক আন্দোলনের ভিডিও বাংলাদেশের আন্দোলন বলে প্রচার", "false_claim_en": "Massive farmer protest in Bangladesh demanding agricultural rights", "false_claim_bn": "বাংলাদেশে কৃষকদের বিশাল আন্দোলন", "actual_origin_country": "India", "actual_origin_city": "Delhi", "actual_origin_date": "2021-01-26", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["india farmer protest", "2021", "delhi", "bangladesh claimed", "কৃষক আন্দোলন"]},
    {"title_en": "India bulldozer demolition footage shared as Bangladesh government demolishing homes", "title_bn": "ভারতের বুলডোজার দিয়ে ভাঙনের ভিডিও বাংলাদেশ সরকারের ঘর ভাঙার বলে প্রচার", "false_claim_en": "Bangladesh government demolishing homes of opposition activists", "false_claim_bn": "বাংলাদেশ সরকার বিরোধী কর্মীদের বাড়ি বুলডোজার দিয়ে গুঁড়িয়ে দিচ্ছে", "actual_origin_country": "India", "actual_origin_city": "Uttar Pradesh", "actual_origin_date": "2022-06-12", "debunk_source": "alt_news", "debunk_url": "https://altnews.in", "keywords": ["india bulldozer", "demolition", "UP", "bangladesh opposition", "বুলডোজার", "ভারত"]},

    # CATEGORY 9: Other countries
    {"title_en": "Sri Lanka economic crisis protest (2022) shared as Bangladesh crisis", "title_bn": "শ্রীলঙ্কার অর্থনৈতিক সংকটের বিক্ষোভের ভিডিও বাংলাদেশের বলে প্রচার", "false_claim_en": "Bangladesh facing economic collapse — people storming government buildings", "false_claim_bn": "বাংলাদেশে অর্থনৈতিক ধস — জনগণ সরকারি ভবনে হামলা", "actual_origin_country": "Sri Lanka", "actual_origin_city": "Colombo", "actual_origin_date": "2022-07-09", "debunk_source": "afp_factcheck", "debunk_url": "https://factcheck.afp.com", "keywords": ["sri lanka", "economic crisis", "2022", "bangladesh crisis claimed", "শ্রীলঙ্কা", "অর্থনৈতিক সংকট"]},
    {"title_en": "Nepal earthquake footage shared as Bangladesh disaster", "title_bn": "নেপালের ভূমিকম্পের ভিডিও বাংলাদেশের দুর্যোগ বলে প্রচার", "false_claim_en": "Powerful earthquake strikes Bangladesh — buildings collapsing", "false_claim_bn": "বাংলাদেশে শক্তিশালী ভূমিকম্প — ভবন ধ্বসে পড়ছে", "actual_origin_country": "Nepal", "actual_origin_city": "Kathmandu", "actual_origin_date": "2015-04-25", "debunk_source": "afp_factcheck", "debunk_url": "https://factcheck.afp.com", "keywords": ["nepal earthquake", "2015", "bangladesh disaster", "নেপাল", "ভূমিকম্প"]},

    # CATEGORY 10: Historical misinfo
    {"title_en": "Rana Plaza collapse footage (2013) recycled as new factory building collapse", "title_bn": "রানা প্লাজা ধসের ভিডিও নতুন কারখানা ধসের বলে প্রচার", "false_claim_en": "Another garment factory building has collapsed in Bangladesh today", "false_claim_bn": "আজ বাংলাদেশে আরেকটি গার্মেন্টস কারখানার ভবন ধসে পড়েছে", "actual_origin_country": "Bangladesh", "actual_origin_city": "Savar, Dhaka", "actual_origin_date": "2013-04-24", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["rana plaza", "2013", "savar", "factory collapse", "রানা প্লাজা", "সাভার"]},
    {"title_en": "Old Dhaka fire footage recycled as new fire disaster", "title_bn": "পুরনো ঢাকার আগুনের ভিডিও নতুন অগ্নিকাণ্ড বলে প্রচার", "false_claim_en": "Massive fire in Dhaka today — hundreds trapped", "false_claim_bn": "আজ ঢাকায় ভয়াবহ অগ্নিকাণ্ড — শত শত আটকা", "actual_origin_country": "Bangladesh", "actual_origin_city": "Dhaka", "actual_origin_date": "2019-02-20", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com/fire", "keywords": ["dhaka fire", "2019", "chawkbazar", "recycled", "পুরান ঢাকা", "আগুন", "চকবাজার"]},
    {"title_en": "Old Bangladesh election violence footage recycled as recent political clashes", "title_bn": "পুরনো বাংলাদেশের নির্বাচনী সহিংসতার ভিডিও সাম্প্রতিক রাজনৈতিক সংঘর্ষ বলে প্রচার", "false_claim_en": "Political violence erupting across Bangladesh — clashes between parties", "false_claim_bn": "বাংলাদেশজুড়ে রাজনৈতিক সহিংসতা", "actual_origin_country": "Bangladesh", "actual_origin_city": "Dhaka", "actual_origin_date": "2018-12-30", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["election violence", "2018", "recycled", "political clash", "নির্বাচনী সহিংসতা"]},
    {"title_en": "India river erosion footage shared as Bangladesh river erosion crisis", "title_bn": "ভারতের নদী ভাঙনের ভিডিও বাংলাদেশের নদী ভাঙন বলে প্রচার", "false_claim_en": "Severe riverbank erosion destroying villages in Bangladesh", "false_claim_bn": "বাংলাদেশে তীব্র নদী ভাঙনে গ্রাম ধ্বংস", "actual_origin_country": "India", "actual_origin_city": "Assam", "actual_origin_date": "2020-07-15", "debunk_source": "boom_live", "debunk_url": "https://boomlive.in", "keywords": ["india river erosion", "assam", "bangladesh erosion", "আসাম", "নদী ভাঙন"]},

    # CATEGORY 11: Political misinfo
    {"title_en": "Fake video of BNP-Jamaat attacking Awami League office", "title_bn": "বিএনপি-জামায়াতের আওয়ামী লীগ অফিসে হামলার ভুয়া ভিডিও", "false_claim_en": "BNP-Jamaat cadres attacking Awami League offices across Bangladesh", "false_claim_bn": "বিএনপি-জামায়াত ক্যাডাররা আওয়ামী লীগ অফিসে হামলা", "actual_origin_country": "Bangladesh", "actual_origin_city": "Dhaka", "actual_origin_date": "2023-10-28", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["BNP jamaat", "awami league", "attack", "2023", "বিএনপি", "আওয়ামী লীগ"]},
    {"title_en": "Deepfake video of Sheikh Hasina making false statements", "title_bn": "শেখ হাসিনার ডিপফেক ভিডিও — মিথ্যা বক্তব্য বানোয়াট", "false_claim_en": "Sheikh Hasina admits to rigging elections in leaked video", "false_claim_bn": "শেখ হাসিনা নির্বাচনে কারচুপির কথা স্বীকার করেছেন", "actual_origin_country": "Bangladesh", "actual_origin_city": "Dhaka", "actual_origin_date": "2024-01-07", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["deepfake", "hasina", "election rigging", "fake video", "ডিপফেক", "হাসিনা"]},
    {"title_en": "Fake footage of Bangladesh army arresting politicians post-August 2024", "title_bn": "আগস্ট ২০২৪-পরবর্তী রাজনীতিবিদ গ্রেপ্তারের ভুয়া ভিডিও", "false_claim_en": "Bangladesh Army arresting senior Awami League leaders nationwide", "false_claim_bn": "বাংলাদেশ সেনাবাহিনী দেশজুড়ে আওয়ামী লীগের শীর্ষ নেতাদের গ্রেপ্তার", "actual_origin_country": "Pakistan", "actual_origin_city": "Islamabad", "actual_origin_date": "2023-11-04", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["army arrest", "awami league", "bangladesh army", "পাকিস্তান", "গ্রেপ্তার"]},

    # CATEGORY 12: Mob violence
    {"title_en": "India lynching mob footage shared as Bangladesh mob violence", "title_bn": "ভারতের গণপিটুনির ভিডিও বাংলাদেশের মব ভায়োলেন্সের বলে প্রচার", "false_claim_en": "Mob lynching happening in Bangladesh — innocent people being attacked", "false_claim_bn": "বাংলাদেশে গণপিটুনি — নির্দোষ মানুষ আক্রান্ত", "actual_origin_country": "India", "actual_origin_city": "Uttar Pradesh", "actual_origin_date": "2023-06-18", "debunk_source": "alt_news", "debunk_url": "https://altnews.in", "keywords": ["india lynching", "mob violence", "UP", "bangladesh mob", "গণপিটুনি", "মব"]},
    {"title_en": "Pakistan mob violence against minorities shared as Bangladesh communal attack", "title_bn": "পাকিস্তানে সংখ্যালঘুদের ওপর মব হামলার ভিডিও বাংলাদেশের সাম্প্রদায়িক হামলার বলে প্রচার", "false_claim_en": "Communal mob attacking minority community in Bangladesh", "false_claim_bn": "বাংলাদেশে সাম্প্রদায়িক মব সংখ্যালঘু সম্প্রদায়ের ওপর হামলা", "actual_origin_country": "Pakistan", "actual_origin_city": "Faisalabad", "actual_origin_date": "2023-08-16", "debunk_source": "afp_factcheck", "debunk_url": "https://factcheck.afp.com", "keywords": ["pakistan mob", "minority attack", "faisalabad", "bangladesh communal", "সাম্প্রদায়িক হামলা"]},
    {"title_en": "Bangladesh mob beating suspect — viral video with wrong crime allegation", "title_bn": "বাংলাদেশে মব পিটুনির ভাইরাল ভিডিও — ভুল অপরাধের অভিযোগে", "false_claim_en": "Man beaten to death by mob for child kidnapping in Bangladesh — wrong person", "false_claim_bn": "শিশু অপহরণের অভিযোগে মব পিটুনিতে নিহত — ভুল মানুষ", "actual_origin_country": "Bangladesh", "actual_origin_city": "Dhaka", "actual_origin_date": "2019-07-20", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["mob beating", "child kidnapping rumor", "2019", "গণপিটুনি", "শিশু অপহরণ", "গুজব"]},

    # CATEGORY 13: Recent incidents
    {"title_en": "Gaza Palestine war footage (2023) shared as Bangladesh sectarian violence", "title_bn": "গাজার যুদ্ধের ভিডিও বাংলাদেশের সাম্প্রদায়িক সহিংসতার বলে প্রচার", "false_claim_en": "Sectarian war breaking out in Bangladesh — people fleeing cities", "false_claim_bn": "বাংলাদেশে সাম্প্রদায়িক যুদ্ধ শুরু", "actual_origin_country": "Palestine", "actual_origin_city": "Gaza", "actual_origin_date": "2023-10-08", "debunk_source": "afp_factcheck", "debunk_url": "https://factcheck.afp.com", "keywords": ["gaza war", "2023", "sectarian bangladesh", "গাজা", "যুদ্ধ", "সাম্প্রদায়িক"]},
    {"title_en": "Ukraine war footage shared as Bangladesh border conflict", "title_bn": "ইউক্রেন যুদ্ধের ভিডিও বাংলাদেশের সীমান্ত সংঘর্ষের বলে প্রচার", "false_claim_en": "Armed conflict breaking out on Bangladesh border", "false_claim_bn": "বাংলাদেশের সীমান্তে সশস্ত্র সংঘর্ষ", "actual_origin_country": "Ukraine", "actual_origin_city": "Donbas", "actual_origin_date": "2022-02-25", "debunk_source": "afp_factcheck", "debunk_url": "https://factcheck.afp.com", "keywords": ["ukraine war", "border conflict", "bangladesh claimed", "ইউক্রেন", "যুদ্ধ"]},
    {"title_en": "Indonesia earthquake rescue footage shared as Bangladesh cyclone rescue", "title_bn": "ইন্দোনেশিয়ার ভূমিকম্পের উদ্ধার ভিডিও বাংলাদেশের ঘূর্ণিঝড়ের বলে প্রচার", "false_claim_en": "Cyclone rescue operations in Bangladesh — villages destroyed", "false_claim_bn": "বাংলাদেশে ঘূর্ণিঝড়ে উদ্ধার অভিযান", "actual_origin_country": "Indonesia", "actual_origin_city": "Cianjur", "actual_origin_date": "2022-11-21", "debunk_source": "afp_factcheck", "debunk_url": "https://factcheck.afp.com", "keywords": ["indonesia earthquake", "cyclone bangladesh", "ইন্দোনেশিয়া", "ঘূর্ণিঝড়"]},
    {"title_en": "Turkey earthquake footage (2023) shared as Bangladesh building collapse", "title_bn": "তুরস্কের ভূমিকম্পের ভিডিও বাংলাদেশের ভবন ধসের বলে প্রচার", "false_claim_en": "Building collapse in Bangladesh — people trapped under rubble", "false_claim_bn": "বাংলাদেশে ভবন ধস — মানুষ ধ্বংসস্তূপের নিচে আটকা", "actual_origin_country": "Turkey", "actual_origin_city": "Hatay", "actual_origin_date": "2023-02-06", "debunk_source": "afp_factcheck", "debunk_url": "https://factcheck.afp.com", "keywords": ["turkey earthquake", "2023", "hatay", "building collapse bangladesh", "তুরস্ক", "ভূমিকম্প"]},
    {"title_en": "Old Bangladesh Padma Bridge protest footage recycled as recent demonstration", "title_bn": "পদ্মা সেতুর বিরোধিতার পুরনো ভিডিও সাম্প্রতিক বিক্ষোভ বলে প্রচার", "false_claim_en": "Mass protests against corruption in Bangladesh breaking out today", "false_claim_bn": "আজ বাংলাদেশে দুর্নীতিবিরোধী গণআন্দোলন শুরু", "actual_origin_country": "Bangladesh", "actual_origin_city": "Dhaka", "actual_origin_date": "2012-08-26", "debunk_source": "rumour_scanner", "debunk_url": "https://rumourscanner.com", "keywords": ["padma bridge", "protest", "2012", "recycled", "পদ্মা সেতু", "বিক্ষোভ"]},
]


def parse_date(s):
    y, m, d = s.split("-")
    return date(int(y), int(m), int(d))


def build_search_text(inc: dict) -> str:
    parts = [
        inc.get("title_en", ""),
        inc.get("title_bn", ""),
        inc.get("false_claim_en", ""),
        inc.get("false_claim_bn", ""),
        inc.get("actual_origin_country", ""),
        inc.get("actual_origin_city", ""),
        " ".join(inc.get("keywords", [])),
    ]
    return " ".join(p for p in parts if p)


def main():
    from sentence_transformers import SentenceTransformer
    logger.info("Loading embedding model...")
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    logger.info("Model loaded.")

    db = SessionLocal()
    inserted = 0
    updated = 0

    try:
        for inc in INCIDENTS:
            existing = db.query(KnownCase).filter(
                KnownCase.title_en == inc["title_en"]
            ).first()

            search_text = build_search_text(inc)
            embedding = model.encode(search_text, normalize_embeddings=True).tolist()
            origin_date = parse_date(inc["actual_origin_date"]) if inc.get("actual_origin_date") else None

            if existing:
                existing.text_embedding = embedding
                # Update tsvector
                db.execute(text("""
                    UPDATE known_cases SET search_vector =
                        to_tsvector('simple', :txt)
                    WHERE id = :id
                """), {"txt": search_text, "id": existing.id})
                updated += 1
                logger.info("Updated: %s", inc["title_en"][:60])
            else:
                case = KnownCase(
                    title_en=inc["title_en"],
                    title_bn=inc.get("title_bn"),
                    false_claim_en=inc.get("false_claim_en"),
                    false_claim_bn=inc.get("false_claim_bn"),
                    actual_origin_country=inc.get("actual_origin_country"),
                    actual_origin_city=inc.get("actual_origin_city"),
                    actual_origin_date=origin_date,
                    debunk_source=inc.get("debunk_source"),
                    debunk_url=inc.get("debunk_url"),
                    keywords=inc.get("keywords", []),
                    text_embedding=embedding,
                )
                db.add(case)
                db.flush()
                db.execute(text("""
                    UPDATE known_cases SET search_vector =
                        to_tsvector('simple', :txt)
                    WHERE id = :id
                """), {"txt": search_text, "id": case.id})
                inserted += 1
                logger.info("Inserted: %s", inc["title_en"][:60])

        db.commit()
        logger.info("Done. Inserted=%d Updated=%d", inserted, updated)

        total = db.execute(text("SELECT COUNT(*) FROM known_cases")).scalar()
        logger.info("Total known_cases in DB: %d", total)

    finally:
        db.close()


if __name__ == "__main__":
    main()
