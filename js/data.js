// Site content. App names, subtitles, categories and store links come from the live
// App Store listings (checked 2026-11-15). Descriptions only claim what each app does.

window.VISTO = {
  email: "iosallapps@gmail.com",
  appleEula: "https://www.apple.com/legal/internet-services/itunes/dev/stdeula/",

  // Filter categories on the Apps page, in display order.
  categories: [
    { id: "productivity", icon: "folder", label: { en: "Productivity", ro: "Productivitate" } },
    { id: "utilities", icon: "layers", label: { en: "Utilities", ro: "Utilitare" } },
    { id: "lifestyle", icon: "heart", label: { en: "Lifestyle", ro: "Stil de viață" } },
    { id: "professional", icon: "briefcase", label: { en: "Professional", ro: "Profesional" } }
  ],

  // Apps are ordered best to worst by App Store proceeds, then first downloads (2026-08-01 to 2026-11-14).
  // The first eight are shown on Home and About.
  featured: ["topoxy", "agrondo", "kipply", "luris", "pdfino", "darc", "shelfready", "appsrank"],
  // The three large cards in the Home hero.
  hero: ["topoxy", "agrondo", "kipply"],

  apps: [
    {
      slug: "jinglemoon", site: "https://jinglemoon.com/", privacy: "https://jinglemoon.com/privacy.html", terms: "https://jinglemoon.com/terms.html", name: "JingleMoon", category: "lifestyle",
      colors: ["#d23a3f", "#6a1218"],
      store: "https://apps.apple.com/us/app/jinglemoon-santa-tracker/id6829834796",
      subtitle: { en: "Santa Tracker & Video Call", ro: "Moș Crăciun și apel video" },
      text: {
        en: "Follow Santa's sleigh on a 3D globe, chat with Santa, write him a letter and get a video call from him.",
        ro: "Urmărești sania lui Moș Crăciun pe un glob 3D, vorbești cu Moșul, îi scrii o scrisoare și primești un apel video de la el."
      }
    },
    {
      slug: "topoxy", site: "https://topoxyapp.com/", privacy: "https://topoxyapp.com/privacy.html", terms: "https://topoxyapp.com/terms.html", name: "TopoXY", category: "professional",
      colors: ["#20c45a", "#0d6450"],
      store: "https://apps.apple.com/us/app/topoxy-coordinate-converter/id6758582908",
      subtitle: { en: "Coordinate Converter", ro: "Conversie Stereo 70" },
      text: {
        en: "Convert coordinates between WGS84, Stereo 70, PUWG, UTM and other national grids, offline.",
        ro: "Convertești coordonate între WGS84, Stereo 70, PUWG, UTM și alte sisteme naționale, offline."
      }
    },
    {
      slug: "agrondo", site: "https://agrondo.com/", privacy: "https://agrondo.com/privacy.html", terms: "https://agrondo.com/terms.html", name: "Agrondo", category: "professional",
      colors: ["#2fbf6a", "#0e5a58"],
      store: "https://apps.apple.com/us/app/agrondo-field-area-measure/id6775927132",
      subtitle: { en: "Field Area Measure", ro: "Măsurare teren" },
      text: {
        en: "Measure field areas on the satellite map and keep records for every parcel.",
        ro: "Măsori terenuri pe harta satelit și ții evidența fiecărei parcele."
      }
    },
    {
      slug: "kipply", site: "https://kipplyapp.com/", privacy: "https://kipplyapp.com/privacy.html", terms: "https://kipplyapp.com/terms.html", name: "Kipply", category: "lifestyle",
      colors: ["#3a9dff", "#1d4ed0"],
      store: "https://apps.apple.com/us/app/kipply-smart-phone-cleaner/id6756061280",
      subtitle: { en: "Smart Phone Cleaner", ro: "Curățare poze" },
      text: {
        en: "Free up space by clearing duplicate, similar and unwanted photos with a swipe.",
        ro: "Faci spațiu ștergând pozele duplicate, asemănătoare și nedorite cu o glisare."
      }
    },
    {
      slug: "luris", site: "https://lurisapp.com/", privacy: "https://lurisapp.com/privacy.html", terms: "https://lurisapp.com/terms.html", name: "Luris", category: "lifestyle",
      colors: ["#2b8cff", "#1a3aa8"],
      store: "https://apps.apple.com/us/app/luris-step-fitness-tracker/id6813596103",
      subtitle: { en: "Step & Fitness Tracker", ro: "Pedometru și alergare" },
      text: {
        en: "Track your steps, walks, runs and rides with GPS, and follow a training plan.",
        ro: "Urmărești pașii, plimbările, alergările și turele cu bicicleta prin GPS, cu un plan de antrenament."
      }
    },
    {
      slug: "pdfino", site: "https://pdfino.com/", privacy: "https://pdfino.com/privacy.html", terms: "https://pdfino.com/terms.html", name: "Pdfino", category: "productivity",
      colors: ["#ea4646", "#8c2470"],
      store: "https://apps.apple.com/us/app/pdfino-compress-pdf-file-size/id6748689545",
      subtitle: { en: "Compress PDF File Size", ro: "Comprimă fișiere PDF" },
      text: {
        en: "Reduce PDF file size quickly, then scan, sign, merge and fill forms on your iPhone.",
        ro: "Micșorează PDF-urile rapid, apoi scanează, semnează, unește și completează formulare pe iPhone."
      }
    },
    {
      slug: "darc", site: "https://darcapp.com/", privacy: "https://darcapp.com/privacy.html", terms: "https://darcapp.com/terms.html", name: "Darc", category: "utilities",
      colors: ["#8a45f5", "#35208f"],
      store: "https://apps.apple.com/us/app/darc-dark-mode-for-safari/id6819036330",
      subtitle: { en: "Dark Mode for Safari", ro: "Mod întunecat în Safari" },
      text: {
        en: "A comfortable dark mode for every site in Safari, with light themes too.",
        ro: "Un mod întunecat confortabil pentru orice site din Safari, plus teme luminoase."
      }
    },
    {
      slug: "shelfready", site: "https://shelfreadyapp.com/", privacy: "https://shelfreadyapp.com/privacy.html", terms: "https://shelfreadyapp.com/terms.html", name: "ShelfReady", category: "productivity",
      colors: ["#c99a6c", "#5e3d36"],
      store: "https://apps.apple.com/us/app/shelfready-product-photos/id6818769240",
      subtitle: { en: "Product Photos", ro: "Poze de produs" },
      text: {
        en: "Turn a quick photo into a clean product shot on a white background, in seconds.",
        ro: "Transformi o poză rapidă într-o fotografie de produs pe fundal alb, în câteva secunde."
      }
    },
    {
      slug: "appsrank", site: "https://appsrankapp.com/", privacy: "https://appsrankapp.com/privacy", terms: "https://appsrankapp.com/terms", name: "AppsRank", category: "utilities",
      colors: ["#9150ff", "#3a2496"],
      store: "https://apps.apple.com/us/app/appsrank-ranking-tracker/id6762045370",
      subtitle: { en: "Ranking Tracker", ro: "Clasament App Store" },
      text: {
        en: "Follow app rankings on the App Store charts in more than 160 countries, every day.",
        ro: "Urmărești zilnic clasamentele aplicațiilor din App Store, în peste 160 de țări."
      }
    },
    {
      slug: "serenity", site: "https://serenityjournalapp.com/", privacy: "https://serenityjournalapp.com/privacy.html", terms: "https://serenityjournalapp.com/terms.html", name: "Serenity", category: "lifestyle",
      colors: ["#8c55dd", "#2b2a70"],
      store: "https://apps.apple.com/us/app/serenity-ai-mood-journal/id6761684674",
      subtitle: { en: "AI Mood Journal", ro: "Jurnal personal AI" },
      text: {
        en: "Log your mood in one tap, write with thoughtful prompts and see what lifts you.",
        ro: "Notezi starea cu o atingere, scrii pornind de la întrebări bine alese și vezi ce te ajută."
      }
    },
    {
      slug: "kupfra", site: "https://kupfra.com/", privacy: "https://kupfra.com/privacy.html", terms: "https://kupfra.com/terms.html", name: "Kupfra", category: "professional",
      colors: ["#f2853a", "#7a2f6e"],
      store: "https://apps.apple.com/us/app/kupfra-construction-calculator/id6827716801",
      subtitle: { en: "Construction Calculator", ro: "Calculator construcții" },
      text: {
        en: "Calculators for concrete, tiles, stairs and electrical work, built on real building standards.",
        ro: "Calcule pentru beton, gresie, scări și instalații electrice, după standardele reale de construcții."
      }
    }
  ]
};

// Romanian strings. English lives in the HTML itself; site.js remembers it on load,
// so there is one copy of every English sentence.
window.VISTO_RO = {
  "meta.home.title": "Visto Apps | Studio de aplicații mobile utile pentru iPhone",
  "meta.home.desc": "Visto Apps este studioul independent din spatele aplicațiilor JingleMoon, TopoXY, Agrondo, Kipply, Luris, Pdfino, Darc, ShelfReady, AppsRank, Serenity și Kupfra.",
  "meta.apps.title": "Aplicațiile noastre: TopoXY, Agrondo, Kipply, Pdfino | Visto Apps",
  "meta.apps.desc": "Toate aplicațiile Visto Apps: comprimi PDF-uri, cureți poze, convertești coordonate Stereo 70, măsori terenuri, numeri pașii și altele, pe iPhone.",
  "meta.about.title": "Despre Visto Apps | Studio independent de aplicații mobile",
  "meta.about.desc": "Visto Apps proiectează și construiește aplicații iPhone practice și sigure pentru nevoi reale. Află cum transformăm idei utile în aplicații.",
  "meta.contact.title": "Contact Visto Apps | Suport și colaborări",
  "meta.contact.desc": "Scrie-ne pentru suport la aplicații, sugestii sau o idee de colaborare. Răspundem pe email cât de repede putem.",
  "meta.privacy.title": "Politica de confidențialitate | Visto Apps",
  "meta.terms.title": "Termeni de utilizare | Visto Apps",
  "meta.404.title": "Pagina nu există | Visto Apps",

  "meta.privacy.desc": "Cum tratează site-ul Visto Apps datele tale, plus link-uri spre politica de confidențialitate a fiecărei aplicații Visto Apps.",
  "meta.terms.desc": "Termenii de utilizare ai site-ului Visto Apps, plus link-uri spre termenii fiecărei aplicații și contractul de licență standard Apple.",
  "meta.404.desc": "Pagina nu există. Descoperă în schimb colecția Visto Apps.",
  "nav.home": "Acasă",
  "nav.apps": "Aplicații",
  "nav.about": "Despre",
  "nav.contact": "Contact",
  "nav.search": "Caută aplicații",
  "nav.menu": "Meniu",
  "nav.lang": "Limba",
  "footer.tagline": "Aplicații mobile<br>gândite atent.",
  "footer.privacy": "Confidențialitate",
  "footer.terms": "Termeni de utilizare",
  "footer.legal": "Apple, logo-ul Apple și iPhone sunt mărci comerciale ale Apple Inc.",

  "home.xmas.kicker": "Lansarea de top pentru Crăciun",
  "home.xmas.new": "Nou",
  "home.xmas.title": "Un apel video de la <em>Moș Crăciun</em>, sania pe un glob 3D și o scrisoare la care răspunde.",
  "home.xmas.lede": "JingleMoon aduce numărătoarea până la Crăciun acasă, pentru toată familia: vorbești cu Moșul, îi urmărești zborul în Ajun și ai totul pe ecranul de blocare. Fără reclame și fără cont.",
  "home.xmas.cta": "Descarcă JingleMoon",
  "home.xmas.site": "Află mai mult",
  "home.kicker": "Studio de aplicații mobile",
  "home.title": "Idei de zi cu zi.<br><em>Aplicații</em> remarcabile.",
  "home.lede": "Creăm aplicații mobile gândite atent, care fac treburile de zi cu zi<br class=\"br-wide\"> mai simple, mai inteligente și mai plăcute.",
  "home.stat.apps": "Aplicații",
  "home.stat.downloads": "Descărcări",
  "home.stat.rating": "Notă medie",
  "home.stat.platforms": "iOS și<br>Android",
  "home.explore": "Vezi aplicațiile",
  "home.apps.kicker": "Aplicațiile noastre",
  "home.apps.title": "O colecție de aplicații utile, în creștere.",
  "home.apps.all": "Vezi toate",
  "home.approach.kicker": "Abordarea noastră",
  "home.approach.title": "Tehnologia ar trebui<br>să fie <em>ușoară</em>.",
  "home.approach.1.title": "Utile prin design",
  "home.approach.1.text": "Pornim de la nevoi reale<br>și soluții practice.",
  "home.approach.2.title": "Gândite și rafinate",
  "home.approach.2.text": "Experiențe simple și intuitive,<br>cu atenție la detalii.",
  "home.approach.3.title": "Îmbunătățite constant",
  "home.approach.3.text": "Ținem aplicațiile la zi și le facem<br>mai bune în timp.",

  "apps.kicker": "Aplicațiile noastre",
  "apps.title": "O colecție de aplicații<br><em>utile</em>, în creștere.",
  "apps.lede": "Aplicații mobile practice, sigure și gândite atent,<br class=\"br-wide\"> pentru viața de zi cu zi și pentru meserii.",
  "apps.all": "Toate aplicațiile",
  "apps.empty": "Nicio aplicație nu se potrivește căutării.",
  "apps.search": "Caută după nume sau funcție",
  "apps.cta.title": "Găsește aplicația potrivită.",
  "apps.cta.text": "Descoperă toată colecția și vezi cum îți pot face aplicațiile noastre<br class=\"br-wide\"> treburile de zi cu zi mai ușoare.",
  "apps.cta.button": "Vezi aplicațiile",
  "app.open": "Deschide în App Store",

  "about.kicker": "Despre Visto Apps",
  "about.title": "Tehnologie făcută pentru<br>viața de <em>zi cu zi</em>.",
  "about.lede": "Creăm aplicații mobile practice, sigure și gândite atent,<br class=\"br-wide\"> care fac treburile de zi cu zi mai simple,<br class=\"br-wide\"> mai inteligente și mai plăcute.",
  "about.story.kicker": "Povestea noastră",
  "about.story.title": "Un studio de aplicații mobile<br>concentrat pe idei utile.",
  "about.story.text": "Visto Apps este un studio independent care proiectează și dezvoltă aplicații de calitate pentru nevoi reale, de zi cu zi. Scopul nostru e simplu: să transformăm idei practice în aplicații ușor de folosit, sigure și cu adevărat utile.",
  "about.philosophy.kicker": "Filozofia noastră",
  "about.philosophy.title": "Utile prin design.<br><em>Atente</em> din fire.",
  "about.p1.title": "Simple",
  "about.p1.text": "Experiențe curate<br>și intuitive.",
  "about.p2.title": "Practice",
  "about.p2.text": "Soluții reale pentru<br>treburile de zi cu zi.",
  "about.p3.title": "Sigure",
  "about.p3.text": "Aplicații pe care<br>te poți baza.",
  "about.build.kicker": "Cum construim",
  "about.build.title": "De la idee la o aplicație utilă.",
  "about.step1.title": "Găsim nevoi reale",
  "about.step1.text": "Ne concentrăm pe probleme practice și idei utile.",
  "about.step2.title": "Proiectăm cu grijă",
  "about.step2.text": "Experiențe curate, intuitive și ușor de folosit.",
  "about.step3.title": "Construim și rafinăm",
  "about.step3.text": "Dezvoltăm, testăm și îmbunătățim continuu.",
  "about.step4.title": "Ascultăm și evoluăm",
  "about.step4.text": "Ținem cont de părerile voastre și facem aplicațiile mai bune în timp.",
  "about.portfolio.kicker": "Portofoliul nostru",
  "about.cta.title": "Hai să creăm ceva util.",
  "about.cta.text": "Ai o întrebare, o idee sau o sugestie? Ne-ar plăcea să ne scrii.",
  "about.cta.button": "Contactează-ne",

  "contact.kicker": "Contactează Visto Apps",
  "contact.title": "Hai să <em>vorbim</em>.",
  "contact.lede": "Ai o întrebare, o sugestie sau o idee de colaborare?<br>Ne-ar plăcea să ne scrii.",
  "contact.email.title": "Email",
  "contact.support.title": "Suport",
  "contact.support.text": "Ajutor pentru aplicațiile noastre",
  "contact.support.subject": "Suport",
  "contact.collab.title": "Colaborări",
  "contact.collab.text": "Parteneriate și oportunități",
  "contact.collab.subject": "Colaborare",
  "contact.card.title": "Scrie-ne un mesaj",
  "contact.card.text": "Trimite-ne un email și îți răspundem cât de repede putem. Spune-ne despre ce aplicație e vorba și, dacă e o problemă, ce model de telefon ai.",
  "contact.card.button": "Trimite un email",
  "contact.card.copy": "Copiază adresa",
  "contact.card.copied": "Adresă copiată",
  "contact.g1.title": "Răspuns rapid",
  "contact.g1.text": "Încercăm să răspundem<br>cât mai repede.",
  "contact.g2.title": "Confidențialitatea contează",
  "contact.g2.text": "Informațiile tale<br>sunt în siguranță.",
  "contact.g3.title": "Suport real",
  "contact.g3.text": "Ajutor pentru aplicații<br>și funcții.",
  "contact.g4.title": "Părerea ta contează",
  "contact.g4.text": "Ideile tale ne ajută<br>să ne îmbunătățim.",

  "legal.apps.privacy": "Politicile de confidențialitate ale aplicațiilor",
  "legal.apps.privacy.text": "Fiecare aplicație are propria politică, publicată pe site-ul ei și legată din pagina ei din App Store.",
  "legal.apps.terms": "Termenii aplicațiilor",
  "legal.apps.terms.text": "Fiecare aplicație are proprii termeni de utilizare. Abonamentele și achizițiile din aplicații sunt guvernate și de Contractul de licență standard Apple (EULA).",
  "legal.col.app": "Aplicație",
  "legal.col.site": "Site",
  "legal.col.privacy": "Confidențialitate",
  "legal.col.terms": "Termeni",
  "legal.privacy": "Politica de confidențialitate",
  "legal.terms": "Termeni de utilizare",
  "legal.eula": "Contractul de licență standard Apple (EULA)",
  "legal.contact": "Întrebări despre aceste documente? Scrie-ne la",
  "privacy.title": "Politica de confidențialitate",
  "privacy.updated": "Actualizată pe 15 noiembrie 2026",
  "privacy.body": "<p>Acest site prezintă aplicațiile Visto Apps. Nu folosește cookie-uri, nu are statistici de trafic sau reclame și nu îți cere date personale. Fonturile și imaginile sunt găzduite pe același server, așa că vizita ta nu este trimisă altor companii.</p><p>Singura preferință salvată este limba aleasă (engleză sau română), în browserul tău, și o poți șterge oricând din setările browserului.</p><p>Dacă ne scrii pe email, folosim adresa și mesajul tău doar ca să-ți răspundem. Fiecare aplicație are propria politică de confidențialitate, legată din pagina ei din App Store.</p><p>Pentru întrebări despre datele tale, scrie-ne la adresa de pe pagina de contact.</p>",
  "terms.title": "Termeni de utilizare",
  "terms.updated": "Actualizați pe 15 noiembrie 2026",
  "terms.body": "<p>Conținutul acestui site, inclusiv textele, logo-ul Visto Apps și imaginile, aparține Visto Apps și este oferit doar pentru informare.</p><p>Aplicațiile se descarcă și se cumpără prin App Store, sub termenii Apple și termenii fiecărei aplicații, afișați în pagina ei. Prețurile și disponibilitatea pot diferi de la o țară la alta.</p><p>Apple, logo-ul Apple, iPhone și App Store sunt mărci comerciale ale Apple Inc.</p>",
  "404.title": "Pagina nu <em>există</em>.",
  "404.text": "Linkul poate fi vechi sau greșit. Aplicațiile sunt la un click distanță.",
  "404.button": "Vezi aplicațiile"
};
