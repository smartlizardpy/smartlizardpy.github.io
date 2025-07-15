# Ozan's Personal Website 🚀

> **Devlog Entry #1** - Building a 13-year-old's dream website

## 🎯 Project Overview

Building a modern, fast, and fun personal website for Ozan - a 13-year-old developer who's already building projects with Vue.js, JavaScript, and Python. This isn't your typical "kid's website" - it's a serious portfolio that happens to be built by someone who's 13!

## 🛠️ Tech Stack Decisions

### Why Astro?
- **Island Architecture**: Perfect for speed + interactivity
- **MDX Support**: Great for blog posts with code highlighting
- **Zero JS by default**: Fast loading, then add interactivity where needed
- **Easy deployment**: Works great with Vercel/Netlify

### Why Tailwind CSS?
- **Rapid prototyping**: Perfect for a 13-year-old who wants to iterate quickly
- **Consistent design**: No more "what color should this be?" decisions
- **Responsive by default**: Mobile-first approach

### Why JSON over databases?
- **Free forever**: No hosting costs for data
- **Simple to edit**: Ozan can update projects without touching code
- **Git-friendly**: Version control for all content
- **No setup complexity**: Just edit files and deploy

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Header.astro    # Navigation with dark mode toggle
│   ├── ProjectCard.astro # Animated project cards
│   ├── PhotoGallery.astro # Responsive image grid
│   └── DrumKit.astro   # Interactive drum kit
├── layouts/            # Page layouts
│   ├── BaseLayout.astro # Main layout with meta tags
│   └── BlogLayout.astro # Blog post layout
├── pages/              # Astro routes
│   ├── index.astro     # Homepage
│   ├── projects.astro  # Projects showcase
│   ├── photography.astro # Photo gallery
│   ├── drumming.astro  # Drumming section
│   ├── blog/           # MDX blog posts
│   ├── secret.astro    # Easter egg page
│   └── 404.astro       # Custom 404
├── data/               # JSON content
│   ├── projects.json   # Project portfolio
│   ├── photos.json     # Photography metadata
│   └── blog-posts.json # Blog post metadata
└── styles/             # Global styles
    └── global.css      # Custom CSS + animations
```

## 🎮 Planned Features

### Core Pages
- [x] **Homepage**: Hero section, quick intro, animated elements
- [ ] **Projects**: Card grid with VEX IQ, BilBots, Concert site
- [ ] **Photography**: Image gallery with Nikon D3300 shots
- [ ] **Drumming**: Metal drumming showcase with interactive kit
- [ ] **Blog**: MDX posts with syntax highlighting

### Easter Eggs & Fun Stuff
- [ ] **Konami Code**: "Ozan OS mode" boot animation
- [ ] **Hidden click zones**: Secret messages and pages
- [ ] **Juicebox Mode**: Random styling chaos
- [ ] **Focus Test**: Minigame on /study page
- [ ] **Drum Kit**: Keyboard-controlled drum sounds
- [ ] **"I'm Bored" Button**: Random fun features

### Technical Features
- [ ] **Dark/Light Mode**: Smooth theme switching
- [ ] **Animations**: GSAP + Framer Motion integration
- [ ] **Responsive Design**: Mobile-first approach
- [ ] **Performance**: Lighthouse 100 scores
- [ ] **SEO**: Meta tags, structured data

## 🚀 Development Log

### Day 1: Project Setup
- ✅ Initialized Astro project with minimal template
- ✅ Added Tailwind CSS integration
- ✅ Set up MDX for blog posts
- ✅ Created project structure
- ✅ Planned JSON data architecture
- ✅ Built stunning homepage with hero section and animations
- ✅ Created modern header with dark mode toggle
- ✅ Built interactive project cards with hover effects
- ✅ Created projects page with filtering and search
- ✅ Built photography page with image grid
- ✅ Created drumming page with interactive drum kit
- ✅ Built blog page with sample posts
- ✅ Created fun 404 page with animations
- ✅ Added GSAP animations throughout
- ✅ Implemented responsive design for all pages

### Next Steps
1. **Add Real Content**: Replace placeholder data with actual projects and photos
2. **Easter Eggs**: Implement Konami code and hidden features
3. **Performance**: Optimize images and add lazy loading
4. **SEO**: Add structured data and meta tags
5. **Deploy**: Set up hosting and domain

## 🎨 Design Philosophy

**"Wait, you're 13??"** - That's the reaction we want visitors to have. The site should be:
- **Professional**: Clean, modern, fast
- **Playful**: Easter eggs, animations, personality
- **Impressive**: Show off real technical skills
- **Accessible**: Works for everyone, including screen readers

## 📊 Performance Goals

- **Lighthouse Score**: 100/100 across all metrics
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1
- **First Input Delay**: < 100ms

## 🎯 Success Metrics

- [ ] Site loads in under 2 seconds
- [ ] All easter eggs work perfectly
- [ ] Mobile experience is smooth
- [ ] Blog posts render beautifully
- [ ] Projects showcase impresses visitors

---

*"Building websites is like building with LEGO - you start with blocks and end up with something amazing." - Ozan, probably*

---

## 🧞 Commands

| Command                   | Action                                           |
| :------------------------ | :----------------------------------------------- |
| `npm install`             | Installs dependencies                            |
| `npm run dev`             | Starts local dev server at `localhost:4321`      |
| `npm run build`           | Build your production site to `./dist/`          |
| `npm run preview`         | Preview your build locally, before deploying     |
