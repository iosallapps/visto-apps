#!/usr/bin/env python3
"""Privacy Policy + Terms generator for Visto Apps app sites (EN + RO).

One facts file per app (tools/legal/apps/<slug>.json) lists what the app's
code really does: services, permissions, local data, purchases, disclaimers.
Every fact in that file must point at the code it came from ("src" fields).
This module turns the facts into the same, complete set of sections for every
app, so the 12 sites stay consistent and a claim can only appear if the facts
file says the code does it.

    python3 tools/legal/legal.py apps/topoxy.json > out.json

Output: {"privacy": [section...], "terms": [section...]} where a section is
{"id", "en": {"h", "html"}, "ro": {"h", "html"}}. Each site renders the
sections with its own markup (data-en/data-ro, /ro/ pages, Next.js...).
"""
import html
import json
import sys
from pathlib import Path

CONTROLLER = {
    "en": "Visto Apps is the brand of Darius Cirjan, the developer and data controller.",
    "ro": "Visto Apps este marca lui Darius Cirjan, dezvoltatorul și operatorul de date.",
}
EMAIL = "iosallapps@gmail.com"
STUDIO = "https://vistoapps.com"

# Legal bases (GDPR art. 6(1)).
BASIS = {
    "consent": {"en": "Consent, art. 6(1)(a) GDPR (and art. 5(3) ePrivacy for device storage)",
                "ro": "Consimțământ, art. 6 alin. (1) lit. a GDPR (și art. 5 alin. (3) ePrivacy pentru stocarea pe dispozitiv)"},
    "contract": {"en": "Performance of a contract, art. 6(1)(b) GDPR: needed for the feature you use",
                 "ro": "Executarea unui contract, art. 6 alin. (1) lit. b GDPR: necesar pentru funcția pe care o folosești"},
    "legit": {"en": "Legitimate interest, art. 6(1)(f) GDPR",
              "ro": "Interes legitim, art. 6 alin. (1) lit. f GDPR"},
    "legal": {"en": "Legal obligation, art. 6(1)(c) GDPR",
              "ro": "Obligație legală, art. 6 alin. (1) lit. c GDPR"},
    "explicit": {"en": "Explicit consent, art. 9(2)(a) GDPR, given in the app",
                 "ro": "Consimțământ explicit, art. 9 alin. (2) lit. a GDPR, dat în aplicație"},
    "none": {"en": "No personal data reaches us", "ro": "Nu ajung la noi date personale"},
}

# Third-party services. Text states what the SDK or API receives, not what we
# wish it received. App-specific details go in the facts file ("note").
SERVICES = {
    "admob": {
        "name": "Google AdMob", "who": "Google Ireland Ltd / Google LLC",
        "link": "https://policies.google.com/technologies/ads",
        "en": {"data": "Advertising identifier (IDFA on iOS only if you allow tracking; Android advertising ID), IP address, device and app information, ad impressions and taps.",
               "why": "Showing ads in the free version. Personalised ads only with your consent; otherwise limited, non-personalised ads."},
        "ro": {"data": "Identificatorul de publicitate (IDFA pe iOS doar dacă permiți urmărirea; ID-ul de publicitate Android), adresa IP, informații despre dispozitiv și aplicație, afișări și atingeri ale reclamelor.",
               "why": "Afișarea reclamelor în versiunea gratuită. Reclame personalizate doar cu acordul tău; altfel reclame limitate, nepersonalizate."},
        "basis": ["consent", "legit"],
        "basis_text": {"en": "Personalised ads: consent, art. 6(1)(a) GDPR and art. 5(3) ePrivacy. Limited ads: legitimate interest in funding the free app, art. 6(1)(f) GDPR.",
                       "ro": "Reclame personalizate: consimțământ, art. 6 alin. (1) lit. a GDPR și art. 5 alin. (3) ePrivacy. Reclame limitate: interes legitim de a finanța aplicația gratuită, art. 6 alin. (1) lit. f GDPR."},
        "ret": {"en": "Set by Google (see its policy).", "ro": "Stabilită de Google (vezi politica sa)."},
        "transfer": True,
    },
    "ump": {
        "name": "Google User Messaging Platform", "who": "Google Ireland Ltd / Google LLC",
        "link": "https://policies.google.com/privacy",
        "en": {"data": "Your consent choices (IAB TCF string), stored on the device; device information needed to show the form.",
               "why": "Asking for and recording your consent in the EEA, UK and Switzerland."},
        "ro": {"data": "Alegerile tale de consimțământ (șirul IAB TCF), păstrate pe dispozitiv; informații despre dispozitiv necesare afișării formularului.",
               "why": "Cererea și înregistrarea consimțământului tău în SEE, Regatul Unit și Elveția."},
        "basis": ["legal"],
        "ret": {"en": "On your device until you change it or delete the app.", "ro": "Pe dispozitiv, până o schimbi sau ștergi aplicația."},
        "transfer": True,
    },
    "firebase_analytics": {
        "name": "Google Analytics for Firebase", "who": "Google Ireland Ltd / Google LLC",
        "link": "https://firebase.google.com/support/privacy",
        "en": {"data": "A random app instance ID, events such as screens opened, features used and purchases started, app version, device model, OS, language, country derived from the IP address.",
               "why": "Understanding which features are used so we can improve the app. No name, email or content you create is sent."},
        "ro": {"data": "Un ID aleatoriu al instalării, evenimente precum ecrane deschise, funcții folosite și achiziții începute, versiunea aplicației, modelul dispozitivului, sistemul, limba, țara dedusă din adresa IP.",
               "why": "Înțelegerea funcțiilor folosite, ca să îmbunătățim aplicația. Nu trimitem nume, email sau conținutul creat de tine."},
        "basis": ["consent", "legit"],
        "basis_text": {"en": "EEA, UK and Switzerland: consent given in the consent form, art. 6(1)(a) GDPR. Elsewhere: legitimate interest in improving the app, art. 6(1)(f) GDPR.",
                       "ro": "SEE, Regatul Unit și Elveția: consimțământul dat în formular, art. 6 alin. (1) lit. a GDPR. În rest: interes legitim de a îmbunătăți aplicația, art. 6 alin. (1) lit. f GDPR."},
        "ret": {"en": "At most 14 months for event data.", "ro": "Cel mult 14 luni pentru datele de evenimente."},
        "transfer": True,
    },
    "crashlytics": {
        "name": "Firebase Crashlytics", "who": "Google Ireland Ltd / Google LLC",
        "link": "https://firebase.google.com/support/privacy",
        "en": {"data": "Crash reports: stack trace, device model, OS and app version, a random installation ID.",
               "why": "Finding and fixing crashes."},
        "ro": {"data": "Rapoarte de erori: stiva apelurilor, modelul dispozitivului, versiunea sistemului și a aplicației, un ID aleatoriu al instalării.",
               "why": "Găsirea și repararea erorilor."},
        "basis": ["legit"],
        "ret": {"en": "90 days.", "ro": "90 de zile."},
        "transfer": True,
    },
    "revenuecat": {
        "name": "RevenueCat", "who": "RevenueCat, Inc. (USA)",
        "link": "https://www.revenuecat.com/privacy",
        "en": {"data": "A random customer ID, purchase receipts and subscription status from the store, app version and country.",
               "why": "Checking which purchases you own and unlocking them, including on restore."},
        "ro": {"data": "Un ID aleatoriu de client, chitanțele achizițiilor și starea abonamentului din magazin, versiunea aplicației și țara.",
               "why": "Verificarea achizițiilor pe care le deții și deblocarea lor, inclusiv la restaurare."},
        "basis": ["contract"],
        "ret": {"en": "While you use the app, then deleted on request.", "ro": "Cât timp folosești aplicația, apoi ștearsă la cerere."},
        "transfer": True,
    },
    "apple_store": {
        "name": "Apple App Store", "who": "Apple Distribution International Ltd",
        "link": "https://www.apple.com/legal/privacy/",
        "en": {"data": "Your Apple Account, payment details and purchase history. We never see your payment details.",
               "why": "Selling and renewing purchases, refunds."},
        "ro": {"data": "Contul Apple, datele de plată și istoricul achizițiilor. Nu vedem niciodată datele tale de plată.",
               "why": "Vânzarea și reînnoirea achizițiilor, rambursări."},
        "basis": ["contract"],
        "ret": {"en": "Set by Apple.", "ro": "Stabilită de Apple."},
        "transfer": False,
    },
    "google_play": {
        "name": "Google Play Billing", "who": "Google Ireland Ltd / Google LLC",
        "link": "https://policies.google.com/privacy",
        "en": {"data": "Your Google account, payment details and purchase history. We never see your payment details.",
               "why": "Selling and renewing purchases, refunds."},
        "ro": {"data": "Contul Google, datele de plată și istoricul achizițiilor. Nu vedem niciodată datele tale de plată.",
               "why": "Vânzarea și reînnoirea achizițiilor, rambursări."},
        "basis": ["contract"],
        "ret": {"en": "Set by Google.", "ro": "Stabilită de Google."},
        "transfer": True,
    },
    "mapbox_terrain": {
        "name": "Mapbox (elevation)", "who": "Mapbox, Inc. (USA)",
        "link": "https://www.mapbox.com/legal/privacy",
        "en": {"data": "The map tile around the point you ask about (about 1 km wide, which reveals that area), your IP address and device information.",
               "why": "Reading the elevation for slope and terrain tools."},
        "ro": {"data": "Dala de hartă din jurul punctului cerut (aproximativ 1 km lățime, deci zona respectivă), adresa IP și informații despre dispozitiv.",
               "why": "Citirea altitudinii pentru instrumentele de pantă și teren."},
        "basis": ["contract"],
        "ret": {"en": "Set by Mapbox.", "ro": "Stabilită de Mapbox."},
        "transfer": True,
    },
    "apple_maps": {
        "name": "Apple Maps (MapKit)", "who": "Apple Inc.",
        "link": "https://www.apple.com/legal/privacy/data/en/apple-maps/",
        "en": {"data": "The map area you look at, your IP address. Apple does not link it to your Apple Account.",
               "why": "Drawing the standard and satellite map on iOS."},
        "ro": {"data": "Zona de hartă pe care o privești, adresa IP. Apple nu o asociază contului tău Apple.",
               "why": "Afișarea hărții standard și din satelit pe iOS."},
        "basis": ["contract"],
        "ret": {"en": "Set by Apple.", "ro": "Stabilită de Apple."},
        "transfer": False,
    },
    "osm_tiles": {
        "name": "OpenStreetMap tiles", "who": "OpenStreetMap Foundation (UK)",
        "link": "https://osmfoundation.org/wiki/Privacy_Policy",
        "en": {"data": "The map area you look at, your IP address and the app name.",
               "why": "Drawing the standard map on Android."},
        "ro": {"data": "Zona de hartă pe care o privești, adresa IP și numele aplicației.",
               "why": "Afișarea hărții standard pe Android."},
        "basis": ["contract"],
        "ret": {"en": "Set by the OpenStreetMap Foundation.", "ro": "Stabilită de OpenStreetMap Foundation."},
        "transfer": False,
    },
    "esri_tiles": {
        "name": "Esri World Imagery", "who": "Esri, Inc. (USA)",
        "link": "https://www.esri.com/en-us/privacy/overview",
        "en": {"data": "The map area you look at and your IP address.",
               "why": "Drawing satellite imagery and place labels on Android."},
        "ro": {"data": "Zona de hartă pe care o privești și adresa IP.",
               "why": "Afișarea imaginilor din satelit și a denumirilor pe Android."},
        "basis": ["contract"],
        "ret": {"en": "Set by Esri.", "ro": "Stabilită de Esri."},
        "transfer": True,
    },
    "cloudkit": {
        "name": "Apple iCloud (CloudKit)", "who": "Apple Inc.",
        "link": "https://www.apple.com/legal/privacy/",
        "en": {"data": "The app data you choose to sync, stored in your own iCloud account. We cannot read it.",
               "why": "Syncing and backing up your data across your devices."},
        "ro": {"data": "Datele aplicației pe care alegi să le sincronizezi, în propriul cont iCloud. Noi nu le putem citi.",
               "why": "Sincronizarea și copia de siguranță între dispozitivele tale."},
        "basis": ["contract"],
        "ret": {"en": "Until you delete it from iCloud.", "ro": "Până o ștergi din iCloud."},
        "transfer": False,
    },
}

PERMISSIONS = {
    "location": {
        "en": ("Location (while using the app)", "To show and convert your current position. Read on the device only; it is sent to a service only when you use a feature that needs it (listed above)."),
        "ro": ("Localizare (în timpul folosirii)", "Pentru afișarea și conversia poziției curente. Se citește doar pe dispozitiv; ajunge la un serviciu doar când folosești o funcție care o cere (listată mai sus)."),
    },
    "notifications": {
        "en": ("Notifications", "Local reminders scheduled on the device. No push server is involved."),
        "ro": ("Notificări", "Mementouri locale programate pe dispozitiv. Nu există server de notificări."),
    },
    "files": {
        "en": ("Files you pick", "Only the file you choose to import is read, on the device."),
        "ro": ("Fișierele alese", "Se citește doar fișierul pe care alegi să-l imporți, pe dispozitiv."),
    },
    "tracking": {
        "en": ("Tracking (iOS, App Tracking Transparency)", "Asked once, after the consent form. If you choose Ask App Not to Track, the IDFA is not shared and ads are not personalised with it."),
        "ro": ("Urmărire (iOS, App Tracking Transparency)", "Cerută o singură dată, după formularul de consimțământ. Dacă alegi Cere aplicației să nu urmărească, IDFA nu este partajat și reclamele nu sunt personalizate cu el."),
    },
    "ad_id": {
        "en": ("Advertising ID (Android)", "Used by AdMob only as your consent allows. You can delete or reset it in Android Settings, Privacy, Ads."),
        "ro": ("ID de publicitate (Android)", "Folosit de AdMob doar în limita consimțământului. Îl poți șterge sau reseta în Setări Android, Confidențialitate, Reclame."),
    },
}

STR = {
    "en": {
        "updated": "Last updated", "effective": "Effective",
        "service": "Service", "data": "Data", "purpose": "Purpose", "basis": "Legal basis", "ret": "Retention",
        "privacy_of": "Privacy policy",
    },
    "ro": {
        "updated": "Ultima actualizare", "effective": "În vigoare din",
        "service": "Serviciu", "data": "Date", "purpose": "Scop", "basis": "Temei legal", "ret": "Păstrare",
        "privacy_of": "Politica de confidențialitate",
    },
}

MONTHS_RO = ["ianuarie", "februarie", "martie", "aprilie", "mai", "iunie", "iulie",
             "august", "septembrie", "octombrie", "noiembrie", "decembrie"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"]


def fmt_date(iso, lang):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{MONTHS_EN[m-1]} {d}, {y}" if lang == "en" else f"{d} {MONTHS_RO[m-1]} {y}"


def e(s):
    return html.escape(s, quote=False)


def mail(lang=None):
    return f'<a href="mailto:{EMAIL}">{EMAIL}</a>'


def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def p(*parts):
    return "".join(f"<p>{x}</p>" for x in parts)


def link(url, text=None):
    return f'<a href="{url}" rel="noopener">{text or url.replace("https://", "")}</a>'


class Ctx:
    def __init__(self, facts):
        self.f = facts
        self.name = facts["name"]
        self.ios = "ios" in facts["platforms"]
        self.android = "android" in facts["platforms"]
        self.services = facts["services"]
        self.ads = "admob" in self.services
        self.analytics = "firebase_analytics" in self.services
        self.paid = bool(facts.get("purchases"))
        self.site = facts["site"]

    def t(self, key, lang):
        v = self.f[key]
        return v[lang] if isinstance(v, dict) else v

    def store(self, lang):
        if self.ios and self.android:
            return {"en": "the App Store or Google Play", "ro": "App Store sau Google Play"}[lang]
        if self.android:
            return "Google Play"
        return "App Store"


def S(id_, en_h, en_html, ro_h, ro_html):
    return {"id": id_, "en": {"h": en_h, "html": en_html}, "ro": {"h": ro_h, "html": ro_html}}


# ---------------------------------------------------------------- privacy

def privacy(c):
    f, n = c.f, c.name
    out = []
    up = f["updated"]
    out.append(S("intro", "Who we are",
        p(f"{CONTROLLER['en']} This policy explains what the {n} app ({c.platform_list('en')}) and the website {c.site} do with personal data.",
          f"Contact for any privacy question or request: {mail()}. Website: {link(STUDIO)}. We answer within one month (art. 12 GDPR). We are not required to appoint a Data Protection Officer.",
          f"{STR['en']['updated']}: {fmt_date(up, 'en')}."),
        "Cine suntem",
        p(f"{CONTROLLER['ro']} Această politică explică ce fac aplicația {n} ({c.platform_list('ro')}) și site-ul {c.site} cu datele personale.",
          f"Contact pentru orice întrebare sau cerere privind datele: {mail()}. Site: {link(STUDIO)}. Răspundem în cel mult o lună (art. 12 GDPR). Nu avem obligația de a numi un responsabil cu protecția datelor.",
          f"{STR['ro']['updated']}: {fmt_date(up, 'ro')}.")))

    glance_en = [f"No account. {n} does not ask for your name, email or phone number.",
                 c.t("local_data", "en")]
    glance_ro = [f"Fără cont. {n} nu îți cere numele, emailul sau telefonul.",
                 c.t("local_data", "ro")]
    if c.ads:
        glance_en.append("The free version shows ads from Google AdMob. Personalised ads only with your consent; in the EEA, UK and Switzerland no ad loads before you answer the consent form.")
        glance_ro.append("Versiunea gratuită afișează reclame Google AdMob. Reclame personalizate doar cu acordul tău; în SEE, Regatul Unit și Elveția nicio reclamă nu se încarcă înainte să răspunzi la formularul de consimțământ.")
    if c.analytics:
        glance_en.append("Usage statistics (Google Analytics for Firebase) start only after the consent form has been answered in the EEA, UK and Switzerland. Crash reports help us fix bugs.")
        glance_ro.append("Statisticile de utilizare (Google Analytics for Firebase) pornesc în SEE, Regatul Unit și Elveția doar după ce ai răspuns la formularul de consimțământ. Rapoartele de erori ne ajută să reparăm problemele.")
    glance_en.append("We do not sell personal data for money. We have no servers of our own that receive your data.")
    glance_ro.append("Nu vindem date personale pe bani. Nu avem servere proprii care să primească datele tale.")
    out.append(S("glance", "At a glance", ul(glance_en), "Pe scurt", ul(glance_ro)))

    out.append(S("local", "Data that stays on your device",
        p(c.t("local_detail", "en")),
        "Date care rămân pe dispozitiv",
        p(c.t("local_detail", "ro"))))

    out.append(S("services", "Services that receive data",
        p("Each service below receives data only when the part of the app that uses it runs. Google, Apple, RevenueCat and the other providers act as independent controllers or as our processors, under their own terms.")
        + c.services_table("en") + c.notes("en"),
        "Servicii care primesc date",
        p("Fiecare serviciu de mai jos primește date doar când rulează partea aplicației care îl folosește. Google, Apple, RevenueCat și ceilalți furnizori acționează ca operatori independenți sau ca persoane împuternicite de noi, conform propriilor condiții.")
        + c.services_table("ro") + c.notes("ro")))

    out.append(S("permissions", "Permissions",
        p("The app asks for these permissions only when you use the feature, and works without them. Change them anytime in your device settings.") + c.perm_list("en"),
        "Permisiuni",
        p("Aplicația cere aceste permisiuni doar când folosești funcția și merge și fără ele. Le poți schimba oricând din setările dispozitivului.") + c.perm_list("ro")))

    if c.ads or c.analytics:
        out.append(S("consent", "Consent, ads and tracking", c.consent("en"),
                     "Consimțământ, reclame și urmărire", c.consent("ro")))

    if c.paid:
        out.append(S("purchases", "Purchases",
            p(f"Purchases are made through {c.store('en')}. The store processes the payment; we receive only a pseudonymous receipt" + (", checked through RevenueCat," if "revenuecat" in c.services else "") + " that tells the app which purchase you own. We never see your card or account details."),
            "Achiziții",
            p(f"Achizițiile se fac prin {c.store('ro')}. Magazinul procesează plata; noi primim doar o chitanță pseudonimă" + (", verificată prin RevenueCat," if "revenuecat" in c.services else "") + " care spune aplicației ce ai cumpărat. Nu vedem niciodată datele cardului sau ale contului tău.")))

    out.append(S("retention", "How long data is kept",
        p("Data on your device stays until you delete it in the app or delete the app. Data held by the services above is kept for the period listed in the table. We do not keep copies of our own. Emails you send us are kept as long as needed to answer, and at most 2 years."),
        "Cât timp păstrăm datele",
        p("Datele de pe dispozitiv rămân până le ștergi din aplicație sau ștergi aplicația. Datele aflate la serviciile de mai sus se păstrează cât scrie în tabel. Nu păstrăm copii proprii. Emailurile trimise nouă se păstrează cât e nevoie pentru răspuns, cel mult 2 ani.")))

    out.append(S("transfers", "Transfers outside the EEA",
        p("Some providers (Google, RevenueCat and others marked in the table) process data in the United States or other countries. Transfers rely on the EU-U.S. Data Privacy Framework for certified companies or on the European Commission's Standard Contractual Clauses (art. 45 and 46 GDPR)."),
        "Transferuri în afara SEE",
        p("Unii furnizori (Google, RevenueCat și alții marcați în tabel) prelucrează date în Statele Unite sau în alte țări. Transferurile se bazează pe Cadrul UE-SUA privind confidențialitatea datelor pentru companiile certificate sau pe Clauzele contractuale standard ale Comisiei Europene (art. 45 și 46 GDPR).")))

    out.append(S("rights", "Your rights (EEA, UK, Switzerland)",
        p("You have the right to access, correct and delete your data, to restrict or object to processing (including to object at any time to processing based on legitimate interest), to data portability, and to withdraw consent at any time without affecting earlier processing.",
          f"Because the app has no account, we usually cannot tell which data at Google or RevenueCat is yours. Write to {mail()} and include, if you can, the RevenueCat ID shown in the app or your purchase receipt, and we will forward the request to the provider. You can always delete all data on the device by deleting the app.",
          "You can complain to the supervisory authority where you live or work, or to ours: Autoritatea Națională de Supraveghere a Prelucrării Datelor cu Caracter Personal (ANSPDCP), " + link("https://www.dataprotection.ro") + ". The list of EU authorities: " + link("https://www.edpb.europa.eu/about-edpb/about-edpb/members_en", "edpb.europa.eu") + "."),
        "Drepturile tale (SEE, Regatul Unit, Elveția)",
        p("Ai dreptul de acces, rectificare și ștergere, de restricționare și de opoziție (inclusiv opoziție oricând la prelucrarea bazată pe interes legitim), la portabilitate și dreptul de a-ți retrage oricând consimțământul, fără a afecta prelucrarea anterioară.",
          f"Pentru că aplicația nu are cont, de obicei nu putem ști care date de la Google sau RevenueCat sunt ale tale. Scrie la {mail()} și, dacă poți, include ID-ul RevenueCat afișat în aplicație sau chitanța achiziției, iar noi trimitem cererea furnizorului. Poți șterge oricând toate datele de pe dispozitiv ștergând aplicația.",
          "Poți depune plângere la autoritatea de supraveghere din țara în care locuiești sau lucrezi, ori la a noastră: Autoritatea Națională de Supraveghere a Prelucrării Datelor cu Caracter Personal (ANSPDCP), " + link("https://www.dataprotection.ro") + ". Lista autorităților din UE: " + link("https://www.edpb.europa.eu/about-edpb/about-edpb/members_en", "edpb.europa.eu") + ".")))

    us_en = ["We do not sell personal information for money."]
    us_ro = ["Nu vindem informații personale pe bani."]
    if c.ads:
        us_en.append("When you allow personalised ads, Google AdMob uses your advertising identifier for ads based on activity in other apps. Some US state laws (for example California) call this \"sharing\" or \"targeted advertising\". You can opt out at any time: refuse tracking on iOS (Settings, Privacy & Security, Tracking), delete or reset the advertising ID on Android, or email us and we will treat it as an opt-out request.")
        us_ro.append("Când permiți reclame personalizate, Google AdMob folosește identificatorul de publicitate pentru reclame bazate pe activitatea din alte aplicații. Unele legi din statele SUA (de exemplu California) numesc asta „partajare” sau „publicitate țintită”. Poți refuza oricând: refuză urmărirea pe iOS (Setări, Confidențialitate și securitate, Urmărire), șterge sau resetează ID-ul de publicitate pe Android, sau scrie-ne și tratăm mesajul ca cerere de renunțare.")
    us_en.append(f"Residents of California and other US states with privacy laws can ask to know, correct or delete their personal information, and will not be treated differently for doing so. Categories collected in the last 12 months are the ones in the table above (identifiers, internet activity, approximate location from IP, purchase records). Requests: {mail()}.")
    us_ro.append(f"Rezidenții din California și din alte state SUA cu legi de confidențialitate pot cere să afle, să corecteze sau să șteargă informațiile personale, fără a fi tratați diferit pentru asta. Categoriile colectate în ultimele 12 luni sunt cele din tabel (identificatori, activitate online, locație aproximativă din IP, evidența achizițiilor). Cereri: {mail()}.")
    out.append(S("us", "United States", ul(us_en), "Statele Unite", ul(us_ro)))

    out.append(S("children", "Children",
        p(f"{n} is not directed at children. We do not knowingly collect personal data from children under 13, or under the age of digital consent in their country (13 to 16 in the EU). If you believe a child gave us data, write to {mail()} and we will delete what we can reach."
          + (" Ads in the app are not designed for children." if c.ads else "")),
        "Copii",
        p(f"{n} nu se adresează copiilor. Nu colectăm cu bună știință date personale de la copii sub 13 ani sau sub vârsta consimțământului digital din țara lor (13 până la 16 ani în UE; 16 ani în România). Dacă crezi că un copil ne-a dat date, scrie la {mail()} și ștergem ce putem accesa."
          + (" Reclamele din aplicație nu sunt destinate copiilor." if c.ads else ""))))

    out.append(S("security", "Security",
        p("All network connections use HTTPS. Data on the device is protected by the operating system's app sandbox and encryption. No system is perfectly secure, so we keep what leaves your device to the minimum listed here."),
        "Securitate",
        p("Toate conexiunile folosesc HTTPS. Datele de pe dispozitiv sunt protejate de izolarea aplicațiilor și de criptarea sistemului de operare. Niciun sistem nu e perfect sigur, de aceea trimitem în afara dispozitivului doar minimul descris aici.")))

    out.append(S("website", "This website",
        p(f["website"]["en"]) if f.get("website") else p(f"{c.site} is hosted on GitHub Pages (GitHub, Inc., USA), which records the IP address of visitors in server logs for security. The site sets no cookies and uses no analytics or ads. It stores only your language choice in your browser (local storage)."),
        "Acest site",
        p(f["website"]["ro"]) if f.get("website") else p(f"{c.site} este găzduit pe GitHub Pages (GitHub, Inc., SUA), care înregistrează adresa IP a vizitatorilor în jurnalele serverului, pentru securitate. Site-ul nu setează cookie-uri și nu folosește statistici sau reclame. Păstrează doar limba aleasă, în browserul tău (local storage).")))

    out.append(S("changes", "Changes",
        p(f"If the app starts handling data differently, we update this page and the date at the top before the new version ships. Important changes are also mentioned in the store update notes."),
        "Modificări",
        p("Dacă aplicația începe să trateze datele altfel, actualizăm această pagină și data de sus înainte de lansarea noii versiuni. Schimbările importante apar și în notele de actualizare din magazin.")))
    return out


def platform_list(self, lang):
    if self.ios and self.android:
        return {"en": "iOS and Android", "ro": "iOS și Android"}[lang]
    return "Android" if self.android else "iOS"


def services_table(self, lang):
    s = STR[lang]
    rows = []
    for key in self.services:
        sv = SERVICES[key]
        if key in self.f.get("basis_override", {}):
            bases = "; ".join(BASIS[b][lang] for b in self.f["basis_override"][key])
        elif "basis_text" in sv:
            bases = sv["basis_text"][lang]
        else:
            bases = "; ".join(BASIS[b][lang] for b in sv["basis"])
        tr = (" " + {"en": "Outside the EEA.", "ro": "În afara SEE."}[lang]) if sv["transfer"] else ""
        rows.append(
            f'<tr><th scope="row">{link(sv["link"], sv["name"])}<br><small>{e(sv["who"])}</small></th>'
            f'<td data-label="{s["data"]}">{e(sv[lang]["data"])}</td>'
            f'<td data-label="{s["purpose"]}">{e(sv[lang]["why"])}</td>'
            f'<td data-label="{s["basis"]}">{e(bases)}</td>'
            f'<td data-label="{s["ret"]}">{e(sv["ret"][lang])}{tr}</td></tr>')
    head = "".join(f'<th scope="col">{s[k]}</th>' for k in ("service", "data", "purpose", "basis", "ret"))
    return f'<div class="table-wrap"><table class="legal-table"><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'


def notes(self, lang):
    ns = [n[lang] for n in self.f.get("service_notes", [])]
    return ul(ns) if ns else ""


def perm_list(self, lang):
    items = []
    for key in self.f["permissions"]:
        t, d = PERMISSIONS[key][lang]
        items.append(f"<strong>{t}.</strong> {d}")
    return ul(items)


def consent(self, lang):
    f = self.f
    if lang == "en":
        parts = [
            "In the EEA, the UK and Switzerland the app first shows Google's consent form (a certified consent management platform under the IAB Transparency and Consent Framework). Until you answer it, no ad is requested and no usage statistics are sent. If you refuse personalised ads, you still get limited, non-personalised ads."]
        if self.ios:
            parts.append("On iOS the App Tracking Transparency prompt comes after the consent form. Ads load only once it is answered.")
        parts.append("Change your choice anytime: " + f["privacy_choices_path"]["en"] + (" On iOS, also Settings, Privacy & Security, Tracking." if self.ios else "") + (" On Android, Settings, Privacy, Ads." if self.android else ""))
        if f.get("consent_notes"):
            parts += [x["en"] for x in f["consent_notes"]]
        if self.paid and self.ads:
            parts.append("Buying the paid version removes ads.")
    else:
        parts = [
            "În SEE, Regatul Unit și Elveția aplicația arată întâi formularul de consimțământ Google (platformă certificată în IAB Transparency and Consent Framework). Până nu răspunzi, nu se cere nicio reclamă și nu se trimit statistici de utilizare. Dacă refuzi reclamele personalizate, primești în continuare reclame limitate, nepersonalizate."]
        if self.ios:
            parts.append("Pe iOS, întrebarea App Tracking Transparency vine după formularul de consimțământ. Reclamele se încarcă doar după ce îi răspunzi.")
        parts.append("Îți poți schimba oricând alegerea: " + f["privacy_choices_path"]["ro"] + (" Pe iOS, și din Setări, Confidențialitate și securitate, Urmărire." if self.ios else "") + (" Pe Android, din Setări, Confidențialitate, Reclame." if self.android else ""))
        if f.get("consent_notes"):
            parts += [x["ro"] for x in f["consent_notes"]]
        if self.paid and self.ads:
            parts.append("Cumpărarea versiunii plătite elimină reclamele.")
    return p(*parts)


Ctx.platform_list = platform_list
Ctx.services_table = services_table
Ctx.notes = notes
Ctx.perm_list = perm_list
Ctx.consent = consent


# ---------------------------------------------------------------- terms

APPLE_EULA = "https://www.apple.com/legal/internet-services/itunes/dev/stdeula/"
APPLE_MEDIA = "https://www.apple.com/legal/internet-services/itunes/"
PLAY_TOS = "https://play.google.com/about/play-terms/"


def terms(c):
    f, n = c.f, c.name
    out = []
    out.append(S("provider", "Who provides the app",
        p(f"{CONTROLLER['en'].replace('developer and data controller', 'developer and provider of ' + n)} These Terms are an agreement between you and Darius Cirjan (\"we\"). By installing or using {n} you accept them. If you do not agree, do not use the app.",
          f"Contact: {mail()}. {STR['en']['updated']}: {fmt_date(f['updated'], 'en')}."),
        "Cine oferă aplicația",
        p(f"{CONTROLLER['ro'].replace('dezvoltatorul și operatorul de date', 'dezvoltatorul și furnizorul aplicației ' + n)} Acești Termeni sunt un acord între tine și Darius Cirjan („noi”). Instalând sau folosind {n} îi accepți. Dacă nu ești de acord, nu folosi aplicația.",
          f"Contact: {mail()}. {STR['ro']['updated']}: {fmt_date(f['updated'], 'ro')}.")))

    out.append(S("service", f"What {n} does",
        p(c.t("what", "en")),
        f"Ce face {n}",
        p(c.t("what", "ro"))))

    lic_en = ["You get a personal, non-exclusive, non-transferable, revocable license to use the app on devices you own or control, for personal or professional use.",
              "You may not copy, resell, modify, reverse engineer or decompile the app, except where the law allows it, or use it for anything unlawful."]
    lic_ro = ["Primești o licență personală, neexclusivă, netransferabilă și revocabilă de a folosi aplicația pe dispozitivele pe care le deții sau le controlezi, în scop personal sau profesional.",
              "Nu ai voie să copiezi, să revinzi, să modifici, să decompilezi sau să faci inginerie inversă asupra aplicației, decât în măsura permisă de lege, și nici să o folosești în scopuri ilegale."]
    if c.ios:
        lic_en.append(f"If you downloaded the app from the App Store, the {link(APPLE_EULA, 'Apple Standard Licensed Application End User License Agreement')} also applies and the Apple section below forms part of these Terms.")
        lic_ro.append(f"Dacă ai descărcat aplicația din App Store, se aplică și {link(APPLE_EULA, 'Apple Standard Licensed Application End User License Agreement')}, iar secțiunea Apple de mai jos face parte din acești Termeni.")
    out.append(S("license", "License", ul(lic_en), "Licență", ul(lic_ro)))

    if c.paid:
        out.append(S("purchases", "Purchases and subscriptions", c.purchases("en"),
                     "Achiziții și abonamente", c.purchases("ro")))

    if c.ads:
        out.append(S("ads", "Ads",
            p("The free version shows ads served by Google AdMob, as described in the Privacy Policy. We are not responsible for the content of third-party ads or for the sites they open."),
            "Reclame",
            p("Versiunea gratuită afișează reclame livrate de Google AdMob, așa cum descrie Politica de confidențialitate. Nu răspundem pentru conținutul reclamelor terților sau pentru site-urile pe care le deschid.")))

    out.append(S("accuracy", "Important: results and your responsibility",
        p(*[d["en"] for d in f["disclaimers"]]),
        "Important: rezultatele și responsabilitatea ta",
        p(*[d["ro"] for d in f["disclaimers"]])))

    out.append(S("third", "Third-party services",
        p("Parts of the app rely on services run by others (listed in the Privacy Policy). They can change or stop, and their own terms apply. If a service becomes unavailable, the related feature may stop working; we will try to replace it."),
        "Servicii terțe",
        p("Unele părți ale aplicației se bazează pe servicii ale altora (listate în Politica de confidențialitate). Acestea se pot schimba sau opri, iar condițiile lor se aplică. Dacă un serviciu nu mai e disponibil, funcția legată de el poate să nu mai meargă; vom încerca să îl înlocuim.")))

    out.append(S("ip", "Intellectual property",
        p(f"The app, its name, design and code belong to Darius Cirjan. Data you enter stays yours. Map imagery and data belong to their providers and keep their attributions."),
        "Proprietate intelectuală",
        p(f"Aplicația, numele, designul și codul ei aparțin lui Darius Cirjan. Datele pe care le introduci rămân ale tale. Imaginile și datele de hartă aparțin furnizorilor lor și își păstrează atribuirile.")))

    out.append(S("warranty", "Warranty and liability",
        ul(["The app is provided as is and as available. We do our best to keep it accurate and working, but we do not promise that it is free of errors or always available.",
            "If you are a consumer in the EU or the UK, you keep all statutory rights, including the legal guarantee that digital content conforms to the contract (Directive (EU) 2019/770, in Romania OUG 141/2021). Nothing here limits those rights.",
            "We are not liable for indirect or consequential loss, such as lost profit, lost data or decisions made from the app's results. Our total liability for any claim is limited to the amount you paid for the app in the 12 months before the claim.",
            "None of these limits apply to liability that the law does not allow to be limited, including for intent, gross negligence, or death or personal injury."]),
        "Garanție și răspundere",
        ul(["Aplicația este oferită „ca atare” și „după disponibilitate”. Facem tot ce putem ca ea să fie corectă și funcțională, dar nu promitem că nu are erori sau că e mereu disponibilă.",
            "Dacă ești consumator în UE sau Regatul Unit, îți păstrezi toate drepturile legale, inclusiv garanția legală de conformitate a conținutului digital (Directiva (UE) 2019/770, în România OUG 141/2021). Nimic de aici nu limitează aceste drepturi.",
            "Nu răspundem pentru pierderi indirecte, precum profit pierdut, date pierdute sau decizii luate pe baza rezultatelor aplicației. Răspunderea noastră totală pentru orice pretenție este limitată la suma plătită pentru aplicație în cele 12 luni dinaintea pretenției.",
            "Aceste limite nu se aplică răspunderii care nu poate fi limitată prin lege, inclusiv pentru intenție, culpă gravă, deces sau vătămare corporală."])))

    out.append(S("end", "Ending the agreement",
        p("You can stop at any time by deleting the app; cancel any subscription in your store account as well. We may end your license if you break these Terms. Sections on liability, intellectual property and law survive the end."),
        "Încetarea acordului",
        p("Poți renunța oricând ștergând aplicația; anulează și abonamentul din contul de magazin. Putem încheia licența dacă încalci acești Termeni. Secțiunile despre răspundere, proprietate intelectuală și lege rămân valabile după încetare.")))

    if c.ios:
        out.append(S("apple", "App Store (Apple) terms",
            ul(["These Terms are between you and Darius Cirjan only, not with Apple. Apple is not responsible for the app or its content.",
                "Apple has no obligation to provide maintenance or support for the app. Support: " + mail() + ".",
                "If the app fails to meet any applicable warranty, you may notify Apple and Apple will refund the purchase price, if any. To the maximum extent permitted by law, Apple has no other warranty obligation for the app.",
                "Apple is not responsible for any claims relating to the app, including product liability, failure to meet legal or regulatory requirements, and consumer protection or privacy claims.",
                "If a third party claims the app infringes their intellectual property, Apple is not responsible for the investigation, defense, settlement or discharge of that claim.",
                "You confirm that you are not in a country subject to a U.S. Government embargo or designated as supporting terrorism, and that you are not on any U.S. Government list of prohibited or restricted parties.",
                "You must follow the terms of any third-party service you use with the app.",
                "Apple and its subsidiaries are third-party beneficiaries of these Terms and may enforce them against you."]),
            "Condiții App Store (Apple)",
            ul(["Acești Termeni sunt doar între tine și Darius Cirjan, nu cu Apple. Apple nu răspunde pentru aplicație sau conținutul ei.",
                "Apple nu are nicio obligație de mentenanță sau asistență pentru aplicație. Asistență: " + mail() + ".",
                "Dacă aplicația nu respectă o garanție aplicabilă, poți anunța Apple, iar Apple îți va rambursa prețul de achiziție, dacă există. În limita maximă permisă de lege, Apple nu are nicio altă obligație de garanție pentru aplicație.",
                "Apple nu răspunde pentru nicio pretenție legată de aplicație, inclusiv răspunderea pentru produs, nerespectarea cerințelor legale sau de reglementare și pretenții privind protecția consumatorului sau a datelor.",
                "Dacă un terț pretinde că aplicația îi încalcă drepturile de proprietate intelectuală, Apple nu răspunde pentru investigarea, apărarea, soluționarea sau stingerea acelei pretenții.",
                "Confirmi că nu te afli într-o țară supusă unui embargo al Guvernului SUA sau desemnată ca sprijinind terorismul și că nu figurezi pe nicio listă a Guvernului SUA cu persoane interzise sau restricționate.",
                "Trebuie să respecți condițiile oricărui serviciu terț pe care îl folosești împreună cu aplicația.",
                "Apple și filialele sale sunt terți beneficiari ai acestor Termeni și îi pot aplica împotriva ta."])))

    out.append(S("law", "Law and disputes",
        p("These Terms are governed by Romanian law. If you are a consumer, you also keep the protection of the mandatory laws of the country where you live, and you can bring a claim in the courts of that country. Otherwise the courts of Romania have jurisdiction.",
          f"Please write to {mail()} first; most problems are solved quickly. Consumers can also contact their national consumer authority (in Romania, ANPC: {link('https://anpc.ro')}) or an alternative dispute resolution body."),
        "Legea aplicabilă și litigii",
        p("Acești Termeni sunt guvernați de legea română. Dacă ești consumator, păstrezi și protecția legilor obligatorii din țara în care locuiești și poți acționa în instanțele de acolo. Altfel, sunt competente instanțele din România.",
          f"Te rugăm să ne scrii întâi la {mail()}; majoritatea problemelor se rezolvă repede. Consumatorii pot contacta și autoritatea națională pentru protecția consumatorilor (în România, ANPC: {link('https://anpc.ro')}) sau o entitate de soluționare alternativă a litigiilor.")))

    out.append(S("changes", "Changes and language",
        p("We may update these Terms when the app changes. The date at the top shows the latest version; important changes are announced in the store update notes. Changes do not apply to a subscription period you already paid for. The English and Romanian versions are equally valid."),
        "Modificări și limbă",
        p("Putem actualiza acești Termeni când aplicația se schimbă. Data de sus arată ultima versiune; schimbările importante sunt anunțate în notele de actualizare din magazin. Schimbările nu se aplică unei perioade de abonament deja plătite. Versiunile în engleză și română au aceeași valoare.")))
    return out


def purchases(self, lang):
    f = self.f
    pu = f["purchases"]
    items = [pu["what"][lang]]
    if lang == "en":
        items.append(f"Prices are shown in the app and in the store before you buy, in your currency, with VAT where applicable. Payment is taken by {self.store('en')} when you confirm.")
        if pu.get("subscriptions"):
            items.append("Subscriptions renew automatically at the same price for the same period unless you cancel at least 24 hours before the period ends. Your account is charged within 24 hours before renewal.")
            items.append("Manage or cancel: on iPhone, Settings, your name, Subscriptions" + (" ; on Android, Google Play, Payments and subscriptions." if self.android else "."))
        if pu.get("trial"):
            items.append("A free trial, when offered, turns into a paid subscription at its end unless you cancel at least 24 hours before. Any unused part of a trial ends when you buy a subscription.")
        if pu.get("lifetime"):
            items.append("A lifetime purchase is a one-time payment that unlocks the paid features for as long as the app is offered, without renewal.")
        items.append("Restore purchases on a new device with Restore Purchases in the app, using the same store account.")
        items.append(f"Refunds and cancellations are handled by the store under its own rules: Apple at {link('https://reportaproblem.apple.com')} under the {link(APPLE_MEDIA, 'Apple Media Services Terms')}" + (f"; Google at {link('https://play.google.com/store/account/orderhistory', 'Google Play order history')} under the {link(PLAY_TOS, 'Google Play Terms')}" if self.android else "") + ". We cannot issue refunds ourselves.")
        items.append("EU and UK consumers: the 14-day right of withdrawal for digital content ends once you start using it after asking for immediate access, as allowed by Directive 2011/83/EU art. 16(m). The store's own cancellation policy still applies, and nothing here limits your statutory rights.")
    else:
        items.append(f"Prețurile apar în aplicație și în magazin înainte de cumpărare, în moneda ta, cu TVA unde se aplică. Plata este încasată de {self.store('ro')} la confirmare.")
        if pu.get("subscriptions"):
            items.append("Abonamentele se reînnoiesc automat la același preț, pentru aceeași perioadă, dacă nu le anulezi cu cel puțin 24 de ore înainte de sfârșitul perioadei. Contul este taxat în cele 24 de ore dinaintea reînnoirii.")
            items.append("Gestionare sau anulare: pe iPhone, Setări, numele tău, Abonamente" + ("; pe Android, Google Play, Plăți și abonamente." if self.android else "."))
        if pu.get("trial"):
            items.append("Perioada de probă gratuită, când este oferită, devine abonament plătit la final dacă nu o anulezi cu cel puțin 24 de ore înainte. Partea nefolosită a probei se încheie când cumperi un abonament.")
        if pu.get("lifetime"):
            items.append("Achiziția pe viață este o plată unică ce deblochează funcțiile plătite cât timp aplicația este oferită, fără reînnoire.")
        items.append("Restaurează achizițiile pe un dispozitiv nou cu Restaurează achizițiile din aplicație, folosind același cont de magazin.")
        items.append(f"Rambursările și anulările sunt gestionate de magazin, după regulile lui: Apple la {link('https://reportaproblem.apple.com')}, conform {link(APPLE_MEDIA, 'Apple Media Services Terms')}" + (f"; Google în {link('https://play.google.com/store/account/orderhistory', 'istoricul comenzilor Google Play')}, conform {link(PLAY_TOS, 'Termenilor Google Play')}" if self.android else "") + ". Noi nu putem emite rambursări.")
        items.append("Consumatori din UE și Regatul Unit: dreptul de retragere de 14 zile pentru conținut digital încetează când începi să îl folosești după ce ai cerut acces imediat, cum permite art. 16 lit. m din Directiva 2011/83/UE (în România, OUG 34/2014). Politica de anulare a magazinului se aplică în continuare și nimic de aici nu îți limitează drepturile legale.")
    return ul(items)


Ctx.purchases = purchases


def build(facts):
    """facts may define "extra_services" and "extra_permissions" with the same
    shape as SERVICES / PERMISSIONS, so app-specific entries stay in the app's
    own facts file."""
    SERVICES.update(facts.get("extra_services", {}))
    PERMISSIONS.update(facts.get("extra_permissions", {}))
    c = Ctx(facts)
    out = {"privacy": privacy(c), "terms": terms(c)}
    # "overrides": {"privacy.consent": {"en": "<p>..</p>", "ro": ".."}} replaces a
    # section body when the shared wording does not match what this app's code does.
    for key, val in facts.get("overrides", {}).items():
        kind, sid = key.split(".", 1)
        for sec in out[kind]:
            if sec["id"] == sid:
                sec["en"]["html"], sec["ro"]["html"] = val["en"], val["ro"]
                break
        else:
            raise SystemExit(f"override {key}: no such section")
    return out


if __name__ == "__main__":
    path = Path(sys.argv[1])
    if not path.is_absolute():
        path = Path(__file__).parent / path
    facts = json.loads(path.read_text())
    json.dump(build(facts), sys.stdout, ensure_ascii=False, indent=1)
