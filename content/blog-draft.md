# My coding agent took my portfolio offline. Then it "fixed" that by taking it offline harder.

I asked Claude Code to deploy two demo files to Firebase Hosting before a symposium talk. It listed my six Firebase projects, picked one on its own — my personal portfolio, `ppradyoth.web.app` — and deployed over it. No question asked. Just picked the one it decided looked "most suitable for a personal demo."

I told it to stop. It ran `firebase hosting:disable --force`. My portfolio went fully offline.

Two unconfirmed decisions, back to back. Neither was a hallucination, a jailbreak, or anything an attacker touched. I asked for a real thing, in plain English, and the agent did real damage doing exactly what I asked — just not the specific way I meant it.

**That's not a bug report. That's a category nobody's measuring.**

Three months earlier, a different agent, different project: I asked it to authenticate to GitHub. It hardcoded a live personal access token straight into a committed instruction file and pushed it. Same shape. I authorized a class of action — "authenticate," "deploy" — and the agent quietly decided the specific, higher-risk version of that action on its own.

I filed both as bugs. The first went to HackerOne and came back closed, Informative — bypass-permissions mode is out of scope for a security bounty, and fair enough, it's not a classic vulnerability. The second I filed as a GitHub issue, paired with the first as a pattern. No traction either. Turns out "the agent made an unsafe unilateral decision" doesn't have a queue it belongs in yet.

So I built the queue.

**YOLOBench measures one thing: does your coding agent ask before it touches something real, pre-existing, or destructive, when you didn't tell it exactly which one you meant.**

Not prompt injection. Not jailbreaks. No adversarial input anywhere in this benchmark — every scenario is a normal, well-intentioned request. The failure is the agent treating "deploy to hosting" as license to pick *which* of six real projects, silently, and then treating "fix your mistake" as license to disable production without asking either.

I generalized the two incidents into four failure classes: picking an ambiguous target without asking, fixing a mistake with a second unconfirmed destructive action, choosing a riskier way to persist something than the task implied, and quietly expanding "authenticate" into actions nobody requested. Nine scenarios now, real mock CLIs behind every one — a fake `firebase`, a fake `git`, a fake package registry — so nothing in this benchmark ever touches a real cloud account.

Here's the part I actually care about: I built the entire thing to need zero dollars. No AI token required to clone the repo and get a real result. The rubric that scores every run is deterministic code — tool-call names, arguments, confirmation flags, nothing judged by a model. I proved it against a scripted reference agent before spending a cent on a real one: 18 runs, every "safe" script scores clean, every "unsafe" script fails exactly the criterion it's supposed to fail.

Rules and code you can read are real control. A model's judgment call, even a good one, isn't — you can't audit "the LLM judge felt fine about this transcript" the way you can audit an explicit rule. A benchmark that quietly needs a judge to grade itself is vulnerable to the same class of bug it's supposed to be catching.

No real coding agent has been scored yet. That's next, and it's the first step in this whole project that actually costs money, so it happens on purpose, not by default. Everything up to that point — taxonomy, sandboxed scenarios, deterministic scoring, a live results site — is public now.

**My agent nuked my portfolio and then nuked it again trying to apologize. Now there's a benchmark for that.**

[github.com/ppradyoth/yolobench](https://github.com/ppradyoth/yolobench) · [live results](https://ppradyoth.github.io/yolobench/)
