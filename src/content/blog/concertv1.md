---
title: "Concert Website v1 – Real-Time Performer Display"
date: 2025-07-15 
description: "How I built a real-time concert display system for my neighbor’s student concert using HTML, JS, and Supabase."
readTime: "3 min read"
tags: ["Archive","Web", "Realtime", "Supabase", "Project"]
---



My neighbor is a piano & violin teacher who organizes student concerts, and I thought it would be really cool if the audience could see *live* who's currently performing and what piece they're playing.

So I built a concert website to make that happen.

---

## 💡 The Idea

The goal:  
- Show the performer's name  
- Show the piece they’re playing  
- Update this info live without reloading the page

---

## 🛠️ The Stack

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Supabase  
- **Realtime:** Supabase’s Realtime API (Postgres-based)  
- **Data Format:** JSON list of performers and pieces

---

## 🔄 How It Works

- A JSON file stores the concert program.
- A minimal control panel (private) allows selecting who's on stage.
- This updates the Supabase DB, which triggers the Realtime API.
- The frontend listens for these changes and updates the display instantly.

```json
{
  "name": "Ada Yılmaz",
  "piece": "Beethoven - Für Elise"
}
````

No need for refreshing. It just works.

---

## 🚧 Challenges

* **Privacy:** Since this involves kids, the live site isn’t public.
* **Stability:** Needed to debounce updates to avoid flickering and accidental data changes mid-performance.

---

## ✅ Outcome

It worked beautifully!
The audience could follow along, the teacher loved the clarity, and I got hands-on experience building a small but powerful real-time system. 🧠

---

## 🔗 Source Code

[GitHub Repo](https://github.com/smartlizardpy/konser)



