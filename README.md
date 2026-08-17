VAT Identifier Discovery

Can a UK company VAT dataset be built from the open web? vat_identifier_discovery.ipynb is the full writeup: research, a proof of concept run on a real sample, and what changes with real resources. Everything in it is either code that ran or a source I checked by hand; nothing below is guessed.

Start there for the actual work. This file covers the four debate questions from the brief, plus the Germany comparison, taken directly from Part 3 of the notebook.

Debate topics

Could you just brute-force the checksum against HMRC's checker? The math: about 20 million valid numbers exist in total (Part 1), against ~2.18 million real ones. Generating all 20 million is trivial, and checking each against HMRC takes about 80 days at their documented rate. Bad idea anyway. Legally: HMRC has already refused Freedom-of-Information requests for exactly this list (1.7), it's protected by law, and their own compliance monitoring can pull your access for exactly this kind of usage pattern. Practically: get flagged, and you lose the same credential you need to verify the customer's real 40,000 suppliers, so this doesn't just fail, it can break the part that already works. To be fair to an earlier version of this argument: matching 2 million HMRC names against 4 million Companies House names in bulk is a normal, solvable data problem, actually easier than doing it one company at a time the way Part 2 did. That half of the old objection was weaker than it should have been. The real reason to say no is the legal one, not the matching one.

How would you keep it current? Companies House's free live feed catches new and closed companies as they happen. For a website's content going stale (a number changing, a VAT registration getting cancelled) there's no equivalent feed, HMRC doesn't publish deregistrations any more than it publishes a forward register. Has to be handled with a re-check schedule instead: recently-invoiced suppliers checked often, everyone else occasionally.

How would you know the dataset is wrong at scale, with nothing complete to check against? Spot-check a random sample against HMRC on a schedule. Let the customer's own invoice-matching failures flag wrong numbers, a lagging but real signal. Treat two independent sources agreeing (like Endole in Part 2) as a weak positive, not proof, since they might share the same root source. And two free internal checks that need no external call at all: does the checksum scheme (older vs newer rule) fit how old the company is, and if a company also has a findable EORI, does it encode the same VAT number found another way.

Which sources wouldn't you sell? Third-party VAT lookup sites: no visibility into where their numbers actually came from, and their own terms probably don't license reselling anyway. Same answer, same reason, for the brute-force idea above. Companies House itself is fine: it's published under a licence written specifically to allow this kind of reuse, including commercial.

Beyond the UK: Germany

Not the same problem, almost the opposite one.

Easier in Germany: finding the number. German law (Impressumspflicht) requires almost every business website, not just online shops, to publish a legal-notice page that includes the VAT number if the company has one. It's actually enforced too: competitors send formal warning letters over a missing one, with real legal fees attached. So once you have the website, the number is much easier to find than in the UK.

Harder in Germany: building the starting list. The UK's Companies House gives one free national file. Germany's equivalent (Handelsregister) is split across roughly 150 local courts, has no bulk download, and is capped at 60 lookups an hour by its own rules, a limit backed by the threat of criminal charges for automated mass querying under German law.

Verifying, once found: also easier in Germany right now. VIES, the EU-wide checker, needs no registration at all, unlike HMRC's now-locked-down API, though it's less predictable (occasional per-country outages, no published rate limit, just an informal guideline).

So: the funnel logic (shape, context, checksum-equivalent, verify-and-match) survives the move basically unchanged. What has to be rebuilt completely is the sourcing layer underneath it, since Germany has nothing like the UK's free, unified, bulk company file.
