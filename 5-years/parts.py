# Three tight parts cut from the raw 5-years Q&A. Each row is one contiguous
# span of the raw file: (start s, end s, speaker lines). Nothing is reworded;
# every row is words she or he actually said, in that order.
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

R, H = "Ruta", "Him"
PARTS = [
 ("Part 1. How we met, and the words we know", [
  (25.9, 46.9, [(R, "Привіт-привіт, ви мене знаєте як технічну продюсерку, але ви ніколи не бачили мого чоловіка. Але сьогодні ми 5 років разом, тому я відповім на ваші питання, які ви мені задали в Threads, про наші відносини. Хто не знає: чистокровний індієць, прям 100%, 24 на 7, народився в Індії, прожив в Індії.")]),
  (79.6, 96.6, [(R, "Where did we meet?"), (H, "Well, we met in Barcelona. I went from India, I was very young, I went to Barcelona to do some kind of stupid degree and wasted a lot of money. But I met you in Barcelona. So yeah."), (R, "Worth it?"), (H, "Worth it. Maybe.")]),
  (97.6, 99.8, [(R, "So what do you like about me?")]),
  (102.2, 106.1, [(H, "Oh my God, that's a different question. I like everything about you.")]),
  (112.5, 116.3, [(H, "You're kind, you take care of me, you love me.")]),
  (117.7, 118.6, [(H, "You're the best.")]),
  (121.7, 127.0, [(R, "Considering that we come from very different backgrounds, what brings us together?")]),
  (130.85, 149.0, [(H, "We are from different backgrounds, but as human beings we are very similar. Like, extremely similar. Like, we got together in like a week or so. We have to be similar. We moved in in six months."), (R, "So… but I think people think that because you're Indian and I'm Ukrainian, yeah, it's like so, so different.")]),
  (150.1, 165.8, [(H, "I think I'm not a stereotypical Indian, in a way. Like, I'm Indian, I love India, but my habits are not what you would consider stereotypical Indian. And you're Ukrainian, but you are not like… I think you're more open as well.")]),
  (184.0, 190.4, [(R, "Also, if we were not similar, there's no relationship."), (H, "Yeah, yeah. Very similar. That's the whole point.")]),
  (360.1, 363.1, [(R, "Which language do we speak?"), (H, "English.")]),
  (365.9, 367.6, [(H, "There's no other common language.")]),
  (371.9, 379.6, [(R, "At some point we kind of migrate into our own language in between, where each of us says our own words.")]),
  (385.0, 390.8, [(H, "And we never fully learned each other's language. We never really wanted to do it. But we do know a few words.")]),
  (412.6, 416.2, [(R, "I know some words in Indian, in Gujarati specifically.")]),
  (419.8, 425.9, [(R, "The most common words we say: arre yaar."), (H, "From me."), (R, "I love it. It just rolls off the tongue.")]),
  (433.6, 451.2, [(H, "Hey, you know a lot of curse words."), (R, "I know a lot of curse words. I know household words like chamchi. Chamchi is spoon. Gandari. Yeah, what else do I know? I know a lot of…"), (H, "You know, like, a lot of curse words. Yeah, she's gandari. Very gandari.")]),
  (453.1, 464.6, [(R, "What words do you know?"), (H, "I know a few. Blyat is one. I know pizda. They're all bad words. Then I know yob tvoyu mat."), (R, "Oh, my favourite.")]),
  (467.5, 470.2, [(R, "Hospody."), (H, "I know Hospody.")]),
  (475.6, 488.0, [(H, "Actually, I know some French words as well."), (R, "What was the French word your dad called?"), (H, "Connasse."), (R, "Connasse. I love it. I think that's my favourite foreign word. Connasse.")]),
 ]),
 ("Part 2. His parents, and our weird habits", [
  (238.1, 240.2, [(R, "How did your family accept me?")]),
  (242.8, 250.7, [(H, "As soon as my mom knew about it, she was over the moon. She was like, \"I was waiting for you. What were you doing?\"")]),
  (257.3, 258.8, [(R, "I think they like me more than they like you.")]),
  (261.2, 275.8, [(H, "My parents in general are very liberal compared to any Indian parent. And I think they like her way more than they like me. I think at this point I'm the adopted child and she's the original child.")]),
  (280.4, 290.9, [(R, "I have to give them props. Because considering that India is still pretty traditional, to let a complete foreigner, white as snow, into their home, live with them.")]),
  (291.9, 299.0, [(R, "There was a question: did I go to India? I did go to India. I lived there for a year, in their house, with their family, fully.")]),
  (317.3, 326.5, [(R, "They were so nice to me. Because, FYI, I cannot have spicy at all. Like, not even mustard."), (H, "Not even pepper."), (R, "Not even European spicy.")]),
  (331.5, 342.1, [(R, "They cooked for me separately. Every single Indian food was cooked for me separately, with no chili, no spice, nothing. And that was an insane amount of work.")]),
  (344.1, 351.7, [(R, "And I love Indian food without spice. Indian food, not spicy: it's delicious."), (H, "I disagree.")]),
  (353.8, 356.4, [(H, "It's not Indian food. It's Valeria food [?].")]),
  (646.9, 650.8, [(R, "What interesting habits does he have that seem strange to us?")]),
  (655.1, 665.7, [(R, "The weirdest for me is that we cannot cuddle. He doesn't like cuddling in his sleep because he feels…"), (H, "Claustrophobic. I have claustrophobia. Big one.")]),
  (680.4, 686.4, [(H, "Once I'm asleep, you can do that. But for me to be able to sleep, I need freedom.")]),
  (687.4, 696.1, [(R, "I'm the complete opposite. I love to be as close as possible, as cuddled as possible. So we are finding compromises.")]),
  (715.6, 717.7, [(H, "She has some weird habits as well.")]),
  (730.7, 736.8, [(H, "If you want to see where she has been in the house, you just have to see: okay, this is there, this is there, this is there.")]),
  (741.4, 752.8, [(H, "There is no place. There is no such thing as a place. Wherever she keeps it is the place. Also, she eats yogurt, and she eats pasta with yogurt. Who the hell eats that?")]),
  (753.5, 758.6, [(H, "I lived with some Italians when I was in Barcelona. If they knew her, she would be crucified.")]),
  (769.3, 776.9, [(R, "Sour cream is the best thing ever and it goes on everything. It is good. Галичина, sponsor me."), (H, "It is good, but who the hell eats it with pasta?")]),
  (780.2, 782.7, [(H, "That's a crime. I think that's a crime.")]),
 ]),
 ("Part 3. Food, and five years", [
  (820.6, 842.2, [(R, "Am I vegetarian now? Because he has been vegetarian from birth, all his life, never tried meat. And I was raised on sausage as young as I can remember, and a little dabble of beer and wine from like 10 years old. You know, the normal European stuff."), (H, "Alcoholics from childhood."), (R, "So I did not turn vegetarian.")]),
  (873.1, 876.7, [(H, "She cooks whatever she likes, I cook whatever I like.")]),
  (887.5, 892.6, [(R, "So he eats his food with spices and whatever, and I eat my pasta with yogurt.")]),
  (898.5, 903.9, [(R, "I like meat. But when I lived in India, I did turn completely vegetarian for that year.")]),
  (912.8, 923.9, [(R, "So I relied heavily on, like, vegan nuggets and cheese and all sorts of milk products."), (H, "India has the best vegetarian food…"), (R, "Not-spicy vegetarian."), (H, "…by a long shot.")]),
  (935.4, 937.8, [(R, "I still haven't tried butter chicken ever in my life.")]),
  (952.5, 968.0, [(R, "So, my favourite Indian food. Can you guess which ones are mine?"), (H, "So, definitely jalebi. She likes jalebi. She likes pav bhaji a lot. She likes palak paneer."), (R, "That was the first Indian food I tried.")]),
  (970.0, 973.7, [(H, "She likes gulab jamun, for example."), (R, "Vada pav."), (H, "Vada pav.")]),
  (976.1, 983.1, [(H, "She loves dahi puri as well."), (R, "Oh yes, I do. I forgot."), (H, "She loves chaat, bhel. She loves chaat a lot.")]),
  (987.6, 990.4, [(R, "You don't like anything from Ukrainian cuisine?")]),
  (991.3, 993.8, [(H, "I actually like, I like, uh, varenyky."), (R, "True."), (H, "I like varenyky.")]),
  (995.3, 1006.7, [(H, "I like the buckwheat thing your mom made."), (R, "Oh yeah, hrechka. And I made you borscht without meat."), (H, "Borscht is fantastic. Without meat, I don't know how authentic it is, but it is fantastic.")]),
  (1042.5, 1047.0, [(H, "Like, I used to live on varenyky in Ukraine. I could eat it every day. It was delicious.")]),
  (1061.2, 1073.3, [(H, "Also the bread chips."), (R, "Yes, грінки. And that video went viral, and I got so hated on in the comments."), (H, "Racism."), (R, "So many bots, so many… I had to close the comments.")]),
  (782.7, 807.1, [(R, "In general, five years together. Are you happy?"), (H, "Yes. Actually, without any jokes, I think I'm very happy. What do you think?"), (R, "I think it's the best. It just flew by."), (H, "Yeah. It's the best decision of my life, at least. I mean, we travelled so much and we did so many things."), (R, "I think we travelled to like 12 countries or something.")]),
  (811.4, 816.0, [(R, "And not just travelled. We actually lived there, like a month or two months.")]),
  (1082.5, 1084.4, [(R, "Say bye-bye."), (H, "Bye-bye.")]),
 ]),
]


def mmss(t):
    t = int(round(t))
    return f"{t // 60}:{t % 60:02d}"


out = ["# 5 years together: three parts", "",
       "Cut from the raw recording `20261022_164346.mp4`. Every line is words you actually said, in a contiguous span of the raw file; only cuts, no rewording. The timestamp on each line is where that span starts in the raw file, so the editor can find it.", "",
       "Lengths are the sum of the kept spans, measured from word-level timings: within a few seconds of the cut.", ""]
for title, rows in PARTS:
    dur = sum(e - s for s, e, _ in rows)
    out += [f"## {title} · about {mmss(dur)}", ""]
    for s, e, lines in rows:
        for i, (who, text) in enumerate(lines):
            stamp = f"`{mmss(s)}` " if i == 0 else ""
            out.append(f"{stamp}**{who}:** {text}  ")
        out.append("")
    print(f"{title}: {mmss(dur)} ({len(rows)} cuts)")
# usage: python 5-years/parts.py   -> work/5-years-parts.md + work/5y/spans.json
open(os.path.join(ROOT, "work", "5-years-parts.md"), "w", encoding="utf-8").write("\n".join(out))
json.dump([{"title": t, "spans": [[s, e] for s, e, _ in rows]} for t, rows in PARTS],
          open(os.path.join(ROOT, "work", "5y", "spans.json"), "w"), indent=1)
