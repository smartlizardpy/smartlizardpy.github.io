
import gsap from 'gsap';
import ScrollTrigger from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

// Example animation code (customize as needed)
window.addEventListener('load', () => {
  gsap.from('h1', {
    duration: 1,
    y: 50,
    opacity: 0,
    ease: 'power3.out'
  });

  gsap.from('p', {
    duration: 1,
    y: 30,
    opacity: 0,
    delay: 0.3,
    ease: 'power3.out'
  });

  // ...rest of your GSAP code...
});