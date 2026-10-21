import sys, os, re
OUT = sys.argv[1]
EMAIL = "bk@techsutralabs.co.in"
SITE = "https://techsutralabs.com"

I = {
 "code":'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 6l-6 6 6 6M16 6l6 6-6 6"/></svg>',
 "cloud":'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 18a5 5 0 01-.5-9.97A6 6 0 0118 9a4.5 4.5 0 01-.5 9z"/></svg>',
 "wrench":'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a4 4 0 00-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 005.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/></svg>',
 "link":'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 14a5 5 0 007 0l3-3a5 5 0 00-7-7l-1 1M14 10a5 5 0 00-7 0l-3 3a5 5 0 007 7l1-1"/></svg>',
 "bulb":'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18h6M10 22h4M12 2a7 7 0 00-4 12.7V17h8v-2.3A7 7 0 0012 2z"/></svg>',
 "db":'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/></svg>',
 "headset":'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 14v-2a9 9 0 0118 0v2M21 14v3a2 2 0 01-2 2h-1v-6h3zM3 14v3a2 2 0 002 2h1v-6H3z"/></svg>',
 "box":'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 8l-9-5-9 5v8l9 5 9-5zM3 8l9 5 9-5M12 13v8"/></svg>',
 "mail":'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
 "pin":'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s7-6.2 7-12a7 7 0 00-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>',
 "ai":'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z"/><path d="M19 15l.9 2.1L22 18l-2.1.9L19 21l-.9-2.1L16 18l2.1-.9z"/></svg>',
 "clock":'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
}
LOGO = '<img src="assets/logo-tsl.png" width="66" height="40" alt="">'
WORDMARK = '<span class="wm"><b>TECHSUTRA</b><small>Labs Ventures</small></span>'
LEGAL = 'TechSutraLabs Ventures (OPC) Private Limited'

SERVICES = [
 ("ai","AI, ML & Generative AI","Practical AI that solves real business problems: machine learning models, generative AI assistants and intelligent automation, designed around your data and requirements.",["AI strategy and use-case discovery","Generative AI assistants and chatbots grounded in your own documents (RAG)","Custom machine learning models for prediction, classification, forecasting and anomaly detection","Intelligent document processing: OCR, data extraction and classification","AI agents that automate multi-step workflows","Integration with leading AI models (OpenAI, Anthropic Claude, Google Gemini) or private open-source models","Evaluation, monitoring, guardrails and human-in-the-loop review"]),
 ("code","Software Development","Design, development and implementation of custom software applications and computer programs, from requirements to production rollout.",["Web and enterprise applications","Requirements analysis and solution design","Implementation, rollout and user training"]),
 ("cloud","Cloud & Digital Platforms","Building, operating and managing cloud-based services and digital platforms that scale with your organisation.",["Cloud-native and containerised deployments","Multi-tenant SaaS platforms","Managed hosting and operations"]),
 ("wrench","Software Support & Maintenance","Keeping your applications healthy, secure and current with ongoing maintenance and upgrades.",["Bug fixes and security patches","Version upgrades and modernisation","Performance tuning and monitoring"]),
 ("link","System Integration","Connecting your applications, data sources and third-party services so they work as one system.",["API design and integration","Single sign-on (SAML / OIDC) and identity","Legacy system integration"]),
 ("bulb","IT Consulting","Practical, vendor-neutral advice on technology strategy, architecture and digital transformation.",["Technology and architecture assessments","Digital transformation roadmaps","Security and compliance readiness"]),
 ("db","Data Management","Organising, securing and governing your data across its lifecycle.",["Database design and migration","Document and records management","Data protection and retention policies"]),
 ("headset","Technical Support","Responsive technical support for your users and IT teams, with clear escalation paths.",["Helpdesk and L2/L3 support","Incident and problem management","Agreed service levels"]),
 ("box","Software Licensing","Ready-to-deploy software products licensed to businesses and institutions, configured to fit.",["Product licensing and subscriptions","Configuration and customisation","Onboarding and training"]),
]

PRODUCTS_RAW = [
 ("edms","Enterprise Document Management","Secure, multi-tenant document management for organisations that handle sensitive records.",["Versioning, metadata, full-text search and workflows","Single sign-on with SAML and OpenID Connect","Sensitivity labels, watermarking and retention","Bring-your-own-key encryption and data residency options","Support for India's DPDP Act requirements"],["Enterprises","Government","BFSI"]),
 ("clos","Commercial Loan Origination","End-to-end loan origination for lenders, from application to sanction and disbursement.",["Configurable credit workflows and approvals","Credit bureau, CKYC and Account Aggregator integration","Built-in business rules and policy checks","Exposure and limit management","Complete audit trail for every decision"],["Banks","NBFCs","Lenders"]),
 ("clm","Contract Lifecycle Management","Manage contracts from drafting and negotiation through approval, renewal and obligations.",["Templates, clause library and approvals","Obligation and renewal tracking","Bulk operations and repository search","User provisioning via SCIM 2.0"],["Legal teams","Procurement","Enterprises"]),
 ("campus","Campus Smart Card & Cashless Payments","A cashless campus platform for schools, colleges and universities.",["RFID / NFC smart cards for students and staff","Wallets with parent top-ups and controls","Point-of-sale for canteens and campus merchants","Settlement and reconciliation for merchants"],["Universities","Schools","Campuses"]),
 ("bpm","Low-Code BPM Platform","A low-code workflow platform to design, automate and run business processes without rewriting core systems.",["Visual BPMN process designer","Drag-and-drop form designer","Task inbox and process monitoring","Integration layer for external systems"],["Operations","Onboarding","Claims"]),
 ("ibre","Intelligent Business Rule Engine","Externalise business decisions so policies can change without code changes.",["Rule studio for business users","Decision tables and versioned rule sets","Fast, embeddable rule execution","Testing and simulation before release"],["BFSI","Insurance","Enterprises"]),
]

AI = {
 "edms":["Automatic document classification and metadata extraction","Semantic search: find documents by meaning, not just keywords","Ask questions of your documents and get answers with sources","AI summaries of long documents"],
 "clos":["Intelligent extraction of data from financial statements, bank statements and KYC documents","ML-assisted credit risk insights to support underwriters","GenAI-drafted credit appraisal notes for review","Anomaly and early-warning signals"],
 "clm":["AI extraction of key clauses, dates, parties and obligations","Risk flagging against your standard positions","Contract summaries and plain-language explanations","GenAI assistance for drafting and redlining"],
 "campus":["Spending insights and trends for students, parents and administrators","Anomaly detection for unusual or suspicious transactions","Demand forecasting for campus merchants","AI assistant for common account queries"],
 "bpm":["Describe a process in plain language and generate a draft workflow","AI-generated forms from a description","Intelligent document processing inside workflow tasks","Smart routing and task prioritisation"],
 "ibre":["Write rules in plain language and convert them to executable logic","AI explanations of why a decision was made","Detection of conflicting or overlapping rules","Combine business rules with ML model scores in one decision"],
}
SHORT = {"edms":"Document Management","clos":"Loan Origination","clm":"Contract Management","campus":"Campus Payments","bpm":"Low-Code BPM","ibre":"Business Rule Engine"}
PRODUCTS = [p + (None, SHORT[p[0]]) for p in PRODUCTS_RAW]

NAV = [("index.html","Home"),("services.html","Services"),("solutions.html","Solutions"),("about.html","About"),("contact.html","Contact")]

def page(fname, title, desc, body):
    base = '<base href="/">\n' if fname=="404.html" else ""
    robots = '<meta name="robots" content="noindex">\n' if fname=="404.html" else ""
    nav = "".join(f'<li><a href="{h}">{t}</a></li>' for h,t in NAV)
    canon = SITE + "/" + ("" if fname=="index.html" else fname)
    return f'''<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{base}{robots}<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:site_name" content="TechSutra Labs Ventures">
<meta property="og:image" content="{SITE}/assets/og-image.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#082f49">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self' mailto:; upgrade-insecure-requests">
<meta name="referrer" content="strict-origin-when-cross-origin">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Organization","name":"TechSutra Labs Ventures","legalName":"{LEGAL}","slogan":"Innovate. Build. Transform.","url":"{SITE}","logo":"{SITE}/assets/apple-touch-icon.png","email":"{EMAIL}","address":{{"@type":"PostalAddress","addressCountry":"IN"}},"description":"Software development, AI, ML and generative AI solutions, IT services, support and AI-powered enterprise software products.","knowsAbout":["Artificial intelligence","Machine learning","Generative AI","Software development","Enterprise software"]}}</script>
<link rel="icon" href="assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="assets/favicon.png" sizes="64x64" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="container nav">
<a class="logo" href="index.html" aria-label="TechSutra Labs Ventures, home">{LOGO}{WORDMARK}</a>
<button class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="primary-nav"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
<nav aria-label="Primary"><ul class="nav-links" id="primary-nav">{nav}<li><a class="btn btn-primary" href="contact.html" style="padding:9px 16px">Get in touch</a></li></ul></nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-footer"><div class="container">
<div class="footer-grid">
<div><a class="logo" href="index.html" aria-label="TechSutra Labs Ventures, home">{LOGO}{WORDMARK}</a>
<p class="legal-name">{LEGAL}</p>
<p style="margin-top:14px;max-width:340px">Software products, IT services and long-term technology support for businesses, institutions and organisations.</p></div>
<div><h2 class="f-h">Company</h2><ul><li><a href="about.html">About us</a></li><li><a href="contact.html">Contact</a></li><li><a href="privacy.html">Privacy policy</a></li><li><a href="terms.html">Terms of use</a></li></ul></div>
<div><h2 class="f-h">Services</h2><ul><li><a href="services.html#ai-ml-generative-ai">AI, ML &amp; GenAI</a></li><li><a href="services.html#software-development">Software development</a></li><li><a href="services.html#software-support-maintenance">Support &amp; maintenance</a></li><li><a href="services.html#system-integration">System integration</a></li><li><a href="services.html#it-consulting">IT consulting</a></li><li><a href="services.html#engagement">Engagement models</a></li></ul></div>
<div><h2 class="f-h">Solutions</h2><ul>{"".join(f'<li><a href="solutions.html#{p[0]}">{p[6]}</a></li>' for p in PRODUCTS)}</ul></div>
</div>
<div class="footer-bottom"><span>&copy; <span id="year">2026</span> {LEGAL}. All rights reserved.</span><span><a href="privacy.html">Privacy</a> &middot; <a href="terms.html">Terms</a> &middot; <a href="mailto:{EMAIL}">{EMAIL}</a></span></div>
</div></footer>
<script src="assets/main.js"></script>
</body>
</html>
'''

def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")

def cta(h="Let's build something that works for you", p="Tell us about your requirement. We'll respond with a clear plan, timeline and estimate."):
    return f'<section class="section"><div class="container"><div class="cta reveal"><h2>{h}</h2><p>{p}</p><a class="btn btn-primary" href="contact.html">Talk to us</a></div></div></section>'

# ---------- HOME
svc_cards = "".join(f'<div class="card reveal"><div class="icon">{I[ic]}</div><h3>{t}</h3><p>{d}</p><a class="card-link" href="services.html#{slug(t)}">Learn more &rarr;</a></div>' for ic,t,d,_ in SERVICES[:6])
prod_cards = "".join(f'<div class="card reveal"><span class="tag tag-ai">AI-powered</span>{"".join(f"<span class=tag>{x}</span>" for x in aud)}<h3 style="margin-top:8px">{t}</h3><p>{d}</p><a class="card-link" href="solutions.html#{k}">View solution &rarr;</a></div>' for k,t,d,_,aud,*_ in PRODUCTS)
home = f'''
<section class="hero"><div class="container" style="position:relative;z-index:1">
<span class="eyebrow">Innovate &middot; Build &middot; Transform</span>
<h1>Software and AI that run your business, <br>built and supported end to end.</h1>
<p class="lead">TechSutra Labs Ventures designs, builds, integrates and maintains software for businesses, institutions and organisations, from custom applications and AI, ML &amp; generative AI solutions to ready-to-deploy, AI-powered enterprise products.</p>
<div class="hero-actions"><a class="btn btn-primary" href="contact.html">Start a conversation</a><a class="btn btn-ghost" href="solutions.html">Explore our solutions</a></div>
</div></section>

<section class="section"><div class="container">
<div class="center"><span class="eyebrow">What we do</span><h2>AI, software and IT services, end to end</h2>
<p class="lead">One partner across the full lifecycle: AI and software design, development, deployment, integration and long-term support.</p></div>
<div class="grid grid-3" style="margin-top:40px">{svc_cards}</div>
<p class="center" style="margin-top:32px"><a class="btn btn-outline" href="services.html">All services</a></p>
</div></section>

<section class="section alt"><div class="container">
<div class="center"><span class="eyebrow">Our solutions</span><h2>AI-powered enterprise products, ready to deploy</h2>
<p class="lead">Platforms with AI, machine learning and generative AI built in, which we license, configure and support, in the cloud or on your own infrastructure.</p></div>
<div class="grid grid-3" style="margin-top:40px">{prod_cards}</div>
</div></section>

<section class="section ai-band"><div class="container">
<div class="center"><span class="eyebrow">AI, ML &amp; Generative AI</span><h2>Intelligence built in, and built for you</h2>
<p class="lead">AI is part of everything we make. Every product we offer has AI built in, and we help organisations design and implement AI, ML and generative AI solutions around their own requirements.</p></div>
<div class="grid grid-2" style="margin-top:40px">
<div class="card reveal"><div class="icon">{I["box"]}</div><h3>AI inside every product</h3><ul class="checklist">
<li>Document understanding, classification and semantic search</li>
<li>Data extraction from financial, KYC and contract documents</li>
<li>Generative AI summaries, drafting and question answering</li>
<li>ML insights, forecasting and anomaly detection</li></ul>
<a class="card-link" href="solutions.html">See AI in our products &rarr;</a></div>
<div class="card reveal"><div class="icon">{I["ai"]}</div><h3>AI solutions for your business</h3><ul class="checklist">
<li>Use-case discovery and AI roadmap</li>
<li>GenAI assistants and chatbots on your own data</li>
<li>Custom ML models for prediction and decisions</li>
<li>AI agents and intelligent workflow automation</li></ul>
<a class="card-link" href="services.html#ai-ml-generative-ai">Explore AI services &rarr;</a></div>
</div>
<div class="tech"><span>Large language models</span><span>Retrieval-augmented generation (RAG)</span><span>Vector search</span><span>Machine learning</span><span>OCR &amp; document AI</span><span>AI agents</span><span>MLOps</span></div>
</div></section>

<section class="section"><div class="container">
<div class="center"><span class="eyebrow">Industries</span><h2>Where our software works</h2>
<p class="lead">Domain-aware solutions for sectors with demanding security, compliance and scale requirements.</p></div>
<div class="grid grid-2" style="margin-top:40px">
<div class="card industry reveal"><div class="icon">{I["db"]}</div><div><h3>Banking &amp; financial services</h3><p>Loan origination, credit rules, KYC integrations and document management with full audit trails.</p></div></div>
<div class="card industry reveal"><div class="icon">{I["bulb"]}</div><div><h3>Education</h3><p>Cashless campus payments, smart cards and digital records for schools, colleges and universities.</p></div></div>
<div class="card industry reveal"><div class="icon">{I["box"]}</div><div><h3>Enterprises</h3><p>Contracts, documents, workflows and integrations that connect departments and systems.</p></div></div>
<div class="card industry reveal"><div class="icon">{I["link"]}</div><div><h3>Public sector &amp; institutions</h3><p>Secure records, data-protection controls and data residency for regulated environments.</p></div></div>
</div></div></section>

<section class="section alt"><div class="container">
<div class="center"><span class="eyebrow">How we work</span><h2>A clear, accountable process</h2></div>
<div class="steps" style="margin-top:40px">
<div class="step reveal"><h3>Understand</h3><p>We study your processes, users and constraints, and agree on scope and success criteria.</p></div>
<div class="step reveal"><h3>Design</h3><p>Architecture, data model and user experience, reviewed with you before we build.</p></div>
<div class="step reveal"><h3>Build &amp; integrate</h3><p>Iterative delivery with regular demos, automated testing and integration with your systems.</p></div>
<div class="step reveal"><h3>Support &amp; evolve</h3><p>Deployment, training, maintenance and upgrades for as long as you run the software.</p></div>
</div></div></section>

<section class="section"><div class="container center">
<span class="eyebrow">Why TechSutra Labs Ventures</span><h2>Built for security, scale and the long run</h2>
<div class="grid grid-3" style="margin-top:40px;text-align:left">
<div class="card reveal"><h3>Security by design</h3><p>Single sign-on, role-based access, encryption, audit trails and data-protection controls are built in from the start.</p></div>
<div class="card reveal"><h3>AI with control</h3><p>AI that works on your data with privacy, human review and the option of private models that never leave your infrastructure.</p></div>
<div class="card reveal"><h3>Long-term partnership</h3><p>We stay after go-live with maintenance, upgrades and responsive support.</p></div>
</div>
<div class="tech"><span>Java &amp; Spring Boot</span><span>React &amp; TypeScript</span><span>PostgreSQL</span><span>Docker</span><span>Keycloak SSO</span><span>REST APIs</span><span>BPMN workflows</span><span>Python &amp; ML</span><span>LLMs &amp; RAG</span></div>
</div></section>
{cta()}
'''

# ---------- SERVICES
svc_detail = "".join(f'''<div class="product" id="{slug(t)}"><div><div class="card" style="box-shadow:none;height:auto"><div class="icon">{I[ic]}</div><h2 style="font-size:1.5rem">{t}</h2><p>{d}</p></div></div>
<div><h3>What's included</h3><ul class="checklist">{"".join(f"<li>{x}</li>" for x in pts)}</ul></div></div>''' for ic,t,d,pts in SERVICES)
services = f'''
<section class="page-hero"><div class="container"><span class="eyebrow">Services</span><h1>IT services across the software lifecycle</h1>
<p class="lead">From the first design workshop to years of maintenance, TechSutra Labs Ventures takes responsibility for your software.</p></div></section>
<section class="section"><div class="container">{svc_detail}</div></section>
<section class="section alt"><div class="container center"><span class="eyebrow">Who we serve</span><h2>Individuals, businesses, institutions and organisations</h2>
<div class="grid grid-3" style="margin-top:32px;text-align:left">
<div class="card"><h3>Businesses</h3><p>From growing companies to large enterprises that need dependable, secure business software.</p></div>
<div class="card"><h3>Banks &amp; financial institutions</h3><p>Lending, document and rule-driven systems with the audit trails and controls regulators expect.</p></div>
<div class="card"><h3>Education &amp; institutions</h3><p>Campus payments, records management and digital services for schools, colleges and universities.</p></div>
</div></div></section>
<section class="section" id="engagement"><div class="container center"><span class="eyebrow">Engagement models</span><h2>Flexible ways to work with us</h2>
<p class="lead">Choose the model that fits your scope, budget and timeline. We can also combine them.</p>
<div class="grid grid-2" style="margin-top:32px;text-align:left;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">
<div class="card"><h3>Fixed-scope project</h3><p>Defined requirements, fixed price and milestones. Best for well-understood projects.</p></div>
<div class="card"><h3>Time &amp; materials</h3><p>Pay for the effort used, with the flexibility to change priorities as you learn.</p></div>
<div class="card"><h3>Dedicated team</h3><p>A team that works as an extension of yours, for ongoing product development.</p></div>
<div class="card"><h3>Annual maintenance (AMC)</h3><p>Ongoing support, fixes, security updates and upgrades under an annual contract.</p></div>
<div class="card"><h3>AI proof of concept</h3><p>A short, fixed-scope pilot that tests an AI use case on your own data before you invest in a full rollout.</p></div>
</div></div></section>
{cta()}
'''

# ---------- SOLUTIONS
prod_detail = "".join(f'''<div class="product" id="{k}"><div>{"".join(f"<span class=tag>{x}</span>" for x in aud)}<h2 style="margin-top:10px">{t}</h2><p class="lead">{d}</p><a class="btn btn-outline" href="contact.html?topic={k}">Request a demo</a></div>
<div class="card" style="height:auto"><h3>Key capabilities</h3><ul class="checklist">{"".join(f"<li>{x}</li>" for x in pts)}</ul>
<div class="ai-box"><h4><span class="ai-badge">{I["ai"]} AI-powered</span></h4><ul class="checklist">{"".join(f"<li>{x}</li>" for x in AI[k])}</ul></div></div></div>''' for k,t,d,pts,aud,*_ in PRODUCTS)
solutions = f'''
<section class="page-hero"><div class="container"><span class="eyebrow">Solutions</span><h1>AI-powered enterprise software products</h1>
<p class="lead">Platforms with AI, machine learning and generative AI built in, which we license, configure, integrate and support, each deployable in the cloud or on your own infrastructure.</p></div></section>
<nav class="subnav" aria-label="Solutions"><div class="container"><ul>{"".join(f'<li><a href="#{p[0]}">{p[6]}</a></li>' for p in PRODUCTS)}</ul></div></nav>
<section class="section" style="padding-top:24px"><div class="container">{prod_detail}</div></section>
<section class="section alt"><div class="container center"><h2>Every solution includes</h2>
<div class="grid grid-3" style="margin-top:32px;text-align:left">
<div class="card"><h3>Implementation</h3><p>Configuration to your processes, data migration and integration with your existing systems.</p></div>
<div class="card"><h3>Training</h3><p>Hands-on training for administrators and end users, plus documentation.</p></div>
<div class="card"><h3>Support &amp; upgrades</h3><p>Ongoing maintenance, security updates and new versions under a support agreement.</p></div>
</div></div></section>
{cta("See a solution in action","Book a walkthrough of any of our products, tailored to your use case.")}
'''

# ---------- ABOUT
TECH = [
 ("AI, ML & generative AI","Large language models, RAG, vector search, machine learning, OCR and document AI, AI agents, MLOps"),
 ("Backend engineering","Java, Spring Boot, REST APIs, modular and microservice architectures"),
 ("Web & front end","React, TypeScript, responsive and accessible user interfaces"),
 ("Data","PostgreSQL, data modelling, migration, full-text search, reporting"),
 ("Cloud & DevOps","Docker containers, CI/CD pipelines, cloud and on-premises deployment"),
 ("Identity & security","Single sign-on (SAML, OpenID Connect), Keycloak, MFA, encryption, audit trails"),
 ("Workflow & rules","BPMN process automation, form builders, business rule engines"),
]
APPROACH = [
 ("Discovery first","Every engagement starts by understanding your processes, users, constraints and success criteria, before any code is written."),
 ("Iterative delivery","Work is delivered in short cycles with regular demos, so you see progress early and can steer priorities."),
 ("Engineering quality","Automated tests, code review and documented designs are part of every release, not optional extras."),
 ("Security by default","Access control, encryption, audit logging and data-protection controls are designed in from the first sprint."),
 ("Clear communication","One accountable point of contact, transparent status reporting and honest timelines."),
 ("Support after go-live","Training, maintenance, upgrades and responsive support for as long as you run the software."),
]
about = f"""
<section class="page-hero"><div class="container"><span class="eyebrow">About us</span><h1>Innovate. Build. Transform.</h1>
<p class="lead">TechSutra Labs Ventures is an Indian technology company that designs, builds, integrates and supports software for businesses, institutions and organisations, and helps them transform how they work.</p></div></section>

<section class="section"><div class="container grid grid-2" style="align-items:start;gap:48px">
<div class="prose"><span class="eyebrow">Who we are</span><h2 style="margin-top:0">Technology partners for the long run</h2>
<p>TechSutra Labs Ventures ({LEGAL}) is a technology company registered in India. We take responsibility for software across its whole life: designing and developing it, implementing and operating it, and maintaining, upgrading and supporting it for years after go-live.</p>
<p>Artificial intelligence runs through everything we do. Every one of our products has AI, machine learning and generative AI built in, and we help clients design and implement AI solutions around their own data, processes and requirements.</p>
<p>Alongside custom development, we build and license our own enterprise products for document management, loan origination, contract management, campus payments, workflow automation and business rules. Building our own products keeps our engineering sharp, and it means clients can start from proven software instead of a blank page.</p>
<p>Our name joins <em>tech</em> with <em>sutra</em>, the Sanskrit word for a thread, or a concise rule that holds a body of knowledge together. That is how we see good software: a clear thread that connects people, processes and data.</p></div>
<div class="card" style="height:auto"><h3>Company at a glance</h3>
<dl class="facts">
<div><dt>Legal name</dt><dd>{LEGAL}</dd></div>
<div><dt>Company type</dt><dd>One Person Company (OPC), private limited</dd></div>
<div><dt>Registered in</dt><dd>India</dd></div>
<div><dt>What we do</dt><dd>Software development, AI, ML &amp; generative AI solutions, IT services, support &amp; maintenance, AI-powered enterprise products</dd></div>
<div><dt>Who we serve</dt><dd>Individuals, businesses, institutions and organisations</dd></div>
<div><dt>Website</dt><dd>techsutralabs.com</dd></div>
<div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
</dl></div>
</div></section>

<section class="section alt"><div class="container"><div class="grid grid-3">
<div class="card reveal"><div class="icon">{I["bulb"]}</div><h3>Our mission</h3><p>Make reliable, secure enterprise software accessible to organisations of every size, and support it for as long as they depend on it.</p></div>
<div class="card reveal"><div class="icon">{I["cloud"]}</div><h3>Our vision</h3><p>To be the technology partner organisations trust to run, and transform, their critical processes.</p></div>
<div class="card reveal"><div class="icon">{I["headset"]}</div><h3>Our promise</h3><p>Clear scope, honest timelines and software that keeps working, backed by people who answer when you call.</p></div>
</div></div></section>

<section class="section"><div class="container"><div class="center"><span class="eyebrow">What we do</span><h2>Services and products under one roof</h2>
<p class="lead">Whether you need something built for you, a product configured for you, or an existing system looked after, we can help.</p></div>
<div class="grid grid-2" style="margin-top:40px">
<div class="card reveal"><h3>IT services</h3><ul class="checklist">{"".join(f'<li><a href="services.html#{slug(t)}">{t}</a></li>' for _,t,_,_ in SERVICES)}</ul><a class="card-link" href="services.html">Explore services &rarr;</a></div>
<div class="card reveal"><h3>Enterprise products</h3><ul class="checklist">{"".join(f'<li><a href="solutions.html#{p[0]}">{p[1]}</a></li>' for p in PRODUCTS)}</ul><a class="card-link" href="solutions.html">Explore solutions &rarr;</a></div>
</div></div></section>

<section class="section alt"><div class="container"><div class="center"><span class="eyebrow">Our approach</span><h2>How we deliver</h2>
<p class="lead">Six principles guide every project, whether it is a new build, an AI initiative, a product rollout or ongoing support.</p></div>
<div class="grid grid-3" style="margin-top:40px">{"".join(f'<div class="card reveal"><h3>{t}</h3><p>{d}</p></div>' for t,d in APPROACH)}</div>
</div></section>

<section class="section"><div class="container"><div class="center"><span class="eyebrow">Technology expertise</span><h2>Modern, proven, open technology</h2>
<p class="lead">We build on widely adopted open standards and open-source foundations, so your software is maintainable and free of lock-in.</p></div>
<div class="grid grid-3" style="margin-top:40px">{"".join(f'<div class="card reveal"><h3>{t}</h3><p>{d}</p></div>' for t,d in TECH)}</div>
</div></section>

<section class="section alt"><div class="container grid grid-2" style="align-items:center;gap:48px">
<div><span class="eyebrow">Security &amp; compliance</span><h2>Your data, protected by design</h2>
<p class="lead">The organisations we build for handle sensitive financial, personal and institutional data. We treat protecting it as a core part of the job.</p></div>
<div class="card" style="height:auto"><ul class="checklist">
<li>Role-based access control and single sign-on</li>
<li>Encryption of data in transit and at rest</li>
<li>Complete audit trails for sensitive actions</li>
<li>Support for India's Digital Personal Data Protection (DPDP) Act, 2023</li>
<li>Data residency and on-premises deployment options</li>
<li>Responsible AI: human review of AI outputs, guardrails, and private model options for sensitive data</li>
<li>NDAs and data-processing agreements on request</li>
</ul></div>
</div></section>

<section class="section"><div class="container center"><span class="eyebrow">Our values</span><h2>What we stand for</h2>
<div class="grid grid-3" style="margin-top:32px;text-align:left">
<div class="card reveal"><h3>Quality</h3><p>Careful engineering and thorough testing behind every release.</p></div>
<div class="card reveal"><h3>Integrity</h3><p>We say what we will do, do what we say, and are honest when something changes.</p></div>
<div class="card reveal"><h3>Security &amp; privacy</h3><p>We treat our clients' data as our own and build in protection from day one.</p></div>
<div class="card reveal"><h3>Ownership</h3><p>We stay accountable for the software after go-live.</p></div>
<div class="card reveal"><h3>Simplicity</h3><p>Software that users understand and administrators can manage.</p></div>
<div class="card reveal"><h3>Continuous learning</h3><p>We keep our skills and products current with modern technology.</p></div>
</div></div></section>

<section class="section alt"><div class="container center"><span class="eyebrow">Careers</span><h2>Build with us</h2>
<p class="lead">We are always glad to hear from engineers, designers and consultants who care about building software properly. Send your profile to <a href="mailto:{EMAIL}?subject=Careers">{EMAIL}</a>.</p></div></section>
{cta("Let's work together","Tell us about your organisation and what you want to achieve. We'll come back with a clear plan.")}
"""

# ---------- CONTACT
opts = '<optgroup label="Services">' + "".join(f'<option value="{t}">{t}</option>' for _,t,_,_ in SERVICES) + '</optgroup><optgroup label="Solutions">' + "".join(f'<option value="{t}" data-key="{k}">{t}</option>' for k,t,_,_,_,*_ in PRODUCTS) + '</optgroup><option>Something else</option>'
FAQ = [
 ("Can you build AI or generative AI solutions for our specific needs?","Yes. We start with your business problem and data, identify where AI adds real value, and then build anything from a quick proof of concept to a production system: assistants on your own documents, ML prediction models, document data extraction or AI agents that automate workflows."),
 ("Is our data safe when you use AI?","Yes. We design AI solutions with access controls, data minimisation and human review. For sensitive data we can use private or on-premises models so your data never leaves your infrastructure."),
 ("Which AI models do you work with?","We are model-agnostic. We work with leading commercial models such as OpenAI, Anthropic Claude and Google Gemini, as well as open-source models that can be hosted privately, and choose based on your accuracy, cost and privacy needs."),
 ("How do we start working together?","Send us a short description of your requirement. We set up a discovery call, understand your goals and constraints, and then share a proposal with scope, timeline and cost."),
 ("Can your products be customised for our organisation?","Yes. Our solutions are configurable, and we also build custom extensions and integrations with your existing systems."),
 ("Do you deploy in the cloud or on our own servers?","Either. Our software runs in the cloud, in a private cloud, or on-premises on your own infrastructure, depending on your security and compliance needs."),
 ("Do you support software you did not build?","Yes. We take over maintenance and support of existing applications after an initial assessment of the code and environment."),
 ("How do you protect our data?","Role-based access, encryption, audit trails and secure development practices are standard. We can sign NDAs and data-processing agreements, and we support the requirements of India's DPDP Act, 2023."),
]
faq = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in FAQ)
contact = f"""
<section class="page-hero"><div class="container"><span class="eyebrow">Contact</span><h1>Let's talk about your project</h1>
<p class="lead">Tell us what you need, whether it's a new application, a product demo or support for an existing system.</p></div></section>
<section class="section"><div class="container grid grid-2" style="align-items:start;grid-template-columns:repeat(auto-fit,minmax(300px,1fr))">
<div class="card" style="height:auto">
<h2 style="font-size:1.35rem">Send us a message</h2>
<form id="contact-form" data-to="{EMAIL}" novalidate>
<div class="form-row"><div><label for="name">Full name *</label><input id="name" name="name" required autocomplete="name"></div>
<div><label for="email">Work email *</label><input id="email" name="email" type="email" required autocomplete="email"></div></div>
<div class="form-row"><div><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
<div><label for="company">Company / institution</label><input id="company" name="company" autocomplete="organization"></div></div>
<div><label for="topic">Interested in</label><select id="topic" name="topic">{opts}</select></div>
<div><label for="message">How can we help? *</label><textarea id="message" name="message" required minlength="10" placeholder="Briefly describe your requirement, timeline and any systems involved"></textarea></div>
<div class="sr-only" aria-hidden="true"><label for="website">Leave this empty</label><input id="website" name="website" tabindex="-1" autocomplete="off"></div>
<div><button class="btn btn-primary" type="submit" style="cursor:pointer">Send message</button></div>
<p class="form-note">Sending opens your email app with the message ready. See our <a href="privacy.html">privacy policy</a>.</p>
<p id="form-status" class="form-note" role="status" aria-live="polite"></p>
</form></div>
<div>
<div class="contact-item"><div class="icon">{I["mail"]}</div><div><h3>Email</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a> <button type="button" class="btn-sm" data-copy="{EMAIL}">Copy</button></p></div></div>
<div class="contact-item"><div class="icon">{I["pin"]}</div><div><h3>Location</h3><p>India. We work with clients across India and abroad.</p></div></div>
<div class="contact-item"><div class="icon">{I["headset"]}</div><div><h3>Existing clients</h3><p>For support on a deployed system, email us with your organisation name and a short description of the issue.</p></div></div>
</div></div></section>
<section class="section alt"><div class="container"><div class="center"><span class="eyebrow">FAQ</span><h2>Frequently asked questions</h2></div>
<div class="faq">{faq}</div></div></section>
"""

# ---------- LEGAL
privacy = f'''
<section class="page-hero"><div class="container"><h1>Privacy policy</h1><p class="lead">Last updated: 8 October 2026</p></div></section>
<section class="section"><div class="container prose">
<p>This policy explains how {LEGAL} ("TechSutra Labs Ventures", "we", "us") handles personal data collected through techsutralabs.com.</p>
<h2>What we collect</h2><p>This website does not use cookies for tracking or advertising. If you contact us by email, we receive the information you choose to send: usually your name, email address, organisation and message.</p>
<h2>How we use it</h2><p>We use it only to respond to your enquiry and, where you engage us, to provide our services. We do not sell or rent personal data.</p>
<h2>Retention</h2><p>We keep enquiry correspondence only as long as needed for the purpose it was shared for, or as required by law.</p>
<h2>Your rights</h2><p>Under the Digital Personal Data Protection Act, 2023 and other applicable law, you may ask us to access, correct or erase your personal data, or withdraw consent. Write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Third parties</h2><p>The site loads fonts from Google Fonts, which may receive your IP address. Our web host may keep standard server logs.</p>
<h2>Changes</h2><p>We may update this policy and will change the date above when we do.</p>
</div></section>'''
terms = f'''
<section class="page-hero"><div class="container"><h1>Terms of use</h1><p class="lead">Last updated: 8 October 2026</p></div></section>
<section class="section"><div class="container prose">
<p>techsutralabs.com is operated by {LEGAL} ("TechSutra Labs Ventures", "we", "us"). By using the site you agree to these terms.</p>
<h2>Content</h2><p>Content on this site is for general information about TechSutra Labs Ventures and its services. It is not an offer or contract; specific engagements are governed by separate written agreements.</p>
<h2>Intellectual property</h2><p>The site's text, design, logos and product names belong to {LEGAL} unless stated otherwise. You may not reproduce them without permission.</p>
<h2>Liability</h2><p>We aim to keep information accurate but provide the site "as is", without warranties. We are not liable for losses arising from use of the site.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of India.</p>
<h2>Contact</h2><p>Questions: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></section>'''
notfound = '''<section class="page-hero"><div class="container center"><h1>Page not found</h1><p class="lead">The page you're looking for doesn't exist or has moved.</p><a class="btn btn-primary" href="index.html">Back to home</a></div></section>'''

pages = [
 ("index.html","TechSutra Labs Ventures | Software, AI/ML & GenAI Solutions, IT Services","TechSutra Labs Ventures builds software, AI, ML and generative AI solutions and AI-powered enterprise products, with IT services and long-term support for businesses and institutions.",home),
 ("services.html","Services | TechSutra Labs Ventures","AI, ML and generative AI solutions, software development, cloud platforms, support and maintenance, system integration, IT consulting, data management and technical support.",services),
 ("solutions.html","Solutions | TechSutra Labs Ventures","AI-powered enterprise products: document management, loan origination, contract management, campus payments, low-code BPM and business rule engine.",solutions),
 ("about.html","About Us | TechSutra Labs Ventures","About TechSutra Labs Ventures (TechSutraLabs Ventures (OPC) Private Limited): who we are, what we do, our approach, technology expertise and values.",about),
 ("contact.html","Contact | TechSutra Labs Ventures","Contact TechSutra Labs Ventures about software development, IT services or our products.",contact),
 ("privacy.html","Privacy Policy | TechSutra Labs Ventures","Privacy policy for techsutralabs.com.",privacy),
 ("terms.html","Terms of Use | TechSutra Labs Ventures","Terms of use for techsutralabs.com.",terms),
 ("404.html","Page not found | TechSutra Labs Ventures","Page not found.",notfound),
]
for f,t,d,b in pages:
    open(os.path.join(OUT,f),"w").write(page(f,t,d,b))
open(os.path.join(OUT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
urls="".join(f"<url><loc>{SITE}/{'' if f=='index.html' else f}</loc><lastmod>{__import__('datetime').date.today().isoformat()}</lastmod></url>" for f,*_ in pages if f!="404.html")
open(os.path.join(OUT,"sitemap.xml"),"w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
HTACCESS = """ErrorDocument 404 /404.html
Options -Indexes
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set X-Frame-Options "SAMEORIGIN"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
  Header set Permissions-Policy "camera=(), microphone=(), geolocation=()"
</IfModule>
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css "access plus 7 days"
  ExpiresByType application/javascript "access plus 7 days"
  ExpiresByType image/png "access plus 30 days"
</IfModule>
"""
open(os.path.join(OUT,".htaccess"),"w").write(HTACCESS)
os.makedirs(os.path.join(OUT,".well-known"),exist_ok=True)
open(os.path.join(OUT,".well-known","security.txt"),"w").write(f"Contact: mailto:{EMAIL}\nExpires: 2027-10-18T00:00:00.000Z\nPreferred-Languages: en\nCanonical: {SITE}/.well-known/security.txt\n")
print("done")
