---
title: "Crowdfunding’s Hamas Problem: A Gaza Fundraiser’s Telegram Badge Leads to an Al-Qassam Chat"
seo_title: "Crowdfunding’s Hamas Problem: Chuffed, GoFundMe and Gaza"
dek: "Both pages pay out to organizers in the United States and Australia. One wrote that the money would reach Gaza “probably via PayPal or a crypto wallet.” Hamas is a designated Foreign Terrorist Organization."
description: "Two Chuffed pages raised $12,948 and $6,736 for a Gaza man whose Telegram status badge traces to a chat named for al-Qassam, Hamas’s armed wing."
date: 2026-10-20
date_modified: 2026-10-20
slug: crowdfunding-hamas-chuffed-gofundme-gaza
canonical: https://www.octoprobe.ai/blog/crowdfunding-hamas-chuffed-gofundme-gaza/
section: Investigations
tags: [Investigation, OSINT, Counterterrorism, Terror Finance]
keywords: [Hamas, cryptocurrency, USDT, Tether, TRON, Foreign Terrorist Organization, crowdfunding, Chuffed, GoFundMe, Gaza fundraiser, terrorist financing, al-Qassam Brigades, Telegram, emoji status, inverted red triangle, PayPal, Stripe, material support, OSINT, identifier graph]
og_image: https://www.octoprobe.ai/blog/crowdfunding-hamas-chuffed-gofundme-gaza/assets/og-cover.png
byline: Colin Aamot
author: Colin Aamot
built_from: hand-authored HTML (blog/crowdfunding-hamas-chuffed-gofundme-gaza/index.html is the source of truth; this file is its Markdown copy. Do not rebuild the page from it with build-blog.py.)
faq:
  - q: "Is it illegal to give to a Gaza crowdfunding campaign?"
    a: "Not in itself. Federal law makes it a crime to knowingly provide material support or resources to a designated Foreign Terrorist Organization such as Hamas, and the Treasury Department has warned that Hamas raises money through sham charities that claim to help civilians in Gaza. Donors to individual appeals usually cannot see where the money goes after the organizer receives it."
  - q: "Does Chuffed allow fundraising for people in Gaza?"
    a: "Yes. The i Paper reported in August 2025 that Chuffed hosted nearly 10,000 campaign pages for Gazans. Chuffed’s terms bar content that breaches applicable laws but, unlike GoFundMe’s, do not mention terrorism or terrorist financing."
  - q: "Does GoFundMe ban terrorist financing?"
    a: "Yes. GoFundMe’s terms prohibit any activity in support of terrorism, terrorist financing, extremist financing, or money laundering, and its Israel–Gaza guidance says fundraising for any armed conflict is not allowed. GoFundMe also places Gaza-related fundraisers under review."
  - q: "What does the red inverted triangle emoji mean?"
    a: "The Anti-Defamation League says the inverted red triangle first appeared in propaganda videos from the al-Qassam Brigades, Hamas’s military wing, which used it to mark Israeli targets, and that it has come to represent Hamas itself. The ADL adds that context matters, because some users treat it as a general symbol of support for Palestine."
  - q: "How does Hamas collect cryptocurrency donations?"
    a: "According to FBI affidavits filed in federal court in Washington, D.C., in 2025 and 2026, the al-Qassam Brigades answered donors who emailed its fundraising address with a fresh USDT address on the TRON network for each transfer. Most of the money was swept into a single consolidation wallet and then moved through exchange accounts and over-the-counter brokers that can swap it for cash. Tether froze the USDT in 18 of those addresses at the U.S. government’s request in March 2025."
  - q: "How does money from a Chuffed campaign reach Gaza?"
    a: "Chuffed’s terms say PayPal and Stripe donations are paid to the campaign organizer’s PayPal or Stripe account at or around the time of the donation. What happens next is up to the organizer; the terms do not describe any onward transfer."
---

# Crowdfunding’s Hamas Problem: A Gaza Fundraiser’s Telegram Badge Leads to an Al-Qassam Chat

![Dark OctoProbe cover over a map of the Gaza Strip with a red pin near Deir al-Balah; at right, an abstract identifier graph links a stylized crowdfunding page to a cluster of nodes, beside the headline Crowdfunding’s Hamas Problem](https://www.octoprobe.ai/blog/crowdfunding-hamas-chuffed-gofundme-gaza/assets/cover.png)

*An abstract identifier graph over a map of the Gaza Strip. No real person is depicted. Illustration: OctoProbe News; map © OpenStreetMap contributors.*

**Do crowdfunding sites host Gaza fundraisers that carry open Hamas signals?**

They do, and the signals sit in plain view. Two live Chuffed campaigns have raised $12,948 and $6,736 for a Gaza man whose Telegram status badge comes from a channel that sends followers to a chat named for al-Qassam, Hamas’s armed wing. Treasury says Hamas exploits Gaza’s suffering to raise money.

The photo is the same on both pages: a young man in a black cap, in profile, against a field of rubble. On Chuffed, an Australian crowdfunding site, it heads two campaigns for “Ashraf,” a 23-year-old in Gaza. As of October 20, 2026, the older page showed $12,948 raised from 192 supporters. The newer one showed $6,736 from 99.

The same photo is the profile picture of the Telegram account @Ashrafgaza, which has posted links to both campaigns. That account wears a status badge from an emoji set called “Resistance-Toast.” A Telegram channel by the same name, with about 17,650 subscribers, points its readers to a group chat called “Al-Qassam Toast.” The Izz ad-Din al-Qassam Brigades are Hamas’s military wing.

Neither campaign mentions Hamas. Neither shows where the money goes after it lands. Chuffed pays donations straight to an organizer’s PayPal or Stripe account, and the onward route to Gaza is the organizer’s call. One organizer told donors the money would reach Ashraf “[probably via PayPal or a crypto wallet](https://chuffed.org/project/127156-help-ashrafs-family#:~:text=probably%20via%20PayPal%20or%20a%20crypto%20wallet).”

> Editor’s note: Hamas has been a [designated Foreign Terrorist Organization](https://www.state.gov/foreign-terrorist-organizations/) since October 8, 1997. Federal law punishes anyone who “[knowingly provides material support or resources to a foreign terrorist organization](https://www.law.cornell.edu/uscode/text/18/2339B).” Under OctoProbe’s standards, this report does not link the Telegram channel or chat described below.

## Key Takeaways

- [Two Chuffed campaigns for the same Gaza man, run by organizers in the United States and Australia, showed $12,948 and $6,736 raised on October 20, 2026.](#two-pages-one-photo)
- [Chuffed pays donations to the organizer at or around the time of each gift. One organizer said the money would move on “probably via PayPal or a crypto wallet.”](#paypal-or-a-crypto-wallet)
- [The man’s Telegram status badge comes from a “Resistance-Toast” emoji set. A channel of that name steers its 17,650 subscribers to a chat called “Al-Qassam Toast.”](#the-telegram-trail)
- [Crowdfunding pays out in ordinary money; Hamas asks for stablecoins. FBI affidavits list a dozen wallets tied to al-Qassam fundraising and trace about 1.35 million USDT into one of them in just over four months.](#the-conversion-cycle)
- [News reports have flagged fundraisers tied to Hamas supporters on both Chuffed and GoFundMe. Treasury says Hamas may have collected as much as $10 million a month through sham-charity donations.](#a-pattern-across-platforms)
- [GoFundMe’s terms ban terrorist financing by name. Chuffed’s terms do not mention terrorism.](#the-rules-on-paper)

## Two Pages, One Photo

The older campaign, “[Help Ashraf’s Family!](https://chuffed.org/project/127156-help-ashrafs-family),” went up on April 6, 2025. Its organizer lists a location in the United States. The story, signed by Ashraf, gives his age as 20. “[We have been displaced and are living in a tent in the city of Deir al-Balah](https://chuffed.org/project/127156-help-ashrafs-family#:~:text=We%20have%20been%20displaced%20and%20are%20living%20in%20a%20tent),” it reads. The page asked for $15,000. It had 192 supporters and 135 shares.

![Screenshot of a Chuffed campaign page titled Help Ashraf’s Family! by an organizer in the United States, showing $12,948 raised of $15,000, 192 supporters and 135 shares](https://www.octoprobe.ai/blog/crowdfunding-hamas-chuffed-gofundme-gaza/assets/chuffed-campaign-gaza-2025-header.jpg)

*The April 2025 campaign on October 20, 2026. Source: [Chuffed](https://chuffed.org/project/127156-help-ashrafs-family), captured October 20, 2026.*

The newer campaign, “[Help Ashraf and his family maintain their life in Gaza](https://chuffed.org/project/help-ashrafs-family-maintain-their-life-in-gaza),” went up on February 20, 2026, under an organizer in Australia. It asks for $10,000. “[I speak for my family of 10 members](https://chuffed.org/project/help-ashrafs-family-maintain-their-life-in-gaza#:~:text=I%20speak%20for%20my%20family%20of%2010%20members),” Ashraf wrote. The organizers’ write-up says they have spoken with him weekly “[For nearly three years](https://chuffed.org/project/help-ashrafs-family-maintain-their-life-in-gaza#:~:text=For%20nearly%20three%20years).”

![Screenshot of a Chuffed campaign page titled Help Ashraf and his family maintain their life in Gaza by an organizer in Australia, showing $6,736 raised of $10,000 and 99 supporters](https://www.octoprobe.ai/blog/crowdfunding-hamas-chuffed-gofundme-gaza/assets/chuffed-campaign-gaza-2026-header.jpg)

*The February 2026 campaign uses the same lead photo as the 2025 page. Source: [Chuffed](https://chuffed.org/project/help-ashrafs-family-maintain-their-life-in-gaza), captured October 20, 2026.*

The two pages are tied together three ways. They lead with the same photograph. They carry the same update, word for word, which opens, “My name is Ashraf, I’m 23 years old and living in Gaza with my family of 10.” And the Telegram account that uses that photograph as its profile picture has posted links to both.

> Chuffed shows each campaign’s total in the organizer’s home currency. The Australian page marks gifts in U.S. dollars separately, which indicates its $6,736 total is in Australian dollars. The two totals are not added together in this report for that reason.

## “Probably via PayPal or a Crypto Wallet”

Chuffed does not hold the money. Its terms say PayPal and Stripe donations “[will be paid to the Social Venture’s PayPal account or Stripe account at or around the time of your Donation](https://chuffed.org/terms-conditions#:~:text=will%20be%20paid%20to%20the%20Social%20Venture).” Both campaign pages tell donors the organizer “[will have quick and easy access to your donation](https://chuffed.org/project/help-ashrafs-family-maintain-their-life-in-gaza#:~:text=will%20have%20quick%20and%20easy%20access%20to%20your%20donation).”

That puts the last leg of the trip, from a Western bank account into Gaza, outside the platform’s view. The U.S. organizer spelled out the plan, writing of work with a small team to “[raise money for him, and transfer it to him probably via PayPal or a crypto wallet](https://chuffed.org/project/127156-help-ashrafs-family#:~:text=raise%20money%20for%20him).”

![Text from the 2025 Chuffed campaign in which the U.S. organizer writes that he is working with a small team to raise money for Ashraf and transfer it to him probably via PayPal or a crypto wallet](https://www.octoprobe.ai/blog/crowdfunding-hamas-chuffed-gofundme-gaza/assets/chuffed-2025-organizer-paypal-crypto-note.jpg)

*The U.S. organizer’s note on the 2025 campaign. Source: [Chuffed](https://chuffed.org/project/127156-help-ashrafs-family), captured October 20, 2026.*

Inside Gaza, Hamas runs its own financial plumbing. When the Treasury Department sanctioned a Gaza lender in October 2024, it described Al-Intaj Bank as “[an unlicensed Hamas-run bank in Gaza that provides financial services for Hamas despite not being connected to international banks](https://home.treasury.gov/news/press-releases/jy2632#:~:text=an%20unlicensed%20Hamas-run%20bank%20in%20Gaza).”

## The Telegram Trail

Screenshots gathered for an OctoProbe investigation show @Ashrafgaza working the campaigns hard. In a Telegram group called “Palestine Lives Matter,” which listed 1,810 members, he posted this appeal above the link to the 2026 campaign:

> A small donation or even a share could save a family struggling to survive. We are living through unimaginable hardship, constant bombardment, and harsh living conditions in Gaza, where every single day has become a fight for survival. I humbly ask for your support to help my family through these extremely difficult times—even the smallest contribution or share makes a world of difference to us. Our full story and details are available in the campaign link below. If you wish to verify our story or reach out directly, please feel free to send me a private message. Thank you for your compassion and humanity. 🙏
>
> — @Ashrafgaza, in the Telegram group “Palestine Lives Matter” (1,810 members), captured October 20, 2026

![Telegram group Palestine Lives Matter, 1,810 members, showing a post from Ashraf asking for a small donation or a share to help his family survive in Gaza, followed by a Chuffed link and a preview card for the campaign Help Ashraf and his family maintain their life in Gaza with a black-and-white photo of a young man in a cap](https://www.octoprobe.ai/blog/crowdfunding-hamas-chuffed-gofundme-gaza/assets/telegram-palestine-lives-matter-ashraf-chuffed-appeal.jpg)

*Ashraf’s appeal in the “Palestine Lives Matter” group, with the preview card for the February 2026 Chuffed campaign. Source: Telegram, captured October 20, 2026.*

It was not a one-time post. A search of the group returned 31 messages from the account, dating back at least to December 2024. Many carry a link to one of the two Chuffed pages, and the most recent ones repeat the 2026 link days apart.

![Telegram search results reading 31 messages found, listing posts from Ashraf dated from December 9, 2024, to October 2026, most showing a link fragment for the Chuffed campaigns help-ashrafs-family](https://www.octoprobe.ai/blog/crowdfunding-hamas-chuffed-gofundme-gaza/assets/telegram-ashraf-31-messages-recurring-chuffed-links.jpg)

*Search results for the account in the group: 31 messages, the oldest shown dated December 9, 2024, most linking to the Chuffed campaigns. Source: Telegram, captured October 20, 2026.*

The same screenshots capture his profile, and here the militant imagery is plain. Telegram’s own panel says Ashraf set an emoji from “Resistance-Toast :: @fStikBot” as his current status. The emoji is a masked fighter, his face wrapped in a red-and-white keffiyeh, a Palestinian flag on his sleeve and one finger raised, ringed by stars. It is a clear nod to [Abu Obeida](https://today.lorientlejour.com/article/1362943/abou-obeida-palestinian-refugees-new-resistance-icon-in-lebanon.html), the masked spokesman of Hamas’s armed wing, the al-Qassam Brigades, whose statements, delivered with his face wrapped in a red keffiyeh and his index finger pointed skyward, made him the brigades’ most recognizable figure. Telegram labels emoji status a premium feature. Its public page for the set says only that “a Telegram user” created it.

![Telegram emoji status panel showing a masked fighter in a red-and-white keffiyeh face covering with a Palestinian flag on his sleeve, raising an index finger, surrounded by stars, above the text Ashraf set this emoji from Resistance-Toast :: @fStikBot as their current status](https://www.octoprobe.ai/blog/crowdfunding-hamas-chuffed-gofundme-gaza/assets/telegram-ashraf-resistance-toast-al-qassam-emoji-status.jpg)

*The status Telegram attributes to Ashraf: a masked fighter from the “Resistance-Toast” emoji set. Source: Telegram, captured October 20, 2026.*

A Telegram channel carries the same name: “Resistance Toast🔻[Cyber Army].” It had about 17,650 subscribers on October 20, 2026. Its description steers readers into a group chat named for al-Qassam, Hamas’s armed wing: “Al-Qassam Toast [Cyber Army],” which listed 3,536 members. The channel signs its posts with a red inverted triangle.

![Four Telegram public pages in a grid: 1, the profile card for Ashraf at @Ashrafgaza; 2, the Resistance-Toast emoji set page; 3, the Resistance Toast Cyber Army channel card with 17,650 subscribers and a description inviting readers to the Al Qassam Toast chat; 4, the Al-Qassam Toast Cyber Army chat card with 3,536 members](https://www.octoprobe.ai/blog/crowdfunding-hamas-chuffed-gofundme-gaza/assets/telegram-status-chain-al-qassam-chat.jpg)

*From status badge to chat: (1) the @Ashrafgaza profile; (2) the “Resistance-Toast” emoji set used as his status; (3) the channel of the same name; (4) the chat its description promotes. Source: Telegram public pages, captured October 20, 2026.*

That triangle has a history. The Anti-Defamation League says the symbol “[first appeared in propaganda videos from the al-Qassam Brigades, Hamas’s military wing, marking Israeli military targets with inverted red triangles](https://www.adl.org/resources/backgrounder/symbol-inverted-red-triangle#:~:text=first%20appeared%20in%20propaganda%20videos).” The ADL also cautions that “[context must be considered](https://www.adl.org/resources/backgrounder/symbol-inverted-red-triangle#:~:text=Context%20must%20be%20considered)” because some users treat it as a general symbol of support for Palestine.

## What the Record Shows, and What It Doesn’t

A status badge is a signal, not a membership card. No public record reviewed for this report ties Ashraf to Hamas operations, and both campaigns describe food, water, medicine, and shelter. The record also cannot say where the $12,948 and $6,736 went after they reached the organizers.

What the record does show is the pattern U.S. officials warn about. “[Hamas has exploited the suffering in Gaza to solicit funds through sham and front charities that falsely claim to help civilians in Gaza](https://home.treasury.gov/news/press-releases/jy2632#:~:text=Hamas%20has%20exploited%20the%20suffering%20in%20Gaza),” the Treasury Department said in October 2024. “[As of early 2024, Hamas may have received as much as $10 million a month through such donations](https://home.treasury.gov/news/press-releases/jy2632#:~:text=As%20of%20early%202024).”

The group has also asked for money online in the open. In 2020 the Justice Department said the al-Qassam Brigades posted calls for bitcoin donations and “[boasted that bitcoin donations were untraceable and would be used for violent causes](https://www.justice.gov/archives/opa/pr/global-disruption-three-terror-finance-cyber-enabled-campaigns#:~:text=boasted%20that%20bitcoin%20donations%20were%20untraceable).” Federal agents seized 150 cryptocurrency accounts tied to the campaign.

## The Conversion Cycle

Crowdfunding runs on ordinary money. Hamas asks for cryptocurrency. The step that joins the two is conversion, when dollars paid out to an organizer are handed to a go-between, such as a friend, a money transfer office, or an exchange, and turned into digital tokens. After that step, a gift raised for food in Gaza looks like any other entry on a blockchain.

GoFundMe bans the step outright. Its terms require organizers “[Not to convert funds raised through the Platform into cryptocurrency for the purposes of delivering those funds to its intended recipients](https://www.gofundme.com/c/terms#:~:text=Not%20to%20convert%20funds%20raised%20through%20the%20Platform%20into%20cryptocurrency)” and add that “[All funds must be withdrawn and delivered in fiat currency](https://www.gofundme.com/c/terms#:~:text=All%20funds%20must%20be%20withdrawn%20and%20delivered%20in%20fiat%20currency).” Chuffed’s terms say nothing about cryptocurrency. The U.S. organizer of the 2025 Ashraf page named a crypto wallet as one likely route.

On the Gaza end, crypto is one of the few ways left to get cash. Al Jazeera reported in June 2025 that with no banking services left in the territory, residents rely on exchange offices and “[the option to swap cryptocurrency for physical currency](https://www.aljazeera.com/news/2025/6/26/as-gaza-starves-gofundme-accused-of-blocking-millions-of-dollars-raised#:~:text=the%20option%20to%20swap%20cryptocurrency%20for%20physical%20currency).” No record reviewed for this report shows that money from either Ashraf campaign took that route or reached Hamas.

Hamas has written its own instructions for the conversion step. In a 2026 affidavit, an FBI agent quoted an email that a confidential source received in February 2025 from fund[@]alqass██.██, an address the FBI ties to the al-Qassam Brigades. In the FBI’s rough translation, it told donors with no crypto experience that they could “[seek the help of a friend inside or outside your country, or go to a money transfer office or exchange in your country that has digital currencies, and show only the wallet information from this message](https://www.justice.gov/opa/media/1459811/dl?inline#page=25).” It added that “[it is necessary not to inform the party that will undertake the transfer on your behalf of our identity](https://www.justice.gov/opa/media/1459811/dl?inline#page=25).”

The email supplied a USDT stablecoin address on the TRON network and warned that “[the address is only valid for one transfer and support process](https://www.justice.gov/opa/media/1459811/dl?inline#page=26).” The agent assessed that the network had been running since about October 2024 and had “[received over $3,000,000 in donations through in or around November 2025](https://www.justice.gov/opa/media/1459811/dl?inline#page=27).” As recently as February 2026, the agent wrote, the address was still emailing FBI sources instructions on how to donate.

### Following the Stablecoins

An earlier affidavit, filed with a March 25, 2025, application to seize USDT held by Tether, traces where the donations went. Of 25,211 USDT sent to the first address an FBI source received, 23,618 USDT moved directly to a wallet the agent called the “[al-Qassam Brigades Operational Wallet](https://www.justice.gov/opa/media/1459791/dl?inline#page=30).” That wallet took in about 1,349,725 USDT between October 28, 2024, and March 3, 2025, according to the filing.

A second source emailed the same address and received seven more donation addresses. Together they took in about 45,948 USDT between February 14 and February 28, 2025. All seven paid their transaction fees from one shared “[Gas Wallet](https://www.justice.gov/opa/media/1459791/dl?inline#page=33),” which the agent wrote marks them as controlled by the same actor. The agent estimated that the operational wallet “[receives an average of approximately 75,000 USDT per week that is subsequently sent to finance terrorism](https://www.justice.gov/opa/media/1459791/dl?inline#page=37).”

![Paragraph 63 of an FBI agent’s affidavit stating that on February 17, 2025, a confidential human source called CHS-2 received seven additional USDT donation addresses by emailing fund[@]alqass██.██, followed by the seven TRON addresses, Target Properties 2, 3, and 14 through 18](https://www.octoprobe.ai/blog/crowdfunding-hamas-chuffed-gofundme-gaza/assets/doj-affidavit-chs2-seven-usdt-addresses.jpg)

*Paragraph 63 of the FBI affidavit lists the seven addresses a second source received. OctoProbe masked the end of the al-Qassam domain. Source: [U.S. Department of Justice](https://www.justice.gov/opa/media/1459791/dl?inline#page=35).*

From there the trail runs back toward cash. The agent described internal “[book transfers](https://www.justice.gov/opa/media/1459791/dl?inline#page=31)” between accounts at the same exchange, which leave no public blockchain record, and payments to a Turkish exchange. The agent wrote that regional over-the-counter brokers “[can be used to obfuscate the flow of funds and swap virtual currency into government-issued fiat currency](https://www.justice.gov/opa/media/1459791/dl?inline#page=32).” Tether froze the USDT in all 18 Tether addresses named in the application at the U.S. government’s request.

These are the wallets an OctoProbe investigation of the fund[@]alqass██.██ address logged from the two filings, with the three additional addresses from paragraph 63:

| USDT address (TRON) | Role in the DOJ filings | In OctoProbe graph |
|---|---|---|
| `TSWL3euRjZWXiFJgzuV9tYAGiwShtPWkZK` | Donation Address 1, sent to the first FBI source in February 2025 | Yes |
| `TA3aQxRwocYytqZBKqMPHPZT6pYvwGjLg1` | Operational wallet, the network’s main consolidation point (Target Property 13) | Yes |
| `TVp7a1r4FGNgWE2ViskhcfVYxbyZRvpvmv` | Sent to the second source (Target Property 2) | No |
| `TB6PG69uKdN6NJirx8PnV7mJMVh4XRZvzp` | Sent to the second source (Target Property 3) | Yes |
| `THeKAQbUnV58Hnt8WxwwXaC4EjzTquoVes` | Sent to the second source (Target Property 14) | Yes |
| `TL4MeyPRooqL9UhCiqAHww7u2pNYs6guJS` | Sent to the second source (Target Property 15) | Yes |
| `TSxBp5UrV7HDp7Zu5EJc1ijDWGWhwsfBFK` | Sent to the second source (Target Property 16) | No |
| `TTzRqud2nVZJUSahxspmqjTHZKmfj3d9Uc` | Sent to the second source (Target Property 17) | Yes |
| `TX8VZHoXwwGDvL75m7cZee1gyipac3p5PQ` | Sent to the second source (Target Property 18) | No |
| `TDyyV8bkNNfttzk3NvjGvLFobsGdYmig9J` | Sent to a third source (Target Property 4) | Yes |
| `TQaNC6oaN8TVtvbVv7vDZUAhPZrfuP76Vp` | Named for seizure (Target Property 5) | Yes |
| `TGmLbZiS4SAhxDwmQteQ2fhsKJQ7VfJLsv` | Named for seizure (Target Property 12) | Yes |

> Every address above passes the TRON checksum. OctoProbe masks the final quarter of the al-Qassam Brigades’ web domain in text and images.

## A Pattern Across Platforms

The two Ashraf pages are a small slice of a large market. In August 2025, the *i* Paper reported that Chuffed “[has nearly 10,000 individual campaign pages for Gazans](https://inews.co.uk/news/how-online-scammers-stole-gazan-doctors-identity-trick-people-cash-3867883#:~:text=has%20nearly%2010%2C000%20individual%20campaign%20pages%20for%20Gazans).” The paper found one of them used a real Gaza doctor’s stolen photos. Chuffed removed it after the paper asked. The company told the paper that a campaign found to be fraudulent “[will be redacted and the campaigner banned from our platform](https://inews.co.uk/news/how-online-scammers-stole-gazan-doctors-identity-trick-people-cash-3867883#:~:text=will%20be%20redacted%20and%20the%20campaigner%20banned).”

In March 2026, the *Telegraph* [reported](https://www.telegraph.co.uk/news/2026/03/21/social-justice-charity-hosting-fundraisers-for-anti-semites/) that Chuffed was hosting fundraisers for people accused of supporting Hamas, among them a suspended National Health Service doctor under police investigation who had raised more than £44,000.

GoFundMe faces the same problem. The *Jerusalem Post* reported in September 2025 that volunteer researchers tied a Gaza cleric’s €500,000 GoFundMe appeal to a member of a Hamas-affiliated preachers’ forum and found footage of a recruiter urging Gazan youth to become “[Soldiers of the next October 7](https://www.jpost.com/israel-news/defense-news/article-866181).” GoFundMe froze the campaign within 36 hours, the paper reported. Writer Eitan Fischberger reported on his Substack in May 2025 that a Gaza doctor who honored relatives in the al-Qassam Brigades had raised more than $40,000 on GoFundMe, and that Western platforms “[are ill-equipped to stop it](https://www.fischfiles.com/p/the-gaza-grift-meet-dr-hamza-al-sharif#:~:text=are%20ill-equipped%20to%20stop%20it).”

The money involved is large. GoFundMe told Al Jazeera it “[has helped raise and deliver over $300m from donors in more than 215 countries and jurisdictions to support individuals and organisations helping those in both Gaza and Israel](https://www.aljazeera.com/news/2025/6/26/as-gaza-starves-gofundme-accused-of-blocking-millions-of-dollars-raised#:~:text=has%20helped%20raise%20and%20deliver%20over).” Charity leaders and activists quoted in the same report accused the company of shutting down or freezing Gaza fundraisers.

## The Rules on Paper

GoFundMe’s terms prohibit “[any activity in support of terrorism, terrorist financing, extremist financing, or money laundering](https://www.gofundme.com/c/terms#:~:text=any%20activity%20in%20support%20of%20terrorism).” Its guidance on the Israel–Gaza war adds, “[Fundraising to support any armed conflict efforts is not allowed, regardless of the country](https://www.gofundme.com/c/blog/fundraise-in-response-to-the-hamas-attacks-and-impacted-civilians-in-gaza-and-israel#:~:text=Fundraising%20to%20support%20any%20armed%20conflict).”

Chuffed’s terms are vaguer. The site is run by Chuffed.org Pty Ltd under the laws of New South Wales, Australia. Its terms, last updated November 11, 2025, never use the word “terrorism.” They bar content that “[breaches applicable laws, regulations or relevant industry codes, or is otherwise unlawful](https://chuffed.org/terms-conditions#:~:text=breaches%20applicable%20laws).” Donations on both Ashraf pages are processed by Stripe and PayPal, according to the pages themselves.

## How This Story Was Reported

An OctoProbe investigation began with two identifiers and grew over four rounds to 33 nodes and 41 links. It connected the campaign pages, the Telegram account, nine images uploaded by the analyst, and contact points for one organizer. Reporters then captured both campaign pages and the public Telegram pages on October 20, 2026, and compared the campaigns’ lead photo with the Telegram profile photo by eye. They match.

> The organizers are private individuals and are not named here. Their contact details surfaced in the investigation and are withheld.

## Frequently Asked Questions

### Is it illegal to give to a Gaza crowdfunding campaign?

Not in itself. Federal law makes it a crime to knowingly provide material support or resources to a designated Foreign Terrorist Organization such as Hamas, and the Treasury Department has warned that Hamas raises money through sham charities that claim to help civilians in Gaza. Donors to individual appeals usually cannot see where the money goes after the organizer receives it.

### Does Chuffed allow fundraising for people in Gaza?

Yes. The i Paper reported in August 2025 that Chuffed hosted nearly 10,000 campaign pages for Gazans. Chuffed’s terms bar content that breaches applicable laws but, unlike GoFundMe’s, do not mention terrorism or terrorist financing.

### Does GoFundMe ban terrorist financing?

Yes. GoFundMe’s terms prohibit any activity in support of terrorism, terrorist financing, extremist financing, or money laundering, and its Israel–Gaza guidance says fundraising for any armed conflict is not allowed. GoFundMe also places Gaza-related fundraisers under review.

### What does the red inverted triangle emoji mean?

The Anti-Defamation League says the inverted red triangle first appeared in propaganda videos from the al-Qassam Brigades, Hamas’s military wing, which used it to mark Israeli targets, and that it has come to represent Hamas itself. The ADL adds that context matters, because some users treat it as a general symbol of support for Palestine.

### How does Hamas collect cryptocurrency donations?

According to FBI affidavits filed in federal court in Washington, D.C., in 2025 and 2026, the al-Qassam Brigades answered donors who emailed its fundraising address with a fresh USDT address on the TRON network for each transfer. Most of the money was swept into a single consolidation wallet and then moved through exchange accounts and over-the-counter brokers that can swap it for cash. Tether froze the USDT in 18 of those addresses at the U.S. government’s request in March 2025.

### How does money from a Chuffed campaign reach Gaza?

Chuffed’s terms say PayPal and Stripe donations are paid to the campaign organizer’s PayPal or Stripe account at or around the time of the donation. What happens next is up to the organizer; the terms do not describe any onward transfer.

## Disclaimer

This report relies on public crowdfunding pages, public Telegram pages, government records and court filings, platform terms, and published journalism, together with screenshots gathered in an OctoProbe investigation.

## Related Reading

- [Jailed, Purged, Still Shipping: How ISIS Media Survives the Takedowns](https://www.octoprobe.ai/blog/isis-media-survives-takedowns/)
- [North Korea’s Fake IT Workers: Thin Covers, Borrowed Lives](https://www.octoprobe.ai/blog/north-korea-it-worker-personas-backstopping/)
- [DHS Lawyers Wrote 24 Pages on Buying Your Phone’s Location Data. They Withheld Every Page of the Analysis.](https://www.octoprobe.ai/blog/dhs-phone-location-data-legal-opinion-foia/)
