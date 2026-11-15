# Platform test Person A

**Interviewer**

Hello, we're picking up again with Person A, whom we've already interviewed. I'll remind you that it's still a simulation: Person A doesn't actually work in support, she's taking on the same role as in the interview. Today, it's not an interview, it's a test. We're going to show you a mockup, you're going to do a task, and the idea is that you think out loud: you say everything you're looking at, what you're looking for, what makes you hesitate. Me, during the test, I'm not going to help you, even if you ask me questions. That's normal, it's to see where it gets stuck. And it's the mockup we're testing, not you. Is that OK with you?

**Person A**

Yes, yes, sounds good. Well, talking at the same time, it's not very natural, but I'll try.

**Interviewer**

So the task: ticket T-48213. Studio Lune says it hasn't received the payment from Dupont, around 1,200 euros, from last week. You handle the ticket until the reply is sent. When you think it's done, you tell me.

**Person A**

OK. Well, first, your thing looks good. I see that I have quite a lot of info in the same place, that already I quite like, now we have to see what it says.

So on the left I have my tickets, there are four of them there, the first one is the right one, T-48213, Studio Lune. It's already open. In the middle, I have the customer's message. So I read: she hasn't received the payment from Dupont, about 1,200 euros, last week, it's urgent because she has to pay a supplier on Friday. And there it says "free message, sent without the form's transaction fields". There you go, typically, that, that's the ticket where there's nothing. No reference, "about 1,200", "last week". Me, usually, there, either I go search with the name, or I send her a message back to get the reference, and then we lose a day when it's something urgent. Well, she did put Dupont, that's something.

Then, on the right, there's the... the copilot, that's it. "Account pre-read". So the first thing I look at, me, is whether there's something on the record. Since my bank-change story, I always look at that first. There it says "no open flag", nothing open, no bank, no contract, no terms. Well, that, it's good that it's right at the top. If it's reliable, that would have avoided my mistake, that. It's, it's really not bad.

Next, "proposed transaction", and it says "confident match" in green. So confident, well, it's confident, me, I'm still going to look. TX-88412, 1,200 euros exactly, received on 3 November, payer DUPONT RENOVATION SARL. The 3rd, yes, that's indeed last week. And underneath, "where it is", now that's interesting. Payer's bank, collected on the 3rd. Ledgerly, received on the 3rd, grouped into transfer VO-2291, 3,480 euros, 3 payments. Merchant's bank, paid on the 5th to the account ending in 4471, no error code. Well, there you go. It's the grouped transfer. She didn't receive 1,200, she received 3,480 with two other payments in it, so she doesn't see it on her statement. That, we get loads of those. There, at a glance, I have everything. That's honestly not bad, that, I like your thing. Normally, that, that's three tools.

Then, "why this one", so why it chose that one. There are four lines, with a little green tick in front of each line. The amount, 1,200, OK. The date, the 3rd, OK. The name, Dupont, OK. And the fourth, "only payment from this payer in the last 30 days". So basically, it's telling me: it's the only payment from Dupont over the last 30 days, there isn't another one. Well. OK.

And just underneath, there's a little blue link, "2 other candidates ruled out", so two other payments it looked at and ruled out. It doesn't show them directly, you have to click. Me, I like to check what I'm doing, so I click, it opens. So, the first one, a Dupuis et Fils, 1,150, well, it's not the same name, that's fine. And the second... TX-88021, 1,200 euros, 20 October, DUPONT RENOVATION SARL. Wait. Dupont Rénovation, that's the same Dupont, that. So there's another payment from Dupont, on 20 October. And it, three lines above, with its green tick, it just told me that it was the only payment from Dupont over 30 days. 20 October, that's within the 30 days, right? So the green tick, there, it's wrong. There's an error in what it's showing me.

Well, careful, on the substance, it doesn't get the wrong payment. The right one is still the one from the 3rd, since she says last week, and the one from 20 October, it's too old. On that, I agree with it. But if it puts a green tick on something that's wrong, then, the other ticks, I don't trust them anymore. That, it would need to be fixed. Because a new person, they're going to see four green ticks, they're going to think "it's fine", they're not going to click to open the little list underneath, and they'll never see that there's a second Dupont.

Well. Underneath, I have the account history. On 14 October, ticket T-47102, same question about a grouped transfer, resolved by explaining the grouping. Ah, that, it's good that it's written there. Because we don't always have time to go look, or there are some who don't do it, to go faster. It's easy and quick there.

So, since 1 October, her payments are paid out in one transfer a day, it's a merchant setting. Well, there you go, that's why. She changed her setting, or someone at her business changed it, and she doesn't remember. And it's the second time she's asked the question. That, it's the kind of thing I usually go looking for in the old tickets, and here it's right in front of me.

Well, I confirm the transaction. "Confirm this transaction". There. Now, the draft appears. I read: "Hello Claire, the payment of €1,200.00 from DUPONT RENOVATION SARL, ref TX-88412, was received on 3 November. It was paid out to your account ending in 4471 on 5 November, grouped with two other payments in a single transfer of €3,480.00, ref VO-2291. That is the amount you will see on your bank statement." OK. It's right. The references are in blue, it says they come from the ledger, that they're not typed. That's good, because sometimes we make mistakes like that.

On the other hand, something's missing. She already asked the question on 14 October. If I just tell her "it's in a grouped transfer", she'll be back in three weeks. You have to tell her why: since 1 October, it's one transfer a day, it's her setting, and if she wants to change it, it's in her space. And then she mentions her supplier on Friday, you have to reassure her: the money has already been in her account since the 5th. So I'm going to edit. "Edit". OK, it opens. I add... "the money is already on your account since 5 November. Since 1 October your payments are paid out in one transfer a day; you can change this setting in your space." There, roughly. "Done editing".

And now I have "Checked: no refund or chargeback promised". Well, OK. On this ticket, it's not much use, but I imagine, on disputes, yes.

And then, I'd really like to see the two other payments in the transfer. If she replies to me "what are the two others in the 3,480?", I have to go look for them. Here, it tells me 3 payments, but it doesn't tell me which ones. Well, I'll do without. I send. "Send". There, "reply sent by you", linked to the ticket and logged. It's done, I think.

**Interviewer**

OK, thanks. The test is over, now I can ask you a few questions. What made you hesitate?

**Person A**

The 30-day line. That's the only moment I stopped. Because everything else, I was checking it, and it was fine, and there, all of a sudden, it's wrong. Me, I saw it because I always open everything, but I don't think everyone opens it. The new people especially, and then with the pace we have to keep to handle the tickets, well, to save time they're going to trust the machine and that's going to create errors. Because we have quotas on quality, a ticket that comes back, that's not good. And then, there are the two other payments in the transfer, that, that was missing for me.

**Interviewer**

And the last time you had a ticket like this one, without a reference, how did it go?

**Person A**

Oh well, grouped transfers, that's every week. Without a reference, there, with the name, I would have found it, but you have to open the dashboard, search for the merchant, filter, find the transfer, open the transfer, see what's in it, go look at the old tickets. I'd say ten minutes, a quarter of an hour if it's a mess. And if she hadn't put the name, then I send her a message back, and it's the next day. Here, I took what, three minutes, and even then, I took the time to open everything.

**Interviewer**

What did you expect to see instead?

**Person A**

That the green box doesn't talk nonsense, first of all. The rest, they're little extras that are really nice, that, I really liked: the list of payments in the transfer, and in the draft, the reason, when it's the second time she's asking. And then there's something I thought of when seeing the history: merchants like her, who ask the same question three times, it would be good to send them a little tutorial or a message to explain their setting to them, before they open a ticket. But well, that, that's no longer support, it's sales or I don't know.

**Interviewer**

OK. Is there anything else you want to add?

**Person A**

Well, me, what I'm wondering is about the tickets where we really have nothing. Here, she put Dupont, so it's easy. When the customer writes "my payment from last week" and he has three of them, what does it do? If it tells me "I don't know, ask him for the reference", that's fine by me, at least it doesn't make things up. Because those tickets, it's the new people who take them, and it's me who goes over them after.

**Interviewer**

OK, thank you. We'll stop there for Person A's test.
