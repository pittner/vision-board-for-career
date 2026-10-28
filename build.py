#!/usr/bin/env python3
"""Builds index.html for pittner/vision-board-for-career.

A single-purpose page for the seasonal "career vision board" / "career goals 2027" intent (people
review their work year and plan a raise, a promotion or a new job in December-January): 36 career
goals in 6 groups, each with why it matters and a first step for this week, and a link that opens the
free maker with that goal and step already filled in (?goal=&step=&layout=text&mode=wallpaper, T-098),
so it can go on the phone lock screen or the desk. Plus 12 questions for a year-end career review,
a 45-minute plan, a box for your own career goal, and FAQ.

No dependencies. Run: python3 build.py
"""
import html as _html
import json
import pathlib
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
URL = "https://pittner.github.io/vision-board-for-career/"
SRC = "ghpages_career"
CAMPAIGN = "career_2027"

# (group, [(career goal, why it matters, a first step for this week)])
GROUPS = [
    ("Pay and promotion", [
        ("Get a 10% raise in 2027", "A raise you ask for with evidence is a raise you can get.", "Write down five results from 2026 with numbers next to them"),
        ("Be promoted to the next level", "Promotions go to people who already act one level up.", "Ask your manager what the next level needs that you do not show yet"),
        ("Know what my job pays on the market", "You cannot negotiate a number you do not know.", "Check three salary reports for your role and city and note the range"),
        ("Have a career talk with my manager every quarter", "Surprises at review time come from silence during the year.", "Book 30 minutes with your manager for January and name the topic"),
        ("Keep a wins file", "At review time you forget most of what you did.", "Create a note called Wins 2027 and add one thing from this week"),
        ("Negotiate one benefit that matters to me", "Remote days, training budget or extra leave can be worth more than money.", "Pick the one benefit you want most and write why it helps the company"),
    ]),
    ("New job or career change", [
        ("Land a better job by summer", "A deadline turns 'someday' into a weekly plan.", "Write the three things your next job must have and the one it must not"),
        ("Switch to a new field", "Most career changes start as a side project, not a jump.", "Find three people who work in that field and read their profiles"),
        ("Talk to one person a week in the role I want", "Short conversations open doors that job boards never show.", "Send one message asking for a 15-minute call"),
        ("Update my CV so it shows results", "Recruiters read results, not duties.", "Rewrite your top three CV lines as 'did X, which led to Y'"),
        ("Apply to five jobs I really want", "Five careful applications beat fifty copied ones.", "Save five job ads and mark what each one asks for most"),
        ("Pass an interview with confidence", "Confidence comes from practice, not talent.", "Write answers to the three questions you fear most and say them out loud"),
    ]),
    ("Skills and learning", [
        ("Learn one skill the market pays for", "The right skill raises your price for years.", "Look at ten job ads one level up and count the skills that repeat"),
        ("Finish one certificate or course", "A finished course beats three started ones.", "Pick one course and block two hours a week in your calendar"),
        ("Get good at AI tools for my work", "People who use AI well will replace people who do not.", "Pick one weekly task and try to do it with an AI assistant"),
        ("Read 12 books about my field", "One book a month adds up to a year of new ideas.", "Choose the first book and put it next to your bed"),
        ("Speak or present with less fear", "Being able to explain your work is half of being promoted.", "Volunteer for one five-minute update in the next team meeting"),
        ("Improve my English (or another language) for work", "A language opens jobs in other countries and bigger companies.", "Do 15 minutes today and set a daily reminder"),
    ]),
    ("Visibility and network", [
        ("Refresh my LinkedIn profile", "Recruiters search for you before they write to you.", "Update your headline to say what you do and for whom"),
        ("Post about my work once a month", "People hire and promote those they have heard of.", "Write down 12 things you learned at work, one post per month"),
        ("Find a mentor", "Someone two steps ahead can save you years.", "Name three people you admire and ask one for 20 minutes"),
        ("Help someone else grow", "Mentoring others shows you are ready to lead.", "Offer a newer colleague one hour of help this week"),
        ("Go to one industry event per quarter", "One good conversation can change a career.", "Find the next meetup or conference and put it in the calendar"),
        ("Get three recommendations", "Other people's words carry more weight than your own.", "Ask one former colleague for a short recommendation"),
    ]),
    ("Work-life balance", [
        ("Log off at a fixed time", "Rested people do better work and make fewer mistakes.", "Set a daily alarm called 'close the laptop'"),
        ("Take all my holiday days", "Unused leave is unpaid work.", "Put your first holiday week of 2027 in the calendar now"),
        ("No work email on weekends", "Your brain needs two days that belong only to you.", "Remove work email from your phone home screen"),
        ("Two hours of deep work every day", "The work that gets you promoted needs quiet time.", "Block 9 to 11 tomorrow and turn off notifications"),
        ("Fewer meetings, shorter meetings", "Every meeting you skip gives back time to think.", "Decline or shorten one recurring meeting this week"),
        ("Move during the workday", "A short walk clears the head better than more coffee.", "Take a 10-minute walk after lunch every day this week"),
    ]),
    ("Own projects and money", [
        ("Start a side project", "A side project can become a new career or extra income.", "Write down three ideas and spend one hour on the best one"),
        ("Earn the first euro outside my job", "One small sale proves someone will pay for your skill.", "Offer one paid hour of your skill to someone you know"),
        ("Build a portfolio of my best work", "Showing beats telling in every interview.", "Collect your three best pieces of work in one folder"),
        ("Save three months of salary", "Savings give you the courage to say no to a bad job.", "Set up an automatic transfer on payday"),
        ("Go freelance or part-time freelance", "Your own clients mean your own rules.", "Ask two contacts if they would pay for your help"),
        ("Celebrate every career win", "Noticing progress keeps you going in the hard months.", "Write down three work wins from 2026 and tell someone"),
    ]),
]

QUESTIONS = [
    "What work in 2026 made me proud?",
    "What did I do that gave me energy, and what drained it?",
    "Which result of mine helped the company the most?",
    "What did I learn this year that I did not know a year ago?",
    "Am I paid fairly for what I do now?",
    "Who helped my career this year, and did I thank them?",
    "What do I want to stop doing at work in 2027?",
    "If I stay in this job, where am I in two years?",
    "If I leave, what would I miss and what would I not?",
    "Which skill would most raise my value next year?",
    "What would my ideal workday look like?",
    "If 2027 goes really well at work, what is different a year from now?",
]

PLAN = [
    ("10 minutes: look back.", "Write three work wins and three frustrations of 2026. Open your calendar and sent emails to remember what you really did."),
    ("15 minutes: answer the questions.", "Go through the 12 questions below. Short, honest answers are enough."),
    ("10 minutes: pick three career goals.", "One for pay or the next role, one for skills, one for your balance or your own project."),
    ("10 minutes: make it visible.", "Turn your most important goal and its first step into a phone lock screen, print it for your desk, or make a full board."),
]

FAQ = [
    ("What is a career vision board?",
     "A board with your work goals for the coming year, such as a raise, a promotion, a new job, a new skill or more balance. "
     "It keeps your career goals in front of you, so busy weeks do not push them aside."),
    ("How do you make a career vision board?",
     "Look back at your work year, answer a few honest questions, pick three career goals and make them visible. "
     "This page has 36 career goals with a first step, 12 year-end career questions and a 45-minute plan."),
    ("What should I put on a career vision board?",
     "Goals for pay and promotion, a new job or field, skills, your network, work-life balance and your own projects. "
     "Add one first step to each goal so the board says what to do this week, not only what to hope for."),
    ("Does a vision board help with getting a new job or a raise?",
     "It helps if it is concrete. A number, a date and a first step turn a wish into a plan you see every time you unlock your phone."),
    ("Is the maker free?",
     "Yes. It runs in your browser, needs no account and uploads nothing. Save the image to your phone or print it for your desk."),
    ("Can I make a full vision board with several career goals?",
     "Yes. Start from your career goal in the AI vision board generator: you see a free preview, and unlocking the full-size board is optional (8.99 EUR)."),
]

def e(s):
    return _html.escape(s, quote=True)


def link(path, **extra):
    q = dict(extra)
    q.update({"utm_source": SRC, "utm_medium": "referral", "utm_campaign": CAMPAIGN})
    return "https://visionboard.bemooore.com" + path + "?" + urlencode(q)


def maker(goal, step, content):
    return link("/free-vision-board-maker/", goal=goal, step=step, layout="text", mode="wallpaper", utm_content=content)


TOOL = link("/free-vision-board-maker/", mode="wallpaper", layout="text", utm_content="plan_tool")
AI = link("/en/create.php", utm_content="faq_ai")
AI_PLAN = link("/en/create.php", utm_content="plan_ai")
HOME = link("/", utm_content="footer_home")


def slug(s):
    return "-".join("".join(c if c.isalnum() else " " for c in s.lower()).split())


def build():
    count = sum(len(gs) for _, gs in GROUPS)
    nav = " ".join(f'<a class="chip" href="#{slug(g)}">{e(g)}</a>' for g, _ in GROUPS)
    blocks = []
    for g, goals in GROUPS:
        cards = []
        for i, (goal, why, step) in enumerate(goals, 1):
            cid = f"{slug(g)}_{i}"
            cards.append(
                f'      <div class="wcard" id="g-{cid}"><h3>{e(goal)}</h3><p>{e(why)}</p>'
                f'<p class="step"><span>First step this week:</span> {e(step)}</p>'
                f'<a class="btn" href="{e(maker(goal, step, "goal_" + cid))}" data-cta="goal_{cid}">Make it my lock screen</a></div>')
        blocks.append(f'  <section class="grp" id="{slug(g)}">\n    <h2>{e(g)}</h2>\n    <div class="grid">\n'
                      + "\n".join(cards) + "\n    </div>\n  </section>")
    questions = "\n".join(f"    <li>{e(q)}</li>" for q in QUESTIONS)
    plan = "\n".join(f"    <li><b>{e(a)}</b> {e(b)}</li>" for a, b in PLAN)
    faq_html = "\n".join(f"  <h3>{e(q)}</h3>\n  <p>{e(a)}</p>" for q, a in FAQ)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False)
    page = TEMPLATE
    for k, v in {
        "%%NAV%%": nav, "%%GROUPS%%": "\n\n".join(blocks), "%%QUESTIONS%%": questions, "%%PLAN%%": plan,
        "%%FAQ%%": faq_html, "%%LD%%": ld, "%%COUNT%%": str(count), "%%NQ%%": str(len(QUESTIONS)),
        "%%TOOL%%": e(TOOL), "%%AI%%": e(AI), "%%AIPLAN%%": e(AI_PLAN), "%%HOME%%": e(HOME),
        "%%URL%%": URL, "%%SRC%%": SRC, "%%CAMPAIGN%%": CAMPAIGN,
    }.items():
        page = page.replace(k, v)
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print("index.html", len(page.encode()), "bytes,", count, "goals")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Career Vision Board 2027: %%COUNT%% Career Goals, %%NQ%% Year-End Questions &amp; a Free Maker</title>
<meta name="description" content="Plan your work year 2027: %%COUNT%% career goals (raise, promotion, new job, skills, balance), each with a first step for this week, %%NQ%% year-end career questions and a 45-minute plan. Turn your goal into a free lock screen. No signup.">
<link rel="canonical" href="%%URL%%">
<meta property="og:type" content="website">
<meta property="og:title" content="Career vision board 2027 - %%COUNT%% career goals and a free maker">
<meta property="og:description" content="Career goals with a first step, %%NQ%% year-end questions, and a lock screen in one click. Free, no signup.">
<meta property="og:url" content="%%URL%%">
<style>
:root{--ink:#111827;--muted:#6B7280;--rule:#E5E7EB;--acc:#1D4ED8;--bg:#F8FAFD}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
a{color:var(--acc)}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px}
header.hero{padding:48px 0 18px}
h1{font:600 clamp(28px,4.4vw,42px)/1.15 Georgia,"Times New Roman",serif;margin:0 0 14px;letter-spacing:-.01em}
.lede{font-size:18px;color:#374151;max-width:64ch;margin:0 0 14px}
.meta{font-size:14px;color:var(--muted);margin:0}
.btn{appearance:none;display:inline-block;text-decoration:none;border:1px solid #D1D5DB;background:#fff;color:var(--ink);padding:9px 15px;border-radius:999px;font:500 14px/1 inherit;cursor:pointer}
.btn:hover{border-color:var(--acc);color:var(--acc)}
.btn.primary{background:var(--acc);border-color:var(--acc);color:#fff}
.btn.primary:hover{background:#1E40AF;color:#fff}
.own{background:#fff;border:1px solid var(--rule);border-radius:16px;padding:18px;margin:8px 0 22px}
.own h2{font:600 21px/1.3 Georgia,serif;margin:0 0 10px}
.own .row{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1.3fr) auto;gap:8px;align-items:end}
@media (max-width:760px){.own .row{grid-template-columns:1fr}}
.own label{display:block;font-size:13px;color:var(--muted);margin:0 0 4px}
.own input{width:100%;border:1px solid #D1D5DB;border-radius:10px;padding:10px 12px;font:16px/1.3 inherit;background:#fff}
.own input:focus{outline:2px solid var(--acc);outline-offset:1px;border-color:var(--acc)}
#ownMsg{font-size:13px;color:var(--muted);margin:8px 0 0}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 6px}
.chip{display:inline-block;text-decoration:none;border:1px solid var(--rule);background:#fff;color:#374151;padding:6px 12px;border-radius:999px;font-size:14px}
.chip:hover{border-color:var(--acc);color:var(--acc)}
section.grp{padding:22px 0 8px}
section.grp h2{font:600 24px/1.25 Georgia,serif;margin:0 0 12px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
@media (max-width:860px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:520px){.grid{grid-template-columns:1fr}}
.wcard{background:#fff;border:1px solid var(--rule);border-radius:14px;padding:14px 14px 16px;display:flex;flex-direction:column}
.wcard h3{font:600 19px/1.25 Georgia,serif;margin:0 0 6px}
.wcard p{margin:0 0 8px;color:#374151;font-size:15px}
.wcard .step{font-size:14px;color:var(--muted);flex:1}
.wcard .step span{color:var(--acc);font-weight:600}
.wcard .btn{align-self:flex-start}
section.block{padding:30px 0;border-top:1px solid var(--rule);margin-top:20px}
section.block h2{font:600 24px/1.25 Georgia,serif;margin:0 0 8px}
section.block>p{max-width:70ch;color:#374151}
ol.how,ol.qs{max-width:70ch;color:#374151;padding-left:22px}
ol.how li,ol.qs li{margin:0 0 10px}
.faq h3{font:600 16px/1.4 inherit;margin:18px 0 4px}
.faq p{margin:0;color:#374151;max-width:70ch}
footer{padding:28px 0 60px;font-size:14px;color:var(--muted);border-top:1px solid var(--rule)}
</style>
</head>
<body>
<div class="wrap">
<header class="hero">
  <h1>Career vision board 2027: %%COUNT%% career goals with a first step for this week</h1>
  <p class="lede">Year-end reviews, raise talks and January job ads all come at once. Decide what you want from your work in 2027 before someone else decides for you. Below are %%COUNT%% career goals, each with why it matters and a first step you can do this week, plus %%NQ%% honest year-end career questions. Press a goal and it opens in a free maker with the first step under it: save it as your phone lock screen or print it for your desk. No signup, nothing uploaded.</p>
  <p class="meta">%%COUNT%% goals in 6 groups &middot; %%NQ%% year-end questions &middot; 45-minute plan &middot; lock screen or desk page &middot; free, MIT licensed</p>
</header>

<div class="own" id="own">
  <h2>Already know your career goal?</h2>
  <div class="row">
    <div><label for="ownGoal">My career goal for 2027</label><input id="ownGoal" maxlength="120" placeholder="e.g. Get a 10% raise in 2027" autocomplete="off"></div>
    <div><label for="ownStep">First step (optional)</label><input id="ownStep" maxlength="120" placeholder="e.g. Write down five results with numbers" autocomplete="off"></div>
    <button class="btn primary" id="ownGo" type="button">Make it my lock screen</button>
  </div>
  <p id="ownMsg">Opens the free maker with your goal filled in. Change colors or layout there, then save it to your phone or print it for your desk.</p>
</div>

<nav class="chips" aria-label="Groups">%%NAV%% <a class="chip" href="#questions">%%NQ%% year-end questions</a> <a class="chip" href="#plan">45-minute plan</a></nav>

%%GROUPS%%

<section class="block" id="questions">
  <h2>%%NQ%% year-end questions before you choose</h2>
  <p>Answer them alone, with a notebook, in 15 minutes. Be honest, nobody else reads it. The answers that surprise you point to your career goals.</p>
  <ol class="qs">
%%QUESTIONS%%
  </ol>
</section>

<section class="block" id="plan">
  <h2>Plan your work year in 45 minutes</h2>
  <ol class="how">
%%PLAN%%
  </ol>
  <p><a class="btn primary" href="%%TOOL%%" data-cta="plan_tool">Open the free lock-screen maker</a>
     <a class="btn" href="%%AIPLAN%%" data-cta="plan_ai">Make a full board with several goals</a></p>
</section>

<section class="block faq">
  <h2>Questions</h2>
%%FAQ%%
  <p style="margin-top:16px"><a class="btn" href="%%AI%%" data-cta="faq_ai">Make a full vision board around my career goals</a></p>
</section>

<footer>
  MIT licensed &middot; published by the team behind
  <a href="%%HOME%%" data-cta="footer_home">visionboard.bemooore.com</a> &middot;
  more: <a href="https://pittner.github.io/vision-board-for-small-business/">small business vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-family/">family vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-couples/">vision board for couples</a>,
  <a href="https://pittner.github.io/vision-board-for-students/">vision board for students</a>,
  <a href="https://pittner.github.io/vision-board-party-kit/">vision board party kit</a>,
  <a href="https://pittner.github.io/word-of-the-year-2027/">word of the year 2027</a>,
  <a href="https://pittner.github.io/2027-vision-board-template/">printable 2027 vision board template</a>,
  <a href="https://pittner.github.io/vision-board-prompts/">54 vision board prompts</a>,
  <a href="https://pittner.github.io/">all free tools</a> &middot;
  <a href="https://github.com/pittner/vision-board-for-career">source</a>
</footer>
</div>

<script type="application/ld+json">
%%LD%%
</script>

<script>
(function(){
  var EP='https://visionboard.bemooore.com/api/event.php',P='%%SRC%%',engaged=false;
  function beacon(ev,label){
    try{
      var b=JSON.stringify({event:ev,utm:P+' | '+label+' | '+location.search});
      if(navigator.sendBeacon){navigator.sendBeacon(EP,new Blob([b],{type:'text/plain'}));}
      else{fetch(EP,{method:'POST',body:b,keepalive:true,mode:'no-cors'});}
    }catch(e){}
  }
  // Every link to our site carries where the visitor came from (e.g. chatgpt.com).
  var src=(location.search.match(/[?&]utm_source=([^&]+)/)||[])[1]||(document.referrer?document.referrer.split('/')[2]:'direct');
  Array.prototype.forEach.call(document.querySelectorAll('a[data-cta][href*="visionboard.bemooore.com"]'),function(a){
    a.href+='&utm_term='+encodeURIComponent('via_'+src);
  });
  function engage(how){ if(engaged)return; engaged=true; beacon('page_engaged',how); }
  setTimeout(function(){engage('dwell6s');},6000);
  window.addEventListener('scroll',function(){
    var h=document.documentElement;
    if((h.scrollTop||document.body.scrollTop)/((h.scrollHeight-h.clientHeight)||1)>0.25) engage('scroll25');
  },{passive:true});
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-cta]'); if(a) beacon('cta_click',a.getAttribute('data-cta'));
  });

  // Own career goal: same prefill as the goal cards (?goal=&step=&layout=text&mode=wallpaper).
  var g=document.getElementById('ownGoal'),s=document.getElementById('ownStep'),msg=document.getElementById('ownMsg');
  function go(){
    var goal=g.value.trim(),step=s.value.trim();
    if(!goal){ msg.textContent='Type your career goal first.'; g.focus(); return; }
    var q=new URLSearchParams({goal:goal,layout:'text',mode:'wallpaper',utm_source:P,utm_medium:'referral',
      utm_campaign:'%%CAMPAIGN%%',utm_content:'own_goal',utm_term:'via_'+src});
    if(step) q.set('step',step);
    beacon('cta_click','own_goal');
    location.href='https://visionboard.bemooore.com/free-vision-board-maker/?'+q.toString();
  }
  document.getElementById('ownGo').addEventListener('click',go);
  [g,s].forEach(function(el){ el.addEventListener('keydown',function(e){ if(e.key==='Enter') go(); }); });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
