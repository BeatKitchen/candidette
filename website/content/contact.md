---
title: "It takes courage to run for office."
description: "YOU'VE GOT IT."
hideAuthor: true
---

<style>
.post-header h1 { font-size: 1.75rem; }
.post-description { color: #E0408A; font-weight: 700; font-size: 1.75rem; }
</style>

<form name="contact" method="POST" data-netlify="true" class="contact-form">
  <input type="hidden" name="form-name" value="contact" />

  <div class="form-group">
    <label for="name">Your name</label>
    <input type="text" id="name" name="name" required placeholder="First and last name" />
  </div>

  <div class="form-group">
    <label for="email">Email</label>
    <input type="email" id="email" name="email" required placeholder="you@email.com" />
  </div>

  <div class="form-group">
    <label for="phone">Phone (optional)</label>
    <input type="tel" id="phone" name="phone" placeholder="(555) 555-5555" />
  </div>

  <div class="form-group">
    <label for="race">Tell me about your race</label>
    <textarea id="race" name="race" required placeholder="What office are you running for? What level — city council, county, state legislature? Where? And what's drawing you to run?"></textarea>
  </div>

  <button type="submit" class="btn btn-primary">SEND</button>
</form>
