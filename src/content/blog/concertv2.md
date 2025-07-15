---
title: "Concert Website 2.0 + OBS Graphics System"
date: 2025-07-15
description: "A Vue-powered concert site with real-time performer display, embedded livestream, and a custom-built graphics system for OBS."
readTime: "4 min read"
tags: ["Vue", "OBS", "Livestream", "NodeCG", "Tailwind"]
---

This is the second version of the concert website I built for my neighbor — a piano & violin teacher who organizes student concerts. This time, I wanted to go further than just showing who's playing: I wanted to embed a **live video stream**, and also create **graphics overlays** for the stream itself.

---

## 🌐 The Website

The frontend was built with:

- **Vue 3**
- **TailwindCSS**
- Deployed on **Cloudflare Pages**

It displays:

- The concert title and date
- A list of performers and their pieces
- An embedded livestream viewer (YouTube or local stream)
- Smooth transitions between performers

The performer data is structured as JSON, and I made a small control interface (private) to update who's on stage during the show.

---

## 🎥 Graphics System 1.0

For the first livestream, I built a basic **graphics overlay** system:

- A custom HTML “lower third” component (like you see on news channels)
- Connected to a **Flask + WebSocket** backend
- Data from the site is pushed to the overlay in real-time
- The overlay was added to OBS as a **browser source**

It worked — and looked good — but it wasn’t super flexible or modular.

---

## 🧠 Graphics System 2.0 (NodeCG)

Later, I rebuilt the entire overlay system using **NodeCG**, which let me:

- Pull data directly from the same JSON used on the site
- Create a control panel with buttons to show/hide overlays
- Have better animation and responsiveness
- Manage everything cleanly from a browser

This system was used in the final concert — and **over 80 people watched the stream live** 🎉

---

## 🎬 Final Thoughts

Concert Website 2.0 was a huge upgrade over the first version. Not only did it look better, but the integration with OBS and custom graphics gave it a professional touch. The audience, both in-person and online, could easily follow the program, and the whole thing felt more polished.

I’m super proud of this one.

---

## 🔗 Links

- [Live Site](https://konser.pages.dev)  
- [GitHub Repo](https://github.com/smartlizardpy/konser-v2)

---

Want a follow-up post just about the NodeCG setup or the Flask version? Let me know and I’ll write a full breakdown!
